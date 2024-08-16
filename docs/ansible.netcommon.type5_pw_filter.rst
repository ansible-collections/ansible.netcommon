
.. Created with antsibull-docs 2.9.0

ansible.netcommon.type5_pw filter -- The type5\_pw filter plugin.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This filter plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.type5_pw``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Filter plugin to produce cisco type5 hashed password.
- Using the parameters below - \ :literal:`xml\_data | ansible.netcommon.type5\_pw(template.yml`\ )








Keyword parameters
------------------

This describes keyword parameters of the filter. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
example: ``input | ansible.netcommon.type5_pw(key1=value1, key2=value2, ...)``

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
      <div class="ansibleOptionAnchor" id="parameter-password"></div>
      <p style="display: inline;"><strong>password</strong></p>
      <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>The password to be hashed.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-salt"></div>
      <p style="display: inline;"><strong>salt</strong></p>
      <a class="ansibleOptionLink" href="#parameter-salt" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Mention the salt to hash the password.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

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







Authors
~~~~~~~

- Ken Celenza (@itdependsnetworks)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
