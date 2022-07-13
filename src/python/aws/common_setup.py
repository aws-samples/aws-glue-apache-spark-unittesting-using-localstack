# -*- coding: utf-8 -*-
"""
common setup for localstack
"""
import os

import boto3
import pyspark

from awsglue.context import GlueContext


class AWSHandler: # pylint: disable=too-few-public-methods
    """
    Manages AWS services resource and client objects
    """
    def __init__(self):
        self.aws_handler_kwargs = {
            "region_name": os.environ["AWS_DEFAULT_REGION"],
            "use_ssl": os.environ["AWS_USE_SSL"],
            "verify": os.environ["AWS_VERIFY"],
            "endpoint_url": os.environ["AWS_ENDPOINT_URL"],
            "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"]
        }

        spark_context = pyspark.context.SparkContext.getOrCreate()
        glue_context = GlueContext(spark_context)
        spark = glue_context.spark_session
        if self.aws_handler_kwargs["endpoint_url"]:
            spark.conf.set("fs.s3a.endpoint",  self.aws_handler_kwargs["endpoint_url"])

        self.s3_client = boto3.client("s3", **self.aws_handler_kwargs)
        self.s3_resource = boto3.resource("s3", **self.aws_handler_kwargs)
        self.sqs_client = boto3.client("sqs", **self.aws_handler_kwargs)
        self.sqs_resource = boto3.resource("sqs", **self.aws_handler_kwargs)
        self.dynamodb_client = boto3.client("dynamodb", **self.aws_handler_kwargs)
        self.dynamodb_resource = boto3.resource("dynamodb", **self.aws_handler_kwargs)
        self.spark = spark
