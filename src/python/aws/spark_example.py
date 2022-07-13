# -*- coding: utf-8 -*-
"""
AWS Glue/Spark sample code to describe automated local unit testing
"""
from aws.common_setup import AWSHandler


def create_temp_view(path=None, file_type=None, view_name=None):
    """
    create spark temp view with data from given S3 path and file type
    """
    try:
        aws_handler = AWSHandler()
        spark = aws_handler.spark

        if file_type.lower() == "csv":
            spark.read.option("header", "true").csv(path).createOrReplaceTempView(view_name)
        elif file_type.lower() == "parquet":
            spark.read.parquet(path).createOrReplaceTempView(view_name)
        else:
            print(f"Found invalid file type: '{file_type}'. Valid file types are: 'csv', 'parquet'")

        print(f"Created temp view {view_name} from location {path}")
    except Exception as excp:
        print(excp)
        raise excp


def process_data(csv_view_name=None, parquet_view_name=None, target_s3_path=None):
    """
    process data using given views and write data to S3 as parquet
    """
    print(f"start writing processed data to location: '{target_s3_path}'")
    try:
        aws_handler = AWSHandler()
        spark = aws_handler.spark
        sql = f"""
        SELECT
            csv.id as id,
            csv.label as label,
            parquet.label_description as label_description,
            csv.qty as qty
        FROM
            {csv_view_name} as csv, {parquet_view_name} as parquet
        WHERE
            csv.label = parquet.label
        """
        print(f"Running SQL: {sql}")
        spark.sql(sql).write.mode("overwrite").parquet(target_s3_path)
    except Exception as excp:
        print(excp)
        raise excp
    print(f"start writing processed data to location: '{target_s3_path}'")


def main():
    """
    main method
    :return:
    """
    aws_handler = AWSHandler()
    spark = aws_handler.spark
    print(spark.sql("select current_timestamp as ts").rdd.collect())

    # Create required temp views
    create_temp_view(path="s3://raw-data/csv/", view_name="vw_csv", file_type="csv")
    create_temp_view(path="s3://raw-data/parquet/", view_name="vw_parquet", file_type="parquet")

    # Write processed data
    process_data(csv_view_name="vw_csv", parquet_view_name="vw_parquet",
                 target_s3_path="s3://processed-data/label/")
