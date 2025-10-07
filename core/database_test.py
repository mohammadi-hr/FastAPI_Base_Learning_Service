from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PythonEnum

# SQLAlchemy_SQLite_URI = sqlite:///path/:memory
# SQLAlchemy_MySQL_URI = mysql://user:password@host[:port]/dbname
# SQLAlchemy_PostgreSQL_URI = postgresql://user:password@host[:port]/dbname


SQLAlchemy_SQLite_URI = "sqlite:///./sqlite.db"
# DEFINE THE ENGINE (CONNECTION OBJECT)
engine = create_engine(
    SQLAlchemy_SQLite_URI,
    echo=True,  # Log SQL to the console
    # Allow use across multiple threads
    connect_args={"check_same_thread": False}  # usre only for sqlite
)
# CREATE THE SESSION OBJECT
Session = sessionmaker(autoflush=False, bind=engine)

# Each Table object is a member of larger collection known as MetaData and this object is available using the .metadata attribute of declarative base class. The MetaData.create_all() method is, passing in our Engine as a source of database connectivity. For all tables that havent been created yet, it issues CREATE TABLE statements to the database.
Base = declarative_base()


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
    firstname = Column(String(32), nullable=True)
    lastname = Column(String(32), nullable=True)
    national_code = Column(String(15), nullable=True)
    username = Column(String(32))
    password = Column(String(48))
    email = Column(String(48))
    address = Column(String(128), nullable=True)
    phone = Column(String(15), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    registeration_datetime = Column(DateTime, nullable=True)
    gender = Column(SQLAlchemyEnum(UserGender), default=UserGender.MALE)
    role = Column(SQLAlchemyEnum(UserType), default=UserType.GUEST)

    def __repr__(self):
        return f"User(id={self.id},username={self.username},email={self.email})"


Base.metadata.create_all(engine)

session = Session()

# Insert Data to DB

# user_1 = User(username='Ali', password='fasdfaefae', email='ali@gmail.com',
#               is_active=True, is_verified=True, gender=UserGender.MALE, role=UserType.ADMIN)
# session.add(user_1)
# session.commit()

# Insert Bulk Data to DB
# user_2 = User(username='Behnam', password='rgvrag', email='Behnam@gmail.com',
#               is_active=True, is_verified=True, gender=UserGender.MALE, role=UserType.USER)
# user_3 = User(username='Mohammad', password='argasga', email='Mohammad@gmail.com',
#               is_active=True, is_verified=True, gender=UserGender.MALE, role=UserType.GUEST)
# user_4 = User(username='Hamid', password='uitl,tu', email='Hamid@gmail.com',
#               is_active=True, is_verified=True, gender=UserGender.MALE, role=UserType.SEO_SPECIALIST)
# user_5 = User(username='Reza', password='ryjreth', email='Reza@gmail.com', is_active=True,
#               is_verified=True, gender=UserGender.MALE, role=UserType.CONTENT_MANAGER)


# users = [user_2, user_3, user_4, user_5]
# session.add_all(users)
# session.commit()
