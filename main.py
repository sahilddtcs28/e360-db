from sqlalchemy.ext.declarative import declarative_base 
from src.eportal import models
from src.eportal.db import engine

models.Base.metadata.create_all(bind=engine)

