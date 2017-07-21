#coding:utf-8
import sys, os
import paramiko




from .user_and_passwd import *


def fun(ipadd, path, reset):
    user = users
    passwd = password

    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ipadd, 22, user, passwd, timeout=5)
    if reset == 'update':
        stdin, stdout, stderr = s.exec_command('cd %s ;sudo git fetch origin master:temp;sudo git merge temp' %path, get_pty=True)
    else:
        stdin, stdout, stderr = s.exec_command('cd %s ;sudo git reset --hard %s' %(path,reset), get_pty=True)
    cmd_result = stdout.read(), stderr.read()
    for line in cmd_result:
         print line
    s.close()