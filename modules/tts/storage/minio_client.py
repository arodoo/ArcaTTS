from minio import Minio
from pathlib import Path
from typing import Optional
from shared.config import minio_config


class MinIOClient:
    """S3-compatible storage client wrapper."""
    
    def __init__(self):
        self.client = Minio(
            minio_config.endpoint,
            access_key=minio_config.access_key,
            secret_key=minio_config.secret_key,
            secure=minio_config.secure
        )
        self._ensure_buckets()
    
    def _ensure_buckets(self) -> None:
        """Create buckets if not exist."""
        buckets = [
            minio_config.bucket_chunks,
            minio_config.bucket_outputs,
            minio_config.bucket_metadata
        ]
        
        for bucket in buckets:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)
    
    def upload_file(
        self,
        file_path: str,
        object_name: str,
        bucket: Optional[str] = None
    ) -> bool:
        """Upload file to storage."""
        bucket = bucket or minio_config.bucket_outputs
        
        try:
            self.client.fput_object(
                bucket,
                object_name,
                file_path
            )
            return True
        except Exception as e:
            print(f"Upload error: {e}")
            return False
    
    def download_file(
        self,
        object_name: str,
        file_path: str,
        bucket: Optional[str] = None
    ) -> bool:
        """Download file from storage."""
        bucket = bucket or minio_config.bucket_outputs
        
        try:
            Path(file_path).parent.mkdir(
                parents=True,
                exist_ok=True
            )
            self.client.fget_object(
                bucket,
                object_name,
                file_path
            )
            return True
        except Exception as e:
            print(f"Download error: {e}")
            return False
