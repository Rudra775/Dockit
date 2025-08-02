from pydantic import BaseModel, HttpUrl, UUID4, Field
from datetime import datetime
from typing import Optional, List, Literal

# Request Models

class DeploymentRequest(BaseModel) :
    """Schema for initiating a deployment request"""
    github_repo_url : HttpUrl = Field(
        ..., 
        description="The GitHub repository URL to deploy"
    )
    aws_region : Optional[str] = Field(
        "ap-south-1", 
        description="AWS region for deployment. Defaults to 'ap-south-1'"
    )
    target_aws_service: Literal["ecs-fargate"] = Field(
        "ecs-fargate",
        description="Target AWS service for deployment. Currently supports only 'ecs-fargate'."
    )
    project_name: Optional[str] = Field(
        None,
        description="Optional: A user-defined name for the deployed application. If not provided, it will be derived from the repository URL."
    )
    
# Response Models

class DeploymentInitiatedResponse(BaseModel):
    """
    Schema for the response when a deployment is successfully initiated.
    """
    deployment_id: UUID4 = Field(..., description="Unique identifier for the initiated deployment.")
    status: str = Field(..., description="Current status of the deployment (e.g., 'QUEUED').")
    message: str = Field(..., description="A descriptive message about the initiation.")

class DeploymentLogEntryResponse(BaseModel):
    """
    Schema for a single log entry within a deployment's status.
    """
    timestamp: datetime = Field(..., description="Timestamp of the log entry.")
    message: str = Field(..., description="Log message content.")

class DeploymentStatusResponse(BaseModel):
    """
    Schema for retrieving the current status and logs of a deployment.
    """
    deployment_id: UUID4 = Field(..., description="Unique identifier of the deployment.")
    github_repo_url: HttpUrl = Field(..., description="The GitHub repository URL being deployed.")
    aws_region: str = Field(..., description="AWS region targeted for deployment.")
    target_aws_service: Literal["ecs-fargate"] = Field(..., description="Target AWS service for deployment.")
    project_name: str = Field(..., description="Name of the deployed application.")
    created_at: datetime = Field(..., description="Timestamp when the deployment was initiated.")
    updated_at: datetime = Field(..., description="Last update timestamp of the deployment status.")

    status: Literal[
        "QUEUED",
        "CLONING_REPO",
        "ANALYZING_PROJECT",
        "BUILDING_DOCKER_IMAGE",
        "PUSHING_TO_ECR",
        "DEPLOYING_AWS",
        "SUCCESS",
        "FAILED"
    ] = Field(..., description="Current phase of the deployment process.")
    progress_percentage: int = Field(..., description="Numerical representation of progress (0-100).")
    logs: List[DeploymentLogEntryResponse] = Field(..., description="List of log messages for the deployment.")
    deployed_url: Optional[str] = Field(None, description="The URL of the deployed application, if successful.")
    error_message: Optional[str] = Field(None, description="Details of the error if the deployment failed.")