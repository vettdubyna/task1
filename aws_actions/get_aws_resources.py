#!/usr/bin/python

from fabric.api import *
import boto3
import os

def get_ec2_ip(instance_id):
    try:
        ec2 = boto3.resource('ec2')
        instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-id', 'Values': [instance_id]}])
        for instance in instances:
            return getattr(instance, 'public_dns_name')
    except Exception as e:
        print "Error: " + str(e)

def put_in_s3(bucket_name):
    try:
        s3 = boto3.client('s3')
        local_file = "source/index.html"
        destination_file = "index.html"
        with open(local_file, 'rb') as data:
            s3.upload_fileobj(data, bucket_name, destination_file)
        return True
    except Exception as e:
        print "Error: " + str(e)
