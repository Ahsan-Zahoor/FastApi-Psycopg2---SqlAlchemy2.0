# import psycopg2
# from psycopg2.extras import RealDictCursor
# import os

# DATABASE_URL = 'postgresql://postgres:venturenox@localhost:5432/content'

# def get_db_connection():
#     conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
#     return conn


from sqlalchemy.orm import Session
from fastapi import Depends

from models import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
