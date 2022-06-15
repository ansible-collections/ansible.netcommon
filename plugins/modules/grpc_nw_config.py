#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: grpc_nw_config
version_added: ""
author:
    - "Gomathi Selvi S (@GomathiselviS)"
short_description: Fetch configuration/state data from gRPC enabled target hosts.
description:
    - gRPC is a high performance, open-source universal RPC framework.
    - This module allows the user to append configs to an existing configuration in a gRPC
      enabled devices.
options:
  config:
    description:
      - This option specifies the string which acts as a filter to restrict the portions of
        the data to be retrieved from the target host device. If this option is not specified the entire
        configuration or state data is returned in response provided it is supported by target host.
  path:
    description: path of the file that has the config in json format.
  state:
    description: action to be performed
   
requirements:
  - grpcio
  - protobuf
notes:
  - This module requires the gRPC system service be enabled on
    the target host being managed.
  - This module supports the use of connection=grpc.
  - This module requires the value of 'ansible_network_os' be defined as an inventory variable.
  - Tested against iosxrv 9k version 6.1.2.
"""

EXAMPLES = """
- name: Merge bgp configuration data
  grpc_nw_config:
    path:  'bgp_merge.json'
    state: merged
"""

RETURN = """
stdout:
  description: The raw string containing response object
               received from the gRPC server.
  returned: always apart from low-level errors (such as action plugin)
  type: Response object
  sample: '...'
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low-level errors (such as action plugin)
  type: list
  sample: ['...', '...']
output:
"""
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils.network.common.utils import to_list
from ansible_collections.ansible.netcommon.plugins.module_utils.network.grpc.grpc import get_capabilities, merge_config, replace_config
import json
import yaml

def main():
    """entry point for module execution
    """
    argument_spec = dict(
        config=dict(),
        path=dict(),
        state=dict(),
    )

    mutually_exclusive = [['config', 'path']]

    module = AnsibleModule(argument_spec=argument_spec,
                           mutually_exclusive=mutually_exclusive,
                           supports_check_mode=True)

    capabilities = get_capabilities(module)

    operations = capabilities['server_capabilities']

    if module.params['config']:
        config = json.dumps(yaml.safe_load(module.params['config']))
        config = json.loads(config)
    if module.params['path']:
        config = open(module.params['path']).read()
        config = json.dumps(yaml.safe_load(config))
        config = json.loads(config)
    state = module.params['state']

    result = {'changed': False}
    try:
        if state == "merged":
            response = merge_config(module, config)
        elif state == "replaced":
            response = replace_config(module, config)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'), code=exc.code)

    
    result['stdout'] = response

    module.exit_json(**result)


if __name__ == '__main__':
    main()
