#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UnauthDashboards(ReconModule):
    name = "Unauthenticated Dashboards"
    severity = Severity.INFO
    description = "Dashboard enumeration without authentication"

    def run(self):
        r = self.client.get(
            f"{self.target}/rest/api/latest/dashboard"
        )

        if r.status_code == 200 and '"dashboards"' in r.text:
            print(Style.GREEN("[+] Unauthenticated dashboards accessible"))
            return True

        return False
