from core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PythonEnum
from datetime import datetime


class Country(PythonEnum):
    IRAN = 'IRAN'
    INDIA = 'INDIA'
    TURKEY = 'TURKEY'


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='addresses')
    country = Column(SQLAlchemyEnum(Country), default=Country.IRAN)
    city = Column(String(32))
    address_detail = Column(String(256), nullable=True)
    postal_code = Column(String(15))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    status = Column(Boolean, default=True)

    def __repr__(self):
        return f"Address (user_id: {self.user_id} , country: {self.country}, city: {self.city}, address_detail: {self.address_detail}, postal_code: {self.postal_code})"
