#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class DevModeEnabled(ReconModule):
    name = "Jira Dev Mode Enabled"
    severity = Severity.LOW
    description = "Jira running with dev mode enabled"

    def run(self):
        r = self.client.get(self.target)

        if '<meta name="ajs-dev-mode" content="true">' in r.text:
            print(Style.GREEN("[+] Jira dev mode enabled"))
            return True

        return False
