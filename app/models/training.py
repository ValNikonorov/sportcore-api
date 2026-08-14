from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from app.db import Base


training_teams = Table(
    "training_teams",
    Base.metadata,
    Column("training_id", Integer, ForeignKey(
        "trainings.id"), primary_key=True),
    Column("team_id", Integer, ForeignKey("teams.id"), primary_key=True),
)


class Training(Base):

    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    training_type = Column(String, nullable=False)
    location = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    teams = relationship(
        "Team",
        secondary=training_teams,
        back_populates="trainings",
    )
