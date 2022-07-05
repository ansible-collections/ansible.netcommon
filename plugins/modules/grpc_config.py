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
  backup:
    description:
    - This argument will cause the module to create a full backup of the current C(running-config)
      from the remote device before any changes are made. If the C(backup_options)
      value is not given, the backup file is written to the C(backup) folder in the
      playbook root directory or role root directory, if playbook is part of an ansible
      role. If the directory does not exist, it is created.
    type: bool
    default: no
  backup_options:
    description:
    - This is a dict object containing configurable options related to backup file
      path. The value of this option is read only when C(backup) is set to I(yes),
      if C(backup) is set to I(no) this option will be silently ignored.
    suboptions:
      filename:
        description:
        - The filename to be used to store the backup configuration. If the filename
          is not given it will be generated based on the hostname, current time and
          date in format defined by <hostname>_config.<current-date>@<current-time>
        type: str
      dir_path:
        description:
        - This option provides the path ending with directory name in which the backup
          configuration file will be stored. If the directory does not exist it will
          be first created and the filename is either the value of C(filename) or
          default filename as described in C(filename) options description. If the
          path value is not given in that case a I(backup) directory will be created
          in the current working directory and backup configuration will be copied
          in C(filename) within I(backup) directory.
        type: path
    type: dict

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

 - name: Find diff
   diff: True
   ansible.netcommon.grpc_nw_config:
     config: "{{ lookup('file', 'bgp_start.yml')  }}"
     state: merged

# Module Execution
# --- before
# +++ after
# @@ -14,7 +14,7 @@
#          ],
#          "default-vrf": {
#           "global": {
# -          "router-id": "12.1.1.10",
# +          "router-id": "11.1.1.10",
#            "global-afs": {
#             "global-af": [
#              {
#
# changed: [10.0.150.231] => changed=true
#   diff:
#     after: |-
#       {
#        "Cisco-IOS-XR-ipv4-bgp-cfg:bgp": {
#         "instance": [
#          {
#           "instance-name": "default",
#           "instance-as": [
#            {
#             "as": 0,
#             "four-byte-as": [
#              {
#               "as": 65400,
#               "bgp-running": [
#                null
#               ],
#               "default-vrf": {
#                "global": {
#                 "router-id": "11.1.1.10",
#                 "global-afs": {
#                  "global-af": [
#                   {
#                    "af-name": "ipv4-unicast",
#                    "enable": [
#                     null
#                    ],
#                    "sourced-networks": {
#                     "sourced-network": [
#                      {
#                       "network-addr": "11.1.1.0",
#                       "network-prefix": 24
#                      }
#                     ]
#                    }
#                   }
#                  ]
#                 }
#                },
#                "bgp-entity": {
#                 "neighbors": {
#                  "neighbor": [
#                   {
#                    "neighbor-address": "11.1.1.20",
#                    "remote-as": {
#                     "as-xx": 0,
#                     "as-yy": 65450
#                    },
#                    "neighbor-afs": {
#                     "neighbor-af": [
#                      {
#                       "af-name": "ipv4-unicast",
#                       "activate": [
#                        null
#                       ],
#                       "next-hop-self": true
#                      }
#                     ]
#                    }
#                   }
#                  ]
#                 }
#                }
#               }
#              }
#             ]
#            }
#           ]
#          }
#         ]
#        }
#       }
#     before: |-
#       {
#        "Cisco-IOS-XR-ipv4-bgp-cfg:bgp": {
#         "instance": [
#          {
#           "instance-name": "default",
#           "instance-as": [
#            {
#             "as": 0,
#             "four-byte-as": [
#              {
#               "as": 65400,
#               "bgp-running": [
#                null
#               ],
#               "default-vrf": {
#                "global": {
#                 "router-id": "12.1.1.10",
#                 "global-afs": {
#                  "global-af": [
#                   {
#                    "af-name": "ipv4-unicast",
#                    "enable": [
#                     null
#                    ],
#                    "sourced-networks": {
#                     "sourced-network": [
#                      {
#                       "network-addr": "11.1.1.0",
#                       "network-prefix": 24
#                      }
#                     ]
#                    }
#                   }
#                  ]
#                 }
#                },
#                "bgp-entity": {
#                 "neighbors": {
#                  "neighbor": [
#                   {
#                    "neighbor-address": "11.1.1.20",
#                    "remote-as": {
#                     "as-xx": 0,
#                     "as-yy": 65450
#                    },
#                    "neighbor-afs": {
#                     "neighbor-af": [
#                      {
#                       "af-name": "ipv4-unicast",
#                       "activate": [
#                        null
#                       ],
#                       "next-hop-self": true
#                      }
#                     ]
#                    }
#                   }
#                  ]
#                 }
#                }
#               }
#              }
#             ]
#            }
#           ]
#          }
#         ]
#        }
#       }
#   invocation:
#     module_args:
#       backup: false
#       backup_options: null
#       config: |-
#         ---
#         Cisco-IOS-XR-ipv4-bgp-cfg:bgp:
#           instance:
#           - instance-name: default
#             instance-as:
#             - as: 0
#               four-byte-as:
#               - as: 65400
#                 bgp-running:
#                 -
#                 default-vrf:
#                   global:
#                     router-id: 11.1.1.10
#                     global-afs:
#                       global-af:
#                       - af-name: ipv4-unicast
#                         enable:
#                         -
#                         sourced-networks:
#                           sourced-network:
#                           - network-addr: 11.1.1.0
#                             network-prefix: 24
#                   bgp-entity:
#                     neighbors:
#                       neighbor:
#                       - neighbor-address: 11.1.1.20
#                         remote-as:
#                           as-xx: 0
#                           as-yy: 65450
#                         neighbor-afs:
#                           neighbor-af:
#                           - af-name: ipv4-unicast
#                             activate:
#                             -
#                             next-hop-self: true
#       state: merged
#
 - name: Backup running config
    ansible.netcommon.grpc_nw_config:
      backup: yes
# Module Execution:
# backup_path: /home/gosriniv/github/backup/10.0.150.231_config.2022-07-04@17:35:56
#  date: '2022-07-04'
#  filename: 10.0.150.231_config.2022-07-04@17:35:56
#  invocation:
#    module_args:
#      backup: true
#      backup_options: null
#      config: null
#      state: null
#  shortname: /home/gosriniv/github/backup/10.0.150.231_config
#  stdout: ''
#  stdout_lines: <omitted>
#  time: '17:35:56'

 - name: Find diff
   diff: True
   ansible.netcommon.grpc_nw_config:
     config: "{{ lookup('file', 'bgp_start.yml')  }}"
     state: merged
# Module Execution
# changed: [10.0.150.231] => changed=true
#   diff:
#     Cisco-IOS-XR-ipv4-bgp-cfg:bgp:
#       instance:
#       - instance-as:
#         - as: 0
#           four-byte-as:
#           - as: 65400
#             bgp-running:
#             - null
#             default-vrf:
#               bgp-entity:
#                 neighbors:
#                   neighbor:
#                   - neighbor-address: 11.1.1.20
#                     neighbor-afs:
#                       neighbor-af:
#                       - activate:
#                         - null
#                         af-name: ipv4-unicast
#                         next-hop-self: true
#                     remote-as:
#                       as-xx: 0
#                       as-yy: 65450
#               global:
#                 global-afs:
#                   global-af:
#                   - af-name: ipv4-unicast
#                     enable:
#                     - null
#                     sourced-networks:
#                       sourced-network:
#                       - network-addr: 11.1.1.0
#                         network-prefix: 24
#                 router-id: 12.1.1.10
#         instance-name: default
#   invocation:
#     module_args:
#       backup: false
#       backup_options: null
#       config: |-
#         ---
#         Cisco-IOS-XR-ipv4-bgp-cfg:bgp:
#           instance:
#           - instance-name: default
#             instance-as:
#             - as: 0
#               four-byte-as:
#               - as: 65400
#                 bgp-running:
#                 -
#                 default-vrf:
#                   global:
#                     router-id: 12.1.1.10
#                     global-afs:
#                       global-af:
#                       - af-name: ipv4-unicast
#                         enable:
#                         -
#                         sourced-networks:
#                           sourced-network:
#                           - network-addr: 11.1.1.0
#                             network-prefix: 24
#                   bgp-entity:
#                     neighbors:
#                       neighbor:
#                       - neighbor-address: 11.1.1.20
#                         remote-as:
#                           as-xx: 0
#                           as-yy: 65450
#                         neighbor-afs:
#                           neighbor-af:
#                           - af-name: ipv4-unicast
#                             activate:
#                             -
#                             next-hop-self: true
#       state: merged
#
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
backup_path:
  description: The full path to the backup file
  returned: when backup is yes
  type: str
  sample: /playbooks/ansible/backup/config.2022-07-16@22:28:34
"""
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import ConnectionError
from ansible_collections.ansible.netcommon.plugins.module_utils.network.grpc.grpc import (
    merge_config,
    replace_config,
    delete_config,
    run_cli,
    sanitize_content,
    validate_config,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_diff,
)
import json
import yaml


def main():
    """entry point for module execution"""
    backup_spec = dict(filename=dict(), dir_path=dict(type="path"))
    argument_spec = dict(
        config=dict(),
        state=dict(),
        backup=dict(type="bool", default=False),
        backup_options=dict(type="dict", options=backup_spec),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    config = {}
    if module.params["config"]:
        config = json.dumps(yaml.safe_load(module.params["config"]))
        config = json.loads(config)
    state = module.params["state"]

    result = {
        "changed": False,
    }
    before = None
    after = None
    before_diff = None
    after_diff = None
    output = ""
    try:
        if module.params["backup"] or state in [
            "merged",
            "replaced",
            "deleted",
        ]:
            if not module.check_mode:
                response, err = run_cli(module, "show running-config", "text")
                before = to_text(
                    response, errors="surrogate_then_replace"
                ).strip()

        if module._diff or module.check_mode:
            before_diff = validate_config(module, config)
        if module.check_mode:
            diff = dict_diff(before_diff, config)
            if diff:
                result["changed"] = True
                result["diff"] = diff
        else:
            if module.params["backup"]:
                result["__backup__"] = before.strip()
            if state == "merged":
                output = merge_config(module, config)
            elif state == "replaced":
                output = replace_config(module, config)
            elif state == "deleted":
                output = delete_config(module, config)
            if state:
                response, err = run_cli(module, "show running-config", "text")
                after = to_text(
                    response, errors="surrogate_then_replace"
                ).strip()
            if before:
                before = sanitize_content(before)
            if after:
                after = sanitize_content(after)
            if before != after:
                result["changed"] = True
                if module._diff:
                    after_diff = validate_config(module, config)
                    result["diff"] = {
                        "before": before_diff,
                        "after": after_diff,
                    }
    except ConnectionError as exc:
        module.fail_json(
            msg=to_text(exc, errors="surrogate_then_replace"), code=exc.code
        )

    result["stdout"] = output

    module.exit_json(**result)


if __name__ == "__main__":
    main()
