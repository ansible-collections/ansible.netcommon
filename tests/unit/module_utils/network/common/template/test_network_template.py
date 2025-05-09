import unittest
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import Template

class TestNetworkTemplate(unittest.TestCase):
    def setUp(self):
        self.template = Template()

    def test_asdot_string_preserved(self):
        """Ensure AS-DOT strings like '65000.1000' are not coerced to float."""
        result = self.template("{{ as_number }}", {"as_number": "65000.1000"})
        self.assertEqual(result, "65000.1000")

    def test_normal_string_eval(self):
        """Ensure normal integer strings still evaluate correctly."""
        result = self.template("{{ as_number }}", {"as_number": "65000"})
        self.assertEqual(result, 65000)

    def test_list_literal_eval(self):
        """Ensure literal_eval still works for lists."""
        result = self.template("{{ value }}", {"value": "[1, 2, 3]"})
        self.assertEqual(result, [1, 2, 3])

if __name__ == '__main__':
    unittest.main()