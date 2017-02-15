#!/usr/bin/python

from fabric.api import *
from aws_actions.create_aws_resources import *
from aws_actions.create_aws_files import *
from aws_actions.get_aws_resources import *
from scripts.prepare import *
import os
import io
import ConfigParser

def set_params(path):
    try:
        params = {}
        with open(path) as f:
            sample_conf = f.read()
        print sample_conf
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(sample_conf))
        for section in config.sections():
            for options in config.options(section):
                params[options] = config.get(section, options)
        return params
    except Exception as e:
        print "Error: " + str(e)

if __name__ == "__main__":
    try:
        ec2_params = {}
        ec2_params = set_params("config/configuration.ini")
        print ec2_params
        print "Creating AWS Files: "
        create_aws_config()
        print "Creating EC2 Instance: "
        instance_id = create_ec2_instance(ec2_params, "MyTag")
        print "Instance ID = " + instance_id
        print "Creating S3 bucket: "
        bucket_name = raw_input("Please type-in your bucket name: ")
        tags = {}
        tags["Key"] = "Name"
        tags["Value"] = "task1-bucket-name-vd"
        print "Bucket " + create_s3(bucket_name, tags, ec2_params["region"]) + "has been created!"
        print "Configuring NGINX on instance: "
        ip_addr = get_ec2_ip(instance_id)
        configure_instance(ip_addr, "ec2-user", "keys/" + ec2_params["key_name"] + ".pem")
    except Exception as e:
        print "Error here: " + str(e)
