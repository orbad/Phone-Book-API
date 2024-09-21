from sqlalchemy import Column, Integer, String
from db.session import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, index=True, primary_key=True)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    phone_number = Column(String(14), index=True, unique=True)
    address = Column(String(255), index=True)

