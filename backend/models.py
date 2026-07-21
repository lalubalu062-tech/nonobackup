from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)


    name = Column(String)
    runtime = Column(String)
    repo = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    worker_id = Column(String, nullable=True)
    pid = Column(Integer, nullable=True)
    auto_restart = Column(String, default="yes")
    restart_count = Column(Integer, default=0)

    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(String, unique=True, index=True)
    status = Column(String, default="offline")
    last_seen = Column(DateTime, default=datetime.utcnow)
    cpu = Column(String, default="0")
    ram = Column(String, default="0")
    projects = Column(Integer, default=0)
    hostname = Column(String, nullable=True)
