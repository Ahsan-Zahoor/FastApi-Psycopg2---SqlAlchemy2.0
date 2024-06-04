# from typing import Optional, List
# from uuid import UUID, uuid4
# from pydantic import BaseModel
# from enum import Enum

# class Gender(str,Enum):
#     male = "male"
#     female = "female"

# class Role(str,Enum):
#     admin = "admin"
#     user = "user"
#     student = "student"

# class User(BaseModel):
#     id: Optional[UUID] = uuid4()
#     first_name: str
#     last_name: str
#     middle_name: Optional[str] = None
#     gender: Gender
#     role: List[Role]

# class UserUpdateRequest(BaseModel):
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     middle_name: Optional[str] = None
#     gender: Optional[Gender] = None
#     role: Optional[List[Role]] = None

from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

DATABASE_URL = 'postgresql://postgres:venturenox@localhost:5432/content'

Base = declarative_base()

# class Department(Base):
#     __tablename__ = 'Departments'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     tenant_id = Column(Integer, nullable=False)
#     hod_id = Column(Integer, nullable=False)
#     parent_department_id = Column(Integer, ForeignKey('Departments.id'), nullable=True, default=None)

class Department(Base):
    __tablename__ = 'Departments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str]
    tenant_id: Mapped[int]
    hod_id: Mapped[int]
    parent_department_id: Mapped[int] = mapped_column(Integer, ForeignKey('Departments.id'), nullable=True, default=None)

# class Department(Base):
#     __tablename__ = 'Departments'
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     tenant_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     hod_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     parent_department_id: Mapped[int] = mapped_column(Integer, ForeignKey('Departments.id'), nullable=True, default=None)

# Pydantic Model
# class DepartmentCreate(Base):
#     name: str
#     tenant_id: int
#     hod_id: int
#     parent_department_id: Optional[int] = None



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
