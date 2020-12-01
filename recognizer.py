#!/usr/bin/python3.7

import uuid
import json
import time
import boto3
import click
import pandas as pd


BUCKET_NAME = 'NAME-YOUR-BUCKET-HERE' # replace this 
REGION = 'us-west-1'

# replace the vars below if you want to run async operations
SNS_TOPIC_ARN = 'YOUR_TOPIC_ARN'
TEXTRACT_ROLE_ARN = 'YOUR_ROLE_ARN'


def upload_doc_to_bucket(file_path):
    client = boto3.client('s3')
    new_file_name = f'{uuid.uuid4()}.{file_path.split(".")[-1]}'
    client.upload_file(file_path, BUCKET_NAME, new_file_name)
    print('>> document uploaded to s3 successfully!')
    return new_file_name


def print_summary(response):
    line_blocks = [block for block in response['Blocks'] if block['BlockType'] == 'LINE']
    summary_matrix = [[block['Text'], block['Confidence']] for block in line_blocks]
    df = pd.DataFrame(summary_matrix, columns=['Identified Text', 'Confidence'])
    # you can do whatever with this df now
    print(df)


def analyze_text(s3_key):
    client = boto3.client('textract', region_name=REGION)
    print('>> calling textract...')
    response = client.analyze_document(
        Document={
            'S3Object': {
            'Bucket': BUCKET_NAME,
            'Name': s3_key
            }
        },
        FeatureTypes=['TABLES']
    )
    print_summary(response)
    return json.dumps(response)


def wait_for_a_while():
    # ideally, you should access the SQS queue to check when the job is done,
    # but for the purposes of testing, just waiting a little is more than enough
    print('>> waiting a few seconds to give it a chance to finish...')
    time.sleep(10)


def async_detect_text(s3_key):
    client = boto3.client('textract', region_name=REGION)
    print('>> calling textract...')
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
            'Bucket': BUCKET_NAME,
            'Name': s3_key
            }
        },
        NotificationChannel={
            'SNSTopicArn': SNS_TOPIC_ARN,
            'RoleArn': TEXTRACT_ROLE_ARN
        }
    )
    print(f'>> JobId: {response["JobId"]}')
    wait_for_a_while()
    response = client.get_document_text_detection(JobId=response['JobId'])
    print_summary(response)
    return json.dumps(response)


@click.command()
@click.argument('file_path')
def main(file_path):
    s3_key = upload_doc_to_bucket(file_path)
    extracted_text = async_detect_text(s3_key)
    with open('output.json', 'w') as output:
        output.write(extracted_text)
    print('>> raw extracted text output available on "output.json"')


if __name__ == '__main__':
    main()
