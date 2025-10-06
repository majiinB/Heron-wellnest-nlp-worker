import os
from typing import Optional, Literal
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EnvConfig(BaseSettings):
    """
    Environment configuration for the NLP Worker API.

    This module defines the environment variables required for the application,
    validates them using Pydantic, and exports them for use throughout the application.

    Usage:
    - Import `env` to access validated environment variables
    - Validates required variables and provides defaults where applicable
    """

    # Application environment
    ENVIRONMENT: Literal["development", "production", "test"] = "development"
    PORT: int = Field(default=8080, ge=1, le=65535)
    MODEL_PATH: str = Field(default="xlm-roberta-base", min_length=1)

    # Database configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = Field(default=5432, ge=1, le=65535)
    DB_USER: str = Field(default="postgres", min_length=1)
    DB_PASSWORD: Optional[str] = ""
    DB_NAME: str = Field(default="nlp_worker_db", min_length=1)

    # Encryption
    CONTENT_ENCRYPTION_KEY: str = Field(
        default="default_content_encryption_key_1234",
        min_length=32,
        description="Content encryption key must be at least 32 characters"
    )
    CONTENT_ENCRYPTION_ALGORITHM: Literal["aes-256-gcm"] = "aes-256-gcm"
    CONTENT_ENCRYPTION_IV_LENGTH: int = Field(default=16, ge=1)  # in bytes
    CONTENT_ENCRYPTION_KEY_LENGTH: int = Field(default=32, ge=1)  # in bytes

    # Google Cloud Pub/Sub
    PUBSUB_NLP_TOPIC: str = Field(
        default="journal-topic",
        min_length=1,
        description="Pub/Sub topic name is required"
    )

    # Google Cloud Project
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = None

    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

# Create and validate environment configuration
try:
    env = EnvConfig()
    print(f"Environment loaded successfully: {env.ENVIRONMENT}")
except ValidationError as e:
    print(f"Environment validation errors:")
    for error in e.errors():
        print(f"  - {error['loc'][0]}: {error['msg']}")
    exit(1)
except Exception as e:
    print(f"Unexpected error loading environment: {e}")
    exit(1)