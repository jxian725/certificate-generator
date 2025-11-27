from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, String, Boolean, DateTime, Integer, LargeBinary
from pydantic import BaseModel
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    cert_no = Column(String(20), nullable=True)
    pdf_url = Column(String(255), nullable=True)
    issued_at = Column(DateTime, nullable=True)
    cert_type = Column(String(50), nullable=False)
    huawei_id = Column(String(100), nullable=True)
    country = Column(String(50), nullable=False)
    entity = Column(String(255), nullable=True)
    cert_blob = Column(LargeBinary, nullable=True)

class ParticipantQuery(BaseModel):
    name: str | None = None
    email: str | None = None
    accountId: str | None = None
    country: str | None = None
    