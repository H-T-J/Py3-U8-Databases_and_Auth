from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base

class Users(Base):
    __tabelname__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    alt_name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    joined_on = Column(DateTime, default=datetime.utcnow)

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)
