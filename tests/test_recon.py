#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import MagicMock, patch
from jiraffe.common import (
    uparse,
    getversion,
    isjira,
    isaws
)


class TestReconUtilities(unittest.TestCase):
    """
    Recon-level helper tests using deterministic local responses.
    """

    def test_uparse_preserves_valid_url(self):
        """
        uparse() should not modify a valid Jira URL
        during reconnaissance.
        """
        data = "https://jira.example.com/secure/Dashboard.jspa"
        self.assertEqual(uparse(data), data)

    def test_getversion_returns_string_or_none(self):
        """
        getversion() should return either a semantic
        version string or None during recon.
        """
        data = "https://jira.example.com/secure/Dashboard.jspa"
        client = MagicMock()
        response = MagicMock()
        response.text = "<html><body>No version</body></html>"
        client.get.return_value = response

        result = getversion(data, client)

        self.assertIsNone(result)

    def test_isjira_detects_jira_instance(self):
        """
        isjira() should positively identify
        a known Jira instance.
        """
        data = "https://jira.example.com/secure/Dashboard.jspa"
        client = MagicMock()
        response = MagicMock()
        response.text = '<meta name="ajs-version-number" content="8.0.0"> Jira'
        client.get.return_value = response
        self.assertTrue(isjira(data, client))

    @patch("jiraffe.common.host_info", return_value=(None, None))
    def test_isaws_detects_known_aws_hostname(self, _):
        """
        isaws() should detect known AWS EC2 hostnames
        during reconnaissance.
        """
        data = "https://ec2-3-91-23-45.compute-1.amazonaws.com"
        self.assertTrue(isaws(data, MagicMock()))

    @patch("jiraffe.common.host_info", return_value=(None, None))
    def test_isaws_always_returns_boolean(self, _):
        """
        isaws() should never raise and must
        always return a boolean value.
        """
        client = MagicMock()
        client.get.side_effect = Exception("unexpected HTTP request")
        result = isaws("https://example.com", client)
        self.assertIsInstance(result, bool)
