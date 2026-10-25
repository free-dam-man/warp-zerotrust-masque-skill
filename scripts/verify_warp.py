#!/usr/bin/env python3
"""Verify whether the current machine's traffic is going through
Cloudflare WARP / Zero Trust, by reading Cloudflare's official trace
endpoint and parsing its key=value output.

Usage:
    python3 scripts/verify_warp.py          # human-readable verdict
    python3 scripts/verify_warp.py --json   # machine-readable

Exit codes:
    0  warp is enabled (on / gateway)
    1  reached Cloudflare but warp is off
    2  could not reach the trace endpoint (network problem)

No third-party dependencies; Python 3.8+ standard library only.
The script only *reads* the trace page. It never changes any setting.
"""

import json
import sys
import urllib.request

TRACE_URL = "https://www.cloudflare.com/cdn-cgi/trace"
TIMEOUT = 15


def fetch_trace(url=TRACE_URL, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": "warp-verify/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def parse_trace(text):
    data = {}
    for line in text.strip().splitlines():
        if "=" in line:
            key, _, value = line.partition("=")
            data[key.strip()] = value.strip()
    return data


def verdict(data):
    warp = data.get("warp", "")
    if warp in ("on", "gateway"):
        return 0, f"PASS: WARP/Zero Trust is ENABLED (warp={warp})"
    if warp == "off":
        return 1, (
            "FAIL: warp=off. This machine is NOT routed through WARP right now.\n"
            "Check: 1) WARP client shows Connected; 2) the device profile that "
            "actually applies to this device has tunnel protocol MASQUE and was "
            "SAVED; 3) no other VPN/proxy is stealing the route."
        )
    return 1, f"FAIL: unexpected warp value: {warp!r}"


def main(argv):
    as_json = "--json" in argv
    try:
        data = parse_trace(fetch_trace())
    except Exception as exc:  # network / proxy / TLS problems
        if as_json:
            print(json.dumps({"ok": False, "error": str(exc)}))
        else:
            print(f"ERROR: could not reach {TRACE_URL}: {exc}")
            print("Check the machine's base connectivity first, then retry.")
        return 2

    code, message = verdict(data)
    if as_json:
        print(json.dumps({"ok": code == 0, "trace": data}, ensure_ascii=False))
    else:
        print(f"ip   = {data.get('ip', '?')}")
        print(f"colo = {data.get('colo', '?')}   loc = {data.get('loc', '?')}")
        print(f"warp = {data.get('warp', '?')}   tls = {data.get('tls', '?')}")
        print(message)
        if code == 0:
            print("Note the colo above: it is the Cloudflare data center your")
            print("traffic exits through. Far-away colo = slower speeds.")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
