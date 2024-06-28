
.. Created with antsibull-docs 2.9.0

ansible.netcommon.netconf_config module -- netconf device configuration
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ansible.netcommon.netconf_config_module_requirements_>`_ for details.

To use it in a playbook, specify: ``ansible.netcommon.netconf_config``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Netconf is a network management protocol developed and standardized by the IETF. It is documented in RFC 6241.
- This module allows the user to send a configuration XML file to a netconf device, and detects if there was a configuration change.



.. _ansible_collections.ansible.netcommon.netconf_config_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- ncclient






Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th colspan="2"><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-backup"></div>
      <p style="display: inline;"><strong>backup</strong></p>
      <a class="ansibleOptionLink" href="#parameter-backup" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>This argument will cause the module to create a full backup of the current <code class='docutils literal notranslate'>running-config</code> from the remote device before any changes are made. If the <code class='docutils literal notranslate'>backup_options</code> value is not given, the backup file is written to the <code class='docutils literal notranslate'>backup</code> folder in the playbook root directory or role root directory, if playbook is part of an ansible role. If the directory does not exist, it is created.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-backup_options"></div>
      <p style="display: inline;"><strong>backup_options</strong></p>
      <a class="ansibleOptionLink" href="#parameter-backup_options" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>This is a dict object containing configurable options related to backup file path. The value of this option is read only when <code class='docutils literal notranslate'>backup</code> is set to <em>yes</em>, if <code class='docutils literal notranslate'>backup</code> is set to <em>no</em> this option will be silently ignored.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-backup_options/dir_path"></div>
      <p style="display: inline;"><strong>dir_path</strong></p>
      <a class="ansibleOptionLink" href="#parameter-backup_options/dir_path" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">path</span>
      </p>
    </td>
    <td valign="top">
      <p>This option provides the path ending with directory name in which the backup configuration file will be stored. If the directory does not exist it will be first created and the filename is either the value of <code class='docutils literal notranslate'>filename</code> or default filename as described in <code class='docutils literal notranslate'>filename</code> options description. If the path value is not given in that case a <em>backup</em> directory will be created in the current working directory and backup configuration will be copied in <code class='docutils literal notranslate'>filename</code> within <em>backup</em> directory.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-backup_options/filename"></div>
      <p style="display: inline;"><strong>filename</strong></p>
      <a class="ansibleOptionLink" href="#parameter-backup_options/filename" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The filename to be used to store the backup configuration. If the filename is not given it will be generated based on the hostname, current time and date in format defined by &lt;hostname&gt;_config.&lt;current-date&gt;@&lt;current-time&gt;</p>
    </td>
  </tr>

  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-commit"></div>
      <p style="display: inline;"><strong>commit</strong></p>
      <a class="ansibleOptionLink" href="#parameter-commit" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>This boolean flag controls if the configuration changes should be committed or not after editing the candidate datastore. This option is supported only if remote Netconf server supports :candidate capability. If the value is set to <em>False</em> commit won&#x27;t be issued after edit-config operation and user needs to handle commit or discard-changes explicitly.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-confirm"></div>
      <p style="display: inline;"><strong>confirm</strong></p>
      <a class="ansibleOptionLink" href="#parameter-confirm" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>
    </td>
    <td valign="top">
      <p>This argument will configure a timeout value for the commit to be confirmed before it is automatically rolled back. If the <code class='docutils literal notranslate'>confirm_commit</code> argument is set to False, this argument is silently ignored. If the value of this argument is set to 0, the commit is confirmed immediately. The remote host MUST support :candidate and :confirmed-commit capability for this option to .</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">0</code></p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-confirm_commit"></div>
      <p style="display: inline;"><strong>confirm_commit</strong></p>
      <a class="ansibleOptionLink" href="#parameter-confirm_commit" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>This argument will execute commit operation on remote device. It can be used to confirm a previous commit.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-content"></div>
      <div class="ansibleOptionAnchor" id="parameter-xml"></div>
      <p style="display: inline;"><strong>content</strong></p>
      <a class="ansibleOptionLink" href="#parameter-content" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;"><span style="color: darkgreen; white-space: normal;">aliases: xml</span></p>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">any</span>
      </p>
    </td>
    <td valign="top">
      <p>The configuration data as defined by the device&#x27;s data models, the value can be either in xml string format or text format or python dictionary representation of JSON format.</p>
      <p>In case of json string format it will be converted to the corresponding xml string using xmltodict library before pushing onto the remote host.</p>
      <p>In case the value of this option isn <em>text</em> format the format should be supported by remote Netconf server.</p>
      <p>If the value of <code class='docutils literal notranslate'>content</code> option is in <em>xml</em> format in that case the xml value should have <em>config</em> as root tag.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-default_operation"></div>
      <p style="display: inline;"><strong>default_operation</strong></p>
      <a class="ansibleOptionLink" href="#parameter-default_operation" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The default operation for &lt;edit-config&gt; rpc, valid values are <em>merge</em>, <em>replace</em> and <em>none</em>. If the default value is merge, the configuration data in the <code class='docutils literal notranslate'>content</code> option is merged at the corresponding level in the <code class='docutils literal notranslate'>target</code> datastore. If the value is replace the data in the <code class='docutils literal notranslate'>content</code> option completely replaces the configuration in the <code class='docutils literal notranslate'>target</code> datastore. If the value is none the <code class='docutils literal notranslate'>target</code> datastore is unaffected by the configuration in the config option, unless and until the incoming configuration data uses the <code class='docutils literal notranslate'>operation</code> operation to request a different operation.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;merge&#34;</code></p></li>
        <li><p><code>&#34;replace&#34;</code></p></li>
        <li><p><code>&#34;none&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-delete"></div>
      <p style="display: inline;"><strong>delete</strong></p>
      <a class="ansibleOptionLink" href="#parameter-delete" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>It instructs the module to delete the configuration from value mentioned in <code class='docutils literal notranslate'>target</code> datastore.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-error_option"></div>
      <p style="display: inline;"><strong>error_option</strong></p>
      <a class="ansibleOptionLink" href="#parameter-error_option" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>This option controls the netconf server action after an error occurs while editing the configuration.</p>
      <p>If <em>error_option=stop-on-error</em>, abort the config edit on first error.</p>
      <p>If <em>error_option=continue-on-error</em>, continue to process configuration data on error. The error is recorded and negative response is generated if any errors occur.</p>
      <p>If <em>error_option=rollback-on-error</em>, rollback to the original configuration if any error occurs. This requires the remote Netconf server to support the <em>error_option=rollback-on-error</em> capability.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;stop-on-error&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;continue-on-error&#34;</code></p></li>
        <li><p><code>&#34;rollback-on-error&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-format"></div>
      <p style="display: inline;"><strong>format</strong></p>
      <a class="ansibleOptionLink" href="#parameter-format" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The format of the configuration provided as value of <code class='docutils literal notranslate'>content</code>.</p>
      <p>In case of json string format it will be converted to the corresponding xml string using xmltodict library before pushing onto the remote host.</p>
      <p>In case of <em>text</em> format of the configuration should be supported by remote Netconf server.</p>
      <p>If the value of <code class='docutils literal notranslate'>format</code> options is not given it tries to guess the data format of <code class='docutils literal notranslate'>content</code> option as one of <em>xml</em> or <em>json</em> or <em>text</em>.</p>
      <p>If the data format is not identified it is set to <em>xml</em> by default.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;xml&#34;</code></p></li>
        <li><p><code>&#34;text&#34;</code></p></li>
        <li><p><code>&#34;json&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-get_filter"></div>
      <p style="display: inline;"><strong>get_filter</strong></p>
      <a class="ansibleOptionLink" href="#parameter-get_filter" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">any</span>
      </p>
    </td>
    <td valign="top">
      <p>This argument specifies the XML string which acts as a filter to restrict the portions of the data retrieved from the remote device when comparing the before and after state of the device following calls to edit_config. When not specified, the entire configuration or state data is returned for comparison depending on the value of <code class='docutils literal notranslate'>source</code> option. The <code class='docutils literal notranslate'>get_filter</code> value can be either XML string or XPath or JSON string or native python dictionary, if the filter is in XPath format the NETCONF server running on remote host should support xpath capability else it will result in an error.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-lock"></div>
      <p style="display: inline;"><strong>lock</strong></p>
      <a class="ansibleOptionLink" href="#parameter-lock" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Instructs the module to explicitly lock the datastore specified as <code class='docutils literal notranslate'>target</code>. By setting the option value <em>always</em> is will explicitly lock the datastore mentioned in <code class='docutils literal notranslate'>target</code> option. It the value is <em>never</em> it will not lock the <code class='docutils literal notranslate'>target</code> datastore. The value <em>if-supported</em> lock the <code class='docutils literal notranslate'>target</code> datastore only if it is supported by the remote Netconf server.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;never&#34;</code></p></li>
        <li><p><code style="color: blue;"><b>&#34;always&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;if-supported&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-save"></div>
      <p style="display: inline;"><strong>save</strong></p>
      <a class="ansibleOptionLink" href="#parameter-save" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>The <code class='docutils literal notranslate'>save</code> argument instructs the module to save the configuration in <code class='docutils literal notranslate'>target</code> datastore to the startup-config if changed and if :startup capability is supported by Netconf server.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-source_datastore"></div>
      <div class="ansibleOptionAnchor" id="parameter-source"></div>
      <p style="display: inline;"><strong>source_datastore</strong></p>
      <a class="ansibleOptionLink" href="#parameter-source_datastore" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;"><span style="color: darkgreen; white-space: normal;">aliases: source</span></p>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Name of the configuration datastore to use as the source to copy the configuration to the datastore mentioned by <code class='docutils literal notranslate'>target</code> option. The values can be either <em>running</em>, <em>candidate</em>, <em>startup</em> or a remote URL</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-target"></div>
      <div class="ansibleOptionAnchor" id="parameter-datastore"></div>
      <p style="display: inline;"><strong>target</strong></p>
      <a class="ansibleOptionLink" href="#parameter-target" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;"><span style="color: darkgreen; white-space: normal;">aliases: datastore</span></p>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Name of the configuration datastore to be edited. - auto, uses candidate and fallback to running - candidate, edit &lt;candidate/&gt; datastore and then commit - running, edit &lt;running/&gt; datastore directly</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;auto&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;candidate&#34;</code></p></li>
        <li><p><code>&#34;running&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-validate"></div>
      <p style="display: inline;"><strong>validate</strong></p>
      <a class="ansibleOptionLink" href="#parameter-validate" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>This boolean flag if set validates the content of datastore given in <code class='docutils literal notranslate'>target</code> option. For this option to work remote Netconf server should support :validate capability.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- This module requires the netconf system service be enabled on the remote device being managed.
- This module supports devices with and without the candidate and confirmed-commit capabilities. It will always use the safer feature.
- This module supports the use of connection=netconf
- This module is supported on \ :literal:`ansible\_network\_os`\  network platforms. See the :ref:\`Network Platform Options \<platform\_options\>\` for details.


Examples
--------

.. code-block:: yaml


    - name: use lookup filter to provide xml configuration
      ansible.netcommon.netconf_config:
        content: "{{ lookup('file', './config.xml') }}"

    - name: set ntp server in the device
      ansible.netcommon.netconf_config:
        content: |
          <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
              <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
                  <ntp>
                      <enabled>true</enabled>
                      <server>
                          <name>ntp1</name>
                          <udp><address>127.0.0.1</address></udp>
                      </server>
                  </ntp>
              </system>
          </config>

    - name: wipe ntp configuration
      ansible.netcommon.netconf_config:
        content: |
          <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
              <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
                  <ntp>
                      <enabled>false</enabled>
                      <server operation="remove">
                          <name>ntp1</name>
                      </server>
                  </ntp>
              </system>
          </config>

    - name: configure interface while providing different private key file path (for connection=netconf)
      ansible.netcommon.netconf_config:
        backup: true
      register: backup_junos_location
      vars:
        ansible_private_key_file: /home/admin/.ssh/newprivatekeyfile

    - name: configurable backup path
      ansible.netcommon.netconf_config:
        backup: true
        backup_options:
          filename: backup.cfg
          dir_path: /home/user

    - name: "configure using direct native format configuration (cisco iosxr)"
      ansible.netcommon.netconf_config:
        format: json
        content:
          {
            "config":
              {
                "interface-configurations":
                  {
                    "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                    "interface-configuration":
                      {
                        "active": "act",
                        "description": "test for ansible Loopback999",
                        "interface-name": "Loopback999",
                      },
                  },
              },
          }
        get_filter:
          {
            "interface-configurations":
              {
                "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                "interface-configuration": null,
              },
          }

    - name: "configure using json string format configuration (cisco iosxr)"
      ansible.netcommon.netconf_config:
        format: json
        content: |
          {
              "config": {
                  "interface-configurations": {
                      "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                      "interface-configuration": {
                          "active": "act",
                          "description": "test for ansible Loopback999",
                          "interface-name": "Loopback999"
                      }
                  }
              }
          }
        get_filter: |
          {
                "interface-configurations": {
                    "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                    "interface-configuration": null
                }
            }

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
    <th><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-backup_path"></div>
      <p style="display: inline;"><strong>backup_path</strong></p>
      <a class="ansibleOptionLink" href="#return-backup_path" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The full path to the backup file</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when backup is yes</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;/playbooks/ansible/backup/config.2016-07-16@22:28:34&#34;</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-diff"></div>
      <p style="display: inline;"><strong>diff</strong></p>
      <a class="ansibleOptionLink" href="#return-diff" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>If --diff option in enabled while running, the before and after configuration change are returned as part of before and after key.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when diff is enabled</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>{&#34;after&#34;: &#34;&lt;rpc-reply&gt; &lt;data&gt; &lt;configuration&gt; &lt;version&gt;17.3R1.10&lt;/version&gt;...&lt;--snip--&gt;&#34;, &#34;before&#34;: &#34;&lt;rpc-reply&gt; &lt;data&gt; &lt;configuration&gt; &lt;version&gt;17.3R1.10&lt;/version&gt;...&lt;--snip--&gt;&#34;}</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-server_capabilities"></div>
      <p style="display: inline;"><strong>server_capabilities</strong></p>
      <a class="ansibleOptionLink" href="#return-server_capabilities" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>list of capabilities of the server</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;urn:ietf:params:netconf:base:1.1&#34;, &#34;urn:ietf:params:netconf:capability:confirmed-commit:1.0&#34;, &#34;urn:ietf:params:netconf:capability:candidate:1.0&#34;]</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Leandro Lisboa Penz (@lpenz)
- Ganesh Nalawade (@ganeshrn)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
