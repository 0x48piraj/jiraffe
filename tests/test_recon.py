import unittest
from jiraffe.recon import *

class TestUtils(unittest.TestCase):
    def test_uparse(self):
        """
        Test that uparse() can parse and return base url
        """
        data = 'https://jira.atlassian.com/secure/Dashboard.jspa'
        result = uparse(data)
        self.assertEqual(result, 'https://jira.atlassian.com/secure/Dashboard.jspa')

    def test_request(self):
        """
        Test that request() works as intended
        """
        data = 'https://jira.atlassian.com/secure/Dashboard.jspa'
        result = request(data)
        self.assertEqual(len(result), 2)

    def test_getversion(self):
        """
        Test that getversion() returns a str containing jira version
        """
        data = 'https://jira.atlassian.com/secure/Dashboard.jspa'
        result = getversion(data)
        self.assertIsInstance(result, str)


class TestBools(unittest.TestCase):
    def test_isjira(self):
        """
        Test that isjira() can detect jira instance
        """
        data = 'https://jira.atlassian.com/secure/Dashboard.jspa'
        result = isjira(data)
        self.assertTrue(result)

    def test_isaws(self):
        """
        Test that isaws() can detect aws instance
        """
        data = 'https://jira.atlassian.com/secure/Dashboard.jspa'
        result = isaws(data)
        self.assertTrue(result)