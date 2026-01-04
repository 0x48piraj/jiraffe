#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UserRegistrationEnabled(ReconModule):
    name = "User Registration Enabled"
    severity = Severity.MEDIUM
    description = "Unauthenticated user signup enabled"

    def run(self):
        r = self.client.get(
            f"{self.target}/secure/Signup!default.jspa"
        )

        if r.status_code == 200 and "private" not in r.text.lower():
            print(Style.GREEN("[+] User registration enabled"))
            return True

        return False
