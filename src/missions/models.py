from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.database import Base
from src.cats.models import Cat

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=True)
    completed = Column(Boolean, default=False)

    cat = relationship("Cat")
    targets = relationship("Target", cascade="all, delete-orphan")


class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    name = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    notes = Column(String, default="")
    completed = Column(Boolean, default=False)

    mission = relationship("Mission", back_populates="targets")
