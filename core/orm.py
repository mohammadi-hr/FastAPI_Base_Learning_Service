from sqlalchemy import create_engine, Column, Integer, String, and_, or_, not_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_test import User, UserGender, UserType
from datetime import datetime, timedelta
from sqlalchemy.sql import func, text

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


# Count number of users in db

total_users = session.query(func.count(User.id)).scalar()
print(total_users)

average_column_data = session.query(
    func.avg(User.registeration_datetime)).scalar()
print(average_column_data)

total_active_users = session.query(func.count(User.is_active == True)).scalar()
print(f"total active users : {total_active_users}")

# Use Customized SQL Query
# total registered users
registered_users_query = text(
    'select count(*) from Users where is_verified = :status')
total_registered_users = session.execute(
    registered_users_query, {'status': True}).scalar()
print(total_registered_users)

# users that its national_code starts with 00
fetch_special_national_code_query = text(
    "select * from Users where national_code like '00%'")
filtered_national_codes = session.execute(
    fetch_special_national_code_query).fetchall()
for fnc in filtered_national_codes:
    print(fnc)

# number of male and female users
gender_group_query = text("select count(*), gender from Users group by gender")
number_of_males_and_females = session.execute(gender_group_query).fetchall()
for nomaf in number_of_males_and_females:
    print("\n", nomaf)
