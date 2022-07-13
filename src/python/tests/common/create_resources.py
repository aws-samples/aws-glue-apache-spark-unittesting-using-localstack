# -*- coding: utf-8 -*-
"""
Common testing functions to create various AWS resources on localstack
"""

from aws.common_setup import AWSHandler
from botocore.exceptions import ClientError


def create_s3_bucket(bucket_name=None):
    """
    testing function to create given  S3 bucket
    @return:
    """
    # Create bucket
    aws_handler = AWSHandler()
    try:
        aws_handler.s3_resource.Bucket(bucket_name).objects.all().delete()
        aws_handler.s3_client.delete_bucket(Bucket=bucket_name)
    except Exception:
        pass

    try:
        resp = aws_handler.s3_resource.create_bucket(Bucket=bucket_name)
        print(f"created bucket: {bucket_name}")
    except ClientError as excp:
        print("*****************************************")
        print(excp)
        print("*****************************************")
        print(f"could not create bucket: {bucket_name}")
    return resp


def upload_to_s3(bucket_name=None, key=None, local_file_path=None):
    """
    testing function to upload given local file to s3 bucket
    """
    aws_handler = AWSHandler()
    try:
        aws_handler.s3_client.upload_file(local_file_path, bucket_name, key)
    except ClientError as excp:
        print(excp)
        print(f"could not upload given local file to bucket: {bucket_name} and key: {key}")
