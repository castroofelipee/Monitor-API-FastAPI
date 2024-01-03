from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql://admin:123@localhost/auth"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Função para obter uma instância de sessão do banco de dados
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
