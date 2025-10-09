from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint, Text, Table
from sqlalchemy.orm import relationship
from datetime import datetime

posts_tags = Table("posts_tags", Base.metadata,
                   Column("id", Integer, primary_key=True, autoincrement=True),
                   Column("post_id", Integer, ForeignKey('posts.id')),
                   Column("tag_id", Integer, ForeignKey('tags.id')),
                   UniqueConstraint('post_id', 'tag_id', name='post_tag_rel')
                   )


class Tag(Base):

    __tablename__ = 'tags'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(128))
    description = Column(Text, nullable=True)
    posts = relationship('Post', secondary=posts_tags, back_populates='tags')

    def __repr__(self):
        return f"Tag(id: {self.id}, title: {self.title})"


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, autoincrement=True, primary_key=True)
    parent_id = Column(Integer(), ForeignKey('categories.id'), nullable=True)
    title = Column(String(128))
    description = Column(Text, nullable=True)
    posts = relationship('Post', backref='category')

    def __repr__(self):
        return f"Category(id: {self.id}, title: {self.title})"


class Post(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    title = Column(String(64))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now(),
                       onupdate=datetime.now())
    tags = relationship('Tag', secondary=posts_tags, back_populates='posts')

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
    UniqueConstraint('user_id', 'post_id', 'title', name='unique_post_reply')

    def __repr__(self):
        return f"Comment(id: {self.id}, user:{self.user_id}, title: {self.title})"
