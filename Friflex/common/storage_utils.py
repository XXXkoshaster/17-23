import boto3
import os
from typing import Optional, BinaryIO
from botocore.exceptions import ClientError

class StorageClient:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=os.getenv('S3_ENDPOINT_URL', 'http://localhost:9000'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'minioadmin'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'minioadmin'),
            config=boto3.session.Config(signature_version='s3v4')
        )
        self.bucket_name = "chess-videos"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure the bucket exists, create it if it doesn't"""
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                self.client.create_bucket(Bucket=self.bucket_name)
            else:
                raise Exception(f"Failed to create bucket: {e}")

    def upload_file(self, file_path: str, object_name: str) -> str:
        """Upload a file to storage"""
        try:
            self.client.upload_file(
                file_path,
                self.bucket_name,
                object_name
            )
            return f"{self.bucket_name}/{object_name}"
        except ClientError as e:
            raise Exception(f"Failed to upload file: {e}")

    def download_file(self, object_name: str, file_path: str) -> None:
        """Download a file from storage"""
        try:
            self.client.download_file(
                self.bucket_name,
                object_name,
                file_path
            )
        except ClientError as e:
            raise Exception(f"Failed to download file: {e}")

    def get_presigned_url(self, object_name: str, expires: int = 3600) -> str:
        """Generate a presigned URL for temporary access"""
        try:
            return self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expires
            )
        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {e}")

    def delete_file(self, object_name: str) -> None:
        """Delete a file from storage"""
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=object_name
            )
        except ClientError as e:
            raise Exception(f"Failed to delete file: {e}")

# Singleton instance
storage_client = StorageClient() 