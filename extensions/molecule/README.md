# Molecule coverage for network CLI consumers

This directory contains independent Molecule scenarios for `ansible.netcommon`
modules that send commands through `ansible.netcommon.network_cli`. The tests
run against NX-OS-shaped CISSHGO transcript fixtures. They exercise these
consumer flows over `network_cli`; they are not a vendor-platform coverage
matrix and do not require a live network device.

## Scenarios

Each flow has its own scenario directory, `molecule.yml`, `converge.yml`, and
collection requirements:

- `cli_command`
- `cli_config`
- `cli_backup`
- `cli_restore`
- `net_ping`
- `network_resource`
- `cli_parse_native`

The converge playbooks call their modules and assert the results explicitly.
This keeps each consumer independently runnable and lets CI report failures by
scenario.

## Fixtures and lifecycle

`cisshgo_fixtures/` contains the CISSHGO version pin, listener and Ansible
inventories, transcript map, and command/response fixtures. The version is
pinned in `cisshgo_fixtures/CISSHGO_VERSION` (`v1.0.0`). The shared `create.yml`
downloads that release when needed and starts the listeners defined by the
scenario inventory. `destroy.yml` stops the listeners, and `verify.yml` checks
the CISSHGO log for critical errors.

The `cli_flows.yml` manifest describes the source command flows used when
recording or regenerating fixtures. Its `task_file` entries are inputs to that
workflow; the checked-in scenario `converge.yml` files do not import the
manifest or those integration-test task files.

To record new device responses, enable recording in the `network_cli`
connection process with `ANSIBLE_NETWORK_CLI_RECORD=1` and set
`ANSIBLE_NETWORK_CLI_RECORD_PATH` to a temporary output directory. Keep live
recording plays and raw JSONL captures outside this collection. Commit the
reviewed, generated CISSHGO fixtures instead of raw device recordings.

## CI and dependencies

The collection test workflow discovers all seven scenarios under
`extensions/molecule` and runs each with both `libssh` and `paramiko`. The
Molecule job is included in the workflow's `all_green` result. CI installs the
`cisco.nxos` and `ansible.utils` collections before running the scenarios.
Individual `requirements.yml` files declare scenario dependencies; for example,
`cli_parse_native` also needs `ansible.utils`.

The dependency collection is named `cisco.nxos`. The scenario inventories use
`cisco.nxos.nxos` as the `ansible_network_os` platform plugin name. These are
different values: the former identifies the collection to install, and the
latter selects its NX-OS platform plugin.

The Molecule test harness is excluded from the built collection in `galaxy.yml`;
it is CI and development content, not installed collection runtime content.

## Run a scenario locally

Activate a Python environment containing Ansible, Molecule, and the SSH backend
dependencies. The `libssh` backend requires `ansible-pylibssh`; the `paramiko`
backend requires Paramiko. Run the commands from the collection root. Molecule
detects `extensions/molecule/config.yml` there and locates the scenarios under
`extensions/molecule`.

Install the scenario's collection requirements first, then run it with each
backend:

```bash
ansible-galaxy collection install \
  -r extensions/molecule/cli_command/requirements.yml
molecule test -s cli_command -- -e ansible_network_cli_ssh_type=libssh
molecule test -s cli_command -- -e ansible_network_cli_ssh_type=paramiko
```

For another scenario, replace `cli_command` in the install path and both
Molecule commands with its name. The `create.yml` playbook obtains the pinned
CISSHGO release and starts its listeners as part of the Molecule lifecycle. No
live device or sibling collection checkout is required.

If Paramiko reports a host-key mismatch for the local CISSHGO listener after a
previous run, remove only that listener's stale key and retry:

```bash
ssh-keygen -R '[127.0.0.1]:10000'
```
