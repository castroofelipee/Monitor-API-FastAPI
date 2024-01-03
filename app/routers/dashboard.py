from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi_users import models
from fastapi_users.authentication import JWTBearer
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.orm import Session
from app.routers.database import get_db
from app.models.user import User

router = APIRouter()

templates = Jinja2Templates(directory="templates")


user_db = SQLAlchemyUserDatabase(UserDB, database, UserDBCreate)

@router.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request, current_user: User = Depends(fastapi_users.get_current_active_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})
