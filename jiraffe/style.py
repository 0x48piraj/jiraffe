#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Style:
    ENABLED = True

    @staticmethod
    def _wrap(code: str, text: str) -> str:
        if not Style.ENABLED:
            return str(text)
        return f"\033[{code}m{text}\033[0m"

    BLACK = staticmethod(lambda x: Style._wrap("30", x))
    RED = staticmethod(lambda x: Style._wrap("31", x))
    GREEN = staticmethod(lambda x: Style._wrap("32", x))
    YELLOW = staticmethod(lambda x: Style._wrap("33", x))
    BLUE = staticmethod(lambda x: Style._wrap("34", x))
    MAGENTA = staticmethod(lambda x: Style._wrap("35", x))
    CYAN = staticmethod(lambda x: Style._wrap("36", x))
    WHITE = staticmethod(lambda x: Style._wrap("37", x))
    UNDERLINE = staticmethod(lambda x: Style._wrap("4", x))
    RESET = staticmethod(lambda x: "\033[0m" + str(x))
