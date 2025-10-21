from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    salary = Column(String)
    company_name = Column(String)
    location = Column(String)
    link = Column(String)

    labels = relationship("Label", back_populates="job")


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    job_id = Column(Integer, ForeignKey("jobs.id"))
    job = relationship("Job", back_populates="labels")
