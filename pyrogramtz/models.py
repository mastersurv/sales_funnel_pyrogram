from sqlalchemy import Column, Integer, String, DateTime
from db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    status = Column(String)
    status_updated_at = Column(DateTime)
