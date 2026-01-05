#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UnauthAdminMenu(ReconModule):
    name = "Unauthenticated Admin Menu"
    severity = Severity.INFO
    description = "Admin menu REST endpoint accessible"

    def run(self):
        r = self.client.get(
            f"{self.target}/rest/menu/latest/admin"
        )

        if r.status_code == 200 and '"label"' in r.text and '"admin"' in r.text.lower():
            print(Style.GREEN("[+] Unauthenticated admin menu accessible"))
            return True

        return False
