from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

job_label_table = Table(
    "job_label",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("jobs.id")),
    Column("label_id", Integer, ForeignKey("labels.id"))
)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    jobNo = Column(String, unique=True, index=True)
    source = Column(String, nullable=False)
    title = Column(String)
    description = Column(String)
    salary = Column(String)
    company_name = Column(String)
    location = Column(String)
    link = Column(String)

    labels = relationship(
        "Label", secondary=job_label_table, back_populates="jobs")


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    jobs = relationship("Job", secondary=job_label_table,
                        back_populates="labels")
