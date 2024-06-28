
.. Created with antsibull-docs 2.9.0

ansible.netcommon.cli_command module -- Run a cli command on cli-based network devices
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.cli_command``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Sends a command to a network device and returns the result read from the device.

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
      <div class="ansibleOptionAnchor" id="parameter-answer"></div>
      <p style="display: inline;"><strong>answer</strong></p>
      <a class="ansibleOptionLink" href="#parameter-answer" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The answer to reply with if <em>prompt</em> is matched. The value can be a single answer or a list of answer for multiple prompts. In case the command execution results in multiple prompts the sequence of the prompt and excepted answer should be in same order.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-check_all"></div>
      <p style="display: inline;"><strong>check_all</strong></p>
      <a class="ansibleOptionLink" href="#parameter-check_all" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>By default if any one of the prompts mentioned in <code class='docutils literal notranslate'>prompt</code> option is matched it won&#x27;t check for other prompts. This boolean flag, that when set to <em>True</em> will check for all the prompts mentioned in <code class='docutils literal notranslate'>prompt</code> option in the given order. If the option is set to <em>True</em> all the prompts should be received from remote host if not it will result in timeout.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-command"></div>
      <p style="display: inline;"><strong>command</strong></p>
      <a class="ansibleOptionLink" href="#parameter-command" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>The command to send to the remote network device.  The resulting output from the command is returned, unless <em>sendonly</em> is set.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-newline"></div>
      <p style="display: inline;"><strong>newline</strong></p>
      <a class="ansibleOptionLink" href="#parameter-newline" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>The boolean value, that when set to false will send <em>answer</em> to the device without a trailing newline.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-prompt"></div>
      <p style="display: inline;"><strong>prompt</strong></p>
      <a class="ansibleOptionLink" href="#parameter-prompt" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>A single regex pattern or a sequence of patterns to evaluate the expected prompt from <em>command</em>.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-sendonly"></div>
      <p style="display: inline;"><strong>sendonly</strong></p>
      <a class="ansibleOptionLink" href="#parameter-sendonly" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>The boolean value, that when set to true will send <em>command</em> to the device but not wait for a result.</p>
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

- This module is supported on \ :literal:`ansible\_network\_os`\  network platforms. See the :ref:\`Network Platform Options \<platform\_options\>\` for details.


Examples
--------

.. code-block:: yaml


    - name: run show version on remote devices
      ansible.netcommon.cli_command:
        command: show version

    - name: run command with json formatted output
      ansible.netcommon.cli_command:
        command: show version | json

    - name: run command expecting user confirmation
      ansible.netcommon.cli_command:
        command: commit replace
        prompt: This commit will replace or remove the entire running configuration
        answer: "yes"

    - name: run command expecting user confirmation
      ansible.netcommon.cli_command:
        command: show interface summary
        prompt: Press any key to continue
        answer: y
        newline: false

    - name: run config mode command and handle prompt/answer
      ansible.netcommon.cli_command:
        command: "{{ item }}"
        prompt:
          - Exit with uncommitted changes
        answer: y
      loop:
        - configure
        - set system syslog file test any any
        - exit

    - name: multiple prompt, multiple answer (mandatory check for all prompts)
      ansible.netcommon.cli_command:
        command: copy sftp sftp://user@host//user/test.img
        check_all: true
        prompt:
          - Confirm download operation
          - Password
          - Do you want to change that to the standby image
        answer:
          - y
          - <password>
          - y





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
      <div class="ansibleOptionAnchor" id="return-json"></div>
      <p style="display: inline;"><strong>json</strong></p>
      <a class="ansibleOptionLink" href="#return-json" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>A dictionary representing a JSON-formatted response</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when the device response is valid JSON</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;{\n  \&#34;architecture\&#34;: \&#34;i386\&#34;,\n  \&#34;bootupTimestamp\&#34;: 1532649700.56,\n  \&#34;modelName\&#34;: \&#34;vEOS\&#34;,\n  \&#34;version\&#34;: \&#34;4.15.9M\&#34;\n  [...]\n}\n&#34;</code></p>
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
      <p>The response from the command</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when sendonly is false</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;Version:      VyOS 1.1.7[...]&#34;</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Nathaniel Case (@Qalthos)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
