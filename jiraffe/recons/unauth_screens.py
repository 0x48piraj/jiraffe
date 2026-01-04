#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UnauthScreens(ReconModule):
    name = "Unauthenticated Screens API"
    severity = Severity.LOW
    description = "Screens API accessible without authentication"

    def run(self):
        r = self.client.get(
            f"{self.target}/rest/api/latest/screens"
        )

        if r.status_code == 200 and '"screens"' in r.text:
            print(Style.GREEN("[+] Unauthenticated screens accessible"))
            return True

        return False
