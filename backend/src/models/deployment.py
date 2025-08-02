from sqlalchemy import Column, String, DateTime, Integer, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

# Base class for declarative models
Base = declarative_base()

class DeploymentLogEntry(Base):
    """
    SQLAlchemy model for individual log entries related to a deployment.
    """
    __tablename__ = "deployment_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    deployment_id = Column(String, ForeignKey("deployments.deployment_id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    message = Column(Text, nullable=False)

    # Relationship to the Deployment model
    deployment = relationship("Deployment", back_populates="logs")

    def __repr__(self):
        return f"<DeploymentLogEntry(id='{self.id}', deployment_id='{self.deployment_id}', message='{self.message[:50]}...')>"

class Deployment(Base):
    """
    SQLAlchemy model for a deployment record.
    """
    __tablename__ = "deployments"

    # Using String for UUIDs for SQLite compatibility
    deployment_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    github_repo_url = Column(String, nullable=False)
    aws_region = Column(String, nullable=False)
    target_aws_service = Column(String, nullable=False)
    project_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    status = Column(String, nullable=False, default="QUEUED")
    progress_percentage = Column(Integer, nullable=False, default=0)
    deployed_url = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)

    # Internal details (JSON type for flexibility)
    clone_path = Column(String, nullable=True)
    docker_image_name = Column(String, nullable=True)
    ecr_repo_uri = Column(String, nullable=True)
    aws_resource_ids = Column(JSON, nullable=True) # Stores dict as JSON string in SQLite

    # Relationship to log entries
    logs = relationship("DeploymentLogEntry", order_by=DeploymentLogEntry.timestamp, back_populates="deployment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Deployment(id='{self.deployment_id}', project='{self.project_name}', status='{self.status}')>"