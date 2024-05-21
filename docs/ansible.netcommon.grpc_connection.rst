.. _ansible.netcommon.grpc_connection:


**********************
ansible.netcommon.grpc
**********************

**Provides a persistent connection using the gRPC protocol**


Version added: 3.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This connection plugin provides a connection to remote devices over gRPC and is typically used with devices for sending and receiving RPC calls over gRPC framework.
- Note this connection plugin requires the grpcio python library to be installed on the local Ansible controller.



Requirements
------------
The below requirements are needed on the local Ansible controller node that executes this connection.

- grpcio
- protobuf


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>certificate_chain_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[grpc_connection]<br>certificate_chain_file = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_CERTIFICATE_CHAIN_FILE</div>
                                <div>var: ansible_certificate_chain_file</div>
                    </td>
                <td>
                        <div>The PEM encoded certificate chain file used to create a SSL-enabled channel. If the value is None, no certificate chain is used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>grpc_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"no"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[grpc_connection]<br>type = no</p>
                            </div>
                                <div>env:ANSIBLE_GRPC_CONNECTION_TYPE</div>
                                <div>var: ansible_grpc_connection_type</div>
                    </td>
                <td>
                        <div>This option indicates the grpc type and it can be used in place of network_os. (example cisco.iosxr.iosxr)</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"inventory_hostname"</div>
                </td>
                    <td>
                                <div>var: ansible_host</div>
                    </td>
                <td>
                        <div>Specifies the remote device FQDN or IP address to establish the gRPC connection to.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>import_modules</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"yes"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible_network]<br>import_modules = yes</p>
                            </div>
                                <div>env:ANSIBLE_NETWORK_IMPORT_MODULES</div>
                                <div>var: ansible_network_import_modules</div>
                    </td>
                <td>
                        <div>Reduce CPU usage and network module execution time by enabling direct execution. Instead of the module being packaged and executed by the shell, it will be directly executed by the Ansible control node using the same python interpreter as the Ansible process. Note- Incompatible with <code>asynchronous mode</code>. Note- Python 3 and Ansible 2.9.16 or greater required. Note- With Ansible 2.9.x fully qualified modules names are required in tasks.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>network_os</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>var: ansible_network_os</div>
                    </td>
                <td>
                        <div>Configures the device platform network operating system. This value is used to load a device specific grpc plugin to communicate with the remote device.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>var: ansible_password</div>
                                <div>var: ansible_ssh_pass</div>
                    </td>
                <td>
                        <div>Configures the user password used to authenticate to the remote device when first establishing the gRPC connection.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>persistent_command_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">30</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[persistent_connection]<br>command_timeout = 30</p>
                            </div>
                                <div>env:ANSIBLE_PERSISTENT_COMMAND_TIMEOUT</div>
                                <div>var: ansible_command_timeout</div>
                    </td>
                <td>
                        <div>Configures, in seconds, the amount of time to wait for a command to return from the remote device.  If this timer is exceeded before the command returns, the connection plugin will raise an exception and close.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>persistent_connect_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">30</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[persistent_connection]<br>connect_timeout = 30</p>
                            </div>
                                <div>env:ANSIBLE_PERSISTENT_CONNECT_TIMEOUT</div>
                                <div>var: ansible_connect_timeout</div>
                    </td>
                <td>
                        <div>Configures, in seconds, the amount of time to wait when trying to initially establish a persistent connection.  If this value expires before the connection to the remote device is completed, the connection will fail.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>persistent_log_messages</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"no"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[persistent_connection]<br>log_messages = no</p>
                            </div>
                                <div>env:ANSIBLE_PERSISTENT_LOG_MESSAGES</div>
                                <div>var: ansible_persistent_log_messages</div>
                    </td>
                <td>
                        <div>This flag will enable logging the command executed and response received from target device in the ansible log file. For this option to work &#x27;log_path&#x27; ansible configuration option is required to be set to a file path with write access.</div>
                        <div>Be sure to fully understand the security implications of enabling this option as it could create a security vulnerability by logging sensitive information in log file.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>remote_port = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_REMOTE_PORT</div>
                                <div>var: ansible_port</div>
                    </td>
                <td>
                        <div>Specifies the port on the remote device that listens for connections when establishing the gRPC connection. If None only the <code>host</code> part will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>private_key_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[grpc_connection]<br>private_key_file = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_PRIVATE_KEY_FILE</div>
                                <div>var: ansible_private_key_file</div>
                    </td>
                <td>
                        <div>The PEM encoded private key file used to authenticate to the remote device when first establishing the grpc connection.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>remote_user</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>remote_user = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_REMOTE_USER</div>
                                <div>var: ansible_user</div>
                    </td>
                <td>
                        <div>The username used to authenticate to the remote device when the gRPC connection is first established.  If the remote_user is not specified, the connection will use the username of the logged in user.</div>
                        <div>Can be configured from the CLI via the <code>--user</code> or <code>-u</code> options.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>root_certificates_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[grpc_connection]<br>root_certificates_file = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_ROOT_CERTIFICATES_FILE</div>
                                <div>var: ansible_root_certificates_file</div>
                    </td>
                <td>
                        <div>The PEM encoded root certificate file used to create a SSL-enabled channel, if the value is None it reads the root certificates from a default location chosen by gRPC at runtime.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ssl_target_name_override</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[grpc_connection]<br>ssl_target_name_override = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_GPRC_SSL_TARGET_NAME_OVERRIDE</div>
                                <div>var: ansible_grpc_ssl_target_name_override</div>
                    </td>
                <td>
                        <div>The option overrides SSL target name used for SSL host name checking. The name used for SSL host name checking will be the target parameter (assuming that the secure channel is an SSL channel). If this parameter is specified and the underlying is not an SSL channel, it will just be ignored.</div>
                </td>
            </tr>
    </table>
    <br/>








Status
------


Authors
~~~~~~~

- Ansible Networking Team (@ansible-network)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
