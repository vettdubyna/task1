#!/usr/bin/python

from fabric.api import *
import os

def create_ec2_instance(params, instance_tag):
    try:
        ec2 = boto3.resource('ec2')
        security_group_id = params["security_group_id"]
        image_id = params["image_id"]
        instance_type = params["instance_type"]
        key_name = params["key_name"]
        instance = ec2.create_instances(ImageId = image_id, MinCount=1, MaxCount=1,
                                        KeyName = key_name,
                                        SecurityGroupIds = security_group_id,
                                        InstanceType = instance_type)
        print "Waiting for instance become running"
        instance.wait_until_running()
        instance.create_tags(Tags=[{'Key': 'Name', 'Value': 'Instance_task1'}, instance_tag)
        return instance.id
    except Exception as e:
        print "Error" + str(e)
    return ''

def create_s3(bucket_name, tag):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.create_bucket(Bucket=bucket_name)
        tagging = bucket.Tagging()
        tagging.put(Tagging={'TagSet': [tag]})
        tagging.reload()
        return bucket.name
    except Exception as e:
        print "Error" + str(e)
