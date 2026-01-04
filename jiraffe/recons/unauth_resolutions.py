#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UnauthResolutions(ReconModule):
    name = "Unauthenticated Resolutions API"
    severity = Severity.INFO
    description = "Resolution list accessible without authentication"

    def run(self):
        r = self.client.get(f"{self.target}/rest/api/latest/resolution")

        if r.status_code == 200 and '"name"' in r.text:
            print(Style.GREEN("[+] Unauthenticated resolutions accessible"))
            return True

        return False
