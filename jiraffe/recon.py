#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import bs4

"""
One can access Confluence's landing page and retrieve version information from three places: [Unauthenticated]
- Login page footer.
- Response Head AJS Tags.
- Response Body What's New Link.
- Response Body Confluence Help Link.
"""

def request(target):
	UA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
	headers = {'X-Atlassian-token':'no-check', 'User-Agent':UA}
	try:
		r = requests.get(target, headers=headers)
	except Exception as e:
		print("Problem with the HTTP request.", e, sep="\n")
		exit(1)

	if (r.status_code != 200):
		print("Something went wrong! (STATUS {})".format(r.status_code))
		if (r.status_code == 302):
			print("HTTP request got redirected. Set this instead: " + r.headers['Location'])
		exit(1)

	return(r.text)

def isjira(target): # reckless check but ok
	response = request(target)
	if "jira" in str(response):
		return True
	else:
		return False

def getversion(target): # Jira version appears to be ____
	target = target if "/login.jsp" in target else target + '/login.jsp'
	response = request(target)
	soup = bs4.BeautifulSoup(response, "html.parser")
	print("Checking for version ...")
	try:
		return soup.find("span", {"id": "footer-build-information"}).get_text() # Login page footer
	except:
		return False