#!/usr/bin/python

import ConfigParser
from fabric import *
import boto3
from fabric.operations import sudo
from fabric.context_managers import settings
from fabric.api import env, run
import os
import sys

def configure_instance(ip_addr, user, key):
    try:
    #    with (settings(host_string=ip_addr, user=user, key_filename=key)):
            #insalling nginx
        env['connection_attempts'] = 100
        env.key_filename = [key]
        env.host_string = user + '@' + ip_addr
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
        print "Error: " + str(e)
        sys.exit(1)
