#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import json
import textwrap

# version guard
if sys.version_info[0] < 3:
    sys.stderr.write("[-] Python 2 is not supported. Please use Python 3.\n")
    sys.exit(1)

from urllib.parse import urlparse

from jiraffe import __version__
from jiraffe.style import Style
from jiraffe.http import HttpClient
from jiraffe.exploits import ALL_EXPLOITS
from jiraffe.recon import isjira, getversion, uparse
from jiraffe.compat import is_compatible
from jiraffe.enums import Severity


BANNER = textwrap.dedent(rf'''
                                                                           /)/)
                                                                          ( ..\    
      ___  __      _______        __       _______   _______   _______    /'-._)
     |   ||  \    /       \      /  \     /       | /       | /       |  /#/ v{__version__}
     ||  |||  |  |:        |    /    \   (: ______)(: ______)(: ______) /#/  @03C0
     |:  ||:  |  |_____/   )   /' /\  \   \/    |   \/    |   \/    |   
  ___|  / |.  |   //      /   //  __'  \  // ___)   // ___)   // ___)_  
 /  :|_/ )/\  |\ |:  __   \  /   /  \\  \(:  (     (:  (     (:       | 
(_______/(__\_|_)|__|  \___)(___/    \___)\__/      \__/      \_______)
''')

def validate_target(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

def list_exploits():
    print("Available exploits:\n")
    for exp in ALL_EXPLOITS:
        print(
            f"- {exp.cve:<18} "
            f"[{exp.severity.value:<8}] "
            f"{exp.description}"
        )
    sys.exit(0)

def interactive_exploit_menu(exploits):
    print(Style.YELLOW("[*] Choose the exploit...\n"))

    for i, exp in enumerate(exploits, 1):
        print(
            f"{i}. {exp.cve} "
            f"[{exp.severity.value}]"
        )

    try:
        choice = input("\n----> ").strip()
        idx = int(choice) - 1
        return exploits[idx]
    except KeyboardInterrupt:
        print(Style.RED("Interrupted."))
        sys.exit(0)
    except (ValueError, IndexError):
        print(Style.RED("[-] Invalid option selected."))
        return None

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=Style.GREEN(BANNER),
        usage=(
            Style.GREEN("jiraffe ")
            + Style.YELLOW("[-h] [-t {}]").format(
                Style.UNDERLINE("https://example-jira-instance.com")
            )
        ),
    )

    parser.add_argument("-t", "--target", help=Style.GREEN("Target Jira Instance URL"), metavar=Style.CYAN("https://example-jira-instance.com"), default=False)
    parser.add_argument("-a", "--auto", action="store_true", help=Style.MAGENTA("Automatic mode"))

    parser.add_argument(
        "--check-only", "--dry-run",
        dest="check_only",
        action="store_true",
        help="Only check for vulnerabilities, do not run exploits",
    )

    parser.add_argument("--list-exploits", action="store_true")
    parser.add_argument("--cmd", help="Command for CVE-2019-11581")
    parser.add_argument("--ssrf", help="SSRF target URL")

    parser.add_argument(
        "--severity",
        choices=[s.value for s in Severity],
        help="Run only exploits of this severity",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format (for automation / scripting)",
    )

    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification (allow self-signed HTTPS)",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output (debug information)",
    )

    args = parser.parse_args()

    print(Style.GREEN(BANNER) + Style.RESET(""))

    if args.list_exploits:
        list_exploits()

    # Interactive target input
    target = uparse(args.target)
    try:
        if not target:
            print(Style.YELLOW("[*] Target not provided, invoking interactive mode..."))
            print("[*] Enter the target Jira instance URL (https://example-jira-instance.com)")
            target = input(Style.GREEN("    ----> ")).strip()
    except KeyboardInterrupt:
        print(Style.RED("Interrupted."))
        sys.exit(0)

    if not target or not validate_target(target):
        print(Style.RED("[-] Invalid target URL."))
        sys.exit(1)

    client = HttpClient(verify_ssl=not args.insecure)

    if not isjira(target, client):
        print(Style.RED("[-] Target does not appear to be Jira."))
        sys.exit(1)

    jira_version = getversion(target, client)
    if jira_version:
        print(Style.GREEN("[+] Jira version detected: ") + Style.MAGENTA(jira_version))

    selected = ALL_EXPLOITS

    # Severity filter
    if args.severity:
        selected = [
            e for e in selected if e.severity.value == args.severity
        ]

    results = []

    # AUTO MODE
    if args.auto:
        exploit_classes = selected

    # INTERACTIVE MODE
    else:
        exploit_cls = interactive_exploit_menu(selected)
        if not exploit_cls:
            sys.exit(1)
        exploit_classes = [exploit_cls]

    # Exploit execution
    for exploit_cls in exploit_classes:
        if jira_version and not is_compatible(exploit_cls.cve, jira_version):
            print(
                Style.YELLOW(
                    f"[!] {exploit_cls.cve} may not be compatible with Jira {jira_version}"
                )
            )

        kwargs = {
            "verbose": args.verbose,
            "check_only": args.check_only,
        }

        if args.ssrf:
            kwargs["ssrf_target"] = args.ssrf

        if exploit_cls.cve == "CVE-2019-11581" and args.cmd:
            kwargs["command"] = args.cmd

        exploit = exploit_cls(client, target, **kwargs)
        ok = exploit.run()

        results.append({
            "cve": exploit.cve,
            "severity": exploit.severity.value,
            "vulnerable": bool(ok),
        })

    if args.json:
        print(json.dumps({
            "target": target,
            "results": results
        }, indent=2))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Style.RED("Interrupted."))
        sys.exit(0) # http://tldp.org/LDP/abs/html/exitcodes.html#EXITCODESREF
