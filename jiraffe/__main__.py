#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, argparse, textwrap
from .recon import request, isjira, getversion

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

	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=style.GREEN(banner) + style.RESET(''), usage=style.GREEN("jiraffe ") + style.YELLOW("[-h] [-t '{}']").format(style.UNDERLINE("https://example-jira-instance.com") + style.RESET('') + style.YELLOW('')) + style.RESET(''))
	optional = parser._action_groups.pop() # popped opt args
	optional = parser.add_argument_group('Options')
	optional.add_argument("-t", "--target", dest="target", metavar=style.CYAN("https://example-jira-instance.com") + style.RESET(''), default=False, help= style.GREEN("Target Jira Instance URL") + style.RESET(''))
	optional.add_argument("-v", "--verbose", dest="verbose", action='store_true', help= style.GREEN("Verbose output") + style.RESET(''))

	verbose = parser.parse_args().verbose
	target = parser.parse_args().target
	print(style.GREEN(banner) + style.RESET(''))
	try:
	    if target == False:
	        print(style.YELLOW("[*] Target not provided, invoking interactive mode ..."))
	        print("[*] Enter the target Jira instance URL (https://example-jira-instance.com)" + style.RESET(''))
	        target = input(style.GREEN("    ----> ") + style.RESET('')).strip()
	except KeyboardInterrupt:
	    print('Interrupted.')
	    sys.exit(0) # http://tldp.org/LDP/abs/html/exitcodes.html#EXITCODESREF


if __name__ == "__main__":
    main()