# Lambda function to copy a file from a s3 to another
This project create 2 s3 bucket: source bucket and destination bucket. when a object is uploaded in source bucket it invokes the lambda function which copies that file from source bucket to destination bucket.

# Files
- **helper.py** - This file has the main function of the project. Flow of main the function -
    - Definition of all the parameter used in the project.
    - Upload the template and job scripts to s3 bucket.
    - Creating or updating stack.
- **stack.py** - This file contains a Stack class which handles all the stack functions like create, delete and  update a stack using boto3.
- **function.py** - Comprises of upload functions like upload a folder, file or zip file to s3.
- **template.ymal** - A cloudforamtion template which comprises of configuration of source bucket, destination bucket, lambda role, lambda function.