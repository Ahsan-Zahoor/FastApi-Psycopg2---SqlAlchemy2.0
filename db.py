import psycopg2
from psycopg2.extras import RealDictCursor
import os

DATABASE_URL = 'postgresql://postgres:venturenox@localhost:5432/content'

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn
