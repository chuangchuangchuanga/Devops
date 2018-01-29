#coding: utf-8

from ansible.module_utils.basic import *

import commands


module = AnsibleModule(
    argument_spec=dict(
        command=dict(required=True),
        path=dict(required=True),
        option=dict
    ),
)


name = module.params['command']
path = module.params['path']
option = module.params['option']


status, output = commands.getstatusoutput('''{0} {1} {2}'''.format(name, path, option))
if status == 0:
    result = dict(stdout=output, changed=False, rc=0)
    module.exit_json(**result)
else:
    result = dict(msg="execute failed", rc=status)
    module.exit_json(**result)