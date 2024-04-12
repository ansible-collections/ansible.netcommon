
.. Created with antsibull-docs 2.9.0

ansible.netcommon.pop_ace filter -- Remove ace entries from a acl source of truth.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This filter plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.pop_ace``.

New in ansible.netcommon 5.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This plugin removes specific keys from a provided acl data.
- Using the parameters below - \ :literal:`acls\_data | ansible.netcommon.pop\_ace(filter\_options=filter\_options, match\_criteria=match\_criteria`\ )








Keyword parameters
------------------

This describes keyword parameters of the filter. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
example: ``input | ansible.netcommon.pop_ace(key1=value1, key2=value2, ...)``

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
      <div class="ansibleOptionAnchor" id="parameter-data"></div>
      <p style="display: inline;"><strong>data</strong></p>
      <a class="ansibleOptionLink" href="#parameter-data" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">any</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>This option represents a list of dictionaries of acls facts.</p>
      <p>For example <code class='docutils literal notranslate'>acls_data | ansible.netcommon.pop_ace(filter_options=filter_options, match_criteria=match_criteria</code>), in this case <code class='docutils literal notranslate'>acls_data</code> represents this option.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-filter_options"></div>
      <p style="display: inline;"><strong>filter_options</strong></p>
      <a class="ansibleOptionLink" href="#parameter-filter_options" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>

    </td>
    <td valign="top">
      <p>Specify filtering options which drives the filter plugin.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-filter_options/failed_when"></div>
      <p style="display: inline;"><strong>failed_when</strong></p>
      <a class="ansibleOptionLink" href="#parameter-filter_options/failed_when" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>On missing it fails when there is no match with the ACL data supplied</p>
      <p>On never it would never fail</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;missing&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;never&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-filter_options/match_all"></div>
      <p style="display: inline;"><strong>match_all</strong></p>
      <a class="ansibleOptionLink" href="#parameter-filter_options/match_all" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>When true ensures ace removed only when it matches all match criteria</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-filter_options/remove"></div>
      <p style="display: inline;"><strong>remove</strong></p>
      <a class="ansibleOptionLink" href="#parameter-filter_options/remove" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Remove first removes one ace from each ACL entry on match</p>
      <p>Remove all is more aggressive and removes more than one on match</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;first&#34;</code></p></li>
        <li><p><code style="color: blue;"><b>&#34;all&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

    </td>
  </tr>

  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-match_criteria"></div>
      <p style="display: inline;"><strong>match_criteria</strong></p>
      <a class="ansibleOptionLink" href="#parameter-match_criteria" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>Specify the matching configuration of the ACEs to remove.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-match_criteria/acl_name"></div>
      <p style="display: inline;"><strong>acl_name</strong></p>
      <a class="ansibleOptionLink" href="#parameter-match_criteria/acl_name" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>ACL name to match</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-match_criteria/afi"></div>
      <p style="display: inline;"><strong>afi</strong></p>
      <a class="ansibleOptionLink" href="#parameter-match_criteria/afi" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>Specify afi to match</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-match_criteria/destination"></div>
      <p style="display: inline;"><strong>destination</strong></p>
      <a class="ansibleOptionLink" href="#parameter-match_criteria/destination" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Destination address/ host/ any of the ACE to natch</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-match_criteria/grant"></div>
      <p style="display: inline;"><strong>grant</strong></p>
      <a class="ansibleOptionLink" href="#parameter-match_criteria/grant" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Grant type permit or deny to match</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-match_criteria/protocol"></div>
      <p style="display: inline;"><strong>protocol</strong></p>
      <a class="ansibleOptionLink" href="#parameter-match_criteria/protocol" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Protocol name of the ACE to match</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-match_criteria/sequence"></div>
      <p style="display: inline;"><strong>sequence</strong></p>
      <a class="ansibleOptionLink" href="#parameter-match_criteria/sequence" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Sequence number of the ACE to match</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-match_criteria/source"></div>
      <p style="display: inline;"><strong>source</strong></p>
      <a class="ansibleOptionLink" href="#parameter-match_criteria/source" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Source address/ host/ any of the ACE to match</p>
    </td>
  </tr>

  </tbody>
  </table>




Notes
-----

- The filter plugin has been tested with facts collected for acls resource module on Cisco IOSXE, IOSXR and NXOS.


Examples
--------

.. code-block:: yaml


    ## Playbook with filter plugin example
    vars:
      filter_options:
        match_all: true
      match_criteria:
        afi: "ipv4"
        source: "192.0.2.0"
        destination: "192.0.3.0"
      acls_data:
        - acls:
            - aces:
                - destination:
                    address: 192.0.3.0
                    wildcard_bits: 0.0.0.255
                  dscp: ef
                  grant: deny
                  protocol: icmp
                  protocol_options:
                    icmp:
                      traceroute: true
                  sequence: 10
                  source:
                    address: 192.0.2.0
                    wildcard_bits: 0.0.0.255
                  ttl:
                    eq: 10
                - destination:
                    host: 198.51.110.0
                    port_protocol:
                      eq: telnet
                  grant: deny
                  protocol: tcp
                  protocol_options:
                    tcp:
                      ack: true
                  sequence: 20
                  source:
                    host: 198.51.100.0
              acl_type: extended
              name: "110"
            - aces:
                - destination:
                    address: 198.51.101.0
                    port_protocol:
                      eq: telnet
                    wildcard_bits: 0.0.0.255
                  grant: deny
                  protocol: tcp
                  protocol_options:
                    tcp:
                      ack: true
                  sequence: 10
                  source:
                    address: 198.51.100.0
                    wildcard_bits: 0.0.0.255
                  tos:
                    service_value: 12
                - destination:
                    address: 192.0.4.0
                    port_protocol:
                      eq: www
                    wildcard_bits: 0.0.0.255
                  dscp: ef
                  grant: deny
                  protocol: tcp
                  protocol_options:
                    tcp:
                      ack: true
                  sequence: 20
                  source:
                    address: 192.0.3.0
                    wildcard_bits: 0.0.0.255
                  ttl:
                    lt: 20
              acl_type: extended
              name: "123"
            - aces:
                - grant: deny
                  sequence: 10
                  source:
                    host: 192.168.1.200
                - grant: deny
                  sequence: 20
                  source:
                    address: 192.168.2.0
                    wildcard_bits: 0.0.0.255
              acl_type: standard
              name: std_acl
            - aces:
                - destination:
                    address: 192.0.3.0
                    port_protocol:
                      eq: www
                    wildcard_bits: 0.0.0.255
                  grant: deny
                  option:
                    traceroute: true
                  protocol: tcp
                  protocol_options:
                    tcp:
                      fin: true
                  sequence: 10
                  source:
                    address: 192.0.2.0
                    wildcard_bits: 0.0.0.255
                  ttl:
                    eq: 10
              acl_type: extended
              name: test
          afi: ipv4
        - acls:
            - aces:
                - destination:
                    any: true
                    port_protocol:
                      eq: telnet
                  dscp: af11
                  grant: deny
                  protocol: tcp
                  protocol_options:
                    tcp:
                      ack: true
                  sequence: 10
                  source:
                    any: true
                    port_protocol:
                      eq: www
              name: R1_TRAFFIC
          afi: ipv6

    tasks:
      - name: Remove ace entries from a provided data
        ansible.builtin.debug:
          msg: "{{ acls_data | ansible.netcommon.pop_ace(filter_options=filter_options, match_criteria=match_criteria) }}"

    ## Output
    # PLAY [Filter plugin example pop_ace] ******************************************************************************************************************

    # TASK [Remove ace entries from a provided data] ***********************************************************************************************************
    # ok: [xe_machine] =>
    #   msg:
    #     clean_acls:
    #       acls:
    #       - acls:
    #         - aces:
    #           - destination:
    #               host: 198.51.110.0
    #               port_protocol:
    #                 eq: telnet
    #             grant: deny
    #             protocol: tcp
    #             protocol_options:
    #               tcp:
    #                 ack: true
    #             sequence: 20
    #             source:
    #               host: 198.51.100.0
    #           name: '110'
    #         - aces:
    #           - destination:
    #               address: 198.51.101.0
    #               port_protocol:
    #                 eq: telnet
    #               wildcard_bits: 0.0.0.255
    #             grant: deny
    #             protocol: tcp
    #             protocol_options:
    #               tcp:
    #                 ack: true
    #             sequence: 10
    #             source:
    #               address: 198.51.100.0
    #               wildcard_bits: 0.0.0.255
    #             tos:
    #               service_value: 12
    #           - destination:
    #               address: 192.0.4.0
    #               port_protocol:
    #                 eq: www
    #               wildcard_bits: 0.0.0.255
    #             dscp: ef
    #             grant: deny
    #             protocol: tcp
    #             protocol_options:
    #               tcp:
    #                 ack: true
    #             sequence: 20
    #             source:
    #               address: 192.0.3.0
    #               wildcard_bits: 0.0.0.255
    #             ttl:
    #               lt: 20
    #           name: '123'
    #         - aces:
    #           - grant: deny
    #             sequence: 10
    #             source:
    #               host: 192.168.1.200
    #           - grant: deny
    #             sequence: 20
    #             source:
    #               address: 192.168.2.0
    #               wildcard_bits: 0.0.0.255
    #           name: std_acl
    #         afi: ipv4
    #       - acls:
    #         - aces:
    #           - destination:
    #               any: true
    #               port_protocol:
    #                 eq: telnet
    #             dscp: af11
    #             grant: deny
    #             protocol: tcp
    #             protocol_options:
    #               tcp:
    #                 ack: true
    #             sequence: 10
    #             source:
    #               any: true
    #               port_protocol:
    #                 eq: www
    #           name: R1_TRAFFIC
    #         afi: ipv6
    #     removed_aces:
    #       acls:
    #       - acls:
    #         - aces:
    #           - destination:
    #               address: 192.0.3.0
    #               wildcard_bits: 0.0.0.255
    #             dscp: ef
    #             grant: deny
    #             protocol: icmp
    #             protocol_options:
    #               icmp:
    #                 traceroute: true
    #             sequence: 10
    #             source:
    #               address: 192.0.2.0
    #               wildcard_bits: 0.0.0.255
    #             ttl:
    #               eq: 10
    #           name: '110'
    #         - aces:
    #           - destination:
    #               address: 192.0.3.0
    #               port_protocol:
    #                 eq: www
    #               wildcard_bits: 0.0.0.255
    #             grant: deny
    #             option:
    #               traceroute: true
    #             protocol: tcp
    #             protocol_options:
    #               tcp:
    #                 fin: true
    #             sequence: 10
    #             source:
    #               address: 192.0.2.0
    #               wildcard_bits: 0.0.0.255
    #             ttl:
    #               eq: 10
    #           name: test
    #         afi: ipv4
    #       - acls: []
    #         afi: ipv6


    ## Playbook with workflow example
    _tasks:
      - name: Gather ACLs config from device existing ACLs config
        cisco.ios.ios_acls:
          state: gathered
        register: result_gathered

      - name: Setting host facts for pop_ace filter plugin
        ansible.builtin.set_fact:
          acls_facts: "{{ result_gathered.gathered }}"
          filter_options:
            match_all: true
          match_criteria:
            afi: "ipv4"
            source: "192.0.2.0"
            destination: "192.0.3.0"

      - name: Invoke pop_ace filter plugin
        ansible.builtin.set_fact:
          clean_acls: "{{ acls_facts | ansible.netcommon.pop_ace(filter_options=filter_options, match_criteria=match_criteria) }}"

      - name: Override ACLs config with device existing ACLs config
        cisco.ios.ios_acls:
          state: overridden
          config: "{{ clean_acls['clean_acls']['acls'] | from_yaml }}"

    ## Output

    # PLAYBOOK: pop_ace_example.yml ***********************************************

    # PLAY [Filter plugin example pop_ace] ****************************************

    # TASK [Gather ACLs config with device existing ACLs config] *********************
    # ok: [xe_machine] => changed=false
    #   gathered:
    #   - acls:
    #     - aces:
    #       - destination:
    #           address: 192.0.3.0
    #           wildcard_bits: 0.0.0.255
    #         dscp: ef
    #         grant: deny
    #         protocol: icmp
    #         protocol_options:
    #           icmp:
    #             traceroute: true
    #         sequence: 10
    #         source:
    #           address: 192.0.2.0
    #           wildcard_bits: 0.0.0.255
    #         ttl:
    #           eq: 10
    #       - destination:
    #           host: 198.51.110.0
    #           port_protocol:
    #             eq: telnet
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 20
    #         source:
    #           host: 198.51.100.0
    #       acl_type: extended
    #       name: '110'
    #     - aces:
    #       - destination:
    #           address: 198.51.101.0
    #           port_protocol:
    #             eq: telnet
    #           wildcard_bits: 0.0.0.255
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 10
    #         source:
    #           address: 198.51.100.0
    #           wildcard_bits: 0.0.0.255
    #         tos:
    #           service_value: 12
    #       - destination:
    #           address: 192.0.4.0
    #           port_protocol:
    #             eq: www
    #           wildcard_bits: 0.0.0.255
    #         dscp: ef
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 20
    #         source:
    #           address: 192.0.3.0
    #           wildcard_bits: 0.0.0.255
    #         ttl:
    #           lt: 20
    #       acl_type: extended
    #       name: '123'
    #     - aces:
    #       - grant: deny
    #         sequence: 10
    #         source:
    #           host: 192.168.1.200
    #       - grant: deny
    #         sequence: 20
    #         source:
    #           address: 192.168.2.0
    #           wildcard_bits: 0.0.0.255
    #       acl_type: standard
    #       name: std_acl
    #     - aces:
    #       - destination:
    #           address: 192.0.3.0
    #           port_protocol:
    #             eq: www
    #           wildcard_bits: 0.0.0.255
    #         grant: deny
    #         option:
    #           traceroute: true
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             fin: true
    #         sequence: 10
    #         source:
    #           address: 192.0.2.0
    #           wildcard_bits: 0.0.0.255
    #         ttl:
    #           eq: 10
    #       acl_type: extended
    #       name: test
    #     afi: ipv4
    #   - acls:
    #     - aces:
    #       - destination:
    #           any: true
    #           port_protocol:
    #             eq: telnet
    #         dscp: af11
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 10
    #         source:
    #           any: true
    #           port_protocol:
    #             eq: www
    #       name: R1_TRAFFIC
    #     afi: ipv6
    #   invocation:
    #     module_args:
    #       config: null
    #       running_config: null
    #       state: gathered

    # TASK [Setting host facts for pop_ace filter plugin] *************************
    # ok: [xe_machine] => changed=false
    #   ansible_facts:
    #     acls_facts:
    #     - acls:
    #       - aces:
    #         - destination:
    #             address: 192.0.3.0
    #             wildcard_bits: 0.0.0.255
    #           dscp: ef
    #           grant: deny
    #           protocol: icmp
    #           protocol_options:
    #             icmp:
    #               traceroute: true
    #           sequence: 10
    #           source:
    #             address: 192.0.2.0
    #             wildcard_bits: 0.0.0.255
    #           ttl:
    #             eq: 10
    #         - destination:
    #             host: 198.51.110.0
    #             port_protocol:
    #               eq: telnet
    #           grant: deny
    #           protocol: tcp
    #           protocol_options:
    #             tcp:
    #               ack: true
    #           sequence: 20
    #           source:
    #             host: 198.51.100.0
    #         acl_type: extended
    #         name: '110'
    #       - aces:
    #         - destination:
    #             address: 198.51.101.0
    #             port_protocol:
    #               eq: telnet
    #             wildcard_bits: 0.0.0.255
    #           grant: deny
    #           protocol: tcp
    #           protocol_options:
    #             tcp:
    #               ack: true
    #           sequence: 10
    #           source:
    #             address: 198.51.100.0
    #             wildcard_bits: 0.0.0.255
    #           tos:
    #             service_value: 12
    #         - destination:
    #             address: 192.0.4.0
    #             port_protocol:
    #               eq: www
    #             wildcard_bits: 0.0.0.255
    #           dscp: ef
    #           grant: deny
    #           protocol: tcp
    #           protocol_options:
    #             tcp:
    #               ack: true
    #           sequence: 20
    #           source:
    #             address: 192.0.3.0
    #             wildcard_bits: 0.0.0.255
    #           ttl:
    #             lt: 20
    #         acl_type: extended
    #         name: '123'
    #       - aces:
    #         - grant: deny
    #           sequence: 10
    #           source:
    #             host: 192.168.1.200
    #         - grant: deny
    #           sequence: 20
    #           source:
    #             address: 192.168.2.0
    #             wildcard_bits: 0.0.0.255
    #         acl_type: standard
    #         name: std_acl
    #       - aces:
    #         - destination:
    #             address: 192.0.3.0
    #             port_protocol:
    #               eq: www
    #             wildcard_bits: 0.0.0.255
    #           grant: deny
    #           option:
    #             traceroute: true
    #           protocol: tcp
    #           protocol_options:
    #             tcp:
    #               fin: true
    #           sequence: 10
    #           source:
    #             address: 192.0.2.0
    #             wildcard_bits: 0.0.0.255
    #           ttl:
    #             eq: 10
    #         acl_type: extended
    #         name: test
    #       afi: ipv4
    #     - acls:
    #       - aces:
    #         - destination:
    #             any: true
    #             port_protocol:
    #               eq: telnet
    #           dscp: af11
    #           grant: deny
    #           protocol: tcp
    #           protocol_options:
    #             tcp:
    #               ack: true
    #           sequence: 10
    #           source:
    #             any: true
    #             port_protocol:
    #               eq: www
    #         name: R1_TRAFFIC
    #       afi: ipv6
    #     filter_options:
    #       match_all: true
    #     match_criteria:
    #       afi: ipv4
    #       destination: 192.0.3.0
    #       source: 192.0.2.0

    # TASK [Invoke pop_ace filter plugin] *****************************************
    # ok: [xe_machine] => changed=false
    #   ansible_facts:
    #     clean_acls:
    #       clean_acls:
    #         acls:
    #         - acls:
    #           - aces:
    #             - destination:
    #                 host: 198.51.110.0
    #                 port_protocol:
    #                   eq: telnet
    #               grant: deny
    #               protocol: tcp
    #               protocol_options:
    #                 tcp:
    #                   ack: true
    #               sequence: 20
    #               source:
    #                 host: 198.51.100.0
    #             name: '110'
    #           - aces:
    #             - destination:
    #                 address: 198.51.101.0
    #                 port_protocol:
    #                   eq: telnet
    #                 wildcard_bits: 0.0.0.255
    #               grant: deny
    #               protocol: tcp
    #               protocol_options:
    #                 tcp:
    #                   ack: true
    #               sequence: 10
    #               source:
    #                 address: 198.51.100.0
    #                 wildcard_bits: 0.0.0.255
    #               tos:
    #                 service_value: 12
    #             - destination:
    #                 address: 192.0.4.0
    #                 port_protocol:
    #                   eq: www
    #                 wildcard_bits: 0.0.0.255
    #               dscp: ef
    #               grant: deny
    #               protocol: tcp
    #               protocol_options:
    #                 tcp:
    #                   ack: true
    #               sequence: 20
    #               source:
    #                 address: 192.0.3.0
    #                 wildcard_bits: 0.0.0.255
    #               ttl:
    #                 lt: 20
    #             name: '123'
    #           - aces:
    #             - grant: deny
    #               sequence: 10
    #               source:
    #                 host: 192.168.1.200
    #             - grant: deny
    #               sequence: 20
    #               source:
    #                 address: 192.168.2.0
    #                 wildcard_bits: 0.0.0.255
    #             name: std_acl
    #           afi: ipv4
    #         - acls:
    #           - aces:
    #             - destination:
    #                 any: true
    #                 port_protocol:
    #                   eq: telnet
    #               dscp: af11
    #               grant: deny
    #               protocol: tcp
    #               protocol_options:
    #                 tcp:
    #                   ack: true
    #               sequence: 10
    #               source:
    #                 any: true
    #                 port_protocol:
    #                   eq: www
    #             name: R1_TRAFFIC
    #           afi: ipv6
    #       removed_aces:
    #         acls:
    #         - acls:
    #           - aces:
    #             - destination:
    #                 address: 192.0.3.0
    #                 wildcard_bits: 0.0.0.255
    #               dscp: ef
    #               grant: deny
    #               protocol: icmp
    #               protocol_options:
    #                 icmp:
    #                   traceroute: true
    #               sequence: 10
    #               source:
    #                 address: 192.0.2.0
    #                 wildcard_bits: 0.0.0.255
    #               ttl:
    #                 eq: 10
    #             name: '110'
    #           - aces:
    #             - destination:
    #                 address: 192.0.3.0
    #                 port_protocol:
    #                   eq: www
    #                 wildcard_bits: 0.0.0.255
    #               grant: deny
    #               option:
    #                 traceroute: true
    #               protocol: tcp
    #               protocol_options:
    #                 tcp:
    #                   fin: true
    #               sequence: 10
    #               source:
    #                 address: 192.0.2.0
    #                 wildcard_bits: 0.0.0.255
    #               ttl:
    #                 eq: 10
    #             name: test
    #           afi: ipv4
    #         - acls: []
    #           afi: ipv6

    # TASK [Override ACLs config with device existing ACLs config] *******************
    # changed: [xe_machine] => changed=true
    #   after:
    #   - acls:
    #     - aces:
    #       - destination:
    #           host: 198.51.110.0
    #           port_protocol:
    #             eq: telnet
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 20
    #         source:
    #           host: 198.51.100.0
    #       acl_type: extended
    #       name: '110'
    #     - aces:
    #       - destination:
    #           address: 198.51.101.0
    #           port_protocol:
    #             eq: telnet
    #           wildcard_bits: 0.0.0.255
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 10
    #         source:
    #           address: 198.51.100.0
    #           wildcard_bits: 0.0.0.255
    #         tos:
    #           service_value: 12
    #       - destination:
    #           address: 192.0.4.0
    #           port_protocol:
    #             eq: www
    #           wildcard_bits: 0.0.0.255
    #         dscp: ef
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 20
    #         source:
    #           address: 192.0.3.0
    #           wildcard_bits: 0.0.0.255
    #         ttl:
    #           lt: 20
    #       acl_type: extended
    #       name: '123'
    #     - aces:
    #       - grant: deny
    #         sequence: 10
    #         source:
    #           host: 192.168.1.200
    #       - grant: deny
    #         sequence: 20
    #         source:
    #           address: 192.168.2.0
    #           wildcard_bits: 0.0.0.255
    #       acl_type: standard
    #       name: std_acl
    #     afi: ipv4
    #   - acls:
    #     - aces:
    #       - destination:
    #           any: true
    #           port_protocol:
    #             eq: telnet
    #         dscp: af11
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 10
    #         source:
    #           any: true
    #           port_protocol:
    #             eq: www
    #       name: R1_TRAFFIC
    #     afi: ipv6
    #   before:
    #   - acls:
    #     - aces:
    #       - destination:
    #           address: 192.0.3.0
    #           wildcard_bits: 0.0.0.255
    #         dscp: ef
    #         grant: deny
    #         protocol: icmp
    #         protocol_options:
    #           icmp:
    #             traceroute: true
    #         sequence: 10
    #         source:
    #           address: 192.0.2.0
    #           wildcard_bits: 0.0.0.255
    #         ttl:
    #           eq: 10
    #       - destination:
    #           host: 198.51.110.0
    #           port_protocol:
    #             eq: telnet
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 20
    #         source:
    #           host: 198.51.100.0
    #       acl_type: extended
    #       name: '110'
    #     - aces:
    #       - destination:
    #           address: 198.51.101.0
    #           port_protocol:
    #             eq: telnet
    #           wildcard_bits: 0.0.0.255
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 10
    #         source:
    #           address: 198.51.100.0
    #           wildcard_bits: 0.0.0.255
    #         tos:
    #           service_value: 12
    #       - destination:
    #           address: 192.0.4.0
    #           port_protocol:
    #             eq: www
    #           wildcard_bits: 0.0.0.255
    #         dscp: ef
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 20
    #         source:
    #           address: 192.0.3.0
    #           wildcard_bits: 0.0.0.255
    #         ttl:
    #           lt: 20
    #       acl_type: extended
    #       name: '123'
    #     - aces:
    #       - grant: deny
    #         sequence: 10
    #         source:
    #           host: 192.168.1.200
    #       - grant: deny
    #         sequence: 20
    #         source:
    #           address: 192.168.2.0
    #           wildcard_bits: 0.0.0.255
    #       acl_type: standard
    #       name: std_acl
    #     - aces:
    #       - destination:
    #           address: 192.0.3.0
    #           port_protocol:
    #             eq: www
    #           wildcard_bits: 0.0.0.255
    #         grant: deny
    #         option:
    #           traceroute: true
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             fin: true
    #         sequence: 10
    #         source:
    #           address: 192.0.2.0
    #           wildcard_bits: 0.0.0.255
    #         ttl:
    #           eq: 10
    #       acl_type: extended
    #       name: test
    #     afi: ipv4
    #   - acls:
    #     - aces:
    #       - destination:
    #           any: true
    #           port_protocol:
    #             eq: telnet
    #         dscp: af11
    #         grant: deny
    #         protocol: tcp
    #         protocol_options:
    #           tcp:
    #             ack: true
    #         sequence: 10
    #         source:
    #           any: true
    #           port_protocol:
    #             eq: www
    #       name: R1_TRAFFIC
    #     afi: ipv6
    #   commands:
    #   - ip access-list extended 110
    #   - no 10 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 traceroute dscp ef ttl eq 10
    #   - no ip access-list extended test







Authors
~~~~~~~

- Sagar Paul (@KB-perByte)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
