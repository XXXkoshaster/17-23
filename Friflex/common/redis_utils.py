import redis
import json
from typing import Optional, Dict, Any
import os
from .message import Job, JobStatus

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )

    def set_job(self, job: Job, ttl: int = 3600) -> None:
        """Store a job in Redis with a TTL"""
        self.client.setex(
            f"job:{job.job_id}",
            ttl,
            job.json()
        )

    def get_job(self, job_id: str) -> Optional[Job]:
        """Retrieve a job from Redis"""
        data = self.client.get(f"job:{job_id}")
        if data:
            return Job.parse_raw(data)
        return None

    def update_job_status(self, job_id: str, status: JobStatus, output_data: Optional[Dict[str, Any]] = None, error: Optional[str] = None) -> None:
        """Update job status and optionally output data"""
        job = self.get_job(job_id)
        if job:
            job.status = status
            if output_data is not None:
                job.output_data = output_data
            if error is not None:
                job.error = error
            job.updated_at = datetime.utcnow()
            self.set_job(job)

    def delete_job(self, job_id: str) -> None:
        """Delete a job from Redis"""
        self.client.delete(f"job:{job_id}")

# Singleton instance
redis_client = RedisClient() 