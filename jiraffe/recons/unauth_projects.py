#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UnauthProjects(ReconModule):
    name = "Unauthenticated Projects API"
    severity = Severity.LOW
    description = "Project enumeration without authentication"

    def run(self):
        r = self.client.get(
            f"{self.target}/rest/api/latest/project?maxResults=1"
        )

        if r.status_code == 200 and '"key"' in r.text:
            print(Style.GREEN("[+] Unauthenticated project enumeration possible"))
            return True

        return False
