
.. Created with antsibull-docs 2.9.0

ansible.netcommon.restconf_config module -- Handles create, update, read and delete of configuration data on RESTCONF enabled devices.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.restconf_config``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- RESTCONF is a standard mechanisms to allow web applications to configure and manage data. RESTCONF is a IETF standard and documented on RFC 8040.
- This module allows the user to configure data on RESTCONF enabled devices.








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
      <div class="ansibleOptionAnchor" id="parameter-content"></div>
      <p style="display: inline;"><strong>content</strong></p>
      <a class="ansibleOptionLink" href="#parameter-content" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The configuration data in format as specififed in <code class='docutils literal notranslate'>format</code> option. Required unless <code class='docutils literal notranslate'>method</code> is <em>delete</em>.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-format"></div>
      <p style="display: inline;"><strong>format</strong></p>
      <a class="ansibleOptionLink" href="#parameter-format" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The format of the configuration provided as value of <code class='docutils literal notranslate'>content</code>. Accepted values are <em>xml</em> and <em>json</em> and the given configuration format should be supported by remote RESTCONF server.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;json&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;xml&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-method"></div>
      <p style="display: inline;"><strong>method</strong></p>
      <a class="ansibleOptionLink" href="#parameter-method" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The RESTCONF method to manage the configuration change on device. The value <em>post</em> is used to create a data resource or invoke an operation resource, <em>put</em> is used to replace the target data resource, <em>patch</em> is used to modify the target resource, and <em>delete</em> is used to delete the target resource.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;post&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;put&#34;</code></p></li>
        <li><p><code>&#34;patch&#34;</code></p></li>
        <li><p><code>&#34;delete&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-path"></div>
      <p style="display: inline;"><strong>path</strong></p>
      <a class="ansibleOptionLink" href="#parameter-path" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>URI being used to execute API calls.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- This module requires the RESTCONF system service be enabled on the remote device being managed.
- This module is supported with \ :emphasis:`ansible\_connection`\  value of \ :emphasis:`ansible.netcommon.httpapi`\  and \ :emphasis:`ansible\_network\_os`\  value of \ :emphasis:`ansible.netcommon.restconf`\ .
- This module is tested against Cisco IOSXE 16.12.02 version.


Examples
--------

.. code-block:: yaml


    - name: create l3vpn services
      ansible.netcommon.restconf_config:
        path: /config/ietf-l3vpn-svc:l3vpn-svc/vpn-services
        content: |
          {
            "vpn-service":[
                            {
                              "vpn-id": "red_vpn2",
                              "customer-name": "blue",
                              "vpn-service-topology": "ietf-l3vpn-svc:any-to-any"
                            },
                            {
                              "vpn-id": "blue_vpn1",
                              "customer-name": "red",
                              "vpn-service-topology": "ietf-l3vpn-svc:any-to-any"
                            }
                          ]
           }





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
      <div class="ansibleOptionAnchor" id="return-candidate"></div>
      <p style="display: inline;"><strong>candidate</strong></p>
      <a class="ansibleOptionLink" href="#return-candidate" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>The configuration sent to the device.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> When the method is not delete</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>{&#34;vpn-service&#34;: [{&#34;customer-name&#34;: &#34;red&#34;, &#34;vpn-id&#34;: &#34;blue_vpn1&#34;, &#34;vpn-service-topology&#34;: &#34;ietf-l3vpn-svc:any-to-any&#34;}]}</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-running"></div>
      <p style="display: inline;"><strong>running</strong></p>
      <a class="ansibleOptionLink" href="#return-running" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>The current running configuration on the device.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> When the method is not delete</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>{&#34;vpn-service&#34;: [{&#34;customer-name&#34;: &#34;blue&#34;, &#34;vpn-id&#34;: &#34;red_vpn2&#34;, &#34;vpn-service-topology&#34;: &#34;ietf-l3vpn-svc:any-to-any&#34;}, {&#34;customer-name&#34;: &#34;red&#34;, &#34;vpn-id&#34;: &#34;blue_vpn1&#34;, &#34;vpn-service-topology&#34;: &#34;ietf-l3vpn-svc:any-to-any&#34;}]}</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
