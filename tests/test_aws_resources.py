from ec2_tags import check_aws_region, perform_action_on_instance


def test_check_aws_region_all_valid(ec2_instance):
    """
    GIVEN List of valid AWS region names.
    WHEN check_aws_region() is called.
    THEN All given region names are valid.
    """
    aws_region_names_valid = ['us-west-1', 'us-east-1', 'eu-north-1', 'ap-south-1', 'eu-central-1']
    for region in aws_region_names_valid:
        assert check_aws_region(region_specified=region)


def test_check_aws_region_partially_valid(ec2_instance):
    """
    GIVEN List containing a values that are not a valid AWS region.
    WHEN check_aws_region() is called.
    THEN All given region names are NOT valid.
    """
    aws_region_names_valid = ['eu-north-xxx', 'ap-south-341', 'eu-central-123']
    for region in aws_region_names_valid:
        assert not check_aws_region(region_specified=region)


def test_perform_action_on_instance_stop(ec2_resource, ec2_instance):
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
