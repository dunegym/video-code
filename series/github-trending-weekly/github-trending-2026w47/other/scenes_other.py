"""GitHub 非AI类项目周热榜（2026 第 47 周）—— Manim CE 场景。
时间轴由 timing_other.json（MiniMax 词级时间戳）驱动；动图演示由 assemble_w46.py 用 ffmpeg 叠加到占位图上，
叠加参数由各场景写入 build/scenes/ov_<scene>.json。"""
import json, os
import numpy as np
from manim import *
from PIL import Image as _PILImage
_fromarray = _PILImage.fromarray
def _fa(arr, mode=None):   # 兼容新版 Pillow：manim 用 2D 零数组 + mode=RGBA 创建空画布
    if mode == "RGBA" and getattr(arr, "ndim", 3) == 2:
        return _PILImage.new("RGBA", (arr.shape[1], arr.shape[0]))
    return _fromarray(arr, mode) if mode else _fromarray(arr)
_PILImage.fromarray = _fa

config.pixel_width, config.pixel_height, config.frame_rate = 1920, 1080, 30
TM = json.load(open("timing_other.json", encoding="utf-8"))
DATA = json.load(open("data.json", encoding="utf-8"))
A = "assets/proc/"
FONT, MONO = "Noto Sans CJK SC", "Noto Sans Mono CJK SC"
BG, PANEL, BORDER = "#0D1117", "#161B22", "#30363D"
FG, MUTED = "#E6EDF3", "#8B949E"
BLUE, GREEN, YELLOW, PURPLE, ORANGE, RED, TEAL = "#2F81F7", "#3FB950", "#E3B341", "#A371F7", "#F0883E", "#F85149", "#39C5CF"
LANG_COLOR = {"JavaScript": "#F1E05A", "TypeScript": "#3178C6", "Python": "#3572A5", "CSS": "#563D7C", "C": "#A8B9CC", "Rust": "#DEA584", "Go": "#00ADD8", "Ruby": "#701516", "Objective-C": "#438EFF"}
REPO = {k: f"{v['owner']}/{v['repo']}" for k, v in DATA.items() if not k.startswith("_")}
OWNER_AV = {k: v["owner"] for k, v in DATA.items() if not k.startswith("_")}

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
def chip(text, color=MUTED, dot=None, size=20, font=FONT):
    t = Text(text, font=font, font_size=size, color=FG)
    inner = VGroup(Dot(radius=0.07, color=dot), t).arrange(RIGHT, buff=0.12) if dot else VGroup(t)
    b = RoundedRectangle(width=inner.width + 0.36, height=max(0.44, inner.height + 0.2), corner_radius=0.2,
                         stroke_color=color, stroke_width=1.5).set_fill(PANEL, 1)
    inner.move_to(b)
    return VGroup(b, inner)
def gh_star(r=0.13, color=YELLOW):
    return Star(5, outer_radius=r, inner_radius=r * 0.45, color=color, fill_opacity=1, stroke_width=0)
def avatar(pid, h=0.5):
    im = ImageMobject(A + f"avatar_{OWNER_AV[pid]}.png").scale_to_fit_height(h)
    return Group(im, SurroundingRectangle(im, buff=0, color=BORDER, stroke_width=1.5, corner_radius=0.06))
def picture(path, width=None, height=None, credit=None, csize=17):
    """官方图片 + 细边框 + 下方来源说明；返回 (图组, 来源文字)"""
    im = ImageMobject(path)
    if width: im.scale_to_fit_width(width)
    if height and im.height > height: im.scale_to_fit_height(height)
    fr = SurroundingRectangle(im, buff=0.02, color=BORDER, stroke_width=2)
    g = Group(im, fr)
    cap = T(credit, csize, MUTED).next_to(g, DOWN, buff=0.1) if credit else None
    return g, cap
CW = None
def terminal(lines, w, size=18, title="bash", maxh=None, hl=None):
    """终端窗口：lines 为真实命令输出。返回 (窗口, 行列表)"""
    global CW
    if CW is None: CW = M("M" * 20, size).width / 20 / size
    cw = CW * size
    rows = []
    cont = False
    for ln in lines:
        n = len(ln) - len(ln.lstrip(" "))
        s = ln.strip(" ") or "·"
        col = GREEN if ln.startswith("$ ") or cont else FG
        cont = ln.rstrip().endswith("\\")
        if hl and any(k in ln for k in hl): col = YELLOW
        t = M(s, size, col)
        if s == "·": t.set_opacity(0)
        rows.append((t, n))
    g = VGroup()
    y = 0
    lh = size / 48 * 0.62
    for t, n in rows:
        t.move_to([0, 0, 0], aligned_edge=LEFT).shift(RIGHT * n * cw + DOWN * y)
        g.add(t); y += lh
    sc = 1.0
    if g.width > w - 0.5: sc = (w - 0.5) / g.width
    g.scale(sc, about_point=g.get_corner(UL))
    h = g.height + 0.95
    if maxh and h > maxh:
        g.scale((maxh - 0.95) / g.height, about_point=g.get_corner(UL)); h = maxh
    win = box(w, h, color=BORDER, fill="#010409", r=0.12)
    bar = Rectangle(width=w - 0.04, height=0.38, stroke_width=0).set_fill("#161B22", 1).move_to(win.get_top() + DOWN * 0.21)
    dots = VGroup(*[Dot(radius=0.065, color=c) for c in ["#FF5F57", "#FEBC2E", "#28C840"]]).arrange(RIGHT, buff=0.12)
    dots.move_to(bar.get_left() + RIGHT * 0.4)
    tt = M(title, 15, MUTED).move_to(bar)
    g.move_to(win.get_corner(UL) + np.array([0.25, -0.6, 0]), aligned_edge=UL)
    return VGroup(win, bar, dots, tt), g
def to_px(m):
    l, r = m.get_left()[0], m.get_right()[0]; t, b = m.get_top()[1], m.get_bottom()[1]
    X = (l + config.frame_width / 2) / config.frame_width * 1920
    Y = (config.frame_height / 2 - t) / config.frame_height * 1080
    W = (r - l) / config.frame_width * 1920; H = (t - b) / config.frame_height * 1080
    ev = lambda v: int(round(v / 2) * 2)
    return ev(X), ev(Y), ev(W), ev(H)
def lines_of(path, maxc=None):
    out = open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    if maxc: out = [l if len(l) <= maxc else l[:maxc - 1] + "…" for l in out]
    return out

class Base(Scene):
    key = ""
    def setup(self):
        self.camera.background_color = BG
        self.tm = TM[self.key]; self.t = 0.0; self.ov = []
    def sub_start(self, prefix):
        return next(x["start"] for x in self.tm["subs"] if x["text"].startswith(prefix))

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
        json.dump(self.ov, open(f"build/scenes/ov_{self.key}.json", "w"), indent=1)
    def overlay(self, clip, mob, t0, dur, ss=0.0, speed=1.0):
        x, y, w, h = to_px(mob)
        self.ov.append({"clip": clip, "t0": round(t0, 3), "dur": round(dur, 3), "ss": ss, "speed": speed,
                        "x": x, "y": y, "w": w, "h": h})
    def header(self, pid, section, color=BLUE):
        d = DATA[pid]
        av = avatar(pid, 0.5)
        rk = T(f"#{d['rank']}", 34, YELLOW, weight=BOLD)
        nm = M(REPO[pid], 24, FG)
        sec = VGroup(Dot(radius=0.05, color=color), T(section, 18, MUTED)).arrange(RIGHT, buff=0.1)
        g = Group(av, rk, nm, sec).arrange(RIGHT, buff=0.22).to_corner(UL, buff=0.32)
        line = Line(LEFT * 7.1 + UP * 3.25, RIGHT * 7.1 + UP * 3.25, color=BORDER, stroke_width=1.5)
        return Group(g, line)
    def counter(self, label, value, color, w=2.75):
        b = box(w, 1.25)
        lab = T(label, 20, MUTED).move_to(b.get_top() + DOWN * 0.3)
        vt = ValueTracker(0)
        num = always_redraw(lambda: fit(M(f"{int(vt.get_value()):,}", 38, color, weight=BOLD), w - 0.75)
                            .move_to(b.get_center() + DOWN * 0.2 + RIGHT * 0.2))
        st = always_redraw(lambda: gh_star(0.15, color).next_to(num, LEFT, buff=0.14))
        return VGroup(b, lab, num, st), vt.animate(rate_func=rate_functions.ease_out_cubic).set_value(value)

def folder_icon(color=BLUE, s=0.32):
    tab = Rectangle(width=s * 0.45, height=s * 0.18, stroke_width=0).set_fill(color, 1)
    body = Rectangle(width=s, height=s * 0.7, stroke_width=0).set_fill(color, 1)
    tab.next_to(body, UP, buff=0).align_to(body, LEFT)
    return VGroup(tab, body)
def step_list(items, w, size=21, color=BLUE):
    rows = VGroup()
    for i, (a, b) in enumerate(items):
        num = Circle(radius=0.2, color=color, stroke_width=2).set_fill(color, 0.15)
        n = T(str(i + 1), 18, FG, weight=BOLD).move_to(num)
        tt = fit(T(a, size, FG, weight=BOLD), w - 0.6)
        txt = VGroup(tt)
        if b: txt.add(fit(T(b, size - 4, MUTED), w - 0.6))
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        rows.add(VGroup(VGroup(num, n), txt).arrange(RIGHT, buff=0.2, aligned_edge=UP))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    return rows
def card_rows(title, rows, w, col=BLUE, size=22):
    """概念卡片：标题 + 若干行（每行一个圆点）"""
    t = T(title, 26, col, weight=BOLD)
    rs = VGroup(*[VGroup(Dot(radius=0.06, color=c or col), fit(T(r, size, FG), w - 0.9)).arrange(RIGHT, buff=0.18) for r, c in rows])
    rs.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    inner = VGroup(t, rs).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    b = box(w, inner.height + 0.7, color=col, fill="#0F141B")
    inner.move_to(b).align_to(b.get_left() + RIGHT * 0.35, LEFT)
    return VGroup(b, t, rs)


# ───────────────────────────── 项目简介（数据保持 v1 快照；左栏垂直居中，减少底部留白）
class IntroScene(Base):
    pid = ""
    def construct(self):
        d = DATA[self.pid]
        rank = T(f"#{d['rank']}", 104, YELLOW, weight=BOLD).to_corner(UL, buff=0.45)
        rank_lab = T("本周热榜", 24, MUTED).next_to(rank, RIGHT, buff=0.25).align_to(rank, DOWN).shift(UP * 0.18)
        av = avatar(self.pid, 0.46)
        owner = M(d["owner"] + " /", 28, MUTED)
        og = Group(av, owner).arrange(RIGHT, buff=0.15).next_to(rank, DOWN, buff=0.25).align_to(rank, LEFT)
        repo = fit(M(d["repo"], 44, FG, weight=BOLD), 6.1).next_to(og, DOWN, buff=0.12).align_to(rank, LEFT)
        chips = VGroup(chip(d["language"], dot=LANG_COLOR.get(d["language"], MUTED), size=22),
                       chip(d["license"], size=22), chip("创建于 " + d["created"][:7], size=22)).arrange(RIGHT, buff=0.16)
        fit(chips, 5.9)
        chips.next_to(repo, DOWN, buff=0.32).align_to(rank, LEFT)
        c1, a1 = self.counter("本周新增 Stars", d["week"], YELLOW, w=2.95)
        c2, a2 = self.counter("总 Stars", d["total"], FG, w=2.95)
        cards = VGroup(c1, c2).arrange(RIGHT, buff=0.2).next_to(chips, DOWN, buff=0.4).align_to(rank, LEFT)
        what = fit(T(d["what"], 28, FG), 6.1).next_to(cards, DOWN, buff=0.45).align_to(rank, LEFT).shift(RIGHT * 0.2)
        bar = Line(what.get_corner(UL) + LEFT * 0.15, what.get_corner(DL) + LEFT * 0.15, color=BLUE, stroke_width=4)
        allg = Group(rank, rank_lab, og, repo, chips, cards, what, bar)
        dy = 0.25 - (allg.get_top()[1] + allg.get_bottom()[1]) / 2
        allg.shift(UP * dy)
        self.P(FadeIn(rank, shift=RIGHT * 0.3), FadeIn(rank_lab), FadeIn(og), FadeIn(repo, shift=UP * 0.2), rt=0.8)
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips], lag_ratio=0.2), rt=0.6)
        self.W(self.cue(1) - 0.3)
        self.P(FadeIn(c1), FadeIn(c2), rt=0.3)
        self.P(a1, a2, rt=1.6)
        self.P(FadeIn(what, shift=RIGHT * 0.2), Create(bar), rt=0.6)
        self.W(self.cue(2) if len(self.tm["cues"]) > 2 else self.t)
        self.right()
        self.finish()
    def right(self): pass

TEAL, SKY = "#39C5CF", "#79C0FF"
def note(s, size=17, w=6.6): return fit(T(s, size, MUTED), w)
def hbars(items, x_lab, x_bar, y0, step, maxv, maxw, size=20, colors=None, hl=0):
    """横向条形图：items=[(名称, 数值, 例子或None)]"""
    rows = VGroup()
    for i, it in enumerate(items):
        name, v = it[0], it[1]
        y = y0 - i * step
        lab = T(name, size, FG).move_to([x_lab, y, 0], aligned_edge=RIGHT)
        col = (colors[i] if colors else (GREEN if i < hl else BLUE))
        bar = Rectangle(width=max(0.05, v / maxv * maxw), height=step * 0.62, stroke_width=0).set_fill(col, 0.9)
        bar.move_to([x_bar, y, 0], aligned_edge=LEFT)
        num = M(str(v), size - 1, MUTED).next_to(bar, RIGHT, buff=0.12)
        g = VGroup(lab, bar, num)
        if len(it) > 2 and it[2]:
            g.add(fit(T(it[2], size - 5, MUTED), 4.2).next_to(num, RIGHT, buff=0.25))
        rows.add(g)
    return rows
def bar_anim(rows, rt):
    return LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), *[FadeIn(x) for x in r[2:]]) for r in rows], lag_ratio=0.3, run_time=rt)


def av_owner(owner, h=0.5):
    im = ImageMobject(A + f"avatar_{owner}.png").scale_to_fit_height(h)
    return Group(im, SurroundingRectangle(im, buff=0, color=BORDER, stroke_width=1.5, corner_radius=0.06))
def bullets(items, w, size=21, col=GREEN, buff=0.22):
    return VGroup(*[VGroup(Dot(radius=0.06, color=col), fit(T(s, size, FG), w - 0.3)).arrange(RIGHT, buff=0.15)
                    for s in items]).arrange(DOWN, aligned_edge=LEFT, buff=buff)
def arrow(a, b, col=MUTED, sw=3, buff=0.1):
    return Arrow(a, b, buff=buff, color=col, stroke_width=sw, max_tip_length_to_length_ratio=0.18)
def credit(s, size=15, w=12.5): return fit(T(s, size, MUTED), w)

# ───────────────────────────── 片头
class S0_Intro(Base):
    key = "S0_Intro"
    def construct(self):
        grid = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                           background_line_style={"stroke_color": "#1B2230", "stroke_width": 1}, axis_config={"stroke_opacity": 0})
        self.add(grid)
        star = gh_star(0.42).move_to(UP * 2.35)
        title = VGroup(T("GitHub 非AI类项目周热榜", 60, FG, weight=BOLD), T("Top 4", 60, YELLOW, weight=BOLD)).arrange(RIGHT, buff=0.3)
        fit(title, 13.2).next_to(star, DOWN, buff=0.28)
        date = chip("2026 · 第 47 周 · 11 月 20 日", color=YELLOW, size=26).next_to(title, DOWN, buff=0.28)
        self.P(GrowFromCenter(star), FadeIn(title, shift=UP * 0.3), rt=0.9)
        self.P(Rotate(star, angle=TAU / 5), FadeIn(date, shift=UP * 0.15), rt=0.6)
        order = ["un", "su", "he", "ax"]
        avs = Group(*[Group(avatar(p, 0.85), M(DATA[p]["repo"], 16, MUTED)).arrange(DOWN, buff=0.08) for p in order]).arrange(RIGHT, buff=0.55)
        avs.next_to(date, DOWN, buff=0.4)
        self.P(LaggedStart(*[FadeIn(a, shift=UP * 0.2) for a in avs], lag_ratio=0.18), rt=1.3)
        self.W(self.cue(1))
        tags = VGroup(
            chip("办公套件", color=BLUE, size=22), chip("理财应用", color=GREEN, size=22),
            chip("爱马仕表盘", color=ORANGE, size=22), chip("设计系统", color=PURPLE, size=22),
        ).arrange(RIGHT, buff=0.2).next_to(avs, DOWN, buff=0.35)
        self.P(LaggedStart(*[FadeIn(c, scale=0.85) for c in tags], lag_ratio=0.15), rt=1.6)
        self.finish()

# ───────────────────────────── #4 univer
class P4a(IntroScene):
    key = "P4a"; pid = "un"
    def right(self):
        c = np.array([3.7, 0.3, 0])
        g, cap = picture("assets/proc/univer-home.png", width=6.15, height=4.4, credit="图：官网 univer.ai（2026-11-20 截取）", csize=14)
        g.move_to(c + UP * 0.15); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)

class P4b(Base):
    key = "P4b"
    def construct(self):
        hd = self.header("un", "开源核心与插件边界", BLUE)
        self.add(hd)
        layers = [
            ("功能插件", "规则和数据：过滤、校验等", GREEN),
            ("产品插件", "表格、文档等产品能力", BLUE),
            ("核心框架", "内容模型、命令、公式与渲染、门面接口", MUTED),
        ]
        nodes = VGroup(*[node(a, 10.5, 0.95, color=c, size=24, sub=b, subsize=16) for a, b, c in layers])
        nodes.arrange(DOWN, buff=0.28).move_to([0, 1.15, 0])
        arrs = VGroup(*[arrow(nodes[i].get_bottom(), nodes[i+1].get_top(), MUTED, 3, 0.06) for i in range(2)])
        self.P(LaggedStart(*[FadeIn(n, shift=UP * 0.12) for n in nodes], lag_ratio=0.2), *[Create(a) for a in arrs], rt=1.4)
        self.W(self.cue(2))
        cmd = box(12.6, 1.2, color=YELLOW, fill="#0F141B").move_to([0, -1.7, 0])
        ct = fit(T("改动走统一的命令系统，跨功能的操作也能一起撤销和重做。", 22, FG), 11.8).move_to(cmd)
        cap = credit("据 Univer README「Explore the open-source architecture」，图层为重绘示意", 14, 12).move_to([0, -2.5, 0])
        self.P(FadeIn(cmd), FadeIn(ct), FadeIn(cap), rt=0.7)
        self.finish()

class P4c(Base):
    key = "P4c"
    def construct(self):
        hd = self.header("un", "同一套接口，不同的授权范围", GREEN)
        self.add(hd)
        g, cap = picture("assets/proc/univer-intro.png", width=6.5, height=2.3, credit="图：仓库 docs/img/readme/intro-banner.png", csize=14)
        g.move_to([0, 2.0, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)
        self.W(self.cue(0) + 0.5)
        parts = VGroup(
            card_rows("开源 Web SDK", [
                ("内容模型、插件和命令", BLUE),
                ("公式与渲染、门面接口", BLUE),
                ("应用和智能体共用这一层", BLUE),
            ], 4.1, BLUE, 18),
            card_rows("服务端扩展", [
                ("实时协作", TEAL),
                ("历史版本", TEAL),
                ("办公文件导入导出", TEAL),
            ], 4.1, TEAL, 18),
            card_rows("另外授权", [
                ("商业插件", ORANGE),
                ("智能套件", ORANGE),
                ("不绑在开源接口上", ORANGE),
            ], 4.1, ORANGE, 18),
        ).arrange(RIGHT, buff=0.22).move_to([0, -0.35, 0])
        self.P(LaggedStart(*[FadeIn(p, shift=UP * 0.12) for p in parts], lag_ratio=0.15), rt=1.2)
        self.W(self.cue(2))
        ws, wcap = picture("assets/proc/univer-workspace.png", width=6.4, height=1.35, credit="图：Univer Workspace 参考应用宣传图", csize=13)
        # may be tight; use a note instead if height is an issue
        note = fit(T("另有可直接使用的工作区应用，作为这套工具包的参考实现。", 22, FG), 12.4)
        note.move_to([0, -2.2, 0])
        self.P(FadeIn(note), rt=0.6)
        self.finish()

# ───────────────────────────── #3 sure
class P3a(IntroScene):
    key = "P3a"; pid = "su"
    def right(self):
        c = np.array([3.7, 0.3, 0])
        g, cap = picture("assets/proc/sure-home.png", width=6.15, height=4.4, credit="图：官网 sure.am（2026-11-20 截取）", csize=14)
        g.move_to(c + UP * 0.15); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)

class P3b(Base):
    key = "P3b"
    def construct(self):
        hd = self.header("su", "社区续命与自托管", GREEN)
        self.add(hd)
        steps = [("Maybe Finance", "商业化没走通"), ("开源后短暂托管", "也没能持续"), ("社区 fork：Sure", "继续自己托管")]
        nodes = VGroup(*[node(a, 3.5, 1.2, color=c, size=22, sub=b, subsize=16)
                         for (a, b), c in zip(steps, [MUTED, ORANGE, GREEN])])
        nodes.arrange(RIGHT, buff=0.4).move_to([0, 1.85, 0])
        arrs = VGroup(*[arrow(nodes[i].get_right(), nodes[i+1].get_left(), MUTED, 3, 0.08) for i in range(2)])
        self.P(LaggedStart(*[FadeIn(n, shift=UP * 0.12) for n in nodes], lag_ratio=0.2), *[Create(a) for a in arrs], rt=1.3)
        self.W(self.cue(1))
        clients = VGroup(
            chip("浏览器", color=BLUE, size=22), chip("桌面", color=BLUE, size=22),
            chip("手机", color=BLUE, size=22), chip("接口", color=BLUE, size=22),
            chip("大模型代理也只是其中一种", color=MUTED, size=22),
        ).arrange(RIGHT, buff=0.16)
        fit(clients, 13.0).move_to([0, 0.25, 0])
        self.P(LaggedStart(*[FadeIn(c, scale=0.9) for c in clients], lag_ratio=0.12), rt=0.9)
        self.W(self.cue(2))
        lic = box(12.6, 1.25, color=YELLOW, fill="#0F141B").move_to([0, -1.4, 0])
        lt = fit(T("许可要求改动后仍要公开源码；「Maybe」商标还在原公司手里，所以必须叫 Sure。", 22, FG), 11.8).move_to(lic)
        cap = credit("据 Sure README「Backstory」「Forking and Attribution」与 docs/clients", 14, 12).move_to([0, -2.3, 0])
        self.P(FadeIn(lic), FadeIn(lt), FadeIn(cap), rt=0.7)
        self.finish()

class P3c(Base):
    key = "P3c"
    def construct(self):
        hd = self.header("su", "开支对比与贷款账户", ORANGE)
        self.add(hd)
        g1, c1 = picture("assets/proc/sure-dash.png", width=6.3, height=3.5, credit="图：Sure 官方仪表盘截图", csize=14)
        g2, c2 = picture("assets/proc/sure-spending.png", width=6.3, height=3.5, credit="图：v0.7.6 发布说明中的 Spending vs normal", csize=14)
        g1.move_to([-3.35, 0.7, 0]); c1.next_to(g1, DOWN, buff=0.08)
        g2.move_to([3.35, 0.7, 0]); c2.next_to(g2, DOWN, buff=0.08)
        self.P(FadeIn(g1), FadeIn(c1), rt=0.7)
        self.W(self.cue(1))
        self.P(FadeIn(g2), FadeIn(c2), rt=0.7)
        self.W(self.cue(2))
        note = fit(T("演示站把慢请求公开出来，方便社区对着改性能。", 22, FG), 12.4)
        note.move_to([0, -2.2, 0])
        self.P(FadeIn(note), rt=0.5)
        self.finish()

# ───────────────────────────── #2 HermesEnabler
class P2a(IntroScene):
    key = "P2a"; pid = "he"
    def right(self):
        c = np.array([3.7, 0.3, 0])
        g, cap = picture("assets/proc/hermes.png", width=5.6, height=4.5, credit="图：项目说明中的实机表盘照片", csize=14)
        g.move_to(c + UP * 0.1); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)

class P2b(Base):
    key = "P2b"
    def construct(self):
        hd = self.header("he", "支持范围与注意点", ORANGE)
        self.add(hd)
        g, cap = picture("assets/proc/hermes.png", width=5.4, height=4.0, credit="图：项目说明中的实机表盘照片", csize=14)
        g.move_to([-3.5, 0.55, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.7)
        cards = VGroup(
            card_rows("使用前提", [
                ("需要侧载到手表", ORANGE),
                ("打开开发者模式", ORANGE),
                ("删除前须恢复系统配置备份", ORANGE),
            ], 6.0, ORANGE, 20),
            card_rows("版本说明", [
                ("最新版加入 27.2 测试版", BLUE),
                ("watchOS 26 不支持", BLUE),
                ("27.3 测试版还不在范围内", BLUE),
            ], 6.0, BLUE, 20),
        ).arrange(DOWN, buff=0.25).move_to([3.4, 0.7, 0])
        self.P(FadeIn(cards[0], shift=LEFT * 0.15), rt=0.7)
        self.W(self.cue(1))
        self.P(FadeIn(cards[1], shift=LEFT * 0.15), rt=0.7)
        self.W(self.cue(2))
        foot = fit(T("项目借用了 Gester 的部分代码，作者写明自行承担风险。", 20, MUTED), 12.4)
        foot.move_to([0, -2.25, 0])
        self.P(FadeIn(foot), rt=0.5)
        self.finish()

class P2c(Base):
    key = "P2c"
    def construct(self):
        hd = self.header("he", "不是官方能力", MUTED)
        self.add(hd)
        g, cap = picture("assets/proc/hermes.png", width=5.6, height=2.85, credit="图：项目说明中的实机表盘照片，并提供多种语言版本", csize=14)
        g.move_to([0, 1.45, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)
        self.W(self.cue(1))
        notes = VGroup(
            box(6.2, 1.2, color=BLUE, fill="#0F141B"),
            box(6.2, 1.2, color=ORANGE, fill="#0F141B"),
        )
        t1 = VGroup(T("版本不支持时", 22, BLUE, weight=BOLD), fit(T("作者建议改用同一作者的 Clocky。", 18, FG), 5.6)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        t2 = VGroup(T("自行判断", 22, ORANGE, weight=BOLD), fit(T("不是苹果官方能力，下次系统更新后可能失效。", 18, FG), 5.6)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        notes.arrange(RIGHT, buff=0.25).move_to([0, -1.75, 0])
        t1.move_to(notes[0]).align_to(notes[0].get_left() + RIGHT * 0.28, LEFT)
        t2.move_to(notes[1]).align_to(notes[1].get_left() + RIGHT * 0.28, LEFT)
        self.P(FadeIn(notes[0]), FadeIn(t1), rt=0.6)
        self.W(self.cue(2))
        self.P(FadeIn(notes[1]), FadeIn(t2), rt=0.6)
        self.finish()

# ───────────────────────────── #1 astryx
class P1a(IntroScene):
    key = "P1a"; pid = "ax"
    def right(self):
        c = np.array([3.7, 0.3, 0])
        g, cap = picture("assets/proc/astryx-home.png", width=6.15, height=4.4, credit="图：官网 astryx.atmeta.com（2026-11-20 截取）", csize=14)
        g.move_to(c + UP * 0.15); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)

class P1b(Base):
    key = "P1b"
    def construct(self):
        hd = self.header("ax", "可组合、可换肤、同一份说明", PURPLE)
        self.add(hd)
        cards = VGroup(
            card_rows("组合与抽源码", [
                ("可在任意一层组合", PURPLE),
                ("必要时把源码抽到项目里改", PURPLE),
            ], 4.1, PURPLE, 19),
            card_rows("样式可覆盖", [
                ("底层写法对使用者透明", BLUE),
                ("原子类或普通样式都能改", BLUE),
            ], 4.1, BLUE, 19),
            card_rows("主题是变量", [
                ("不用包一层组件", TEAL),
                ("整套视觉可改成自己的品牌", TEAL),
            ], 4.1, TEAL, 19),
        ).arrange(RIGHT, buff=0.22).move_to([0, 1.35, 0])
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.18), rt=1.2)
        self.W(self.cue(2))
        cli = box(12.6, 1.5, color=YELLOW, fill="#0F141B").move_to([0, -1.2, 0])
        ct = VGroup(
            T("命令行会写下给智能体看的说明", 22, YELLOW, weight=BOLD),
            fit(T("人和助手对着同一份参考来写，而不是靠猜。", 20, FG), 11.8),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ct.move_to(cli).align_to(cli.get_left() + RIGHT * 0.35, LEFT)
        cap = credit("据 Astryx README「What makes Astryx different」与 Getting Started", 14, 12).move_to([0, -2.3, 0])
        self.P(FadeIn(cli), FadeIn(ct), FadeIn(cap), rt=0.8)
        self.finish()

class P1c(Base):
    key = "P1c"
    def construct(self):
        hd = self.header("ax", "三层结构与原则", GREEN)
        self.add(hd)
        layers = VGroup(
            node("基础", 3.6, 1.35, MUTED, 26, "字体、颜色、布局", 18),
            node("组件", 3.6, 1.35, BLUE, 26, "可复用的界面积木", 18),
            node("页面模式", 3.6, 1.35, PURPLE, 26, "表格页、详情页、表单向导", 18),
        ).arrange(RIGHT, buff=0.35).move_to([0, 1.7, 0])
        self.P(LaggedStart(*[FadeIn(n, shift=UP * 0.12) for n in layers], lag_ratio=0.2), rt=1.0)
        self.W(self.cue(1))
        prin = card_rows("引导而不是强制", [
            ("你传入值，组件就按你的值渲染", GREEN),
            ("约定写在文档里，人和模型形成同样预期", GREEN),
        ], 12.6, GREEN, 22)
        prin.move_to([0, -0.15, 0])
        self.P(FadeIn(prin, shift=UP * 0.1), rt=0.8)
        self.W(self.cue(2))
        take = fit(T("为智能体好用的改动，往往也让人更好用。", 26, FG), 12.4)
        take.move_to([0, -1.9, 0])
        cap = credit("据 Astryx README「Architecture」「Principles」；官网写超过 180 个组件", 14, 12).move_to([0, -2.5, 0])
        self.P(FadeIn(take), FadeIn(cap), rt=0.6)
        self.finish()

# ───────────────────────────── 片尾
class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        title = T("本周非AI类项目回顾（4 项）", 42, FG, weight=BOLD).to_edge(UP, buff=0.4)
        self.P(FadeIn(title, shift=DOWN * 0.2), rt=0.6)
        tag = {"ax": "人和智能体共用一套设计系统", "he": "普通手表上的爱马仕表盘",
               "su": "社区续命的自托管理财", "un": "可嵌入产品的 Office SDK"}
        rows = Group()
        for pid in ["ax", "he", "su", "un"]:
            d = DATA[pid]
            b = box(13.0, 0.9, r=0.1)
            av = avatar(pid, 0.55)
            rk = T(f"#{d['rank']}", 30, YELLOW, weight=BOLD)
            nm = fit(M(REPO[pid], 24, FG), 5.2)
            tg = fit(T(tag[pid], 20, MUTED), 4.2)
            ws = VGroup(gh_star(0.12), M(f"+{d['week']:,}", 24, YELLOW)).arrange(RIGHT, buff=0.1)
            rk.move_to(b.get_left() + RIGHT * 0.45); av.move_to(b.get_left() + RIGHT * 1.1)
            nm.move_to(b.get_left() + RIGHT * 1.55, aligned_edge=LEFT)
            tg.move_to(b.get_left() + RIGHT * 6.9, aligned_edge=LEFT)
            ws.move_to(b.get_right() + LEFT * 0.3, aligned_edge=RIGHT)
            rows.add(Group(b, rk, av, nm, tg, ws))
        rows.arrange(DOWN, buff=0.16).next_to(title, DOWN, buff=0.35)
        self.P(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15), rt=1.4)
        self.W(self.cue(1))
        kw = VGroup(chip("同一套接口给人和智能体", color=BLUE, size=24),
                    chip("社区把应用接住", color=GREEN, size=24),
                    chip("周榜里也有很具体的设备需求", color=ORANGE, size=24)).arrange(RIGHT, buff=0.22)
        fit(kw, 13.2).next_to(rows, DOWN, buff=0.35)
        self.P(FadeIn(kw[0], scale=0.9), FadeIn(kw[1], scale=0.9), rt=0.6)
        self.W(self.cue(2))
        self.P(FadeIn(kw[2], scale=0.9), rt=0.55)
        self.W(self.cue(3))
        bye = T("下周见", 34, YELLOW).next_to(title, RIGHT, buff=0.4).align_to(title, DOWN)
        self.P(FadeIn(bye), rt=0.5)
        self.finish()
