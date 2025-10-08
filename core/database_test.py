from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PythonEnum
from sqlalchemy_conf import *
from orm_entity_relations import User, UserType

# SQLAlchemy_SQLite_URI = sqlite:///path/:memory
# SQLAlchemy_MySQL_URI = mysql://user:password@host[:port]/dbname
# SQLAlchemy_PostgreSQL_URI = postgresql://user:password@host[:port]/dbname


Base.metadata.create_all(engine)

# Insert Data to DB

user_1 = User(username='ali_sh', password='fasdfaefae',
              email='ali_sh@gmail.com', is_active=True, is_verified=False, role=UserType.ADMIN)
# session.add(user_1)
# session.commit()

# Insert Bulk Data to DB
user_2 = User(username='mohsen_rf', password='rgvrag',
              email='mohsen_rf@gmail.com', is_active=True, is_verified=True, role=UserType.USER)
user_3 = User(username='rahim_kz', password='argasga',
              email='rahim_kz@gmail.com', is_active=False, is_verified=True, role=UserType.GUEST)
user_4 = User(username='atefeh_hsn', password='uitl,tu', email='atefeh_hsn@gmail.com',
              is_active=True, is_verified=True, role=UserType.SEO_SPECIALIST)
user_5 = User(username='zahra_mkh', password='ryjreth', email='zahra_mkh@gmail.com',
              is_active=True, is_verified=True, role=UserType.CONTENT_MANAGER)


users = [user_2, user_3, user_4, user_5]
# session.add_all(users)
# session.commit()
