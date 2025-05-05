from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobType(str, Enum):
    DOWNLOAD = "download"
    PARSE = "parse"
    LLM = "llm"
    TRANSLATE = "translate"
    TTS = "tts"
    FORMAT = "format"
    COMPOSE = "compose"

class Job(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: JobStatus = JobStatus.PENDING
    job_type: JobType
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(BaseModel):
    job_id: str
    job_type: JobType
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow) 