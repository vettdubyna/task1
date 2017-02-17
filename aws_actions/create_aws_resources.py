#!/usr/bin/python

from fabric.api import *
import boto3
import os
import sys
import json
import time

def create_ec2_instance(params, instance_tag, role):
    try:
        ec2 = boto3.resource('ec2')
        security_group_id = []
        security_group_id.append(params["security_group_id"])
        image_id = params["image_id"]
        instance_type = params["instance_type"]
        subnet_id = params["subnet_id"]
        key_name = params["key_name"]
        instances = ec2.create_instances(ImageId = image_id, MinCount=1, MaxCount=1,
                                        KeyName = key_name,
                                        SecurityGroupIds = security_group_id,
                                        InstanceType = instance_type,
                                        SubnetId = subnet_id,
                                        IamInstanceProfile={'Name': role}
                                        )
        print "Waiting for instance become running"
        for instance in instances:
            instance.wait_until_running()
            instance.create_tags(Tags=[{'Key': 'Name', 'Value': 'Instance_task1'}])
            return instance.id
    except Exception as e:
        print "Error: " + str(e)
        sys.exit(1)

def create_s3(bucket_name, tag, region):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        tagging = bucket.Tagging()
        tagging.put(Tagging={'TagSet': [tag]})
        tagging.reload()
        return bucket.name
    except Exception as e:
        print "Error: " + str(e)
        sys.exit(1)

def generate_json_policy(bucket_name):
    try:
        file_name = "policy.json"
        policy = {}
        action1 = ['s3:ListBucket']
        action2 = ["s3:PutObject", "s3:GetObject","s3:DeleteObject","s3:ListObject"]
        resource1 = ['arn:aws:s3:::' + bucket_name]
        resource2 = ['arn:aws:s3:::' + bucket_name + '/*']
        policy["Version"] = "2012-10-17"
        policy["Statement"] = []
        policy["Statement"].append({"Effect": "Allow", "Action": action1, "Resource": resource1})
        policy["Statement"].append({"Effect": "Allow", "Action": action2, "Resource": resource2})
        with open('policy.json', 'w') as outfile:
            json.dump(policy, outfile)
        return os.getcwd() + '/' + file_name
    except Exception as e:
        print "Error: " + str(e)
        sys.exit(1)

def create_iam_role(bucket_name, role_profile):
    conn = boto3.client('iam')
    role_name = "Allow_actions_s3"
    policy_name = "Policy_Allow_Access_S3"
    document = ''
    with open(generate_json_policy(bucket_name), 'r') as myfile:
        document = myfile.read()
    try:
        role = conn.create_role(RoleName=role_name, AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":["ec2.amazonaws.com"]},"Action":["sts:AssumeRole"]}]}')
        conn.put_role_policy(RoleName=role_name, PolicyName=policy_name, PolicyDocument=document)
        instance_profile = conn.create_instance_profile(InstanceProfileName=role_profile)
        conn.add_role_to_instance_profile(InstanceProfileName=role_profile, RoleName=role_name)
        print "Applying changes..."
        time.sleep(10)
        return True
    except Exception as e:
        print "Error: " + str(e)
        sys.exit(1)
