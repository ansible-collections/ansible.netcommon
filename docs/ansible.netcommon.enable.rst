
.. _ansible.netcommon.enable_:


ansible.netcommon.enable

Switch to elevated permissions on a network device



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This become plugins allows elevated permissions on a remote network device.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                            <th>Configuration</th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>become_pass</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                                                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                    <div> ini entries:
                                                                    <p>[enable_become_plugin]<br>password = VALUE</p>
                                                            </div>
                                                                                                            <div>env:ANSIBLE_BECOME_PASS</div>
                                                            <div>env:ANSIBLE_ENABLE_PASS</div>
                                                                                                                                        <div>var: ansible_become_password</div>
                                                            <div>var: ansible_become_pass</div>
                                                            <div>var: ansible_enable_pass</div>
                                                                        </td>
                                                <td>
                                            <div>password</div>
                                                        </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
   - enable is really implemented in the network connection handler and as such can only be used with network connections.
   - This plugin ignores the 'become_exe' and 'become_user' settings as it uses an API and not an executable.







Status
------


Authors
~~~~~~~

- ansible (@core)


.. hint::
    If you notice any issues in this documentation, you can `edit this document <https://github.com/ansible/ansible/edit/devel/lib/ansible/plugins//?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr>`_ to improve it.


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
