from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "sqlite:///./e360.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False}) # different thread for each connection or request

sessionLocalFactory = sessionmaker(bind=engine, autoflush=False, autocommit= False)
Base = declarative_base()


def get_db():
    db = sessionLocalFactory()

    with db:
        yield db

db_injection =  Annotated[Session, Depends(get_db)]
