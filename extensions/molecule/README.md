# Molecule scenarios for `network_cli` consumers

These scenarios exercise `ansible.netcommon` modules as collection consumers
over `ansible.netcommon.network_cli`. Each module flow has its own Molecule
scenario, explicit converge tasks, inventory, and cisshgo transcript. CI can
run the scenarios independently with both `libssh` and `paramiko`; none needs a
live device or a workstation-specific collection path.

## Coverage

| Scenario | What it checks | Why this flow is included |
| --- | --- | --- |
| `cli_command` | Runs `show version` and checks stable NX-OS version fields. | Covers the basic command request and response path. |
| `cli_config` | Applies hostname, NX-API, and templated interface configuration; checks resulting lines; removes the temporary interface; reapplies the hostname and feature to check idempotence. | Exercises configuration mode, templated input, state verification, and an unchanged second apply. |
| `cli_backup` | Creates a controller-side backup, checks that it is non-empty and contains stable configuration lines, then removes it. | Verifies both device retrieval and the local backup artifact. |
| `cli_restore` | Restores a staged full configuration backup and checks the device response. | Covers the restore command and its completion result. |
| `net_ping` | Pings the fixture's permitted destination and checks the received packet count and packet loss. | Exercises the network CLI ping response parser. |
| `network_resource` | Merges an interface description, restores the captured pre-change configuration, and checks that a repeat replace is unchanged. | Covers the resource-module consumer flow and restoration of the prior state. |
| `cli_parse_native` | Parses `show interface` output with the native parser using a checked-in template; also parses the same text response. | Covers both command and supplied-text entry points for the native parser. |
| `cli_parse_ntc_templates` | Parses `show interface` through NTC Templates from a command and from its text response, then compares the results. | Adds the lightweight NTC Templates backend also exercised by integration tests. It reuses the native scenario's identical command transcript. |
| `cli_parse_textfsm` | Parses `show version` output with a checked-in TextFSM template and checks boot image and platform fields. | Adds the TextFSM backend while keeping CLI transport replayed by cisshgo. |

The scenarios test netcommon modules and their network CLI transport. They do
not test `cisco.nxos` resource modules or include the separate NX-OS
`nxos_config` `src` caller flow. That caller-owned coverage belongs with the
NX-OS collection. The integration suite's pyATS parser case is deferred
because it requires a heavier controller dependency. Its XML parser case reads
a checked-in XML fixture and does not need a network CLI session.

## Dependencies and fixtures

The generic CLI scenarios use a small `molecule` terminal and cliconf plugin
from `cisshgo_fixtures/plugins/`. Molecule adds those fixture directories to
Ansible's plugin paths and sets `ansible_network_os: molecule`; these scenarios
do not install or load `cisco.nxos`. This keeps command, config, backup,
restore, and parser coverage independent of the NX-OS collection while still
replaying the reviewed NX-OS-shaped command transcripts.

`network_resource` declares `cisco.nxos` from Git main because the resource
module calls NX-OS resource definitions. `net_ping` declares the released
`cisco.nxos` collection because its action plugin dispatches to the
platform-specific `cisco.nxos.nxos_ping` implementation. These are the
only Molecule scenarios that install `cisco.nxos`. Parser scenarios declare
`ansible.utils` in their own `requirements.yml`; the NTC Templates scenario
sets its parser OS to `cisco_nxos` so it can select the NX-OS NTC template
while the transport remains `molecule`. NTC Templates and TextFSM also
install their Python parser packages in `prepare.yml`. Scenarios without
collection dependencies have no Galaxy dependency stage. The Molecule workflow
does not globally preinstall `cisco.nxos`.

`cisshgo_fixtures/` contains the pinned cisshgo version, per-scenario Ansible
and cisshgo inventories, the transcript map, and reviewed command/response
fixtures. The shared `create.yml` starts listeners for the selected scenario;
`destroy.yml` stops them and `verify.yml` checks the cisshgo log. Transcript
filenames describe the flow point, such as `before_show_running_config.txt`
and `after_hostname_feature_show_running_config.txt`.

`cli_flows.yml` records integration task files used as provenance when a live
flow is captured and a fixture is regenerated. It does not drive the Molecule
converge plays: each scenario defines its module calls and assertions
explicitly. Its `network_os` value identifies the real platform for live
recording; it does not install a collection or affect Molecule's runtime
requirements.

Transcript recording is opt-in through `ANSIBLE_NETWORK_CLI_RECORD=1` and
`ANSIBLE_NETWORK_CLI_RECORD_PATH`. The hook records command exchanges at the
`network_cli` send boundary; traffic that does not reach that method is outside
the recording. Recording is disabled by default and does not add hooks to
Cliconf or other connection plugins.

## Run locally

Run from the collection root with Molecule, Ansible, `ansible-pylibssh`, and
Paramiko installed in the active Python environment. Activate that environment
so Molecule's child `ansible-playbook` process uses the same Python. Scenarios
with declared collection requirements install them during their dependency
stage; `cli_command`, `cli_config`, `cli_backup`, and `cli_restore` need no
Galaxy dependency stage.

```bash
molecule test -s cli_config -- -e ansible_network_cli_ssh_type=libssh
molecule test -s cli_config -- -e ansible_network_cli_ssh_type=paramiko
```

Replace `cli_config` with another scenario name to run that flow. Repeat with
`ansible_network_cli_ssh_type=paramiko` to select the other backend. CI runs
scenario/backend pairs as isolated jobs. When running several Paramiko
scenarios locally, use an isolated `HOME` per run because each cisshgo listener
uses an ephemeral host key.

Molecule uses `extensions/molecule/config.yml` to locate the scenarios. A CI
runner needs access to the pinned cisshgo release when it is not already
installed; it does not need access to a network device.
