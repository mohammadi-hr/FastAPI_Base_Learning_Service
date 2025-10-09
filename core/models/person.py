from database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PythonEnum
from datetime import datetime


class Person(Base):

    __tablename__ = 'persons'

    id = Column(Integer, autoincrement=True, primary_key=True)
    firstname = Column(String(12))
    lastname = Column(String(18))
    national_code = Column(String(15), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(),
                        onupdate=datetime.now(), nullable=True)

    def __repr__(self):
        return f"Person(id: {self.id}, firstname: {self.firstname}, lastname: {self.lastname})"
