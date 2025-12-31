#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

DEFAULT_USER_AGENT = "Jiraffe/2.x" # Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1
DEFAULT_HEADERS = {
    "X-Atlassian-Token": "no-check",
}

class HttpClient:
    def __init__(
        self,
        verify_ssl: bool = True,
        timeout: int = 10,
        user_agent: str = DEFAULT_USER_AGENT,
    ):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.session.headers["User-Agent"] = user_agent
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
