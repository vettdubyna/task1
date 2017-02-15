#!/usr/bin/python

from fabric.api import *
#from aws_actions import *
import os
import sys
import ConfigParser
import io

def get_params():
    try:
        params = {}
        with open("config/configuration.ini", "r") as f:
            sample_conf = f.read()
        print sample_conf
        #
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(sample_conf))
        for section in config.sections():
            for options in config.options(section):
                params[options] = config.get(section, options)
        return params
    except Exception as e:
        print "oops"
        return ''

if __name__ == "__main__":
    ec2_params = {}
    ec2_params = get_params()
    print ec2_params
