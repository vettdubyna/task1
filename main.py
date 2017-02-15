#!/usr/bin/python

from fabric.api import *
from aws_actions.create_aws_resources import *
from aws_actions.create_aws_files import *
from scripts.prepare import *
import os
import sys

if __name__ == "__main__":
    try:
        ec2_params = {}
        ec2_params = set_params()
        #print ec2_params
        print "Creating AWS Files: "
        create_aws_config()
        print "Creating EC2 Instance: "
        #instance_id = create_ec2_instance(ec2_params, "MyTag")
        #print "Instance ID = " + instance_id
        print "Creating S3 bucket: "
        bucket_name = raw_input("Please type-in your bucket name: ")
        tags = {}
        tags["Key"] = "Name"
        tags["Value"] = "task1-bucket-name-vd"
        print "Bucket " + create_s3(bucket_name, tags, ec2_params["region"]) + "has been created!"
    except Exception as e:
        raise
