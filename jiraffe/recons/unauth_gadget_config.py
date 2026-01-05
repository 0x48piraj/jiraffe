#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jiraffe.recons.base import ReconModule
from jiraffe.enums import Severity
from jiraffe.style import Style


class UnauthGadgetConfig(ReconModule):
    name = "Unauthenticated Gadget Configuration"
    severity = Severity.LOW
    description = "Gadget config directory accessible"

    def run(self):
        r = self.client.get(
            f"{self.target}/rest/config/1.0/directory"
        )

        if r.status_code == 200 and "jaxbDirectoryContents" in r.text:
            print(Style.GREEN("[+] Unauthenticated gadget config accessible"))
            return True

        return False
