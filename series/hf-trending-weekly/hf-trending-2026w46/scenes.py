"""Hugging Face 本周热门 Top 5（2026 第 46 周）—— Manim CE 场景。时间轴由 timing.json（MiniMax 词级时间戳）驱动；
动图/转台演示由 assemble.py 用 ffmpeg 叠加到占位图上，叠加参数由各场景写入 build/ov_<scene>.json。"""
import json, os, wave, textwrap
import numpy as np
from manim import *
from PIL import Image as _PILImage
_fromarray = _PILImage.fromarray
def _fa(arr, mode=None):
    if mode == "RGBA" and getattr(arr, "ndim", 3) == 2:
        return _PILImage.new("RGBA", (arr.shape[1], arr.shape[0]))
    return _fromarray(arr, mode) if mode else _fromarray(arr)
_PILImage.fromarray = _fa

config.pixel_width, config.pixel_height, config.frame_rate = 1920, 1080, 30
TM = json.load(open("timing.json", encoding="utf-8"))
DJ = json.load(open("data.json", encoding="utf-8")); DATA = DJ["items"]
TRD = {m["id"]: m for m in json.load(open("raw/trending_models.json"))}
A = "assets/proc/"
FONT, MONO = "Noto Sans CJK SC", "Noto Sans Mono CJK SC"
BG, PANEL, BORDER = "#0D1117", "#161B22", "#30363D"
FG, MUTED, DIM = "#E6EDF3", "#8B949E", "#6E7681"
BLUE, GREEN, YELLOW, PURPLE, ORANGE, RED = "#2F81F7", "#3FB950", "#E3B341", "#A371F7", "#F0883E", "#F85149"
HF = "#FFD21E"
INFO = {
    "jackrong": dict(chips=["text-generation", "Apache-2.0", "蒸馏于 2026-07-19"], what="DeepSeek V4 Pro 蒸馏到 Qwen3.5-9B 的数学模型", note="冲上榜首的是 Heretic 衍生仓库，不是原作者仓库"),
    "h3img": dict(chips=["text-to-image", "H3-Image 社区许可", "发布于 2026-11-10"], what="文生图和改图共用一个检查点 · 直接出 16MP", note="MiniMax H3 去音频分支 · 33.1B DiT · 6 步蒸馏"),
    "ltx": dict(chips=["image-to-video", "LTX-2.x 社区许可", "创建于 2026-07-23"], what="音视频联合生成 · 22B DiT", note="上周原榜 #3 → 本周仍是 #3"),
    "qwen": dict(chips=["image-text-to-text", "Apache-2.0", "发布于 2026-08-05"], what="27B 稠密多模态模型，原生看图看视频", note="官方模型 · 若干量化 / 去审查衍生仓库已合并"),
    "arete": dict(chips=["Qwen3.8-27B 微调", "Apache-2.0", "发布于 2026-11-06"], what="监督微调，改变敏感话题上的拒答和表述", note="Nous Research · 只做 SFT，没有强化学习"),
}
PIDS = ["jackrong", "h3img", "ltx", "qwen", "arete"]

def T(s, size=28, color=FG, font=FONT, **kw): return Text(s, font=font, font_size=size, color=color, **kw)
def M(s, size=24, color=FG, **kw): return Text(s, font=MONO, font_size=size, color=color, **kw)
def fit(m, w):
    if m.width > w: m.scale_to_fit_width(w)
    return m
def box(w, h, color=BORDER, fill=PANEL, r=0.16, sw=2, op=1):
    return RoundedRectangle(width=w, height=h, corner_radius=r, stroke_color=color, stroke_width=sw).set_fill(fill, op)
def node(label, w=1.9, h=0.75, color=BLUE, size=24, sub=None, subsize=16):
    b = box(w, h, color=color)
    t = T(label, size, FG)
    g = VGroup(t, T(sub, subsize, MUTED)).arrange(DOWN, buff=0.07) if sub else t
    fit(g, w - 0.2)
    if g.height > h - 0.12: g.scale_to_fit_height(h - 0.12)
    g.move_to(b)
    return VGroup(b, g)
def chip(text, color=MUTED, dot=None, size=20, font=FONT, fg=FG):
    t = Text(text, font=font, font_size=size, color=fg)
    inner = VGroup(Dot(radius=0.07, color=dot), t).arrange(RIGHT, buff=0.12) if dot else VGroup(t)
    b = RoundedRectangle(width=inner.width + 0.36, height=max(0.44, inner.height + 0.2), corner_radius=0.2,
                         stroke_color=color, stroke_width=1.5).set_fill(PANEL, 1)
    inner.move_to(b)
    return VGroup(b, inner)
def avatar(pid, h=0.5):
    im = ImageMobject(A + f"av_{pid}.png").scale_to_fit_height(h)
    return Group(im, SurroundingRectangle(im, buff=0, color=BORDER, stroke_width=1.5, corner_radius=0.06))
def picture(path, width=None, height=None, credit=None, csize=17):
    im = ImageMobject(path)
    if width: im.scale_to_fit_width(width)
    if height and im.height > height: im.scale_to_fit_height(height)
    fr = SurroundingRectangle(im, buff=0.02, color=BORDER, stroke_width=2)
    g = Group(im, fr)
    cap = T(credit, csize, MUTED).next_to(g, DOWN, buff=0.1) if credit else None
    if cap: fit(cap, max(g.width, 5.5))
    return g, cap
def heart(s=0.3, color=RED):
    c1 = Circle(radius=s * 0.28).set_fill(color, 1).set_stroke(width=0).shift(LEFT * s * 0.2 + UP * s * 0.1)
    c2 = c1.copy().shift(RIGHT * s * 0.4)
    sq = Square(side_length=s * 0.56).set_fill(color, 1).set_stroke(width=0).rotate(PI / 4).shift(DOWN * s * 0.12)
    return VGroup(c1, c2, sq)
def down_icon(s=0.3, color=BLUE):
    return VGroup(Line(UP * s * 0.5, DOWN * s * 0.2, color=color, stroke_width=5),
                  Triangle(color=color).set_fill(color, 1).set_stroke(width=0).scale(s * 0.28).rotate(PI).shift(DOWN * s * 0.25),
                  Line(LEFT * s * 0.4 + DOWN * s * 0.5, RIGHT * s * 0.4 + DOWN * s * 0.5, color=color, stroke_width=5))
def trend_icon(s=0.3, color=GREEN):
    return VMobject(color=color, stroke_width=5).set_points_as_corners(
        [np.array([-0.5, -0.4, 0]) * s, np.array([-0.15, 0.0, 0]) * s, np.array([0.1, -0.2, 0]) * s, np.array([0.5, 0.4, 0]) * s])
def step_list(items, w, size=21, color=BLUE):
    rows = VGroup()
    for i, (a, b) in enumerate(items):
        num = Circle(radius=0.2, color=color, stroke_width=2).set_fill(color, 0.15)
        n = T(str(i + 1), 18, FG, weight=BOLD).move_to(num)
        txt = VGroup(fit(T(a, size, FG, weight=BOLD), w - 0.6))
        if b: txt.add(fit(T(b, size - 4, MUTED), w - 0.6))
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        rows.add(VGroup(VGroup(num, n), txt).arrange(RIGHT, buff=0.2, aligned_edge=UP))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    return rows
def card_rows(title, rows, w, col=BLUE, size=22, tsize=26):
    t = fit(T(title, tsize, col, weight=BOLD), w - 0.6)
    rs = VGroup(*[VGroup(Dot(radius=0.06, color=c or col), fit(T(r, size, FG), w - 0.9)).arrange(RIGHT, buff=0.18) for r, c in rows])
    rs.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    inner = VGroup(t, rs).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    b = box(w, inner.height + 0.6, color=col, fill="#0F141B")
    inner.move_to(b).align_to(b.get_left() + RIGHT * 0.32, LEFT)
    return VGroup(b, t, rs)
def para(s, width_chars, size=18, color=FG, font=FONT, lh=0.36):
    lines = textwrap.wrap(s, width_chars)
    g = VGroup(*[Text(l, font=font, font_size=size, color=color) for l in lines])
    for i, l in enumerate(g): l.move_to([0, -i * lh, 0], aligned_edge=LEFT)
    return g
def hbars(rows, maxv, bw=4.0, lw=2.6, size=20, h=0.34, gap=0.16, fmt="{:g}", base=0.0):
    """横向条形图：rows=[(标签, 数值或 None, 颜色)]；标签右对齐于 x=-0.1，条从 x=0 起"""
    g = VGroup()
    for i, (lab, v, c) in enumerate(rows):
        y = -i * (h + gap)
        lt = fit(T(lab, size, FG if c not in (DIM, MUTED) else MUTED), lw - 0.1).move_to([-0.12, y, 0], aligned_edge=RIGHT)
        wv = 0.02 if v is None else max((v - base) / (maxv - base) * bw, 0.02)
        bar = Rectangle(width=wv, height=h, stroke_width=0).set_fill(c, 1).move_to([0, y, 0], aligned_edge=LEFT)
        vt = M("–" if v is None else fmt.format(v), size - 1, FG).next_to(bar, RIGHT, buff=0.1)
        g.add(VGroup(lt, bar, vt))
    return g
def grow(rows, lag=0.08):
    return LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows], lag_ratio=lag)
def mini(title, rows, maxv, bw=1.8, lw=1.6, size=15, h=0.2, gap=0.07, tsize=19, fmt="{:g}"):
    t = T(title, tsize, FG, weight=BOLD)
    bars = hbars(rows, maxv, bw, lw, size, h, gap, fmt)
    bars.next_to(t, DOWN, buff=0.14).align_to(t, LEFT)
    return VGroup(t, bars)
def legend(items, size=17):
    return VGroup(*[VGroup(Square(0.2).set_fill(c, 1).set_stroke(width=0), T(n, size, MUTED)).arrange(RIGHT, buff=0.1) for n, c in items]).arrange(RIGHT, buff=0.35)
def quote(s, w, src, col=ORANGE, size=21):
    t = fit(T(s, size, FG), w - 0.6)
    st = T(src, 15, MUTED)
    inner = VGroup(t, st).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    b = box(w, inner.height + 0.36, color=col, fill="#0F141B")
    inner.move_to(b).align_to(b.get_left() + RIGHT * 0.3, LEFT)
    bar = Line(b.get_corner(UL) + RIGHT * 0.12 + DOWN * 0.15, b.get_corner(DL) + RIGHT * 0.12 + UP * 0.15, color=col, stroke_width=4)
    return VGroup(b, bar, inner)
def stat_card(big, lab, w=2.7, h=1.35, col=BLUE, bsize=34, lsize=17, note=None):
    b = box(w, h, color=col, fill="#0F141B")
    bt = fit(M(big, bsize, col, weight=BOLD), w - 0.3)
    lt = fit(T(lab, lsize, FG), w - 0.25)
    g = VGroup(bt, lt)
    if note: g.add(fit(T(note, 14, MUTED), w - 0.25))
    g.arrange(DOWN, buff=0.1).move_to(b)
    return VGroup(b, g)

class Base(Scene):
    key = ""
    def setup(self):
        self.camera.background_color = BG
        self.tm = TM[self.key]; self.t = 0.0; self.ov = []
    def cue(self, i): return self.tm["cues"][min(i, len(self.tm["cues"]) - 1)]["start"]
    def P(self, *anims, rt=1.0, **kw):
        self.play(*anims, run_time=rt, **kw); self.t += rt
    def W(self, until):
        if until > self.t + 1 / 30:
            self.wait(until - self.t); self.t = until
    def finish(self):
        end = self.tm["total"]
        self.W(end - 0.55)
        self.P(*[FadeOut(m) for m in self.mobjects], rt=0.45)
        self.W(end)
        json.dump(self.ov, open(f"build/ov_{self.key}.json", "w"), indent=1)
    def overlay(self, clip, mob, t0, t1, ss=0.0, speed=1.0):
        x, y, w, h = to_px(mob)
        self.ov.append({"clip": clip, "t0": round(t0, 3), "dur": round(t1 - t0, 3), "ss": ss, "speed": speed, "x": x, "y": y, "w": w, "h": h})
    def header(self, pid, section, color=BLUE):
        d = DATA[pid]
        av = avatar(pid, 0.5)
        rk = T(f"#{d['rank']}", 34, YELLOW, weight=BOLD)
        nm = M(d["repo"], 24, FG)
        sec = VGroup(Dot(radius=0.05, color=color), T(section, 18, MUTED)).arrange(RIGHT, buff=0.1)
        g = Group(av, rk, nm, sec).arrange(RIGHT, buff=0.22).to_corner(UL, buff=0.32)
        line = Line(LEFT * 7.1 + UP * 3.25, RIGHT * 7.1 + UP * 3.25, color=BORDER, stroke_width=1.5)
        return Group(g, line)
    def head(self, pid, section, color=BLUE):
        h = self.header(pid, section, color); self.P(FadeIn(h), rt=0.4); return h
    def counter(self, label, value, color, icon, w=2.05):
        b = box(w, 1.25)
        lab = T(label, 18, MUTED).move_to(b.get_top() + DOWN * 0.28)
        vt = ValueTracker(0)
        num = always_redraw(lambda: fit(M(f"{int(vt.get_value()):,}", 32, color, weight=BOLD), w - 0.75)
                            .move_to(b.get_center() + DOWN * 0.2 + RIGHT * 0.2))
        ic = always_redraw(lambda: icon().next_to(num, LEFT, buff=0.14))
        return VGroup(b, lab, num, ic), vt.animate(rate_func=rate_functions.ease_out_cubic).set_value(value)

def note_line(s, w=6.3, size=17): return fit(T(s, size, MUTED), w)
PX = 1920 / config.frame_width   # 每单位像素
def _sub_t(self, prefix):
    for x in self.tm["subs"]:
        if prefix in x["text"]: return x["start"]
    print("WARN sub_t not found", self.key, prefix); return self.t
Base.sub_t = _sub_t
def src_t(s, size=15): return T(s, size, MUTED)
def vbars(groups, cols, maxv, gw=1.0, bw=0.22, hmax=2.2, size=14, fmt="{:g}", lab_size=16, lab_w=None):
    """分组竖条：groups=[(标签, [值...])]，cols=[颜色...]"""
    g = VGroup()
    for i, (lab, vals) in enumerate(groups):
        x0 = i * gw
        bars = VGroup()
        for j, (v, c) in enumerate(zip(vals, cols)):
            h = max(v / maxv * hmax, 0.02)
            r = Rectangle(width=bw, height=h, stroke_width=0).set_fill(c, 1).move_to([x0 + (j - (len(vals) - 1) / 2) * (bw + 0.04), h / 2, 0])
            vt = M(fmt.format(v), size, FG).next_to(r, UP, buff=0.05)
            bars.add(VGroup(r, vt))
        lt = T(lab, lab_size, FG).next_to([x0, 0, 0], DOWN, buff=0.12)
        if lab_w: fit(lt, lab_w)
        g.add(VGroup(bars, lt))
    return g
def grow_v(g, lag=0.1):
    return LaggedStart(*[AnimationGroup(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in grp[0]], FadeIn(grp[1])) for grp in g], lag_ratio=lag)


def to_px(m):
    l, r = m.get_left()[0], m.get_right()[0]; t, b = m.get_top()[1], m.get_bottom()[1]
    X = (l + config.frame_width / 2) / config.frame_width * 1920
    Y = (config.frame_height / 2 - t) / config.frame_height * 1080
    W = (r - l) / config.frame_width * 1920; H = (t - b) / config.frame_height * 1080
    ev = lambda v: int(round(v / 2) * 2)
    return ev(X), ev(Y), ev(W), ev(H)
def dashed_sep(y, x0=-6.9, x1=6.9): return DashedLine([x0, y, 0], [x1, y, 0], color=BORDER, dash_length=0.12)
def sec_title(s, col=FG, size=22): return T(s, size, col, weight=BOLD)

# ───────────────────────────── 开场
class S0_Intro(Base):
    key = "S0_Intro"
    def construct(self):
        face = Circle(radius=0.62).set_fill(HF, 1).set_stroke(width=0)
        eyes = VGroup(*[Ellipse(width=0.12, height=0.2).set_fill("#3A2A00", 1).set_stroke(width=0).move_to(face.get_center() + [dx, 0.15, 0]) for dx in (-0.22, 0.22)])
        mouth = Arc(radius=0.3, start_angle=PI * 1.15, angle=PI * 0.7, color="#3A2A00", stroke_width=6).move_to(face.get_center() + DOWN * 0.2)
        hands = VGroup(*[Circle(radius=0.17).set_fill("#F4B400", 1).set_stroke(width=0).move_to(face.get_center() + [dx, -0.42, 0]) for dx in (-0.45, 0.45)])
        emo = VGroup(face, eyes, mouth, hands)
        t1 = T("Hugging Face", 64, FG, weight=BOLD)
        t2 = T("本周热门模型 Top 5", 54, HF, weight=BOLD)
        tt = VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        title = VGroup(emo, tt).arrange(RIGHT, buff=0.5).move_to(UP * 1.75)
        date = chip("2026 年第 46 周 · 11 月 14 日", color=HF, size=24).next_to(title, DOWN, buff=0.4)
        self.P(FadeIn(emo, scale=0.6), FadeIn(tt, shift=RIGHT * 0.3), rt=0.9)
        self.P(FadeIn(date, shift=UP * 0.15), rt=0.5)
        cards = Group()
        for pid in PIDS:
            d = DATA[pid]
            b = box(2.45, 2.0)
            av = avatar(pid, 0.7)
            rk = T(f"#{d['rank']}", 30, YELLOW, weight=BOLD)
            nm = fit(T(d["name"], 18, FG), 2.2)
            Group(av, rk, nm).arrange(DOWN, buff=0.14).move_to(b)
            cards.add(Group(b, av, rk, nm))
        cards.arrange(RIGHT, buff=0.18).move_to(DOWN * 1.15)
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in cards], lag_ratio=0.15), rt=1.2)
        self.P(cards[0][0].animate.set_stroke(YELLOW, 3), rt=0.4)
        self.finish()

# ───────────────────────────── 模型简介
class IntroScene(Base):
    pid = ""
    def construct(self):
        d = DATA[self.pid]; info = INFO[self.pid]
        likes, dl, ts = d["likes"], d["downloads_30d"], d["trendingScore"]
        rank = T(f"#{d['rank']}", 104, YELLOW, weight=BOLD).to_corner(UL, buff=0.45)
        rank_lab = T("本周热门", 24, MUTED).next_to(rank, RIGHT, buff=0.25).align_to(rank, DOWN).shift(UP * 0.18)
        av = avatar(self.pid, 0.46)
        owner = M(d["repo"].split("/")[0] + " /", 28, MUTED)
        og = Group(av, owner).arrange(RIGHT, buff=0.15).next_to(rank, DOWN, buff=0.25).align_to(rank, LEFT)
        repo = fit(M(d["repo"].split("/")[1], 44, FG, weight=BOLD), 6.2).next_to(og, DOWN, buff=0.12).align_to(rank, LEFT)
        chips = VGroup(*[chip(c, size=20) for c in info["chips"]]).arrange(RIGHT, buff=0.12)
        fit(chips, 6.3).next_to(repo, DOWN, buff=0.3).align_to(rank, LEFT)
        c1, a1 = self.counter("点赞", likes, FG, lambda: heart(0.3))
        c2, a2 = self.counter("近 30 天下载", dl, FG, lambda: down_icon(0.3))
        c3, a3 = self.counter("热度分", ts, HF, lambda: trend_icon(0.3, HF))
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.12).next_to(chips, DOWN, buff=0.4).align_to(rank, LEFT)
        what = fit(T(info["what"], 28, FG), 6.1).next_to(cards, DOWN, buff=0.45).align_to(rank, LEFT).shift(RIGHT * 0.2)
        bar = Line(what.get_corner(UL) + LEFT * 0.15, what.get_corner(DL) + LEFT * 0.15, color=HF, stroke_width=4)
        nt = note_line(info["note"], 6.3, 17).next_to(what, DOWN, buff=0.3).align_to(rank, LEFT)
        allg = Group(rank, rank_lab, og, repo, chips, cards, what, bar, nt); self.nt = nt
        allg.shift(UP * (0.3 - (allg.get_top()[1] + allg.get_bottom()[1]) / 2))
        self.P(FadeIn(rank, shift=RIGHT * 0.3), FadeIn(rank_lab), FadeIn(og), FadeIn(repo, shift=UP * 0.2), rt=0.8)
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips], lag_ratio=0.2), rt=0.6)
        self.P(FadeIn(c1), FadeIn(c2), FadeIn(c3), rt=0.3)
        self.P(a1, a2, a3, rt=1.6)
        self.right()
        self.W(max(self.cue(1) - 0.3, self.t) if len(self.tm["cues"]) > 1 else self.t)
        self.P(FadeIn(what, shift=RIGHT * 0.2), Create(bar), FadeIn(nt), rt=0.6)
        self.later()
        self.finish()
    def right(self): pass
    def later(self): pass
    def panel(self, h=5.6): return box(6.5, h, color=BORDER, fill="#0F141B").move_to([3.55, 0.3, 0])

class P1a(IntroScene):
    key = "P1a"; pid = "jackrong"
    def right(self):
        lc = DATA["jackrong"]["likes_check"]
        b = self.panel()
        t = T("点赞账号是什么时候注册的？", 22, FG, weight=BOLD)
        st = fit(T("占比 = 2026 年 8 月及以后 / 全部点赞账号", 15, MUTED), 6.0)
        sh = hbars([
            ("衍生仓库（登顶）", lc["heretic"]["share_new"], ORANGE),
            ("原作者仓库", lc["canonical"]["share_new"], DIM),
            ("H3-Image（对照）", lc["MiniMax-H3-Image"]["share_new"], BLUE),
            ("Arete-27B（对照）", lc["Arete-27B"]["share_new"], GREEN),
        ], 100, bw=2.5, lw=2.5, size=16, h=0.28, gap=0.1, fmt="{:.1f}%")
        mt = T("衍生仓库：按注册月份", 17, MUTED)
        mon = lc["heretic"]["by_month"]
        vb = vbars([(k[5:] + " 月" if k != "2026-11" else "11 月 1–14 日", [mon[k]]) for k in ["2026-08", "2026-09", "2026-10", "2026-11"]],
                   [ORANGE], 5200, gw=1.35, bw=0.45, hmax=1.55, size=13, lab_size=14)
        src = fit(T("公开点赞列表复核（2026-11-14）；只反映注册时间，不能证明刷量", 14, MUTED), 6.0)
        note = fit(T(f"原仓库点赞 {DATA['jackrong']['canonical_likes']} · 衍生仓库列表 {lc['heretic']['total']} 条（热榜显示 {DATA['jackrong']['likes']}）", 14, MUTED), 6.0)
        G = VGroup(VGroup(t, st).arrange(DOWN, aligned_edge=LEFT, buff=0.08), sh, mt, vb, src, note).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(G[0]), rt=0.4)
        self.G = G
    def later(self):
        G = self.G
        self.W(self.sub_t("真正冲上榜首"))
        self.P(grow(G[1]), rt=1.0)
        self.W(self.sub_t("七成来自"))
        self.P(FadeIn(G[2]), grow_v(G[3]), FadeIn(G[4]), FadeIn(G[5]), rt=1.2)

class P1b(Base):
    key = "P1b"
    def construct(self):
        self.head("jackrong", "训练与自报评测")
        n1 = node("DeepSeek V4 Pro", 3.1, 0.95, BORDER, 20, "教师 · Max Effect")
        n2 = node("约 25 万条数学 / STEM", 3.2, 0.95, PURPLE, 20, "SFT → 轻度 GSPO")
        n3 = node("Qwen3.5-9B 学生", 3.0, 0.95, HF, 20, "没有编程数据")
        fl = VGroup(n1, n2, n3).arrange(RIGHT, buff=0.55).move_to(UP * 2.35)
        ar = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3) for a, b in zip(fl[:-1], fl[1:])])
        self.P(FadeIn(n1, shift=UP * 0.15), rt=0.5)
        self.P(GrowArrow(ar[0]), FadeIn(n2), GrowArrow(ar[1]), FadeIn(n3), rt=1.0)
        self.W(self.cue(1))
        gsm = DATA["jackrong"]["bench_gsm8k"]
        mmlu = DATA["jackrong"]["bench_mmlu"]
        eff = DATA["jackrong"]["efficiency"]
        left = mini("GSM8K（官方自报，%）", [
            ("本模型 NVFP4", gsm["GSM8K"][0], HF),
            ("教师 V4 Pro", gsm["GSM8K"][1], DIM),
            ("Llama-3.3-70B", gsm["GSM8K"][2], "#3B4452"),
        ], 100, bw=2.15, lw=2.35, size=15, h=0.22, gap=0.07, tsize=17, fmt="{:.2f}")
        mid = mini("MMLU-Pro 均分（抽 1500 题）", [
            ("本模型 9B", mmlu["Average"][0], HF),
            ("Qwen3.5-9B 底座", mmlu["Average"][1], BLUE),
            ("Mythos-distill 9B", mmlu["Average"][2], DIM),
        ], 100, bw=2.15, lw=2.45, size=15, h=0.22, gap=0.07, tsize=17, fmt="{:.2f}")
        right = mini("每道答对题的推理 token", [
            ("本模型", eff["tokens_per_correct"][0], HF),
            ("Qwen3.5-9B", eff["tokens_per_correct"][1], BLUE),
            ("Mythos-distill 9B", eff["tokens_per_correct"][2], DIM),
        ], 5200, bw=2.0, lw=2.35, size=15, h=0.22, gap=0.07, tsize=17, fmt="{:,}")
        row = VGroup(left, mid, right).arrange(RIGHT, buff=0.35, aligned_edge=UP)
        fit(row, 13.0)
        row.move_to([0, -0.15, 0])
        src = fit(T("来源：Jackrong 模型卡（官方自报）。GSM8K 为四次平均，对照分转引自 openai/gsm8k；MMLU-Pro 每个子集抽 500 题，不是完整题库。", 15, MUTED), 13.0)
        src.next_to(row, DOWN, buff=0.22).align_to(row, LEFT)
        self.P(FadeIn(left[0]), grow(left[1]), FadeIn(mid[0]), grow(mid[1]), rt=1.2)
        self.W(self.sub_t("答对每道题"))
        self.P(FadeIn(right[0]), grow(right[1]), FadeIn(src), rt=0.9)
        self.W(self.cue(2))
        ff = DATA["jackrong"]["format_follow"]
        fbars = mini("只输出一个字母的比例（官方自报）", [
            ("本模型", ff["this"]["terse_letter_pct"], HF),
            ("Qwen3.5-9B 底座", ff["Qwen3.5-9B"]["terse_letter_pct"], BLUE),
        ], 100, bw=2.8, lw=2.6, size=16, h=0.24, gap=0.08, tsize=18, fmt="{:.1f}%")
        fbars.next_to(src, DOWN, buff=0.2).align_to(row, LEFT)
        self.P(FadeIn(fbars[0]), grow(fbars[1]), rt=0.8)
        self.W(self.cue(3))
        note = fit(T("Artificial Analysis 尚未收录（2026-11-14）· 编程迁移只是作者的初步观察", 16, ORANGE), 13.0).next_to(fbars, DOWN, buff=0.14).align_to(row, LEFT)
        self.P(FadeIn(note, shift=UP * 0.1), rt=0.5)
        self.finish()

class P2a(IntroScene):
    key = "P2a"; pid = "h3img"
    def right(self):
        b = self.panel(h=5.8)
        im, cap = picture(A + "h3_hero.png", width=6.05, credit="官方展示：文生图多风格样张（已缩小）", csize=15)
        im.move_to(b.get_center() + UP * 0.2)
        src = fit(T("来源：MiniMaxAI/MiniMax-H3-Image 模型卡 assets/showcase_hero.jpg", 13, MUTED), 6.0)
        src.next_to(cap, DOWN, buff=0.06)
        cap.next_to(im, DOWN, buff=0.1)
        self.P(FadeIn(b), FadeIn(im), FadeIn(cap), FadeIn(src), rt=0.6)
        self.hero = (im, cap, src, b)
    def later(self):
        self.W(self.sub_t("官方示例里"))
        im, cap, src, b = self.hero
        self.P(FadeOut(im), FadeOut(cap), FadeOut(src), rt=0.3)
        g1, c1 = picture(A + "h3_edit_map.png", width=6.05, height=2.35, credit="改图：游戏地图 → 第一人称场景（官方）", csize=15)
        g2, c2 = picture(A + "h3_edit_multi.png", width=6.05, height=2.35, credit="改图：空房 + 九件家具 → 一张客厅（官方）", csize=15)
        col = Group(Group(g1, c1).arrange(DOWN, buff=0.06), Group(g2, c2).arrange(DOWN, buff=0.06)).arrange(DOWN, buff=0.16)
        col.move_to(b.get_center())
        self.P(FadeIn(col), rt=0.7)
        self.W(self.cue(2))
        tip = fit(chip("最多 16 张参考图 · 官方提供提示词扩写（PE / Context-IR）", color=HF, size=18), 6.2)
        # 替换左侧备注，避免芯片落入底部字幕安全区
        tip.align_to(self.nt, LEFT).align_to(self.nt, UP)
        if tip.get_bottom()[1] < -3.18:
            tip.shift(UP * (-3.18 - tip.get_bottom()[1]))
        self.P(FadeOut(self.nt), FadeIn(tip, shift=UP * 0.05), rt=0.5)

class P2b(Base):
    key = "P2b"
    def construct(self):
        self.head("h3img", "结构与第三方评测")
        n_txt = node("H3 文本编码器", 2.7, 0.95, BORDER, 18, "Qwen3-VL，读第 50 层")
        n_ref = node("参考图 VAE", 2.3, 0.95, PURPLE, 18, "最多 16 张")
        n_dit = node("单流 DiT 33.1B", 3.2, 1.05, HF, 20, "50 层 · 6 步 · 不用 CFG")
        n_out = node("图像 VAE 解码", 2.6, 0.95, GREEN, 18, "直接约 16MP")
        top = VGroup(n_txt, n_ref).arrange(RIGHT, buff=0.4).move_to(UP * 2.15)
        n_dit.move_to(UP * 0.85)
        n_out.move_to(DOWN * 0.45)
        a1 = Arrow(n_txt.get_bottom(), n_dit.get_top() + LEFT * 0.8, buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        a2 = Arrow(n_ref.get_bottom(), n_dit.get_top() + RIGHT * 0.8, buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        a3 = Arrow(n_dit.get_bottom(), n_out.get_top(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        srcd = fit(T("结构示意 · 来源：MiniMax-H3-Image 模型卡", 14, MUTED), 8.0).next_to(n_out, DOWN, buff=0.12)
        left = VGroup(top, n_dit, n_out)
        # shift group to left
        grp = VGroup(n_txt, n_ref, n_dit, n_out, a1, a2, a3, srcd)
        grp.shift(LEFT * 3.15)
        self.P(FadeIn(n_txt), FadeIn(n_ref), rt=0.5)
        self.P(GrowArrow(a1), GrowArrow(a2), FadeIn(n_dit), rt=0.7)
        self.P(GrowArrow(a3), FadeIn(n_out), FadeIn(srcd), rt=0.5)
        self.W(self.cue(1))
        aa = DATA["h3img"]["third_party"]["Artificial Analysis"]
        ed, t2i = aa["editing"]["H3-Image"], aa["t2i"]["H3-Image"]
        s1 = stat_card("开源第 1", "图像编辑 Elo 1137", 2.35, 1.45, HF, 28, 16, f"全榜第 {ed['rank_overall']} · {ed['appearances']:,} 次对比")
        s2 = stat_card("开源第 1", "文生图 Elo 1066", 2.35, 1.45, GREEN, 28, 16, f"全榜第 {t2i['rank_overall']} · {t2i['appearances']:,} 次对比")
        ss = VGroup(s1, s2).arrange(RIGHT, buff=0.15).move_to([3.55, 1.85, 0])
        at = fit(T("Artificial Analysis 图像竞技场（第三方，2026-11-14）", 16, MUTED), 5.5).next_to(ss, UP, buff=0.15)
        note = fit(T("Highspeed 是 API 版本：文生图 Elo 1072、编辑 1134", 15, MUTED), 5.5).next_to(ss, DOWN, buff=0.12)
        self.P(FadeIn(at), LaggedStart(FadeIn(s1, shift=UP * 0.12), FadeIn(s2, shift=UP * 0.12), lag_ratio=0.25), FadeIn(note), rt=1.0)
        self.W(self.sub_t("这是人类两两投票"))
        vot = fit(T("Elo 来自两两偏好投票，不是指令执行正确率", 16, YELLOW), 5.5).next_to(note, DOWN, buff=0.12)
        self.P(FadeIn(vot, shift=UP * 0.08), rt=0.5)
        self.W(self.cue(3))
        lic = card_rows("社区许可要点", [
            ("适用地区不包括欧盟、英国、韩国和美国", ORANGE),
            ("年收入超过 100 万美元，或对外提供托管服务：需另行书面授权", ORANGE),
            ("商用界面需标明 MiniMax-H3-Image", None),
        ], 6.6, YELLOW, 17, 20)
        lic.move_to([3.55, -1.7, 0])
        src = fit(T("来源：MiniMax-H3-Image Community License（2026-11-10）", 14, MUTED), 6.4).next_to(lic, DOWN, buff=0.1)
        self.P(FadeIn(lic, shift=UP * 0.1), FadeIn(src), rt=0.6)
        self.finish()

class P3a(IntroScene):
    key = "P3a"; pid = "ltx"
    def right(self):
        lc = DATA["ltx"]["likes_check"]
        b = self.panel()
        t = T("点赞账号是什么时候注册的？", 22, FG, weight=BOLD)
        st = fit(T("占比 = 2026 年 8 月及以后注册的账号 / 全部点赞", 15, MUTED), 6.0)
        sh = hbars([
            ("LTX-2.5", lc["LTX-2.5"]["share_new"], ORANGE),
            ("H3-Image（对照）", lc["MiniMax-H3-Image"]["share_new"], DIM),
            ("Arete-27B（对照）", lc["Arete-27B"]["share_new"], GREEN),
        ], 70, bw=2.7, lw=2.5, size=16, h=0.3, gap=0.1, fmt="{:.1f}%")
        mt = T("新账号点赞数（按注册月份）", 17, MUTED)
        mons = ["2026-08", "2026-09", "2026-10", "2026-11"]
        vb = vbars([(m[5:] + " 月" if m != "2026-11" else "11 月 1–14 日",
                     [lc["LTX-2.5"]["by_month"][m], lc["MiniMax-H3-Image"]["by_month"][m]]) for m in mons],
                   [ORANGE, DIM], 2800, gw=1.35, bw=0.28, hmax=1.35, size=12, lab_size=13)
        lg = legend([("LTX-2.5", ORANGE), ("H3-Image", DIM)], 14)
        src = fit(T("公开点赞列表复核（2026-11-14）；只反映注册时间，不能证明刷量", 14, MUTED), 6.0)
        prev = lc["share_new_w45"]
        dc = fit(chip(f"上周同口径 {prev}% → 本周 {lc['LTX-2.5']['share_new']}%", color=BORDER, size=16), 6.0)
        G = VGroup(VGroup(t, st).arrange(DOWN, aligned_edge=LEFT, buff=0.08), sh, VGroup(mt, lg).arrange(RIGHT, buff=0.3), vb, src, dc).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(G[0]), rt=0.4)
        self.G = G
    def later(self):
        G = self.G
        self.W(self.sub_t("将近六成"))
        self.P(grow(G[1]), rt=0.9)
        self.P(FadeIn(G[2]), grow_v(G[3]), FadeIn(G[4]), rt=1.1)
        self.W(self.sub_t("上周到这周"))
        self.P(FadeIn(G[5], shift=UP * 0.08), rt=0.45)
        self.W(self.sub_t("下载量倒是"))
        dl = fit(T(f"30 天下载：上周 {DATA['ltx']['likes_check']['downloads_w45']:,} → 本周 {DATA['ltx']['downloads_30d']:,}", 16, FG), 6.0)
        dl.next_to(G[5], DOWN, buff=0.12).align_to(G[5], LEFT)
        self.P(FadeIn(dl), rt=0.4)

class P3b(Base):
    key = "P3b"
    def construct(self):
        self.head("ltx", "设计与第三方评测")
        txt = node("文本编码器", 2.6, 0.95, BORDER, 19, "定制 Gemma 4 12B").move_to([-5.3, 1.55, 0])
        vs = node("视频流", 3.6, 1.1, HF, 22, "容量大（LTX-2：14B）").move_to([-1.1, 2.35, 0])
        au = node("音频流", 2.4, 0.85, PURPLE, 19, "LTX-2：5B").move_to([-1.1, 0.75, 0])
        xa = DoubleArrow(vs.get_bottom(), au.get_top(), buff=0.04, color=GREEN, stroke_width=3, tip_length=0.15)
        xl = T("双向音视频交叉注意力", 15, GREEN).next_to(xa, RIGHT, buff=0.15)
        dec = node("扩散视频解码器", 3.0, 1.1, GREEN, 19, "取代 VAE 重建（2.5 新增）").move_to([4.3, 2.35, 0])
        ad = node("音频 VAE + 声码器", 3.0, 0.85, BORDER, 17).move_to([4.3, 0.75, 0])
        a1 = Arrow(txt.get_right(), vs.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        a1b = Arrow(txt.get_right(), au.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        a2 = Arrow(vs.get_right(), dec.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        a3 = Arrow(au.get_right(), ad.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        srcd = fit(T("结构示意 · 来源：LTX-2 论文 arXiv:2601.03233 与 LTX-2.5 模型卡（2.5 的 DiT 共 22B）", 14, MUTED), 12.0).move_to([0, -0.05, 0])
        self.P(FadeIn(txt), GrowArrow(a1), GrowArrow(a1b), FadeIn(vs), FadeIn(au), rt=0.8)
        self.P(GrowFromCenter(xa), FadeIn(xl), rt=0.5)
        self.P(GrowArrow(a2), FadeIn(dec), GrowArrow(a3), FadeIn(ad), FadeIn(srcd), rt=0.6)
        self.W(self.cue(1))
        aa = DATA["ltx"]["third_party"]["Artificial Analysis Video Arena"]["text-to-video"]
        rows = [
            (f"Wan 3.0（第 {aa['Wan 3.0'][0]}）", aa["Wan 3.0"][1], DIM),
            (f"MiniMax H3 768p（第 {aa['MiniMax H3 (768p)'][0]}）", aa["MiniMax H3 (768p)"][1], GREEN),
            (f"LTX-2.5 Fast（第 {aa['LTX-2.5 Fast'][0]}）", aa["LTX-2.5 Fast"][1], HF),
        ]
        ch = hbars(rows, 1250, bw=3.2, lw=3.4, size=17, h=0.32, gap=0.12, fmt="{:.0f}", base=750)
        at = T("AA 视频竞技场 · 文生视频 Elo", 20, FG, weight=BOLD)
        i2v = DATA['ltx']['third_party']['Artificial Analysis Video Arena']['image-to-video']['LTX-2.5 Fast']
        an = VGroup(
            T("横轴从 750 起 · 2026-11-14 查询", 14, MUTED),
            T("测的是 LTX API 版本", 14, MUTED),
            T(f"图生视频 Fast 第 {i2v[0]}（Elo {i2v[1]:.0f}）", 14, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        left = VGroup(at, ch, an).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        lic = card_rows("LTX-2.x 社区许可", [("年收入 < 1000 万美元：免费商用", GREEN), ("以上：需签付费商业协议", ORANGE)], 4.7, YELLOW, 16, 18)
        R = VGroup(left, lic).arrange(RIGHT, aligned_edge=DOWN, buff=0.4)
        R.move_to([0, -1.85, 0])
        if R.get_right()[0] > 6.95:
            R.shift(LEFT * (R.get_right()[0] - 6.95))
        if R.get_left()[0] < -6.95:
            R.shift(RIGHT * (-6.95 - R.get_left()[0]))
        if R.get_top()[1] > -0.28:
            R.shift(DOWN * (R.get_top()[1] + 0.35))
        self.P(FadeIn(at), grow(ch), FadeIn(an), rt=1.2)
        self.W(self.cue(2))
        self.P(FadeIn(lic, shift=UP * 0.1), rt=0.5)
        self.finish()

class P4a(IntroScene):
    key = "P4a"; pid = "qwen"
    def right(self):
        b = self.panel()
        t = T("层结构示意（64 层）", 22, FG, weight=BOLD)
        # 16 repeats of 3 DeltaNet + 1 Gated Attn
        cells = VGroup()
        for i in range(16):
            trio = VGroup(*[Rectangle(width=0.16, height=0.7, stroke_width=0).set_fill(BLUE, 1) for _ in range(3)]).arrange(RIGHT, buff=0.04)
            att = Rectangle(width=0.22, height=0.7, stroke_width=0).set_fill(ORANGE, 1)
            blk = VGroup(trio, att).arrange(RIGHT, buff=0.06)
            cells.add(blk)
        cells.arrange_in_grid(4, 4, buff=(0.18, 0.18))
        fit(cells, 5.9)
        lg = VGroup(*[VGroup(Square(0.22).set_fill(c, 1).set_stroke(width=0), T(n, 16, FG)).arrange(RIGHT, buff=0.1)
                      for n, c in [("Gated DeltaNet × 48", BLUE), ("Gated Attention × 16", ORANGE)]]).arrange(RIGHT, buff=0.35)
        facts = VGroup(*[T(s, 16, MUTED) for s in [
            "27B 稠密 · hidden 5120 · 原生 262,144 上下文，可到 1M",
            "默认开思考，可按请求关闭",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        src = fit(T("来源：Qwen/Qwen3.8-27B 模型卡", 14, MUTED), 5.9)
        G = VGroup(t, cells, lg, facts, src).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(t), rt=0.4)
        self.P(LaggedStart(*[FadeIn(c, scale=0.8) for c in cells], lag_ratio=0.05), FadeIn(lg), FadeIn(src), rt=1.2)
        self.facts, self.lg, self.src_p = facts, lg, src
    def later(self):
        self.W(self.sub_t("原生就能看图"))
        self.P(FadeIn(self.facts, shift=UP * 0.1), rt=0.5)
        self.W(self.cue(2))
        ctx = VGroup(
            stat_card("262K", "原生上下文", 2.15, 1.05, GREEN, 30, 16),
            stat_card("1M", "官方称可扩展至", 2.15, 1.05, BLUE, 30, 16),
        ).arrange(RIGHT, buff=0.15)
        self.P(FadeOut(self.facts), FadeOut(self.src_p), rt=0.35)
        ctx.next_to(self.lg, DOWN, buff=0.22).align_to(self.lg, LEFT)
        nsrc = fit(T("来源：Qwen/Qwen3.8-27B 模型卡", 14, MUTED), 5.9).next_to(ctx, DOWN, buff=0.12).align_to(ctx, LEFT)
        self.P(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in ctx], lag_ratio=0.2), FadeIn(nsrc), rt=0.7)

class P4b(Base):
    key = "P4b"
    def construct(self):
        self.head("qwen", "评测", GREEN)
        bt = DATA["qwen"]["bench_text"]
        bv = DATA["qwen"]["bench_vl"]
        cols = [("Qwen3.8-27B", HF, 0), ("Qwen3.6-27B", DIM, 1), ("Opus4.6 Max", PURPLE, 4)]
        lg = legend([(n, c) for n, c, _ in cols], 16)
        def mk(tab, k, lab, mx=100):
            rows = []
            for n, c, i in cols:
                v = tab[k][i]
                rows.append((" ", v, c if v is not None else DIM))
            return mini(lab, rows, mx, bw=2.2, lw=0.15, size=14, h=0.16, gap=0.04, tsize=16, fmt="{:g}")
        g1 = mk(bt, "Terminal Bench 2.1", "Terminal Bench 2.1")
        g2 = mk(bt, "SWE-bench Pro", "SWE-bench Pro")
        g3 = mk(bv, "OSWorld-Verified", "OSWorld-Verified")
        g4 = mk(bt, "CoWorkBench", "CoWorkBench（自建）")
        grid = VGroup(VGroup(g1, g2).arrange(RIGHT, buff=0.55, aligned_edge=UP),
                      VGroup(g3, g4).arrange(RIGHT, buff=0.55, aligned_edge=UP)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        tt = T("官方对比（自报）", 21, FG, weight=BOLD)
        src = fit(T("来源：Qwen3.8-27B 模型卡。SWE-bench Pro 等用 Claude Code 工具链复测；CoWorkBench 为通义自建。", 14, MUTED), 7.2)
        L = VGroup(VGroup(tt, lg).arrange(DOWN, aligned_edge=LEFT, buff=0.1), grid, src).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        L.move_to([-3.15, 0.15, 0])
        self.P(FadeIn(tt), FadeIn(lg), FadeIn(src), rt=0.5)
        self.P(*[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.08)) for m in (g1, g2, g3, g4)], rt=1.3)
        self.W(self.cue(2))
        aa = DATA["qwen"]["third_party"]["Artificial Analysis"]
        s1 = stat_card("20", "智能指数 v5.0.1（xhigh）", 2.3, 1.4, HF, 36, 16, f"同尺寸开源中位数 {aa['comparable_open_median']}")
        s2 = stat_card(f"{aa['time_per_task_min']['xhigh']:g} 分", "单任务耗时", 2.15, 1.4, ORANGE, 30, 16, f"同级中位数 {aa['time_per_task_min']['median_comparable']} 分")
        s3 = stat_card(f"${aa['cost_per_task_usd']:.2f}", "单任务成本", 2.15, 1.4, ORANGE, 30, 16, "入 $0.50 / 出 $3.00（每百万）")
        ss = VGroup(s1, s2, s3).arrange(DOWN, buff=0.12).move_to([4.15, 0.35, 0])
        at = fit(T("Artificial Analysis（第三方，2026-11-14，Alibaba API）", 15, MUTED), 5.2).next_to(ss, DOWN, buff=0.12)
        vb = fit(T("指数评测输出 1.28 亿 token，同级中位数 0.78 亿（更冗长）", 14, MUTED), 5.2).next_to(at, DOWN, buff=0.08)
        self.P(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.12) for s in ss], lag_ratio=0.2), FadeIn(at), FadeIn(vb), rt=1.0)
        self.finish()

class P5a(IntroScene):
    key = "P5a"; pid = "arete"
    def right(self):
        b = self.panel()
        t = T("七个训练主题", 22, FG, weight=BOLD)
        cats = DATA["arete"]["facts"]["categories"]
        chips = VGroup(*[chip(c, color=PURPLE, size=18) for c in cats]).arrange_in_grid(4, 2, buff=(0.15, 0.15))
        fit(chips, 5.9)
        rows = card_rows("后训练设置", [
            ("只做监督微调，没有 RL、没有改结构", None),
            ("教师模型：Inkling（开源）", None),
            ("约 2 万条提示 → 28,886 条样本", None),
            ("两轮共约 52.8M token，64k 上下文", None),
            ("视觉编码器冻结，数据只有文本", MUTED),
        ], 6.05, PURPLE, 17, 20)
        src = fit(T("来源：Arete-27B 模型卡与 Nous 训练数据画像页", 14, MUTED), 5.9)
        G = VGroup(t, chips, rows, src).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(t), LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in chips], lag_ratio=0.08), rt=0.8)
        self.rest = VGroup(rows, src)
    def later(self):
        self.W(self.sub_t("数据量不大"))
        self.P(FadeIn(self.rest, shift=UP * 0.1), rt=0.6)
        self.W(self.cue(2))
        self.P(Indicate(self.rest[0], color=PURPLE, scale_factor=1.03), rt=0.6)

class P5b(Base):
    key = "P5b"
    def construct(self):
        self.head("arete", "自报评测与社区讨论", GREEN)
        bp = DATA["arete"]["bench_prop"]
        bc = DATA["arete"]["bench_cap"]
        # fact means
        fact = mini("事实分（0–5，官方自报）", [
            ("Inkling 教师", bp["fact_mean"][2], DIM),
            ("Mistral Large 4", bp["fact_mean"][3], "#3B4452"),
            ("Arete-27B", bp["fact_mean"][0], HF),
            ("Qwen3.8-27B 底座", bp["fact_mean"][1], ORANGE),
        ], 5, bw=3.0, lw=2.6, size=16, h=0.26, gap=0.08, tsize=18, fmt="{:.2f}")
        prop = mini("被标为宣传口径的占比", [
            ("Inkling 教师", bp["propaganda_pct"][2], DIM),
            ("Arete-27B", bp["propaganda_pct"][0], HF),
            ("Qwen3.8-27B 底座", bp["propaganda_pct"][1], ORANGE),
        ], 25, bw=3.0, lw=2.6, size=16, h=0.26, gap=0.08, tsize=18, fmt="{:.1f}%")
        caps = mini("能力对照（作者自测）", [
            ("Hermes Bench 底座 / Arete", None, DIM),
        ], 1)  # placeholder unused
        cap_bars = VGroup(
            mini("Hermes Bench", [("Qwen3.8-27B", bc["Hermes Bench"][0], ORANGE), ("Arete-27B", bc["Hermes Bench"][1], HF)],
                 80, bw=2.4, lw=2.3, size=15, h=0.22, gap=0.07, tsize=16, fmt="{:.2f}"),
            mini("Terminal-Bench 2.1", [("Qwen3.8-27B", bc["Terminal-Bench-2.1"][0], ORANGE), ("Arete-27B", bc["Terminal-Bench-2.1"][1], HF)],
                 80, bw=2.4, lw=2.3, size=15, h=0.22, gap=0.07, tsize=16, fmt="{:g}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        left = VGroup(fact, prop).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([-3.5, 0.2, 0])
        right = cap_bars.move_to([3.6, 1.0, 0])
        src = VGroup(
            fit(T("来源：Arete-27B 模型卡。803 题 × 5 次；裁判为 Grok 4.7。", 14, MUTED), 6.3),
            fit(T("Arete / 底座为 temperature 0，其余对照为 0.6，不完全可比。", 14, MUTED), 6.3),
            fit(T("作者不把 Terminal-Bench 的看似提升视为自己的成绩。", 14, MUTED), 6.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        src.next_to(left, DOWN, buff=0.28).align_to(left, LEFT)
        if src.get_bottom()[1] < -3.18:
            src.shift(UP * (-3.18 - src.get_bottom()[1]))
        self.P(FadeIn(fact[0]), grow(fact[1]), FadeIn(prop[0]), grow(prop[1]), rt=1.3)
        self.W(self.sub_t("通用和智能体"))
        self.P(FadeIn(right), rt=0.7)
        self.P(FadeIn(src), rt=0.4)
        self.W(self.cue(1))
        fo = DATA["arete"]["bench_prop"]["freedom_of_expression"]
        fo_card = mini("言论自由一类（官方自报）", [
            ("底座宣传口径", fo["propaganda_pct"][0], ORANGE),
            ("Arete 宣传口径", fo["propaganda_pct"][1], HF),
        ], 70, bw=2.5, lw=2.4, size=15, h=0.22, gap=0.07, tsize=16, fmt="{:g}%")
        fo_card.next_to(right, DOWN, buff=0.25).align_to(right, LEFT)
        self.P(FadeIn(fo_card[0]), grow(fo_card[1]), rt=0.8)
        self.W(self.cue(2))
        q1 = quote("有人把它看成价值观的可选项，也有人质疑“西方价值观”该怎么定义。", 6.0, "讨论区多方观点 · 概述（非原话）", ORANGE, 17)
        q2 = quote("有用户对比底座后认为，在提问不存在的事物时可能有副作用。", 6.0, "讨论 #23 · 概述，未独立核实", YELLOW, 17)
        qs = VGroup(q1, q2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        qs.next_to(fo_card, DOWN, buff=0.18).align_to(fo_card, LEFT)
        if qs.get_right()[0] > 6.95:
            qs.shift(LEFT * (qs.get_right()[0] - 6.95))
        if qs.get_bottom()[1] < -3.18:
            qs.shift(UP * (-3.18 - qs.get_bottom()[1]))
        self.P(FadeIn(q1, shift=UP * 0.1), FadeIn(q2, shift=UP * 0.1), rt=0.7)
        self.W(self.cue(3))
        self.P(Indicate(src, color=YELLOW, scale_factor=1.02), rt=0.5)
        self.finish()

class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        t1 = T("看热度，还得回到仓库本身", 40, FG, weight=BOLD)
        t2 = T("和第三方评测", 40, HF, weight=BOLD)
        title = VGroup(t1, t2).arrange(DOWN, buff=0.15).move_to(UP * 2.2)
        rows = Group()
        notes = [
            ("#1  Jackrong", "9B 蒸馏登顶，靠的是衍生仓库的点赞"),
            ("#2  MiniMax H3-Image", "开源改图、文生图竞技场目前都排第一"),
            ("#3  LTX-2.5", "还在榜上，点赞结构仍然异常"),
            ("#4  Qwen3.8-27B", "27B 稠密多模态，官方模型回到前排"),
            ("#5  Arete-27B", "一次小规模的价值对齐实验"),
        ]
        for i, (a, b) in enumerate(notes):
            pid = PIDS[i]
            av = avatar(pid, 0.42)
            lab = VGroup(fit(T(a, 22, FG, weight=BOLD), 4.2), fit(T(b, 18, MUTED), 7.5)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            rows.add(Group(av, lab).arrange(RIGHT, buff=0.2, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(title, DOWN, buff=0.45)
        self.P(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.12), rt=1.6)
        self.W(self.cue(1))
        self.P(FadeIn(title, shift=UP * 0.15), rt=0.7)
        bye = T("下周见。", 28, MUTED).next_to(rows, DOWN, buff=0.4)
        self.W(self.cue(2) if len(self.tm["cues"]) > 2 else self.tm["total"] - 2)
        self.P(FadeIn(bye), rt=0.5)
        self.finish()
