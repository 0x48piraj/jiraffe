#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from packaging.version import Version


# Inclusive ranges
CVE_COMPATIBILITY = {
    "CVE-2017-9506": (Version("6.0.0"), Version("7.13.0")),
    "CVE-2019-8449": (Version("7.0.0"), Version("8.4.0")),
    "CVE-2019-8451": (Version("7.0.0"), Version("8.4.0")),
    "CVE-2019-11581": (Version("8.0.0"), Version("8.5.0"))
}

def is_compatible(cve: str, jira_version: str) -> bool:
    if cve not in CVE_COMPATIBILITY:
        return True

    min_v, max_v = CVE_COMPATIBILITY[cve]
    v = Version(jira_version)
    return min_v <= v <= max_v
