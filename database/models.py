from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Text, Boolean, Float, Date, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone, timedelta
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Создаем базовый класс для декларативных моделей
Base = declarative_base()


class UserSession(Base):
    __tablename__ = 'user_sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    platform = Column(VARCHAR)
    accumulated_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    last_message_at = Column(DateTime, server_default=func.now())
    client_name = Column(Text)
    actual = Column(Boolean, default=True)


