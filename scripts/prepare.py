#!/usr/bin/python

import ConfigParser
from fabric import *
import boto3
from fabric.operations import sudo
from fabric.context_managers import settings
import json
import os

def configure_instance(ip_addr, user, key):
    try:
        with (settings(host_string=ip_addr, user=user, key_filename=key)):
            #insalling nginx
            sudo('curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"')
            sudo('python get-pip.py')
            sudo('pip install --upgrade pip')
            sudo('yum -y install kernel-headers python-devel.x86_64 vim less git wget curl')
            sudo('rpm -Uvh http://nginx.org/packages/rhel/7/noarch/RPMS/nginx-release-rhel-7-0.el7.ngx.noarch.rpm')
            sudo('yum -y install nginx')
            sudo('pip install awscli')
            sudo('systemctl start nginx.service')
            sudo('chkconfig nginx on')
        return True
    except Exception as e:
        print "Error " + str(e)

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
        raise

def create_iam_role(bucket_name, profile):
    conn = boto3.client('iam')
    role_name = "Allow_actions_s3"
    role_profile = profile
    policy_name = "Policy_Allow_Access_S3"
    document = ''
    with open(generate_json_policy(bucket_name), 'r') as myfile:
        document = myfile.read()
    try:
        instance_profile = conn.create_instance_profile(InstanceProfileName=role_profile)
        role = conn.create_role(RoleName=role_name)
        conn.add_role_to_instance_profile(InstanceProfileName=role_profile, RoleName=role_name)
        conn.put_role_policy(RoleName=role_name, PolicyName=policy_name, PolicyDocument=document)
        return True
    except Exception as e:
        print "Error: " + str(e)
