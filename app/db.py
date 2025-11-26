import os
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
load_dotenv()


# SQLAlchemy database URL
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL = os.getenv("DATABASE_URL")

# ==============================
# Engine & Session
# ==============================
engine = create_engine(
    DATABASE_URL,
    echo=True,   # set False in production
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==============================
# Models
# ==============================
class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    cert_type = Column(String(255), nullable=False)
    cert_no = Column(String(255), nullable=True)
    pdf_url = Column(String(255), nullable=True)
    issued_at = Column(DateTime, nullable=True)

# ==============================
# Utility to create tables
# ==============================
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except SQLAlchemyError as e:
        print("Error creating tables:", e)

# ==============================
# Dependency for FastAPI
# ==============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
