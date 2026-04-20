from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

URL = "postgresql+psycopg2://postgres:Pin05almm@localhost:5432/swiftdocsdb"
if not URL:
    raise Exception("URL for db not found")

engine = create_engine(URL)
sessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
public_base = declarative_base()
schema_base = declarative_base()