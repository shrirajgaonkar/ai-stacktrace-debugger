from fastapi import FastAPI, Depends, Request, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from app.config import settings
from app.auth.github_oauth import router as auth_router
from app.auth.deps import get_current_user
from app.db import get_db
from app.models import User, Session, SessionComment
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sse_starlette.sse import EventSourceResponse
import asyncio

# Need celery task import (will be implemented in later parts)
from app.workers.tasks import process_session_task

app = FastAPI(title="StackTrace AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth/github", tags=["auth"])

@app.get("/api/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "github_login": current_user.github_login,
        "avatar_url": current_user.avatar_url
    }

class SessionCreate(BaseModel):
    title: Optional[str] = None
    raw_log: str
    tags: Optional[List[str]] = []

@app.post("/api/sessions")
async def create_session(
    file: Optional[UploadFile] = File(None),
    title: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    json_data: Optional[SessionCreate] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    raw_log_content = ""
    session_title = title
    session_tags = []
    
    if file:
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large")
        # sanitize null bytes
        raw_log_content = content.decode('utf-8', errors='ignore').replace('\x00', '')
        if tags:
            session_tags = [t.strip() for t in tags.split(",")]
        if not title:
            session_title = file.filename
    elif json_data:
        raw_log_content = json_data.raw_log.replace('\x00', '')
        session_title = json_data.title or "Untitled Session"
        session_tags = json_data.tags or []
    else:
        raise HTTPException(status_code=400, detail="Must provide either file or JSON body")

    new_session = Session(
        user_id=current_user.id,
        title=session_title,
        status="queued",
        raw_log=raw_log_content,
        tags=session_tags
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    # Enqueue Celery task
    process_session_task.delay(str(new_session.id))
    
    return {"session_id": str(new_session.id), "status": "queued"}

@app.get("/api/sessions")
async def list_sessions(
    status: Optional[str] = None,
    tag: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Session).where(Session.user_id == current_user.id).order_by(Session.created_at.desc())
    if status:
        query = query.where(Session.status == status)
    if tag:
        query = query.where(Session.tags.contains([tag]))
        
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return {
        "items": [{
            "id": str(i.id),
            "title": i.title,
            "status": i.status,
            "created_at": i.created_at,
            "updated_at": i.updated_at,
            "tags": i.tags
        } for i in items],
        "page": page,
        "page_size": page_size,
        "total": total
    }

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Session).where(Session.id == session_id, Session.user_id == current_user.id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

class CommentCreate(BaseModel):
    text: str

@app.post("/api/sessions/{session_id}/comment")
async def add_comment(session_id: str, data: CommentCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    comment = SessionComment(session_id=session_id, user_id=current_user.id, text=data.text)
    db.add(comment)
    await db.commit()
    return {"ok": True}

class ResolveCreate(BaseModel):
    github_issue_url: Optional[str] = None

@app.post("/api/sessions/{session_id}/resolve")
async def resolve_session(session_id: str, data: ResolveCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Session).where(Session.id == session_id, Session.user_id == current_user.id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.resolved_at = func.now()
    session.github_issue_url = data.github_issue_url
    await db.commit()
    return {"ok": True}

@app.get("/api/sessions/{session_id}/status")
async def get_session_status(session_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Session).where(Session.id == session_id, Session.user_id == current_user.id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": session.status, "updated_at": session.updated_at}

@app.get("/api/sse/sessions/{session_id}")
async def sse_session_status(session_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    async def event_generator():
        last_status = None
        while True:
            # Reattach session in standard sync logic or use fresh connection
            async with db.bind.connect() as conn:
                # Lightweight polling for SSE
                result = await db.execute(select(Session.status, Session.updated_at).where(Session.id == session_id))
                row = result.first()
                if row:
                    status, updated_at = row
                    if status != last_status:
                        yield {"event": "status", "data": f'{{"status": "{status}", "updated_at": "{updated_at}"}}'}
                        last_status = status
                    if status in ["completed", "failed"]:
                        break
            await asyncio.sleep(2)
    return EventSourceResponse(event_generator())
