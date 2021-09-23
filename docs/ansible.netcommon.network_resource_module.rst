.. _ansible.netcommon.network_resource_module:


**********************************
ansible.netcommon.network_resource
**********************************

**Manage resource modules**


Version added: 2.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get list of available resource modules for given os name
- Retrieve given resource module configuration facts
- Push given resource module configuration




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The resource module configuration. For details on the type and structure of this option refer the individual resource module platform documentation.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the resource module to manage.</div>
                        <div>The resource module should be supported for given <em>os_name</em>, if not supported it will result in error.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>os_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the os to manage the resource modules.</div>
                        <div>The name should be fully qualified collection name format, that is <em>&lt;namespace&gt;.&lt;collection-name&gt;.&lt;plugin-name&gt;</em>.</div>
                        <div>If value of this option is not set the os value will be read from <em>ansible_network_os</em> variable.</div>
                        <div>If value of both <em>os_name</em> and <em>ansible_network_os</em> is not set it will result in error.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>running_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option is used only with state <em>parsed</em>.</div>
                        <div>The value of this option should be the output received from the host device by executing the cli command to get the resource configuration on host.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The state the configuration should be left in.</div>
                        <div>For supported values refer the individual resource module platform documentation.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Refer the individual module documentation for the valid inputs of *state* and *config* modules.



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
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>after</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when changed and  when <em>state</em> and/or <em>config</em> option is set</td>
                <td>
                            <div>The configuration as structured data after module completion.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format of the parameters above.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>before</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>When <em>state</em> and/or <em>config</em> option is set</td>
                <td>
                            <div>The configuration as structured data prior to module invocation.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format of the parameters above.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>When <em>state</em> and/or <em>config</em> option is set</td>
                <td>
                            <div>The set of commands pushed to the remote device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip access-list extended 110&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>modules</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>When only <em>os_name</em> or <em>ansible_network_os</em> is set</td>
                <td>
                            <div>List of resource modules supported for given OS.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;acl_interfaces&#x27;, &#x27;acls&#x27;, &#x27;bgp_global&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ganesh B. Nalawade (@ganeshrn)
