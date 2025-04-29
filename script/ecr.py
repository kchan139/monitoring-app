"""
This script creates an Amazon ECR repository and should only be run once.
"""

import boto3

ecr_client = boto3.client('ecr')

repository_name = 'monitoring-app'
response = ecr_client.create_repository(repositoryName=repository_name)

repository_uri = response['repository']['repositoryUri']
print(repository_uri)