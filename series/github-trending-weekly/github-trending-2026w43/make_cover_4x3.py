"""封面图：1920x1080，GitHub 暗色风格，Noto Sans CJK（与视频一致）"""
import json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1440, 1080
BG, PANEL, BORDER = "#0D1117", "#161B22", "#30363D"
FG, MUTED = "#E6EDF3", "#8B949E"
BLUE, GREEN, YELLOW, PURPLE, ORANGE = "#2F81F7", "#3FB950", "#E3B341", "#A371F7", "#F0883E"
FB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"; FR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def F(sz, bold=True, mono=False): return ImageFont.truetype(FB if bold else FR, sz, index=7 if mono else 2)
D = json.load(open("data.json", encoding="utf-8"))
items = sorted([v for k, v in D.items() if not k.startswith("_")], key=lambda v: v["rank"])
AV = {"morluto": "avatar_morluto.png", "anthropics": "avatar_anthropics.png", "ruvnet": "avatar_ruvnet.png", "android": "avatar_android.png", "K-Dense-AI": "avatar_K-Dense-AI.png"}

img = Image.new("RGB", (W, H), BG)
# 柔和光晕
glow = Image.new("RGB", (W, H), BG); g = ImageDraw.Draw(glow)
g.ellipse((-300, -420, 900, 560), fill="#13294B"); g.ellipse((950, -300, 1800, 460), fill="#241B3D")
img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(180)), 0.9)
d = ImageDraw.Draw(img)
# 点阵网格
for x in range(40, W, 48):
    for y in range(40, 470, 48): d.point((x, y), fill="#1B222C")

def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)
def tw(s, f): b = d.textbbox((0, 0), s, font=f); return b[2] - b[0], b[3] - b[1], b
def text(xy, s, f, fill, anchor="la"): d.text(xy, s, font=f, fill=fill, anchor=anchor)

# 日期胶囊
X0 = 90
cf = F(32)
cs = "2026 · 第 43 周 · 10月23日"
w_, h_, _ = tw(cs, cf)
d.rounded_rectangle((X0, 48, X0 + w_ + 60, 48 + 62), radius=31, fill=PANEL, outline=YELLOW, width=3)
text((X0 + 30, 48 + 31), cs, cf, YELLOW, "lm")
text((X0 - 5, 124), "GitHub 本周热榜", F(128), FG, "la")
tf = F(160)
text((X0 - 4, 238), "Top 5", tf, YELLOW, "la")
tw5 = tw("Top 5", tf)[0]
text((X0 + tw5 + 56, 328), "智能体技能 · 插件 · 外壳 · 逆向", F(38, bold=False), MUTED, "lm")
text((X0 + tw5 + 56, 386), "五个项目全是 AI 智能体生态", F(38), FG, "lm")

# 竖排列表
rw, rh, gap = W - 2 * X0, 100, 12
y = 490
AVS = 76
for it in items:
    hl = it["rank"] == 1
    d.rounded_rectangle((X0, y, X0 + rw, y + rh), radius=20, fill=PANEL, outline=YELLOW if hl else BORDER, width=5 if hl else 3)
    cy = y + rh // 2
    text((X0 + 30, cy), f"#{it['rank']}", F(52), YELLOW if hl else FG, "lm")
    ax, ay = X0 + 120, cy - AVS // 2
    av = Image.open("assets/" + AV[it["owner"]]).convert("RGBA").resize((AVS, AVS), Image.LANCZOS)
    bgp = Image.new("RGBA", (AVS, AVS), (255, 255, 255, 255)); bgp.alpha_composite(av)
    m = Image.new("L", (AVS, AVS), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, AVS - 1, AVS - 1), radius=16, fill=255)
    img.paste(bgp.convert("RGB"), (ax, ay), m)
    d.rounded_rectangle((ax - 2, ay - 2, ax + AVS + 1, ay + AVS + 1), radius=17, outline=BORDER, width=2)
    tx = ax + AVS + 26
    of = F(40, mono=True)
    own = it["owner"] + "/"
    text((tx, cy - 18), own, F(40, bold=False, mono=True), MUTED, "lm")
    text((tx + tw(own, F(40, bold=False, mono=True))[0] + 2, cy - 18), it["repo"], of, FG, "lm")
    text((tx, cy + 26), it["short"], F(26, bold=False), MUTED, "lm")
    # 星标（右对齐）
    sf = F(44, mono=True); st = f"+{it['week']:,}"
    rx = X0 + rw - 30
    text((rx, cy - 4), "本周", F(24, bold=False), MUTED, "rm")
    sw = tw(st, sf)[0]
    text((rx - 72, cy - 4), st, sf, YELLOW, "rm")
    star(rx - 72 - sw - 28, cy - 4, 20, YELLOW)
    y += rh + gap
img.save("cover_4x3.png")
img.resize((480, 360), Image.LANCZOS).save("build_fri/cover_4x3_480_v2.png")
img.save("build_fri/cover_4x3_v2.png")
print("ok", y - gap)
