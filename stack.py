import boto3
import time
from botocore.client import ClientError


class Stack:
    def __init__(self, stack_name, template_url, region, source_bucket, destination_bucket, data_bucket):
        self.stack_name = stack_name
        self.template_url = template_url
        self.client_cloudformation = boto3.client('cloudformation', region_name=region)
        self.client_s3 = boto3.client('s3', region_name=region)
        self.source_bucket = source_bucket
        self.destination_bucket = destination_bucket
        self.data_bucket = data_bucket

    # if stack is in rollback stage then stack get deleted and then it gets created.
    # if stack is in create stage then it gets updated

    def create_update_stack(self):
        status = self.status_stack()
        if status == 'ROLLBACK_COMPLETE' or status == 'ROLLBACK_FAILED' or status == 'DELETE_FAILED' or \
                status == 'UPDATE_ROLLBACK_COMPLETE':
            self.delete_object(self.source_bucket)
            self.delete_object(self.destination_bucket)
            self.client_cloudformation.delete_stack(StackName=self.stack_name)
            print("deleting stack")
            while self.status_stack() == 'DELETE_IN_PROGRESS':
                time.sleep(2)
            print("stack deleted")
            self.create_stack()
            print("creating stack")
        elif status == 'CREATE_COMPLETE' or status == 'UPDATE_COMPLETE':
            self.update_stack()
            print("updating stack")
        else:
            self.create_stack()
            print("creating stack")
        while self.status_stack() == 'CREATE_IN_PROGRESS' or \
                self.status_stack() == 'UPDATE_IN_PROGRESS' or \
                self.status_stack() == 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS':
            time.sleep(2)
        print("stack created")

    def create_stack(self):
        try:
            self.client_cloudformation.create_stack(
                StackName=self.stack_name,
                TemplateURL=self.template_url,
                Capabilities=['CAPABILITY_NAMED_IAM'],
                Parameters=[
                    {
                        'ParameterKey': "SourceBucket",
                        'ParameterValue': self.source_bucket
                    },
                    {
                        'ParameterKey': "DestinationBucket",
                        'ParameterValue': self.destination_bucket
                    },
                    {
                        'ParameterKey': "DataBucket",
                        'ParameterValue': self.data_bucket
                    }
                ]
            )
        except ClientError as ce:
            print(ce)

    def update_stack(self):
        try:
            self.client_cloudformation.update_stack(
                StackName=self.stack_name,
                TemplateURL=self.template_url,
                Capabilities=['CAPABILITY_NAMED_IAM'],
                Parameters=[
                    {
                        'ParameterKey': "SourceBucket",
                        'ParameterValue': self.source_bucket
                    },
                    {
                        'ParameterKey': "DestinationBucket",
                        'ParameterValue': self.destination_bucket
                    },
                    {
                        'ParameterKey': "DataBucket",
                        'ParameterValue': self.data_bucket
                    }
                ]
            )
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'ValidationError':
                print("Stack Already Updated")
            else:
                print(ce)

    def status_stack(self):
        try:
            stack = self.client_cloudformation.describe_stacks(StackName=self.stack_name)
            status = stack['Stacks'][0]['StackStatus']
            return status
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'ValidationError':
                print("No stack present")
            else:
                print(ce)

    # delete all the objects from the bucket

    def delete_object(self, bucket_name):
        try:
            res = self.client_s3.list_objects(Bucket=bucket_name)
            for list_key in res['Contents']:
                self.client_s3.delete_object(Bucket=bucket_name, Key=list_key['Key'])
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'NoSuchBucket':
                print("No Bucket")
            else:
                print(ce)
        except Exception as e:
            print(e)
