from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from app.db import Base


class Training(Base):

    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True)

    team_id = Column(Integer, nullable=False)
    team_name = Column(Integer, nullable=False)
    title = Column(String, nullable=True)
    training_type = Column(String, nullable=True)
    location = Column(String, nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)

    players = relationship("Player", back_populates="team")

    team = relationship("Team", back_populates="trainings")
