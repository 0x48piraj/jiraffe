#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from jiraffe.recon import uparse, getversion, isjira, isaws
from jiraffe.http import HttpClient


class TestReconUtilities(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = HttpClient()

    def test_uparse_preserves_valid_url(self):
        """
        uparse() should return a normalized URL
        without altering a valid Jira path.
        """
        data = "https://jira.atlassian.com/secure/Dashboard.jspa"
        result = uparse(data)
        self.assertEqual(result, data)

    def test_getversion_returns_string_or_none(self):
        """
        getversion() should return a semantic version string
        or None if version detection fails.
        """
        data = "https://jira.atlassian.com"
        result = getversion(data, self.client)
        self.assertTrue(result is None or isinstance(result, str))

    def test_isjira_detects_jira_instance(self):
        """
        isjira() should correctly identify a Jira instance.
        """
        data = "https://jira.atlassian.com"
        result = isjira(data, self.client)
        self.assertTrue(result)

    def test_isaws_known_aws_hostname(self):
        """
        isaws() should detect known AWS EC2 hostnames.
        """
        data = "https://ec2-3-91-23-45.compute-1.amazonaws.com"
        result = isaws(data)
        self.assertTrue(result)

    def test_isaws_returns_boolean(self):
        """
        isaws() should always return a boolean value.
        """
        result = isaws("https://example.com")
        self.assertIsInstance(result, bool)
