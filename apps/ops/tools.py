#coding:utf-8
import paramiko
import os
import re


key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "id_rsa")
# from id_rsa import *

class ssh:

    def __init__(self, host):
        self.host = host
        self.user = 'root'
        self.private_key = paramiko.RSAKey.from_private_key_file(key_file)

    def tools_git(self, dir, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, username=self.user, pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('cd {0}; git {1}'.format(dir, command), timeout=30)
        result = re.sub(r'\n', '<br>', stdout.read())
        ssh.close()
        return result

    def tools_deamon(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, username=self.user, pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('supervisorctl restart all', timeout=30)
        result = re.sub(r'\n', '<br>', stdout.read())
        ssh.close()
        return result

    def tools_php_artisan(self, dir, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, username=self.user, pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('/usr/bin/php {0}artisan {1}'.format(dir, command), timeout=30)
        result = re.sub(r'\n', '<br>', stdout.read())
        print stderr.read()
        ssh.close()
        return result