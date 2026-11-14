"""Conservative website status checks for trusted, local-only use."""

import ipaddress
import socket
from urllib.parse import urlsplit

import requests


def is_website_online(url: str) -> bool:
    """Check public HTTP(S) hosts only; never follow redirects.

    This function is disabled by default in the hosted Streamlit application.
    DNS checks alone are not sufficient for a general-purpose public SSRF defence.
    """
    try:
        parsed = urlsplit(url.strip())
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return False
        if parsed.username or parsed.password:
            return False
        hostname = parsed.hostname.rstrip(".").lower()
        if hostname in ("localhost",) or hostname.endswith((".local", ".internal")):
            return False
        addresses = socket.getaddrinfo(hostname, parsed.port or (443 if parsed.scheme == "https" else 80))
        if not addresses or any(
            not ipaddress.ip_address(info[4][0]).is_global for info in addresses
        ):
            return False
        response = requests.get(
            url, timeout=5, allow_redirects=False, stream=True,
            headers={"User-Agent": "Useful-Code-Snippets/1.0"},
        )
        try:
            return 200 <= response.status_code < 400
        finally:
            response.close()
    except (OSError, ValueError, requests.exceptions.RequestException):
        return False
