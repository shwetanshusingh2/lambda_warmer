import boto3
import os
import time

s3 = boto3.resource('s3')


def handler(event, context):

    if(event[warmer]=="true"):
        time.sleep(100)
    else:
        destination_bucket = s3.Bucket(os.environ['des'])
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        s3.Object(destination_bucket.name, key).copy_from(CopySource={'Bucket': source_bucket, 'Key': key})
