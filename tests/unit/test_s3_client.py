import pytest
from unittest.mock import patch, MagicMock
from src.core.s3_client import S3Client

def test_list_buckets():
    client = S3Client()
    mock_boto = MagicMock()
    mock_boto.list_buckets.return_value = {
        'Buckets': [
            {'Name': 'bucket1', 'CreationDate': '2023-01-01T00:00:00Z'},
            {'Name': 'bucket2', 'CreationDate': '2023-01-02T00:00:00Z'}
        ]
    }
    client.s3_client = mock_boto
    buckets = client.list_buckets()
    assert len(buckets) == 2
    assert buckets[0]['name'] == 'bucket1' 