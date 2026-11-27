"""Fetch GitHub Weekly Trending snapshot and save raw HTML, snapshot time, and parsed JSON."""
import datetime
import json
import os
import pathlib
import re
import urllib.request
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "raw"
RAW.mkdir(parents=True, exist_ok=True)
(ROOT / "ai").mkdir(parents=True, exist_ok=True)
(ROOT / "other").mkdir(parents=True, exist_ok=True)

URL = "https://github.com/trending?since=weekly"


def fetch_html(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_trending(html: str):
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.select("article.Box-row")
        items = []
        for idx, art in enumerate(articles, 1):
            a = art.select_one("h2 a")
            full = "/".join(p.strip() for p in a.get_text().split("/") if p.strip())
            desc_el = art.select_one("p")
            desc = desc_el.get_text(" ", strip=True) if desc_el else ""
            lang_el = art.select_one('[itemprop="programmingLanguage"]')
            lang = lang_el.get_text(strip=True) if lang_el else "Unknown"
            star_a = art.select_one('a[href$="/stargazers"]')
            total_stars = int(star_a.get_text(strip=True).replace(",", "")) if star_a else 0
            wk_el = art.select_one("span.d-inline-block.float-sm-right")
            wk_txt = wk_el.get_text(strip=True) if wk_el else ""
            m = re.search(r"([\d,]+)", wk_txt)
            week_stars = int(m.group(1).replace(",", "")) if m else 0
            items.append({
                "page_rank": idx,
                "repo": full,
                "owner": full.split("/")[0],
                "name": full.split("/")[1],
                "language": lang,
                "total_stars": total_stars,
                "week_stars": week_stars,
                "description": desc,
            })
        return items
    except ImportError:
        # Regex fallback if bs4 not installed
        blocks = re.findall(r'<article[^>]*class="Box-row"[^>]*>(.*?)</article>', html, re.S)
        items = []
        for idx, b in enumerate(blocks, 1):
            m_href = re.search(r'<h2[^>]*>.*?<a[^>]*href="/([^/"]+/[^/"]+)"', b, re.S)
            full = m_href.group(1).strip() if m_href else ""
            m_desc = re.search(r'<p[^>]*>(.*?)</p>', b, re.S)
            desc = re.sub(r"<[^>]+>", "", m_desc.group(1)).strip() if m_desc else ""
            desc = re.sub(r"\s+", " ", desc)
            m_lang = re.search(r'itemprop="programmingLanguage"[^>]*>(.*?)</span>', b, re.S)
            lang = m_lang.group(1).strip() if m_lang else "Unknown"
            m_tot = re.search(r'href="/[^"]+/stargazers"[^>]*>.*?([\d,]+)\s*</a>', b, re.S)
            total_stars = int(m_tot.group(1).replace(",", "")) if m_tot else 0
            m_wk = re.search(r'([\d,]+)\s+stars\s+this\s+week', b, re.S)
            week_stars = int(m_wk.group(1).replace(",", "")) if m_wk else 0
            items.append({
                "page_rank": idx,
                "repo": full,
                "owner": full.split("/")[0] if "/" in full else "",
                "name": full.split("/")[1] if "/" in full else full,
                "language": lang,
                "total_stars": total_stars,
                "week_stars": week_stars,
                "description": desc,
            })
        return items


def main():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_bj = now_utc.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    now_pst = now_utc.astimezone(datetime.timezone(datetime.timedelta(hours=-8)))

    html = fetch_html(URL)
    (RAW / "trending_weekly.html").write_text(html, encoding="utf-8")

    snap = (
        f"Beijing (UTC+8): {now_bj.strftime('%Y-%m-%d %H:%M:%S %z')}\n"
        f"PST (UTC-8):     {now_pst.strftime('%Y-%m-%d %H:%M:%S %z')}\n"
        f"URL:             {URL}\n"
    )
    (RAW / "snapshot_time.txt").write_text(snap, encoding="utf-8")
    print(snap)

    items = parse_trending(html)
    print(f"Total items on page: {len(items)}\n")
    for it in items:
        print(
            f"{it['page_rank']:2d}. {it['repo']:42s} | +{it['week_stars']:6d}/wk | "
            f"{it['total_stars']:7d} total | {it['language']:14s} | {it['description'][:65]}"
        )

    out = {
        "snapshot_bj": now_bj.isoformat(),
        "snapshot_pst": now_pst.isoformat(),
        "url": URL,
        "count": len(items),
        "items": items,
    }
    (ROOT / "trending_weekly.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
