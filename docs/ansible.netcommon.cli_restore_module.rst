.. _ansible.netcommon.cli_restore_module:


*****************************
ansible.netcommon.cli_restore
*****************************

**Restore device configuration to network devices over network_cli**


Version added: 6.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides platform agnostic way of restore text based configuration to network devices over network_cli connection plugin.
- The module uses the platforms `config replace` commands to restore backup configuration that is already copied over to the appliance.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filename</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Filename of the backup file, present in the appliance where the restore operation is to be performed. Check appliance for the configuration backup file name.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The location in the target appliance where the file containing the backup exists. The path and the filename together create the input to the config replace command,</div>
                        <div>For an IOSXE appliance the path pattern is flash://&lt;filename&gt;</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module is supported on ``ansible_network_os`` network platforms. See the :ref:`Network Platform Options <platform_options>` for details.



Examples
--------

.. code-block:: yaml

    - name: Restore IOS-XE configuration
      ansible.netcommon.cli_restore:
        filename: backupDday.cfg
        path: flash://

    # Command fired
    # -------------
    # config replace flash://backupDday.cfg force

    # Task Output
    # -----------
    #
    # ok: [BATMON] => changed=false
    #   __restore__: |-
    #     The rollback configlet from the last pass is listed below:
    #     ********
    #     !List of Rollback Commands:
    #     Building configuration...
    #     Current configuration : 3781 bytes
    #     end
    #     ********
    #
    #
    #     Rollback aborted after 5 passes
    #     The following commands are failed to apply to the IOS image.
    #     ********
    #     Building configuration...
    #     Current configuration : 3781 bytes
    #     ********
    #   invocation:
    #     module_args:
    #       filename: backupDday.cfg




Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)
