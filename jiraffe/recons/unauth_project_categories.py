#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UnauthProjectCategories(ReconModule):
    name = "Unauthenticated Project Categories"
    severity = Severity.LOW
    description = "Project categories accessible without authentication"

    def run(self):
        r = self.client.get(
            f"{self.target}/rest/api/latest/projectCategory"
        )

        if r.status_code == 200 and '"name"' in r.text:
            print(Style.GREEN("[+] Unauthenticated project categories accessible"))
            return True

        return False
