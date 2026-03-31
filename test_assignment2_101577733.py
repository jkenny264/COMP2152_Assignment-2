"""
Unit Tests for Assignment 2 — Port Scanner
"""

import unittest

from assignment2_101577733 import PortScanner, common_ports


class TestPortScanner(unittest.TestCase):

    def test_scanner_initialization(self):
        """Test that PortScanner initializes with correct target and empty results list."""
        ps1 = PortScanner("127.0.0.1")
        self.assertEqual(ps1.target, "127.0.0.1")
        

    def test_get_open_ports_filters_correctly(self):
        """Test that get_open_ports returns only Open ports."""
        ps1 = PortScanner("127.0.0.1")
        ps1.scan_results.append((22, "Open", "SSH"))
        ps1.scan_results.append((23, "Closed", "Telnet"))
        ps1.scan_results.append((80, "Open", "HTTP"))
        self.assertEqual(len(ps1.get_open_ports()), 2)

    def test_common_ports_dict(self):
        """Test that common_ports dictionary has correct entries."""
        sample_ports = (common_ports[80], common_ports[22])
        self.assertEqual(sample_ports, ("HTTP", "SSH"))


    def test_invalid_target(self):
        """Test that setter rejects empty string target."""
        ps1 = PortScanner("127.0.0.1")
        ps1.target = ""
        self.assertEqual(ps1.target, "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
