
.. Created with antsibull-docs 2.9.0

ansible.netcommon.cli_restore module -- Restore device configuration to network devices over network\_cli
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.cli_restore``.

New in ansible.netcommon 6.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This module provides platform agnostic way of restore text based configuration to network devices over network\_cli connection plugin.
- The module uses the platforms \`config replace\` commands to restore backup configuration that is already copied over to the appliance.








Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-filename"></div>
      <p style="display: inline;"><strong>filename</strong></p>
      <a class="ansibleOptionLink" href="#parameter-filename" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Filename of the backup file, present in the appliance where the restore operation is to be performed. Check appliance for the configuration backup file name.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-path"></div>
      <p style="display: inline;"><strong>path</strong></p>
      <a class="ansibleOptionLink" href="#parameter-path" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The location in the target appliance where the file containing the backup exists. The path and the filename together create the input to the config replace command,</p>
      <p>For an IOSXE appliance the path pattern is flash://&lt;filename&gt;</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- This module is supported on \ :literal:`ansible\_network\_os`\  network platforms. See the :ref:\`Network Platform Options \<platform\_options\>\` for details.


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







Authors
~~~~~~~

- Sagar Paul (@KB-perByte)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
