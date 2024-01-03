# app/main.py
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from routers import auth, dashboard, database
from database import get_db
from models.user import UserDB, UserDBCreate
from fastapi_users.db.sqlalchemy import SQLAlchemyUserDatabase
import uvicorn

DATABASE_URL = "postgresql://admin:123@localhost/auth"

app = FastAPI()

database = create_engine(DATABASE_URL)
Base = declarative_base()

user_db = SQLAlchemyUserDatabase(UserDB, database, UserDBCreate)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(database.router, prefix="/database", tags=["database"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
