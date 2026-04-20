import os
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:8333",
    aws_access_key_id="Mahesh",
    aws_secret_access_key=os.getenv("S3_SECRET_KEY")
)
""" s3.create_bucket(Bucket="testbucket") """

s3.upload_file(
    Filename="C:/Personal/Extra/OtherWork/Doc3.pdf",
    Bucket= "testbucket",
    Key = "documents/Doc3.pdf",
    ExtraArgs={"ContentType": "application/pdf"}
)