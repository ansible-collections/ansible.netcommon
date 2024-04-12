
.. Created with antsibull-docs 2.9.0

ansible.netcommon.restconf_get module -- Fetch configuration/state data from RESTCONF enabled devices.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.restconf_get``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- RESTCONF is a standard mechanisms to allow web applications to access the configuration data and state data developed and standardized by the IETF. It is documented in RFC 8040.
- This module allows the user to fetch configuration and state data from RESTCONF enabled devices.








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
      <div class="ansibleOptionAnchor" id="parameter-content"></div>
      <p style="display: inline;"><strong>content</strong></p>
      <a class="ansibleOptionLink" href="#parameter-content" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The <code class='docutils literal notranslate'>content</code> is a query parameter that controls how descendant nodes of the requested data nodes in <code class='docutils literal notranslate'>path</code> will be processed in the reply. If value is <em>config</em> return only configuration descendant data nodes of value in <code class='docutils literal notranslate'>path</code>. If value is <em>nonconfig</em> return only non-configuration descendant data nodes of value in <code class='docutils literal notranslate'>path</code>. If value is <em>all</em> return all descendant data nodes of value in <code class='docutils literal notranslate'>path</code></p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;config&#34;</code></p></li>
        <li><p><code>&#34;nonconfig&#34;</code></p></li>
        <li><p><code>&#34;all&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-output"></div>
      <p style="display: inline;"><strong>output</strong></p>
      <a class="ansibleOptionLink" href="#parameter-output" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The output of response received.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;json&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;xml&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-path"></div>
      <p style="display: inline;"><strong>path</strong></p>
      <a class="ansibleOptionLink" href="#parameter-path" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>URI being used to execute API calls.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- This module requires the RESTCONF system service be enabled on the remote device being managed.
- This module is supported with \ :emphasis:`ansible\_connection`\  value of \ :emphasis:`ansible.netcommon.httpapi`\  and \ :emphasis:`ansible\_network\_os`\  value of \ :emphasis:`ansible.netcommon.restconf`\ .
- This module is tested against Cisco IOSXE 16.12.02 version.


Examples
--------

.. code-block:: yaml


    - name: get l3vpn services
      ansible.netcommon.restconf_get:
        path: /config/ietf-l3vpn-svc:l3vpn-svc/vpn-services





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
      <div class="ansibleOptionAnchor" id="return-response"></div>
      <p style="display: inline;"><strong>response</strong></p>
      <a class="ansibleOptionLink" href="#return-response" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>A dictionary representing a JSON-formatted response</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when the device response is valid JSON</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>{&#34;vpn-services&#34;: {&#34;vpn-service&#34;: [{&#34;customer-name&#34;: &#34;red&#34;, &#34;vpn-id&#34;: &#34;blue_vpn1&#34;, &#34;vpn-service-topology&#34;: &#34;ietf-l3vpn-svc:any-to-any&#34;}]}}</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
