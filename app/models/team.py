from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db import Base


class Team(Base):

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    city = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
