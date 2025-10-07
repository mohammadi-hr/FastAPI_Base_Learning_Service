from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(32))
    lastname = Column(String(32))
    national_code = Column(String(15))
    email = Column(String(48))
    address = Column(String(128))
    phone = Column(String(15))

    def __repr__(self):
        return f"User(id={self.id},firstname={self.firstname},lastname={self.lastname})"


Base.metadata.create_all(engine)
