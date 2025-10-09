from database import SessionLocal, engine, Base
from sqlalchemy import insert
from models.user import User, UserGender, UserType, Profile
from models.address import Address, Country
from models.post import Post, Category, Tag, Comment, posts_tags


# create tables only once
Base.metadata.create_all(bind=engine)

# create a new session
session = SessionLocal()

if __name__ == '__main__':
    try:
        # insert users records in to the database

        user_1 = User(username='ali_sh', password='fasdfaefae', email='ali_sh@gmail.com',
                      is_active=True, is_verified=False, role=UserType.ADMIN)
        session.add(user_1)

        user_2 = User(username='mohsen_rf', password='rgvrag',
                      email='mohsen_rf@gmail.com', is_active=True, is_verified=True, role=UserType.USER)
        user_3 = User(username='rahim_kz', password='argasga',
                      email='rahim_kz@gmail.com', is_active=False, is_verified=True, role=UserType.GUEST)
        user_4 = User(username='atefeh_hsn', password='uitl,tu', email='atefeh_hsn@gmail.com',
                      is_active=True, is_verified=True, role=UserType.SEO_SPECIALIST)
        user_5 = User(username='zahra_mkh', password='ryjreth', email='zahra_mkh@gmail.com',
                      is_active=True, is_verified=True, role=UserType.CONTENT_MANAGER)

        users = [user_2, user_3, user_4, user_5]
        session.add_all(users)

        # insert addresses records in to the database

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
        session.add_all(addresses)

        user_addresses = session.query(Address).filter_by(user_id=3).all()
        for ud in user_addresses:
            print(ud.user.username)

        addr_6 = Address(user_id=5, city='بوشهر',
                         address_detail="خیابان کاج", postal_code='687645143')
        session.add(addr_6)

        # insert addresses records in to the database

        profile_01 = Profile(user_id=1, firstname='علی',
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

        session.add_all(profiles)

        # insert posts records in to the database

        post_01 = Post(id=1, user_id=3, title='Starlette Quick Start', category_id=4,
                       content="Other arguments that are transferrable include the relationship.secondary parameter that refers to a many-to-many association table, as well as the “join” arguments relationship.primaryjoin and relationship.secondaryjoin; “backref” is smart enough to know that these two arguments should also be “reversed” when generating the opposite side.")
        post_02 = Post(id=2, user_id=3, title='Starlette Configuration', category_id=4,
                       content="Other arguments that are transferrable include the relationship.secondary parameter that refers to a many-to-many association table, as well as the “join” arguments relationship.primaryjoin and relationship.secondaryjoin; “backref” is smart enough to know that these two arguments should also be “reversed” when generating the opposite side.")
        post_03 = Post(id=3, user_id=1, title='PHP Relationship Patterns', category_id=3,
                       content="Other arguments that are transferrable include the relationship.secondary parameter that refers to a many-to-many association table, as well as the “join” arguments relationship.primaryjoin and relationship.secondaryjoin; “backref” is smart enough to know that these two arguments should also be “reversed” when generating the opposite side.")
        post_04 = Post(id=4, user_id=2, title='PHP List Relationships', category_id=3,
                       content="Other arguments that are transferrable include the relationship.secondary parameter that refers to a many-to-many association table, as well as the “join” arguments relationship.primaryjoin and relationship.secondaryjoin; “backref” is smart enough to know that these two arguments should also be “reversed” when generating the opposite side.")
        post_05 = Post(id=5, user_id=5, title='Python Relationship Joins', category_id=2,
                       content="Other arguments that are transferrable include the relationship.secondary parameter that refers to a many-to-many association table, as well as the “join” arguments relationship.primaryjoin and relationship.secondaryjoin; “backref” is smart enough to know that these two arguments should also be “reversed” when generating the opposite side.")

        insert_posts = [post_01, post_02, post_03, post_04, post_05]
        session.add_all(insert_posts)

        # insert categories records in to the database

        category_01 = Category(
            title='SQLAlchemy', description="SQLAlchemy description", parent_id=2)
        category_02 = Category(
            title='Python', description="Python description")
        category_03 = Category(title='PHP', description="web backend program")
        category_04 = Category(
            title='Starlette', description="Starlette description ", parent_id=2)
        category_05 = Category(
            title='Pydamic', description="Pydamic description", parent_id=2)
        category_list = [category_01, category_02,
                         category_03, category_04, category_05]
        session.add_all(category_list)

        # insert tags records in to the database

        tag_1 = Tag(title="python_performance",
                    description="python_performance description")
        tag_2 = Tag(title="refactor", description="refactor description")
        tag_3 = Tag(title="python_security",
                    description="python_security description")
        tag_4 = Tag(title="fastapi_validation",
                    description="fastapi_validation description")
        tag_5 = Tag(title="fastapi_serialization",
                    description="fastapi_serialization description")

        tags_list = [tag_1, tag_2, tag_3, tag_4, tag_5]
        session.add_all(tags_list)

        # insert posts_tags records in to the database

        post_tag_insetion = insert(posts_tags).values([{"post_id": 1, "tag_id": 1}, {"post_id": 2, "tag_id": 1}, {
            "post_id": 3, "tag_id": 4}, {"post_id": 3, "tag_id": 5}, {"post_id": 5, "tag_id": 2}, {"post_id": 2, "tag_id": 2}])

        with engine.connect() as conn:
            result = conn.execute(post_tag_insetion)
            conn.commit()
            conn.close()

        # insert comments records in to the database

        comment_1 = Comment(user_id=1, post_id=1,
                            title="comment 1", content="comment's content 1")
        comment_2 = Comment(user_id=2, post_id=1, parent_id=1,
                            title="comment 2", content="comment's content 2")
        comment_3 = Comment(user_id=1, post_id=1, parent_id=2,
                            title="comment 3", content="comment's content 3")
        comment_4 = Comment(user_id=3, post_id=2,
                            title="comment 4", content="comment's content 4")
        comment_5 = Comment(user_id=4, post_id=2,
                            title="comment 5", content="comment's content 5")
        comment_6 = Comment(user_id=4, post_id=5,
                            title="comment 6", content="comment's content 6")
        comment_7 = Comment(user_id=1, post_id=5, parent_id=6,
                            title="comment 7", content="comment's content 7")
        comment_8 = Comment(user_id=5, post_id=5, parent_id=6,
                            title="comment 8", content="comment's content 8")
        comment_9 = Comment(user_id=2, post_id=5, parent_id=8,
                            title="comment 9", content="comment's content 9")
        comment_10 = Comment(user_id=1, post_id=3,
                             title="comment 10", content="comment's content 10")

        comments = [comment_1, comment_2, comment_3, comment_4, comment_5,
                    comment_6, comment_7, comment_8, comment_9, comment_10]
        session.add_all(comments)

        session.commit()

    finally:
        session.close()
