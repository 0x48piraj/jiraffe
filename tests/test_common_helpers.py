#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import MagicMock, patch
from jiraffe.common import (
    normalize_version,
    color_severity,
    uparse,
    host_info,
    isaws,
    get_deployment_type,
    getversion
)
from jiraffe.compat import is_compatible
from jiraffe.enums import Severity
from jiraffe.style import Style


class TestCommonHelpers(unittest.TestCase):
    """
    Tests for helpers in jiraffe.common.

    These tests focus on pure helpers and heuristic logic.
    Network, DNS, and HTTP calls are mocked to ensure predictable behaviour.
    """

    def test_normalize_version_extracts_semver_from_parentheses(self):
        """
        normalize_version() should extract a semantic version
        from strings containing parentheses or prefixes.
        """
        self.assertEqual(normalize_version("(v8.13.4)"), "8.13.4")

    def test_normalize_version_extracts_major_minor(self):
        """
        normalize_version() should extract major.minor versions
        when patch versions are not present.
        """
        self.assertEqual(normalize_version("JIRA 7.6"), "7.6")

    def test_normalize_version_empty_string(self):
        """
        normalize_version() should return None when given
        an empty string.
        """
        self.assertIsNone(normalize_version(""))

    def test_normalize_version_none(self):
        """
        normalize_version() should return None when input is None.
        """
        self.assertIsNone(normalize_version(None))

    def test_normalize_version_no_match(self):
        """
        normalize_version() should return None when
        no semantic version is present.
        """
        self.assertIsNone(normalize_version("no version here"))

    def test_color_severity_known_levels(self):
        """
        color_severity() should return the correct Style
        wrapper for known severity levels.
        """
        self.assertIs(color_severity("HIGH"), Style.ORANGE)
        self.assertIs(color_severity("MEDIUM"), Style.YELLOW)
        self.assertIs(color_severity("LOW"), Style.GREEN)
        self.assertIs(color_severity("INFO"), Style.CYAN)
        self.assertIs(color_severity("CRITICAL"), Style.MAGENTA)

    def test_color_severity_unknown_level(self):
        """
        color_severity() should default to Style.RESET
        for unknown severity values.
        """
        self.assertIs(color_severity("UNKNOWN"), Style.RESET)

    def test_style_wrap_disabled(self):
        """
        Style._wrap() should return raw text
        when styling is disabled.
        """
        Style.ENABLED = False
        self.assertEqual(Style.RED("test"), "test")
        Style.ENABLED = True

    def test_uparse_preserves_valid_url(self):
        """
        uparse() should return a normalized URL
        without modifying a valid Jira URL.
        """
        url = "https://jira.example.com/secure/Dashboard.jspa"
        self.assertEqual(uparse(url), url)

    def test_uparse_missing_scheme(self):
        """
        uparse() should return the original string
        if the URL is missing a scheme or netloc.
        """
        self.assertEqual(uparse("jira.example.com"), "jira.example.com")

    @patch("socket.gethostbyname", side_effect=Exception())
    def test_host_info_resolution_failure(self, _):
        """
        host_info() should return (None, None)
        if DNS resolution fails.
        """
        ip, rdns = host_info("https://nonexistent.invalid")
        self.assertIsNone(ip)
        self.assertIsNone(rdns)

    def test_isaws_detects_aws_hostname(self):
        """
        isaws() should return True when the hostname
        matches known AWS patterns.
        """
        client = MagicMock()
        self.assertTrue(
            isaws("https://ec2-1-2-3-4.compute.amazonaws.com", client)
        )

    @patch("jiraffe.common.host_info", return_value=("1.2.3.4", "ec2.amazonaws.com"))
    def test_isaws_detects_aws_reverse_dns(self, _):
        """
        isaws() should return True when reverse DNS
        indicates an Amazon AWS host.
        """
        client = MagicMock()
        self.assertTrue(isaws("https://example.com", client))

    def test_isaws_http_server_header(self):
        """
        isaws() should return True when the HTTP Server
        header indicates an AWS ELB/ALB.
        """
        client = MagicMock()
        response = MagicMock()
        response.headers = {"Server": "awselb/2.0"}
        client.get.return_value = response

        self.assertTrue(isaws("https://example.com", client))

    def test_isaws_non_aws_target(self):
        """
        isaws() should return False for non-AWS targets.
        """
        client = MagicMock()
        client.get.side_effect = Exception()
        self.assertFalse(isaws("https://example.com", client))

    def test_get_deployment_type_success(self):
        """
        get_deployment_type() should return the deploymentType
        field when the Jira serverInfo endpoint responds successfully.
        """
        client = MagicMock()
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"deploymentType": "Server"}
        client.get.return_value = response

        result = get_deployment_type("https://jira.example.com", client)
        self.assertEqual(result, "Server")

    def test_get_deployment_type_failure(self):
        """
        get_deployment_type() should return None
        if the request fails or an exception is raised.
        """
        client = MagicMock()
        client.get.side_effect = Exception()

        self.assertIsNone(
            get_deployment_type("https://jira.example.com", client)
        )

    def test_getversion_from_meta_tag(self):
        """
        getversion() should extract the Jira version
        from HTML meta tags when present.
        """
        client = MagicMock()
        response = MagicMock()
        response.text = """
        <html>
            <head>
                <meta name="ajs-version-number" content="8.20.1">
            </head>
        </html>
        """
        client.get.return_value = response

        result = getversion("https://jira.example.com", client)
        self.assertEqual(result, "8.20.1")

    def test_getversion_returns_none_when_no_version_found(self):
        """
        getversion() should return None when no
        version indicators are found.
        """
        client = MagicMock()
        response = MagicMock()
        response.text = "<html><body>No Jira here</body></html>"
        client.get.return_value = response

        self.assertIsNone(getversion("https://jira.example.com", client))

    def test_severity_enum_values(self):
        """
        Severity enum should expose all expected values.
        """
        self.assertEqual(Severity.LOW.value, "LOW")
        self.assertEqual(Severity.CRITICAL.value, "CRITICAL")

    def test_is_compatible_unknown_cve(self):
        """
        is_compatible() should return True
        for unknown CVE identifiers.
        """
        self.assertTrue(is_compatible("CVE-2099-9999", "9.0.0"))


    def test_is_compatible_in_range(self):
        """
        is_compatible() should return True
        when Jira version is within the vulnerable range.
        """
        self.assertTrue(is_compatible("CVE-2019-8449", "8.2.0"))


    def test_is_compatible_out_of_range(self):
        """
        is_compatible() should return False
        when Jira version is outside the vulnerable range.
        """
        self.assertFalse(is_compatible("CVE-2019-8449", "8.10.0"))
