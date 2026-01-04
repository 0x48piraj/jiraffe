#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UnauthUserPicker(ReconModule):
    name = "Unauthenticated User Picker"
    severity = Severity.INFO
    description = "User picker popup accessible without authentication"

    def run(self):
        r = self.client.get(
            f"{self.target}/secure/popups/UserPickerBrowser.jspa"
        )

        if r.status_code == 200 and "user-picker" in r.text.lower():
            print(Style.GREEN("[+] Unauthenticated user picker accessible"))
            return True

        return False
