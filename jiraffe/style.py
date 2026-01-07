#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Style:
    ENABLED = True

    @staticmethod
    def _wrap(code: str, text: str, reset: bool = True) -> str:
        """Wrap text with ANSI code, if reset=False, don't append reset code."""
        if not Style.ENABLED:
            return str(text)
        return f"\033[{code}m{text}" + ("\033[0m" if reset else "")

    BLACK   = staticmethod(lambda x, reset=True: Style._wrap("30", x, reset))
    RED     = staticmethod(lambda x, reset=True: Style._wrap("31", x, reset))
    GREEN   = staticmethod(lambda x, reset=True: Style._wrap("32", x, reset))
    YELLOW  = staticmethod(lambda x, reset=True: Style._wrap("33", x, reset))
    BLUE    = staticmethod(lambda x, reset=True: Style._wrap("34", x, reset))
    MAGENTA = staticmethod(lambda x, reset=True: Style._wrap("35", x, reset))
    CYAN    = staticmethod(lambda x, reset=True: Style._wrap("36", x, reset))
    WHITE   = staticmethod(lambda x, reset=True: Style._wrap("37", x, reset))
    UNDERLINE = staticmethod(lambda x, reset=True: Style._wrap("4", x, reset))
    RESET   = staticmethod(lambda x: "\033[0m" + str(x))
    ORANGE  = staticmethod(lambda x, reset=True: Style._wrap("38;5;208", x, reset))
