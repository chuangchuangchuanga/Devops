#coding:utf-8
import sys, os
import paramiko

# ipadd = sys.argv[1]
# path = sys.argv[2]
# reset = sys.argv[3]

def fun(ipadd, path, reset):
    user = 'git'
    passwd = '123456'

    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ipadd, 22, user, passwd, timeout=5)
    if reset == 'update':
        stdin, stdout, stderr = s.exec_command('cd %s ;sudo git fetch origin master; sudo git merge origin/master' %path, get_pty=True)
    else:
        stdin, stdout, stderr = s.exec_command('cd %s ;sudo git reset --hard %s' %(path,reset), get_pty=True)
    cmd_result = stdout.read(), stderr.read()
    #for line in cmd_result:
    #     print line
    s.close()
    print cmd_result