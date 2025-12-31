#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


DEFAULT_HEADERS = {
    "X-Atlassian-Token": "no-check",
    "User-Agent": "Jiraffe/2.x",
}

class HttpClient:
    def __init__(self, verify_ssl=True, timeout=10):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.verify_ssl = verify_ssl
        self.timeout = timeout

    def get(self, url, **kwargs):
        return self.session.get(
            url,
            verify=self.verify_ssl,
            timeout=self.timeout,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self.session.post(
            url,
            verify=self.verify_ssl,
            timeout=self.timeout,
            **kwargs
        )
