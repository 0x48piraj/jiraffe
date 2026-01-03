#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from jiraffe.enums import Severity
from jiraffe.style import Style


class ReconModule(ABC):
    name: str
    severity: Severity
    description: str

    def __init__(self, client, target, verbose=False):
        self.client = client
        self.target = target
        self.verbose = verbose

    def banner(self):
        print(
            Style.CYAN(
                f"[*] {self.name} [{self.severity.value}]"
            )
        )

    @abstractmethod
    def run(self) -> bool:
        """Return True if condition is present"""
        pass
