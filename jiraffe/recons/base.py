#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from jiraffe.enums import Severity
from jiraffe.style import Style
from jiraffe.common import color_severity


class ReconModule(ABC):
    name: str
    severity: Severity
    description: str

    def __init__(self, client, target, verbose=False):
        self.client = client
        self.target = target
        self.verbose = verbose

    def banner(self):
        severity_color = color_severity(self.severity.value)
        print(
            f"{Style.YELLOW(f'[*] Running:')} "
            f"{Style.RESET(self.name)} "
            f"[{severity_color(self.severity.value):<8}]"
        )

    @abstractmethod
    def run(self) -> bool:
        """Return True if condition is present"""
        pass
