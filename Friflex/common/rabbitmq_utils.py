import pika
import json
from typing import Dict, Any
import os
from .message import Message

class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """Establish connection to RabbitMQ"""
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

    def publish_message(self, queue: str, message: Message):
        """Publish a message to a specific queue"""
        if not self.connection or self.connection.is_closed:
            self.connect()
        
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message.dict()),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )

    def close(self):
        """Close the connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()

# Singleton instance
rabbitmq_client = RabbitMQClient() 