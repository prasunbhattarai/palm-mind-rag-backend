from sqlalchemy import Column, Integer, String, DateTime, Date, Time
from sqlalchemy.orm import declarative_base
from datetime import datetime



Base = declarative_base()


class Document(Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    chunk_strategy = Column(String, nullable=False)
    chunks_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)



class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    interview_date = Column(Date, nullable=False)
    interview_time = Column(Time, nullable=False)
    booking_time = Column(DateTime, default=datetime.now)