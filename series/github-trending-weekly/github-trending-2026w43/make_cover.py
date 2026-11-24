"""封面图：1920x1080，GitHub 暗色风格，Noto Sans CJK（与视频一致）"""
import json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1920, 1080
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
g.ellipse((-300, -420, 1100, 620), fill="#13294B"); g.ellipse((1250, -300, 2300, 520), fill="#241B3D")
img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(180)), 0.9)
d = ImageDraw.Draw(img)
# 点阵网格
for x in range(40, W, 48):
    for y in range(40, 560, 48): d.point((x, y), fill="#1B222C")

def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)
def tw(s, f): b = d.textbbox((0, 0), s, font=f); return b[2] - b[0], b[3] - b[1], b
def text(xy, s, f, fill, anchor="la"): d.text(xy, s, font=f, fill=fill, anchor=anchor)

# 日期胶囊
X0 = 110
cf = F(34)
cs = "2026 · 第 43 周 · 10月23日"
w_, h_, _ = tw(cs, cf)
d.rounded_rectangle((X0, 72, X0 + w_ + 64, 72 + 66), radius=33, fill=PANEL, outline=YELLOW, width=3)
text((X0 + 32, 72 + 33), cs, cf, YELLOW, "lm")
# 标题
text((X0 - 6, 168), "GitHub 本周热榜", F(150), FG, "la")
tf = F(200)
text((X0 - 4, 286), "Top 5", tf, YELLOW, "la")
tw5 = tw("Top 5", tf)[0]
sub = F(44, bold=False)
text((X0 + tw5 + 70, 410), "智能体技能 · 插件 · 外壳 · 逆向", sub, MUTED, "lm")
text((X0 + tw5 + 70, 475), "五个项目全是 AI 智能体生态", F(44), FG, "lm")

# 项目卡片
cw, ch, gap = 320, 420, 26
x = (W - (5 * cw + 4 * gap)) // 2; y0 = 600
for it in items:
    hl = it["rank"] == 1
    col = YELLOW if hl else BORDER
    d.rounded_rectangle((x, y0, x + cw, y0 + ch), radius=22, fill=PANEL, outline=col, width=5 if hl else 3)
    # 排名徽章
    rf = F(54, mono=True)
    text((x + 26, y0 + 22), f"#{it['rank']}", rf, YELLOW if hl else FG, "la")
    # 头像
    av = Image.open("assets/" + AV[it["owner"]]).convert("RGBA").resize((132, 132), Image.LANCZOS)
    m = Image.new("L", (132, 132), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 131, 131), radius=26, fill=255)
    ax, ay = x + cw - 132 - 26, y0 + 24
    bgp = Image.new("RGBA", (132, 132), (255, 255, 255, 255)); bgp.alpha_composite(av)
    img.paste(bgp.convert("RGB"), (ax, ay), m)
    d.rounded_rectangle((ax - 2, ay - 2, ax + 133, ay + 133), radius=27, outline=BORDER, width=3)
    # 仓库名（过长则在连字符处折行）
    name = it["repo"]; nf = F(38, mono=True)
    lines = [name]
    if tw(name, nf)[0] > cw - 52:
        parts = name.split("-"); best = None
        for k in range(1, len(parts)):
            a, b = "-".join(parts[:k]) + "-", "-".join(parts[k:])
            wmax = max(tw(a, nf)[0], tw(b, nf)[0])
            if best is None or wmax < best[0]: best = (wmax, [a, b])
        lines = best[1]
        while max(tw(l, nf)[0] for l in lines) > cw - 52: nf = F(nf.size - 2, mono=True)
    ty = y0 + 178
    text((x + 26, ty), it["owner"] + " /", F(26, bold=False, mono=True), MUTED, "la")
    ty += 38
    for l in lines:
        text((x + 26, ty), l, nf, FG, "la"); ty += nf.size + 4
    # 本周星标
    sy = y0 + ch - 50
    star(x + 44, sy, 17, YELLOW)
    text((x + 72, sy), f"+{it['week']:,}", F(36, mono=True), YELLOW, "lm")
    text((x + cw - 24, sy + 2), "本周", F(24, bold=False), MUTED, "rm")
    x += cw + gap
img.save("cover.png")
img.resize((480, 270), Image.LANCZOS).save("build_fri/cover_480.png")
print("ok")
