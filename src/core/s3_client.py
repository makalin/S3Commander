"""
S3 Client for handling AWS S3 operations
"""

import boto3
import botocore
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
import logging
from pathlib import Path


class S3Client:
    """Handles all S3 operations"""
    
    def __init__(self):
        self.s3_client = None
        self.logger = logging.getLogger(__name__)
        
    def initialize(self):
        """Initialize the S3 client"""
        try:
            # Create S3 client with default credentials
            self.s3_client = boto3.client('s3')
            
            # Test connection
            self.s3_client.list_buckets()
            self.logger.info("S3 client initialized successfully")
            
        except botocore.exceptions.NoCredentialsError:
            raise Exception("AWS credentials not found. Please configure your AWS credentials.")
        except botocore.exceptions.ClientError as e:
            raise Exception(f"AWS authentication failed: {e}")
        except Exception as e:
            raise Exception(f"Failed to initialize S3 client: {e}")
    
    def list_buckets(self) -> List[Dict[str, Any]]:
        """List all S3 buckets"""
        try:
            response = self.s3_client.list_buckets()
            buckets = []
            
            for bucket in response['Buckets']:
                bucket_info = {
                    'name': bucket['Name'],
                    'creation_date': bucket['CreationDate'],
                    'type': 'bucket'
                }
                buckets.append(bucket_info)
            
            return buckets
            
        except Exception as e:
            self.logger.error(f"Failed to list buckets: {e}")
            raise
    
    def list_objects(self, bucket_name: str, prefix: str = "") -> List[Dict[str, Any]]:
        """List objects in a bucket with optional prefix"""
        try:
            objects = []
            
            # Handle root level
            if prefix == "" or prefix == "/":
                prefix = ""
            
            paginator = self.s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(
                Bucket=bucket_name,
                Prefix=prefix,
                Delimiter='/'
            )
            
            for page in page_iterator:
                # Add common prefixes (folders)
                if 'CommonPrefixes' in page:
                    for common_prefix in page['CommonPrefixes']:
                        folder_name = common_prefix['Prefix'].rstrip('/').split('/')[-1]
                        objects.append({
                            'name': folder_name,
                            'key': common_prefix['Prefix'],
                            'type': 'folder',
                            'size': 0,
                            'last_modified': None
                        })
                
                # Add objects
                if 'Contents' in page:
                    for obj in page['Contents']:
                        # Skip the prefix itself if it's not a folder
                        if obj['Key'] == prefix:
                            continue
                            
                        obj_name = obj['Key'].split('/')[-1]
                        objects.append({
                            'name': obj_name,
                            'key': obj['Key'],
                            'type': 'file',
                            'size': obj['Size'],
                            'last_modified': obj['LastModified']
                        })
            
            return objects
            
        except Exception as e:
            self.logger.error(f"Failed to list objects in {bucket_name}/{prefix}: {e}")
            raise
    
    def get_object_info(self, bucket_name: str, key: str) -> Dict[str, Any]:
        """Get detailed information about an object"""
        try:
            response = self.s3_client.head_object(Bucket=bucket_name, Key=key)
            
            return {
                'name': key.split('/')[-1],
                'key': key,
                'size': response['ContentLength'],
                'last_modified': response['LastModified'],
                'content_type': response.get('ContentType', 'application/octet-stream'),
                'etag': response.get('ETag', ''),
                'storage_class': response.get('StorageClass', 'STANDARD')
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get object info for {bucket_name}/{key}: {e}")
            raise
    
    def copy_object(self, source_bucket: str, source_key: str, 
                   dest_bucket: str, dest_key: str) -> bool:
        """Copy an object from source to destination"""
        try:
            copy_source = {'Bucket': source_bucket, 'Key': source_key}
            self.s3_client.copy_object(
                CopySource=copy_source,
                Bucket=dest_bucket,
                Key=dest_key
            )
            
            self.logger.info(f"Copied {source_bucket}/{source_key} to {dest_bucket}/{dest_key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to copy object: {e}")
            raise
    
    def delete_object(self, bucket_name: str, key: str) -> bool:
        """Delete an object from S3"""
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=key)
            
            self.logger.info(f"Deleted {bucket_name}/{key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete object: {e}")
            raise
    
    def download_object(self, bucket_name: str, key: str, local_path: str) -> bool:
        """Download an object to local filesystem"""
        try:
            # Create directory if it doesn't exist
            Path(local_path).parent.mkdir(parents=True, exist_ok=True)
            
            self.s3_client.download_file(bucket_name, key, local_path)
            
            self.logger.info(f"Downloaded {bucket_name}/{key} to {local_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to download object: {e}")
            raise
    
    def upload_object(self, local_path: str, bucket_name: str, key: str) -> bool:
        """Upload a local file to S3"""
        try:
            self.s3_client.upload_file(local_path, bucket_name, key)
            
            self.logger.info(f"Uploaded {local_path} to {bucket_name}/{key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to upload object: {e}")
            raise
    
    def get_object_content(self, bucket_name: str, key: str, max_size: int = 1024*1024) -> str:
        """Get the content of a text object (limited size)"""
        try:
            # Check object size first
            obj_info = self.get_object_info(bucket_name, key)
            if obj_info['size'] > max_size:
                raise Exception(f"Object too large ({obj_info['size']} bytes). Max size: {max_size} bytes")
            
            response = self.s3_client.get_object(Bucket=bucket_name, Key=key)
            content = response['Body'].read().decode('utf-8')
            
            return content
            
        except Exception as e:
            self.logger.error(f"Failed to get object content: {e}")
            raise
    
    def search_objects(self, bucket_name: str, search_term: str, prefix: str = "") -> List[Dict[str, Any]]:
        """Search for objects by name"""
        try:
            all_objects = self.list_objects(bucket_name, prefix)
            matching_objects = []
            
            for obj in all_objects:
                if search_term.lower() in obj['name'].lower():
                    matching_objects.append(obj)
            
            return matching_objects
            
        except Exception as e:
            self.logger.error(f"Failed to search objects: {e}")
            raise

    def create_bucket(self, bucket_name: str, region: str = None) -> bool:
        """Create a new S3 bucket"""
        try:
            if region:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            else:
                self.s3_client.create_bucket(Bucket=bucket_name)
            self.logger.info(f"Created bucket: {bucket_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create bucket: {e}")
            raise

    def delete_bucket(self, bucket_name: str) -> bool:
        """Delete an S3 bucket"""
        try:
            self.s3_client.delete_bucket(Bucket=bucket_name)
            self.logger.info(f"Deleted bucket: {bucket_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete bucket: {e}")
            raise

    def rename_object(self, bucket_name: str, old_key: str, new_key: str) -> bool:
        """Rename (move) an object within a bucket"""
        try:
            self.copy_object(bucket_name, old_key, bucket_name, new_key)
            self.delete_object(bucket_name, old_key)
            self.logger.info(f"Renamed {old_key} to {new_key} in {bucket_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to rename object: {e}")
            raise

    def move_object(self, source_bucket: str, source_key: str, dest_bucket: str, dest_key: str) -> bool:
        """Move an object between buckets or prefixes"""
        try:
            self.copy_object(source_bucket, source_key, dest_bucket, dest_key)
            self.delete_object(source_bucket, source_key)
            self.logger.info(f"Moved {source_bucket}/{source_key} to {dest_bucket}/{dest_key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to move object: {e}")
            raise 