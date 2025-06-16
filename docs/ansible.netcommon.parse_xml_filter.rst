.. _ansible.netcommon.parse_xml_filter:


***************************
ansible.netcommon.parse_xml
***************************

**The parse_xml filter plugin.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This filter will load the spec file and pass the command output through it, returning JSON output.
- The YAML spec file defines how to parse the CLI output.
- This plugin is deprecated and will be removed in a future release after 2027-02-01, please Use ansible.utils.cli_parse instead.




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
                    <b>output</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>This source xml on which parse_xml invokes.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tmpl</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The spec file should be valid formatted YAML. It defines how to parse the XML output and return JSON data.</div>
                        <div>For example <code>xml_data | ansible.netcommon.parse_xml(template.yml</code>), in this case <code>xml_data</code> represents xml data option.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - To convert the XML output of a network device command into structured JSON output.



Examples
--------

.. code-block:: yaml

    # Using parse_xml

    # example_output.xml

    # <?xml version="1.0" encoding="UTF-8"?>
    # <rpc-reply message-id="urn:uuid:0cadb4e8-5bba-47f4-986e-72906227007f">
    # 	<data>
    # 		<ntp>
    # 			<nodes>
    # 				<node>
    # 					<node>0/0/CPU0</node>
    # 					<associations>
    # 						<is-ntp-enabled>true</is-ntp-enabled>
    # 						<sys-leap>ntp-leap-no-warning</sys-leap>
    # 						<peer-summary-info>
    # 							<peer-info-common>
    # 								<host-mode>ntp-mode-client</host-mode>
    # 								<is-configured>true</is-configured>
    # 								<address>10.1.1.1</address>
    # 								<reachability>0</reachability>
    # 							</peer-info-common>
    # 							<time-since>-1</time-since>
    # 						</peer-summary-info>
    # 						<peer-summary-info>
    # 							<peer-info-common>
    # 								<host-mode>ntp-mode-client</host-mode>
    # 								<is-configured>true</is-configured>
    # 								<address>172.16.252.29</address>
    # 								<reachability>255</reachability>
    # 							</peer-info-common>
    # 							<time-since>991</time-since>
    # 						</peer-summary-info>
    # 					</associations>
    # 				</node>
    # 			</nodes>
    # 		</ntp>
    # 	</data>
    # </rpc-reply>

    # parse_xml.yml

    # ---
    # vars:
    #   ntp_peers:
    #     address: "{{ item.address }}"
    #     reachability: "{{ item.reachability}}"
    # keys:
    #   result:
    #     value: "{{ ntp_peers }}"
    #     top: data/ntp/nodes/node/associations
    #     items:
    #       address: peer-summary-info/peer-info-common/address
    #       reachability: peer-summary-info/peer-info-common/reachability


    - name: Facts setup
      ansible.builtin.set_fact:
        xml: "{{ lookup('file', 'example_output.xml') }}"

    - name: Parse xml invocation
      ansible.builtin.debug:
        msg: "{{ xml | ansible.netcommon.parse_xml('parse_xml.yml') }}"


    # Task Output
    # -----------
    #
    # TASK [set xml Data]
    # ok: [host] => changed=false
    #   ansible_facts:
    #     xml: |-
    #       <?xml version="1.0" encoding="UTF-8"?>
    #       <rpc-reply message-id="urn:uuid:0cadb4e8-5bba-47f4-986e-72906227007f">
    #               <data>
    #                       <ntp>
    #                               <nodes>
    #                                       <node>
    #                                               <node>0/0/CPU0</node>
    #                                               <associations>
    #                                                       <is-ntp-enabled>true</is-ntp-enabled>
    #                                                       <sys-leap>ntp-leap-no-warning</sys-leap>
    #                                                       <peer-summary-info>
    #                                                               <peer-info-common>
    #                                                                       <host-mode>ntp-mode-client</host-mode>
    #                                                                       <is-configured>true</is-configured>
    #                                                                       <address>10.1.1.1</address>
    #                                                                       <reachability>0</reachability>
    #                                                               </peer-info-common>
    #                                                               <time-since>-1</time-since>
    #                                                       </peer-summary-info>
    #                                                       <peer-summary-info>
    #                                                               <peer-info-common>
    #                                                                       <host-mode>ntp-mode-client</host-mode>
    #                                                                       <is-configured>true</is-configured>
    #                                                                       <address>172.16.252.29</address>
    #                                                                       <reachability>255</reachability>
    #                                                               </peer-info-common>
    #                                                               <time-since>991</time-since>
    #                                                       </peer-summary-info>
    #                                               </associations>
    #                                       </node>
    #                               </nodes>
    #                       </ntp>
    #               </data>
    #       </rpc-reply>

    # TASK [Parse Data]
    # ok: [host] => changed=false
    #   ansible_facts:
    #     output:
    #       result:
    #       - address:
    #         - 10.1.1.1
    #         - 172.16.252.29
    #         reachability:
    #         - '0'
    #         - '255'




Status
------


Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
