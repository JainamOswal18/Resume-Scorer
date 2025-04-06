from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Create the database directory if it doesn't exist
os.makedirs('database', exist_ok=True)

# Create SQLite engine
DATABASE_URL = "sqlite:///database/resume_scorer.db"
engine = create_engine(DATABASE_URL)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

class JobDetails(Base):
    __tablename__ = "job_details"

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String(255), nullable=False)
    job_details = Column(Text, nullable=False)
    skills_requirement = Column(Text, nullable=False)
    education_requirement = Column(Text, nullable=False)
    experience_requirement = Column(Text, nullable=False)
    additional_requirements = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "job_id": self.job_id,
            "job_title": self.job_title,
            "job_details": self.job_details,
            "skills_requirement": self.skills_requirement,
            "education_requirement": self.education_requirement,
            "experience_requirement": self.experience_requirement,
            "additional_requirements": self.additional_requirements,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, default=200)
    user_name = Column(String(255), nullable=False)
    user_email = Column(String(255), nullable=False, unique=True)
    resume_url = Column(String(255), nullable=False)
    parameter_score = Column(Float, default=0.0, nullable=False)
    job_similarity_score = Column(Float, default=0.0, nullable=False)
    github_score = Column(Float, default=0.0, nullable=False)
    total_score = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "resume_url": self.resume_url,
            "parameter_score": self.parameter_score,
            "job_similarity_score": self.job_similarity_score,
            "github_score": self.github_score,
            "total_score": self.total_score,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Run this to create tables if not exists
if __name__ == "__main__":
    create_tables() 