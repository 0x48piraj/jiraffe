#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class QueryComponentFields(ReconModule):
    name = "Query Component Field Disclosure"
    severity = Severity.LOW
    description = "JQL field metadata exposed"

    def run(self):
        r = self.client.get(
            f"{self.target}/secure/QueryComponent!Jql.jspa?jql="
        )

        if r.status_code == 200 and "searchers" in r.text:
            print(Style.GREEN("[+] Query component fields disclosed"))
            return True

        return False
