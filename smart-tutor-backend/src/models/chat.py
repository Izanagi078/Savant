from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from src.config.dbConfig import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    history = Column(JSON, nullable=False, default=list)  # Stores: [{"role": "user"/"tutor", "text": "..."}]
