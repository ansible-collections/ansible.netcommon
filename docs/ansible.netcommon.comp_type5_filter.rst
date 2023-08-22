.. _ansible.netcommon.comp_type5_filter:


****************************
ansible.netcommon.comp_type5
****************************

**The comp_type5 filter plugin.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The filter confirms configuration idempotency on use of type5_pw.




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
                    <b>encrypted_password</b>
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
                        <div>The encrypted text.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>return_original</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Return the original text.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>unencrypted_password</b>
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
                        <div>The unencrypted text.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - The filter confirms configuration idempotency on use of type5_pw.
   - Can be used to validate password post hashing username cisco secret 5 {{ ansible_ssh_pass | ansible.netcommon.comp_type5(encrypted, True) }}



Examples
--------

.. code-block:: yaml

    # Using comp_type5

    # playbook

    - name: Set the facts
      ansible.builtin.set_fact:
        unencrypted_password: "cisco@123"
        encrypted_password: "$1$avs$uSTOEMh65ADDBREAKqzvpb9yBMpzd/"

    - name: Invoke comp_type5
      ansible.builtin.debug:
        msg: "{{ unencrypted_password | ansible.netcommon.comp_type5(encrypted_password, False) }}"

    # Task Output
    # -----------
    #
    # TASK [Set the facts]
    # ok: [35.155.113.92] => changed=false
    #   ansible_facts:
    #     encrypted_password: $1$avs$uSTOEMh65ADDBREAKqzvpb9yBMpzd/
    #     unencrypted_password: cisco@123

    # TASK [Invoke comp_type5]
    # ok: [35.155.113.92] =>
    #   msg: true




Status
------


Authors
~~~~~~~

- Ken Celenza (@itdependsnetworks)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
