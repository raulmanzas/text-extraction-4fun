#!/usr/bin/python3.7


import uuid
import json
import boto3
import click
import pandas as pd


BUCKET_NAME = 'NAME-YOUR-BUCKET-HERE' # replace this 
REGION = 'us-west-1'


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


def extract_text(s3_key):
    client = boto3.client('textract', region_name=REGION)
    print('>> calling textract...')
    response = client.analyze_document(
        Document={
            'S3Object': {
            'Bucket': BUCKET_NAME,
            'Name': s3_key
            }
        },
        FeatureTypes=['FORMS', 'TABLES']
    )
    print_summary(response)
    return json.dumps(response)


@click.command()
@click.argument('file_path')
def main(file_path):
    s3_key = upload_doc_to_bucket(file_path)
    extracted_text = extract_text(s3_key)
    with open('output.json', 'w') as output:
        output.write(extracted_text)
    print('>> raw extracted text output available on "output.json"')


if __name__ == '__main__':
    main()
