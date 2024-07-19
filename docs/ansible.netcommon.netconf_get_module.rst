
.. Created with antsibull-docs 2.9.0

ansible.netcommon.netconf_get module -- Fetch configuration/state data from NETCONF enabled network devices.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ansible.netcommon.netconf_get_module_requirements_>`_ for details.

To use it in a playbook, specify: ``ansible.netcommon.netconf_get``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- NETCONF is a network management protocol developed and standardized by the IETF. It is documented in RFC 6241.
- This module allows the user to fetch configuration and state data from NETCONF enabled network devices.



.. _ansible_collections.ansible.netcommon.netconf_get_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- ncclient (\>=v0.5.2)
- jxmlease (for display=json)
- xmltodict (for display=native)






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
        <li><p><code>&#34;native&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-filter"></div>
      <p style="display: inline;"><strong>filter</strong></p>
      <a class="ansibleOptionLink" href="#parameter-filter" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">any</span>
      </p>
    </td>
    <td valign="top">
      <p>This argument specifies the string which acts as a filter to restrict the portions of the data to be are retrieved from the remote device. If this option is not specified entire configuration or state data is returned in result depending on the value of <code class='docutils literal notranslate'>source</code> option. The <code class='docutils literal notranslate'>filter</code> value can be either XML string or XPath or JSON string or native python dictionary, if the filter is in XPath format the NETCONF server running on remote host should support xpath capability else it will result in an error. If the filter is in JSON format the xmltodict library should be installed on the control node for JSON to XML conversion.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-lock"></div>
      <p style="display: inline;"><strong>lock</strong></p>
      <a class="ansibleOptionLink" href="#parameter-lock" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Instructs the module to explicitly lock the datastore specified as <code class='docutils literal notranslate'>source</code>. If no <em>source</em> is defined, the <em>running</em> datastore will be locked. By setting the option value <em>always</em> is will explicitly lock the datastore mentioned in <code class='docutils literal notranslate'>source</code> option. By setting the option value <em>never</em> it will not lock the <code class='docutils literal notranslate'>source</code> datastore. The value <em>if-supported</em> allows better interworking with NETCONF servers, which do not support the (un)lock operation for all supported datastores.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;never&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;always&#34;</code></p></li>
        <li><p><code>&#34;if-supported&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-source"></div>
      <p style="display: inline;"><strong>source</strong></p>
      <a class="ansibleOptionLink" href="#parameter-source" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>This argument specifies the datastore from which configuration data should be fetched. Valid values are <em>running</em>, <em>candidate</em> and <em>startup</em>. If the <code class='docutils literal notranslate'>source</code> value is not set both configuration and state information are returned in response from running datastore.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;running&#34;</code></p></li>
        <li><p><code>&#34;candidate&#34;</code></p></li>
        <li><p><code>&#34;startup&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- This module requires the NETCONF system service be enabled on the remote device being managed.
- This module supports the use of connection=netconf
- This module is supported on \ :literal:`ansible\_network\_os`\  network platforms. See the :ref:\`Network Platform Options \<platform\_options\>\` for details.


Examples
--------

.. code-block:: yaml


    - name: Get running configuration and state data
      ansible.netcommon.netconf_get:

    - name: Get configuration and state data from startup datastore
      ansible.netcommon.netconf_get:
        source: startup

    - name: Get system configuration data from running datastore state (junos)
      ansible.netcommon.netconf_get:
        source: running
        filter: <configuration><system></system></configuration>

    - name: Get configuration and state data in JSON format
      ansible.netcommon.netconf_get:
        display: json

    - name: get schema list using subtree w/ namespaces
      ansible.netcommon.netconf_get:
        display: json
        filter: <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring"><schemas><schema/></schemas></netconf-state>
        lock: never

    - name: get schema list using xpath
      ansible.netcommon.netconf_get:
        display: xml
        filter: /netconf-state/schemas/schema

    - name: get interface configuration with filter (iosxr)
      ansible.netcommon.netconf_get:
        display: pretty
        filter: <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"></interface-configurations>
        lock: if-supported

    - name: Get system configuration data from running datastore state (junos)
      ansible.netcommon.netconf_get:
        source: running
        filter: <configuration><system></system></configuration>
        lock: if-supported

    - name: Get complete configuration data from running datastore (SROS)
      ansible.netcommon.netconf_get:
        source: running
        filter: <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf"/>

    - name: Get complete state data (SROS)
      ansible.netcommon.netconf_get:
        filter: <state xmlns="urn:nokia.com:sros:ns:yang:sr:state"/>

    - name: "get configuration with json filter string and native output (using xmltodict)"
      netconf_get:
        filter: |
          {
              "interface-configurations": {
                  "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                  "interface-configuration": null
              }
          }
        display: native

    - name: Define the Cisco IOSXR interface filter
      set_fact:
        filter:
          interface-configurations:
            "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"
            interface-configuration: null

    - name: "get configuration with native filter type using set_facts"
      ansible.netcommon.netconf_get:
        filter: "{{ filter }}"
        display: native
      register: result

    - name: "get configuration with direct native filter type"
      ansible.netcommon.netconf_get:
        filter:
          {
            "interface-configurations":
              {
                "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                "interface-configuration": null,
              },
          }
        display: native
      register: result

    # Make a round-trip interface description change, diff the before and after
    # this demonstrates the use of the native display format and several utilities
    # from the ansible.utils collection

    - name: Define the openconfig interface filter
      set_fact:
        filter:
          interfaces:
            "@xmlns": "http://openconfig.net/yang/interfaces"
            interface:
              name: Ethernet2

    - name: Get the pre-change config using the filter
      ansible.netcommon.netconf_get:
        source: running
        filter: "{{ filter }}"
        display: native
      register: pre

    - name: Update the description
      ansible.utils.update_fact:
        updates:
          - path: pre.output.data.interfaces.interface.config.description
            value: "Configured by ansible {{ 100 | random }}"
      register: updated

    - name: Apply the new configuration
      ansible.netcommon.netconf_config:
        content:
          config:
            interfaces: "{{ updated.pre.output.data.interfaces }}"

    - name: Get the post-change config using the filter
      ansible.netcommon.netconf_get:
        source: running
        filter: "{{ filter }}"
        display: native
      register: post

    - name: Show the differences between the pre and post configurations
      ansible.utils.fact_diff:
        before: "{{ pre.output.data|ansible.utils.to_paths }}"
        after: "{{ post.output.data|ansible.utils.to_paths }}"
    # TASK [Show the differences between the pre and post configurations] ********
    # --- before
    # +++ after
    # @@ -1,11 +1,11 @@
    #  {
    # -    "@time-modified": "2020-10-23T12:27:17.462332477Z",
    # +    "@time-modified": "2020-10-23T12:27:21.744541708Z",
    #      "@xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
    #      "interfaces.interface.aggregation.config['fallback-timeout']['#text']": "90",
    #      "interfaces.interface.aggregation.config['fallback-timeout']['@xmlns']": "http://arista.com/yang/openconfig/interfaces/augments",
    #      "interfaces.interface.aggregation.config['min-links']": "0",
    #      "interfaces.interface.aggregation['@xmlns']": "http://openconfig.net/yang/interfaces/aggregate",
    # -    "interfaces.interface.config.description": "Configured by ansible 56",
    # +    "interfaces.interface.config.description": "Configured by ansible 67",
    #      "interfaces.interface.config.enabled": "true",
    #      "interfaces.interface.config.mtu": "0",
    #      "interfaces.interface.config.name": "Ethernet2",





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
      <p style="margin-top: 8px;"><b>Returned:</b> If the display format is selected as <em>json</em> it is returned as dict type and the conversion is done using jxmlease python library. If the display format is selected as <em>native</em> it is returned as dict type and the conversion is done using xmltodict python library. If the display format is xml or pretty it is returned as a string apart from low-level errors (such as action plugin).</p>
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
