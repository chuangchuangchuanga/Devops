#coding: utf-8

import json
from ansible import constants as C
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from collback import YunweiCallback
from ansible.utils.ssh_functions import check_for_controlpersist


from Inventory import YunweiInventory as Inventory
try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

class YunweiPlaybookExecutor(PlaybookExecutor):
    def __init__(self, playbooks, inventory, variable_manager, loader, options, passwords, stdout_callback):
        self._playbooks = playbooks
        self._inventory = inventory
        self._variable_manager = variable_manager
        self._loader = loader
        self._options = options
        self.passwords = passwords
        self._unreachable_hosts = dict()

        if options.listhosts or options.listtasks or options.listtags or options.syntax:
            self._tqm = None
        else:
            self._tqm = TaskQueueManager(inventory=inventory,
                                         variable_manager=variable_manager,
                                         loader=loader, options=options,
                                         passwords=self.passwords,
                                         stdout_callback=stdout_callback)
            check_for_controlpersist(C.ANSIBLE_SSH_EXECUTABLE)

class PlayBookJob(object):
    def __init__(self, playbooks,
                 host_list,
                 ssh_user='root',
                 passwords='123456',
                 project_name='all',
                 ack_pass=False,
                 forks=5,
                 ext_vars=None):
        self.playbooks = playbooks
        self.host_list = host_list
        self.ssh_user = ssh_user
        self.passwords = dict(vault_pass=passwords)
        self.project_name = project_name
        self.ack_pass = ack_pass
        self.forks = forks
        self.connection = 'smart'
        self.ext_vars = ext_vars

        self.loader = DataLoader()

        self.variable_manager = VariableManager()

        self.inventory = Inventory(loader = self.loader,
                                   variable_manager = self.variable_manager,
                                   group_name = self.project_name,
                                   ext_vars = self.ext_vars,
                                   host_list = self.host_list)

        self.variable_manager.set_inventory(self.inventory)

        self.Options = namedtuple('Options',
                                  ['connection',
                                   'remote_user',
                                   'ask_sudo_pass',
                                   'verbosity',
                                   'ack_pass',
                                   'module_path',
                                   'forks',
                                   'become',
                                   'become_method',
                                   'become_user',
                                   'check',
                                   'listhosts',
                                   'listtasks',
                                   'listtags',
                                   'syntax',
                                   'sudo_user',
                                   'sudo'])

        self.options = self.Options(connection = self.connection,
                                    remote_user = self.ssh_user,
                                    ack_pass = self.ack_pass,
                                    sudo_user = self.ssh_user,
                                    forks = self.forks,
                                    sudo = 'yes',
                                    ask_sudo_pass = False,
                                    verbosity = 5,
                                    module_path = None,
                                    become = True,
                                    become_method = 'sudo',
                                    become_user = 'root',
                                    check = None,
                                    listhosts = None,
                                    listtasks = None,
                                    listtags = None,
                                    syntax = None
                                    )

        self.callback = YunweiCallback()
        self.run()

    def run(self):
        pb = None
        pb = YunweiPlaybookExecutor(
            playbooks = self.playbooks,
            inventory = self.inventory,
            variable_manager= self.variable_manager,
            loader= self.loader,
            options= self.options,
            passwords= self.passwords,
            stdout_callback= self.callback
        )
        result = pb.run()

if __name__ == "__main__":
    PlayBookJob(playbooks=['/Users/wangchuang/Devops/library/my.yml'],
                host_list=['192.168.1.14'],
                ssh_user= 'root',
                project_name='test',
                forks=20,
                ext_vars=None)