#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class ServiceDeskSignup(ReconModule):
    name = "Service Desk Signup Enabled"
    severity = Severity.MEDIUM
    description = "Service desk customer signup enabled"

    def run(self):
        r = self.client.get(
            f"{self.target}/servicedesk/customer/user/signup"
        )

        if r.status_code == 200 and "service management" in r.text.lower():
            print(Style.GREEN("[+] Service desk signup enabled"))
            return True

        return False
