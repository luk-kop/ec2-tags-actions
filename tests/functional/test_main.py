from ec2_tags import main


def test_main_single_instance_no_tags_stop(ec2_instance):
    """
    GIVEN Single instance without assigned tag.
    WHEN main() is called.
    THEN The stop action has been performed on given instance.
    """
    ec2_instance.start()
    main(aws_region='eu-west-1', ec2_action='stop', ec2_no_tags=True)
    assert ec2_instance.state['Name'] == 'stopped'


def test_main_single_instance_no_tags_terminate(ec2_instance):
    """
    GIVEN Single instance without assigned tag.
    WHEN main() is called.
    THEN The terminate action has been performed on given instance.
    """
    ec2_instance.start()
    main(aws_region='eu-west-1', ec2_action='terminate', ec2_no_tags=True)
    assert ec2_instance.state['Name'] == 'terminated'


def test_main_single_instance_no_tags_stop_no_action(ec2_instance_with_tag):
    """
    GIVEN Single instance with assigned tag.
    WHEN main() is called.
    THEN The NO action has been performed on given instance.
    """
    ec2_instance_with_tag.start()
    main(aws_region='eu-west-1', ec2_action='stop', ec2_no_tags=True)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_main_single_instance_no_tags_terminate_no_action(ec2_instance_with_tag):
    """
    GIVEN Single instance with assigned tag.
    WHEN main() is called.
    THEN The NO action has been performed on given instance.
    """
    ec2_instance_with_tag.start()
    main(aws_region='eu-west-1', ec2_action='terminate', ec2_no_tags=True)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_main_single_instance_no_name_tag_stop(ec2_instance):
    """
    GIVEN Single instance without assigned Name tag.
    WHEN main() is called.
    THEN The stop action has been performed on given instance.
    """
    ec2_instance.start()
    main(aws_region='eu-west-1', ec2_action='stop', ec2_no_name_tag=True)
    assert ec2_instance.state['Name'] == 'stopped'


def test_main_single_instance_no_name_tag_terminate(ec2_instance):
    """
    GIVEN Single instance without assigned Name tag.
    WHEN main() is called.
    THEN The stop action has been performed on given instance.
    """
    ec2_instance.start()
    main(aws_region='eu-west-1', ec2_action='terminate', ec2_no_name_tag=True)
    assert ec2_instance.state['Name'] == 'terminated'


def test_main_single_instance_specified_ec2_tag_stop(ec2_instance_with_tag):
    """
    GIVEN Single instance with specified tag assigned.
    WHEN main() is called.
    THEN The stop action has been performed on given instance.
    """
    ec2_instance_with_tag.start()
    ec2_tag_wanted = {
        'tag_key': 'Env',
        'tag_value': 'Production'
    }
    ec2_instance_with_tag.start()
    main(aws_region='eu-west-1', ec2_action='stop', ec2_tag=ec2_tag_wanted)
    assert ec2_instance_with_tag.state['Name'] == 'stopped'


def test_main_single_instance_specified_ec2_tag_terminate(ec2_instance_with_tag):
    """
    GIVEN Single instance with specified tag assigned.
    WHEN main() is called.
    THEN The stop action has been performed on given instance.
    """
    ec2_instance_with_tag.start()
    ec2_tag_wanted = {
        'tag_key': 'Env',
        'tag_value': 'Production'
    }
    main(aws_region='eu-west-1', ec2_action='terminate', ec2_tag=ec2_tag_wanted)
    assert ec2_instance_with_tag.state['Name'] == 'terminated'


def test_main_single_instance_with_other_tag_no_name_tag_stop(ec2_instance_with_tag):
    """
    GIVEN Single instance with assigned tags other than Name tag.
    WHEN main() is called.
    THEN The stop action has been performed on given instance.
    """
    ec2_instance_with_tag.start()
    main(aws_region='eu-west-1', ec2_action='stop', ec2_no_name_tag=True)
    assert ec2_instance_with_tag.state['Name'] == 'stopped'


def test_main_single_instance_with_other_tag_no_name_tag_terminate(ec2_instance_with_tag):
    """
    GIVEN Single instance with assigned tags other than Name tag.
    WHEN main() is called.
    THEN The terminate action has been performed on given instance.
    """
    ec2_instance_with_tag.start()
    main(aws_region='eu-west-1', ec2_action='terminate', ec2_no_name_tag=True)
    assert ec2_instance_with_tag.state['Name'] == 'terminated'


def test_main_single_instance_with_name_tag_no_name_tag_stop(ec2_resource, ec2_instance_with_tag):
    """
    GIVEN Single instance with assigned Name tag and one dummy tag.
    WHEN main() is called.
    THEN The NO action has been performed on given instance.
    """
    # Add Name tag to instance
    ec2_resource.create_tags(
        Resources=[ec2_instance_with_tag.id],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Dummy-instance'
            }
        ]
    )
    ec2_instance_with_tag.start()
    main(aws_region='eu-west-1', ec2_action='stop', ec2_no_name_tag=True)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_main_single_instance_with_name_tag_no_name_tag_terminate(ec2_resource, ec2_instance_with_tag):
    """
    GIVEN Single instance with assigned Name tag and one dummy tag.
    WHEN main() is called.
    THEN The NO action has been performed on given instance.
    """
    # Add Name tag to instance
    ec2_resource.create_tags(
        Resources=[ec2_instance_with_tag.id],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Dummy-instance'
            }
        ]
    )
    ec2_instance_with_tag.start()
    main(aws_region='eu-west-1', ec2_action='terminate', ec2_no_name_tag=True)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_main_single_instance_specified_ec2_tag_other_tag_stop(ec2_resource, ec2_instance_with_tag):
    """
    GIVEN Single instance with assigned tag other than wanted.
    WHEN main() is called.
    THEN The NO action has been performed on given instance.
    """
    # Add Name tag to instance
    ec2_resource.create_tags(
        Resources=[ec2_instance_with_tag.id],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Dummy-instance'
            }
        ]
    )
    ec2_instance_with_tag.start()
    ec2_tag_wanted = {
        'tag_key': 'Env',
        'tag_value': 'Staging'
    }
    main(aws_region='eu-west-1', ec2_action='terminate', ec2_tag=ec2_tag_wanted)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_main_single_instance_specified_ec2_tag_other_tag_terminate(ec2_resource, ec2_instance_with_tag):
    """
    GIVEN Single instance with assigned tag other than wanted.
    WHEN main() is called.
    THEN The NO action has been performed on given instance.
    """
    # Add Name tag to instance
    ec2_resource.create_tags(
        Resources=[ec2_instance_with_tag.id],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Staging'
            }
        ]
    )
    ec2_instance_with_tag.start()
    main(aws_region='eu-west-1', ec2_action='terminate', ec2_no_name_tag=True)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_main_single_instance_no_name_tag_stop_diff_region(ec2_instance_with_tag):
    """
    GIVEN Single instance with not assigned Name tag.
    WHEN main() is called with different region attr than EC2 instance.
    THEN The NO action has been performed on given instance.
    """
    # Start instance in other region
    ec2_instance_with_tag.start()
    main(aws_region='eu-west-2', ec2_action='stop', ec2_no_name_tag=True)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_main_single_instance_no_name_tag_terminate_diff_region(ec2_instance_with_tag):
    """
    GIVEN Single instance with not assigned Name tag.
    WHEN main() is called with different region attr than EC2 instance.
    THEN The NO action has been performed on given instance.
    """
    # Start instance in other region
    ec2_instance_with_tag.start()
    main(aws_region='eu-west-2', ec2_action='terminate', ec2_no_name_tag=True)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_main_single_instance_specified_ec2_tag_stop_diff_region(ec2_instance_with_tag):
    """
    GIVEN Single instance with assigned specified tag.
    WHEN main() is called with different region attr than EC2 instance.
    THEN The NO action has been performed on given instance.
    """
    # Start instance in other region
    ec2_instance_with_tag.start()
    ec2_tag_wanted = {
        'tag_key': 'Env',
        'tag_value': 'Production'
    }
    main(aws_region='eu-west-2', ec2_action='terminate', ec2_tag=ec2_tag_wanted)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_main_single_instance_specified_ec2_tag_terminate_diff_region(ec2_instance_with_tag):
    """
    GIVEN Single instance with assigned specified tag.
    WHEN main() is called with different region attr than EC2 instance.
    THEN The NO action has been performed on given instance.
    """
    # Start instance in other region
    ec2_instance_with_tag.start()
    ec2_tag_wanted = {
        'tag_key': 'Env',
        'tag_value': 'Production'
    }
    main(aws_region='eu-west-2', ec2_action='terminate', ec2_tag=ec2_tag_wanted)
    assert ec2_instance_with_tag.state['Name'] == 'running'


def test_main_multiple_instances_no_tags_stop(ec2_instance_multiple_instances_no_tags):
    """
    GIVEN Multiple instance without assigned tag.
    WHEN main() is called.
    THEN The stop action has been performed on all given instance.
    """
    ec2_instances = ec2_instance_multiple_instances_no_tags
    for ec2_instance in ec2_instances:
        ec2_instance.start()
    main(aws_region='eu-west-1', ec2_action='stop', ec2_no_tags=True)
    for ec2_instance in ec2_instances:
        assert ec2_instance.state['Name'] == 'stopped'


def test_main_multiple_instances_stopped_no_tags_terminate(ec2_instance_multiple_instances_no_tags):
    """
    GIVEN Multiple stopped instances without assigned tag.
    WHEN main() is called.
    THEN The terminate action has been performed on all given instance.
    """
    ec2_instances = ec2_instance_multiple_instances_no_tags
    for ec2_instance in ec2_instances:
        ec2_instance.stop()
    main(aws_region='eu-west-1', ec2_action='terminate', ec2_no_tags=True)
    for ec2_instance in ec2_instances:
        assert ec2_instance.state['Name'] == 'terminated'


def test_main_multiple_instances_no_tags_stop_not_all_instances(ec2_resource, ec2_instance_multiple_instances_no_tags):
    """
    GIVEN Multiple instances without assigned tag.
    WHEN main() is called.
    THEN The stop action has been performed on all instance without tags.
    """
    ec2_instances = ec2_instance_multiple_instances_no_tags
    for num, ec2_instance in enumerate(ec2_instances, 1):
        # Assign tag only to 1st instance
        if num == 1:
            # Store instance id for later test
            tagged_instance_id = ec2_instance.id
            ec2_resource.create_tags(
                Resources=[tagged_instance_id],
                Tags=[
                    {
                        'Key': 'Env',
                        'Value': 'Production'
                    }
                ]
            )
        ec2_instance.start()
    # Stop instances except instance with tagged_instance_id
    main(aws_region='eu-west-1', ec2_action='stop', ec2_no_tags=True)
    for ec2_instance in ec2_instances:
        if ec2_instance.id == tagged_instance_id:
            assert ec2_instance.state['Name'] == 'running'
        else:
            assert ec2_instance.state['Name'] == 'stopped'


def test_main_multiple_instances_no_name_tag_stop(ec2_resource, ec2_instance_multiple_instances_no_tags):
    """
    GIVEN Multiple instances - only two with assigned Name tag.
    WHEN main() is called.
    THEN The stop action has been performed on instance without Name tag.
    """
    ec2_instances = ec2_instance_multiple_instances_no_tags
    tagged_instance_ids = []
    for num, ec2_instance in enumerate(ec2_instances, 1):
        # Assign Name tag only to 1st nad 3rd instance
        if num in [1, 3]:
            # Store instance id for later test
            tagged_instance_ids.append(ec2_instance.id)
            ec2_resource.create_tags(
                Resources=[ec2_instance.id],
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': f'Dummy-instance-{num}'
                    }
                ]
            )
        ec2_instance.start()
    # Stop instances except instance without name tags (only 2nd instance)
    main(aws_region='eu-west-1', ec2_action='stop', ec2_no_name_tag=True)
    for ec2_instance in ec2_instances:
        if ec2_instance.id in tagged_instance_ids:
            assert ec2_instance.state['Name'] == 'running'
        else:
            assert ec2_instance.state['Name'] == 'stopped'


def test_main_multiple_instances_stopped_no_name_tag_terminate(ec2_resource, ec2_instance_multiple_instances_no_tags):
    """
    GIVEN Multiple stopped instances - only two with assigned Name tag.
    WHEN main() is called.
    THEN The stop action has been performed on instance without Name tag.
    """
    ec2_instances = ec2_instance_multiple_instances_no_tags
    tagged_instance_ids = []
    for num, ec2_instance in enumerate(ec2_instances, 1):
        # Assign Name tag only to 1st nad 3rd instance
        if num in [1, 3]:
            # Store instance id for later test
            tagged_instance_ids.append(ec2_instance.id)
            ec2_resource.create_tags(
                Resources=[ec2_instance.id],
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': f'Dummy-instance-{num}'
                    }
                ]
            )
        ec2_instance.stop()
    # Stop instances except instance without name tags (only 2nd instance)
    main(aws_region='eu-west-1', ec2_action='terminate', ec2_no_name_tag=True)
    for ec2_instance in ec2_instances:
        if ec2_instance.id in tagged_instance_ids:
            assert ec2_instance.state['Name'] == 'stopped'
        else:
            assert ec2_instance.state['Name'] == 'terminated'

