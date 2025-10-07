from sqlalchemy import create_engine, Column, Integer, String, and_, or_, not_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_test import User, UserGender, UserType
from datetime import datetime, timedelta

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
# SQLAlchemy 'filter_by' query not support the complicated filteration
first_user = session.query(User).filter_by(username='Hamid').first()
# one_or_none is useful when we want to user if clause
one_or_none_user = session.query(User).filter_by(
    username='Hamid').one_or_none()
if one_or_none_user:
    # Update User
    one_or_none_user.firstname = 'Hamidreza'

    # Update User Registraion_Date
    init_time_for_now = datetime.now()
    one_or_none_user.registeration_datetime = init_time_for_now - \
        timedelta(days=365)

    session.commit()
    # Delete User
    # session.delete(one_or_none_user)
    # session.commit()

several_user = session.query(User).filter_by(
    username='Behnam', is_active=True).all()
print(several_user)


# Do Better Query By 'filter' method
time_filter = datetime.now() - timedelta(days=366)
# Users that register after 1 year ago
users_registered_after_last_year = session.query(User).filter(
    User.registeration_datetime > time_filter).all()
for u in users_registered_after_last_year:
    print(f"{u.username} : {u.registeration_datetime}")
# users that have gmail account
users_with_gmail = session.query(User).filter(User.email.ilike("%gmail%"))
for ug in users_with_gmail:
    print(f"{ug.username} : {ug.email}")

# Get users that is active and is male
male_active_users = session.query(User).filter(
    and_(User.is_active == True, User.gender == 'MALE'))
for mau in male_active_users:
    print(f"{mau.username}: {mau.gender}")
