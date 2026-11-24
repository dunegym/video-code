"""Hugging Face 本周热门 Top 5（2026 第 47 周）—— Manim CE 场景。时间轴由 timing.json（MiniMax 词级时间戳）驱动；
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
    "inkling": dict(chips=["image-text-to-text", "Apache-2.0", "发布于 2026-11-20"], what="面向本地部署的循环 MoE 多模态模型", note="已合并官方 GGUF 量化仓库 · 点赞账号注册时间正常"),
    "haru": dict(chips=["audio-to-audio", "Apache-2.0", "研究用基座"], what="全双工语音对话：听和说同时进行", note="热榜 5,711 点赞，公开列表只有 801 条"),
    "pi": dict(chips=["LoRA / AsyncGRPO", "Apache-2.0", "适配 pi 编程代理"], what="在 Qwen3.8-27B 上做强化学习 LoRA", note="第三方适配器，没有并入官方底座"),
    "sentinel": dict(chips=["社区 LoRA 合集", "无模型卡", "创建于 2026-08-06"], what="面向 MiniMax H3 视频的社区微调打包", note="近 30 天下载为 0 · 不是官方发布"),
    "ltx": dict(chips=["image-to-video", "LTX-2.x 社区许可", "创建于 2026-07-23"], what="音视频联合生成 · 22B DiT", note="上周原榜 #3 → 本周 #5 · 点赞结构仍偏新"),
}
PIDS = ["inkling", "haru", "pi", "sentinel", "ltx"]

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
        date = chip("2026 年第 47 周 · 11 月 21 日", color=HF, size=24).next_to(title, DOWN, buff=0.4)
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
    key = "P1a"; pid = "inkling"
    def right(self):
        lc = DATA["inkling"]["likes_check"]
        b = self.panel()
        t = T("点赞账号是什么时候注册的？", 22, FG, weight=BOLD)
        st = fit(T("2026 年 8 月及以后注册占比 · 对照为同期热门仓库", 15, MUTED), 6.0)
        sh = hbars([
            ("Inkling 2 Mini", lc["listed"]["share_new"], GREEN),
            ("Qwen3.8-27B（对照）", lc["controls"]["Qwen3.8-27B"], BLUE),
            ("Hy4-flash（对照）", lc["controls"]["Hy4-flash"], PURPLE),
            ("Inkling 2 Small（对照）", lc["controls"]["Inkling-2-Small"], DIM),
        ], 100, bw=2.6, lw=2.6, size=16, h=0.28, gap=0.12, fmt="{:.1f}%")
        src = fit(T("公开点赞列表复核（2026-11-21）；只反映注册时间，不能证明刷量", 14, MUTED), 6.0)
        note = fit(T(f"列表 {lc['listed']['total']} 条（热榜显示 {lc['displayed_likes']}）· 已合并 unsloth GGUF", 14, MUTED), 6.0)
        G = VGroup(VGroup(t, st).arrange(DOWN, aligned_edge=LEFT, buff=0.08), sh, src, note).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(G[0]), rt=0.4)
        self.G = G
    def later(self):
        G = self.G
        self.W(self.sub_t("点赞账号的注册时间"))
        self.P(grow(G[1]), FadeIn(G[2]), FadeIn(G[3]), rt=1.2)


class P1b(Base):
    key = "P1b"
    def construct(self):
        self.head("inkling", "结构与评测")
        n0 = node("层 0–5", 1.7, 0.85, BLUE, 18, "一遍")
        n1 = node("层 6–17 循环 ×3", 3.3, 0.85, HF, 18, "共享权重")
        n2 = node("层 18–23", 1.7, 0.85, BLUE, 18, "一遍")
        fl = VGroup(n0, n1, n2).arrange(RIGHT, buff=0.35).move_to(UP * 2.25)
        arrs = VGroup(*[Arrow(fl[i].get_right(), fl[i+1].get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.25) for i in range(2)])
        cap = fit(T("24 层权重 · 每 token 48 次层计算 · 每层 8 / 128 专家 · 有效激活约 5.4B", 16, MUTED), 12.5)
        cap.next_to(fl, DOWN, buff=0.18)
        self.P(LaggedStart(FadeIn(n0), FadeIn(n1), FadeIn(n2), lag_ratio=0.2), Create(arrs), rt=1.0)
        self.P(FadeIn(cap), rt=0.4)

        sr = DATA["inkling"]["self_reported"]["selected"]
        def tcell(s, w, size, color, weight=NORMAL, right=False):
            r = Rectangle(width=w, height=0.38, stroke_width=0, fill_opacity=0)
            tx = fit(T(s, size, color, weight=weight), w)
            if right:
                tx.next_to(r.get_right(), LEFT, buff=0)
            else:
                tx.next_to(r.get_left(), RIGHT, buff=0)
            tx.set_y(r.get_y())
            return VGroup(r, tx)
        def trow(lab, a, b, head=False):
            c = MUTED if head else FG
            w = BOLD if head else NORMAL
            return VGroup(
                tcell(lab, 3.5, 17, c, w),
                tcell(a, 1.6, 17, MUTED if head else HF, BOLD if not head else NORMAL, right=True),
                tcell(b, 2.1, 17, MUTED if head else BLUE, BOLD if not head else NORMAL, right=True),
            ).arrange(RIGHT, buff=0.2)
        tab = VGroup(
            trow("基准（作者自报）", "Inkling", "Qwen3.8-27B", head=True),
            trow("SWE-bench Pro Hard", "77.9%", "73.8%"),
            trow("Terminal Bench 2.1", "71.6%", "73.0%"),
            trow("BrowseComp", "79.0%", "61.6%"),
            trow("MMMU Pro", "74.9%", "76.3%"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        # light separators
        line = Line(ORIGIN, RIGHT * 6.8, color=BORDER, stroke_width=1)
        src1 = fit(T("来源：Inkling 2 Mini 模型卡评测表（作者自报，评测设置不同）", 13, MUTED), 6.8)
        leftg = VGroup(tab, src1).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(LEFT * 3.15 + DOWN * 1.15)

        aa = DATA["inkling"]["third_party"]["Artificial Analysis"]
        cards = VGroup(
            stat_card("20", "智能指数 v5", 2.55, 1.35, HF, 40, 16, "同尺寸中位数 10"),
            stat_card("9.0 分", "每任务耗时", 2.55, 1.35, GREEN, 34, 16, "中位数 9.2 分"),
            stat_card("$0.59", "每任务费用", 2.55, 1.35, ORANGE, 34, 16, "输入 $0.15 / 输出 $0.50"),
        ).arrange(DOWN, buff=0.16).move_to(RIGHT * 3.4 + DOWN * 1.0)
        src2 = fit(T("Artificial Analysis，2026-11-21；输出 161M token，中位数 85.7M，偏长", 13, MUTED), 6.0).next_to(cards, DOWN, buff=0.14)

        self.W(self.sub_t("官方自报"))
        self.P(FadeIn(leftg), rt=1.1)
        self.W(self.sub_t("第三方智能指数"))
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.15), FadeIn(src2), rt=1.1)
        self.finish()


class P2a(IntroScene):
    key = "P2a"; pid = "haru"
    def right(self):
        lc = DATA["haru"]["likes_check"]
        b = self.panel()
        t = T("热榜点赞和公开列表对不上", 22, FG, weight=BOLD)
        st = fit(T("模型页显示 5.71k，登录后拉取 /likers 仍是 801 条", 15, MUTED), 6.0)
        # two big numbers
        left = stat_card("5,711", "热榜 / 模型页点赞", 2.85, 1.55, ORANGE, 42, 16)
        right = stat_card("801", "公开点赞列表", 2.85, 1.55, BLUE, 42, 16)
        pair = VGroup(left, right).arrange(RIGHT, buff=0.2)
        sh = hbars([
            ("列表内 · 8 月后注册", lc["listed"]["share_new"], GREEN),
            ("Inkling 2 Mini（对照）", lc["controls"]["Inkling-2-Mini"], BLUE),
            ("Qwen3.8-27B（对照）", lc["controls"]["Qwen3.8-27B"], DIM),
        ], 100, bw=2.5, lw=2.4, size=15, h=0.26, gap=0.1, fmt="{:.1f}%")
        src = fit(T("公开点赞列表复核（2026-11-21）；列表内账号注册时间并不异常", 14, MUTED), 6.0)
        G = VGroup(VGroup(t, st).arrange(DOWN, aligned_edge=LEFT, buff=0.08), pair, sh, src).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(G[0]), rt=0.4)
        self.G = G
    def later(self):
        G = self.G
        self.W(self.sub_t("五千多个点赞"))
        self.P(FadeIn(G[1], shift=UP * 0.1), rt=0.8)
        self.W(self.sub_t("注册时间看起来并不异常"))
        self.P(grow(G[2]), FadeIn(G[3]), rt=1.0)


class P2b(Base):
    key = "P2b"
    def construct(self):
        self.head("haru", "结构和训练")
        s1 = node("用户音频", 2.2, 0.9, BLUE, 18, "24 kHz 潜变量")
        s2 = node("模型音频", 2.2, 0.9, PURPLE, 18, "上一帧")
        s3 = node("模型文本", 2.2, 0.9, GREEN, 18, "上一 token")
        streams = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.35).move_to(UP * 2.2)
        plus = T("三路相加，每 133 ms 一帧", 18, MUTED)
        lm = node("Qwen3.5-4B 骨干", 3.4, 0.95, HF, 20, "32 层 · hidden 2560")
        head = node("MeanFlow 头 · 1 步", 3.0, 0.95, ORANGE, 18, "连续音频，无离散码")
        mid = VGroup(lm, head).arrange(RIGHT, buff=0.4)
        plus.next_to(streams, DOWN, buff=0.18)
        mid.next_to(plus, DOWN, buff=0.22)
        self.P(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in streams], lag_ratio=0.15), rt=0.9)
        self.P(FadeIn(plus), FadeIn(mid), rt=0.7)

        hours = VGroup(
            stat_card("4,000 万 h", "真实语音预训练", 3.3, 1.4, BLUE, 32, 16, "160+ 语言，主攻 9 语"),
            stat_card("1,300 万 h", "分离后的全双工对话", 3.3, 1.4, PURPLE, 32, 16, "样本最长 60 分钟"),
            stat_card("65 ms", "Mac 端到端延迟", 3.3, 1.4, GREEN, 36, 16, "作者自测 · M1 Max int8"),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 1.55)
        src = fit(T("来源：Haru-4B 技术博客 / 模型卡（官方自报，2026-11-13）；不含最多 133 ms 的帧填充", 14, MUTED), 13.0)
        src.next_to(hours, DOWN, buff=0.16)
        self.W(self.sub_t("四千万小时"))
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in hours], lag_ratio=0.12), FadeIn(src), rt=1.2)
        self.finish()


class P3a(IntroScene):
    key = "P3a"; pid = "pi"
    def right(self):
        b = self.panel()
        t = T("关掉思考，接近最高思考强度", 20, FG, weight=BOLD)
        st = fit(T("作者自报 · 全部在 pi 框架下，不能直接和 Qwen 模型卡比", 14, MUTED), 6.0)
        tb = DATA["pi"]["self_reported"]["table"]
        # grouped bars: 4 series would be tight; show base / adapter / base xhigh for two benches
        vb = vbars([
            ("SWE-bench Pro\nHard 51", [tb["SWE-bench Pro (hard 51)"]["base"], tb["SWE-bench Pro (hard 51)"]["adapter"], tb["SWE-bench Pro (hard 51)"]["base_xhigh"]]),
            ("Terminal-Bench\n2.1", [tb["Terminal-Bench 2.1"]["base"], tb["Terminal-Bench 2.1"]["adapter"], tb["Terminal-Bench 2.1"]["base_xhigh"]]),
        ], [DIM, HF, BLUE], 80, gw=2.7, bw=0.32, hmax=2.3, size=13, fmt="{:.1f}", lab_size=15, lab_w=2.5)
        leg = legend([("底座，思考关", DIM), ("本适配器，思考关", HF), ("底座，xhigh 思考", BLUE)], 14)
        src = fit(T("来源：模型卡 Results 表（官方自报，2026-11）", 13, MUTED), 6.0)
        G = VGroup(VGroup(t, st).arrange(DOWN, aligned_edge=LEFT, buff=0.08), leg, vb, src).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(G[0]), rt=0.4)
        self.G = G
    def later(self):
        G = self.G
        self.W(self.sub_t("关掉思考时"))
        self.P(FadeIn(G[1]), grow_v(G[2]), FadeIn(G[3]), rt=1.3)


class P3b(Base):
    key = "P3b"
    def construct(self):
        self.head("pi", "自报结果与限度")
        pr = DATA["pi"]["self_reported"]["paired"]
        # paired improvement table as cards + bars
        rows = hbars([
            ("SWE-bench Pro  hard 51", pr["SWE-bench Pro (hard 51)"]["adapter"], HF),
            ("同基准 · 底座", pr["SWE-bench Pro (hard 51)"]["base"], DIM),
            ("Terminal-Bench 2.1", pr["Terminal-Bench 2.1"]["adapter"], BLUE),
            ("同基准 · 底座", pr["Terminal-Bench 2.1"]["base"], DIM),
        ], 80, bw=5.5, lw=3.6, size=18, h=0.32, gap=0.12, fmt="{:.1f}%")
        rows.move_to(UP * 1.15 + LEFT * 0.2)
        note = VGroup(
            fit(T("配对结果：SWE 新解 15 题、丢掉 2 题（p=0.0023）；Terminal 新解 16 题、丢掉 2 题（p=0.0013）", 16, MUTED), 13.0),
            fit(T("相对底座 xhigh 思考，生成 token 大约少到四分之一（SWE 中位 48.8k / 9.4k）", 16, MUTED), 13.0),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(rows, DOWN, buff=0.28)
        src = fit(T("来源：模型卡 Full paired results / Thinking vs no thinking（官方自报）", 14, MUTED), 13.0)
        src.next_to(note, DOWN, buff=0.16)
        self.P(grow(rows), rt=1.1)

        caveats = VGroup(
            chip("不可与官方模型卡直接比", color=ORANGE, size=18),
            chip("部分提升来自更能跑完预算", color=ORANGE, size=18),
            chip("作者已修正两轮早先数字", color=YELLOW, size=18),
            chip("尚无第三方复现", color=RED, size=18),
        ).arrange(RIGHT, buff=0.16).move_to(DOWN * 1.85)
        fit(caveats, 13.2)
        self.W(self.sub_t("不能直接和 Qwen"))
        self.P(FadeIn(note), FadeIn(src), rt=0.8)
        self.W(self.sub_t("修正过两轮"))
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in caveats], lag_ratio=0.15), rt=1.0)
        self.finish()


class P4a(IntroScene):
    key = "P4a"; pid = "sentinel"
    def right(self):
        f = DATA["sentinel"]["facts"]
        b = self.panel()
        t = T("没有模型卡的打包仓库", 22, FG, weight=BOLD)
        st = fit(T("快照文件清单统计，未下载任何权重", 15, MUTED), 6.0)
        cards = VGroup(
            stat_card("404 组", "数字目录 / LoRA 包", 2.85, 1.35, ORANGE, 36, 16),
            stat_card("419 个", "safetensors 文件", 2.85, 1.35, BLUE, 36, 16),
            stat_card("0", "近 30 天下载", 2.85, 1.35, RED, 40, 16),
            stat_card("563", "热榜点赞", 2.85, 1.35, HF, 40, 16),
        )
        cards.arrange_in_grid(2, 2, buff=0.18)
        src = fit(T("列表点赞 564 条，与热榜接近；8 月后注册占 24.3%，与对照接近", 14, MUTED), 6.0)
        G = VGroup(VGroup(t, st).arrange(DOWN, aligned_edge=LEFT, buff=0.08), cards, src).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(G[0]), rt=0.4)
        self.G = G
    def later(self):
        G = self.G
        self.W(self.sub_t("四百多组"))
        self.P(FadeIn(G[1], shift=UP * 0.1), FadeIn(G[2]), rt=1.0)


class P4b(Base):
    key = "P4b"
    def construct(self):
        self.head("sentinel", "它不是官方模型")
        # comparison cards
        a = box(6.0, 3.6)
        b = box(6.0, 3.6)
        ta = T("Sentinel7/h3（本周 #4）", 22, ORANGE, weight=BOLD)
        tb = T("官方 MiniMax 仓库（不是同一项）", 22, BLUE, weight=BOLD)
        la = VGroup(
            fit(T("社区 LoRA 合集，无模型卡、无许可说明", 18, FG), 5.5),
            fit(T("主要面向 MiniMax H3 视频微调", 18, FG), 5.5),
            fit(T("近 30 天下载为 0", 18, FG), 5.5),
            fit(T("同作者还有十几个类似打包仓库", 18, FG), 5.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        lb = VGroup(
            fit(T("MiniMax-H3：官方视频生成模型", 18, FG), 5.5),
            fit(T("MiniMax-H3-Image：官方文生图，上周 #2", 18, FG), 5.5),
            fit(T("本周 H3-Image 已落到原榜第 14", 18, FG), 5.5),
            fit(T("有完整模型卡和社区许可", 18, FG), 5.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        ga = VGroup(ta, la).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(a)
        gb = VGroup(tb, lb).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(b)
        pair = VGroup(VGroup(a, ga), VGroup(b, gb)).arrange(RIGHT, buff=0.3).move_to(UP * 0.45)
        note = fit(T("讨论区有内容投诉和补卡请求，不构成已裁定结论。成片不展示任何样例。", 16, MUTED), 13.0)
        note.next_to(pair, DOWN, buff=0.22)
        src = fit(T("来源：热榜快照文件清单、作者页 /api/models?author=Sentinel7、仓库讨论区", 14, MUTED), 13.0)
        src.next_to(note, DOWN, buff=0.1)
        self.P(FadeIn(pair[0]), rt=0.7)
        self.W(self.sub_t("不能和上周还在榜上"))
        self.P(FadeIn(pair[1]), rt=0.7)
        self.P(FadeIn(note), FadeIn(src), rt=0.5)
        self.finish()


class P5a(IntroScene):
    key = "P5a"; pid = "ltx"
    def right(self):
        lc = DATA["ltx"]["likes_check"]
        wow = DATA["ltx"]["facts"]["wow"]
        b = self.panel()
        t = T("连续三周：新账号占比还在升", 22, FG, weight=BOLD)
        st = fit(T("2026 年 8 月及以后注册占全部点赞账号的比例", 15, MUTED), 6.0)
        sh = hbars([
            ("第 45 周", lc["share_new_w45"], DIM),
            ("第 46 周", lc["share_new_w46"], ORANGE),
            ("第 47 周（本周）", lc["share_new"], RED),
            ("Inkling 2 Mini（对照）", lc["controls"]["Inkling-2-Mini"], GREEN),
            ("Qwen3.8-27B（对照）", lc["controls"]["Qwen3.8-27B"], BLUE),
        ], 100, bw=2.5, lw=2.5, size=15, h=0.24, gap=0.09, fmt="{:.1f}%")
        src = fit(T("公开点赞列表复核；只反映注册时间，不能证明刷量或谁在操作", 14, MUTED), 6.0)
        note = fit(T(f"本周列表 {lc['total']} 条，与热榜 {DATA['ltx']['likes']} 一致；点赞较上周 +{wow['likes']:,}", 14, MUTED), 6.0)
        G = VGroup(VGroup(t, st).arrange(DOWN, aligned_edge=LEFT, buff=0.08), sh, src, note).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(G[0]), rt=0.4)
        self.G = G
    def later(self):
        G = self.G
        self.W(self.sub_t("连续三周复核"))
        self.P(grow(G[1]), FadeIn(G[2]), FadeIn(G[3]), rt=1.2)


class P5b(Base):
    key = "P5b"
    def construct(self):
        self.head("ltx", "模型和第三方竞技场")
        facts = VGroup(
            chip("22B DiT · 音视频联合生成", color=BLUE, size=18),
            chip("2.5 版：一次出多镜头", color=PURPLE, size=18),
            chip("扩散视频解码器", color=GREEN, size=18),
            chip("年收入 < 1000 万美元可免费用", color=ORANGE, size=18),
        ).arrange(RIGHT, buff=0.14).move_to(UP * 2.2)
        fit(facts, 13.4)
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in facts], lag_ratio=0.12), rt=0.8)

        aa = DATA["ltx"]["third_party"]["Artificial Analysis Video Arena"]
        # T2V and I2V ranks
        t2v = aa["t2v"]; i2v = aa["i2v"]
        def board(title, cur, prev, url_note):
            h = T(title, 20, FG, weight=BOLD)
            c1 = stat_card(f"#{cur['rank_overall']}", "本周名次", 2.2, 1.35, ORANGE, 40, 16, f"Elo {cur['elo']:g}")
            c2 = stat_card(f"#{prev['rank_overall']}", "上周名次", 2.2, 1.35, DIM, 40, 16, f"Elo {prev['elo']:g}")
            src = fit(T(url_note, 13, MUTED), 4.8)
            return VGroup(h, VGroup(c1, c2).arrange(RIGHT, buff=0.16), src).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        left = board("文生视频  LTX-2.5 Fast", t2v["LTX-2.5 Fast"], t2v["w46_fast"], "AA-Video-T2V v2.1 · 2026-11-21")
        right = board("图生视频  LTX-2.5 Fast", i2v["LTX-2.5 Fast"], i2v["w46_fast"], "AA-Video-I2V v2.1 · 2026-11-21")
        pair = VGroup(left, right).arrange(RIGHT, buff=0.8).move_to(DOWN * 0.05)
        foot = fit(T("名次 = JSON rank + 1；AA 测的是 API 的 Fast / Pro。文生视频榜首仍是 Wan 3.0（Elo 1175.5）。偏好投票不等于指令执行正确率。", 15, MUTED), 13.2)
        foot.next_to(pair, DOWN, buff=0.22)
        self.W(self.sub_t("第三方视频竞技场"))
        self.P(FadeIn(pair), FadeIn(foot), rt=1.0)
        self.finish()


class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        t1 = T("看热度，还得回到仓库本身", 40, FG, weight=BOLD)
        t2 = T("和第三方评测", 40, HF, weight=BOLD)
        title = VGroup(t1, t2).arrange(DOWN, buff=0.15).move_to(UP * 2.55)
        notes = [
            ("#1  Inkling 2 Mini", "本地循环 MoE，第三方智能指数 20"),
            ("#2  Haru-4B", "全双工语音，点赞数字和列表对不上"),
            ("#3  Qwen3.8-27B-pi-adapted", "给编程代理用的强化学习 LoRA"),
            ("#4  Sentinel7/h3", "没有模型卡、下载为零的社区合集"),
            ("#5  LTX-2.5", "还在榜上，点赞结构仍然偏新"),
        ]
        rows = Group()
        for i, (a, b) in enumerate(notes):
            pid = PIDS[i]
            av = avatar(pid, 0.42)
            lab = VGroup(fit(T(a, 22, FG, weight=BOLD), 5.6), fit(T(b, 18, MUTED), 8.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            rows.add(Group(av, lab).arrange(RIGHT, buff=0.2, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(title, DOWN, buff=0.28)
        self.P(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.12), rt=1.6)
        self.W(self.cue(2))
        self.P(FadeIn(title, shift=UP * 0.15), rt=0.7)
        bye = T("下周见。", 28, MUTED).next_to(rows, DOWN, buff=0.18)
        self.W(self.cue(3) if len(self.tm["cues"]) > 3 else self.tm["total"] - 2)
        self.P(FadeIn(bye), rt=0.5)
        self.finish()
