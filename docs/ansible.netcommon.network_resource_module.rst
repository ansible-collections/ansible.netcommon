
.. Created with antsibull-docs 2.9.0

ansible.netcommon.network_resource module -- Manage resource modules
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.network_resource``.

New in ansible.netcommon 2.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Get list of available resource modules for given os name
- Retrieve given resource module configuration facts
- Push given resource module configuration

This module has a corresponding action plugin.







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
      <div class="ansibleOptionAnchor" id="parameter-config"></div>
      <p style="display: inline;"><strong>config</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">any</span>
      </p>
    </td>
    <td valign="top">
      <p>The resource module configuration. For details on the type and structure of this option refer the individual resource module platform documentation.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-name"></div>
      <p style="display: inline;"><strong>name</strong></p>
      <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The name of the resource module to manage.</p>
      <p>The resource module should be supported for given <em>os_name</em>, if not supported it will result in error.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-os_name"></div>
      <p style="display: inline;"><strong>os_name</strong></p>
      <a class="ansibleOptionLink" href="#parameter-os_name" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The name of the os to manage the resource modules.</p>
      <p>The name should be fully qualified collection name format, that is <em>&lt;namespace&gt;.&lt;collection-name&gt;.&lt;plugin-name&gt;</em>.</p>
      <p>If value of this option is not set the os value will be read from <em>ansible_network_os</em> variable.</p>
      <p>If value of both <em>os_name</em> and <em>ansible_network_os</em> is not set it will result in error.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-running_config"></div>
      <p style="display: inline;"><strong>running_config</strong></p>
      <a class="ansibleOptionLink" href="#parameter-running_config" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>This option is used only with state <em>parsed</em>.</p>
      <p>The value of this option should be the output received from the host device by executing the cli command to get the resource configuration on host.</p>
      <p>The state <em>parsed</em> reads the configuration from <code class='docutils literal notranslate'>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The state the configuration should be left in.</p>
      <p>For supported values refer the individual resource module platform documentation.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- Refer the individual module documentation for the valid inputs of \ :emphasis:`state`\  and \ :emphasis:`config`\  modules.


Examples
--------

.. code-block:: yaml


    - name: get list of resource modules for given network_os
      ansible.netcommon.network_resource:
      register: result

    - name: fetch acl config for
      ansible.netcommon.network_resource:
        os_name: cisco.ios.ios
        name: acls
        state: gathered

    - name: manage acl config for cisco.ios.ios network os.
      ansible.netcommon.network_resource:
        name: acls
        config:
          - afi: ipv4
            acls:
              - name: test_acl
                acl_type: extended
                aces:
                  - grant: deny
                    protocol_options:
                      tcp:
                        fin: true
                    source:
                      address: 192.0.2.0
                      wildcard_bits: 0.0.0.255
                    destination:
                      address: 192.0.3.0
                      wildcard_bits: 0.0.0.255
                      port_protocol:
                        eq: www
                    option:
                      traceroute: true
                    ttl:
                      eq: 10
        state: merged





Return Values
-------------
The following are the fields unique to this module:

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-after"></div>
      <p style="display: inline;"><strong>after</strong></p>
      <a class="ansibleOptionLink" href="#return-after" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The configuration as structured data after module completion.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when changed and  when <em>state</em> and/or <em>config</em> option is set</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;The configuration returned will always be in the same format of the parameters above.&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-before"></div>
      <p style="display: inline;"><strong>before</strong></p>
      <a class="ansibleOptionLink" href="#return-before" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The configuration as structured data prior to module invocation.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> When <em>state</em> and/or <em>config</em> option is set</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;The configuration returned will always be in the same format of the parameters above.&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-commands"></div>
      <p style="display: inline;"><strong>commands</strong></p>
      <a class="ansibleOptionLink" href="#return-commands" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The set of commands pushed to the remote device</p>
      <p style="margin-top: 8px;"><b>Returned:</b> When <em>state</em> and/or <em>config</em> option is set</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;ip access-list extended 110&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-modules"></div>
      <p style="display: inline;"><strong>modules</strong></p>
      <a class="ansibleOptionLink" href="#return-modules" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>List of resource modules supported for given OS.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> When only <em>os_name</em> or <em>ansible_network_os</em> is set</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;acl_interfaces&#34;, &#34;acls&#34;, &#34;bgp_global&#34;]</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Ganesh B. Nalawade (@ganeshrn)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
