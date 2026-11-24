"""Hugging Face 本周热门 Top 5（2026 第 45 周）—— Manim CE 场景。时间轴由 timing.json（MiniMax 词级时间戳）驱动；
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
    "kimi": dict(chips=["image-text-to-text", "Kimi K3.1-Pro 许可（改版 MIT）", "权重上传于 2026-11-02"], what="2.8T 总参数 · 104B 激活的多模态智能体模型", note="月之暗面 · 1M 上下文 · 基于 Kimi K3 后训练"),
    "idol": dict(chips=["image-to-3d", "Apache-2.0", "发布于 2026-10-28"], what="一张照片 → 可以转着看的 3D 高斯模型", note="自有参数 0.66B · 峰值显存 7.2 GB（官方）"),
    "coder3d": dict(chips=["Qwen3.5-4B 微调", "Apache-2.0", "上传于 2026-10-25"], what="4B 小模型，专写 Three.js 三维场景", note="姊妹模型 GLB-3D-Coder 位列原榜 #19（另一个模型，未合并）"),
    "ltx": dict(chips=["image-to-video", "LTX-2.x 社区许可", "创建于 2026-07-23"], what="音视频联合生成 · 22B DiT", note="上周原榜 #7 → 本周 #4"),
    "ripple": dict(chips=["text-generation", "Apache-2.0", "发布于 2026-11-04"], what="不用 MoE 的 65B 稠密模型", note="Ricursive Intelligence · 1M 上下文 · Preview 版"),
}
PIDS = ["kimi", "idol", "coder3d", "ltx", "ripple"]

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
        date = chip("2026 年第 45 周 · 11 月 7 日", color=HF, size=24).next_to(title, DOWN, buff=0.4)
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

# ───────────────────────────── 模型简介（左：卡片；右：各自面板）
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
        self.W(max(self.cue(1) - 0.3, self.t))
        self.P(FadeIn(what, shift=RIGHT * 0.2), Create(bar), FadeIn(nt), rt=0.6)
        self.later()
        self.finish()
    def right(self): pass
    def later(self): pass
    def panel(self, h=5.6): return box(6.5, h, color=BORDER, fill="#0F141B").move_to([3.55, 0.3, 0])

class P1a(IntroScene):
    key = "P1a"; pid = "kimi"
    def right(self):
        aa = DATA["kimi"]["third_party"]["Artificial Analysis"]
        b = self.panel()
        t = T("Artificial Analysis 智能指数 v5.0.1", 22, FG, weight=BOLD)
        st = T("开源权重模型（第三方评测）", 17, MUTED)
        ow = aa["open_weights_index"]
        rows = [(n, v, HF if "Kimi" in n else DIM) for n, v in ow.items()]
        ch = hbars(rows, 62, bw=2.7, lw=2.6, size=17, h=0.3, gap=0.1, fmt="{:.1f}")
        pt = T("闭源参考", 17, MUTED)
        pr = hbars([(n.replace(" (Max)", ""), v, "#3B4452") for n, v in aa["proprietary_ref"].items()], 62, bw=2.7, lw=2.6, size=17, h=0.3, gap=0.1, fmt="{:.1f}")
        src = fit(T("来源：artificialanalysis.ai（2026-11-07 查询）", 14, MUTED), 5.9)
        G = VGroup(VGroup(t, st).arrange(DOWN, aligned_edge=LEFT, buff=0.08), ch, pt, pr, src).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        pr.shift(RIGHT * (ch[0][1].get_left()[0] - pr[0][1].get_left()[0]))
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(G[0]), rt=0.4)
        self.P(grow(ch), FadeIn(src), rt=1.2)
        self.pp = VGroup(pt, pr)
    def later(self):
        self.W(self.sub_t("已经追到"))
        self.P(FadeIn(self.pp[0]), grow(self.pp[1]), rt=1.0)

class P1b(Base):
    key = "P1b"
    def construct(self):
        self.head("kimi", "设计")
        n1 = node("Kimi K3 底座", 2.6, 0.95, BORDER, 22, "沿用预训练")
        n2 = node("加大后训练算力", 3.2, 0.95, PURPLE, 22, "数百个领域联合 RL")
        n3 = node("Kimi K3.1 Pro", 2.6, 0.95, HF, 22, "2.8T / 104B 激活")
        fl = VGroup(n1, n2, n3).arrange(RIGHT, buff=0.7).move_to(UP * 2.35)
        ar = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3) for a, b in zip(fl[:-1], fl[1:])])
        self.P(FadeIn(n1, shift=UP * 0.15), rt=0.5)
        self.P(GrowArrow(ar[0]), FadeIn(n2), GrowArrow(ar[1]), FadeIn(n3), rt=1.0)
        self.W(self.cue(1))
        kinds = ["dsa" if i % 4 == 3 else "kda" for i in range(92)] + ["dsa"]
        col = {"kda": BLUE, "dsa": ORANGE}
        blocks = VGroup(*[Rectangle(width=0.1, height=0.8, stroke_width=0).set_fill(col[k], 1) for k in kinds]).arrange(RIGHT, buff=0.04)
        fit(blocks, 13.0).move_to(UP * 0.95)
        lg = VGroup(*[VGroup(Square(0.24).set_fill(c_, 1).set_stroke(width=0), T(n, 19, FG)).arrange(RIGHT, buff=0.12) for n, c_ in
                      [("KDA 线性注意力 × 69", BLUE), ("Gated DSA 稀疏注意力 × 24：每个查询只取 2048 个位置", ORANGE)]]).arrange(RIGHT, buff=0.5)
        lg.next_to(blocks, DOWN, buff=0.2)
        nt = T("93 层 · 排列为示意 · K3 的 24 层全注意力（Gated MLA）→ 本版换成 Gated DSA", 15, MUTED).next_to(blocks, UP, buff=0.12).align_to(blocks, LEFT)
        self.P(LaggedStart(*[GrowFromEdge(b, DOWN) for b in blocks], lag_ratio=0.01), FadeIn(nt), rt=1.4)
        self.P(FadeIn(lg), rt=0.5)
        self.W(self.cue(2))
        c1 = card_rows("专家切得很细，权重 4 bit", [("896 个专家，每个 token 选 16 个 + 2 个共享", None), ("MXFP4 权重 / MXFP8 激活：量化感知训练", None),
                        ("检查点约 1.5 TB（社区 NVFP4 移植笔记，讨论 #7）", MUTED)], 6.5, BLUE, 19, 23)
        c1.move_to([-3.45, -1.6, 0])
        self.P(FadeIn(c1, shift=UP * 0.15), rt=0.6)
        self.W(self.cue(3))
        s1 = stat_card("≈2 tok/s", "单张 96 GB 显卡生成速度", 3.0, 1.45, ORANGE, 34, 17, "预填充约 40 tok/s")
        s2 = stat_card("1M", "上下文", 2.2, 1.45, GREEN, 34, 17, "MoonViT-V2 视觉编码器")
        ss = VGroup(s1, s2).arrange(RIGHT, buff=0.15).move_to([3.5, -1.45, 0])
        cap = fit(T("社区第三方移植（讨论 #12，发帖者自述，未核实）", 15, MUTED), 6.0).next_to(ss, DOWN, buff=0.12)
        self.P(LaggedStart(FadeIn(s1, shift=UP * 0.15), FadeIn(s2, shift=UP * 0.15), lag_ratio=0.3), FadeIn(cap), rt=0.8)
        self.finish()

class P1c(Base):
    key = "P1c"
    def construct(self):
        self.head("kimi", "评测", GREEN)
        bc = DATA["kimi"]["bench_card"]
        cc = [("Kimi K3.1 Pro", HF, 0), ("Claude Opus 5.5", PURPLE, 1), ("GPT-6 Astra", BLUE, 2)]
        lg = legend([(n, c) for n, c, _ in cc], 16)
        def mk(k, lab):
            return mini(lab, [(" ", bc[k][i], c) for _, c, i in cc], 100, bw=2.3, lw=0.1, size=14, h=0.17, gap=0.04, tsize=17, fmt="{:g}")
        good = VGroup(mk("Terminal-Bench 4.0", "Terminal-Bench 4.0"), mk("BenchCAD w/ tools", "BenchCAD（带工具）"), mk("OfficeQA Pro v2", "OfficeQA Pro v2")).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        bad = VGroup(mk("HLE-Diamond", "HLE-Diamond"), mk("ExploitBench", "ExploitBench（漏洞利用）")).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        gt = T("互有胜负", 19, GREEN, weight=BOLD); bt = T("明显落后", 19, RED, weight=BOLD)
        C1 = VGroup(gt, good).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        C2 = VGroup(bt, bad).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        cols = VGroup(C1, C2).arrange(RIGHT, buff=0.55, aligned_edge=UP)
        tt = T("官方对比（自报）", 21, FG, weight=BOLD)
        src = fit(T("来源：Kimi K3.1 Pro 模型卡 · 对手分数部分转引各家报告", 14, MUTED), 6.6)
        L = VGroup(VGroup(tt, lg).arrange(DOWN, aligned_edge=LEFT, buff=0.12), cols, src).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        fit(L, 7.0); L.move_to([-3.25, 2.95 - L.height / 2, 0])
        self.P(FadeIn(tt), FadeIn(lg), FadeIn(src), rt=0.5)
        self.P(FadeIn(gt), *[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.1)) for m in good], rt=1.2)
        self.W(self.sub_t("最难的推理题"))
        self.P(FadeIn(bt), *[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.1)) for m in bad], rt=1.0)
        self.W(self.cue(1))
        cy = DATA["kimi"]["cyber"]["xdev_bench_hard_pass3"]
        xt = T("xdev-bench-hard（内部漏洞利用基准，pass@3）", 18, FG, weight=BOLD)
        xb = hbars([("剔除网络安全数据前", cy["未做网络安全数据剔除的检查点"], DIM), ("发布版", cy["发布版 K3.1 Pro"], HF)], 100, bw=2.6, lw=2.5, size=16, h=0.3, gap=0.1, fmt="{:g}%")
        xs = fit(T("来源：Kimi 技术博客（官方自报）", 14, MUTED), 6.0)
        X = VGroup(xt, xb, xs).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        X.move_to([0, 2.95 - X.height / 2, 0]); X.shift(RIGHT * (0.45 - X.get_left()[0]))
        self.P(FadeIn(xt), grow(xb), FadeIn(xs), rt=1.0)
        self.W(self.cue(2))
        aa = DATA["kimi"]["third_party"]["Artificial Analysis"]
        s1 = stat_card(f"${aa['cost_per_task_usd']:.2f}", "单任务成本", 2.05, 1.3, ORANGE, 30, 16, "每百万 $2 入 / $10 出")
        s2 = stat_card(f"{aa['time_per_task_min']:g} 分", "单任务耗时", 2.05, 1.3, ORANGE, 30, 16, "同级中位数 14.2 分")
        s3 = stat_card(f"{aa['output_tok_s']} tok/s", "输出速度", 2.05, 1.3, DIM, 26, 16, "基于 Kimi 官方 API")
        ss = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.1)
        at = T("Artificial Analysis（第三方，2026-11-07）", 16, MUTED)
        A_ = VGroup(at, ss).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(X, DOWN, buff=0.3).align_to(X, LEFT)
        self.P(FadeIn(at), LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in ss], lag_ratio=0.25), rt=0.9)
        self.W(self.cue(3))
        q = quote("总是坚持自称 Kimi，系统提示很难改掉默认人设", 6.4, "社区讨论 #5 · 观点概述（非原话）", ORANGE, 18)
        q.next_to(A_, DOWN, buff=0.25).align_to(X, LEFT)
        self.P(FadeIn(q, shift=UP * 0.1), rt=0.5)
        self.finish()

# ───────────────────────────── #2 Idol
class P2a(IntroScene):
    key = "P2a"; pid = "idol"
    def right(self):
        b = self.panel()
        names = ["armchair", "lamp", "castle", "grandma"]
        ims = Group(*[ImageMobject(A + f"idol_{n}_f0.png").scale_to_fit_width(3.0) for n in names]).arrange_in_grid(2, 2, buff=(0.15, 0.2))
        ims.move_to(b).shift(UP * 0.25)
        cap = fit(T("左：输入图片 · 右：Idol 生成的 3D（官方示例动图）", 16, FG), 6.1).next_to(ims, DOWN, buff=0.2)
        src = fit(T("来源：speridlabs/idol 模型卡 Examples", 14, MUTED), 6.0).next_to(cap, DOWN, buff=0.08)
        self.P(FadeIn(b), FadeIn(ims), FadeIn(cap), FadeIn(src), rt=0.6)
        end = self.tm["total"] - 0.6
        for n, im in zip(names, ims): self.overlay(A + f"idol_{n}_loop.mp4", im, self.t, end)

class P2b(Base):
    key = "P2b"
    def construct(self):
        self.head("idol", "设计")
        steps = [("BiRefNet", "抠图 · 框住物体", BORDER), ("DINOv3 + FLUX.2 VAE", "两个现成编码器读图", PURPLE), ("DiT 去噪", "扩散生成八叉树", HF), ("高斯解码器", "→ 标准 3DGS .ply", GREEN)]
        ns = VGroup(*[node(a, 2.85, 1.0, c, 20, b_, 16) for a, b_, c in steps]).arrange(RIGHT, buff=0.42).move_to(UP * 2.3)
        ar = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.35) for a, b in zip(ns[:-1], ns[1:])])
        pr = VGroup(T("自有 0.66B：DiT 370.6M · 八叉树解码 50.8M · 高斯解码 237.3M", 16, MUTED), T("整条流水线约 1.8B（含两个编码器与抠图模型）· 峰值显存 7.2 GB", 16, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        pr.next_to(ns, DOWN, buff=0.18).align_to(ns, LEFT)
        self.P(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.1) for n in ns], lag_ratio=0.25), LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.3), rt=1.6)
        self.P(FadeIn(pr), rt=0.4)
        self.W(self.cue(1))
        lod = VGroup(*[stat_card(a, b_, 1.95, 1.1, BLUE, 24, 15) for a, b_ in [("32,768", "高斯 · 0.4 MB"), ("262,144", "默认 · 3.2 MB"), ("1,048,576", "最高 · 12.2 MB")]]).arrange(RIGHT, buff=0.12)
        lt = T("同一物体，多种精细度（官方项目页）", 18, FG, weight=BOLD)
        LOD = VGroup(lt, lod).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.55, -1.15, 0])
        self.P(FadeIn(lt), LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in lod], lag_ratio=0.2), rt=0.8)
        self.W(self.cue(2))
        bc = DATA["idol"]["bench_card"]; cols = bc["cols"]
        cc = [(n, HF if n == "Idol" else (BLUE if n == "TRELLIS" else (ORANGE if n == "LGM" else DIM))) for n in cols]
        def mk(k, lab, mx, fmt, base=0.0):
            return mini(lab, [(n, bc[k][i], c) for i, (n, c) in enumerate(cc)], mx, bw=1.5, lw=1.35, size=16, h=0.22, gap=0.05, tsize=18, fmt=fmt)
        m1 = mk("DINOv2", "新视角 DINOv2 ↑", 0.9, "{:.3f}"); m2 = mk("CLIP", "新视角 CLIP ↑", 0.95, "{:.3f}"); m3 = mk("PSNR", "输入视角 PSNR ↑", 13.5, "{:.2f}")
        ms = VGroup(m1, m2, m3)
        n3 = VGroup(T("LGM 的 PSNR 最高，", 15, ORANGE), T("但结果明显模糊", 15, ORANGE), T("官方注：PSNR 是平方像素误差的平均", 14, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        src = T("来源：speridlabs/idol 模型卡（官方自报，1×H100）", 14, MUTED)
        col1 = VGroup(m1, m2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        col2 = VGroup(m3, n3).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        R = VGroup(VGroup(col1, col2).arrange(RIGHT, buff=0.45, aligned_edge=UP), src).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fit(R, 6.6); R.move_to([3.6, -2.95 + R.height / 2 + 0.05, 0])
        self.P(*[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.08)) for m in ms[:2]], rt=1.0)
        self.W(self.sub_t("输入视角的像素误差"))
        self.P(FadeIn(m3[0]), grow(m3[1], 0.08), FadeIn(n3), FadeIn(src), rt=0.9)
        self.W(self.cue(3))
        self.P(FadeOut(LOD), rt=0.3)
        w = card_rows("先申请两个 gated 仓库的访问权限", [("facebook/dinov3-vith16plus-pretrain-lvd1689m", None), ("black-forest-labs/FLUX.2-dev（只用其 VAE）", None),
                       ("社区：有人申请 DINOv3 被拒，无法运行（讨论 #3）", ORANGE)], 6.6, ORANGE, 17, 21)
        w.move_to([-3.5, -1.15, 0])
        self.P(FadeIn(w, shift=UP * 0.15), rt=0.6)
        self.finish()

class P2s(Base):
    key = "P2s"
    def construct(self):
        self.head("idol", "实测：官方 Space 示例")
        inp = ImageMobject(A + "idol_backpack_input.png").scale_to_fit_height(3.9)
        ib = SurroundingRectangle(inp, buff=0.02, color=BORDER, stroke_width=2)
        IG = Group(inp, ib).move_to([-4.85, 0.3, 0])
        il = T("输入图片", 19, MUTED).next_to(IG, UP, buff=0.12)
        ph = ImageMobject("demo/splat_bg/f000.png").scale_to_fit_height(3.9)
        pb = SurroundingRectangle(ph, buff=0.02, color=HF, stroke_width=2)
        PG = Group(ph, pb).move_to([-0.55, 0.3, 0])
        pl = T("返回的 262,144 个高斯 · 本地转台渲染", 19, HF).next_to(PG, UP, buff=0.12)
        ar = Arrow(IG.get_right(), PG.get_left(), buff=0.12, color=MUTED, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        src = fit(T("Space：speridlabs/idol 的预置示例（/show_default_example）· 输入图取自该 Space 的 examples/obj-backpack.webp", 14, MUTED), 12.8).move_to([0, -2.4, 0])
        self.P(FadeIn(IG), FadeIn(il), rt=0.5)
        self.P(GrowArrow(ar), FadeIn(PG), FadeIn(pl), FadeIn(src), rt=0.6)
        self.overlay("demo/idol_turntable_x4.mp4", ph, self.t, self.tm["total"] - 0.6, speed=0.75)
        self.W(self.cue(1))
        c = VGroup(chip("正面：皮带扣、口袋与原图一致", color=GREEN, size=17), chip("背面：照片里没有，肩带与提手被补出", color=GREEN, size=17)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fit(c, 4.7); c.move_to([0, 1.2, 0]); c.shift(RIGHT * (1.95 - c.get_left()[0]))
        self.P(LaggedStart(*[FadeIn(x, shift=LEFT * 0.1) for x in c], lag_ratio=0.4), rt=0.8)
        self.W(self.cue(2))
        w = fit(VGroup(chip("简化点渲染（numpy + matplotlib）", color=ORANGE, size=17), T("并非真正的高斯光栅化，孔洞与颗粒感来自渲染方式", 14, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.1), 4.7).next_to(c, DOWN, buff=0.3).align_to(c, LEFT)
        w2 = fit(T("另试自备图片调用 /run：匿名 ZeroGPU 配额不足，未成功", 14, MUTED), 4.7).next_to(w, DOWN, buff=0.12).align_to(c, LEFT)
        self.P(FadeIn(w), FadeIn(w2), rt=0.5)
        self.finish()

# ───────────────────────────── #3 Qwen3.5-4B-3D-Coder
class P3a(IntroScene):
    key = "P3a"; pid = "coder3d"
    def right(self):
        b = self.panel()
        r = ImageMobject(A + "cc_tree_ref.png").scale_to_fit_width(1.9)
        o = ImageMobject(A + "cc_tree_out.png").scale_to_fit_width(4.0)
        rl = T("参考图", 16, MUTED); ol = T("生成的 Three.js 场景（截图）", 16, MUTED)
        R = Group(rl, r).arrange(DOWN, buff=0.1); O = Group(ol, o).arrange(DOWN, buff=0.1)
        row = Group(R, O).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        pt = fit(T("提示词：“create this scene using voxels 3d”", 16, FG), 6.0)
        src = fit(T("来源：ccore/Qwen3.5-4B-3D-Coder 模型卡（作者示例，参考图来自社区讨论 #9）", 14, MUTED), 6.1)
        G = Group(row, pt, src).arrange(DOWN, buff=0.25).move_to(b)
        self.P(FadeIn(b), FadeIn(R), rt=0.5)
        self.P(FadeIn(O, shift=LEFT * 0.15), FadeIn(pt), FadeIn(src), rt=0.8)

class P3b(Base):
    key = "P3b"
    def construct(self):
        self.head("coder3d", "训练")
        c1 = card_rows("数据：全部合成", [("4,146 条场景（3,933 训练 / 213 验证）", None), ("MiniMax M3.1 Flash 生成：完整思考 + HTML/JS", None),
                        ("最长一条 71,229 token，全部不截断", GREEN), ("41 个领域 · 数据集公开（MIT）", MUTED)], 6.5, BLUE, 19, 23)
        c1.move_to([-3.5, 2.95 - c1.height / 2, 0])
        self.P(FadeIn(c1, shift=UP * 0.15), rt=0.6)
        self.W(self.cue(1))
        stages = [("全量微调", "Checkpoint 1–4", BLUE), ("LoRA 一轮 · 178 条", "45 分钟 → 合并", PURPLE), ("继续全量微调", "→ Checkpoint 8", HF)]
        ns = VGroup(*[node(a, 2.0, 1.0, c, 18, b_, 15) for a, b_, c in stages]).arrange(RIGHT, buff=0.32)
        ar = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.04, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.35) for a, b in zip(ns[:-1], ns[1:])])
        nt = VGroup(T("累计约 59 小时 · 每次单卡（RTX PRO 6000 96GB；LoRA 用 L4）", 16, FG), T("无强化学习 · 更长的 LoRA 分支重复声明变量增多 → 弃用", 16, ORANGE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        TR = VGroup(VGroup(ns, ar), nt).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fit(TR, 6.5); TR.move_to([3.6, 0, 0]).align_to(c1, UP)
        self.P(LaggedStart(*[FadeIn(n) for n in ns], lag_ratio=0.3), LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.4), rt=1.2)
        self.P(FadeIn(nt), rt=0.4)
        self.W(self.cue(2))
        ev = DATA["coder3d"]["eval_rows"]
        zh = {"Voxel ancient Rome": "体素古罗马", "Kyoto temple": "京都寺庙", "Venice canal": "威尼斯运河", "Victorian library": "维多利亚图书馆",
              "Alpine castle": "阿尔卑斯城堡", "Container harbour": "集装箱港口", "Regional airport": "地区机场", "Pool table": "台球桌"}
        rows = [(zh[k], v, GREEN if v == 1 else (ORANGE if v >= 5 else BLUE)) for k, v in ev.items() if k != "source"]
        g = VGroup()
        for i, (lab, v, c) in enumerate(rows):
            lt = T(lab, 18, FG)
            sq = VGroup(*[Square(0.3).set_stroke(BG, 1).set_fill(c if j == v - 1 else "#3B4452", 1) for j in range(v)]).arrange(RIGHT, buff=0.06)
            col, r = divmod(i, 4)
            lt.move_to([col * 5.6, -r * 0.42, 0], aligned_edge=RIGHT); sq.next_to(lt, RIGHT, buff=0.2); sq.align_to([col * 5.6 + 0.2, 0, 0], LEFT)
            g.add(VGroup(lt, sq))
        et = T("Checkpoint 8 · 每个开发测试场景第几次尝试才被接受", 20, FG, weight=BOLD)
        lg = legend([("第 1 次", GREEN), ("第 3 次", BLUE), ("第 5 次", ORANGE), ("之前未被接受的尝试", "#3B4452")], 15)
        en = T("共 18 次调用，其中 8 次陷入推理循环、没交出网页；古罗马与京都两个场景做了小修复 · 来源：作者技术报告（探索性自测）", 15, MUTED)
        E_ = VGroup(VGroup(et, lg).arrange(RIGHT, buff=0.5), g, en).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fit(E_, 13.2); E_.move_to([0, -2.95 + E_.height / 2, 0])
        sep = dashed_sep(E_.get_top()[1] + 0.15)
        self.P(Create(sep), FadeIn(E_[0]), LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.1), rt=1.4)
        self.P(FadeIn(en), rt=0.4)
        self.finish()

class P3c(Base):
    key = "P3c"
    def construct(self):
        self.head("coder3d", "姊妹模型 GLB-3D-Coder · 社区", GREEN)
        sib = DATA["coder3d"]["sibling"]
        ph = ImageMobject(A + "glb_riftward_f0.png").scale_to_fit_width(6.2)
        fr = SurroundingRectangle(ph, buff=0.02, color=BORDER, stroke_width=2)
        G = Group(ph, fr).move_to([-3.55, 0.95, 0])
        cap = fit(T("RIFTWARD：用 GLB-3D-Coder 生成的资产拼成的浏览器小游戏（作者 Space）", 14, MUTED), 6.3).next_to(G, DOWN, buff=0.08)
        info = VGroup(chip(f"ccore/Qwen3.5-4B-GLB-3D-Coder · 原榜 #{sib['trending_position']}", color=HF, size=17), chip("页面自带 Export GLB → 导入 Godot", color=GREEN, size=17)).arrange(RIGHT, buff=0.12)
        fit(info, 6.4).next_to(cap, DOWN, buff=0.15)
        self.P(FadeIn(G), FadeIn(cap), FadeIn(info), rt=0.7)
        self.overlay(A + "glb_riftward_loop.mp4", ph, self.t, self.tm["total"] - 0.6)
        self.W(self.cue(1))
        cmp_ = ImageMobject(A + "glb_coral.png").scale_to_fit_width(6.2)
        cf = SurroundingRectangle(cmp_, buff=0.02, color=BORDER, stroke_width=2)
        CG = Group(cmp_, cf).move_to([3.5, 1.2, 0])
        lab = VGroup(T("左：DeepSeek V4.1 Flash 1017", 15, MUTED), T("右：GLB-3D-Coder 4B", 15, HF)).arrange(RIGHT, buff=0.5).next_to(CG, DOWN, buff=0.08)
        pc = fit(T("提示词“Create a coral-armored lighthouse keeper.” · 作者挑选的对比，非盲测", 14, MUTED), 6.3).next_to(lab, DOWN, buff=0.06)
        self.P(FadeIn(CG, shift=LEFT * 0.15), FadeIn(lab), FadeIn(pc), rt=0.7)
        self.W(self.sub_t("也有用户"))
        q = quote("让更大的模型当总指挥、把它当子代理分步搭建，效果更好", 6.4, "社区讨论 #15 · 观点概述（非原话）", BLUE, 17)
        q.next_to(pc, DOWN, buff=0.2).align_to(CG, LEFT)
        self.P(FadeIn(q, shift=UP * 0.1), rt=0.5)
        self.finish()

# ───────────────────────────── #4 LTX-2.5
class P4a(IntroScene):
    key = "P4a"; pid = "ltx"
    def right(self):
        lc = DATA["ltx"]["likes_check"]
        b = self.panel()
        t = T("点赞账号是什么时候注册的？", 22, FG, weight=BOLD)
        st = fit(T("占比 = 2026 年 8 月及以后注册的账号 / 全部点赞账号", 15, MUTED), 6.0)
        sh = hbars([("LTX-2.5", lc["LTX-2.5"]["share_new"], ORANGE), ("MiniMax-H3", lc["MiniMax-H3"]["share_new"], DIM)], 70, bw=2.8, lw=2.0, size=18, h=0.36, gap=0.14, fmt="{:.1f}%")
        mt = T("新账号点赞数（按注册月份）", 17, MUTED)
        mons = ["2026-08", "2026-09", "2026-10", "2026-11"]
        vb = vbars([(m[5:] + " 月" if m != "2026-11" else "11 月 1–7 日", [lc["LTX-2.5"]["by_month"][m], lc["MiniMax-H3"]["by_month"][m]]) for m in mons], [ORANGE, DIM], 2700, gw=1.35, bw=0.32, hmax=1.35, size=13, lab_size=14)
        lg = legend([("LTX-2.5", ORANGE), ("MiniMax-H3", DIM)], 14)
        src = fit(T("我们用公开点赞列表复核（2026-11-07）；只反映账号注册时间，不能证明刷量", 14, MUTED), 6.0)
        d = DATA["ltx"]
        dc = fit(chip(f"30 天下载：{d['likes_check']['downloads_w44']:,} → {d['downloads_30d']:,}（上周 → 本周）", color=BORDER, size=16), 6.0)
        G = VGroup(VGroup(t, st).arrange(DOWN, aligned_edge=LEFT, buff=0.08), sh, VGroup(mt, lg).arrange(RIGHT, buff=0.3), vb, src, dc).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        G.move_to(b)
        self.P(FadeIn(b), FadeIn(G[0]), rt=0.4)
        self.G = G
    def later(self):
        G = self.G
        self.W(self.sub_t("我们复核"))
        self.P(grow(G[1]), rt=0.9)
        self.P(FadeIn(G[2]), grow_v(G[3]), FadeIn(G[4]), rt=1.2)
        self.W(self.sub_t("而它一个月"))
        self.P(FadeIn(G[5], shift=UP * 0.1), rt=0.4)

class P4b(Base):
    key = "P4b"
    def construct(self):
        self.head("ltx", "设计与第三方评测")
        txt = node("文本编码器", 2.6, 0.95, BORDER, 19, "定制 Gemma 4 12B").move_to([-5.3, 1.5, 0])
        vs = node("视频流", 3.6, 1.1, HF, 22, "容量大（LTX-2：14B）").move_to([-1.1, 2.3, 0])
        au = node("音频流", 2.4, 0.85, PURPLE, 19, "LTX-2：5B").move_to([-1.1, 0.7, 0])
        xa = DoubleArrow(vs.get_bottom(), au.get_top(), buff=0.04, color=GREEN, stroke_width=3, tip_length=0.15)
        xl = T("双向音视频交叉注意力", 15, GREEN).next_to(xa, RIGHT, buff=0.15)
        dec = node("扩散视频解码器", 3.0, 1.1, GREEN, 19, "取代 VAE 重建（2.5 新增）").move_to([4.3, 2.3, 0])
        ad = node("音频 VAE + 声码器", 3.0, 0.85, BORDER, 17).move_to([4.3, 0.7, 0])
        a1 = Arrow(txt.get_right(), vs.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        a1b = Arrow(txt.get_right(), au.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        a2 = Arrow(vs.get_right(), dec.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        a3 = Arrow(au.get_right(), ad.get_left(), buff=0.06, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        srcd = fit(T("结构示意 · 来源：LTX-2 论文 arXiv:2601.03233 与 LTX-2.5 模型卡（2.5 的 DiT 共 22B）", 14, MUTED), 12.0).move_to([0, -0.05, 0])
        self.P(FadeIn(txt), GrowArrow(a1), GrowArrow(a1b), FadeIn(vs), FadeIn(au), rt=0.8)
        self.P(GrowFromCenter(xa), FadeIn(xl), rt=0.6)
        self.P(GrowArrow(a2), FadeIn(dec), GrowArrow(a3), FadeIn(ad), FadeIn(srcd), rt=0.6)
        self.W(self.cue(1))
        ms = VGroup(*[box(1.2, 0.7, color=HF, r=0.08) for _ in range(3)]).arrange(RIGHT, buff=0.12)
        ml = VGroup(*[T(f"镜头 {i + 1}", 15, FG).move_to(b) for i, b in enumerate(ms)])
        mt = T("一次生成多个镜头：人物、场景、声音保持一致", 17, FG)
        MS = VGroup(mt, VGroup(ms, ml)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.6, -1.75, 0])
        self.P(FadeIn(mt), LaggedStart(*[FadeIn(VGroup(b, l), shift=RIGHT * 0.1) for b, l in zip(ms, ml)], lag_ratio=0.3), rt=0.8)
        self.W(self.sub_t("解码端"))
        self.P(Indicate(dec, color=GREEN, scale_factor=1.06), rt=0.6)
        self.W(self.cue(2))
        aa = DATA["ltx"]["third_party"]["Artificial Analysis Video Arena"]["text-to-video"]
        rows = [(f"MiniMax H3 768p（第 {aa['MiniMax H3 (768p)'][0]}）", aa["MiniMax H3 (768p)"][1], DIM), (f"LTX-2.5 Fast（第 {aa['LTX-2.5 Fast'][0]}）", aa["LTX-2.5 Fast"][1], HF),
                (f"LTX-2.3 Pro（第 {aa['LTX-2.3 Pro'][0]}）", aa["LTX-2.3 Pro"][1], "#3B4452")]
        ch = hbars(rows, 1200, bw=2.4, lw=3.0, size=16, h=0.28, gap=0.1, fmt="{:.0f}", base=750)
        at = T("AA 视频竞技场 · 文生视频 Elo", 18, FG, weight=BOLD)
        an = VGroup(T("H3 是该榜标注为开源权重的模型中最高的", 14, MUTED), T("横轴从 750 起 · 第三方，2026-11-07 查询 · 测的是 LTX API 版本", 14, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        R = VGroup(at, ch, an).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        R.move_to([3.4, -1.65, 0])
        self.P(FadeIn(at), grow(ch), FadeIn(an), rt=1.2)
        self.W(self.cue(3))
        self.P(FadeOut(MS), rt=0.3)
        lic = card_rows("LTX-2.x 社区许可", [("年收入 < 1000 万美元：免费商用", GREEN), ("以上：需签付费商业协议", ORANGE)], 6.3, YELLOW, 17, 20)
        lic.move_to([-3.6, -1.7, 0])
        self.P(FadeIn(lic, shift=UP * 0.1), rt=0.5)
        self.finish()

# ───────────────────────────── #5 Ripple-65B
class P5a(IntroScene):
    key = "P5a"; pid = "ripple"
    def right(self):
        bc = DATA["ripple"]["bench_card"]
        b = self.panel()
        t = T("Terminal-Bench 2.1（官方自报）", 22, FG, weight=BOLD)
        rows = [(f"{n.split(' ')[0] if 'Ripple' in n else n}", v, HF if "Ripple" in n else DIM) for n, v in zip(bc["cols"], bc["Terminal-Bench 2.1 (self-reported)"])]
        rows = [(("Ripple-65B（稠密）" if "Ripple" in n else n.replace(" 501B", "").replace(" 816B", "").replace(" 975B", "").replace(" 550B", "")), v, c) for n, v, c in rows]
        ch = hbars(rows, 90, bw=2.6, lw=2.4, size=17, h=0.32, gap=0.12, fmt="{:.1f}")
        ps = VGroup(*[M(f"{p}B", 15, MUTED) for p in bc["total_params_B"]])
        for p, r in zip(ps, ch): p.next_to(r[2], RIGHT, buff=0.18)
        pl = T("总参数", 14, MUTED)
        src = fit(T("来源：ricursiveAI/Ripple-65B-Preview 模型卡 · 各家自报分数", 14, MUTED), 5.9)
        G = VGroup(t, ch, src).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        G.move_to(b).shift(LEFT * 0.25)
        for p, r in zip(ps, ch): p.next_to(r[2], RIGHT, buff=0.18)
        pl.next_to(ps[0], UP, buff=0.12).align_to(ps, LEFT)
        self.P(FadeIn(b), FadeIn(t), rt=0.4)
        self.P(grow(ch), FadeIn(src), rt=1.2)
        self.R = (ch, ps, pl, src)
    def later(self):
        ch, ps, pl, src = self.R
        self.W(self.sub_t("它的自报分数"))
        self.P(FadeIn(pl), LaggedStart(*[FadeIn(p) for p in ps], lag_ratio=0.15), rt=0.6)

class P5b(Base):
    key = "P5b"
    def construct(self):
        self.head("ripple", "设计、成本与短板")
        def slab(w, h, c, lab):
            return VGroup(Rectangle(width=w, height=h, stroke_width=0).set_fill(c, 1), T(lab, 14, FG))
        deep = VGroup(*[Rectangle(width=1.1, height=0.045, stroke_width=0).set_fill(BLUE if i % 5 else ORANGE, 1) for i in range(40)]).arrange(DOWN, buff=0.03)
        dl = VGroup(T("80 层 · d_model 5120", 16, FG), T("又窄又深", 16, MUTED)).arrange(DOWN, buff=0.05).next_to(deep, DOWN, buff=0.1)
        D = VGroup(deep, dl).move_to([0, 0.85, 0]); D.shift(RIGHT * (-6.9 - D.get_left()[0]))
        c1 = card_rows("结构", [("注意力头超配", None), ("更多、更短的滑动窗口层把成本压回来", None), ("门控注意力 · 全局 NoPE · value residual", MUTED), ("（蓝：滑窗层 · 橙：全局层，比例为示意）", MUTED)], 4.4, BLUE, 16, 20)
        c1.next_to(D, RIGHT, buff=0.3).align_to(D, UP)
        self.P(LaggedStart(*[GrowFromEdge(r, LEFT) for r in deep], lag_ratio=0.02), FadeIn(dl), rt=1.0)
        self.P(FadeIn(c1, shift=LEFT * 0.1), rt=0.5)
        self.W(self.cue(1))
        s1 = stat_card("40%", "MFU：无定制算子、无量化", 2.3, 1.3, GREEN, 32, 15)
        s2 = stat_card("1 → 5 人", "团队规模", 2.3, 1.3, BLUE, 30, 15)
        s3 = stat_card("$32M", "全部研发成本（官方）", 2.3, 1.3, HF, 32, 15, "称约为此前 SOTA 的 1/10")
        ss = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.12)
        fit(ss, 6.0); ss.move_to([0, 2.25, 0]); ss.shift(RIGHT * (6.9 - ss.get_right()[0]))
        self.P(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in ss], lag_ratio=0.25), rt=0.9)
        self.W(self.cue(2))
        rl = card_rows("强化学习用量（官方）", [("TerminalBench 2.1 达到 80.5 只用 1.4M 条 rollout", None), ("约为 Reflection Beam 的 1/70", GREEN)], 6.0, GREEN, 16, 20)
        rl.next_to(ss, DOWN, buff=0.25).align_to(ss, LEFT)
        self.P(FadeIn(rl, shift=UP * 0.1), rt=0.5)
        self.W(self.cue(3))
        bc = DATA["ripple"]["bench_card"]
        cc = [("Ripple-65B", HF, 0), ("Muse Spark Open", PURPLE, 2), ("Reflection Beam", BLUE, 1)]
        lg = legend([(n, c) for n, c, _ in cc], 14)
        ms = VGroup(*[mini(k, [(" ", bc[k][i], c) for _, c, i in cc], 100, bw=1.9, lw=0.1, size=13, h=0.15, gap=0.03, tsize=16, fmt="{:g}") for k in ["MMLU-Pro", "SciCode", "MCP Atlas"]]).arrange(RIGHT, buff=0.45, aligned_edge=UP)
        nt = fit(T("短板：知识与科学代码 · 表中不少对手分数为 Ricursive 自测 · Artificial Analysis 暂未收录（2026-11-07）", 14, MUTED), 12.8)
        B = VGroup(VGroup(T("模型卡对比（自报）", 17, FG, weight=BOLD), lg).arrange(RIGHT, buff=0.4), ms, nt).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fit(B, 13.0); B.move_to([0, -2.95 + B.height / 2, 0])
        if B.get_top()[1] > rl.get_bottom()[1] - 0.1 or B.get_top()[1] > D.get_bottom()[1] - 0.1:
            top = min(rl.get_bottom()[1], D.get_bottom()[1], c1.get_bottom()[1]) - 0.15
            B.scale_to_fit_height(top + 2.95); B.move_to([0, -2.95 + B.height / 2, 0])
        self.P(FadeIn(B[0]), *[AnimationGroup(FadeIn(m[0]), grow(m[1], 0.1)) for m in ms], FadeIn(nt), rt=1.2)
        self.finish()

# ───────────────────────────── 结尾
class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        t = T("本周回顾", 40, HF, weight=BOLD).move_to(UP * 2.85)
        self.P(FadeIn(t, shift=DOWN * 0.15), rt=0.5)
        tag = {"kimi": "开源智能指数第一 · CAD 建模接近闭源", "idol": "单图生成 3D 高斯 · 补出背面",
               "coder3d": "4B 小模型写 Three.js 场景", "ltx": "音视频联合生成 · 点赞数据存疑", "ripple": "65B 稠密 · 小团队低成本"}
        three = {"kimi", "idol", "coder3d"}
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
        rows.arrange(DOWN, buff=0.12).move_to(UP * 0.25)
        self.P(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.15), rt=1.4)
        self.W(self.cue(1))
        tg = VGroup(*[chip("3D", color=GREEN, size=16).next_to(r[0], LEFT, buff=0.12) for r, pid in zip(rows, PIDS) if pid in three])
        self.P(*[r[0].animate.set_stroke(GREEN, 2.5) for r, pid in zip(rows, PIDS) if pid in three], FadeIn(tg), rt=0.6)
        self.W(self.cue(2))
        self.P(rows[3][0].animate.set_stroke(ORANGE, 2.5), rt=0.5)
        self.W(self.cue(3))
        bye = T("下周见", 36, HF, weight=BOLD).next_to(t, RIGHT, buff=0.6)
        self.P(FadeIn(bye, scale=0.8), rt=0.4)
        self.finish()
