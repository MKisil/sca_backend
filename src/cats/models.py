from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from src.database import Base

class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    experience = Column(Integer, nullable=False)
    breed = Column(String(255), nullable=False)
    salary = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint('experience >= 0', name='check_experience_non_negative'),
        CheckConstraint('salary > 0', name='check_salary_positive'),
    )
