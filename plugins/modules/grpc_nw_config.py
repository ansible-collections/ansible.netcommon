#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
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
  state:
    description: action to be performed

requirements:
  - grpcio
  - protobuf
notes:
  - This module requires the gRPC system service be enabled on
    the target host being managed.
  - This module supports the use of connection=connection=ansible.netcommon.grpc
  - This module requires the value of 'ansible_network_os' or 'grpc_type' configuration option
    (refer ansible.netcommon.grpc connection plugin documentation)
    be defined as an inventory variable.
  - Tested against iosxrv 9k version 6.1.2.
"""

EXAMPLES = """
- name: Merge bgp configuration data
  - name: Merge static route config
    ansible.netcommon.grpc_nw_config:
      config:
        Cisco-IOS-XR-ip-static-cfg:router-static:
          default-vrf:
            address-family:
              vrfipv4:
                vrf-unicast:
                  vrf-prefixes:
                    vrf-prefix:
                      - prefix: "1.2.3.6"
                        prefix-length: 32
                        vrf-route:
                          vrf-next-hop-table:
                            vrf-next-hop-next-hop-address:
                              - next-hop-address: "10.0.2.2"

      state: merged

 - name: Merge bgp config
    ansible.netcommon.grpc_nw_config:
      config: {{ lookup('file', 'bgp.json')  }}"
      state: merged

"""

RETURN = """
stdout:
  description: The raw string containing response object
               received from the gRPC server.
  returned: error mesage, when failure happens.
            empty , when the operation is successful
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
from ansible_collections.ansible.netcommon.plugins.module_utils.network.grpc.grpc import (
    merge_config,
    replace_config,
    delete_config,
)
import json
import yaml


def main():
    """entry point for module execution"""
    argument_spec = dict(
        config=dict(),
        state=dict(),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    config = json.dumps(yaml.safe_load(module.params["config"]))
    config = json.loads(config)
    state = module.params["state"]

    result = {"changed": False}
    try:
        if state == "merged":
            response = merge_config(module, config)
        elif state == "replaced":
            response = replace_config(module, config)
        elif state == "deleted":
            response = delete_config(module, config)
    except ConnectionError as exc:
        module.fail_json(
            msg=to_text(exc, errors="surrogate_then_replace"), code=exc.code
        )

    result["stdout"] = response

    module.exit_json(**result)


if __name__ == "__main__":
    main()
