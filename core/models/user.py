from core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PythonEnum
from datetime import datetime


class UserGender(PythonEnum):
    MALE = 'male'
    FEMALE = 'female'


class UserType(PythonEnum):
    ADMIN = 'admin'
    CONTENT_MANAGER = 'content_manager'
    SEO_SPECIALIST = 'seo_specialist'
    GUEST = "guest"
    USER = "user"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
    password = Column(String(48))
    email = Column(String(48))
    # user backref in Address Class and remove the following line
    # addresses = relationship(Address, back_populates='user')
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    registeration_datetime = Column(DateTime, nullable=True)
    role = Column(SQLAlchemyEnum(UserType), default=UserType.GUEST)
    profile = relationship("Profile", back_populates="user", uselist=False)
    posts = relationship("Post", backref='user')
    comments = relationship("Comment", backref='user')

    def __repr__(self):
        return f"User(id={self.id},username={self.username},email={self.email})"


class Profile(Base):

    __tablename__ = 'profiles'

    int = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    user = relationship("User", back_populates="profile")
    firstname = Column(String(32), nullable=True)
    lastname = Column(String(32), nullable=True)
    national_code = Column(String(15), nullable=True)
    phone = Column(String(15), nullable=True)
    gender = Column(SQLAlchemyEnum(UserGender), default=UserGender.MALE)
    bio = Column(String(512), nullable=True)
    update_at = Column(DateTime(), default=datetime.now())
