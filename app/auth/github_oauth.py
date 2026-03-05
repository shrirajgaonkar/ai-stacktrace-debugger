import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from app.config import settings
from app.db import get_db
from app.models import User
from app.auth.jwt import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

@router.get("/login")
async def github_login():
    url = f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.GITHUB_CALLBACK_URL}&scope=read:user"
    return {"url": url}

@router.get("/callback")
async def github_callback(code: str, db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        # Get access token
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.GITHUB_CALLBACK_URL
            },
            headers={"Accept": "application/json"}
        )
        token_data = token_response.json()
        if "error" in token_data:
            raise HTTPException(status_code=400, detail="GitHub auth failed")
        
        access_token = token_data["access_token"]
        
        # Get user info
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_response.json()
        
    github_id = str(user_data["id"])
    github_login = user_data["login"]
    avatar_url = user_data.get("avatar_url", "")
    
    result = await db.execute(select(User).where(User.github_id == github_id))
    user = result.scalars().first()
    
    if not user:
        user = User(github_id=github_id, github_login=github_login, avatar_url=avatar_url)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    jwt_token = create_access_token({"sub": str(user.id)})
    
    return {
        "jwt": jwt_token,
        "user": {
            "id": str(user.id),
            "github_login": user.github_login,
            "avatar_url": user.avatar_url
        }
    }
