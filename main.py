from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends
from models import User, Gender, Role, UserUpdateRequest
from psycopg2.extensions import connection as _connection
from pydantic import BaseModel
from db import get_db_connection

app = FastAPI()


# Dependency
def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()

# db: List[User] = [
#     User(
#         id=UUID("6eed99ea-a65c-4496-9e1c-f9353ba7ce09"),
#         first_name="Ahsan",
#         last_name="Zahoor",
#         gender=Gender.male,
#         role=[Role.student]
#     ),
#     User(
#         id=UUID("9836cb32-3467-4bf8-8f6c-8d91498cf982"),
#         first_name="John",
#         last_name="Doe",
#         gender=Gender.female,
#         role=[Role.admin, Role.user]
#     )
# ]

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

@app.get("/v1/departments/")
async def get_departmenst(db: _connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM "Departments"')
    departments = cursor.fetchall()
    return departments

@app.get("/v1/departments/{department_id}")
async def get_department(department_id: int, db: _connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM "Departments" WHERE id = %s', (str(department_id)))
    department = cursor.fetchone()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

# @app.get("/api/v1/users")
# async def get_users():
#     return db

# @app.post("/api/v1/users")
# async def create_user(user: User):
#     db.append(user)
#     return {"id": user.id}

# @app.delete("/api/v1/users/{user_id}")
# async def delete_user(user_id: UUID):
#     for user in db:
#         if user.id == user_id:
#             db.remove(user)
#             return {"message": "User deleted"}
#     raise HTTPException(status_code=404, detail="User not found")

# @app.put("/api/v1/users/{user_id}")
# async def update_user(user_id: UUID, user: UserUpdateRequest):
#     for u in db:
#         if u.id == user_id:
#             if user.first_name is not None:
#                 u.first_name = user.first_name
#             if user.last_name is not None:
#                 u.last_name = user.last_name
#             if user.middle_name is not None:
#                 u.middle_name = user.middle_name
#             if user.gender is not None:
#                 u.gender = user.gender
#             if user.role is not None:
#                 u.role = user.role
#             return {"message": "User updated"}
#     raise HTTPException(status_code=404, detail="User not found")