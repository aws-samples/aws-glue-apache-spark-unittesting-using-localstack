# -*- coding: utf-8 -*-
"""
Test cases for spark_example
"""
import os

import aws

from aws.common_setup import AWSHandler
from tests.common import create_resources as cr

import pytest


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
@pytest.fixture()
def create_aws_resources(monkeypatch, set_localstack_env_vars):
    """
    pytest fixture to create required resources
    """
    raw_bucket_name = "raw-data"
    processed_bucket_name = "processed-data"

    cr.create_s3_bucket(bucket_name=raw_bucket_name)
    cr.create_s3_bucket(bucket_name=processed_bucket_name)

    # Upload CAV test file
    key = "csv/csv_data.csv"
    local_path = os.path.dirname(os.path.relpath(__file__))
    local_file_path = f"{local_path}/test_data/csv_data.csv"
    cr.upload_to_s3(bucket_name=raw_bucket_name, key=key, local_file_path=local_file_path)

    # Upload Parquet test file
    key = "parquet/parquet_data.parquet"
    local_file_path = f"{local_path}/test_data/parquet_data.parquet"
    cr.upload_to_s3(bucket_name=raw_bucket_name, key=key, local_file_path=local_file_path)


def test_spark_example(monkeypatch, set_localstack_env_vars, create_aws_resources):
    """
    test cases for spark_example
    """
    print(os.environ)

    # Call main method as base test
    aws.spark_example.main()

    aws_handler = AWSHandler()
    spark = aws_handler.spark

    # Test CAV view
    count = spark.sql("SELECT COUNT(*) FROM VW_CSV").rdd.map(lambda x: x[0]).collect()[0]
    assert count == 5

    # Test Parquet view
    count = spark.sql("SELECT COUNT(*) FROM VW_PARQUET").rdd.map(lambda x: x[0]).collect()[0]
    assert count == 5

    # Test Processed data
    count = spark.read.parquet("s3://processed-data/label/").count()
    assert count == 5
