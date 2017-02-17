#!/usr/bin/python

from fabric.api import *
import os
import shutil

def manual_input():
    try:
        aws_key_id = raw_input("Please enter your AWS KEY ID: ")
        aws_secret_key = raw_input("Please enter your AWS SECRET KEY: ")
        aws_dir = "/home/" + os.getlogin() + "/.aws1"
        local("rm -rf " + aws_dir + " 2>&1", capture=True)
        local("mkdir -p " + aws_dir + " 2>&1", capture=True)
        with open(aws_dir + '/credentials', 'w') as aws_cred:
            aws_cred.write("[default]\n")
            aws_cred.write("aws_access_key_id = %s\n" %aws_key_id)
            aws_cred.write("aws_secret_access_key = %s\n" %aws_secret_key)
        local("chmod 600 " + aws_dir + "/*"+" 2>&1", capture=True)
        local("chmod 750 " + aws_dir +" 2>&1", capture=True)
    except Exception as e:
        print "Error" + str(e)

def overwrite(conf_path="../config/creds"):
    try:
        aws_dir = "/home/" + os.getlogin() + "/.aws1"
        local("rm -rf " + aws_dir + " 2>&1", capture=True)
        local("mkdir -p " + aws_dir + " 2>&1", capture=True)
        local("cp " + conf_path + " " + aws_dir + "/credentials")
        local("chmod 600 " + aws_dir + "/*"+" 2>&1", capture=True)
        local("chmod 750 " + aws_dir +" 2>&1", capture=True)
    except Exception as e:
        print "Error" + str(e)

def check_dir_excist():
    try:
        if (os.path.exists("/home/" + os.getlogin() + "/.aws1")) == False:
            print "File doesn't exists! Please ru-run script"
            raise Exception
        else:
            print "Great!"
    except Exception as e:
        print "Error" + str(e)

#Create AWS config files in .aws
def create_aws_config(path_to_creds="config/creds"):
    try:
        print "1. Input manually"
        print "2. Use conf.ini"
        print "3. Have already changed"
        choise = input("Choose the way you want to change aws configuration: ")
        if choise == 1:
            manual_input()
        elif choise == 2:
            overwrite(path_to_creds)
        elif choise == 3:
            check_dir_excist()
        else:
            print "Please type correct value"
            raise Exception

    except Exception as e:
        print "Error " + str(e)
