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
from jiraffe.exploits import load_exploits
from jiraffe.recons import load_recon_modules
from jiraffe.common import (
    isjira,
    getversion,
    uparse,
    get_deployment_type,
    host_info,
    color_severity
)
from jiraffe.compat import is_compatible
from jiraffe.enums import Severity


BANNER = Style.GREEN(textwrap.dedent(rf'''
                                                                           /)/)
                                                                          ( ..\   
      ___  __      _______        __       _______   _______   _______    /'-._)
     |   ||  \    /       \      /  \     /       | /       | /       |  /#/ v{__version__}
     ||  |||  |  |:        |    /    \   (: ______)(: ______)(: ______) /#/  @03C0
     |:  ||:  |  |_____/   )   /  /\  \   \/    |   \/    |   \/    |   
  ___|  / |.  |   //      /   // '__'  \  // ___)   // ___)   // ___)_   
 /  :|_/ )/\  |\ |:  __   \  /   /  \\  \(:  (     (:  (     (:       |
(_______/(__\_|_)|__|  \___)(___/    \___)\__/      \__/      \_______)
'''))
BANNER = BANNER.replace(f"v{__version__}", Style.CYAN(f"v{__version__}") + Style.GREEN("", reset=False))
BANNER = BANNER.replace("@03C0", Style.ORANGE("@03C0") + Style.GREEN("", reset=False))
ALL_EXPLOITS = load_exploits()
ALL_RECONS = load_recon_modules()

def validate_target(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

def list_exploits():
    print(Style.YELLOW("[*] Available exploits:\n"))
    for i, exp in enumerate(ALL_EXPLOITS, 1):
        severity_color = color_severity(exp.severity.value)
        print(
            f"{Style.YELLOW(f'{i:>2}.')} "
            f"[{severity_color(exp.severity.value):<8}] "
            f"{Style.RESET(exp.cve)}: "
            f"{Style.CYAN(exp.description)}"
        )
    sys.exit(0)

def build_module_list(exploits, recons):
    modules = []

    for r in recons:
        modules.append(("recon", r))

    for e in exploits:
        modules.append(("exploit", e))

    return modules

def interactive_module_menu(modules):
    print(Style.YELLOW("[*] Available modules\n"))

    for i, (mtype, cls) in enumerate(modules, 1):
        label = Style.CYAN("RECON") if mtype == "recon" else Style.ORANGE("EXPLOIT")

        name = cls.name if mtype == "recon" else cls.cve
        severity = cls.severity.value
        severity_color = color_severity(severity)

        print(
            f"{Style.YELLOW(f'{i:>2}.')} "
            f"[{label:<7}] "
            f"[{severity_color(severity):<8}] "
            f"{Style.RESET(name)}"
        )

    try:
        choice = input(Style.YELLOW("\n----> ")).strip()
        idx = int(choice) - 1
        return modules[idx]
    except KeyboardInterrupt:
        print(Style.RED("Interrupted."))
        sys.exit(0)
    except (ValueError, IndexError):
        print(Style.RED("[-] Invalid option selected."))
        return None

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=BANNER,
        usage=(
            Style.GREEN("jiraffe ")
            + Style.YELLOW("[-h] [-t {}]").format(
                Style.UNDERLINE("https://jira.company.com")
            )
        ),
    )

    parser.add_argument("-t", "--target", help=Style.YELLOW("Target Jira instance URL"), metavar=Style.CYAN("https://jira.company.com"), default=False)
    parser.add_argument("-a", "--auto", action="store_true", help=Style.YELLOW("Automatic mode"))

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
        "--user-agent",
        help="Custom User-Agent header",
    )

    parser.add_argument(
        "--severity",
        choices=[color_severity(s.value)(s.value) for s in Severity],
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

    print(BANNER)

    if args.list_exploits:
        list_exploits()

    # Interactive target input
    target = args.target
    try:
        if not target:
            print(Style.YELLOW("[*] Target not provided, invoking interactive mode..."))
            print("[?] Enter the target Jira instance URL (e.g. https://jira.company.com)")
            target = input(Style.YELLOW("    ----> ")).strip()
    except KeyboardInterrupt:
        print(Style.RED("Interrupted."))
        sys.exit(0)

    if not target or not validate_target(target):
        print(Style.RED("[-] Invalid target URL."))
        sys.exit(1)

    client = HttpClient(
        verify_ssl=not args.insecure,
        user_agent=args.user_agent or "Jiraffe/2.x",
    )

    target = uparse(target).rstrip("/")

    ip, rdns = host_info(target)
    if ip:
        print(Style.GREEN("[+] Target IP: ") + Style.CYAN(ip))
    if rdns:
        print(Style.GREEN("[+] Reverse DNS: ") + Style.CYAN(rdns))

    if not isjira(target, client):
        print(Style.RED("[-] Target does not appear to be Jira."))
        sys.exit(1)

    jira_version = getversion(target, client)
    if jira_version:
        print(Style.GREEN("[+] Jira version detected: ") + Style.MAGENTA(jira_version))

    deployment = get_deployment_type(target, client)
    if deployment:
        print(Style.GREEN("[+] Deployment type: ") + Style.MAGENTA(deployment))

    selected = ALL_EXPLOITS

    # Severity filter
    if args.severity:
        selected = [
            e for e in selected if e.severity.value == args.severity
        ]

    results = []

    # AUTO MODE
    if args.auto:
        modules = build_module_list(ALL_EXPLOITS, ALL_RECONS)

    # INTERACTIVE MODE
    else:
        modules = build_module_list(ALL_EXPLOITS, ALL_RECONS)

        selected_module = interactive_module_menu(modules)
        if not selected_module:
            sys.exit(1)

        modules = [selected_module]

    # Module execution
    for mtype, module_cls in modules:
        if mtype == "recon":
            recon = module_cls(
                client,
                target,
                verbose=args.verbose
            )

            recon.banner()
            found = recon.run()

            results.append({
                "type": "recon",
                "name": recon.name,
                "severity": recon.severity.value,
                "found": bool(found),
            })

        else: # exploit
            if jira_version and not is_compatible(module_cls.cve, jira_version):
                print(
                    f"[!] {Style.RESET(module_cls.cve)} "
                    f"{Style.CYAN('may not be compatible with Jira')} "
                    f"{Style.YELLOW(jira_version)}"
                )

            kwargs = {
                "verbose": args.verbose,
                "check_only": args.check_only,
            }

            if args.ssrf:
                kwargs["ssrf_target"] = args.ssrf

            if module_cls.cve == "CVE-2019-11581" and args.cmd:
                kwargs["command"] = args.cmd

            try:
                exploit = module_cls(client, target, **kwargs)
            except ValueError as e:
                print(Style.RED(f"[-] {e}"))
                continue

            ok = exploit.run()

            results.append({
                "type": "exploit",
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
