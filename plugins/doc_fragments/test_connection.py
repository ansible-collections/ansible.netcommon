# (c) 2022 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Standard files documentation fragment
    DOCUMENTATION = """
options:
  test_parameters:
    default: {}
    type: dict
    description:
    - This option allows to pass additional parameters for testing purposes.
    suboptions:
      fixture_directory:
        description:
        - The directory where the test fixture files will be/are located.
        required: true
        type: string
      mode:
        choices:
        - compare
        - playback
        - record
        description:
        - The mode in which the test fixture files will be used.
        - I(compare) Compare the fixture to live output from the device.
        - I(playback) Use the fixtures rather than directly interacting with the device.
        - I(record) Record the output from the device to the fixture files.
        required: true
        type: string
      exempted:
        default: []
        description: A list of regular expressions that will be used to exclude the output from the compare.
        type: list
        elements: string
    env:
    - name: ANSIBLE_NETWORK_TEST_PARAMETERS
    vars:
    - name: ansible_network_test_parameters
"""
