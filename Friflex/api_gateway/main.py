from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from common.message import Job, JobType, JobStatus
from common.redis_utils import redis_client
from common.rabbitmq_utils import rabbitmq_client
from common.storage_utils import storage_client

app = FastAPI(title="Chess Video Service API Gateway")

class VideoRequest(BaseModel):
    video_url: str
    target_language: Optional[str] = "en"

@app.post("/process-video")
async def process_video(request: VideoRequest):
    # Create a new job
    job = Job(
        job_type=JobType.DOWNLOAD,
        input_data={
            "video_url": request.video_url,
            "target_language": request.target_language
        }
    )
    
    # Store job in Redis
    redis_client.set_job(job)
    
    # Publish message to download queue
    message = {
        "job_id": job.job_id,
        "job_type": JobType.DOWNLOAD,
        "data": job.input_data
    }
    rabbitmq_client.publish_message("download_queue", message)
    
    return {"job_id": job.job_id, "status": "processing"}

@app.get("/job-status/{job_id}")
async def get_job_status(job_id: str):
    job = redis_client.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job.job_id,
        "status": job.status,
        "output_data": job.output_data,
        "error": job.error
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 