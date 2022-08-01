.. _ansible.netcommon.grpc_get_module:


**************************
ansible.netcommon.grpc_get
**************************

**Fetch configuration/state data from gRPC enabled target hosts.**


Version added: 3.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- gRPC is a high performance, open-source universal RPC framework.
- This module allows the user to fetch configuration and state data from gRPC enabled devices.



Requirements
------------
The below requirements are needed on the host that executes this module.

- grpcio
- protobuf


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
                    <b>command</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The option specifies the command to be executed on the target host and return the response in result. This option is supported if the gRPC target host supports executing CLI command over the gRPC connection.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>data_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The type of data that should be fetched from the target host. The value depends on the capability of the gRPC server running on target host. The values can be <em>config</em>, <em>oper</em> etc. based on what is supported by the gRPC server. By default it will return both configuration and operational state data in response.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>display</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Encoding scheme to use when serializing output from the device. The encoding scheme value depends on the capability of the gRPC server running on the target host. The values can be <em>json</em>, <em>text</em> etc.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>section</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option specifies the string which acts as a filter to restrict the portions of the data to be retrieved from the target host device. If this option is not specified the entire configuration or state data is returned in response provided it is supported by target host.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: filter</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module requires the gRPC system service be enabled on the target host being managed.
   - This module supports the use of connection=ansible.netcommon.grpc.
   - This module requires the value of 'ansible_network_os or grpc_type' configuration option (refer ansible.netcommon.grpc connection plugin documentation) be defined as an inventory variable.
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
            command: 'show version'
            display: text



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
                    <b>output</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when the device response is valid JSON</td>
                <td>
                            <div>A dictionary representing a JSON-formatted response, if the response is a valid json string</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{
        &quot;Cisco-IOS-XR-ip-static-cfg:router-static&quot;: {
            &quot;default-vrf&quot;: {
                &quot;address-family&quot;: {
                    &quot;vrfipv4&quot;: {
                        &quot;vrf-unicast&quot;: {
                            &quot;vrf-prefixes&quot;: {
                                &quot;vrf-prefix&quot;: [
                                    {
                                        &quot;prefix&quot;: &quot;0.0.0.0&quot;,
                                        &quot;prefix-length&quot;: 0,
                                        &quot;vrf-route&quot;: {
                                            &quot;vrf-next-hop-table&quot;: {
                                                &quot;vrf-next-hop-interface-name-next-hop-address&quot;: [
                                                    {
                                                        &quot;interface-name&quot;: &quot;MgmtEth0/RP0/CPU0/0&quot;,
                                                        &quot;next-hop-address&quot;: &quot;10.0.2.2&quot;
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
    }]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always apart from low-level errors (such as action plugin)</td>
                <td>
                            <div>The raw string containing configuration or state data received from the gRPC server.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">...</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout_lines</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always apart from low-level errors (such as action plugin)</td>
                <td>
                            <div>The value of stdout split into a list</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;...&#x27;, &#x27;...&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)
- Gomathi Selvi S (@GomathiselviS)
