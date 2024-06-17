from sqlalchemy import Column, Integer, String, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Contact(Base):
    """
    Represents a contact.

    Attributes:
    -----------
    id : int
        Unique identifier for the contact.
    first_name : str
        First name of the contact.
    last_name : str
        Last name of the contact.
    email : str
        Email address of the contact.
    phone_number : str
        Phone number of the contact.
    birthday : date
        Birthday of the contact.
    additional_info : str, optional
        Additional information about the contact.
    owner_id : int
        ID of the user who owns this contact.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)
    birthday = Column(Date)
    additional_info = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="contacts")

class User(Base):
    """
    Represents a user.

    Attributes:
    -----------
    id : int
        Unique identifier for the user.
    email : str
        Email address of the user.
    hashed_password : str
        Hashed password of the user.
    is_verified : bool
        Verification status of the user.
    avatar_url : str, optional
        URL of the user's avatar.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)

    contacts = relationship("Contact", back_populates="owner")
