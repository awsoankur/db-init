from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__="posts"
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String, nullable= False)
    content = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable= False)
    email = Column(String, nullable=False, unique= True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()'))
    account_id = Column(Integer,ForeignKey("account.id",ondelete="CASCADE"),nullable=False)

class Votes(Base):
    __tablename__="votes"
    direction = Column(Integer,nullable=False)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)

class Account(Base):
    __tablename__="account"
    id = Column(Integer, primary_key=True, nullable= False)
    dob = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()'))