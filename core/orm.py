from sqlalchemy.sql import func, text, and_, or_, not_
from database import SessionLocal
from datetime import datetime, timedelta
from models.user import User, UserGender, UserType
from models.post import Category, Comment, Post, Tag

session = SessionLocal()


user_ali = session.query(User).filter_by(username='ali_sh').one_or_none()
print(f"{user_ali.profile.lastname}\n\n\n\n\n")


# retrive posts of user with id=2
user_id_2 = session.query(User).filter_by(id=2).one_or_none()
print(user_id_2.posts)
post_obj = user_id_2.posts[0]
print(f"{post_obj.comments}\n\n\n\n\n")
# session.add(Comment(title='Relationships API',
#             post_id=post_obj.id, user_id=user_id_2.id, content="In today's post, I will explain how to perform queries on an SQL database using Python. Particularly, I will cover how to query a database with SQLAlchemy"))
# session.commit()

parent_comment = post_obj.comments[0]
# session.add(Comment(title='comment 11', post_id=post_obj.id, user_id=5,
#             parent_id=parent_comment.id, content="this is a second reply to parent comment"))
# session.commit()

print(post_obj.comments)

category = session.query(Category).filter_by(title='PHP').one_or_none()
print(f"posts for {category.title} is {category.posts}")

# Retrieve All Data From DB

users = session.query(User).all()
print(users)

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
users_registered_after_last_year = session.query(
    User).filter(User.registered_at > time_filter).all()
for u in users_registered_after_last_year:
    print(f"{u.username} : {u.registered_at}")
# users that have gmail account
users_with_gmail = session.query(User).filter(User.email.ilike("%gmail%"))
for ug in users_with_gmail:
    print(f"{ug.username} : {ug.email}")

# Get users that is active and not verified
male_active_users = session.query(User).filter(
    and_(User.is_active == True, User.is_verified != True))
for mau in male_active_users:
    print(f"{mau.username}: {mau.email}")


# Count number of users in db

total_users = session.query(func.count(User.id)).scalar()
print(total_users)

average_column_data = session.query(
    func.avg(User.registered_at)).scalar()
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
    "select * from profiles where national_code like '00%'")
filtered_national_codes = session.execute(
    fetch_special_national_code_query).fetchall()
for fnc in filtered_national_codes:
    print(fnc)

# number of male and female users
gender_group_query = text(
    "select count(*), gender from profiles group by gender")
number_of_males_and_females = session.execute(gender_group_query).fetchall()
for nomaf in number_of_males_and_females:
    print("\n", nomaf)


post = session.query(Post).filter_by(
    title='PHP List Relationships', user_id=2).one()
tag = session.query(Tag).filter_by(title='refactor').one()
# post.tags.append(tag)
# session.commit()
print(f"\n{post.tags}\n")


session.close()
