
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100))
    password = Column(String(128))
    name = Column(String(100))

    user_informations = relationship("UserInformations", back_populates="user")


class UserInformations(Base):
    __tablename__ = "user_informations"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    phone = Column(String)
    dob = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", back_populates="user_informations")
