#!/usr/bin/env python3
"""通用周榜封面生成器：一次输出 16:9 / 4:3 / 3:4 三种封面（GitHub 暗色风格，Noto Sans CJK）。

用法：
  python make_covers.py <项目目录> [--sizes 16x9,4x3,3x4] [--config cover.json] [--preview-dir build_covers]

输入：
  <项目目录>/data.json   榜单数据。支持两种结构：
      - 顶层 {key: {rank, owner, repo, week, short, ...}}（GitHub 周榜，"_" 开头的键忽略）
      - {"items": {key: {rank, org/owner, repo|name, likes, ...}}}（Hugging Face 周榜）
  <项目目录>/cover.json  文案与指标配置（可选，下面是全部字段与默认值）：
      brand "GitHub" | title_suffix "本周热榜" | top "Top 5" | date "" | sub1 "" | sub2 ""
      metric "week"（数值字段，如 HF 用 "likes"）| metric_label "本周" | metric_prefix "+"
      desc_key "short"（条目里的一行中文短描述字段）| descs {key: 描述}（覆盖/补充）
      avatars {key或owner: 相对路径}（覆盖头像查找）
  头像查找顺序：cover.json avatars → assets/avatar_<owner>.png → assets/av/<key>.png
      → assets/proc/avatar_<owner>.png → 首字母占位图。
输出：
  cover.png (1920x1080) / cover_4x3.png (1440x1080) / cover_3x4.png (1080x1440)，
  以及 <preview-dir> 下的缩略预览（16:9/4:3 → 480 宽，3:4 → 360 宽）。
"""
import argparse, json, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BG, PANEL, BORDER = "#0D1117", "#161B22", "#30363D"
FG, MUTED, YELLOW = "#E6EDF3", "#8B949E", "#E3B341"
FB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
_fc = {}
def F(sz, bold=True, mono=False):
    k = (sz, bold, mono)
    if k not in _fc: _fc[k] = ImageFont.truetype(FB if bold else FR, sz, index=7 if mono else 2)
    return _fc[k]

SIZES = {"16x9": (1920, 1080, "cover.png", 480), "4x3": (1440, 1080, "cover_4x3.png", 480),
         "3x4": (1080, 1440, "cover_3x4.png", 360)}

# ---------- 数据 ----------
def load(proj, cfg_path):
    d = json.load(open(os.path.join(proj, "data.json"), encoding="utf-8"))
    cfg = {"brand": "GitHub", "title_suffix": "本周热榜", "top": "Top 5", "date": "", "sub1": "", "sub2": "",
           "metric": "week", "metric_label": "本周", "metric_prefix": "+", "desc_key": "short", "descs": {}, "avatars": {}}
    cp = cfg_path or os.path.join(proj, "cover.json")
    if os.path.exists(cp): cfg.update(json.load(open(cp, encoding="utf-8")))
    src = d["items"] if isinstance(d.get("items"), dict) else {k: v for k, v in d.items() if not k.startswith("_")}
    items = []
    for key, v in src.items():
        if not isinstance(v, dict) or "rank" not in v: continue
        full = v.get("repo") or v.get("id") or v.get("name", key)
        owner = full.split("/")[0] if "/" in full else (v.get("owner") or v.get("org") or "")
        name = full.split("/", 1)[1] if "/" in full else full
        if v.get("owner") and "/" not in full: name = full
        items.append(dict(key=key, rank=v["rank"], owner=owner, name=name,
                          metric=v.get(cfg["metric"]), desc=cfg["descs"].get(key) or v.get(cfg["desc_key"], "")))
    items.sort(key=lambda x: x["rank"])
    return items[:5], cfg

def avatar(proj, cfg, it, size):
    cands = [cfg["avatars"].get(it["key"]), cfg["avatars"].get(it["owner"]),
             f"assets/avatar_{it['owner']}.png", f"assets/av/{it['key']}.png", f"assets/proc/avatar_{it['owner']}.png"]
    for c in cands:
        if c and os.path.exists(os.path.join(proj, c)):
            av = Image.open(os.path.join(proj, c)).convert("RGBA").resize((size, size), Image.LANCZOS)
            out = Image.new("RGBA", (size, size), (255, 255, 255, 255)); out.alpha_composite(av)
            return out.convert("RGB")
    out = Image.new("RGB", (size, size), "#21262D"); dd = ImageDraw.Draw(out)
    dd.text((size / 2, size / 2), (it["owner"] or it["name"])[:1].upper(), font=F(int(size * .5)), fill=FG, anchor="mm")
    return out

# ---------- 绘图基础 ----------
class Canvas:
    def __init__(s, W, H):
        s.W, s.H = W, H
        img = Image.new("RGB", (W, H), BG)
        glow = Image.new("RGB", (W, H), BG); g = ImageDraw.Draw(glow)
        g.ellipse((-W * .16, -H * .39, W * .57 if W > H else W * .8, H * .57 if W > H else H * .42), fill="#13294B")
        g.ellipse((W * .65, -H * .28, W * 1.2, H * .48 if W > H else H * .3), fill="#241B3D")
        s.img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(180)), 0.9)
        s.d = ImageDraw.Draw(s.img)
        gy = int(H * (.52 if W >= H * 1.5 else .43))
        for x in range(40, W, 48):
            for y in range(40, gy, 48): s.d.point((x, y), fill="#1B222C")
    def tw(s, t, f): b = s.d.textbbox((0, 0), t, font=f); return b[2] - b[0]
    def text(s, xy, t, f, fill, anchor="la"): s.d.text(xy, t, font=f, fill=fill, anchor=anchor)
    def star(s, cx, cy, r):
        s.d.polygon([(cx + (r if i % 2 == 0 else r * .45) * math.cos(-math.pi / 2 + i * math.pi / 5),
                      cy + (r if i % 2 == 0 else r * .45) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)], fill=YELLOW)
    def fit(s, t, size, maxw, bold=True, mono=False, minsize=10):
        while size > minsize and s.tw(t, F(size, bold, mono)) > maxw: size -= 2
        return size
    def pill(s, x, y, t, size):
        f = F(size); w = s.tw(t, f); h = round(size * 1.94)
        s.d.rounded_rectangle((x, y, x + w + round(size * 1.88), y + h), radius=h // 2, fill=PANEL, outline=YELLOW, width=3)
        s.text((x + round(size * .94), y + h // 2), t, f, YELLOW, "lm")
    def paste_av(s, im, x, y, size, radius):
        m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
        s.img.paste(im, (x, y), m)
        s.d.rounded_rectangle((x - 2, y - 2, x + size + 1, y + size + 1), radius=radius + 1, outline=BORDER, width=2 if size < 100 else 3)

def mfmt(cfg, v): return f"{cfg['metric_prefix']}{v:,}" if isinstance(v, (int, float)) else str(v or "")
def title_text(cfg): return f"{cfg['brand']} {cfg['title_suffix']}".strip()

# ---------- 16:9：标题 + 五张竖卡 ----------
def layout_wide(proj, items, cfg, W, H):
    c = Canvas(W, H); X0 = 110
    if cfg["date"]: c.pill(X0, 72, cfg["date"], 34)
    ts = c.fit(title_text(cfg), 150, W - 2 * X0)
    c.text((X0 - 6, 168), title_text(cfg), F(ts), FG)
    tf = F(200); c.text((X0 - 4, 286), cfg["top"], tf, YELLOW)
    sx = X0 + c.tw(cfg["top"], tf) + 70
    if cfg["sub1"]: c.text((sx, 410), cfg["sub1"], F(c.fit(cfg["sub1"], 44, W - X0 - sx, False), False), MUTED, "lm")
    if cfg["sub2"]: c.text((sx, 475), cfg["sub2"], F(c.fit(cfg["sub2"], 44, W - X0 - sx)), FG, "lm")
    cw, ch, gap = 320, 420, 26
    x = (W - (5 * cw + 4 * gap)) // 2; y0 = 600
    for it in items:
        hl = it["rank"] == 1
        c.d.rounded_rectangle((x, y0, x + cw, y0 + ch), radius=22, fill=PANEL, outline=YELLOW if hl else BORDER, width=5 if hl else 3)
        c.text((x + 26, y0 + 22), f"#{it['rank']}", F(54, mono=True), YELLOW if hl else FG)
        c.paste_av(avatar(proj, cfg, it, 132), x + cw - 158, y0 + 24, 132, 26)
        nf = F(38, mono=True); lines = [it["name"]]; maxw = cw - 52
        if c.tw(it["name"], nf) > maxw:
            parts = it["name"].split("-")
            if len(parts) > 1:
                best = min((("-".join(parts[:k]) + "-", "-".join(parts[k:])) for k in range(1, len(parts))),
                           key=lambda ab: max(c.tw(ab[0], nf), c.tw(ab[1], nf)))
                lines = list(best)
            sz = 38
            while max(c.tw(l, F(sz, mono=True)) for l in lines) > maxw: sz -= 2
            nf = F(sz, mono=True)
        ty = y0 + 172
        if it["owner"]: c.text((x + 26, ty), it["owner"] + " /", F(c.fit(it["owner"] + " /", 26, maxw, False, True), False, True), MUTED)
        ty += 38
        for l in lines: c.text((x + 26, ty), l, nf, FG); ty += nf.size + 4
        wd = cfg.get("descs_wide", {}).get(it["name"]) or it["desc"]
        if wd:
            c.text((x + 26, ty + 8), wd, F(c.fit(wd, 25, maxw, False, minsize=18), False), MUTED)
        sy = y0 + ch - 50
        c.star(x + 44, sy, 17)
        c.text((x + 72, sy), mfmt(cfg, it["metric"]), F(c.fit(mfmt(cfg, it["metric"]), 36, cw - 72 - 80, mono=True), mono=True), YELLOW, "lm")
        c.text((x + cw - 24, sy + 2), cfg["metric_label"], F(24, False), MUTED, "rm")
        x += cw + gap
    return c.img

# ---------- 列表行（4:3 单行名称；3:4 名称独占一行） ----------
def list_rows(c, proj, items, cfg, X0, y, rw, rh, gap, portrait):
    AVS = 84 if portrait else 76
    # 统一名称字号：所有行取同一字号，保证整齐
    for it in items:
        it["_full"] = (it["owner"] + "/" if it["owner"] else "") + it["name"]
    for it in items:
        hl = it["rank"] == 1
        c.d.rounded_rectangle((X0, y, X0 + rw, y + rh), radius=20, fill=PANEL, outline=YELLOW if hl else BORDER, width=5 if hl else 3)
        cy = y + rh // 2
        c.text((X0 + (28 if portrait else 30), cy), f"#{it['rank']}", F(50 if portrait else 52), YELLOW if hl else FG, "lm")
        ax = X0 + (112 if portrait else 120)
        c.paste_av(avatar(proj, cfg, it, AVS), ax, cy - AVS // 2, AVS, 16)
        tx = ax + AVS + 26; right = X0 + rw - (28 if portrait else 30)
        sf = F(40 if portrait else 44, mono=True); st = mfmt(cfg, it["metric"])
        lab = F(22 if portrait else 24, False)
        lab_w = c.tw(cfg["metric_label"], lab)
        num_r = right - lab_w - (14 if portrait else 24); st_w = c.tw(st, sf); star_x = num_r - st_w - (26 if portrait else 28)
        sy = cy + 24 if portrait else cy - 4
        c.text((right, sy), cfg["metric_label"], lab, MUTED, "rm")
        c.text((num_r, sy), st, sf, YELLOW, "rm")
        c.star(star_x, sy, 19 if portrait else 20)
        name_max = (right - tx) if portrait else (star_x - 26 - tx)
        it["_geom"] = (tx, cy, name_max, star_x - 22 - tx)
        y += rh + gap
    # 名称：统一字号
    ns = min(c.fit(it["_full"], 40 if not portrait else 38, it["_geom"][2], mono=True, minsize=26) for it in items)
    for it in items:
        tx, cy, name_max, desc_max = it["_geom"]
        n = c.fit(it["_full"], ns, name_max, mono=True, minsize=14)  # 个别超长名称再单独缩小
        reg, bold = F(n, False, True), F(n, mono=True)
        ny = cy - (24 if portrait else 18)
        own = it["owner"] + "/" if it["owner"] else ""
        if own: c.text((tx, ny), own, reg, MUTED, "lm")
        c.text((tx + (c.tw(own, reg) + 2 if own else 0), ny), it["name"], bold, FG, "lm")
        if it["desc"]:
            ds = c.fit(it["desc"], 26, desc_max if portrait else name_max, False, minsize=18)
            c.text((tx, cy + (24 if portrait else 26)), it["desc"], F(ds, False), MUTED, "lm")

def layout_4x3(proj, items, cfg, W, H):
    c = Canvas(W, H); X0 = 90
    if cfg["date"]: c.pill(X0, 48, cfg["date"], 32)
    ts = c.fit(title_text(cfg), 128, W - 2 * X0)
    c.text((X0 - 5, 124), title_text(cfg), F(ts), FG)
    tf = F(160); c.text((X0 - 4, 238), cfg["top"], tf, YELLOW)
    sx = X0 + c.tw(cfg["top"], tf) + 56
    if cfg["sub1"]: c.text((sx, 328), cfg["sub1"], F(c.fit(cfg["sub1"], 38, W - X0 - sx, False), False), MUTED, "lm")
    if cfg["sub2"]: c.text((sx, 386), cfg["sub2"], F(c.fit(cfg["sub2"], 38, W - X0 - sx)), FG, "lm")
    list_rows(c, proj, items, cfg, X0, 490, W - 2 * X0, 100, 12, False)
    return c.img

def layout_3x4(proj, items, cfg, W, H):
    c = Canvas(W, H); X0 = 72
    if cfg["date"]: c.pill(X0, 70, cfg["date"], 32)
    ts = c.fit(title_text(cfg), 124, W - 2 * X0)
    c.text((X0 - 5, 160), title_text(cfg), F(ts), FG)
    tf = F(190); c.text((X0 - 6, 272), cfg["top"], tf, YELLOW)
    if cfg["sub1"]: c.text((X0, 566), cfg["sub1"], F(c.fit(cfg["sub1"], 40, W - 2 * X0, False), False), MUTED, "lm")
    if cfg["sub2"]: c.text((X0, 624), cfg["sub2"], F(c.fit(cfg["sub2"], 40, W - 2 * X0)), FG, "lm")
    list_rows(c, proj, items, cfg, X0, 686, W - 2 * X0, 132, 14, True)
    return c.img

LAYOUTS = {"16x9": layout_wide, "4x3": layout_4x3, "3x4": layout_3x4}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project"); ap.add_argument("--sizes", default="16x9,4x3,3x4")
    ap.add_argument("--config"); ap.add_argument("--preview-dir", default="build_covers")
    ap.add_argument("--out-dir", help="输出目录（默认 = 项目目录）")
    a = ap.parse_args()
    items, cfg = load(a.project, a.config)
    out = a.out_dir or a.project; pv = os.path.join(out, a.preview_dir); os.makedirs(pv, exist_ok=True)
    for s in a.sizes.split(","):
        W, H, fn, pw = SIZES[s]
        im = LAYOUTS[s](a.project, items, cfg, W, H)
        im.save(os.path.join(out, fn))
        im.resize((pw, round(H * pw / W)), Image.LANCZOS).save(os.path.join(pv, fn.replace(".png", f"_{pw}w.png")))
        print("wrote", os.path.join(out, fn), im.size)

if __name__ == "__main__":
    main()
