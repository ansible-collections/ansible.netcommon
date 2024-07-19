
.. Created with antsibull-docs 2.9.0

ansible.netcommon.netconf_rpc module -- Execute operations on NETCONF enabled network devices.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ansible.netcommon.netconf_rpc_module_requirements_>`_ for details.

To use it in a playbook, specify: ``ansible.netcommon.netconf_rpc``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- NETCONF is a network management protocol developed and standardized by the IETF. It is documented in RFC 6241.
- This module allows the user to execute NETCONF RPC requests as defined by IETF RFC standards as well as proprietary requests.



.. _ansible_collections.ansible.netcommon.netconf_rpc_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- ncclient (\>=v0.5.2)
- jxmlease






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
      <p>This argument specifies the optional request content (all RPC attributes). The <em>content</em> value can either be provided as XML formatted string or as dictionary.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-display"></div>
      <p style="display: inline;"><strong>display</strong></p>
      <a class="ansibleOptionLink" href="#parameter-display" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Encoding scheme to use when serializing output from the device. The option <em>json</em> will serialize the output as JSON data. If the option value is <em>json</em> it requires jxmlease to be installed on control node. The option <em>pretty</em> is similar to received XML response but is using human readable format (spaces, new lines). The option value <em>xml</em> is similar to received XML response but removes all XML namespaces.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;json&#34;</code></p></li>
        <li><p><code>&#34;pretty&#34;</code></p></li>
        <li><p><code>&#34;xml&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-rpc"></div>
      <p style="display: inline;"><strong>rpc</strong></p>
      <a class="ansibleOptionLink" href="#parameter-rpc" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>This argument specifies the request (name of the operation) to be executed on the remote NETCONF enabled device.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-xmlns"></div>
      <p style="display: inline;"><strong>xmlns</strong></p>
      <a class="ansibleOptionLink" href="#parameter-xmlns" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>NETCONF operations not defined in rfc6241 typically require the appropriate XML namespace to be set. In the case the <em>request</em> option is not already provided in XML format, the namespace can be defined by the <em>xmlns</em> option.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- This module requires the NETCONF system service be enabled on the remote device being managed.
- This module supports the use of connection=netconf
- To execute \ :literal:`get-config`\ , \ :literal:`get`\  or \ :literal:`edit-config`\  requests it is recommended to use the Ansible \ :emphasis:`netconf\_get`\  and \ :emphasis:`netconf\_config`\  modules.
- This module is supported on \ :literal:`ansible\_network\_os`\  network platforms. See the :ref:\`Network Platform Options \<platform\_options\>\` for details.


Examples
--------

.. code-block:: yaml


    - name: lock candidate
      ansible.netcommon.netconf_rpc:
        rpc: lock
        content:
          target:
            candidate:

    - name: unlock candidate
      ansible.netcommon.netconf_rpc:
        rpc: unlock
        xmlns: urn:ietf:params:xml:ns:netconf:base:1.0
        content: "{'target': {'candidate': None}}"

    - name: discard changes
      ansible.netcommon.netconf_rpc:
        rpc: discard-changes

    - name: get-schema
      ansible.netcommon.netconf_rpc:
        rpc: get-schema
        xmlns: urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring
        content:
          identifier: ietf-netconf
          version: '2011-06-01'

    - name: copy running to startup
      ansible.netcommon.netconf_rpc:
        rpc: copy-config
        content:
          source:
            running:
          target:
            startup:

    - name: get schema list with JSON output
      ansible.netcommon.netconf_rpc:
        rpc: get
        content: |
          <filter>
            <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
              <schemas/>
            </netconf-state>
          </filter>
        display: json

    - name: get schema using XML request
      ansible.netcommon.netconf_rpc:
        rpc: get-schema
        xmlns: urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring
        content: |
          <identifier>ietf-netconf-monitoring</identifier>
          <version>2010-10-04</version>
        display: json





Return Values
-------------
The following are the fields unique to this module:

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th colspan="2"><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="return-output"></div>
      <p style="display: inline;"><strong>output</strong></p>
      <a class="ansibleOptionLink" href="#return-output" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">complex</span>
      </p>
    </td>
    <td valign="top">
      <p>Based on the value of display option will return either the set of transformed XML to JSON format from the RPC response with type dict or pretty XML string response (human-readable) or response with namespace removed from XML string.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when the display format is selected as JSON it is returned as dict type, if the display format is xml or pretty pretty it is returned as a string apart from low-level errors (such as action plugin).</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-output/formatted_output"></div>
      <p style="display: inline;"><strong>formatted_output</strong></p>
      <a class="ansibleOptionLink" href="#return-output/formatted_output" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Contains formatted response received from remote host as per the value in display format.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
    </td>
  </tr>

  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="return-stdout"></div>
      <p style="display: inline;"><strong>stdout</strong></p>
      <a class="ansibleOptionLink" href="#return-stdout" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The raw XML string containing configuration or state data received from the underlying ncclient library.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always apart from low-level errors (such as action plugin)</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;...&#34;</code></p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="return-stdout_lines"></div>
      <p style="display: inline;"><strong>stdout_lines</strong></p>
      <a class="ansibleOptionLink" href="#return-stdout_lines" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The value of stdout split into a list</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always apart from low-level errors (such as action plugin)</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;...&#34;, &#34;...&#34;]</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)
- Sven Wisotzky (@wisotzky)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
