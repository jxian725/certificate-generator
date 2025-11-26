from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Integer
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    cert_type: Mapped[str] = mapped_column(String(255))
    cert_no: Mapped[str | None] = mapped_column(String(50), nullable=True)
    pdf_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    issued_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
