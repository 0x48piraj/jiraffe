#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UnauthGroupPicker(ReconModule):
    name = "Unauthenticated Group Picker"
    severity = Severity.INFO
    description = "REST groupuserpicker endpoint accessible without authentication"

    def run(self):
        r = self.client.get(
            f"{self.target}/rest/api/latest/groupuserpicker"
        )

        if r.status_code == 200 and "authentication required" not in r.text.lower() and r.headers.get("Content-Type","").startswith("application/json"):
            print(Style.GREEN("[+] Unauthenticated group picker accessible"))
            return True

        return False
