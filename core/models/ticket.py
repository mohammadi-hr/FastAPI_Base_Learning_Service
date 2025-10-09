from database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PythonEnum
from datetime import datetime


class Ticket(Base):

    __tablename__ = 'tickets'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(128))
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    # user_id = Column(Integer, ForeignKey('users.id'))
    # category = Column(Integer, ForeignKey('categories.id'))

    def __repr__(self):
        return f"Ticket(user: {self.user_id}, id: {self.id}, title: {self.title})"
