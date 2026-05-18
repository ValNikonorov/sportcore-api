from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

from app.db import Base


class Organization(Base):

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    city = Column(String, nullable=False)

    organization_type = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
