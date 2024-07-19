
.. Created with antsibull-docs 2.9.0

ansible.netcommon.net_ping module -- Tests reachability using ping from a network device
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.net_ping``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Tests reachability using ping from network device to a remote destination.

This module has a corresponding action plugin.







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
      <div class="ansibleOptionAnchor" id="parameter-count"></div>
      <p style="display: inline;"><strong>count</strong></p>
      <a class="ansibleOptionLink" href="#parameter-count" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Number of packets to send.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">5</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-dest"></div>
      <p style="display: inline;"><strong>dest</strong></p>
      <a class="ansibleOptionLink" href="#parameter-dest" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>The IP Address or hostname (resolvable by switch) of the remote node.</p>
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
      <p>The source IP Address.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Determines if the expected result is success or fail.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;absent&#34;</code></p></li>
        <li><p><code style="color: blue;"><b>&#34;present&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-vrf"></div>
      <p style="display: inline;"><strong>vrf</strong></p>
      <a class="ansibleOptionLink" href="#parameter-vrf" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The VRF to use for forwarding.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;default&#34;</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- For targets running Python, use the \ `ansible.builtin.shell <shell_module.rst>`__\  module along with ping command instead.
- This module is supported on \ :literal:`ansible\_network\_os`\  network platforms. See the :ref:\`Network Platform Options \<platform\_options\>\` for details.


Examples
--------

.. code-block:: yaml


    - name: Test reachability to 10.10.10.10 using default vrf
      ansible.netcommon.net_ping:
        dest: 10.10.10.10

    - name: Test reachability to 10.20.20.20 using prod vrf
      ansible.netcommon.net_ping:
        dest: 10.20.20.20
        vrf: prod

    - name: Test unreachability to 10.30.30.30 using default vrf
      ansible.netcommon.net_ping:
        dest: 10.30.30.30
        state: absent

    - name: Test reachability to 10.40.40.40 using prod vrf and setting count and source
      ansible.netcommon.net_ping:
        dest: 10.40.40.40
        source: loopback0
        vrf: prod
        count: 20

    - Note:
        - For targets running Python, use the M(ansible.builtin.shell) module along with ping command instead.
        - Example:
            name: ping
            shell: ping -c 1 <remote-ip>





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
      <div class="ansibleOptionAnchor" id="return-commands"></div>
      <p style="display: inline;"><strong>commands</strong></p>
      <a class="ansibleOptionLink" href="#return-commands" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>Show the command sent.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;ping vrf prod 10.40.40.40 count 20 source loopback0&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-packet_loss"></div>
      <p style="display: inline;"><strong>packet_loss</strong></p>
      <a class="ansibleOptionLink" href="#return-packet_loss" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Percentage of packets lost.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;0%&#34;</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-packets_rx"></div>
      <p style="display: inline;"><strong>packets_rx</strong></p>
      <a class="ansibleOptionLink" href="#return-packets_rx" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>
    </td>
    <td valign="top">
      <p>Packets successfully received.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>20</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-packets_tx"></div>
      <p style="display: inline;"><strong>packets_tx</strong></p>
      <a class="ansibleOptionLink" href="#return-packets_tx" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>
    </td>
    <td valign="top">
      <p>Packets successfully transmitted.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>20</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-rtt"></div>
      <p style="display: inline;"><strong>rtt</strong></p>
      <a class="ansibleOptionLink" href="#return-rtt" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Show RTT stats.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>{&#34;avg&#34;: 2, &#34;max&#34;: 8, &#34;min&#34;: 1}</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Jacob McGill (@jmcgill298)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
