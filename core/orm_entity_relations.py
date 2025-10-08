from sqlalchemy import create_engine, Column, Integer, String, and_, or_, not_, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.sql import func, text
from sqlalchemy_conf import *


class Country(PythonEnum):
    IRAN = 'IRAN'
    INDIA = 'INDIA'
    TURKEY = 'TURKEY'


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='addresses')
    country = Column(Enum(Country), default=Country.IRAN)
    city = Column(String(32))
    address_detail = Column(String(256), nullable=True)
    postal_code = Column(String(15))
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)
    status = Column(Boolean(), default=True)

    def __repr__(self):
        return f"Address (user_id: {self.user_id} , country: {self.country}, city: {self.city}, address_detail: {self.address_detail}, postal_code: {self.postal_code})"


class UserGender(PythonEnum):
    MALE = 'male'
    FEMALE = 'female'


class UserType(PythonEnum):
    ADMIN = 'admin'
    CONTENT_MANAGER = 'content_manager'
    SEO_SPECIALIST = 'seo_specialist'
    GUEST = "guest"
    USER = "user"


class Post(Base):

    __tablename__ = 'posts'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    category_id = Column(Integer(), ForeignKey('categories.id'))
    title = Column(String(64))
    content = Column(Text())
    created_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now(),
                       onupdate=datetime.now())

    def __repr__(self):
        return f"Post(id: {self.id}, title:{self.title})"
    comments = relationship('Comment', backref='post')


class Comment(Base):

    __tablename__ = 'comments'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    post_id = Column(Integer(), ForeignKey('posts.id'))
    parent_id = Column(Integer(), ForeignKey('comments.id'), nullable=True)
    title = Column(String(128))
    content = Column(Text())
    created_at = Column(DateTime(), default=datetime.now())
    is_approved = Column(Boolean(), default=False)
    parent = relationship(
        'Comment', back_populates='children', remote_side=[id])
    children = relationship(
        'Comment', back_populates='parent', remote_side=[parent_id])

    def __repr__(self):
        return f"Comment(id: {self.id}, user:{self.user_id}, title: {self.title})"


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


Base.metadata.create_all(engine)
addr_1 = Address(user_id=2, city='اراک',
                 address_detail="میدان امام خمینی ، منطقه سر دشت", postal_code='8945134')
addr_2 = Address(user_id=3, city='تهران',
                 address_detail="قلهک", postal_code='52745272')
addr_3 = Address(user_id=3, city='قم',
                 address_detail="هفتاد و دو تن", postal_code='727272')
addr_4 = Address(user_id=4, city='رشت',
                 address_detail="بوستان مادر", postal_code='542134')
addr_5 = Address(user_id=5, city='زاهدان',
                 address_detail="عباس آباد", postal_code='752726')
addresses = [addr_1, addr_2, addr_3, addr_4, addr_5]
# session.add_all(addresses)
# session.commit()


user_addresses = session.query(Address).filter_by(user_id=3).all()
for ud in user_addresses:
    print(ud.user.username)

addr_6 = Address(user_id=5, city='بوشهر',
                 address_detail="خیابان کاج", postal_code='687645143')
# session.add(addr_6)
# session.commit()

user_ali = session.query(User).filter_by(username='ali_sh').one_or_none()
print(user_ali.profile.lastname)

profile_01 = Profile(user_id=user_ali.id, firstname='علی',
                     lastname='شریفی', gender=UserGender.MALE)
profile_02 = Profile(user_id=2, firstname='محسن', lastname='رفیعی',
                     gender=UserGender.MALE)
profile_03 = Profile(user_id=3, firstname='رحیم', lastname='کاظمی',
                     gender=UserGender.MALE)
profile_04 = Profile(user_id=4, firstname='عاطفه', lastname='حسنی',
                     gender=UserGender.FEMALE)
profile_05 = Profile(user_id=5, firstname='زهرا', lastname='مختاری',
                     gender=UserGender.FEMALE)
profiles = [profile_01, profile_02, profile_03, profile_04, profile_05]

# session.add_all(profiles)
# session.commit()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, autoincrement=True, primary_key=True)
    parent_id = Column(Integer(), ForeignKey('categories.id'), nullable=True)
    title = Column(String(128))
    description = Column(Text(), nullable=True)

    def __repr__(self):
        return f"Category(id: {self.id}, title: {self.content})"


Base.metadata.create_all(engine)
session = Session()
post_01 = Post(id=1, user_id=3, title='ORM Quick Start', category_id=4, content="Other arguments that are transferrable include the relationship.secondary parameter that refers to a many-to-many association table, as well as the “join” arguments relationship.primaryjoin and relationship.secondaryjoin; “backref” is smart enough to know that these two arguments should also be “reversed” when generating the opposite side.")
post_02 = Post(id=2, user_id=3, title='ORM Mapped Class Configuration', category_id=4,
               content="Other arguments that are transferrable include the relationship.secondary parameter that refers to a many-to-many association table, as well as the “join” arguments relationship.primaryjoin and relationship.secondaryjoin; “backref” is smart enough to know that these two arguments should also be “reversed” when generating the opposite side.")
post_03 = Post(id=3, user_id=1, title='Basic Relationship Patterns', category_id=4,
               content="Other arguments that are transferrable include the relationship.secondary parameter that refers to a many-to-many association table, as well as the “join” arguments relationship.primaryjoin and relationship.secondaryjoin; “backref” is smart enough to know that these two arguments should also be “reversed” when generating the opposite side.")
post_04 = Post(id=4, user_id=2, title='Adjacency List Relationships', category_id=4,
               content="Other arguments that are transferrable include the relationship.secondary parameter that refers to a many-to-many association table, as well as the “join” arguments relationship.primaryjoin and relationship.secondaryjoin; “backref” is smart enough to know that these two arguments should also be “reversed” when generating the opposite side.")
post_05 = Post(id=5, user_id=5, title='Configuring how Relationship Joins', category_id=4,
               content="Other arguments that are transferrable include the relationship.secondary parameter that refers to a many-to-many association table, as well as the “join” arguments relationship.primaryjoin and relationship.secondaryjoin; “backref” is smart enough to know that these two arguments should also be “reversed” when generating the opposite side.")

insert_posts = [post_01, post_02, post_03, post_04, post_05]
# session.add_all(insert_posts)
# session.commit()


# retrive posts of user with id=2
user_id_2 = session.query(User).filter_by(id=2).one_or_none()
# print(user_id_2.posts)
post_obj = user_id_2.posts[0]
print(post_obj.comments[0])
# session.add(Comment(title='Relationships API',
#             post_id=post_obj.id, user_id=user_id_2.id, content="In today's post, I will explain how to perform queries on an SQL database using Python. Particularly, I will cover how to query a database with SQLAlchemy"))
# session.commit()
parent_comment = post_obj.comments[0]
# session.add(Comment(title='comment 3', post_id=post_obj.id, user_id=5,
#             parent_id=parent_comment.id, content="this is a second reply to parent comment"))
# session.commit()

print(post_obj.comments)
