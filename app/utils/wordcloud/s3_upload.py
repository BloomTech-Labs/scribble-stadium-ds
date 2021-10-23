import boto3
from botocore.exceptions import ClientError
import os
import random
import string
import logging
from os import getenv, environ, path
from dotenv import load_dotenv

load_dotenv()

def upload_file(file_name):
    """Upload a file to an S3 bucket
    :return: url if file was uploaded, else False
    """
    bucket = os.getenv('BUCKET_NAME')
    letters = string.ascii_letters
    object_name = ''.join(random.choice(letters) for i in range(10))
    # If S3 object_name was not specified, use file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return os.getenv('URL_BEGINNING') + object_name