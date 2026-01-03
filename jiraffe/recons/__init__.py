#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pkgutil
import importlib
import inspect
from jiraffe.recons.base import ReconModule


def load_recon_modules():
    modules = []

    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name == "base":
            continue

        module = importlib.import_module(
            f"{__name__}.{module_info.name}"
        )

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, ReconModule) and obj is not ReconModule:
                modules.append(obj)

    return modules
