from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from datetime import datetime
from src.config.dbConfig import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True)  # Stores request_id (UUID)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic = Column(String, nullable=False)
    level = Column(String, nullable=False)
    syllabus = Column(JSON, nullable=False)  # JSON type supported on both Postgres and SQLite fallbacks
    created_at = Column(DateTime, default=datetime.utcnow)
