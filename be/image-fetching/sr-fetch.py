import boto3
import os
client_key = os.environ['AWS_CLIENT_KEY']
secret_key = os.environ['AWS_SECRET_KEY']

session = boto3.Session(aws_access_key_id=client_key, aws_secret_access_key=secret_key)
s3client = session.client('s3')

def getObject(client, path):
    return client.get_object(Bucket='usgs-landsat', RequestPayer='requester', Key=path)['Body'].read()