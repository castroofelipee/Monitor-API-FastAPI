from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_users import FastAPIUsers, models
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import create_engine, Column, String, Integer, MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Session, sessionmaker
from databases import Database


DATABASE_URL = "postgresql://user:password@localhost/dbname"
database = Database(DATABASE_URL)
metadata = MetaData()

e
Base: DeclarativeMeta = declarative_base()


class ExampleTable(Base):
    __tablename__ = "example_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class UserDB(Base, models.BaseUserDB):
    __tablename__ = "users"
    name = Column(String, default="")
    age = Column(Integer, nullable=True)

class User(UserDB, models.BaseUser):
    pass

class UserCreate(models.BaseUserCreate):
    name: str
    age: int

class UserUpdate(UserCreate, models.BaseUserUpdate):
    pass

class UserInDB(UserDB):
    pass

class UserDBCreate(UserDB, models.BaseUserDBCreate):
    pass


def create_database():
    Base.metadata.create_all(bind=database.engine)


user_db = SQLAlchemyUserDatabase(UserDB, database, UserDBCreate)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


fastapi_users = FastAPIUsers(
    user_db,
    [models.User, models.UserCreate, models.UserUpdate, models.UserInDB, models.UserDBCreate, User],
    "c14c9d4219c8a733ce98fcfa68324f0470a927ca79c21513ea5e7fa0dd92d556",
    30,
)


@app.post("/token", response_model=models.Token)
async def login_for_access_token(data: models.UserCreate = Depends()):
    return await fastapi_users.get_auth_token(data)


@app.get("/protected")
async def protected_route(user: models.User = Depends(fastapi_users.get_current_active_user)):
    return {"message": "This is a protected route"}

o
@app.post("/users/", response_model=models.User)
async def create_user(user: models.UserCreate):
    return await fastapi_users.create_user(user)


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: models.User = Depends(fastapi_users.get_current_active_user)):
    return current_user


@app.get("/database_data")
async def get_database_data(
    current_user: models.User = Depends(fastapi_users.get_current_active_user),
    db: Session = Depends(database.session),
):
    examples = db.query(ExampleTable).all()
    return {"data": [{"id": example.id, "name": example.name} for example in examples]}


create_database()


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("dashboard.html", {"request": "root"})


@app.get("/plot", response_class=HTMLResponse)
async def plot_example():

    data = {"Category": ["A", "B", "C"], "Values": [10, 20, 15]}


    fig = px.bar(data, x="Category", y="Values", title="Exemplo de Gráfico Interativo")

    
    plot_div = plot(fig, output_type="div")

    return templates.TemplateResponse("plot.html", {"request": "plot", "plot_div": plot_div})
