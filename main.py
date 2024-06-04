# from typing import List
# from uuid import UUID
# from fastapi import FastAPI, HTTPException, Depends
# from models import User, Gender, Role, UserUpdateRequest
# from psycopg2.extensions import connection as _connection
# from pydantic import BaseModel
# from db import get_db_connection

# app = FastAPI()

# # Dependency
# def get_db():
#     conn = get_db_connection()
#     try:
#         yield conn
#     finally:
#         conn.close()

# @app.get("/v1/departments/")
# async def get_departmenst(db: _connection = Depends(get_db)):
#     cursor = db.cursor()
#     cursor.execute('SELECT * FROM "Departments"')
#     departments = cursor.fetchall()
#     return departments

# @app.get("/v1/departments/{department_id}")
# async def get_department(department_id: int, db: _connection = Depends(get_db)):
#     cursor = db.cursor()
#     cursor.execute('SELECT * FROM "Departments" WHERE id = %s', (str(department_id)))
#     department = cursor.fetchone()
#     if department is None:
#         raise HTTPException(status_code=404, detail="Department not found")
#     return department

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from pydantic import BaseModel
from typing import Optional

from models import Department
from db import get_db

app = FastAPI()

insp = inspect(Department)

# print(insp.columns.name)
# print(insp.all_orm_descriptors.keys())

# Pydantic models for request and response
class DepartmentCreate(BaseModel):
    name: str
    tenant_id: int
    hod_id: int
    parent_department_id: Optional[int] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    tenant_id: Optional[int] = None
    hod_id: Optional[int] = None
    parent_department_id: Optional[int] = None

class DepartmentResponse(BaseModel):
    id: int
    name: str
    tenant_id: int
    hod_id: int
    parent_department_id: Optional[int] = None

    class Config:
        orm_mode = True


@app.get("/v1/departments/")
async def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return departments

@app.get("/v1/departments/{department_id}")
async def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).get(department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

# @app.post("/v1/departments/")
# async def create_department(department: Department, db: Session = Depends(get_db)):
#     db.add(department)
#     db.commit()
#     db.refresh(department)
#     return departmentt

@app.post("/v1/departments/", response_model=DepartmentResponse)
async def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    db_department = Department(
        name=department.name,
        tenant_id=department.tenant_id,
        hod_id=department.hod_id,
        parent_department_id=department.parent_department_id,
    )
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

@app.put("/v1/departments/{department_id}")
async def update_department(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    db_department = db.query(Department).get(department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    if department.name:
        db_department.name = department.name
    if department.tenant_id:
        db_department.tenant_id = department.tenant_id
    if department.hod_id:
        db_department.hod_id = department.hod_id
    if department.parent_department_id:
        db_department.parent_department_id = department.parent_department_id
    db.commit()
    db.refresh(db_department)
    return db_department

@app.delete("/v1/departments/{department_id}")
async def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).get(department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(department)
    db.commit()
    return department