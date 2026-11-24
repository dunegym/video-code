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
    "deepseek": dict(chips=["image-text-to-text", "MIT", "上传于 2026-10-17"], what="把 KV 缓存压到上一代约 1/4 的百万上下文模型",
                     note="已合并：dealignai 去审查 FP8 版（#12）、unsloth GGUF 版（#34）"),
    "flint": dict(chips=["text-generation", "Apache-2.0", "上传于 2026-10-21"], what="约 40B 总参数、2.5B 激活的本地编程智能体模型",
                  note="已合并：unsloth/flint-GGUF（#21）"),
    "flux": dict(chips=["文生图 · 图像编辑", "FLUX Kommunity", "上传于 2026-10-13"], what="生成、编辑、多参考图合一的 5.6B 图像模型",
                 stats="black-forest-labs/flux-3-image-klein-comfy",
                 note="热榜数据取自排名更高的官方 ComfyUI 版；原仓库（#22）已合并"),
    "moss": dict(chips=["text-to-image", "Apache-2.0", "上传于 2026-10-11"], what="先规划版面、再渲染长文本的开源文生图模型",
                 note="已合并：MOSS-Image-Base（#8）、Comfy-Org/MOSS-Image（#11）"),
    "ltx": dict(chips=["image-to-video · 带音频", "LTX-2.x Community", "发布于 2026-08-11"], what="画面与声音同时生成的 22B 视频模型",
                note="热榜第 5 · 发布两个多月后仍在榜"),
}

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
        date = chip("2026 年第 43 周 · 10 月 24 日", color=HF, size=24).next_to(title, DOWN, buff=0.4)
        self.P(FadeIn(emo, scale=0.6), FadeIn(tt, shift=RIGHT * 0.3), rt=0.9)
        self.P(FadeIn(date, shift=UP * 0.15), rt=0.5)
        cards = Group()
        for pid in ["deepseek", "flint", "flux", "moss", "ltx"]:
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
        st = TRD[info["stats"]] if "stats" in info else None
        likes = st["likes"] if st else d["likes"]; dl = st["downloads"] if st else d["downloads_30d"]; ts = st["trendingScore"] if st else d["trendingScore"]
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
        self.finish()
    def right(self): pass

class P1a(IntroScene):
    key = "P1a"; pid = "deepseek"
    def right(self):
        bm = DATA["deepseek"]["bench_card_1017"]
        b = box(6.4, 5.4, color=BORDER, fill="#0F141B").move_to([3.6, 0.3, 0])
        t = T("1017 版 vs 上一版 V4.1-Flash", 24, FG, weight=BOLD)
        lg = legend([("V4.1-Flash", DIM), ("1017", BLUE)])
        rows = VGroup()
        for k, lab in [("HLE w/o tools", "HLE（无工具）"), ("Terminal-Bench 4.0", "Terminal-Bench 4.0"), ("Automation-Bench v1.0.6", "Automation-Bench"), ("DeepSWE v1.1", "DeepSWE"), ("BabyVision (w/tools)", "BabyVision")]:
            new, old = bm[k][0], bm[k][1]
            rows.add(VGroup(T(lab, 18, FG), hbars([("", old, DIM), ("", new, BLUE)], 100, bw=4.6, lw=0.2, size=16, h=0.17, gap=0.04)).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        src = T("来源：DeepSeek-V4.1-Flash-1017 模型卡（官方自报）", 15, MUTED)
        VGroup(VGroup(t, lg).arrange(DOWN, buff=0.12), rows, src).arrange(DOWN, buff=0.22).move_to(b)
        self.P(FadeIn(b), FadeIn(t), FadeIn(lg), rt=0.5)
        self.P(LaggedStart(*[AnimationGroup(FadeIn(r[0]), grow(r[1], 0.2)) for r in rows], lag_ratio=0.15), FadeIn(src), rt=1.4)

class P2a(IntroScene):
    key = "P2a"; pid = "flint"
    def right(self):
        b = box(6.3, 5.4, color=BORDER, fill="#0F141B").move_to([3.65, 0.3, 0])
        big = VGroup(M("39.8B", 60, BLUE, weight=BOLD), T("总参数", 22, MUTED), M("~2.5B", 60, GREEN, weight=BOLD), T("激活", 22, MUTED)).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        r2 = VGroup(M("262K", 40, YELLOW, weight=BOLD), T("上下文", 20, MUTED), M("49", 40, FG, weight=BOLD), T("层 · 256 专家选 6 + 1 共享", 20, MUTED)).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
        cs = VGroup(chip("从零训练", color=BLUE, size=19), chip("单张 H200 / B300 可部署", color=BLUE, size=19)).arrange(RIGHT, buff=0.12)
        cs2 = VGroup(chip("M4 Pro 笔记本 >125 tok/s（官方）", color=GREEN, size=19)).arrange(RIGHT)
        src = T("来源：RecursiveSI/flint 模型卡、Recursive 官方博客", 15, MUTED)
        inner = VGroup(fit(big, 5.8), fit(r2, 5.8), fit(cs, 5.8), fit(cs2, 5.8), src).arrange(DOWN, buff=0.38).move_to(b)
        self.P(FadeIn(b), FadeIn(big, shift=UP * 0.15), rt=0.7)
        self.P(LaggedStart(FadeIn(r2), FadeIn(cs), FadeIn(cs2), FadeIn(src), lag_ratio=0.25), rt=1.0)

class P3a(IntroScene):
    key = "P3a"; pid = "flux"
    def right(self):
        g, cap = picture(A + "flux_teaser.png", width=6.0, credit="图片来源：black-forest-labs/flux-3-image-klein 模型卡")
        g.move_to([3.7, 0.65, 0]); cap.next_to(g, DOWN, buff=0.1)
        cs = VGroup(chip("5.6B 图像 Transformer", color=BLUE, size=19), chip("最多 10 张参考图", color=BLUE, size=19)).arrange(RIGHT, buff=0.15).next_to(cap, DOWN, buff=0.22)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        self.P(FadeIn(cs, shift=UP * 0.15), rt=0.5)

class P4a(IntroScene):
    key = "P4a"; pid = "moss"
    def right(self):
        g, cap = picture(A + "moss_teaser.png", width=6.5, credit="图片来源：MOSS-Image 模型卡（Apache-2.0）")
        g.move_to([3.6, 0.85, 0]); cap.next_to(g, DOWN, buff=0.1)
        cs = VGroup(chip("5B DiT · 从头预训练", color=BLUE, size=20), chip("Base + SFT 两个版本", color=BLUE, size=20)).arrange(RIGHT, buff=0.15).next_to(cap, DOWN, buff=0.25)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        self.P(FadeIn(cs, shift=UP * 0.15), rt=0.5)

class P5a(IntroScene):
    key = "P5a"; pid = "ltx"
    def right(self):
        b = box(6.4, 5.4, color=BORDER, fill="#0F141B").move_to([3.6, 0.3, 0])
        t = T("近 30 天下载（本周五个模型的主仓库）", 22, FG, weight=BOLD)
        rows = [(DATA[p]["name"].replace("DeepSeek-V4.1-Flash-1017", "DeepSeek 1017"), DATA[p]["downloads_30d"], BLUE if p == "ltx" else DIM)
                for p in ["ltx", "flux", "deepseek", "moss", "flint"]]
        ch = hbars(rows, 2100000, bw=2.3, lw=2.3, size=18, h=0.36, gap=0.16, fmt="{:,}")
        src = T("来源：Hugging Face API（2026-10-24 18:15 CST）", 15, MUTED)
        ss = VGroup(chip("22B DiT", color=BLUE, size=19), chip("音视频一次生成", color=BLUE, size=19)).arrange(RIGHT, buff=0.12)
        VGroup(t, ch, src, ss).arrange(DOWN, buff=0.32).move_to(b)
        self.P(FadeIn(b), FadeIn(t), rt=0.5)
        self.P(grow(ch), FadeIn(src), rt=1.2)
        self.P(FadeIn(ss, shift=UP * 0.1), rt=0.4)

# ───────────────────────────── #1 DeepSeek-V4.1-Flash-1017
class P1b(Base):
    key = "P1b"
    def construct(self):
        self.head("deepseek", "设计")
        t0 = T("长程智能体：上下文越来越长 →", 24, FG, weight=BOLD)
        bot = VGroup(*[chip(s, color=ORANGE, size=20) for s in ["存储（HBM / SSD）", "带宽", "部署成本"]]).arrange(RIGHT, buff=0.15)
        prob = VGroup(t0, bot, T("主线：压缩 KV 缓存", 24, YELLOW, weight=BOLD)).arrange(RIGHT, buff=0.3).move_to(UP * 2.6)
        fit(prob, 13.2)
        self.P(FadeIn(t0), LaggedStart(*[FadeIn(c, scale=0.85) for c in bot], lag_ratio=0.2), rt=1.0)
        self.P(FadeIn(prob[2], shift=LEFT * 0.15), rt=0.5)
        self.W(self.cue(1))
        g, cap = picture(A + "ds_arch.png", width=6.6, credit="图片来源：DeepSeek-V4.1-Flash 技术报告 Fig.3（模型仓库内 PDF）")
        g.move_to([-3.6, 0.1, 0]); cap.next_to(g, DOWN, buff=0.08)
        c1 = card_rows("因果编码器 + 解码器（CED）", [("解码器的全局 KV = 编码器输出投影", None), ("多数提示词不必走完整解码器", None),
                       ("预填充计算接近减半", GREEN), ("激活参数：预填充 8B / 解码 16B", MUTED)], 6.2, BLUE, 20, 24)
        c1.move_to([3.6, -0.05, 0])
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.7)
        self.P(FadeIn(c1, shift=LEFT * 0.2), rt=0.6)
        self.W(self.cue(2))
        c2 = card_rows("跨层复用（CSA2）+ FP4", [("Full：本层计算全局 KV 并检索", None), ("Reindex：借用前层 KV，重新挑 Top-K", None),
                       ("Reuse：KV 和检索结果都借用", None), ("全局 KV 以 FP4 精度存储", GREEN)], 6.2, PURPLE, 20, 24)
        c2.move_to(c1)
        self.P(FadeOut(c1, shift=UP * 0.2), FadeIn(c2, shift=UP * 0.2), rt=0.6)
        self.W(self.cue(3))
        g2, cap2 = picture(A + "ds_kvcache.png", width=4.8, credit="图片来源：技术报告 Fig.1b（每 token 全局 KV 缓存字节数）")
        g2.move_to([3.65, 0.35, 0]); cap2.next_to(g2, DOWN, buff=0.08)
        self.P(FadeOut(c2), FadeIn(g2, shift=UP * 0.2), FadeIn(cap2), rt=0.7)
        q = chip("V4-Flash 3,514 B → V4.1-Flash 890 B（≈ 1/4）", color=GREEN, size=20).next_to(cap2, DOWN, buff=0.15)
        self.P(FadeIn(q, scale=0.85), rt=0.4)
        self.finish()

class P1c(Base):
    key = "P1c"
    def construct(self):
        self.head("deepseek", "评测与反响", GREEN)
        bm = DATA["deepseek"]["bench_card_1017"]
        cols = [("1017", BLUE), ("K3", PURPLE), ("GLM-5.3", PURPLE), ("GPT-5.6 Sol", ORANGE), ("Opus 5", ORANGE)]
        idx = [0, 2, 3, 4, 5]
        sel = [("DeepSWE v1.1", "DeepSWE"), ("Automation-Bench v1.0.6", "Automation-Bench"), ("Terminal-Bench 4.0", "Terminal-Bench 4.0"), ("HLE w/o tools", "HLE（无工具）")]
        ms = VGroup(*[mini(lab, [(c[0], bm[k][i], c[1]) for c, i in zip(cols, idx)], 100, bw=1.6, lw=1.35, size=15, h=0.19, gap=0.06, tsize=19) for k, lab in sel])
        grid = VGroup(VGroup(ms[0], ms[1]).arrange(RIGHT, buff=0.45, aligned_edge=UP), VGroup(ms[2], ms[3]).arrange(RIGHT, buff=0.45, aligned_edge=UP)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        lg = legend([("DeepSeek 1017", BLUE), ("开源对手", PURPLE), ("闭源旗舰", ORANGE)], 16)
        src = T("来源：DeepSeek-V4.1-Flash-1017 模型卡（官方自报）", 15, MUTED)
        Lf = VGroup(lg, grid, src).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, 0.45, 0]).to_edge(LEFT, buff=0.3)
        self.P(FadeIn(lg), *[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.1)) for m in ms], rt=1.6)
        self.P(FadeIn(src), rt=0.3)
        self.W(self.sub_t("但在专业知识"))
        hl = SurroundingRectangle(ms[3], color=ORANGE, buff=0.1, corner_radius=0.1)
        self.P(Create(hl), rt=0.5)
        self.W(self.cue(1))
        aa = DATA["deepseek"]["third_party"]["Artificial Analysis"]
        s1 = stat_card(str(aa["intelligence_index"]), "AA 智能指数", 1.95, 1.3, BLUE, 34, 16, "开放权重第 2 / 121")
        s2 = stat_card("195", "输出 token/秒", 1.95, 1.3, GREEN, 34, 16, "$0.30 / $1.20 每百万")
        s3 = stat_card("2.1 亿", "跑完指数的输出 token", 1.95, 1.3, ORANGE, 28, 16, "中位数 1.4 亿")
        ss = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.12)
        at = T("Artificial Analysis（第三方，2026-10-24 查询）", 18, MUTED)
        AA = VGroup(at, ss).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.75, 2.15, 0])
        self.P(FadeIn(at), LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in ss], lag_ratio=0.25), rt=1.0)
        self.W(self.cue(2))
        ht = T("Hacker News · 943 分 · 707 条评论", 18, MUTED)
        q1 = quote("称赞最多：速度快、性价比高", 6.1, "讨论观点（归纳，非原话）", GREEN, 20)
        q2 = quote("也有反馈：真实代码审查里不如顶级闭源模型", 6.1, "讨论观点（归纳，非原话）", RED, 20)
        HN = VGroup(ht, q1, q2).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(AA, DOWN, buff=0.22).align_to(AA, LEFT)
        self.P(FadeIn(ht), FadeIn(q1, shift=LEFT * 0.2), FadeIn(q2, shift=LEFT * 0.2), rt=0.7)
        self.W(self.sub_t("这份底气"))
        lb = box(13.2, 0.72, color=BLUE, r=0.12).move_to(DOWN * 2.35)
        lt = fit(VGroup(M("KV 缓存 ≈ 上一代 Flash 的 1/4", 24, BLUE, weight=BOLD), T("→", 26, MUTED), T("同样的硬件，更快、更便宜、上下文更长", 25, FG)).arrange(RIGHT, buff=0.3), 12.6).move_to(lb)
        self.P(FadeIn(VGroup(lb, lt), shift=UP * 0.2), rt=0.6)
        self.finish()
    def sub_t(self, prefix):
        for x in self.tm["subs"]:
            if x["text"].startswith(prefix): return x["start"]
        for x in self.tm["subs"]:
            if prefix in x["text"]: return x["start"]
        return self.t

# ───────────────────────────── #2 Flint
def mask(kind, n=10, s=0.14, col=BLUE):
    g = VGroup()
    for i in range(n):
        for j in range(n):
            on = j <= i and (kind == "full" or i - j < 3)
            g.add(Square(s).set_stroke(BORDER, 0.6).set_fill(col if on else PANEL, 0.9 if on else 1).move_to([j * s, -i * s, 0]))
    return g

class P2b(Base):
    key = "P2b"
    def construct(self):
        self.head("flint", "设计")
        m1 = mask("swa", col=BLUE); m2 = mask("full", col=ORANGE)
        l1 = VGroup(T("35 层 · 滑动窗口", 21, FG, weight=BOLD), T("窗口 513 token · RoPE", 17, MUTED)).arrange(DOWN, buff=0.06)
        l2 = VGroup(T("14 层 · 全局注意力", 21, FG, weight=BOLD), T("不加位置编码（NoPE）", 17, MUTED)).arrange(DOWN, buff=0.06)
        g1 = VGroup(m1, l1).arrange(DOWN, buff=0.18); g2 = VGroup(m2, l2).arrange(DOWN, buff=0.18)
        att = VGroup(g1, g2).arrange(RIGHT, buff=0.7)
        ab = box(6.5, att.height + 0.9, color=BLUE, fill="#0F141B")
        at = T("注意力分工（示意）", 18, MUTED)
        A1 = VGroup(ab, att, at); att.move_to(ab).shift(DOWN * 0.15); at.move_to(ab.get_top() + DOWN * 0.25)
        A1.move_to([-3.45, 3.0 - A1.height / 2, 0])
        ex = T("另：QK RMSNorm · 可学习 attention sink", 16, MUTED).next_to(ab, DOWN, buff=0.1)
        self.P(FadeIn(ab), FadeIn(at), FadeIn(m1), FadeIn(l1), rt=0.6)
        self.P(FadeIn(m2), FadeIn(l2), FadeIn(ex), rt=0.6)
        self.W(self.cue(1))
        n1 = node("35B-A3B 基线", 2.2, 0.8, DIM, 21)
        n2 = node("Eureka Machine", 2.3, 0.8, PURPLE, 20, "自动化研究系统")
        n3 = node("40B-A2.5B", 1.9, 0.8, BLUE, 21)
        fl = VGroup(n1, n2, n3).arrange(RIGHT, buff=0.35)
        ar = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.35) for a, b in zip(fl[:-1], fl[1:])])
        st = VGroup(*[chip(s, color=BORDER, size=17) for s in ["预训练", "中期训练", "SFT", "RL"]]).arrange(RIGHT, buff=0.1)
        sl = T("从零训练 · 小团队 · 不到 4 个月", 18, MUTED)
        eb = box(6.6, 2.25, color=PURPLE, fill="#0F141B")
        et = T("研发：架构搜索交给自动化系统", 21, PURPLE, weight=BOLD)
        E = VGroup(et, fit(VGroup(fl, ar), 6.1), VGroup(st, sl).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.22)
        fit(E[2], 6.1)
        eb.stretch_to_fit_height(E.height + 0.45)
        VGroup(eb).move_to([3.5, 3.0 - eb.height / 2, 0]); E.move_to(eb)
        self.P(FadeIn(eb), FadeIn(et), FadeIn(n1), rt=0.5)
        self.P(GrowArrow(ar[0]), FadeIn(n2), GrowArrow(ar[1]), FadeIn(n3), rt=0.9)
        self.P(FadeIn(E[2], shift=UP * 0.1), rt=0.4)
        self.W(self.cue(2))
        qb = box(13.4, 2.0, color=GREEN, fill="#0F141B").move_to([0, -1.25, 0])
        qt = T("量化：连输出层（lm_head）也压到 4 bit", 22, GREEN, weight=BOLD)
        left = VGroup(T("常规做法", 17, MUTED), T("lm_head 保持高精度", 20, FG)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        why = VGroup(T("为什么能动它", 17, MUTED), T("激活仅 ~2.5B，输出层占每 token 读取量的一大块", 20, FG)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        how = VGroup(T("怎么补回精度", 17, MUTED), T("16 bit 教师 · 自选 coreset · 离线自蒸馏（步数约为 QAT 一半）", 20, FG)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        row1 = VGroup(left, why).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        Q = VGroup(qt, row1, how).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fit(Q, 12.8)
        top = min(ex.get_bottom()[1], eb.get_bottom()[1]) - 0.2
        qb.stretch_to_fit_height(Q.height + 0.4).move_to([0, top - (Q.height + 0.4) / 2, 0])
        Q.move_to(qb).align_to(qb.get_left() + RIGHT * 0.3, LEFT)
        srcq = T("来源：Recursive 官方博客 “Introducing Recursive Flint”", 15, MUTED)
        self.P(FadeIn(qb), FadeIn(qt), rt=0.5)
        self.P(FadeIn(left, shift=UP * 0.1), rt=0.4)
        self.P(FadeIn(why, shift=UP * 0.1), rt=0.5)
        self.W(self.sub_t("于是也被压到"))
        self.P(FadeIn(how, shift=UP * 0.1), rt=0.5)
        self.W(self.cue(3))
        cs = VGroup(chip("NVFP4 与 BF16 六项平均差 0.6 分", color=GREEN, size=19), chip("Metal 解码 megakernel（M4 / M5）", color=BLUE, size=19)).arrange(RIGHT, buff=0.2)
        srcq2 = VGroup(cs, srcq).arrange(RIGHT, buff=0.35)
        fit(srcq2, 13.2).next_to(qb, DOWN, buff=0.16)
        self.P(FadeIn(srcq2, shift=UP * 0.1), rt=0.5)
        self.finish()
    def sub_t(self, prefix):
        for x in self.tm["subs"]:
            if prefix in x["text"]: return x["start"]
        return self.t

class P2s(Base):
    key = "P2s"
    def construct(self):
        self.head("flint", "实测：社区 Space")
        meta = json.load(open("demo/flint_sample.json"))
        code = meta["response"][-1]["content"].strip().strip("`").replace("python\n", "", 1).strip()
        b = box(8.0, 5.55, color=BORDER, fill="#0F141B").move_to([-3.02, 0.3, 0])
        pt = T("输入", 17, MUTED)
        pr = para(meta["message"], 78, 15, FG, MONO, 0.27)
        ot = T("输出（思考 4 秒后给出）", 17, MUTED)
        cw = M("x" * 20, 17).width / 20
        cl = VGroup(*[M(l.strip() if l.strip() else ".", 17, "#C9D1D9") for l in code.split("\n")])
        for i, (l, raw) in enumerate(zip(cl, code.split("\n"))):
            l.move_to([cw * (len(raw) - len(raw.lstrip())), -i * 0.31, 0], aligned_edge=LEFT)
            if not raw.strip(): l.set_opacity(0)
        lines = code.split("\n")
        for i, l in enumerate(lines):
            if "assert" in l: cl[i].set_color(YELLOW)
        inner = VGroup(pt, pr, ot, cl).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fit(inner, 7.5)
        if inner.height > 5.25: inner.scale_to_fit_height(5.25)
        inner.move_to(b).align_to(b.get_left() + RIGHT * 0.22, LEFT)
        cap = T("社区 Space mrfakename/flint（非官方）· 54.4 tok/s 为共享 GPU 速度，不代表本地", 15, MUTED).next_to(b, DOWN, buff=0.08)
        fit(cap, 7.6)
        self.P(FadeIn(b), FadeIn(pt), FadeIn(pr), FadeIn(cap), rt=0.6)
        self.P(FadeIn(ot), LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in cl], lag_ratio=0.08), rt=1.6)
        self.W(self.cue(1))
        def item(ok, a, b_):
            ic = T("✓" if ok else "✗", 26, GREEN if ok else RED, weight=BOLD)
            tx = VGroup(T(a, 20, FG, weight=BOLD), T(b_, 16, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            return VGroup(ic, tx).arrange(RIGHT, buff=0.2, aligned_edge=UP)
        its = VGroup(item(True, "列表输入结果正确", "[[8,10],[1,3],[2,6],[15,18]] → [[1,6],[8,10],[15,18]]"),
                     item(False, "两条 assert 写成了输入检查", "非空、每项长度为 2，没有测试用例"),
                     item(False, "原地修改传入的列表", "sort() 和 merged[-1][1] 都改了原数据"),
                     item(False, "元组输入直接报错", "TypeError: 'tuple' object does not support item assignment")).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rb = box(5.4, its.height + 0.9, color=GREEN, fill="#0F141B")
        rt = T("我们在本机检查这段代码", 18, MUTED)
        fit(its, 5.0)
        R = VGroup(rb, rt, its); rt.move_to(rb.get_top() + DOWN * 0.3).align_to(rb.get_left() + RIGHT * 0.25, LEFT)
        its.next_to(rt, DOWN, buff=0.22).align_to(rt, LEFT)
        R.move_to([4.15, 0.3, 0])
        self.P(FadeIn(rb), FadeIn(rt), FadeIn(its[0], shift=LEFT * 0.15), rt=0.6)
        self.W(self.sub_t("但它把"))
        self.P(FadeIn(its[1], shift=LEFT * 0.15), rt=0.4)
        self.W(self.sub_t("还会直接改动"))
        self.P(FadeIn(its[2], shift=LEFT * 0.15), FadeIn(its[3], shift=LEFT * 0.15), rt=0.5)
        self.finish()
    def sub_t(self, prefix):
        for x in self.tm["subs"]:
            if prefix in x["text"]: return x["start"]
        return self.t

class P2c(Base):
    key = "P2c"
    def construct(self):
        self.head("flint", "评测与反响", GREEN)
        bc = DATA["flint"]["bench_card"]; cols = bc["cols"]
        pick = [("Flint BF16", BLUE), ("Qwen3.6", PURPLE), ("Qwen3.8", ORANGE), ("Muse Glimmer", ORANGE)]
        names = ["Terminal-Bench 2.1", "SWE-bench Pro v2", "SWE-bench Verified", "LiveCodeBench v6", "IFBench", "IFEval"]
        ms = VGroup(*[mini(n, [(p.replace("Flint BF16", "Flint"), bc[n][cols.index(p)], c) for p, c in pick], 100, bw=1.55, lw=1.45, size=15, h=0.2, gap=0.06, tsize=19, fmt="{:.1f}") for n in names])
        grid = VGroup(VGroup(*ms[:3]).arrange(RIGHT, buff=0.55, aligned_edge=UP), VGroup(*ms[3:]).arrange(RIGHT, buff=0.55, aligned_edge=UP)).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        lg = legend([("Flint（BF16）", BLUE), ("稀疏 MoE 33–35B · 3B 激活", PURPLE), ("稠密 27–31B", ORANGE)], 16)
        src = T("来源：RecursiveSI/flint 模型卡对比图（官方自报，部分对手分数为官方内部测得）", 15, MUTED)
        L = VGroup(lg, grid, src).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        fit(L, 13.2).move_to([0, 3.0 - L.height / 2, 0])
        self.P(FadeIn(lg), *[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.1)) for m in ms], rt=1.6)
        self.P(FadeIn(src), rt=0.3)
        self.W(self.sub_t("对上更大的稠密模型"))
        hl = VGroup(*[SurroundingRectangle(ms[i][1][2], color=ORANGE, buff=0.04, corner_radius=0.05) for i in range(4)])
        hl2 = VGroup(*[SurroundingRectangle(ms[i][1][0], color=GREEN, buff=0.04, corner_radius=0.05) for i in (4, 5)])
        self.P(Create(hl), rt=0.6)
        self.P(Create(hl2), rt=0.5)
        self.W(self.cue(1))
        s1 = stat_card("未收录", "Artificial Analysis 等第三方", 3.4, 1.05, DIM, 26, 16, "2026-10-24 检查")
        s2 = stat_card("27 分 · 5 条评论", "Hacker News 讨论", 3.4, 1.05, ORANGE, 24, 16)
        s3 = stat_card("54.9 vs 73.0", "Terminal-Bench：Flint vs Qwen3.8", 3.4, 1.05, BLUE, 24, 16)
        ss = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.2).next_to(L, DOWN, buff=0.25)
        self.P(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in ss], lag_ratio=0.3), rt=1.0)
        self.finish()
    def sub_t(self, prefix):
        for x in self.tm["subs"]:
            if prefix in x["text"]: return x["start"]
        return self.t

# ───────────────────────────── #3 FLUX 3 Image Klein
class P3b(Base):
    key = "P3b"
    def construct(self):
        self.head("flux", "设计与实测")
        n1 = node("一句话需求", 2.2, 0.95, DIM, 22)
        n2 = node("提示扩写模型", 2.5, 0.95, PURPLE, 22, "官方单独提供")
        n3 = node("完整场景描述", 2.3, 0.95, DIM, 22)
        n4 = node("Klein 5.6B", 2.6, 0.95, BLUE, 24, "文本编码：Qwen3-VL-4B")
        n5 = node("图像", 1.4, 0.95, GREEN, 22)
        ns = VGroup(n1, n2, n3, n4, n5).arrange(RIGHT, buff=0.42).move_to(UP * 2.35)
        ar = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.35) for a, b in zip(ns[:-1], ns[1:])])
        refc = chip("+ 最多 10 张参考图", color=BLUE, size=18).next_to(n4, DOWN, buff=0.15)
        self.P(FadeIn(n4, shift=UP * 0.15), FadeIn(n5), GrowArrow(ar[3]), rt=0.7)
        self.P(FadeIn(refc), rt=0.4)
        self.W(self.cue(1))
        warn = chip("官方提醒：别直接喂短提示", color=ORANGE, size=18).next_to(n2, DOWN, buff=0.15)
        self.P(LaggedStart(FadeIn(n1), GrowArrow(ar[0]), FadeIn(n2), GrowArrow(ar[1]), FadeIn(n3), GrowArrow(ar[2]), lag_ratio=0.3), rt=1.4)
        self.P(FadeIn(warn), rt=0.4)
        self.W(self.cue(2))
        self.P(FadeOut(refc), FadeOut(warn), rt=0.3)
        g, cap = picture(A + "flux_sample.png", height=3.55, credit="我们用官方 Space 生成：蒸馏版 16 步 · 开启提示扩写")
        g.move_to([-4.6, -0.35, 0]); fit(cap, 4.6).next_to(g, DOWN, buff=0.08)
        meta = json.load(open("demo/flux_sample.json"))
        b1 = box(8.4, 1.05, color=DIM, fill="#0F141B")
        p1 = para(meta["prompt"], 92, 15, FG, MONO, 0.27)
        G1 = VGroup(T("输入（一句话）", 17, MUTED), p1).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        ups = ". ".join(meta["upsampled"].split(". ")[:3]) + ". …"
        b2 = box(8.4, 1.85, color=PURPLE, fill="#0F141B")
        p2 = para(ups.replace("..", "."), 92, 15, FG, MONO, 0.27)
        G2 = VGroup(T("扩写模型的输出（节选）", 17, PURPLE), p2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        fit(G1, 8.0)
        if G2.height > 1.65: G2.scale_to_fit_height(1.65)
        fit(G2, 8.0)
        VGroup(b1, b2).arrange(DOWN, buff=0.3).move_to([2.55, -0.35, 0])
        G1.move_to(b1).align_to(b1.get_left() + RIGHT * 0.2, LEFT)
        G2.move_to(b2).align_to(b2.get_left() + RIGHT * 0.2, LEFT)
        arr = Arrow(b1.get_bottom(), b2.get_top(), buff=0.03, color=PURPLE, stroke_width=3, max_tip_length_to_length_ratio=0.5)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), FadeIn(b1), FadeIn(G1), rt=0.7)
        self.P(GrowArrow(arr), FadeIn(b2), FadeIn(G2, shift=DOWN * 0.1), rt=0.8)
        self.W(self.sub_t("生成的标题文字"))
        hl = Rectangle(width=g[0].width * 0.86, height=g[0].height * 0.11, color=GREEN, stroke_width=4).move_to(g[0].get_top() + DOWN * g[0].height * 0.075)
        self.P(Create(hl), rt=0.5)
        self.finish()
    def sub_t(self, prefix):
        for x in self.tm["subs"]:
            if prefix in x["text"]: return x["start"]
        return self.t

class P3c(Base):
    key = "P3c"
    def construct(self):
        self.head("flux", "控制、门槛与评测", GREEN)
        g, cap = picture(A + "ui_flux.png", width=5.9, credit="界面截图：Space black-forest-labs/flux-3-image-klein（边界框模式）")
        g.move_to([-3.85, 1.05, 0]); fit(cap, 5.6).next_to(g, DOWN, buff=0.08)
        bb = card_rows("边界框控制", [("在 0–1000 坐标网格上给元素划位置", None), ("可移动、替换、删除指定元素", None), ("框只是引导，不是硬遮罩", ORANGE)], 6.6, BLUE, 20, 24)
        bb.move_to([3.3, 2.95 - bb.height / 2, 0])
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.6)
        self.P(FadeIn(bb, shift=LEFT * 0.2), rt=0.6)
        self.W(self.cue(1))
        vr = hbars([("BF16", 11.2, DIM), ("FP8", 5.6, DIM), ("INT8", None, GREEN)], 12, bw=3.4, lw=0.9, size=18, h=0.26, gap=0.08, fmt="{:g} GB")
        vr[2][2].become(T("8GB 消费级显卡可跑", 18, GREEN).next_to(vr[2][1], RIGHT, buff=0.1))
        vt = T("显存占用（官方）", 18, MUTED)
        V = VGroup(vt, vr).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        V.next_to(bb, DOWN, buff=0.3).align_to(bb, LEFT)
        self.P(FadeIn(vt), grow(vr, 0.2), rt=1.0)
        self.W(self.cue(2))
        s1 = stat_card("47%", "Design Arena 胜率", 3.0, 1.2, BLUE, 32, 17, "Elo 1165 · 第 48 名 · 2026-10-24")
        s2 = stat_card("未收录", "Artificial Analysis", 3.0, 1.2, DIM, 28, 17, "只列完整版 FLUX 3（Elo 1117）")
        s3 = stat_card("+91 Elo", "官方内部评测（自报）", 3.0, 1.2, ORANGE, 30, 17, "文生图，对比 FLUX.2 [klein] 9B")
        ss = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.2).move_to([0, -1.95, 0])
        self.P(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in ss], lag_ratio=0.3), rt=1.0)
        self.finish()

# ───────────────────────────── #4 MOSS-Image
class P4b(Base):
    key = "P4b"
    def construct(self):
        self.head("moss", "设计")
        g, cap = picture(A + "moss_arch.png", width=7.4, credit="图片来源：MOSS-Image 技术报告 Fig.2（arXiv:2610.23374）")
        g.move_to([-3.35, 0.65, 0]); cap.next_to(g, DOWN, buff=0.1)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.7)
        n1 = node("负责“想”", 2.9, 0.9, PURPLE, 24, "提示增强智能体")
        n2 = node("负责“画”", 2.9, 0.9, BLUE, 24, "5B 单流 DiT · 从头预训练")
        two = VGroup(n1, n2).arrange(RIGHT, buff=0.3).move_to([3.6, 2.35, 0])
        self.P(FadeIn(n1, shift=DOWN * 0.15), FadeIn(n2, shift=DOWN * 0.15), rt=0.6)
        self.W(self.cue(1))
        st = step_list([("任务路由", "海报？信息图？界面？"), ("检索", "查资料、找参考图"), ("版面构建", "输出带坐标的 JSON 版面描述")], 5.8, 21, PURPLE)
        st.next_to(two, DOWN, buff=0.4).align_to(two, LEFT).shift(RIGHT * 0.1)
        self.P(LaggedStart(*[FadeIn(r, shift=LEFT * 0.15) for r in st], lag_ratio=0.3), rt=1.2)
        self.W(self.cue(2))
        old = Group(g, cap, two, st)
        g2, cap2 = picture(A + "moss_layout.png", width=11.4, credit="图片来源：MOSS-Image 模型卡（版面控制示例）")
        g2.move_to([0, 1.2, 0]); cap2.next_to(g2, DOWN, buff=0.1)
        k1 = chip("自然语言提示 + JSON 版面 → 同一条文本通道", color=BLUE, size=22)
        k2 = chip("训练时保留文字换行：换行本身就是版式", color=BLUE, size=22)
        ks = VGroup(k1, k2).arrange(RIGHT, buff=0.3).next_to(cap2, DOWN, buff=0.3)
        fit(ks, 13)
        self.P(FadeOut(old), rt=0.4)
        self.P(FadeIn(g2, shift=UP * 0.2), FadeIn(cap2), rt=0.7)
        self.P(LaggedStart(FadeIn(k1, shift=UP * 0.1), FadeIn(k2, shift=UP * 0.1), lag_ratio=0.5), rt=0.9)
        self.W(self.cue(3))
        dd = VGroup(box(13.2, 0.72, color=ORANGE, r=0.12))
        dt = fit(VGroup(T("数据", 24, ORANGE, weight=BOLD), T("标注而不是过滤：水印、模糊等瑕疵写进描述，而不是直接丢弃", 25, FG)).arrange(RIGHT, buff=0.35), 12.6).move_to(dd)
        self.P(FadeIn(VGroup(dd, dt).move_to(DOWN * 2.3), shift=UP * 0.2), rt=0.6)
        self.finish()

class P4c(Base):
    key = "P4c"
    def construct(self):
        self.head("moss", "实测与评测", GREEN)
        g, cap = picture(A + "moss_sample.png", height=4.3, credit="我们用官方 Space 生成：MOSS-Image-Base · 1024² · 50 步")
        g.move_to([-4.55, 0.85, 0]); fit(cap, 4.6).next_to(g, DOWN, buff=0.1)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        h1 = Rectangle(width=g[0].width * 0.66, height=g[0].height * 0.13, color=GREEN, stroke_width=4).move_to(g[0].get_top() + DOWN * g[0].height * 0.18)
        h2 = Rectangle(width=g[0].width * 0.66, height=g[0].height * 0.08, color=GREEN, stroke_width=4).move_to(g[0].get_top() + DOWN * g[0].height * 0.835)
        self.P(Create(h1), Create(h2), rt=0.6)
        self.W(self.cue(1))
        lt = [("GPT Image 2", 99.0), ("Nano Banana Pro", 96.6), ("MOSS-Image", 96.3), ("Qwen Image 3.0 Pro", 94.3),
              ("Qwen Image 2512", 64.9), ("Ideogram 4.0", 63.5), ("ERNIE", 55.7), ("FLUX.2", 11.8)]
        t = T("LLTB 长文本渲染（Mean-6，越高越好）", 22, FG, weight=BOLD)
        ch = hbars([(n, v, BLUE if "MOSS" in n else DIM) for n, v in lt], 100, bw=3.9, lw=2.7, size=17, h=0.26, gap=0.08, fmt="{:.1f}")
        R = VGroup(t, ch).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        R.move_to([2.4, 3.0 - R.height / 2, 0])
        k1 = chip("RLA Elo 1698.7 · 仅次于 GPT Image 2（1844.4）", color=BLUE, size=18)
        k2 = chip("7Bench 版面 mIoU 0.88 vs Ideogram 4.0 的 0.44", color=BLUE, size=18)
        ks = VGroup(k1, k2).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(R, DOWN, buff=0.25).align_to(t, LEFT)
        self.P(FadeIn(t), grow(ch), rt=1.4)
        self.P(FadeIn(ks, shift=UP * 0.1), rt=0.5)
        self.W(self.cue(2))
        note = chip("以上评测均由 MOSS 团队自行完成（arXiv:2610.23374）· 暂无第三方榜单收录", color=ORANGE, size=18)
        note.next_to(ks, DOWN, buff=0.15).align_to(ks, LEFT)
        fit(note, 6.85 - ks.get_left()[0]).next_to(ks, DOWN, buff=0.15).align_to(ks, LEFT)
        self.P(FadeIn(note, shift=UP * 0.1), rt=0.5)
        self.finish()

# ───────────────────────────── #5 LTX-2.5
class P5b(Base):
    key = "P5b"
    def construct(self):
        self.head("ltx", "设计")
        g, cap = picture(A + "ltx_arch.png", width=8.0, credit="图片来源：LTX-2 论文 Fig.1（arXiv:2601.03233）")
        g.move_to([-2.85, 1.0, 0]); cap.next_to(g, DOWN, buff=0.08)
        c1 = card_rows("非对称双流", [("视频流 14B + 音频流 5B（LTX-2）", None), ("双向音视频交叉注意力", None), ("交叉注意力只用时间维 RoPE", GREEN), ("LTX-2.5 整体 22B", MUTED)], 4.7, BLUE, 19, 23)
        c1.move_to([4.55, 2.95 - c1.height / 2, 0])
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.7)
        self.P(FadeIn(c1, shift=LEFT * 0.2), rt=0.6)
        self.W(self.cue(1))
        g2, cap2 = picture(A + "ltx_attn.png", height=4.6, credit="图片来源：LTX-2 论文 注意力可视化（Q: 音频，KV: 视频）")
        g2.move_to([3.85, 0.6, 0]); fit(cap2, 6.2).next_to(g2, DOWN, buff=0.08)
        l1 = chip("车驶过：声音盯着车", color=YELLOW, size=19)
        l2 = chip("轮流说话：焦点跟着说话人", color=YELLOW, size=19)
        VGroup(l1, l2).arrange(RIGHT, buff=0.2).next_to(cap, DOWN, buff=0.3).align_to(g, LEFT)
        self.P(FadeOut(c1), rt=0.3)
        self.P(FadeIn(g2, shift=UP * 0.2), FadeIn(cap2), rt=0.7)
        self.P(FadeIn(l1, shift=UP * 0.1), rt=0.4)
        self.W(self.sub_t("两个人轮流"))
        self.P(FadeIn(l2, shift=UP * 0.1), rt=0.4)
        self.W(self.cue(2))
        st = step_list([("原生多镜头", "一次生成，跨镜头保持人物、光线和声音"), ("扩散视频解码器", "取代 VAE 重建：脸、纹理、画面文字更清晰"),
                        ("按复杂度分配算力", "diffusion fidelity rendering"), ("Gemma 4 12B 文本编码 + 提示增强", "另有可选的时长预测头"),
                        ("蒸馏版 8 步 · CFG=1", "画质与动作一致性明显改进")], 6.0, 21, BLUE)
        tt = T("LTX-2.5 的新变化（模型卡）", 22, BLUE, weight=BOLD)
        S = VGroup(tt, st).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        if S.height > 5.6: S.scale_to_fit_height(5.6)
        S.move_to([-3.6, 3.0 - S.height / 2, 0])
        self.P(FadeOut(l1), FadeOut(l2), FadeOut(g), FadeOut(cap), rt=0.4)
        self.P(FadeIn(tt), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in st], lag_ratio=0.25), rt=1.6)
        self.finish()
    def sub_t(self, prefix):
        for x in self.tm["subs"]:
            if prefix in x["text"]: return x["start"]
        return self.t

class P5s(Base):
    key = "P5s"
    VBOX = (-0.55, 0.45, 4.6)   # 视频画框中心 x, y 与边长（单位）
    def construct(self):
        self.head("ltx", "实测：官方 Space")
        meta = json.load(open("demo/ltx_sample.json"))
        g, cap = picture("demo/flux_sample.png", height=2.5, credit="输入：前面 FLUX Klein 生成的海报")
        g.move_to([-5.2, 1.6, 0]); fit(cap, 3.4).next_to(g, DOWN, buff=0.08)
        cx, cy, s = self.VBOX
        fr = Square(s).set_stroke(BORDER, 2).set_fill(BLACK, 1).move_to([cx, cy, 0])
        first = ImageMobject("demo/ltx_f_0.1.png").scale_to_fit_width(s).move_to(fr)
        vc = T("LTX-2.5 实际输出（768² · 3 秒 · 循环播放）", 17, MUTED).next_to(fr, DOWN, buff=0.08)
        arr = Arrow(g.get_right(), fr.get_left(), buff=0.12, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        rows = VGroup(
            VGroup(T("提示词", 17, MUTED), para(meta["prompt"], 44, 15, FG, MONO, 0.27)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(T("设置", 17, MUTED), T("扩散解码器 · 提示增强开启 · seed 24", 18, FG)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rb = box(4.75, 2.6, color=BLUE, fill="#0F141B")
        fit(rows, 4.4)
        rb.stretch_to_fit_height(rows.height + 0.45).move_to([4.6, 2.95 - (rows.height + 0.45) / 2, 0])
        rows.move_to(rb).align_to(rb.get_left() + RIGHT * 0.2, LEFT)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.6)
        self.P(GrowArrow(arr), FadeIn(fr), FadeIn(first), FadeIn(vc), FadeIn(rb), FadeIn(rows), rt=0.6)
        self.ov_start = self.t
        strip = Group(*[ImageMobject(f"demo/ltx_f_{t}.png").scale_to_fit_width(1.1) for t in ("0.1", "1.5", "2.9")]).arrange(RIGHT, buff=0.08)
        sl = T("抽帧：0.1 / 1.5 / 2.9 秒", 16, MUTED)
        SG = Group(strip, sl).arrange(DOWN, buff=0.08).next_to(cap, DOWN, buff=0.3)
        self.W(self.cue(1))
        self.P(FadeIn(SG, shift=UP * 0.1), rt=0.5)
        warn = chip("推镜过猛：结尾整个画面被气球的脸占满", color=ORANGE, size=18)
        fit(warn, 4.75).next_to(rb, DOWN, buff=0.25).align_to(rb, LEFT)
        self.W(self.sub_t("可惜推得太猛"))
        self.P(FadeIn(warn, shift=UP * 0.1), Create(SurroundingRectangle(strip[2], color=ORANGE, buff=0.03)), rt=0.5)
        # 视频叠加位置（像素）与时间段，供 assemble 使用
        X0 = int(round(960 + (cx - s / 2) * PX)); Y0 = int(round(540 - (cy + s / 2) * PX)); SZ = int(round(s * PX))
        os.makedirs("build", exist_ok=True)
        json.dump({"x": X0, "y": Y0, "size": SZ, "start": round(self.ov_start, 3), "end": round(self.tm["total"] - 0.6, 3)}, open("build/overlay_P5s.json", "w"))
        self.finish()
    def sub_t(self, prefix):
        for x in self.tm["subs"]:
            if prefix in x["text"]: return x["start"]
        return self.t

class P5c(Base):
    key = "P5c"
    def construct(self):
        self.head("ltx", "评测与生态", GREEN)
        aa = DATA["ltx"]["third_party"]["Artificial Analysis T2V v2.1 开放权重（带音频）"]
        rows = [(k, v, BLUE if "2.5" in k else (ORANGE if "MiniMax" in k else DIM)) for k, v in aa.items() if isinstance(v, int)]
        t1 = T("Artificial Analysis 视频竞技场 · 开放权重 · 带音频", 26, FG, weight=BOLD)
        s1 = T("Elo，横轴从 800 起 · 2026-10-24 查询", 18, MUTED)
        ch = hbars(rows, 1200, bw=3.4, lw=2.7, size=22, h=0.46, gap=0.2, base=800)
        n1 = VGroup(T("Fast / Pro 为 LTX API 的两档", 18, MUTED),
                    T("总榜第一为 Wan 3.0（1175），LTX-2.5 排第 24、25", 18, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        Lg = VGroup(VGroup(t1, s1).arrange(DOWN, aligned_edge=LEFT, buff=0.08), ch, n1).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        Lg.scale_to_fit_width(6.6).move_to([-3.45, 0.45, 0])
        self.P(FadeIn(Lg[0]), grow(ch), rt=1.3)
        self.P(FadeIn(n1), rt=0.4)
        self.W(self.cue(1))
        c = card_rows("为什么还挂在热榜上", [("权重按 ComfyUI 组件格式拆分发布", None), ("多数 LTX-2.3 LoRA 可直接沿用", None),
                      ("年收入 < 1000 万美元免费商用", GREEN), ("10 月：LTX Desktop 1.3.1 新增 IC-LoRA、4K", MUTED)], 6.2, GREEN, 20, 24)
        c.move_to([3.65, 0.45, 0])
        self.P(FadeIn(c, shift=LEFT * 0.2), rt=0.7)
        src = T("来源：Lightricks/LTX-2.5 模型卡、LTX 官方更新", 15, MUTED).next_to(c, DOWN, buff=0.12).align_to(c, LEFT)
        self.P(FadeIn(src), rt=0.3)
        self.finish()

# ───────────────────────────── 结尾
class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        t = T("本周回顾", 40, HF, weight=BOLD).move_to(UP * 2.85)
        self.P(FadeIn(t, shift=DOWN * 0.15), rt=0.5)
        tag = {"deepseek": "KV 缓存压到上一代的约 1/4", "flint": "2.5B 激活 · 笔记本上跑编程智能体", "flux": "5.6B · 量化后 8GB 显卡可跑",
               "moss": "先规划版面、再渲染长文本", "ltx": "音视频一起生成 · ComfyUI 生态"}
        rows = Group()
        for pid in ["deepseek", "flint", "flux", "moss", "ltx"]:
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
        self.W(self.cue(1))
        self.P(FadeOut(rows), rt=0.4)
        rp = DJ["on_screen_charts"]["repack_downloads"]
        tt = T("近 30 天下载：原仓库 vs 打包版", 26, FG, weight=BOLD)
        grp = VGroup()
        for r in rp:
            mx = max(r["original_dl"], r["repack_dl"])
            lab = T(r["model"], 21, FG, weight=BOLD)
            bars = hbars([("原仓库", r["original_dl"], DIM), (r["label"], r["repack_dl"], GREEN if r["repack_dl"] > r["original_dl"] else DIM)],
                         mx, bw=3.2, lw=2.6, size=16, h=0.24, gap=0.06, fmt="{:,}")
            grp.add(VGroup(lab, bars).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        gg = VGroup(VGroup(grp[0], grp[1]).arrange(RIGHT, buff=0.9, aligned_edge=UP), VGroup(grp[2], grp[3]).arrange(RIGHT, buff=0.9, aligned_edge=UP)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        src = T("每行各自按最大值缩放 · 来源：Hugging Face API（2026-10-24），创建不足 30 天的仓库为创建以来累计", 15, MUTED)
        C = VGroup(tt, gg, src).arrange(DOWN, buff=0.28)
        C.scale_to_fit_width(12.6)
        if C.height > 5.3: C.scale_to_fit_height(5.3)
        C.move_to([0, 0.2, 0])
        self.P(FadeIn(tt), *[AnimationGroup(FadeIn(g_[0]), grow(g_[1], 0.2)) for g_ in grp], FadeIn(src), rt=1.6)
        self.W(self.cue(2))
        bye = T("下周见", 36, HF, weight=BOLD).next_to(t, RIGHT, buff=0.6)
        self.P(FadeIn(bye, scale=0.8), rt=0.4)
        self.finish()
