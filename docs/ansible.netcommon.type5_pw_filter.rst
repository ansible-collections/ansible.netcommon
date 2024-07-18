.. _ansible.netcommon.type5_pw_filter:


**************************
ansible.netcommon.type5_pw
**************************

**The type5_pw filter plugin.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Filter plugin to produce cisco type5 hashed password.
- Using the parameters below - ``xml_data | ansible.netcommon.type5_pw(template.yml``)




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
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The password to be hashed.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>salt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Mention the salt to hash the password.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - The filter plugin generates cisco type5 hashed password.



Examples
--------

.. code-block:: yaml

    # Using type5_pw

    - name: Set some facts
      ansible.builtin.set_fact:
        password: "cisco@123"

    - name: Filter type5_pw invocation
      ansible.builtin.debug:
        msg: "{{ password | ansible.netcommon.type5_pw(salt='avs') }}"


    # Task Output
    # -----------
    #
    # TASK [Set some facts]
    # ok: [host] => changed=false
    #   ansible_facts:
    #     password: cisco@123

    # TASK [Filter type5_pw invocation]
    # ok: [host] =>
    #   msg: $1$avs$uSTOEMh65qzvpb9yBMpzd/




Status
------


Authors
~~~~~~~

- Ken Celenza (@itdependsnetworks)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
