#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UnauthPopularFilters(ReconModule):
    name = "Unauthenticated Popular Filters"
    severity = Severity.INFO
    description = "Popular filters page accessible without authentication"

    def run(self):
        r = self.client.get(
            f"{self.target}/secure/ManageFilters.jspa?filter=popular&filterView=popular"
        )

        if r.status_code == 200 and "popular filters" in r.text.lower():
            print(Style.GREEN("[+] Unauthenticated popular filters accessible"))
            return True

        return False
