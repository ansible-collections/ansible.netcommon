.. _ansible.netcommon.netconf_get_module:


*****************************
ansible.netcommon.netconf_get
*****************************

**Fetch configuration/state data from NETCONF enabled network devices.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- NETCONF is a network management protocol developed and standardized by the IETF. It is documented in RFC 6241.
- This module allows the user to fetch configuration and state data from NETCONF enabled network devices.



Requirements
------------
The below requirements are needed on the host that executes this module.

- ncclient (>=v0.5.2)
- jxmlease


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
                    <b>display</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                                                    </div>
                                    </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>json</li>
                                                                                                                                                                                                <li>pretty</li>
                                                                                                                                                                                                <li>xml</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                            <div>Encoding scheme to use when serializing output from the device. The option <em>json</em> will serialize the output as JSON data. If the option value is <em>json</em> it requires jxmlease to be installed on control node. The option <em>pretty</em> is similar to received XML response but is using human readable format (spaces, new lines). The option value <em>xml</em> is similar to received XML response but removes all XML namespaces.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                                                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>This argument specifies the XML string which acts as a filter to restrict the portions of the data to be are retrieved from the remote device. If this option is not specified entire configuration or state data is returned in result depending on the value of <code>source</code> option. The <code>filter</code> value can be either XML string or XPath, if the filter is in XPath format the NETCONF server running on remote host should support xpath capability else it will result in an error.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lock</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                                                    </div>
                                    </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>never</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>always</li>
                                                                                                                                                                                                <li>if-supported</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                            <div>Instructs the module to explicitly lock the datastore specified as <code>source</code>. If no <em>source</em> is defined, the <em>running</em> datastore will be locked. By setting the option value <em>always</em> is will explicitly lock the datastore mentioned in <code>source</code> option. By setting the option value <em>never</em> it will not lock the <code>source</code> datastore. The value <em>if-supported</em> allows better interworking with NETCONF servers, which do not support the (un)lock operation for all supported datastores.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                                                    </div>
                                    </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>running</li>
                                                                                                                                                                                                <li>candidate</li>
                                                                                                                                                                                                <li>startup</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                            <div>This argument specifies the datastore from which configuration data should be fetched. Valid values are <em>running</em>, <em>candidate</em> and <em>startup</em>. If the <code>source</code> value is not set both configuration and state information are returned in response from running datastore.</div>
                                                        </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
   - This module requires the NETCONF system service be enabled on the remote device being managed.
   - This module supports the use of connection=netconf
   - This module is supported on ``ansible_network_os`` network platforms. See the :ref:`Network Platform Options <platform_options>` for details.



Examples
--------

.. code-block:: yaml+jinja


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




Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>output</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">complex</span>
                                          </div>
                                    </td>
                <td>when the display format is selected as JSON it is returned as dict type, if the display format is xml or pretty pretty it is returned as a string apart from low-level errors (such as action plugin).</td>
                <td>
                                                                        <div>Based on the value of display option will return either the set of transformed XML to JSON format from the RPC response with type dict or pretty XML string response (human-readable) or response with namespace removed from XML string.</div>
                                                                <br/>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>formatted_output</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">-</span>
                                          </div>
                                    </td>
                <td></td>
                <td>
                                                                        <div>Contains formatted response received from remote host as per the value in display format.</div>
                                                                <br/>
                                    </td>
            </tr>

                                                <tr>
                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>always apart from low-level errors (such as action plugin)</td>
                <td>
                                                                        <div>The raw XML string containing configuration or state data received from the underlying ncclient library.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">...</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
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
- Sven Wisotzky (@wisotzky)
