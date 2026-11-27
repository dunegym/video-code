"""Fetch GitHub API metadata, latest releases, READMEs, and owner avatars for W48 repos."""
import base64
import json
import pathlib
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "raw"

REPOS = [
    # AI Top 5
    "backnotprop/plannotator",
    "google-labs-code/stitch-skills",
    "GoogleChrome/modern-web-guidance-src",
    "n8n-io/nod",
    "alibaba/open-code-review",
    # Other Top 4
    "meta/astryx",
    "pookjw/HermesEnabler",
    "we-promise/sure",
    "dream-num/univer",
    # Verify new entrant classification
    "obsidianmd/obsidian-skills",
]

HEADERS = {
    "User-Agent": "github-trending-weekly-research/1.0",
    "Accept": "application/vnd.github+json",
}


def get_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def get_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


for full in REPOS:
    owner, repo = full.split("/")
    meta_path = RAW / f"meta_{owner}_{repo}.json"
    readme_path = RAW / f"README_{owner}_{repo}.md"

    try:
        meta = get_json(f"https://api.github.com/repos/{full}")
        # Also try latest release
        try:
            rel = get_json(f"https://api.github.com/repos/{full}/releases/latest")
            meta["_latest_release"] = {
                "tag_name": rel.get("tag_name"),
                "name": rel.get("name"),
                "published_at": rel.get("published_at"),
                "body": (rel.get("body") or "")[:1500],
            }
        except Exception:
            meta["_latest_release"] = None
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        lic = (meta.get("license") or {}).get("spdx_id") or "None"
        created = (meta.get("created_at") or "")[:10]
        rel_tag = (meta.get("_latest_release") or {}).get("tag_name") or "-"
        rel_dt = ((meta.get("_latest_release") or {}).get("published_at") or "")[:10]
        print(f"META OK: {full:40s} | lic={lic:12s} | created={created} | stars={meta.get('stargazers_count')} | rel={rel_tag} ({rel_dt})")
    except Exception as e:
        print(f"META ERR {full}: {e}")

    try:
        rm = get_json(f"https://api.github.com/repos/{full}/readme")
        content = base64.b64decode(rm["content"]).decode("utf-8", errors="replace")
        readme_path.write_text(content, encoding="utf-8")
        print(f"  README OK ({len(content)} chars)")
    except Exception as e:
        print(f"  README ERR {full}: {e}")

    time.sleep(0.3)
