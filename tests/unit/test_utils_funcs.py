import pytest

from ec2_tags import check_tag_exist, is_action_allowed, check_proper_instance_state


def test_check_tag_exist_true():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag_exist() is called.
    THEN The key with the given value is in the provided tags list.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert check_tag_exist(tags=dummy_tags, tag_key='Project', tag_value='ansible-lab')


def test_check_tag_exist_false_wrong_value():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag_exist() is called.
    THEN The key with the given value is not in the provided tags list.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert not check_tag_exist(tags=dummy_tags, tag_key='Project', tag_value='ansible-lab1')


def test_check_tag_exist_false_wrong_key():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag_exist() is called.
    THEN The key with the given value is not in the provided tags list.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert not check_tag_exist(tags=dummy_tags, tag_key='Project1', tag_value='ansible-lab')


def test_check_tag_exist_false_wrong_key_and_value():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag_exist() is called.
    THEN The key with the given value is not in the provided tags list.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert not check_tag_exist(tags=dummy_tags, tag_key='Project1', tag_value='ansible-lab1')


def test_check_tag_exist_instance_with_no_tags():
    """
    GIVEN Empty list of EC2 instance tags.
    WHEN check_tag_exist() is called.
    THEN False - because the EC2 instance has NO tags assigned to it.
    """
    dummy_tags = []
    assert not check_tag_exist(tags=dummy_tags, tag_key='Project', tag_value='ansible-lab')


def test_check_tag_exist_only_key_true():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag_exist() is called.
    THEN The key is on the provided list of tags.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert check_tag_exist(tags=dummy_tags, tag_key='Project', tag_value='')
    assert check_tag_exist(tags=dummy_tags, tag_key='Project')


def test_check_tag_exist_only_key_false():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag_exist() is called.
    THEN The key is NOT on the provided list of tags.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert not check_tag_exist(tags=dummy_tags, tag_key='Project1', tag_value='')
    assert not check_tag_exist(tags=dummy_tags, tag_key='Project1')


def test_is_action_allowed_true():
    """
    GIVEN List of allowed EC2 actions.
    WHEN is_action_allowed() is called.
    THEN None is returned.
    """
    for action in ['stop', 'terminate']:
        assert is_action_allowed(action=action) is None


def test_is_action_allowed_false():
    """
    GIVEN List of NOT allowed EC2 actions.
    WHEN is_action_allowed() is called.
    THEN sys.exit() is called with exit code = 1 .
    """

    for action in ['update', 'destroy']:
        # SystemExit should be raised
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            is_action_allowed(action=action)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1


def test_check_proper_instance_state_terminate_true():
    """
    GIVEN List of allowed EC2 states and 'terminate' action.
    WHEN check_proper_instance_state() is called.
    THEN True is returned.
    """
    for state in ['pending', 'running', 'stopping', 'stopped']:
        assert check_proper_instance_state(action='terminate', ec2_current_state=state)


def test_check_proper_instance_state_terminate_false():
    """
    GIVEN List of NOT allowed EC2 states and 'terminate' action.
    WHEN check_proper_instance_state() is called.
    THEN False is returned.
    """
    for state in ['terminated', 'shutting-down', 'test', 'down', 'xxxx']:
        assert not check_proper_instance_state(action='terminate', ec2_current_state=state)


def test_check_proper_instance_state_stop_true():
    """
    GIVEN List of allowed EC2 states and 'terminate' action.
    WHEN check_proper_instance_state() is called.
    THEN True is returned.
    """
    for state in ['pending', 'running']:
        assert check_proper_instance_state(action='stop', ec2_current_state=state)


def test_check_proper_instance_state_stop_false():
    """
    GIVEN List of NOT allowed EC2 states and 'terminate' action.
    WHEN check_proper_instance_state() is called.
    THEN False is returned.
    """
    for state in ['shutting-down', 'terminated', 'stopping', 'stopped', 'test', 'down', 'xxxx']:
        assert not check_proper_instance_state(action='stop', ec2_current_state=state)