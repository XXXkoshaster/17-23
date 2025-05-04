import pika
import json
import os
from typing import Dict, Any, Optional
from .message import Job, JobType, JobStatus, Message
from .redis_utils import redis_client
from .storage_utils import storage_client

class BaseWorker:
    def __init__(self, worker_type: JobType, input_queue: str, output_queue: Optional[str] = None):
        self.worker_type = worker_type
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.connection = None
        self.channel = None
        self.setup_rabbitmq()

    def setup_rabbitmq(self):
        """Setup RabbitMQ connection and channel"""
        credentials = pika.PlainCredentials(
            os.getenv('RABBITMQ_USER', 'admin'),
            os.getenv('RABBITMQ_PASSWORD', 'admin')
        )
        parameters = pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            port=int(os.getenv('RABBITMQ_PORT', 5672)),
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.input_queue, durable=True)
        if self.output_queue:
            self.channel.queue_declare(queue=self.output_queue, durable=True)

    def process_message(self, message: Message) -> Dict[str, Any]:
        """Process a message and return the result"""
        raise NotImplementedError("Subclasses must implement process_message")

    def callback(self, ch, method, properties, body):
        """RabbitMQ callback for processing messages"""
        try:
            message_data = json.loads(body)
            message = Message(**message_data)
            
            # Update job status to processing
            redis_client.update_job_status(
                message.job_id,
                JobStatus.PROCESSING
            )
            
            # Process the message
            result = self.process_message(message)
            
            # Update job status and output data
            redis_client.update_job_status(
                message.job_id,
                JobStatus.COMPLETED,
                output_data=result
            )
            
            # If there's an output queue, publish the result
            if self.output_queue:
                next_message = Message(
                    job_id=message.job_id,
                    job_type=self.worker_type,
                    data=result
                )
                self.channel.basic_publish(
                    exchange='',
                    routing_key=self.output_queue,
                    body=json.dumps(next_message.dict()),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # make message persistent
                    )
                )
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            # Update job status to failed
            redis_client.update_job_status(
                message.job_id,
                JobStatus.FAILED,
                error=str(e)
            )
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start(self):
        """Start consuming messages"""
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.input_queue,
            on_message_callback=self.callback
        )
        print(f"Starting {self.worker_type} worker...")
        self.channel.start_consuming()

    def stop(self):
        """Stop the worker"""
        if self.connection and not self.connection.is_closed:
            self.connection.close() 