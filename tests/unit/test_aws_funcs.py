from ec2_tags import check_aws_region, perform_action_on_instance


def test_check_aws_region_all_valid(ec2_resource):
    """
    GIVEN List of valid AWS region names.
    WHEN check_aws_region() is called.
    THEN All given region names are valid.
    """
    aws_region_names_valid = ['us-west-1', 'us-east-1', 'eu-north-1', 'ap-south-1', 'eu-central-1']
    for region in aws_region_names_valid:
        assert check_aws_region(region_specified=region)


def test_check_aws_region_partially_valid(ec2_resource):
    """
    GIVEN List containing a values that are not a valid AWS region.
    WHEN check_aws_region() is called.
    THEN All given region names are NOT valid.
    """
    aws_region_names_valid = ['eu-north-xxx', 'ap-south-341', 'eu-central-123']
    for region in aws_region_names_valid:
        assert not check_aws_region(region_specified=region)


def test_perform_action_on_instance_specified_ec2_tag_stop(ec2_resource, ec2_instance):
    """
    GIVEN Instance with assigned tag.
    WHEN perform_action_on_instance() is called.
    THEN The stop action has been performed on given instance.
    """
    # Add Name tag to instance
    ec2_resource.create_tags(
        Resources=[ec2_instance.id],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Dummy-Instance'
            }
        ]
    )
    ec2_instance.start()
    ec2_tag_wanted = {
        'tag_key': 'Name',
        'tag_value': 'Dummy-Instance'
    }
    assert perform_action_on_instance(action='stop', instance=ec2_instance, ec2_tag=ec2_tag_wanted)
    assert ec2_instance.state['Name'] == 'stopped'


def test_perform_action_on_instance_specified_ec2_tag_terminate(ec2_resource, ec2_instance):
    """
    GIVEN Instance with assigned tag.
    WHEN perform_action_on_instance() is called.
    THEN The terminate action has been performed on given instance.
    """
    # Add Name tag to instance
    ec2_resource.create_tags(
        Resources=[ec2_instance.id],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Dummy-Instance'
            }
        ]
    )
    ec2_instance.start()
    ec2_tag_wanted = {
        'tag_key': 'Name',
        'tag_value': 'Dummy-Instance'
    }
    assert perform_action_on_instance(action='terminate', instance=ec2_instance, ec2_tag=ec2_tag_wanted)
    assert ec2_instance.state['Name'] == 'terminated'


def test_perform_action_on_instance_no_tags_stop(ec2_resource, ec2_instance):
    """
    GIVEN Instance without assigned tag.
    WHEN perform_action_on_instance() is called.
    THEN The stop action has been performed on given instance.
    """
    ec2_instance.start()
    assert perform_action_on_instance(action='stop', instance=ec2_instance, ec2_no_tags=True)
    assert ec2_instance.state['Name'] == 'stopped'


def test_perform_action_on_instance_no_tags_terminate(ec2_instance):
    """
    GIVEN Instance without assigned tag.
    WHEN perform_action_on_instance() is called.
    THEN The terminate action has been performed on given instance.
    """
    ec2_instance.start()
    assert perform_action_on_instance(action='terminate', instance=ec2_instance, ec2_no_tags=True)
    assert ec2_instance.state['Name'] == 'terminated'


def test_perform_action_on_instance_no_name_tag_terminate(ec2_instance):
    """
    GIVEN Instance without assigned Name tag.
    WHEN perform_action_on_instance() is called.
    THEN The terminate action has been performed on given instance.
    """
    ec2_instance.start()
    assert perform_action_on_instance(action='terminate', instance=ec2_instance, ec2_no_name_tag=True)
    assert ec2_instance.state['Name'] == 'terminated'


def test_perform_action_on_instance_no_name_tag_stop(ec2_instance):
    """
    GIVEN Instance without assigned Name tag.
    WHEN perform_action_on_instance() is called.
    THEN The stop action has been performed on given instance.
    """
    ec2_instance.start()
    assert perform_action_on_instance(action='stop', instance=ec2_instance, ec2_no_name_tag=True)
    assert ec2_instance.state['Name'] == 'stopped'


def test_perform_action_on_instance_no_action_name_tag_terminate(ec2_resource, ec2_instance):
    """
    GIVEN Instance with assigned Name tag.
    WHEN perform_action_on_instance() is called.
    THEN No action has been performed on given instance.
    """
    # Add Name tag to instance
    ec2_resource.create_tags(
        Resources=[ec2_instance.id],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Dummy-Instance'
            }
        ]
    )
    ec2_instance.start()
    assert not perform_action_on_instance(action='terminate', instance=ec2_instance, ec2_no_name_tag=True)
    assert ec2_instance.state['Name'] == 'running'


def test_perform_action_on_instance_no_action_name_tag_stop(ec2_resource, ec2_instance):
    """
    GIVEN Instance with assigned Name tag.
    WHEN perform_action_on_instance() is called.
    THEN No action has been performed on given instance.
    """
    # Add Name tag to instance
    ec2_resource.create_tags(
        Resources=[ec2_instance.id],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Dummy-Instance'
            }
        ]
    )
    ec2_instance.start()
    assert not perform_action_on_instance(action='stop', instance=ec2_instance, ec2_no_name_tag=True)
    assert ec2_instance.state['Name'] == 'running'


def test_perform_action_on_instance_no_action_no_tags_stop(ec2_instance_with_tag):
    """
    GIVEN Instance with assigned tag.
    WHEN perform_action_on_instance() is called.
    THEN No action has been performed on given instance.
    """
    ec2_instance_with_tag.start()
    assert not perform_action_on_instance(action='stop', instance=ec2_instance_with_tag, ec2_no_tags=True)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_perform_action_on_instance_no_action_no_tags_terminate(ec2_instance_with_tag):
    """
    GIVEN Instance with assigned tag.
    WHEN perform_action_on_instance() is called.
    THEN No action has been performed on given instance.
    """
    ec2_instance_with_tag.start()
    assert not perform_action_on_instance(action='terminate', instance=ec2_instance_with_tag, ec2_no_tags=True)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_perform_action_on_instance_no_action_specified_ec2_tag_terminate(ec2_instance_with_tag):
    """
    GIVEN Instance with assigned tag.
    WHEN perform_action_on_instance() is called.
    THEN No action has been performed on given instance.
    """
    ec2_instance_with_tag.start()
    ec2_tag_wanted = {
        'tag_key': 'Env',
        'tag_value': 'Staging'
    }
    assert not perform_action_on_instance(action='terminate', instance=ec2_instance_with_tag, ec2_tag=ec2_tag_wanted)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_perform_action_on_instance_no_action_specified_ec2_tag_stop(ec2_instance_with_tag):
    """
    GIVEN Instance with assigned tag.
    WHEN perform_action_on_instance() is called.
    THEN No action has been performed on given instance.
    """
    ec2_instance_with_tag.start()
    ec2_tag_wanted = {
        'tag_key': 'Env',
        'tag_value': 'Staging'
    }
    assert not perform_action_on_instance(action='stop', instance=ec2_instance_with_tag, ec2_tag=ec2_tag_wanted)
    assert ec2_instance_with_tag.state['Name'] == 'running'
