from pytest import fixture
import os

import boto3
from moto import mock_ec2


@fixture
def aws_credentials():
    """
    Mocked AWS Credentials for moto.
    """
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-1'


@fixture
def ec2_resource(aws_credentials):
    """
    Create mocked EC2 service resource.
    """
    with mock_ec2():
        yield boto3.resource('ec2')


@fixture
def ec2_client(aws_credentials):
    """
    Create mocked EC2 service client.
    """
    with mock_ec2():
        yield boto3.client('ec2')


@fixture
def ec2_instance(ec2_resource, ec2_client):
    """
    Dummy EC2 instance.
    """
    # Get image id
    image_id = ec2_client.describe_images()['Images'][0]['ImageId']
    # Create dummy instance
    instances = ec2_resource.create_instances(ImageId=image_id, MinCount=1, MaxCount=1)
    yield instances[0]


@fixture
def ec2_instance_with_tag(ec2_resource, ec2_client):
    """
    Dummy EC2 instance with tag.
    """
    # Get image id
    image_id = ec2_client.describe_images()['Images'][0]['ImageId']
    # Create dummy instance
    instances = ec2_resource.create_instances(ImageId=image_id, MinCount=1, MaxCount=1)
    single_instance = instances[0]
    # Add tag to instance
    ec2_resource.create_tags(
        Resources=[single_instance.id],
        Tags=[
            {
                'Key': 'Env',
                'Value': 'Production'
            }
        ]
    )
    yield single_instance


@fixture
def ec2_instance_multiple_instances_no_tags(ec2_resource, ec2_client):
    """
    Dummy EC2 instances without tags.
    """
    # Get image id
    image_id = ec2_client.describe_images()['Images'][0]['ImageId']
    # Create dummy instance
    instances = ec2_resource.create_instances(ImageId=image_id, MinCount=3, MaxCount=3)
    yield instances
