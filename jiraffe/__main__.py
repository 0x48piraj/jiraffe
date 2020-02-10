#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, argparse, textwrap
from .recon import request, isjira, getversion
from .exploits import *

def main():
	if sys.platform.lower() == "win32":
	    os.system('color')
	  # Group of Different functions for different styles
	    class style():
	        BLACK = lambda x: '\033[30m' + str(x)
	        RED = lambda x: '\033[31m' + str(x)
	        GREEN = lambda x: '\033[32m' + str(x)
	        YELLOW = lambda x: '\033[33m' + str(x)
	        BLUE = lambda x: '\033[34m' + str(x)
	        MAGENTA = lambda x: '\033[35m' + str(x)
	        CYAN = lambda x: '\033[36m' + str(x)
	        WHITE = lambda x: '\033[37m' + str(x)
	        UNDERLINE = lambda x: '\033[4m' + str(x)
	        RESET = lambda x: '\033[0m' + str(x)
	else:
	    class style():
	        BLACK = ""
	        RED = ""
	        GREEN = ""
	        YELLOW = ""
	        BLUE = ""
	        MAGENTA = ""
	        CYAN = ""
	        WHITE = ""
	        UNDERLINE = ""
	        RESET = ""

	banner = textwrap.dedent(r'''
                                                                           /)/)
                                                                          ( ..\    
      ___  __      _______        __       _______   _______   _______    /'-._)
     |"  ||" \    /"      \      /""\     /"     "| /"     "| /"     "|  /#/  
     ||  |||  |  |:        |    /    \   (: ______)(: ______)(: ______) /#/  @0x48piraj 
     |:  ||:  |  |_____/   )   /' /\  \   \/    |   \/    |   \/    |   
  ___|  / |.  |   //      /   //  __'  \  // ___)   // ___)   // ___)_  
 /  :|_/ )/\  |\ |:  __   \  /   /  \\  \(:  (     (:  (     (:      "| 
(_______/(__\_|_)|__|  \___)(___/    \___)\__/      \__/      \_______)
''')

	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=style.GREEN(banner) + style.RESET(''), usage=style.GREEN("jiraffe ") + style.YELLOW("[-h] [-t {}]").format(style.UNDERLINE("https://example-jira-instance.com") + style.RESET('') + style.YELLOW('')) + style.RESET(''))
	optional = parser._action_groups.pop() # popped opt args
	optional = parser.add_argument_group('Options')
	optional.add_argument("-t", "--target", dest="target", metavar=style.CYAN("https://example-jira-instance.com") + style.RESET(''), default=False, help= style.GREEN("Target Jira Instance URL") + style.RESET(''))
	optional.add_argument("-v", "--verbose", dest="verbose", action='store_true', help= style.GREEN("Verbose output") + style.RESET(''))
	optional.add_argument("-a", "--auto", dest="automatic", action='store_true', help= style.GREEN("Automatic mode") + style.RESET(''))

	verbose = parser.parse_args().verbose
	target = parser.parse_args().target
	auto = parser.parse_args().automatic
	print(style.GREEN(banner) + style.RESET(''))
	try:
	    if target == False:
	        print(style.YELLOW("[*] Target not provided, invoking interactive mode ..."))
	        print("[*] Enter the target Jira instance URL (https://example-jira-instance.com)" + style.RESET(''))
	        target = input(style.GREEN("    ----> ") + style.RESET('')).strip()
	except KeyboardInterrupt:
	    print(style.RED('Interrupted.') + style.RESET(''))
	    sys.exit(0) # http://tldp.org/LDP/abs/html/exitcodes.html#EXITCODESREF

	if target == "":
		print(style.RED("[-] Not provided any target. Quitting.") + style.RESET(''))
		sys.exit(1)

	if auto == True:
		print(style.YELLOW("[*] Detecting the target ...") + style.RESET(''))
		if isjira(target): # detect if jira
			print(style.GREEN("[+] Jira instance detected") + style.RESET(''), style.YELLOW("[*] Enumerating the version ...") + style.RESET(''), sep="\n")
			vs = getversion(target) # grab version
			if vs:
				print(style.GREEN("[+] Jira version detected: {}").format(style.UNDERLINE(vs) + style.RESET('')) + style.RESET(''))
			else:
				print(style.GREEN("[-] Jira version detection failed.") + style.RESET(''))
			print(style.YELLOW("[*] Launching all attacks ...") + style.RESET(''))
			# should launch based on version
			cve2019_8451(target)
			cve2017_9506(target)
			cve2019_8449(target)
	else:
			print(style.YELLOW("[*] Mode not provided, invoking interactive mode ..."))
			print("[*] Choose the exploit ..." + style.RESET(''))
			EXMSG = (
				'\n\n'
				'1. CVE-2017-9506 [HIGH]\n'
				'2. CVE-2019-8449 [LOW]\n'
				'3. CVE-2019-8451 [HIGH]'
			)
			print(style.GREEN(EXMSG) + style.RESET(''))
			exploit = input(style.GREEN("    ----> ") + style.RESET('')).strip()
			if exploit == '1': # func. mapping
				cve2017_9506(target)
			elif exploit == '2':
				cve2019_8449(target)
			elif exploit == '3':
				cve2019_8451(target)
			else:
				print(style.RED("[-] Invalid option selected. Quitting.") + style.RESET(''))

if __name__ == "__main__":
    main()