import boto3
from botocore.client import ClientError
import functions
import stack

DATA_BUCKET = "data-shwet"
REGION = "ap-south-1"
STACK_NAME = "week1"
TEMPLATE_URL = "https://" + DATA_BUCKET + ".s3." + REGION + ".amazonaws.com/template.yaml"
SOURCE_BUCKET = "sudarshan-week1"
DESTINATION_BUCKET = "sudarshan-week1-destination"


# uploading templates and job file to S3

def upload_template_python_scripts():
    s3_client = boto3.client('s3', region_name=REGION)
    try:
        s3_client.create_bucket(Bucket=DATA_BUCKET, CreateBucketConfiguration={'LocationConstraint': REGION})
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print("Data Bucket Already Created")
        else:
            print(ce)
    functions_obj = functions.Functions(REGION)
    functions_obj.upload_object(DATA_BUCKET, "template.yaml", "template.yaml")
    functions_obj.upload_zip_object(DATA_BUCKET, "lambda_function.py", "lambda_function.zip", "lambda_function.zip")


if __name__ == "__main__":

    # uploading the template files and python scripts

    upload_template_python_scripts()

    # stack create and update

    stack_obj = stack.Stack(STACK_NAME, TEMPLATE_URL, REGION, SOURCE_BUCKET, DESTINATION_BUCKET, DATA_BUCKET)
    status = stack_obj.create_update_stack()
