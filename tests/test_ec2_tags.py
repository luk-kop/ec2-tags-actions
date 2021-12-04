from ec2_tags import check_tag_exist


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
