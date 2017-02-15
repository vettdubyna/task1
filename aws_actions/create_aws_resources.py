#!/usr/bin/python

from fabric.api import *
import boto3
import os

def create_ec2_instance(params, instance_tag):
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
                                        SubnetId = subnet_id
                                        )
        print "Waiting for instance become running"
        for instance in instances:
            instance.wait_until_running()
            instance.create_tags(Tags=[{'Key': 'Name', 'Value': 'Instance_task1'}])
            return instance.id
    except Exception as e:
        print "Error " + str(e)
    return ''

def create_s3(bucket_name, tag, region):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        tagging = bucket.Tagging()
        tagging.put(Tagging={'TagSet': [tag]})
        tagging.reload()
        return bucket.name
    except Exception as e:
        print "Error" + str(e)
