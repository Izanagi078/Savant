from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from src.config.dbConfig import Base

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
