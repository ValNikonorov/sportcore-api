from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from datetime import datetime

from app.db import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    team_id = Column(Integer, nullable=False)

    position = Column(String, nullable=True)
    weight = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
