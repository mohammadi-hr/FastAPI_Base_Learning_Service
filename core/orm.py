from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_test import User, UserGender, UserType

SQLAlchemy_SQLite_URI = "sqlite:///./sqlite.db"

engine = create_engine(
    SQLAlchemy_SQLite_URI,
    echo=True,  # Log SQL to the console
    # Allow use across multiple threads
    connect_args={"check_same_thread": False}  # usre only for sqlite
)

Session = sessionmaker(autoflush=False, bind=engine)


# Retrieve All Data From DB

session = Session()
users = session.query(User).all()
# print(users)

# Retrieve Data By Filter From DB
# SQLAlchemy not support the complicated queries
first_user = session.query(User).filter_by(username='Ali').first()
# one_or_none is useful when we want to user if clause
one_or_none_user = session.query(User).filter_by(username='Ali').one_or_none()
if one_or_none_user:
    # Update User
    one_or_none_user.firstname = 'Ali'
    session.commit()
    # Delete User
    session.delete(one_or_none_user)
    session.commit()

several_user = session.query(User).filter_by(
    username='Behnam', is_active=True).all()
print(several_user)
