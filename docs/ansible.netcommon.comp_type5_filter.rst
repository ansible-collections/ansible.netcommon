
.. Created with antsibull-docs 2.9.0

ansible.netcommon.comp_type5 filter -- The comp\_type5 filter plugin.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This filter plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.comp_type5``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- The filter confirms configuration idempotency on use of type5\_pw.








Keyword parameters
------------------

This describes keyword parameters of the filter. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
example: ``input | ansible.netcommon.comp_type5(key1=value1, key2=value2, ...)``

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
      <div class="ansibleOptionAnchor" id="parameter-encrypted_password"></div>
      <p style="display: inline;"><strong>encrypted_password</strong></p>
      <a class="ansibleOptionLink" href="#parameter-encrypted_password" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>The encrypted text.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-return_original"></div>
      <p style="display: inline;"><strong>return_original</strong></p>
      <a class="ansibleOptionLink" href="#parameter-return_original" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>Return the original text.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-unencrypted_password"></div>
      <p style="display: inline;"><strong>unencrypted_password</strong></p>
      <a class="ansibleOptionLink" href="#parameter-unencrypted_password" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>The unencrypted text.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- The filter confirms configuration idempotency on use of type5\_pw.
- Can be used to validate password post hashing username cisco secret 5 {{ ansible\_ssh\_pass | ansible.netcommon.comp\_type5(encrypted, True) }}


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







Authors
~~~~~~~

- Ken Celenza (@itdependsnetworks)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
