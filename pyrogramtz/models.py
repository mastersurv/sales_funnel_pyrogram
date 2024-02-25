from sqlalchemy import Column, BIGINT, String, DateTime
from db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(BIGINT, primary_key=True)
    created_at = Column(DateTime)
    status = Column(String)
    status_updated_at = Column(DateTime)
    message1_sent_at = Column(DateTime, default=None)
    message2_sent_at = Column(DateTime, default=None)
    message3_sent_at = Column(DateTime, default=None)
