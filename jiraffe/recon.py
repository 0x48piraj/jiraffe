#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, socket
import re
import bs4
from urllib.parse import urlparse
from packaging import version


def uparse(target):
	url = urlparse(target)
	if url.path:
		if url.path == "/":
			print("[-] Target URL doesn't seems to be correct.\n\t\tValid Target URL Paths: http(s)://target.com/.../(login.action;/view.action;/viewpage.action;/releaseview.action;/aboutconfluencepage.action;/secure/Dashboard.jspa)")
			return url.scheme + "://" + url.netloc + url.path
		else:
			return url.scheme + "://" + url.netloc + url.path
		return 
	else:
		print("[-] Target URL doesn't seems to be correct.\n\t\tValid Target URL Paths: http(s)://target.com/.../(login.action;/view.action;/viewpage.action;/releaseview.action;/aboutconfluencepage.action;/secure/Dashboard.jspa)")
		return url.scheme + "://" + url.netloc

def request(target):
	UA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
	headers = {'X-Atlassian-Token':'no-check', 'User-Agent':UA}
	try:
		r = requests.get(target, headers=headers)
	except Exception as e:
		print("[-] Problem with the HTTP request.", e, sep="\n")
		if r.status_code != 200:
			print("[-] Something went wrong! (STATUS {})".format(r.status_code))
			if r.status_code == 302:
				print("[*] HTTP request got redirected. Set this instead: " + r.headers['Location'])
		exit(1) # https://stackoverflow.com/a/2434619

	return r, r.text

def isjira(target):
	target = uparse(target)
	res, response = request(target)
	if "ajs-" in str(response):
		if "footer-build-information" in str(response) or "atlassian-footer" in str(response):
			return True
	else:
		return False

def isaws(target):
	target = urlparse(target)
	data = socket.gethostbyaddr(target.netloc)
	if "amazonaws" in str(data):
		return True
	else:
		return False

def getversion(target): # ENUM #1: Jira version appears to be ____
	target = uparse(target)
	f_build = '0.0.0' # default
	vers = []
	final_version = ""
	res, response = request(target)
	soup = bs4.BeautifulSoup(response, "html.parser")
	try:
		vers = vers + [item["data-version"] for item in soup.find_all() if "data-version" in item.attrs] # ajs tags
		f_build = soup.find("span", {"id": "footer-build-information"}).get_text() # login page footer
		vers.append(f_build.split("#")[0]) # grabbing & appending the version
	except:
		pass
	try: # finalize the version
		for n, i in enumerate(vers):
			vers[n] = version.parse(i)
		final_version = str(max(vers))
	except Exception as e:
		final_version = False # if fails

	return final_version