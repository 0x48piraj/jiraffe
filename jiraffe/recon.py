#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket
import requests
import bs4
from urllib.parse import urlparse
from packaging import version


def uparse(target):
	url = urlparse(target)

	if not url.scheme or not url.netloc:
		print(
			"[-] Target URL doesn't seem to be correct.\n\t\t"
			"Valid Target URL Paths: http(s)://target.com/.../"
			"(login.action;/view.action;/viewpage.action;/releaseview.action;"
			"/aboutconfluencepage.action;/secure/Dashboard.jspa)"
		)
		return target

	return url.scheme + "://" + url.netloc + (url.path or "")

def request(target):
	UA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
	headers = {
		"X-Atlassian-Token": "no-check",
		"User-Agent": UA,
	}

	try:
		r = requests.get(target, headers=headers)
	except Exception as e:
		print("[-] Problem with the HTTP request.", e, sep="\n")
		if r.status_code != 200:
			print("[-] Something went wrong! (STATUS {})".format(r.status_code))
			if r.status_code == 302:
				print("[*] HTTP request got redirected. Set this instead: " + r.headers['Location'])
		sys.exit(1)

	return r, r.text

def isjira(target):
	target = uparse(target)
	_, response = request(target)

	return (
		"ajs-" in response
		and (
			"footer-build-information" in response
			or "atlassian-footer" in response
		)
	)


def isaws(target):
	try:
		host = urlparse(target).netloc
		data = socket.gethostbyaddr(host)
		return "amazonaws" in str(data)
	except Exception:
		return False

def getversion(target):
	target = uparse(target)
	_, response = request(target)

	versions = []
	soup = bs4.BeautifulSoup(response, "html.parser")

	# ajs attributes
	for tag in soup.find_all(attrs={"data-version": True}):
		versions.append(tag["data-version"]) # ajs tags

	# footer build info from login page
	footer = soup.find("span", {"id": "footer-build-information"})
	if footer:
		versions.append(footer.get_text().split("#")[0])

	if not versions:
		return False

	try:
		parsed = [version.parse(v) for v in versions]
		return str(max(parsed))
	except Exception:
		return False
