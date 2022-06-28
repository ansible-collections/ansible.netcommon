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
from ansible.module_utils.connection import Connection, ConnectionError
from ansible_collections.ansible.netcommon.plugins.module_utils.network.grpc.grpc import (
    merge_config,
    replace_config,
    delete_config,
    get_capabilities,
    get,
    run_cli,
    sanitize_content,
)
import json
import yaml


def main():
    """entry point for module execution"""
    _config_module = True
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

    if module.params["config"]:
        config = json.dumps(yaml.safe_load(module.params["config"]))
        config = json.loads(config)
    state = module.params["state"]

    capabilities = get_capabilities(module)
    #operations = capabilities["device_operations"]

    result = {
        "changed": False,
    }
    before = None
    after = None
    output = ""
    try:
        if module.params["backup"] or state in ["merged", "replaced", "deleted"]:
            response, err = run_cli(module, "show running-config", "text")
            before = to_text(
                response, errors="surrogate_then_replace"
            ).strip()
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
                result["diff"] = {
                    "before": before,
                    "after": after,
                }
    except ConnectionError as exc:
        module.fail_json(
            msg=to_text(exc, errors="surrogate_then_replace"), code=exc.code
        )

    result["stdout"] = output

    module.exit_json(**result)


if __name__ == "__main__":
    main()
