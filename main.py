import sys

import boto3
from botocore.exceptions import ClientError


def check_tag_exist(tags: list, tag_key: str, tag_value: str = '') -> bool:
    """
    Checks whether a specified tag is in the list of given tags.
    """
    for tag in tags:
        if tag_value:
            if tag.get('Key') == tag_key and tag.get('Value') == tag_value:
                return True
        else:
            if tag.get('Key') == tag_key:
                return True
    return False


def check_proper_instance_state(action: str, ec2_current_state: str) -> bool:
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


def perform_action_on_instance(action: str, instance, **kwargs) -> bool:
    """
    Performs the specified action (stop or terminate) on the EC2 instance if necessary.
    Returns True if the action was performed on the EC2 instance.
    """
    instance_tags = instance.tags
    take_action = False
    # Get additional attrs
    no_tags: bool = kwargs.get('ec2_no_tags', False)
    no_name_tag: bool = kwargs.get('ec2_no_name_tag', False)
    specified_tag: dict = kwargs.get('ec2_tag', {})
    if no_tags and not instance_tags:
        # Perform an action if EC2 instance has NO tag assigned
        take_action = True
    elif no_name_tag:
        # Perform an action ONLY if tag "Name" IS NOT assigned to EC2 instance
        if instance_tags:
            take_action = not check_tag_exist(tags=instance_tags, tag_key='Name')
        else:
            take_action = True
    elif specified_tag and instance_tags:
        # Perform an action ONLY if specified tag IS assigned to EC2 instance
        take_action = check_tag_exist(tags=instance_tags, **specified_tag)
    if not take_action:
        return take_action
    # Take action on EC2 instance if necessary
    if action == 'terminate':
        instance.terminate()
        print(f'Instance with id "{instance.id}" terminated...')
    else:
        try:
            instance.stop()
            print(f'Instance with id "{instance.id}" stopped...')
        except ClientError as err:
            # Handle exception when instance in 'pending' state.
            error_msg = err.response['Error']['Message']
            print(f'Error: {error_msg}. Try later...')
    return take_action


def main(aws_region, ec2_action, **kwargs) -> None:
    """
    Script's main func.
    """
    is_action_allowed(action=ec2_action)
    # Get additional func args
    additional_args = kwargs
    # Get all EC2 instances in specified AWS region
    ec2 = boto3.resource('ec2', region_name=aws_region)
    ec2_instances_all = ec2.instances.all()

    for instance in ec2_instances_all:
        instance_current_state = instance.state['Name']
        instance_proper_state: bool = check_proper_instance_state(action=ec2_action, ec2_current_state=instance_current_state)
        print(f'{instance.id}, {instance_current_state}, instance_tags: {instance.tags}')   # For tests
        # Perform action on EC2 instance if it is in the correct state
        if instance_proper_state:
            action_taken: bool = perform_action_on_instance(action=ec2_action, instance=instance, **additional_args)
    if 'action_taken' not in locals() or not action_taken:
        print('Nothing to do...')


if __name__ == '__main__':
    aws_region_name = 'eu-west-1'
    # Action that should be performed on the EC2 instances
    ec2_action = 'stop'

    main_attrs = {
        'aws_region': aws_region_name,
        'ec2_action': ec2_action
    }

    main_attrs['ec2_no_tags'] = True
    # main_attrs['ec2_no_name_tag'] = True
    # main_attrs['ec2_tag'] = {
    #     'tag_key': 'Name',
    #     'tag_value': 'test1'
    # }
    # Run script's main func
    main(**main_attrs)

