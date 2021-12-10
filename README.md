# EC2 tags actions

[![Python 3.8.10](https://img.shields.io/badge/python-3.8.5-blue.svg)](https://www.python.org/downloads/release/python-377/)
[![Boto3](https://img.shields.io/badge/Boto3-1.20.14-blue.svg)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

> The **EC2 tags actions** is a simple script that allows you to perform selected actions on EC2 instances based on instance tags.

## Features
- EC2 instances in the selected AWS region can be **stopped**, **terminated** or only **listed** based on the tags assigned to them.
- The script can perform an action on one of the following groups::
  - EC2 instances **without assigned tags** (default option);
  - EC2 instances **without assigned `Name` tag**;
  - EC2 instances **with specified tag** (tag key and tag value).
- You can execute the script with the following arguments:
  - **mandatory**:
    - AWS region name (`-r` or `--region`, default `eu-west-1`);
    - action to be performed on EC2 instances (`stop`, `terminate` or `list`).
  - **optional**:
    - tag key (`-k` or `--tag-key`);
    - tag value (`-v` or `--tag-value`);
    - no `Name` tag (`-n` or `--no-name`).
- Running the script without optional arguments will perform actions on **EC2 instances that have not been assigned any tags**.
- As a result of invoking the script you will get the EC2 instance ids, against which the action was taken (if any).

## Requirements
- Python third party packages: [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- Before using the script, you need to set up default AWS region value and valid authentication credentials for your AWS account (programmatic access) using either the IAM Management Console or the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html) tool.
- The entity running the script should have the appropriate permissions to stop or terminate EC2 instances.

## Installation with venv
The script can be run locally with virtualenv tool. Run following commands in order to create virtual environment and install the required packages.
```bash
$ virtualenv venv
# or
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Running the script
Script usage (detailed help):
```bash
(venv) $ python ec2_tags.py --help
usage: ec2_tags.py [-h] [-r REGION] [-n] [-k TAG_KEY] [-v TAG_VALUE] {stop,terminate,list}

The EC2 tags actions script

positional arguments:
  {stop,terminate}      action to be performed on instances

optional arguments:
  -h, --help            show this help message and exit
  -r REGION, --region REGION
                        AWS region in which instances are deployed (default: eu-west-1)
  -n, --no-name         perform action on instances without Name tag
  -k TAG_KEY, --tag-key TAG_KEY
                        perform action on instances with specified tag key
  -v TAG_VALUE, --tag-value TAG_VALUE
                        perform action on instances with specified tag value

```
You can start the script using one of the following examples:
```bash
# Run script with default options (AWS region: eu-west-1, action on EC2 instances without assigned tags).
(venv) $ python ec2_tags.py stop
# You should get the similar output:
Instance with id "i-12345678901234567" stopped...
Instance with id "i-01234567890123456" stopped...
# or if no action has been taken
Nothing to do...

# List EC2 instances in us-east-1 region without Name tag assigned.
python ec2_tags.py --no-name list

# Terminate EC2 instances in default region (eu-west-1) without Name tag assigned.
python ec2_tags.py --no-name terminate

# Stop EC2 instances in us-east-1 region with tag - Key: Project and Value: Carrot assigned.
python ec2_tags.py --region us-east-1 --tag-key Project --tag-value Carrot stop

# Terminate EC2 instances in default region (eu-west-1) with tag - Key: Env and Value: Test assigned.
python ec2_tags.py --tag-key Env --tag-value Test terminate
```