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


    def git_pull(self, dir):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, username=self.user, pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('cd {0}; git pull'.format(dir), timeout=30)
        if stdout.read:
            result = re.sub(r'\n', '<br>', stdout.read())
            ssh.close()
            return result
        else:
            result = re.sub(r'\n', '<br>', stderr.read())
            ssh.close()
            return result


    def git_reset_hard(self, dir, hard_code):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, username=self.user, pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('cd {0}; git reset --hard {1}'.format(dir, hard_code), timeout=30)
        if stdout.read:
            result = re.sub(r'\n', '<br>', stdout.read())
            ssh.close()
            return result
        else:
            result = re.sub(r'\n', '<br>', stderr.read())
            ssh.close()
            return result



    def deamon_process_restart(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, username=self.user, pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('supervisorctl restart all', timeout=30)
        if stdout.read:
            result = re.sub(r'\n', '<br>', stdout.read())
            ssh.close()
            return result
        else:
            result = re.sub(r'\n', '<br>', stderr.read())
            ssh.close()
            return result


    def php_artisan_option(self, dir, artisan_option_value):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, username=self.user, pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('/usr/bin/php {0}artisan {1}'.format(dir, artisan_option_value), timeout=30)
        if stdout.read:
            result = re.sub(r'\n', '<br>', stdout.read())
            ssh.close()
            return result
        else:
            result = re.sub(r'\n', '<br>', stderr.read())
            ssh.close()
            return result


    def npm_dev_option(self, dir, npm_dev_option_value):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, username=self.user, pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('cd {0}; /usr/local/node/bin/npm run {1}'.format(dir, npm_dev_option_value), timeout=30)
        if stdout.read:
            result = re.sub(r'\n', '<br>', stdout.read())
            ssh.close()
            return result
        else:
            print stderr.read
            result = re.sub(r'\n', '<br>', stderr.read())
            ssh.close()
            return result

    def pl_queue_git_pull(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='47.91.165.145', username='root', pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('cd /home/pl/wwwroot/; git pull', timeout=30)
        if stdout.read:
            result = re.sub(r'\n', '<br>', stdout.read())
            ssh.close()
            result
            return
        else:
            result = re.sub(r'\n', '<br>', stderr.read())
            ssh.close()
            result
            return

    def pl_queue_deamon_process_restart(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='47.91.165.145', username='root', pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('supervisorctl restart all', timeout=30)
        result = re.sub(r'\n', '<br>', stdout.read())
        ssh.close()
        result

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='47.75.17.124', username='root', pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('supervisorctl restart all', timeout=30)
        result = re.sub(r'\n', '<br>', stdout.read())
        ssh.close()
        result

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='47.75.28.193', username='root', pkey=self.private_key)
        stdin, stdout, stderr = ssh.exec_command('supervisorctl restart all', timeout=30)
        result = re.sub(r'\n', '<br>', stdout.read())
        ssh.close()
        result





