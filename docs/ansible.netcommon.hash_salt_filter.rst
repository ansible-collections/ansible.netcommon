
.. Created with antsibull-docs 2.9.0

ansible.netcommon.hash_salt filter -- The hash\_salt filter plugin.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This filter plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.hash_salt``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- The filter plugin produces the salt from a hashed password.
- Using the parameters below - \ :literal:`password | ansible.netcommon.hash\_salt(template.yml`\ )








Keyword parameters
------------------

This describes keyword parameters of the filter. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
example: ``input | ansible.netcommon.hash_salt(key1=value1, key2=value2, ...)``

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
      <p>This source data on which hash_salt invokes.</p>
      <p>For example <code class='docutils literal notranslate'>password | ansible.netcommon.hash_salt</code>, in this case <code class='docutils literal notranslate'>password</code> represents the hashed password.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

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







Authors
~~~~~~~

- Ken Celenza (@itdependsnetworks)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
