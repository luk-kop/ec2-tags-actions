import sys

import boto3


def check_tag(tags: list, tag_key: str, tag_value: str) -> bool:
    """
    Checks whether a tag with the given key and value exists in the list of instance tags.
    """
    for tag in tags:
        if tag.get('Key') == tag_key and tag.get('Value') == tag_value:
            return True
    return False


def test_check_tag_true():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag() is called.
    THEN The key with the given value is in the provided tags list.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert check_tag(tags=dummy_tags, tag_key='Project',tag_value='ansible-lab')


if __name__ == '__main__':
    aws_region_name = 'eu-west-1'
    # Action that should be performed on the EC2 instances
    ec2_action = 'stop'

    allowed_ec2_actions = ['stop', 'terminate']
    if ec2_action not in allowed_ec2_actions:
        print('Not allowed "ec2_action" value')
        sys.exit()

    # Get all EC2 instances in specified AWS region
    ec2 = boto3.resource('ec2', region_name=aws_region_name)
    ec2_instances_all = ec2.instances.all()

    for instance in ec2_instances_all:
        print(instance.state['Name'])   # Only for tests
        if instance.state['Name'] not in ['terminated', 'shutting-down'] and not instance.tags:
            print(f'id={instance.id}, public DNS={instance.public_dns_name}, state={instance.state}')
