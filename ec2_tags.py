import sys
from typing import TypeVar
import argparse

import boto3
from botocore.exceptions import ClientError


# Declare type variable for boto3.resources.factory.ec2.Instance
Ec2Instance = TypeVar('Ec2Instance', bound='boto3.resources.factory.ec2.Instance')


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
        print('Not allowed "ec2_action" value!')
        sys.exit()


def perform_action_on_instance(action: str, instance: Ec2Instance, **kwargs) -> bool:
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
    # Helper variable indicating whether an action has been performed on any instance
    ec2_instance_action_taken = False
    for instance in ec2_instances_all:
        instance_current_state = instance.state['Name']
        instance_proper_state: bool = check_proper_instance_state(action=ec2_action, ec2_current_state=instance_current_state)
        # print(f'{instance.id}, {instance_current_state}, instance_tags: {instance.tags}')   # For tests
        # Perform action on EC2 instance if it is in the correct state
        if instance_proper_state:
            instance_state_changed: bool = perform_action_on_instance(action=ec2_action,
                                                                      instance=instance,
                                                                      **additional_args)
            if instance_state_changed:
                ec2_instance_action_taken = True
    if not ec2_instance_action_taken:
        print('Nothing to do...')


if __name__ == '__main__':
    aws_region_default = 'eu-west-1'

    parser = argparse.ArgumentParser(description='The EC2 tags actions script')
    # Positional argument
    parser.add_argument('action', choices=['stop', 'terminate'], help='action to be performed on instances')
    parser.add_argument('-r', '--region', default=aws_region_default, type=str,
                        help=f'AWS region in which instances are deployed (default: {aws_region_default})')
    # 1st "mutually exclusive" group of args
    parser.add_argument('-n', '--no-name', action='store_true', help='perform action on instances without Name tag')
    # 2nd "mutually exclusive" group of args
    parser.add_argument('-k', '--tag-key', type=str, help='perform action on instances with specified tag key')
    parser.add_argument('-v', '--tag-value', type=str, help='perform action on instances with specified tag value')

    args = parser.parse_args()
    # Simple mutually exclusive check - ec2_tags [-n | [-k abc -v def]]
    if args.no_name and (args.tag_key or args.tag_value):
        parser.error('-n/--no-name and pair of -k/--tag-key, -v/--tag-value are mutually exclusive')
        sys.exit()
    # Checks whether -k and -v tags have been specified together
    if bool(args.tag_key) ^ bool(args.tag_value):
        parser.error('-k/--tag-key and -v/--tag-value must be given together')
        sys.exit()

    # Get data from argparse
    main_attrs = {
        'aws_region': args.region,
        'ec2_action': args.action
    }
    if args.no_name:
        main_attrs['ec2_no_name_tag'] = args.no_name
    elif args.tag_key and args.tag_value:
        main_attrs['ec2_tag'] = {
            'tag_key': args.tag_key,
            'tag_value': args.tag_value
        }
    else:
        # Default option - EC2 instances without assigned tags
        main_attrs['ec2_no_tags'] = True

    # Run script's main func
    main(**main_attrs)

