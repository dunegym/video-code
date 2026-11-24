"""Hugging Face 本周热门 Top 5 —— Manim CE 场景。时间轴由 timing.json（TTS 词边界实测）驱动。"""
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
    "nanbeige": dict(chips=["text-generation", "Apache-2.0", "上传于 2026-10-24"], what="以“教师智能体”为目标的 33B 稠密模型", note="BOSS直聘 / 看准科技旗下南北阁团队"),
    "deepseek": dict(chips=["image-text-to-text", "MIT", "连续第二周上榜"], what="这周的热度来自本地部署：量化版 + llama.cpp",
                     note="已合并：ISTA-DASLab GSQ-RCO GGUF（#9）、orcarouter 去审查 GGUF（#15）"),
    "lfm3": dict(chips=["text-generation", "LFM Open License v1.0", "发布于 2026-10-27"], what="4 bit 约 1GB 的端侧智能体模型",
                 note="已合并：官方 LFM3-1.7B-GGUF（#29）、AtomicChat 去审查 GGUF（#32）"),
    "nemotron": dict(chips=["automatic-speech-recognition", "OpenMDW-1.1", "发布于 2026-10-28"], what="用一句指令决定怎么转写的语音大模型",
                     note="约 34B 总参数 · 约 4.3B 激活"),
    "mistral": dict(chips=["image-text-to-text", "Mistral 开放权重许可", "权重发布于 2026-10-29"], what="约 1T 总参数、49B 激活的多模态 MoE",
                    note="代号 Le Chonk · 10/6 预览，10/29 放出权重"),
}
PIDS = ["nanbeige", "deepseek", "lfm3", "nemotron", "mistral"]

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
        self.tm = TM[self.key]; self.t = 0.0
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
        date = chip("2026 年第 44 周 · 10 月 31 日", color=HF, size=24).next_to(title, DOWN, buff=0.4)
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
        allg = Group(rank, rank_lab, og, repo, chips, cards, what, bar, nt)
        allg.shift(UP * (0.3 - (allg.get_top()[1] + allg.get_bottom()[1]) / 2))
        self.P(FadeIn(rank, shift=RIGHT * 0.3), FadeIn(rank_lab), FadeIn(og), FadeIn(repo, shift=UP * 0.2), rt=0.8)
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips], lag_ratio=0.2), rt=0.6)
        self.P(FadeIn(c1), FadeIn(c2), FadeIn(c3), rt=0.3)
        self.P(a1, a2, a3, rt=1.6)
        self.right()
        self.W(max(self.cue(1) - 0.3, self.t))
        self.P(FadeIn(what, shift=RIGHT * 0.2), Create(bar), FadeIn(nt), rt=0.6)
        self.later()
        self.finish()
    def right(self): pass
    def later(self): pass
    def panel(self): return box(6.4, 5.5, color=BORDER, fill="#0F141B").move_to([3.6, 0.3, 0])

class P1a(IntroScene):
    key = "P1a"; pid = "nanbeige"
    def right(self):
        bc = DATA["nanbeige"]["bench_card"]
        b = self.panel()
        t = T("智能体任务（官方自报）", 24, FG, weight=BOLD)
        cols = [("Nanbeige4.3-33B", HF, 0), ("Qwen3.8-27B", PURPLE, 1), ("Gemma4-31B", DIM, 3)]
        lg = legend([(n, c) for n, c, _ in cols], 16)
        rows = VGroup()
        for k in ["Terminal-Bench 2.1", "Terminal-Bench 4.0", "DeepSWE", "Automation Bench"]:
            rows.add(VGroup(T(k, 18, FG), hbars([("", bc[k][i], c) for _, c, i in cols], 100, bw=4.6, lw=0.2, size=15, h=0.16, gap=0.04)).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        src = src_t("来源：Nanbeige4.3-33B 模型卡表格")
        VGroup(VGroup(t, lg).arrange(DOWN, buff=0.12), rows, src).arrange(DOWN, buff=0.22).move_to(b)
        self.P(FadeIn(b), FadeIn(t), FadeIn(lg), rt=0.5)
        self.P(LaggedStart(*[AnimationGroup(FadeIn(r[0]), grow(r[1], 0.15)) for r in rows], lag_ratio=0.15), FadeIn(src), rt=1.4)

class P2a(IntroScene):
    key = "P2a"; pid = "deepseek"
    def right(self):
        b = self.panel()
        t = T("近 30 天下载：原仓库 vs 量化版", 23, FG, weight=BOLD)
        m = {x["repo"]: x for x in DATA["deepseek"]["merged"]}
        rows = [("原仓库（官方）", DATA["deepseek"]["downloads_30d"], DIM),
                ("ISTA-DASLab GGUF", m["ISTA-DASLab/DeepSeek-V4.1-Flash-1017-GSQ-RCO-GGUF"]["downloads_30d"], GREEN),
                ("orcarouter 去审查 GGUF", m["orcarouter/DeepSeek-V4.1-Flash-1017-abliterated-GGUF"]["downloads_30d"], DIM)]
        ch = hbars(rows, 2100000, bw=2.3, lw=2.6, size=18, h=0.4, gap=0.18, fmt="{:,}")
        n1 = fit(T("下载数按文件请求计，分片多的 GGUF 仓库会偏高", 16, MUTED), 5.8)
        src = src_t("来源：Hugging Face API（2026-10-31 03:12 PDT）")
        cs = VGroup(chip("上周热榜第 1", color=HF, size=19), chip("763B 总参数 · 384 专家选 6", color=BLUE, size=19)).arrange(RIGHT, buff=0.12)
        fit(cs, 5.9)
        VGroup(t, ch, n1, src, cs).arrange(DOWN, buff=0.3).move_to(b)
        self.P(FadeIn(b), FadeIn(t), FadeIn(cs), rt=0.5)
        self.P(grow(ch), FadeIn(n1), FadeIn(src), rt=1.2)

class P3a(IntroScene):
    key = "P3a"; pid = "lfm3"
    def right(self):
        e = DATA["lfm3"]["edge"]; cols = e["cols"]; ip = e["iPhone 17 Pro"]
        b = self.panel()
        t = fit(T("iPhone 17 Pro 实测（官方，llama.cpp Q4_0）", 21, FG, weight=BOLD), 5.9)
        nm = ["LFM3-1.7B", "MiniCPM5-2B", "Qwen3.5-4B", "Qwen3.5-9B", "Gemma 4 E4B"]
        d1 = hbars([(n, v, BLUE if i == 0 else DIM) for i, (n, v) in enumerate(zip(nm, ip["decode"]))], 45, bw=2.6, lw=2.0, size=16, h=0.24, gap=0.07)
        d2 = hbars([(n, v, GREEN if i == 0 else DIM) for i, (n, v) in enumerate(zip(nm, ip["mem_gb"]))], 7, bw=2.6, lw=2.0, size=16, h=0.24, gap=0.07, fmt="{:.2f} GB")
        G1 = VGroup(T("生成速度 tok/s（越高越好）", 18, MUTED), d1).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        G2 = VGroup(T("内存占用（越低越好）", 18, MUTED), d2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        src = src_t("来源：LFM3-1.7B 模型卡 Edge Inference 图")
        VGroup(t, G1, G2, src).arrange(DOWN, buff=0.28).move_to(b)
        G1.shift(RIGHT * 0.3); G2.shift(RIGHT * 0.3)
        self.P(FadeIn(b), FadeIn(t), rt=0.5)
        self.P(FadeIn(G1[0]), grow(d1), rt=1.0)
        self.P(FadeIn(G2[0]), grow(d2), FadeIn(src), rt=1.0)

class P4a(IntroScene):
    key = "P4a"; pid = "nemotron"
    def right(self):
        g, cap = picture(A + "nem_hero.png", width=6.6, credit="图片来源：NVIDIA-Nemotron-3.5-Transcribe 模型卡")
        g.move_to([3.55, 0.75, 0]); cap.next_to(g, DOWN, buff=0.1)
        cs = VGroup(chip("40 种语言", color=GREEN, size=19), chip("最多 8 人 · 单段 1 小时", color=GREEN, size=19), chip("离线，非流式", color=ORANGE, size=19)).arrange(RIGHT, buff=0.12)
        fit(cs, 6.6).next_to(cap, DOWN, buff=0.22)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        self.P(FadeIn(cs, shift=UP * 0.15), rt=0.5)

class P5a(IntroScene):
    key = "P5a"; pid = "mistral"
    def right(self):
        b = self.panel()
        big = VGroup(M("~1T", 64, BLUE, weight=BOLD), T("总参数", 22, MUTED), M("49B", 64, GREEN, weight=BOLD), T("激活", 22, MUTED)).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        r2 = VGroup(M("1M", 42, YELLOW, weight=BOLD), T("上下文", 20, MUTED), M("72", 42, FG, weight=BOLD), T("层 · 128 专家选 4 + 1 共享", 20, MUTED)).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
        tl = VGroup(chip("10/6 预览", color=BORDER, size=19), T("→ 3 周 RL →", 19, MUTED), chip("10/29 放出权重", color=GREEN, size=19)).arrange(RIGHT, buff=0.15)
        cs = VGroup(chip("3,800 张 GB200 · 欧洲自建机房", color=BLUE, size=19), chip("1.6B 视觉编码器", color=BLUE, size=19)).arrange(RIGHT, buff=0.12)
        src = src_t("来源：mistralai/Mistral-Large-4-1T-A52B 模型卡")
        inner = VGroup(fit(big, 5.8), fit(r2, 5.8), fit(tl, 5.8), fit(cs, 5.8), src).arrange(DOWN, buff=0.4).move_to(b)
        self.P(FadeIn(b), FadeIn(big, shift=UP * 0.15), rt=0.7)
        self.P(LaggedStart(FadeIn(r2), FadeIn(cs), FadeIn(src), lag_ratio=0.25), rt=0.9)
        self.tl = tl
    def later(self):
        self.W(self.sub_t("十月初"))
        self.P(FadeIn(self.tl, shift=UP * 0.1), rt=0.6)

# ───────────────────────────── #1 Nanbeige4.3-33B
class P1b(Base):
    key = "P1b"
    def construct(self):
        self.head("nanbeige", "设计")
        n1 = node("Nanbeige4.3-33B", 3.0, 1.0, HF, 24, "教师智能体 · 稠密 33.1B")
        n2 = node("智能体能力蒸馏", 2.7, 1.0, PURPLE, 22, "轨迹 · 工具调用")
        n3 = node("Nanbeige4.3-3B", 2.7, 1.0, BLUE, 24, "即将推出")
        fl = VGroup(n1, n2, n3).arrange(RIGHT, buff=0.6).move_to(UP * 2.2)
        ar = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3) for a, b in zip(fl[:-1], fl[1:])])
        n3[0].set_stroke(BLUE, 2).set_fill(PANEL, 1); n3[0].set_stroke(opacity=0.8)
        self.P(FadeIn(n1, shift=UP * 0.15), rt=0.5)
        self.P(GrowArrow(ar[0]), FadeIn(n2), GrowArrow(ar[1]), FadeIn(n3), rt=1.0)
        self.W(self.cue(1))
        c1 = card_rows("不走稀疏，直接稠密", [("52 层 · hidden 7168", None), ("GQA：56 个查询头 / 8 个 KV 头", None), ("上下文 512K（Base 版 131K）", GREEN)], 6.3, HF, 20, 24)
        c1.move_to([-3.55, 0.95 - c1.height / 2, 0])
        self.P(FadeIn(c1, shift=UP * 0.15), rt=0.6)
        self.W(self.cue(2))
        c2 = card_rows("多轮智能体模板", [("preserve_thinking = true：保留前几轮思考", None), ("工具调用、办公、代码智能体建议开启", None), ("工具调用格式推荐 XML（也支持 JSON）", MUTED)], 6.3, PURPLE, 20, 24)
        c2.move_to([3.55, 0.95 - c2.height / 2, 0])
        self.P(FadeIn(c2, shift=UP * 0.15), rt=0.6)
        self.W(self.cue(3))
        self.P(FadeOut(c2), rt=0.3)
        rows = [("16 bit 权重", 66.2, DIM), ("512K KV 缓存（16 bit）", 111.7, ORANGE), ("4 bit 权重", 19.8, GREEN)]
        ch = hbars(rows, 115, bw=3.0, lw=2.4, size=17, h=0.3, gap=0.1, fmt="{:g} GB")
        t = T("显存账（单路满上下文）", 21, FG, weight=BOLD)
        src = fit(T("KV 与 4 bit 数字：the9.pro 第三方测算 · 16 bit 权重 = 33.1B × 2 字节", 14, MUTED), 6.0)
        G = VGroup(t, ch, src).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        G.move_to([3.55, 0.95 - G.height / 2 - 0.05, 0])
        self.P(FadeIn(t), grow(ch), FadeIn(src), rt=1.2)
        self.finish()

class P1c(Base):
    key = "P1c"
    def construct(self):
        self.head("nanbeige", "评测", GREEN)
        jb = DATA["nanbeige"]["jobbench"]
        zh = {"Web administrators": "网站管理员", "Technical writers": "技术写作", "Online merchants": "网店运营", "Lawyers": "律师",
              "Customer service representatives": "客服", "Secretaries & administrative assistants": "秘书 / 行政助理",
              "Mechanical engineering technicians": "机械工程技术员", "Healthcare managers": "医疗管理"}
        t = T("JobBench · 35 种职业（节选）", 23, FG, weight=BOLD)
        lg = legend([("Nanbeige4.3-33B", HF), ("Qwen3.8-27B", PURPLE)], 16)
        win = ["Web administrators", "Technical writers", "Online merchants", "Lawyers"]
        lose = ["Customer service representatives", "Secretaries & administrative assistants", "Healthcare managers", "Mechanical engineering technicians"]
        def grp(keys):
            out = VGroup()
            for k in keys:
                a, q = jb["rows"][k]
                out.add(VGroup(T(zh[k], 17, FG), hbars([("", a, HF), ("", q, PURPLE)], 80, bw=3.2, lw=0.1, size=14, h=0.14, gap=0.03)).arrange(DOWN, aligned_edge=LEFT, buff=0.05))
            return out.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        W_, L_ = grp(win), grp(lose)
        wt = T("领先明显", 18, GREEN, weight=BOLD); lt = T("反而落后", 18, RED, weight=BOLD)
        col1 = VGroup(wt, W_).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        col2 = VGroup(lt, L_).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        cols = VGroup(col1, col2).arrange(RIGHT, buff=0.5, aligned_edge=UP)
        ov = VGroup(*[T(f"总分 {n.split('-')[0]} {v:.1f}", 16, MUTED) for n, v in jb["overall"].items()]).arrange(RIGHT, buff=0.3)
        src = src_t("来源：Nanbeige 模型卡 JobBench 职业分项图（官方自报）")
        L = VGroup(VGroup(t, lg).arrange(RIGHT, buff=0.4), cols, ov, src).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        L.scale_to_fit_height(5.75); fit(L, 8.9); L.move_to([-2.35, 3.0 - L.height / 2, 0])
        self.P(FadeIn(t), FadeIn(lg), FadeIn(ov), FadeIn(src), rt=0.6)
        self.W(self.cue(1))
        self.P(FadeIn(wt), LaggedStart(*[AnimationGroup(FadeIn(r[0]), grow(r[1], 0.1)) for r in W_], lag_ratio=0.15), rt=1.2)
        self.W(self.sub_t("可到了"))
        self.P(FadeIn(lt), LaggedStart(*[AnimationGroup(FadeIn(r[0]), grow(r[1], 0.1)) for r in L_], lag_ratio=0.15), rt=1.2)
        self.W(self.cue(2))
        bc = DATA["nanbeige"]["bench_card"]
        cc = [("Nanbeige", HF, 0), ("Qwen3.8", PURPLE, 1), ("Gemma4", DIM, 3)]
        ms = VGroup(*[mini(k, [(n, bc[k][i], c) for n, c, i in cc], 100, bw=2.0, lw=1.1, size=15, h=0.2, gap=0.06, tsize=19) for k in ["GPQA-Diamond", "AIME26"]])
        ms.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        mt = T("通用题：基本打平", 20, FG, weight=BOLD)
        R = VGroup(mt, ms).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        R.scale(1.12); R.move_to([6.8 - R.width / 2, 3.0 - R.height / 2 - 0.1, 0])
        self.P(FadeIn(mt), *[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.1)) for m in ms], rt=1.2)
        self.W(self.cue(3))
        s1 = stat_card("未收录", "Artificial Analysis", 3.6, 1.1, DIM, 26, 16, "2026-10-31 检查")
        s1.next_to(R, DOWN, buff=0.35).align_to(R, LEFT)
        self.P(FadeIn(s1, shift=UP * 0.15), rt=0.5)
        self.finish()

# ───────────────────────────── #2 DeepSeek-V4.1-Flash-1017
class P2b(Base):
    key = "P2b"
    def construct(self):
        self.head("deepseek", "本地化：量化")
        tl = VGroup(chip("10/17 发布 1017 权重", color=BORDER, size=19), T("→", 22, MUTED), chip("10/23 ISTA 量化仓库上线", color=BORDER, size=19), T("→", 22, MUTED),
                    chip("10/25 llama.cpp b11870 正式支持", color=GREEN, size=19)).arrange(RIGHT, buff=0.15).move_to(UP * 2.55)
        fit(tl, 13.2)
        self.P(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in tl], lag_ratio=0.2), rt=1.2)
        self.W(self.cue(1))
        rng = np.random.default_rng(3)
        bits = rng.choice([1, 2, 3, 4], size=(6, 12), p=[0.3, 0.4, 0.2, 0.1])
        pal = {1: "#1F3A5F", 2: BLUE, 3: PURPLE, 4: ORANGE}
        def grid(uniform):
            g = VGroup()
            for i in range(6):
                for j in range(12):
                    c = BLUE if uniform else pal[bits[i, j]]
                    g.add(Square(0.3).set_stroke(BG, 2).set_fill(c, 1).move_to([j * 0.32, -i * 0.32, 0]))
            return g
        g1, g2 = grid(True), grid(False)
        G1 = VGroup(T("均匀量化：所有张量同一精度", 19, MUTED), g1).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        G2 = VGroup(T("GSQ-RCO：梯度搜索，按敏感度逐张量分配", 19, FG), g2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        lg = legend([("低", "#1F3A5F"), ("", BLUE), ("", PURPLE), ("高精度", ORANGE)], 15)
        Gs = VGroup(G1, G2, lg).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([-3.6, -0.35, 0])
        nt = fit(T("示意图 · 总大小卡在预算内 · arXiv:2604.18556 / 2605.00649", 14, MUTED), 5.5).next_to(Gs, DOWN, buff=0.12).align_to(Gs, LEFT)
        self.P(FadeIn(G1), rt=0.5)
        self.P(FadeIn(G2[0]), LaggedStart(*[FadeIn(s, scale=0.5) for s in g2], lag_ratio=0.01), FadeIn(lg), FadeIn(nt), rt=1.2)
        self.W(self.cue(2))
        ist = DATA["deepseek"]["ista"]; bm = ist["bench"]
        t = T("三项平均（AIME25 · GPQA-D · LCB v6）", 20, FG, weight=BOLD)
        rows = [("原版 FP8/FP4", bm["Base"][3], DIM)] + [(f"{b['id']} · {b['bpw']:.2f} bit", bm[b["id"]][3], GREEN if b["id"] == "IQ2_XXS" else BLUE) for b in ist["builds"]]
        ch = hbars(rows, 95, bw=2.4, lw=2.3, size=17, h=0.32, gap=0.12, fmt="{:.2f}", base=85)
        rec = VGroup(*[T(f"{b['recovery']:.1f}%", 16, GREEN if b["recovery"] >= 99.9 else MUTED) for b in ist["builds"]])
        for r, row in zip(rec, ch[1:]): r.next_to(row[2], RIGHT, buff=0.2)
        sz = VGroup(*[chip(f"{b['id']} {b['total_gb']:.0f} GB", color=BORDER, size=16) for b in ist["builds"]]).arrange(RIGHT, buff=0.1)
        src = fit(T("横轴从 85 起 · 来源：ISTA-DASLab 量化模型卡（量化作者自测，reasoning effort 50）", 14, MUTED), 6.2)
        R = VGroup(t, ch, sz, src).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        R.move_to([3.5, -0.3, 0])
        for r, row in zip(rec, ch[1:]): r.next_to(row[2], RIGHT, buff=0.2)
        rec_all = rec
        self.P(FadeIn(t), grow(ch), rt=1.2)
        self.P(FadeIn(rec_all), FadeIn(sz), FadeIn(src), rt=0.6)
        self.finish()

class P2c(Base):
    key = "P2c"
    def construct(self):
        self.head("deepseek", "本地化：部署与第三方评测", GREEN)
        def tier(name, sub, col, w=4.0, h=1.15):
            b = box(w, h, color=col, fill="#0F141B")
            g = VGroup(T(name, 22, col, weight=BOLD), fit(T(sub, 16, FG), w - 0.3)).arrange(DOWN, buff=0.08).move_to(b)
            return VGroup(b, g)
        ssd = tier("SSD · 内存映射", "Engram 查找表 196.6B 参数 · IQ4_NL · 110.6 GB", ORANGE, 5.4)
        ram = tier("系统内存", "主干 121–155 GB（随版本）", BLUE, 5.4)
        gpu = tier("12 GB 显卡", "第三方引擎 Strata 调度", GREEN, 5.4)
        st = VGroup(gpu, ram, ssd).arrange(DOWN, buff=0.22).move_to([-3.5, -0.05, 0])
        nt = fit(T("每个 token 只读查找表的一行 → 不必占显存或内存", 17, MUTED), 5.6).next_to(st, DOWN, buff=0.15)
        src = fit(T("来源：ISTA-DASLab 量化模型卡（Strata 部分卡内仍标注待补充）", 14, MUTED), 5.6).next_to(nt, DOWN, buff=0.08)
        self.P(FadeIn(ssd, shift=UP * 0.15), FadeIn(nt), rt=0.7)
        self.W(self.cue(1))
        self.P(FadeIn(ram, shift=UP * 0.15), rt=0.5)
        self.P(FadeIn(gpu, shift=UP * 0.15), FadeIn(src), rt=0.5)
        self.W(self.cue(2))
        aa = DATA["deepseek"]["third_party"]["Artificial Analysis"]
        s1 = stat_card(str(aa["intelligence_index_v5"]), "AA 智能指数 v5", 2.0, 1.35, BLUE, 34, 16, aa["rank"])
        s2 = stat_card("175", "输出 token/秒", 2.0, 1.35, GREEN, 34, 16, "$0.30 / $1.20 每百万")
        s3 = stat_card("1.7 亿", "跑完指数的输出 token", 2.0, 1.35, ORANGE, 28, 16, "偏长")
        ss = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.12)
        at = T("Artificial Analysis（第三方，2026-10-31 查询）", 18, MUTED)
        n2 = fit(T("上周页面显示旧版指数 45 分；指数改版后两周分数不可直接比较", 15, MUTED), 6.3)
        AAg = VGroup(at, ss, n2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.6, 0.4, 0])
        self.P(FadeIn(at), LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in ss], lag_ratio=0.25), rt=1.0)
        self.P(FadeIn(n2), rt=0.4)
        self.finish()

# ───────────────────────────── #3 LFM3-1.7B
class P3b(Base):
    key = "P3b"
    def construct(self):
        self.head("lfm3", "设计")
        kinds = ["conv"] * 13 + ["swa"] * 5 + ["glob"] * 6
        order = []
        c, s, g = 13, 5, 6
        pat = ["conv", "conv", "swa", "conv", "glob", "conv", "conv", "swa", "glob", "conv", "conv", "glob", "conv", "swa", "conv", "glob", "conv", "swa", "conv", "glob", "conv", "swa", "conv", "glob"]
        col = {"conv": BLUE, "swa": PURPLE, "glob": ORANGE}
        blocks = VGroup(*[RoundedRectangle(width=0.42, height=1.0, corner_radius=0.06, stroke_width=0).set_fill(col[k], 1) for k in pat]).arrange(RIGHT, buff=0.08)
        blocks.move_to([0, 1.75, 0])
        lg = VGroup(*[VGroup(Square(0.24).set_fill(c_, 1).set_stroke(width=0), T(n, 19, FG)).arrange(RIGHT, buff=0.12) for n, c_ in
                      [("门控短卷积 × 13（卷积核 7）", BLUE), ("滑动窗口注意力 × 5（窗口 256）", PURPLE), ("全局注意力 × 6", ORANGE)]]).arrange(RIGHT, buff=0.5)
        lg.next_to(blocks, DOWN, buff=0.25)
        nt = T("24 层 · 排列顺序为示意", 15, MUTED).next_to(blocks, UP, buff=0.12).align_to(blocks, LEFT)
        self.P(LaggedStart(*[GrowFromEdge(b, DOWN) for b in blocks], lag_ratio=0.04), FadeIn(nt), rt=1.4)
        self.P(FadeIn(lg), rt=0.5)
        self.W(self.cue(1))
        c1 = card_rows("硬件在环架构搜索", [("14 种设备 / 推理后端组合上实测", None), ("速度和质量一起筛选候选架构", None), ("8K 上下文：单位参数比 LFM2-1.2B 快约 25%", GREEN)], 6.4, BLUE, 19, 23)
        c1.move_to([-3.5, -0.05 - c1.height / 2 + 0.6, 0])
        self.P(FadeIn(c1, shift=UP * 0.15), rt=0.6)
        self.W(self.cue(2))
        c2 = card_rows("为 4 bit 量化而设计", [("按头 sigmoid 门控注意力：压住激活离群值", None), ("全局层部分 RoPE：一半维度不旋转", None), ("三明治归一化", MUTED)], 6.4, PURPLE, 19, 23)
        c2.move_to([3.55, c1.get_center()[1], 0])
        self.P(FadeIn(c2, shift=UP * 0.15), rt=0.6)
        self.W(self.cue(3))
        old = VGroup(blocks, lg, nt, c1, c2)
        g, cap = picture(A + "lfm3_post.png", width=10.0, credit="图片来源：LFM3 模型卡 / Liquid AI 博客（后训练流程）")
        g.move_to([0, 0.7, 0]); cap.next_to(g, DOWN, buff=0.08)
        k = VGroup(chip("SFT 1.75T token", color=BORDER, size=18), chip("混合 RL 带长度惩罚", color=BORDER, size=18), chip("MOPD：多教师蒸馏回一个学生", color=PURPLE, size=18),
                   chip("真实环境智能体 RL", color=GREEN, size=18)).arrange(RIGHT, buff=0.12).next_to(cap, DOWN, buff=0.15)
        fit(k, 12.8)
        self.P(FadeOut(old), rt=0.4)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.7)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in k], lag_ratio=0.2), rt=0.9)
        self.finish()

class P3c(Base):
    key = "P3c"
    def construct(self):
        self.head("lfm3", "评测", GREEN)
        bc = DATA["lfm3"]["bench_card"]; cols = bc["cols"]
        pick = [("LFM3-1.7B", BLUE), ("Qwen3.5-4B", DIM), ("Qwen3.5-9B", PURPLE)]
        good = ["WebArena-Verified", "AutomationBench", "BFCL V4", "LiveClaw"]
        bad = ["GPQA-Diamond", "RULER 128K"]
        def mk(names):
            return VGroup(*[mini(n, [(p, bc[n][cols.index(p)], c) for p, c in pick], 100, bw=1.7, lw=1.35, size=15, h=0.2, gap=0.06, tsize=19, fmt="{:.1f}") for n in names])
        mg, mb = mk(good), mk(bad)
        G = VGroup(VGroup(mg[0], mg[1]).arrange(RIGHT, buff=0.5, aligned_edge=UP), VGroup(mg[2], mg[3]).arrange(RIGHT, buff=0.5, aligned_edge=UP)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        gt = T("智能体任务：领先", 21, GREEN, weight=BOLD)
        LG = VGroup(gt, G).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bt = T("知识与超长上下文：落后", 21, RED, weight=BOLD)
        B = VGroup(bt, VGroup(*mb).arrange(DOWN, aligned_edge=LEFT, buff=0.35)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lg = legend([(p, c) for p, c in pick], 16)
        src = src_t("来源：LiquidAI/LFM3-1.7B 模型卡（官方自报）")
        top = VGroup(LG, B).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        Lall = VGroup(lg, top, src).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        Lall.scale_to_fit_height(4.6); fit(Lall, 13.2); Lall.move_to([0, 3.0 - Lall.height / 2, 0])
        self.P(FadeIn(lg), FadeIn(gt), *[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.1)) for m in mg], FadeIn(src), rt=1.6)
        self.W(self.cue(1))
        self.P(FadeIn(bt), *[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.1)) for m in mb], rt=1.2)
        w = chip("模型卡：不建议用于智能体编程和复杂推理", color=ORANGE, size=18).next_to(B, DOWN, buff=0.3).align_to(B, LEFT)
        fit(w, 6.6 - B.get_left()[0])
        self.W(self.sub_t("模型卡自己"))
        self.P(FadeIn(w, shift=UP * 0.1), rt=0.4)
        self.W(self.cue(2))
        s1 = chip("Artificial Analysis：未收录（2026-10-31 检查）", color=DIM, size=17).next_to(w, DOWN, buff=0.15).align_to(w, LEFT)
        fit(s1, 6.6 - B.get_left()[0])
        for m_ in (w, s1):
            if m_.get_right()[0] > 6.8: m_.shift(LEFT * (m_.get_right()[0] - 6.8))
        self.P(FadeIn(s1, shift=UP * 0.1), rt=0.4)
        self.finish()

# ───────────────────────────── #4 Nemotron-3.5-Transcribe
class P4b(Base):
    key = "P4b"
    def construct(self):
        self.head("nemotron", "设计")
        g, cap = picture(A + "nem_arch.png", width=9.3, credit="图片来源：NVIDIA-Nemotron-3.5-Transcribe 模型卡（架构图）")
        g.move_to([-2.3, 0.75, 0]); cap.next_to(g, DOWN, buff=0.08).align_to(g, LEFT)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        im = g[0]; W_, H_ = im.width, im.height; ul = im.get_corner(UL)
        def rect(x0, y0, x1, y1, c):  # 归一化坐标（相对原图 1648×791）
            return Rectangle(width=(x1 - x0) * W_, height=(y1 - y0) * H_, color=c, stroke_width=4).move_to(ul + RIGHT * (x0 + x1) / 2 * W_ + DOWN * (y0 + y1) / 2 * H_)
        r1 = rect(0.18, 0.08, 0.49, 0.80, YELLOW)
        c1 = card_rows("并行专家编码器", [("ASR 编码器 600M：听清内容", None), ("说话人分离 ~99M（冻结）：分清是谁", None), ("→ Nemotron 3.5 Lightning 30B-A3B", GREEN)], 4.2, YELLOW, 17, 21)
        c1.move_to([4.85, 2.95 - c1.height / 2, 0])
        self.P(Create(r1), FadeIn(c1, shift=LEFT * 0.15), rt=0.7)
        self.W(self.cue(1))
        r2 = rect(0.0, 0.38, 0.16, 0.62, BLUE)
        c2 = card_rows("时间戳：生成后再对齐", [("CTC 头 47M 参数", None), ("任何指令格式都能出词级时间", None)], 4.2, BLUE, 17, 21)
        c2.next_to(c1, DOWN, buff=0.2)
        self.P(ReplacementTransform(r1, r2), FadeIn(c2, shift=LEFT * 0.15), rt=0.7)
        self.W(self.cue(2))
        r3 = rect(0.80, 0.08, 0.99, 0.24, GREEN)
        cs = VGroup(chip("MTP 投机解码（最多 8 token）", color=GREEN, size=17), chip("可选 DFlash2 草稿模型", color=GREEN, size=17), chip("仅离线 · 不支持流式", color=ORANGE, size=17)).arrange(RIGHT, buff=0.12)
        fit(cs, 13.0).move_to([0, -2.6, 0])
        if cs.get_top()[1] > cap.get_bottom()[1] - 0.1: cs.next_to(cap, DOWN, buff=0.15).set_x(0)
        self.P(ReplacementTransform(r2, r3), FadeIn(cs, shift=UP * 0.1), rt=0.7)
        self.finish()

def waveform(path, w=4.6, h=1.0, n=120, col=GREEN):
    with wave.open(path) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(float)
    seg = np.array_split(np.abs(a), n); env = np.array([s.max() for s in seg]); env = env / env.max()
    bw = w / n
    return VGroup(*[Rectangle(width=bw * 0.6, height=max(e * h, 0.02), stroke_width=0).set_fill(col, 1).move_to([i * bw, 0, 0]) for i, e in enumerate(env)])

class P4s(Base):
    key = "P4s"
    def construct(self):
        self.head("nemotron", "实测：在线 Space")
        meta = json.load(open("demo/nemotron_sample.json", encoding="utf-8"))
        import re
        clean = lambda s: re.sub(r"<sub>.*?</sub>", "", s, flags=re.S).replace("&lt;", "<").replace("&gt;", ">").strip()
        lb = box(3.7, 5.6, color=BORDER, fill="#0F141B").move_to([-5.05, 0.25, 0])
        wf = waveform("demo/nemotron_test.wav", 3.3, 1.1)
        it = VGroup(T("输入音频", 19, MUTED), wf, T("25 秒 · 英文双人对话", 18, FG), fit(T("edge-tts 合成，含 um / uh 与重复", 16, MUTED), 3.3),
                    fit(T("Space：hugging-apps/", 16, MUTED), 3.3), fit(T("nemotron-3-5-transcribe", 16, MUTED), 3.3), fit(T("（非 NVIDIA 官方）", 16, MUTED), 3.3),
                    fit(T("每次约 4.5 秒（共享 ZeroGPU）", 16, MUTED), 3.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        it.move_to(lb)
        self.P(FadeIn(lb), FadeIn(it[0]), LaggedStart(*[GrowFromCenter(b) for b in wf], lag_ratio=0.005), rt=1.0)
        self.P(FadeIn(it[2:]), rt=0.5)
        runs = meta["runs"]
        spec = [("逐字（Verbatim）", YELLOW, clean(runs[0]["output"])), ("清理（Clean）", GREEN, clean(runs[1]["output"])),
                ("说话人标注", PURPLE, clean(runs[2]["output"])), ("翻成中文（自定义指令）", BLUE, clean(runs[3]["output"]))]
        cards = Group()
        for name, c, txt in spec:
            zh = any(ord(ch) > 0x2e80 for ch in txt)
            p = para(txt, 50 if zh else 92, 17, FG, FONT if zh else MONO, 0.3)
            if "说话人" in name:
                txt2 = txt.replace(" <spk:", "\n<spk:")
                p = VGroup(*[para(l, 92, 17, FG, MONO, 0.3) for l in txt2.split("\n")]).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            lab = T(name, 17, c, weight=BOLD)
            inner = VGroup(lab, p).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            fit(inner, 9.9)
            b = box(10.3, inner.height + 0.26, color=c, fill="#0F141B")
            inner.move_to(b).align_to(b.get_left() + RIGHT * 0.18, LEFT)
            cards.add(Group(b, inner))
        cards.arrange(DOWN, buff=0.12)
        if cards.height > 5.9: cards.scale_to_fit_height(5.9)
        cards.move_to([1.85, 0.2, 0])
        self.P(FadeIn(cards[0], shift=LEFT * 0.15), rt=0.6)
        self.W(self.sub_t("逐字模式"))
        self.W(self.sub_t("清理模式"))
        self.P(FadeIn(cards[1], shift=LEFT * 0.15), rt=0.5)
        self.W(self.sub_t("说话人模式"))
        self.P(FadeIn(cards[2], shift=LEFT * 0.15), rt=0.5)
        self.W(self.cue(2))
        self.P(FadeIn(cards[3], shift=LEFT * 0.15), rt=0.5)
        self.finish()

class P4c(Base):
    key = "P4c"
    def construct(self):
        self.head("nemotron", "评测", GREEN)
        bc = DATA["nemotron"]["bench_card"]
        keys = ["多说话人 cpWER", "偏好 ASR WER（指令）", "英文 Open ASR（9 套）WER", "长音频 WER", "多语言（7 种）WER"]
        ms = VGroup()
        for k in keys:
            (n1, v1), (n2, v2) = list(bc[k].items())
            ms.add(mini(k, [("Nemotron", v1, GREEN), (n2, v2, DIM)], 18, bw=2.2, lw=2.3, size=15, h=0.22, gap=0.06, tsize=18, fmt="{:.2f}"))
        ms.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        t = T("错误率（越低越好）· 官方自报", 21, FG, weight=BOLD)
        L = VGroup(t, ms).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        if L.height > 5.9: L.scale_to_fit_height(5.9)
        L.move_to([-3.4, 3.0 - L.height / 2, 0])
        self.P(FadeIn(t), LaggedStart(*[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.1)) for m in ms], lag_ratio=0.12), rt=1.8)
        self.W(self.cue(1))
        s1 = stat_card("2,238×", "实时速率（单张 RTX PRO 6000）", 3.0, 1.35, GREEN, 32, 16, "NVFP4 + DFlash2")
        s2 = stat_card("0.13 秒", "处理 30 秒音频", 3.0, 1.35, BLUE, 32, 16, "同一配置")
        ss = VGroup(s1, s2).arrange(RIGHT, buff=0.15)
        w = chip("该方案尚未开源，仅 NIM 提供", color=ORANGE, size=18)
        R = VGroup(ss, w).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.7, 1.6, 0])
        self.P(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in ss], lag_ratio=0.3), rt=0.8)
        self.P(FadeIn(w), rt=0.4)
        self.W(self.cue(2))
        q = quote("VoiceArena 第一 · David AI 说话人分离榜错误率最低", 6.2, "NVIDIA 在 Hugging Face 博客中的说法 · 未独立核实", ORANGE, 19)
        q.next_to(R, DOWN, buff=0.35).align_to(R, LEFT)
        tc = T("另见：TechCrunch 10/28 发布报道", 15, MUTED).next_to(q, DOWN, buff=0.12).align_to(q, LEFT)
        self.P(FadeIn(q, shift=UP * 0.1), FadeIn(tc), rt=0.6)
        self.finish()

# ───────────────────────────── #5 Mistral Large 4
class P5b(Base):
    key = "P5b"
    def construct(self):
        self.head("mistral", "设计")
        q = node("当前查询", 2.0, 0.85, FG, 21)
        ix = node("轻量索引器", 2.4, 0.85, PURPLE, 21, "DSA 式打分")
        sel = node("≤ 2048 个位置", 2.5, 0.85, YELLOW, 21, "从 1M 上下文里挑")
        att = node("MLA 注意力", 2.4, 0.85, BLUE, 21, "压缩后的 KV")
        fl = VGroup(q, ix, sel, att).arrange(RIGHT, buff=0.55).move_to(UP * 2.2)
        ar = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3) for a, b in zip(fl[:-1], fl[1:])])
        self.P(FadeIn(q), FadeIn(att), rt=0.5)
        self.P(GrowArrow(ar[0]), FadeIn(ix), GrowArrow(ar[1]), FadeIn(sel), GrowArrow(ar[2]), rt=1.2)
        dots = VGroup(*[Square(0.12).set_stroke(width=0).set_fill(YELLOW if i in (3, 4, 11, 17, 18, 19, 30, 36, 37) else "#21262D", 1) for i in range(44)]).arrange(RIGHT, buff=0.04)
        dots.next_to(fl, DOWN, buff=0.3)
        dl = T("示意：只有少数位置参与注意力", 15, MUTED).next_to(dots, DOWN, buff=0.08)
        self.P(FadeIn(dots, lag_ratio=0.02), FadeIn(dl), rt=0.8)
        self.W(self.cue(1))
        layers = VGroup(*[box(2.2, 0.5, color=BORDER, r=0.08) for _ in range(4)]).arrange(DOWN, buff=0.12)
        labs = VGroup(*[T(f"第 {n} 层", 17, FG).move_to(l) for n, l in zip(["n", "n+1", "n+2", "n+3"], layers)])
        L = VGroup(layers, labs).move_to([-4.2, -1.3, 0])
        sh1 = VGroup(chip("共享索引器 + KV", color=GREEN, size=16)).next_to(VGroup(layers[0], layers[1]), RIGHT, buff=0.25)
        br1 = Brace(VGroup(layers[0], layers[1]), RIGHT, color=GREEN, buff=0.08); sh1.next_to(br1, RIGHT, buff=0.1)
        br2 = Brace(VGroup(layers[2], layers[3]), RIGHT, color=GREEN, buff=0.08); sh2 = chip("共享索引器 + KV", color=GREEN, size=16).next_to(br2, RIGHT, buff=0.1)
        c = card_rows("其他细节", [("RoPE : NoPE = 3 : 1", None), ("LeRope：YaRN + 每个频率可学习的乘子", None), ("首层稠密 · 128 专家选 4 + 1 共享", MUTED)], 5.6, BLUE, 18, 22)
        c.move_to([3.85, -1.3, 0])
        self.P(FadeIn(L), rt=0.4)
        self.P(GrowFromCenter(br1), FadeIn(sh1), GrowFromCenter(br2), FadeIn(sh2), rt=0.7)
        self.P(FadeIn(c, shift=LEFT * 0.15), rt=0.5)
        self.W(self.cue(2))
        old = VGroup(L, br1, br2, sh1, sh2, c)
        self.P(FadeOut(old), rt=0.3)
        tgt = node("Mistral Large 4", 3.0, 1.0, BLUE, 23, "目标模型 · 1T")
        dr = node("DSpark 草稿头", 3.0, 1.0, GREEN, 23, "3 层 MLA · BF16")
        blk = VGroup(*[box(0.6, 0.6, color=GREEN, r=0.08) for _ in range(3)]).arrange(RIGHT, buff=0.08)
        bl = VGroup(*[T(f"t+{i + 1}", 15, FG).move_to(b) for i, b in enumerate(blk)])
        B = VGroup(blk, bl)
        row = VGroup(dr, B, tgt).arrange(RIGHT, buff=0.7).move_to([-0.6, -1.25, 0])
        a1 = Arrow(dr.get_right(), B.get_left(), buff=0.08, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        a2 = Arrow(B.get_right(), tgt.get_left(), buff=0.08, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        lab = T("一次提 3 个 token → 目标模型一次验证", 17, MUTED).next_to(B, DOWN, buff=0.2)
        s = stat_card("1.9×", "吞吐最高提升（官方）", 2.6, 1.3, GREEN, 34, 16).next_to(row, RIGHT, buff=0.4)
        self.P(FadeIn(dr), GrowArrow(a1), FadeIn(B), GrowArrow(a2), FadeIn(tgt), FadeIn(lab), rt=1.0)
        self.P(FadeIn(s, shift=UP * 0.15), rt=0.5)
        self.finish()

class P5c(Base):
    key = "P5c"
    def construct(self):
        self.head("mistral", "评测与许可", GREEN)
        ca = DATA["mistral"]["third_party"]["coding_agent_index_chart"]
        order = ["GLM-5.3", "Mistral Large 4", "DeepSeek V4.1 Flash 1017", "Kimi K3", "Muse Spark Open", "Beam 1.0"]
        t = T("AA 编程智能体指数", 23, FG, weight=BOLD)
        ch = hbars([(n, ca[n], ORANGE if "Mistral" in n else (BLUE if "DeepSeek" in n else DIM)) for n in order], 55, bw=3.0, lw=3.0, size=17, h=0.3, gap=0.1, fmt="{:g}%")
        src = fit(T("图表来源：Mistral 模型卡转引 Artificial Analysis；“token 少 47%”为 Mistral 自称", 14, MUTED), 6.6)
        L = VGroup(t, ch, src).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        L.move_to([-3.45, 3.0 - L.height / 2, 0])
        self.P(FadeIn(t), grow(ch), FadeIn(src), rt=1.4)
        self.W(self.sub_t("Mistral 还称"))
        tk = chip("Mistral：token 用量少 47%", color=ORANGE, size=17).next_to(L, DOWN, buff=0.2).align_to(L, LEFT)
        self.P(FadeIn(tk, shift=UP * 0.1), rt=0.4)
        self.W(self.cue(1))
        ma = DATA["mistral"]["third_party"]["Artificial Analysis"]; da = DATA["deepseek"]["third_party"]["Artificial Analysis"]
        at = T("Artificial Analysis 综合（第三方，2026-10-31）", 18, MUTED)
        rows = VGroup()
        for lab, a, b, f in [("智能指数 v5", ma["intelligence_index_v5"], da["intelligence_index_v5"], "{:g}"), ("单任务成本", ma["cost_per_task_usd"], da["cost_per_task_usd"], "${:.2f}"),
                             ("输出 token/秒", ma["output_tokens_per_s"], da["output_tokens_per_s"], "{:g}")]:
            mx = max(a, b) * 1.1
            rows.add(VGroup(T(lab, 18, FG, weight=BOLD), hbars([("Mistral Large 4", a, ORANGE), ("DeepSeek 1017", b, BLUE)], mx, bw=2.6, lw=2.2, size=15, h=0.22, gap=0.05, fmt=f)).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rk = T("智能指数：第 9 / 22 · 每百万 $0.70 / $2.10", 15, MUTED)
        R = VGroup(at, rows, rk).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.45, 0.55, 0])
        R.align_to(UP * 2.95, UP)
        self.P(FadeIn(at), LaggedStart(*[AnimationGroup(FadeIn(r[0]), grow(r[1], 0.1)) for r in rows], lag_ratio=0.2), FadeIn(rk), rt=1.4)
        self.W(self.cue(2))
        lb = box(13.4, 0.72, color=YELLOW, r=0.12)
        lt = fit(VGroup(T("许可", 22, YELLOW, weight=BOLD), T("Mistral Ecosystem Open-Weight License（改版 MIT）：可商用 · 模型即服务需另签商业许可", 20, FG)).arrange(RIGHT, buff=0.3), 12.9).move_to(lb)
        LB = VGroup(lb, lt).move_to(DOWN * 2.55)
        self.P(FadeIn(LB, shift=UP * 0.15), rt=0.5)
        self.finish()

# ───────────────────────────── 结尾
class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        t = T("本周回顾", 40, HF, weight=BOLD).move_to(UP * 2.85)
        self.P(FadeIn(t, shift=DOWN * 0.15), rt=0.5)
        tag = {"nanbeige": "33B 稠密教师智能体 · 职业任务领先", "deepseek": "2 bit 量化几乎不掉分 · 12GB 显卡可跑",
               "lfm3": "1.7B 三路混合 · 手机上跑智能体", "nemotron": "一句指令决定怎么转写", "mistral": "1T MoE · 编程智能体接近头部"}
        rows = Group()
        for pid in PIDS:
            d = DATA[pid]
            b = box(11.6, 0.68, r=0.12)
            rk = T(f"#{d['rank']}", 26, YELLOW, weight=BOLD)
            av = avatar(pid, 0.44)
            nm = fit(M(d["name"], 22, FG), 4.2)
            ds = T(tag[pid], 20, FG)
            rk.move_to(b.get_left() + RIGHT * 0.45); av.next_to(rk, RIGHT, buff=0.22)
            nm.next_to(av, RIGHT, buff=0.2)
            ds.move_to(b.get_right() + LEFT * 0.25, aligned_edge=RIGHT)
            rows.add(Group(b, rk, av, nm, ds))
        rows.arrange(DOWN, buff=0.12).move_to(UP * 0.4)
        self.P(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.15), rt=1.4)
        self.W(self.cue(2))
        self.P(FadeOut(rows), rt=0.4)
        rp = DJ["on_screen_charts"]["repack_downloads"]
        tt = T("近 30 天下载：原仓库 vs GGUF 量化版", 26, FG, weight=BOLD)
        grp = VGroup()
        for r in rp:
            mx = max(r["original_dl"], r["repack_dl"])
            lab = T(r["model"], 21, FG, weight=BOLD)
            bars = hbars([("原仓库", r["original_dl"], DIM), (r["label"], r["repack_dl"], GREEN)], mx, bw=3.6, lw=1.8, size=19, h=0.38, gap=0.1, fmt="{:,}")
            grp.add(VGroup(lab, bars).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        gg = VGroup(*grp).arrange(RIGHT, buff=1.4, aligned_edge=UP)
        src = T("每组各自按最大值缩放 · 来源：Hugging Face API（2026-10-31），下载按文件请求计", 15, MUTED)
        C = VGroup(tt, gg, src).arrange(DOWN, buff=0.35)
        fit(C, 12.6).move_to([0, 0.2, 0])
        self.P(FadeIn(tt), *[AnimationGroup(FadeIn(g_[0]), grow(g_[1], 0.2)) for g_ in grp], FadeIn(src), rt=1.6)
        self.W(self.cue(3))
        bye = T("下周见", 36, HF, weight=BOLD).next_to(t, RIGHT, buff=0.6)
        self.P(FadeIn(bye, scale=0.8), rt=0.4)
        self.finish()
