import unittest

from api.tools import openvpn


class TestOpenVPN(unittest.TestCase):

    def setUp(self):
        pass

    def test_ip_db(self):
        ccd = "eniac\t10.0.0.2\nskull\t10.0.0.6"
        expected = [
            {
                'certificate': 'eniac',
                'ip': '10.0.0.2'
            },
            {
                'certificate': 'skull',
                'ip': '10.0.0.6'
            },
        ]
        self.assertEqual("", openvpn.get_ip_db())
