import boto3
from botocore.exceptions import ClientError
import os

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:8333",
    aws_access_key_id="Mahesh",
    aws_secret_access_key=os.getenv("S3_SECRET_KEY")
)

def upload_file(bucket: str, key: str, file_obj):
    s3.upload_fileobj(
        Fileobj = file_obj.file.seek(0),
        Bucket = bucket,
        Key = key,
        ExtraArgs = {"ContentType":file_obj.content_type}
    )

def download_file(bucket: str, key: str,filename:str | None):
    params = {
        "Bucket":bucket,
        "Key":key
    }

    if filename:
        params["ResponseContentDisposition"] = f"attachment; filename={filename}"
    else:
        raise Exception("No filename found")
    
    try:
        url = s3.generate_presigned_url(
            ClientMethod = "get_object",
            Params = params,
            ExpiresIn = 300
        )
        return {"download_url":url}
    except ClientError as e:
        raise e


    

    



