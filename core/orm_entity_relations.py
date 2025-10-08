from sqlalchemy import create_engine, Column, Integer, String, and_, or_, not_, ForeignKey, Enum
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
