import asyncio
from typing import Optional
from app.workers.celery_app import celery_app
from app.db import AsyncSessionLocal
from app.services.session_service import process_session

async def async_process_session(session_id: str):
    async with AsyncSessionLocal() as db:
        await process_session(session_id, db)

@celery_app.task(bind=True, max_retries=3)
def process_session_task(self, session_id: str):
    """
    Background job to parse logs, match patterns, and call LLMs.
    """
    try:
        # Run async logic in a sync celery wrapper
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(async_process_session(session_id))
    return {"status": "success", "session_id": session_id}
