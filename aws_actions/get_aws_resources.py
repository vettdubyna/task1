#!/usr/bin/python

from fabric.api import *
import boto3
import os

def get_ec2_ip(instance_id):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-id', 'Values': [instance_id]}])
    for instance in instances:
        return getattr(instance, 'public_dns_name')
