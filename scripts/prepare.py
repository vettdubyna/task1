#!/usr/bin/python

import ConfigParser
from fabric import *
import boto3
from fabric.operations import sudo
from fabric.context_managers import settings

def configure_instance(ip_addr, user, key):
    try:
        with (settings(host_string=ip_addr, user=user, key_filename=key)):
            #insalling nginx
            sudo('yum -y install kernel-headers python-pip python-devel.x86_64 vim less git wget ntsysv openssl-devel gcc libffi-devel')
            sudo('rpm -Uvh http://nginx.org/packages/rhel/7/noarch/RPMS/nginx-release-rhel-7-0.el7.ngx.noarch.rpm')
            sudo('sudo yum install nginx')
            sudo('yum -y update')
            sudo('nginx -v')
            sudo('systemctl start nginx.service')
            sudo('chkconfig nginx on')
            
        return True
    except Exception as e:
        print "Error " + str(e)
