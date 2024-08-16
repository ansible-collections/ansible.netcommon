
.. Created with antsibull-docs 2.9.0

ansible.netcommon.grpc_get module -- Fetch configuration/state data from gRPC enabled target hosts.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ansible.netcommon.grpc_get_module_requirements_>`_ for details.

To use it in a playbook, specify: ``ansible.netcommon.grpc_get``.

New in ansible.netcommon 3.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- gRPC is a high performance, open-source universal RPC framework.
- This module allows the user to fetch configuration and state data from gRPC enabled devices.

This module has a corresponding action plugin.


.. _ansible_collections.ansible.netcommon.grpc_get_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- grpcio
- protobuf






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
      <div class="ansibleOptionAnchor" id="parameter-command"></div>
      <p style="display: inline;"><strong>command</strong></p>
      <a class="ansibleOptionLink" href="#parameter-command" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The option specifies the command to be executed on the target host and return the response in result. This option is supported if the gRPC target host supports executing CLI command over the gRPC connection.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-data_type"></div>
      <p style="display: inline;"><strong>data_type</strong></p>
      <a class="ansibleOptionLink" href="#parameter-data_type" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The type of data that should be fetched from the target host. The value depends on the capability of the gRPC server running on target host. The values can be <em>config</em>, <em>oper</em> etc. based on what is supported by the gRPC server. By default it will return both configuration and operational state data in response.</p>
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
      <p>Encoding scheme to use when serializing output from the device. The encoding scheme value depends on the capability of the gRPC server running on the target host. The values can be <em>json</em>, <em>text</em> etc.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-section"></div>
      <div class="ansibleOptionAnchor" id="parameter-filter"></div>
      <p style="display: inline;"><strong>section</strong></p>
      <a class="ansibleOptionLink" href="#parameter-section" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;"><span style="color: darkgreen; white-space: normal;">aliases: filter</span></p>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>This option specifies the string which acts as a filter to restrict the portions of the data to be retrieved from the target host device. If this option is not specified the entire configuration or state data is returned in response provided it is supported by target host.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- This module requires the gRPC system service be enabled on the target host being managed.
- This module supports the use of connection=ansible.netcommon.grpc.
- This module requires the value of 'ansible\_network\_os or grpc\_type' configuration option (refer ansible.netcommon.grpc connection plugin documentation) be defined as an inventory variable.
- Tested against iosxrv 9k version 6.1.2.


Examples
--------

.. code-block:: yaml


    - name: Get bgp configuration data
      grpc_get:
        section:
          Cisco-IOS-XR-ip-static-cfg:router-static:
            - null
    - name: run cli command
      grpc_get:
        command: "show version"
        display: text





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
      <div class="ansibleOptionAnchor" id="return-output"></div>
      <p style="display: inline;"><strong>output</strong></p>
      <a class="ansibleOptionLink" href="#return-output" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>A dictionary representing a JSON-formatted response, if the response is a valid json string</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when the device response is valid JSON</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;[{\n    \&#34;Cisco-IOS-XR-ip-static-cfg:router-static\&#34;: {\n        \&#34;default-vrf\&#34;: {\n            \&#34;address-family\&#34;: {\n                \&#34;vrfipv4\&#34;: {\n                    \&#34;vrf-unicast\&#34;: {\n                        \&#34;vrf-prefixes\&#34;: {\n                            \&#34;vrf-prefix\&#34;: [\n                                {\n                                    \&#34;prefix\&#34;: \&#34;0.0.0.0\&#34;&#34;, &#34;\n                                    \&#34;prefix-length\&#34;: 0&#34;, &#34;\n                                    \&#34;vrf-route\&#34;: {\n                                        \&#34;vrf-next-hop-table\&#34;: {\n                                            \&#34;vrf-next-hop-interface-name-next-hop-address\&#34;: [\n                                                {\n                                                    \&#34;interface-name\&#34;: \&#34;MgmtEth0/RP0/CPU0/0\&#34;&#34;, &#34;\n                                                    \&#34;next-hop-address\&#34;: \&#34;10.0.2.2\&#34;\n                                                }\n                                            ]\n                                        }\n                                    }\n                                }\n                            ]\n                        }\n                    }\n                }\n            }\n        }\n    }\n}]\n&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-stdout"></div>
      <p style="display: inline;"><strong>stdout</strong></p>
      <a class="ansibleOptionLink" href="#return-stdout" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The raw string containing configuration or state data received from the gRPC server.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always apart from low-level errors (such as action plugin)</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;...&#34;</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
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
- Gomathi Selvi S (@GomathiselviS)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
