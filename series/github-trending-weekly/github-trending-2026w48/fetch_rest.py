"""Fetch remaining READMEs, latest releases, and official images/avatars for W48."""
import json
import pathlib
import re
import shutil
import urllib.request
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "raw"
W47 = ROOT.parent / "github-trending-2026w47"


def fetch_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def fetch_text(url):
    return fetch_bytes(url).decode("utf-8", errors="replace")


# 1. Remaining READMEs + latest releases (no API rate limit)
repos = [
    ("meta", "astryx", "main"),
    ("pookjw", "HermesEnabler", "main"),
    ("we-promise", "sure", "main"),
    ("dream-num", "univer", "dev"),
    ("obsidianmd", "obsidian-skills", "main"),
]

for owner, repo, branch in repos:
    rm_path = RAW / f"README_{owner}_{repo}.md"
    for br in [branch, "main", "master"]:
        try:
            txt = fetch_text(f"https://raw.githubusercontent.com/{owner}/{repo}/{br}/README.md")
            rm_path.write_text(txt, encoding="utf-8")
            print(f"README OK: {owner}/{repo} ({br}, {len(txt)} chars)")
            break
        except Exception:
            pass
    try:
        html = fetch_text(f"https://github.com/{owner}/{repo}/releases/latest")
        m_tag = re.search(r'/releases/tag/([^"/?#]+)', html)
        m_dt = re.search(r'<relative-time[^>]*datetime="([^"]+)"', html)
        tag = m_tag.group(1) if m_tag else None
        dt = m_dt.group(1)[:10] if m_dt else None
    except Exception:
        tag, dt = None, None
    w47_meta = W47 / "raw" / f"meta_{owner}_{repo}.json"
    meta = json.loads(w47_meta.read_text(encoding="utf-8")) if w47_meta.exists() else {"full_name": f"{owner}/{repo}"}
    meta["_w48_latest_release"] = {"tag_name": tag, "published_at": dt}
    meta["_note"] = "README and latest release fetched fresh on 2026-11-27 via raw.githubusercontent.com and github.com HTML."
    (RAW / f"meta_{owner}_{repo}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  REL: {owner}/{repo} -> {tag} ({dt})")

# 2. Prepare assets/proc for ai and other
ai_proc = ROOT / "ai" / "assets" / "proc"
other_proc = ROOT / "other" / "assets" / "proc"
ai_proc.mkdir(parents=True, exist_ok=True)
other_proc.mkdir(parents=True, exist_ok=True)

# Copy reusable verified official images & avatars from W47
w47_ai_proc = W47 / "ai" / "assets" / "proc"
for f in w47_ai_proc.glob("*"):
    if f.is_file() and not f.name.startswith("l30") and not f.name.startswith("avatar_mvanhorn"):
        shutil.copy2(f, ai_proc / f.name)

w47_other_proc = W47 / "other" / "assets" / "proc"
for f in w47_other_proc.glob("*"):
    if f.is_file():
        shutil.copy2(f, other_proc / f.name)

print("Copied reusable W47 assets.")

# 3. Download n8n-io avatar and official Nod visuals from n8n-io/nod repo
nod_imgs = [
    ("avatar_n8n-io.png", "https://github.com/n8n-io.png?size=256"),
    ("nod-hero.png", "https://raw.githubusercontent.com/n8n-io/nod/main/docs/src/assets/readme/hero-dark.webp"),
    ("nod-call-brief.png", "https://raw.githubusercontent.com/n8n-io/nod/main/docs/src/assets/readme/call-brief.webp"),
    ("nod-approval.png", "https://raw.githubusercontent.com/n8n-io/nod/main/docs/src/assets/readme/approval.webp"),
    ("nod-use-cases.png", "https://raw.githubusercontent.com/n8n-io/nod/main/docs/src/assets/readme/use-cases.webp"),
]
tmp_dir = ROOT / "ai" / "assets" / "raw"
tmp_dir.mkdir(parents=True, exist_ok=True)

for fname, url in nod_imgs:
    try:
        data = fetch_bytes(url)
        raw_f = tmp_dir / (fname + ".orig")
        raw_f.write_bytes(data)
        im = Image.open(raw_f)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA")
        out_p = ai_proc / fname
        im.save(out_p, "PNG")
        print(f"IMG OK: {fname} ({im.size})")
    except Exception as e:
        print(f"IMG ERR {fname}: {e}")
