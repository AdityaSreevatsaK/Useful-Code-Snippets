"""Check that a Hugging Face Space reaches a healthy runtime after deployment.

Uses public Hub metadata, never a deployment token.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def read_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "Utility-Shelf-Deployment-Check/1.0"})
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def http_healthy(url: str) -> bool:
    try:
        with urlopen(Request(url, headers={"User-Agent": "Utility-Shelf-Health-Check/1.0"}), timeout=20) as response:
            return response.status == 200
    except (HTTPError, URLError, TimeoutError):
        return False


def check_space(repo: str, expected_sha: str, attempts: int = 24, interval: int = 15) -> bool:
    url = f"https://huggingface.co/api/spaces/{repo}"
    failures = {"BUILD_ERROR", "RUNTIME_ERROR", "ERROR", "CONFIG_ERROR"}
    allowed = {"RUNNING", "SLEEPING"}
    for attempt in range(1, attempts + 1):
        try:
            data = read_json(url)
            stage = str((data.get("runtime") or {}).get("stage") or "UNKNOWN").upper()
            current_sha = data.get("sha")
            print(f"Check {attempt}/{attempts}: stage={stage}; sha={current_sha}", flush=True)
            if current_sha and expected_sha and current_sha != expected_sha:
                print("The Space has not yet received the expected revision.", flush=True)
            elif stage in failures:
                print("Space build/runtime reports failure.", file=sys.stderr, flush=True)
                return False
            elif stage in allowed:
                if stage == "SLEEPING":
                    print("Space deployed and sleeping; runtime wakes on access.", flush=True)
                    return True
                subdomain = data.get("subdomain")
                if subdomain:
                    health_url = f"https://{subdomain}.hf.space/api/health"
                    if http_healthy(health_url):
                        print("Space runtime health endpoint returned HTTP 200.", flush=True)
                        return True
                    print("Runtime metadata is RUNNING, but HTTP health is not yet ready.", flush=True)
                else:
                    print("Space reports RUNNING. No subdomain returned for HTTP probe.", flush=True)
                    return True
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
            print(f"Space check {attempt} failed: {type(exc).__name__}: {exc}", flush=True)
        if attempt < attempts:
            time.sleep(interval)
    print("Space failed to reach a healthy state before the verification deadline.", file=sys.stderr)
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--expected-sha", required=True)
    args = parser.parse_args()
    raise SystemExit(0 if check_space(args.repo, args.expected_sha) else 1)
