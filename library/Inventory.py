#coding: utf-8

import fnmatch
import os
from ansible.compat.six import string_types, iteritems
from ansible import constants as C
from ansible.errors import AnsibleError

from ansible.inventory.dir import InventoryDirectory, get_file_parser
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.module_utils._text import to_bytes, to_text
from ansible.parsing.utils.addresses import parse_address
from ansible.plugins import vars_loader
from ansible.utils.vars import combine_vars
from ansible.utils.path import unfrackpath

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


HOSTS_PATTERNS_CACHE ={}
from ansible.inventory import Inventory

class YunweiInventory(Inventory):
    def __init__(self, loader, variable_manager, group_name, ext_vars=None, host_list=C.DEFAULT_HOST_LIST):
        self.host_list = host_list
        self.group_name = group_name
        self.ext_vars = ext_vars

        self._vars_per_host = {}
        self._vars_per_group = {}
        self._hosts_cache = {}
        self._pattern_dict_cache = {}
        self._group_dict_cache = {}
        self._vars_plugins = []

        self._basedir = self.basedir()

        self._group_vars_files = self._find_group_vars_files(self._basedir)
        self._host_vars_files = self._find_host_vars_files(self._basedir)

        self._playbook_basedir = None
        self.groups = {}

        self._restriction = None
        self._subset = None

        self.clear_pattern_cache()
        self.clear_group_dict_cache()

        self.parse_inventory(host_list)

    def parse_inventory(self, host_list):

        if isinstance(host_list, string_types):
            if "," in host_list:
                host_list = host_list.split(",")
                host_list = [ h for h in host_list if h and h.strip() ]

        self.parser = None

        ungrouped = Group('ungrouped')
        all = Group("all")
        all.add_child_group(ungrouped)

        local_group = Group("local")

        zdy_group_name = Group(self.group_name)
        self.groups = {self.group_name: zdy_group_name, "all":all, "ungrouped":ungrouped, "local":local_group}

        if host_list is None:
            pass
        elif isinstance(host_list, list):

            (lhost, lport) = parse_address('127.0.0.1', allow_ranges=False)
            new_host = Host(lhost, lport)
            local_group.add_host(new_host)

            for h in host_list:
                try:
                    (host, port) = parse_address(h, allow_ranges=False)
                except AnsibleError as e:
                    display.vvv("Unable to parse address from hostname, leaving unchanged: %s" % to_text(e))
                    host = h
                    port = None
                new_host = Host(host, port)
                if h in C.LOCALHOST:
                    if self.localhost is not None:
                        display.warning("A duplicate localhost-like entry was found (%s). First found localhost was %s" % (h, self.localhost.name))
                    display.vvvv("set default localhost to %s" % h)
                    self.localhost = new_host
                zdy_group_name.add_host(new_host)

                if self.ext_vars and isinstance(self.ext_vars, dict):
                    for k,v in self.ext_vars.items():
                        zdy_group_name.set_variable(k,v)
                        local_group.set_variable(k,v)

        elif self._loader.path_exists(host_list):
            if self.is_directory(host_list):
                host_list = os.path.join(self.host_list, "")
                self.parser = InventoryDirectory(loader=self._loader, groups=self.groups, filename=host_list)
            else:
                self.parser = get_file_parser(host_list, self.groups, self._loader)
                vars_loader.add_directory(self._basedir, with_subdir=True)

            if not self.parser:
                raise AnsibleError("Unable to parse %s as an inventory source" % host_list)

        else:
            display.warning("Host file not found: %s" % to_text(host_list))

        self._vars_plugins = [x for x in vars_loader.all(self)]




