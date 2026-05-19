from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from app.db import Base


class Team(Base):

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    city = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    age_group = Column(String, nullable=True)
    level = Column(String, nullable=True)

    organization_id = Column(ForeignKey("organizations.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    players = relationship("Player", back_populates="team")

    organization = relationship("Organization", back_populates="teams")
