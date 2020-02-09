#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import bs4
from urllib.parse import urlparse
from packaging import version

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
	url = urlparse(target)
	target = url.scheme + "://" + url.netloc
	response = request(target)
	if "jira" in str(response):
		return True
	else:
		return False

def getversion(target): # Jira version appears to be ____
	url = urlparse(target)
	target = url.scheme + "://" + url.netloc
	# ENUM TYPE 1
	f_build = '0.0.0' # default
	vers = []
	final_version = ""
	target = target + url.path if "/login.jsp" in url.path else target + '/login.jsp'
	response = request(target)
	soup = bs4.BeautifulSoup(response, "html.parser")
	
	print("Checking for version ...")
	try:
		vers = vers + [item["data-version"] for item in soup.find_all() if "data-version" in item.attrs] # ajs tags
		f_build = soup.find("span", {"id": "footer-build-information"}).get_text() # Login page footer
		vers.append(f_build.split("#")[0]) # grabbing & appending the version
	except:
		pass
	print(vers)
	# finalize the version
	try:
		for n, i in enumerate(vers):
			vers[n] = version.parse(i)
		print(vers)
		final_version = str(max(vers))
	except Exception as e:
		final_version = '0.0.0' # if fails

	return final_version