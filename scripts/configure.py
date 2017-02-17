#!/usr/bin/python

import ConfigParser
from fabric import *
import boto3
from fabric.operations import sudo
from fabric.context_managers import settings
from fabric.api import env, run
import os
import sys

def configuring_web_site(ip_addr, user, key, bucket_name):
    try:
        env['connection_attempts'] = 100
        env.key_filename = [key]
        env.host_string = user + '@' + ip_addr
        sudo('aws s3 cp s3://' + bucket_name + '/index.html /usr/share/nginx/html/index.html')
        print "Restarting nginx..."
        sudo('systemctl restart nginx.service')
    except Exception as e:
        print "Error: " + str(e)
        sys.exit(1)
