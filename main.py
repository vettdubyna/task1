#!/usr/bin/python

from fabric.api import *
from aws_actions.create_aws_resources import *
from aws_actions.create_aws_files import *
from aws_actions.get_aws_resources import *
from scripts.prepare import *
from scripts.configure import *
import os
import io
import ConfigParser
import webbrowser
import time

def set_params(path):
    try:
        params = {}
        with open(path) as f:
            sample_conf = f.read()
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(sample_conf))
        for section in config.sections():
            for options in config.options(section):
                params[options] = config.get(section, options)
        return params
    except Exception as e:
        print "Error: " + str(e)

def print_headers(str):
    print " ====================== " + str + " ====================== "

if __name__ == "__main__":
    try:
        ec2_params = {}
        ec2_params = set_params("config/configuration.ini")
        base_name = ec2_params["base_name"]
        print_headers("Creating AWS Files")
        create_aws_config()
        print_headers("Creating S3 bucket")
        bucket_name = raw_input("Please type-in your bucket name: ")
        tags = {}
        tags["Key"] = "Name"
        tags["Value"] = bucket_name
        print "Bucket " + create_s3(bucket_name, tags, ec2_params["region"]) + " has been created!"
        print_headers("Putting file to S3")
        if put_in_s3(bucket_name) == True:
            print "Done!"
        else:
            print "Fail!"
        print_headers("Creating EC2 Role")
        role_profile = base_name + '-profile'
        print create_iam_role(bucket_name, role_profile)
        print_headers("Creating EC2 Instance")
        instance_id = create_ec2_instance(ec2_params, base_name, role_profile)
        print "Instance ID = " + instance_id
        print_headers("Configuring NGINX on instance")
        ip_addr = get_ec2_ip(instance_id)
        preparing_instance(ip_addr, "ec2-user", "keys/" + ec2_params["key_name"] + ".pem")
        print_headers("Configuring web-site")
        configuring_web_site(ip_addr, "ec2-user", "keys/" + ec2_params["key_name"] + ".pem", bucket_name)
        print_headers("Running application")
        webbrowser.open("http://" + ip_addr, new=0, autoraise=True)
    except Exception as e:
        print "Error here: " + str(e)
