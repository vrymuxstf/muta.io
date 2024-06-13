from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base


class User(Base):
    __tablename__ = "User"

    username = Column(String, unique=True, index=True, primary_key=True)
    password = Column(String, index=True)


class Message(Base):
    __tablename__ = "Message"

    username = Column(String, index=True, primary_key=True)
    content = Column(String)
