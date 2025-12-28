#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import textwrap

# version guard
if sys.version_info[0] < 3:
    sys.stderr.write("[-] Python 2 is not supported. Please use Python 3.\n")
    sys.exit(1)

from urllib.parse import urlparse
from .recon import isjira, getversion
from .exploits import (
	cve2017_9506,
	cve2019_8449,
	cve2019_8451,
	cve2019_11581,
)


class Style:
	ENABLED = True

	@staticmethod
	def _wrap(code, text):
		if not Style.ENABLED:
			return str(text)
		return "\033[{}m{}\033[0m".format(code, text)

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

BANNER = textwrap.dedent(r'''
                                                                           /)/)
                                                                          ( ..\    
      ___  __      _______        __       _______   _______   _______    /'-._)
     |   ||  \    /       \      /  \     /       | /       | /       |  /#/  
     ||  |||  |  |:        |    /    \   (: ______)(: ______)(: ______) /#/  @0x48piraj 
     |:  ||:  |  |_____/   )   /' /\  \   \/    |   \/    |   \/    |   
  ___|  / |.  |   //      /   //  __'  \  // ___)   // ___)   // ___)_  
 /  :|_/ )/\  |\ |:  __   \  /   /  \\  \(:  (     (:  (     (:       | 
(_______/(__\_|_)|__|  \___)(___/    \___)\__/      \__/      \_______)
''')

AUTO_EXPLOIT_ORDER = [
    "3",  # CVE-2019-8451
    "1",  # CVE-2017-9506
    "2",  # CVE-2019-8449
    "4",  # CVE-2019-11581
]

INTERACTIVE_EXPLOITS = {
	"1": ("CVE-2017-9506", cve2017_9506),
	"2": ("CVE-2019-8449", cve2019_8449),
	"3": ("CVE-2019-8451", cve2019_8451),
	"4": ("CVE-2019-11581", cve2019_11581),
}

def validate_target(url):
	parsed = urlparse(url)
	return parsed.scheme in ("http", "https") and parsed.netloc

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

	parser.add_argument("-t", "--target", help="Target Jira URL")
	parser.add_argument("-a", "--auto", action="store_true", help="Automatic mode")
	parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

	args = parser.parse_args()

	print(Style.GREEN(BANNER) + Style.RESET(""))

	target = args.target
	try:
		if not target:
			print(Style.YELLOW("[*] Target not provided, invoking interactive mode..."))
			print("[*] Enter the target Jira instance URL (https://example-jira-instance.com)")
			target = input(Style.GREEN("	----> ")).strip()
	except KeyboardInterrupt:
		print(Style.RED("Interrupted."))
		sys.exit(0) # http://tldp.org/LDP/abs/html/exitcodes.html#EXITCODESREF

	if not target or not validate_target(target):
		print(Style.RED("[-] Not provided any valid target. Quitting."))
		sys.exit(1)

	if args.auto:
		print(Style.YELLOW("[*] Detecting the target..."))
		if isjira(target):
			print(
				Style.GREEN("[+] Jira instance detected") + "\n"
				+ Style.YELLOW("[*] Enumerating the version...")
			)

			version = getversion(target)
			if version:
				print(
					Style.GREEN("[+] Jira version detected: ")
					+ Style.UNDERLINE(version)
				)
			else:
				print(Style.RED("[-] Jira version detection failed."))

			print(Style.YELLOW("[*] Launching all exploits..."))
			for key in AUTO_EXPLOIT_ORDER:
				_, exploit = INTERACTIVE_EXPLOITS[key]
				exploit(target)
	else:
		print(Style.YELLOW("[*] Mode not provided, invoking interactive mode..."))
		print("[*] Choose the exploit...")

		print(Style.GREEN(
			"\n\n"
			"1. CVE-2017-9506 [HIGH]\n"
			"2. CVE-2019-8449 [LOW]\n"
			"3. CVE-2019-8451 [HIGH]\n"
			"4. CVE-2019-11581 [CRITICAL]"
		))

		choice = input(Style.GREEN("	----> ")).strip()
		if choice not in INTERACTIVE_EXPLOITS:
			print(Style.RED("[-] Invalid option selected. Quitting."))
			return

		_, exploit = INTERACTIVE_EXPLOITS[choice]
		if choice == "4":
			print("[*] Input the payload (spawning harmless 'calc.exe', or maybe bash -c '...')")
			cmd = input("Enter the payload (default: calc.exe): ").strip()
			if cmd:
				cve2019_11581(target, cmd)
			else:
				cve2019_11581(target)
		else:
			exploit(target)

if __name__ == "__main__":
	main()
