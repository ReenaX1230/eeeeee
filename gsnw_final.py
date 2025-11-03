#!/usr/bin/env python3
import requests, sys, time, os
from pathlib import Path

token = os.getenv("GITHUB_TOKEN")
if not token:
    print("[x] export GITHUB_TOKEN=ghp_...")
    sys.exit(1)

def search(query, out):
    h = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    matched = set(); page = 1
    print("GSNW - FINAL WORKING\n[i] Query:", query)
    while True:
        r = requests.get("https://api.github.com/search/code", headers=h,
                         params={"q": query, "per_page": 100, "page": page}, timeout=15)
        if r.status_code != 200:
            print("[x]", r.status_code, r.json().get("message",""))
            break
        data = r.json()
        items = data.get("items", [])
        if not items:
            print(f"Page {page} → done")
            break
        new = 0
        for item in items:
            path = item["path"]
            for seg in path.replace("\\","/").split("/"):
                if seg and query.split()[0].lower() in seg.lower() and seg not in matched:
                    print(f"[x] {seg}")
                    matched.add(seg)
                    new += 1
        print(f"Page {page} → {new} new")
        page += 1
        time.sleep(0.8)
    if out:
        Path(out).write_text("\n".join(sorted(f"[x] {s}" for s in matched)) + "\n")
        print(f"\nSaved {len(matched)} → {out}")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("output", nargs="?")
    a = p.parse_args()
    search(f"{a.query} in:file", a.output)
