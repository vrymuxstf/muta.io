from sqlalchemy import Column, Integer, String

from database import Base


class Message(Base):
    __tablename__ = "usernames"

    username = Column(String, unique=True, index=True)
    content = Column(String, index=True)
