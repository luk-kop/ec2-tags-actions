import sys
from typing import Union

import boto3


def check_tag(tags: Union[list, None], tag_key: str, tag_value: str = '') -> bool:
    """
    Returns whether to perform action on the EC2 instance.
    Checks that any instance tags are assigned. Then verifies whether a tag with the given key or given key and value
    pair exists in the list of instance tags.
    """
    if not tags and not tag_key:
        # blad bo jezeli ma byc tylko usunieta instancja z konkretnym tagiem to sie wykona!!!
        return True
    for tag in tags:
        if not tag_key and not tag_value:
            return True
        elif tag_value:
            if tag.get('Key') == tag_key and tag.get('Value') == tag_value:
                return True
        else:
            if tag.get('Key') == tag_key:
                return True
    return False


def check_proper_ec2_state(action: str, ec2_current_state: str) -> bool:
    """
    Checks whether the EC2 instance is in desired state.
    """
    if action == 'terminate':
        return ec2_current_state not in ['terminated', 'shutting-down']
    elif action == 'stop':
        return ec2_current_state not in ['terminated', 'shutting-down', 'stopping', 'stopped']
    return False


def is_action_allowed(action: str) -> None:
    """
    Checks whether given EC2 action is allowed.
    """
    allowed_ec2_actions = ['stop', 'terminate']
    if action not in allowed_ec2_actions:
        print('Not allowed "ec2_action" value')
        sys.exit()


if __name__ == '__main__':
    aws_region_name = 'eu-west-1'
    # Action that should be performed on the EC2 instances
    ec2_action = 'terminate'

    # Tag to check - default not tags (action on instances without tags)
    ec2_tag = {
        'tag_key': 'Environment',
        'tag_value': 'Test',
    }

    # Get all EC2 instances in specified AWS region
    ec2 = boto3.resource('ec2', region_name=aws_region_name)
    ec2_instances_all = ec2.instances.all()

    for instance in ec2_instances_all:
        # Verify instance tag
        instance_tag_status: bool = check_tag(tags=instance.tags, **ec2_tag)

        instance_state = instance.state['Name']
        print(f'{instance.id}, {instance_state}, instance_tags: {instance.tags}, tag_status: {instance_tag_status}')

        if instance_tag_status:
            if ec2_action == 'terminate' and instance_state not in ['terminated', 'shutting-down']:
                instance.terminate()
                print(f'Instance with id "{instance.id}" terminated...')
            elif ec2_action == 'stop' and instance_state not in ['terminated', 'shutting-down', 'stopping', 'stopped']:
                instance.stop()
                print(f'Instance with id "{instance.id}" stopped...')
