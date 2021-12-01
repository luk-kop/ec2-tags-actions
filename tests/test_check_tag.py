from main import check_tag


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
    assert check_tag(tags=dummy_tags, tag_key='Project', tag_value='ansible-lab')


def test_check_tag_false_wrong_value():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag() is called.
    THEN The key with the given value is not in the provided tags list.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert not check_tag(tags=dummy_tags, tag_key='Project', tag_value='ansible-lab1')


def test_check_tag_false_wrong_key():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag() is called.
    THEN The key with the given value is not in the provided tags list.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert not check_tag(tags=dummy_tags, tag_key='Project1', tag_value='ansible-lab')


def test_check_tag_false_wrong_key_and_value():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag() is called.
    THEN The key with the given value is not in the provided tags list.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert not check_tag(tags=dummy_tags, tag_key='Project1', tag_value='ansible-lab1')


def test_check_tag_no_ec2_tags():
    """
    GIVEN Empty list of EC2 instance tags.
    WHEN check_tag() is called.
    THEN The key with the given value is in the provided tags list.
    """
    dummy_tags = []
    assert not check_tag(tags=dummy_tags, tag_key='Project', tag_value='ansible-lab')


def test_check_tag_only_key_true():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag() is called.
    THEN The key is in the provided tags list.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert check_tag(tags=dummy_tags, tag_key='Project', tag_value='')
    assert check_tag(tags=dummy_tags, tag_key='Project')


def test_check_tag_only_key_false():
    """
    GIVEN List of EC2 instance tags.
    WHEN check_tag() is called.
    THEN The key is not in the provided tags list.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert not check_tag(tags=dummy_tags, tag_key='Project1', tag_value='')
    assert not check_tag(tags=dummy_tags, tag_key='Project1')


def test_check_tag_default():
    """
    GIVEN List of EC2 instance tags and the tag with default key & value.
    WHEN check_tag() is called.
    THEN True - because the EC2 instance has tags assigned to it.
    """
    dummy_tags = [
        {'Key': 'Environment', 'Value': 'dev'},
        {'Key': 'Project', 'Value': 'ansible-lab'},
        {'Key': 'Name', 'Value': 'ansible-0'}
    ]
    assert check_tag(tags=dummy_tags, tag_key='', tag_value='')


def test_check_tag_default_no_ec2_tags():
    """
    GIVEN Empty list of EC2 instance tags and the tag with default key & value.
    WHEN check_tag() is called.
    THEN True - because the EC2 instance has NO tags assigned to it.
    """
    dummy_tags = []
    ec2_tag = {
        'tag_key': '',
        'tag_value': '',
    }
    assert not check_tag(tags=dummy_tags, **ec2_tag)