from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, ARRAY
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    days = relationship("Day", back_populates="user")

class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer(), primary_key=True, index=True)
    text = Column(Text(), nullable=False)
    emotions = Column(ARRAY(String(20)), nullable=False)
    response = Column(Text(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="days")