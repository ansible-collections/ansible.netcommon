.. _ansible.netcommon.hash_salt_filter:


***************************
ansible.netcommon.hash_salt
***************************

**The hash_salt filter plugin.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The filter plugin produces the salt from a hashed password.
- Using the parameters below - ``password | ansible.netcommon.hash_salt(template.yml``)




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
                        <div>This source data on which hash_salt invokes.</div>
                        <div>For example <code>password | ansible.netcommon.hash_salt</code>, in this case <code>password</code> represents the hashed password.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - The filter plugin produces the salt from a hashed password.



Examples
--------

.. code-block:: yaml

    # Using hash_salt

    # playbook

    - name: Set the facts
      ansible.builtin.set_fact:
        password: "$1$avs$uSTOEMh65ADDBREAKqzvpb9yBMpzd/"

    - name: Invoke hash_salt
      ansible.builtin.debug:
        msg: "{{ password | ansible.netcommon.hash_salt() }}"


    # Task Output
    # -----------
    #
    # TASK [Set the facts]
    # ok: [host] => changed=false
    #   ansible_facts:
    #     password: $1$avs$uSTOEMh65ADDBREAKqzvpb9yBMpzd/

    # TASK [Invoke hash_salt]
    # ok: [host] =>
    #   msg: avs




Status
------


Authors
~~~~~~~

- Ken Celenza (@itdependsnetworks)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
