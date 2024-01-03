from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi_users import FastAPIUsers, models
from sqlalchemy.orm import Session
from routers.database import get_db
from models.user import User, UserCreate, UserDB

router = APIRouter()

templates = Jinja2Templates(directory="templates")

fastapi_users = FastAPIUsers(
    UserDB, UserCreate, User, models.UserDB, get_db
)


@router.post("/token", response_model=models.Token)
async def login_for_access_token(data: UserCreate = Depends()):
    return await fastapi_users.get_auth_token(data)



@router.get("/protected")
async def protected_router(user: User = Depends(fastapi_users.get_current_active_user)):
    return {"message": "Esta é uma rota protegida"}

 
@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return await fastapi_users.create_user(user, db=db)


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(fastapi_users.get_current_active_user)):
    return current_user
