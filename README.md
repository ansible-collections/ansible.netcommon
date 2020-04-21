

# Ansible Network Collection for Common Code (netcommon)
[![CI](https://zuul-ci.org/gated.svg)](https://dashboard.zuul.ansible.com/t/ansible/builds?project=ansible-collections%2Fansible.netcommon) [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/ansible.netcommon)](https://codecov.io/gh/ansible-collections/ansible.netcommon)

The Ansible ``ansible.netcommon`` collection includes common content to help automate the management of network, security, and cloud devices.
This includes  connection plugins, such as ``network_cli``, ``httpapi``, and ``netconf``.

## Included content

This collection includes:
- Common network modules, such as ``net_*``, ``cli_*``, ``netconf_*``, and ``restconf_*`` modules.
- Common connection plugins, such ``network_cli``, ``httpapi``, and ``network_cli``.
- IP address, network manipulation, and network output filters.

Click the ``Content`` button to see the full list of content included in this collection.

### Included filters

This collection includes the following IP and network filters:
- cidr_merge
- ipaddr
- ipmath
- ipwrap
- ip4_hex
- ipv4
- ipv6
- ipsubnet
- next_nth_usable
- network_in_network
- network_in_usable
- reduce_on_network
- nthhost
- previous_nth_usable
- slaac


MAC and Hardware address filters:
- hwaddr
- macaddr

See the [ipaddr filter](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters_ipaddr.html) documentation for details on these filters.

This collection also includes the following output filters:

- parse_cli
- parse_cli_textfsm
- parse_xml
- type5_pw
- hash_salt
- comp_type5
- vlan_parser

See the [network filters](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#network-cli-filters) documentation for more details on these filters.


## Installing this collection

You can install the ``ansible.netcommon`` collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install ansible.netcommon

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: ansible.netcommon
    version: 0.0.3
```
## Using this collection

The most common use case for this collection is to include it as a dependency in a network device-specific collection. Use the Fully Qualified Collection Name (FQCN) when referring to content in this collection (for example, `ansible.netcommon.network_cli`).

See the [Vyos collection](https://github.com/ansible-collections/vyos) for an example of this.


### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [ansible.netcommon collection repository](https://github.com/ansible-collections/ansible.netcommon).

You cal also join us on:

- Freenode IRC - ``#ansible-network`` Freenode channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.


## Release notes
<!--Add a link to a changelog.md file or an external docsite to cover this information. -->

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Developing network resource modules](https://docs.ansible.com/ansible/latest/network/dev_guide/developing_resource_modules_network.html#developing-resource-modules)
- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENCE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
