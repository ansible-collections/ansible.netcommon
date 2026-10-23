# Molecule scenarios for `network_cli` consumers

These scenarios exercise `ansible.netcommon` modules as they are consumed by
collections through `ansible.netcommon.network_cli`. Each scenario has its own
Molecule configuration, inventory, converge play, and cisshgo transcript
fixture. They run without a live device and do not model vendor resource-module
states.

## Scenarios

| Scenario | Coverage |
| --- | --- |
| `cli_command` | Sends `show version` with `ansible.netcommon.cli_command` and checks the response. |
| `cli_config` | Applies hostname, feature, and interface configuration with `ansible.netcommon.cli_config`, then removes the temporary interface. |
| `cli_backup` | Uses `ansible.netcommon.cli_backup` and checks that its controller-side backup file is non-empty. |
| `cli_restore` | Restores a staged configuration with `ansible.netcommon.cli_restore`. |
| `net_ping` | Calls `ansible.netcommon.net_ping` and checks that packets are received. |
| `network_resource` | Merges an interface description, restores the captured interface configuration, and checks the restored state. |
| `cli_parse_native` | Parses `show interface` output with the native parser and a checked-in NX-OS template. |
| `cli_parse_ntc_templates` | Parses `show interface` with NTC Templates from both a command and the same text response, then compares the parsed results. |
| `cli_parse_textfsm` | Gets `show version` through `cli_command`, parses it with the checked-in TextFSM template, and checks the boot image and platform fields. |
| `nxos_config_src` | Renders a configuration file on the controller, passes its path to `cisco.nxos.nxos_config` through `network_cli`, and checks that configuration changed. |

The parser scenarios exercise distinct integration paths. The NTC Templates
and TextFSM dependencies are installed by each scenario's `prepare.yml` into
the active Ansible Python environment. The integration suite's pyATS parser
case is deferred because it requires a heavier controller dependency. Its XML
parser case reads a checked-in XML fixture and does not exercise a network CLI
session.

`cli_config` covers inline and templated configuration through the netcommon
module. `nxos_config_src` is a separate caller flow for the NX-OS config
module's `src` parameter; its temporary rendered file is removed even if the
apply or assertion task fails.

## Fixtures and lifecycle

`cisshgo_fixtures/` contains the pinned cisshgo version, per-scenario Ansible
and cisshgo inventories, the transcript map, and reviewed command/response
transcripts. The shared `create.yml` downloads the pinned cisshgo release and
starts listeners described by the selected scenario inventory. `destroy.yml`
stops those listeners, and `verify.yml` checks the cisshgo log.

`cli_flows.yml` records the integration task files used as input when device
flows are recorded and fixtures regenerated. Those entries are fixture
provenance; checked-in `converge.yml` files define their tasks explicitly and
do not import integration task files at runtime.

Each scenario has a `requirements.yml` for the collections it needs. The
parser scenarios install their Python parser packages during `prepare.yml`.
No scenario depends on an absolute workstation path or a sibling collection
checkout. CI installs collection requirements in its runner and exercises
each scenario with both `libssh` and `paramiko`.

## Run locally

Run these commands from the collection root with Ansible, Molecule,
`ansible-pylibssh`, and Paramiko available in the active Python environment.
Install a scenario's collection requirements before running it:

```bash
ansible-galaxy collection install \
  -r extensions/molecule/cli_parse_ntc_templates/requirements.yml
molecule test -s cli_parse_ntc_templates -- -e ansible_network_cli_ssh_type=libssh
molecule test -s cli_parse_ntc_templates -- -e ansible_network_cli_ssh_type=paramiko
```

Replace `cli_parse_ntc_templates` with another scenario name to run that
scenario. To run the full set with both SSH backends, install each scenario's
requirements and run:

```bash
for scenario in \
  cli_command cli_config cli_backup cli_restore net_ping network_resource \
  cli_parse_native cli_parse_ntc_templates cli_parse_textfsm nxos_config_src; do
  ansible-galaxy collection install \
    -r "extensions/molecule/${scenario}/requirements.yml"
  for backend in libssh paramiko; do
    molecule test -s "$scenario" \
      -- -e "ansible_network_cli_ssh_type=$backend" || exit 1
  done
done
```

Molecule uses `extensions/molecule/config.yml` to locate these scenarios. The
test runner needs access to the pinned cisshgo release when it is not already
installed; it does not need access to a network device.
