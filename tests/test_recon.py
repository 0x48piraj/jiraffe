#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from jiraffe.common import (
    uparse,
    getversion,
    isjira,
    isaws
)
from jiraffe.http import HttpClient


class TestReconUtilities(unittest.TestCase):
    """
    Recon-level tests using real network targets.

    These tests validate heuristic behavior against
    known public services and must tolerate failure.
    """

    @classmethod
    def setUpClass(cls):
        cls.client = HttpClient()

    def test_uparse_preserves_valid_url(self):
        """
        uparse() should not modify a valid Jira URL
        during reconnaissance.
        """
        data = "https://jira.atlassian.com/secure/Dashboard.jspa"
        self.assertEqual(uparse(data), data)

    def test_getversion_returns_string_or_none(self):
        """
        getversion() should return either a semantic
        version string or None during recon.
        """
        data = "https://jira.atlassian.com/secure/Dashboard.jspa"
        result = getversion(data, self.client)

        self.assertTrue(result is None or isinstance(result, str))

    def test_isjira_detects_jira_instance(self):
        """
        isjira() should positively identify
        a known Jira instance.
        """
        data = "https://jira.atlassian.com/secure/Dashboard.jspa"
        self.assertTrue(isjira(data, self.client))

    def test_isaws_detects_known_aws_hostname(self):
        """
        isaws() should detect known AWS EC2 hostnames
        during reconnaissance.
        """
        data = "https://ec2-3-91-23-45.compute-1.amazonaws.com"
        self.assertTrue(isaws(data, self.client))

    def test_isaws_always_returns_boolean(self):
        """
        isaws() should never raise and must
        always return a boolean value.
        """
        result = isaws("https://example.com", self.client)
        self.assertIsInstance(result, bool)
