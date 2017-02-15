#!/usr/bin/python

import ConfigParser
import io
from fabric import *

def set_params():
    try:
        params = {}
        with open("config/configuration.ini", "r") as f:
            sample_conf = f.read()
        config = ConfigParser.RawConfigParser(allow_no_value=False)
        config.readfp(io.BytesIO(sample_conf))
        for section in config.sections():
            for options in config.options(section):
                params[options] = config.get(section, options)
        return params
    except Exception as e:
        print sys.exit(0)

def configure_instance(ip_addr, user, key):
    try:
        with (settings(host_string=ip_addr, user=user, key_filename=key)):
            sudo('yum -y install kernel-headers python-pip python-devel.x86_64 vim less git wget ntsysv openssl-devel gcc libffi-devel')
            sudo('yum -y install nginx')
            sudo('systemctl restart nginx.service')
            sudo('chkconfig nginx on')
            
    except Exception as e:
        raise
