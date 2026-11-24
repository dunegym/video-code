"""GitHub 本周热榜 Top 5（2026 第 45 周）—— Manim CE 场景。
时间轴由 timing_jingying.json（TTS 词边界实测）驱动；GIF 演示由 assemble_w45.py 用 ffmpeg 叠加到占位图上，
叠加参数由各场景写入 build_jingying/scenes_jingying/ov_<scene>.json。"""
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
TM = json.load(open("timing_jingying.json", encoding="utf-8"))
DATA = json.load(open("data.json", encoding="utf-8"))
A = "assets/proc/"
FONT, MONO = "Noto Sans CJK SC", "Noto Sans Mono CJK SC"
BG, PANEL, BORDER = "#0D1117", "#161B22", "#30363D"
FG, MUTED = "#E6EDF3", "#8B949E"
BLUE, GREEN, YELLOW, PURPLE, ORANGE, RED, TEAL = "#2F81F7", "#3FB950", "#E3B341", "#A371F7", "#F0883E", "#F85149", "#39C5CF"
LANG_COLOR = {"JavaScript": "#F1E05A", "TypeScript": "#3178C6", "Python": "#3572A5", "CSS": "#563D7C", "C": "#A8B9CC", "Rust": "#DEA584"}
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
        json.dump(self.ov, open(f"build_jingying/scenes_jingying/ov_{self.key}.json", "w"), indent=1)
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
    def takeaway(self, s, y=-2.3):
        tb = box(13.2, 0.72, color=GREEN, r=0.12).move_to(UP * y)
        tk = fit(VGroup(T("启示", 24, GREEN, weight=BOLD), T(s, 26, FG)).arrange(RIGHT, buff=0.35), 12.6).move_to(tb)
        return VGroup(tb, tk)
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

# ───────────────────────────── 片头
class S0_Intro(Base):
    key = "S0_Intro"
    def construct(self):
        grid = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                           background_line_style={"stroke_color": "#1B2230", "stroke_width": 1}, axis_config={"stroke_opacity": 0})
        self.add(grid)
        star = gh_star(0.42).move_to(UP * 2.55)
        title = VGroup(T("GitHub 本周热榜", 76, FG, weight=BOLD), T("Top 5", 76, YELLOW, weight=BOLD)).arrange(RIGHT, buff=0.35)
        title.next_to(star, DOWN, buff=0.3)
        date = chip("2026 · 第 45 周 · 11 月 6 日", color=YELLOW, size=26).next_to(title, DOWN, buff=0.3)
        self.P(GrowFromCenter(star), FadeIn(title, shift=UP * 0.3), rt=0.9)
        self.P(Rotate(star, angle=TAU / 5), FadeIn(date, shift=UP * 0.15), rt=0.6)
        order = ["dt", "sk", "t3", "hm", "cm"]
        avs = Group(*[Group(avatar(p, 0.85), M(DATA[p]["owner"], 16, MUTED)).arrange(DOWN, buff=0.1) for p in order]).arrange(RIGHT, buff=0.55)
        avs.next_to(date, DOWN, buff=0.45)
        self.P(LaggedStart(*[FadeIn(a, shift=UP * 0.2) for a in avs], lag_ratio=0.18), rt=1.3)
        self.W(self.cue(1))
        tags = VGroup(
            chip("补记忆", color=BLUE, size=22), chip("管界面", color=PURPLE, size=22),
            chip("控编排", color=GREEN, size=22), chip("装技能", color=ORANGE, size=22),
            chip("终身辅导", color=TEAL, size=22),
        ).arrange(RIGHT, buff=0.18).next_to(avs, DOWN, buff=0.4)
        self.P(LaggedStart(*[FadeIn(c, scale=0.85) for c in tags], lag_ratio=0.15), rt=1.2)
        self.finish()


# ───────────────────────────── #5 DeepTutor
class P5a(IntroScene):
    key = "P5a"; pid = "dt"
    def right(self):
        c = np.array([3.7, 0.35, 0])
        pan = box(6.2, 4.7, fill="#0F141B").move_to(c)
        try:
            g, cap = picture("assets/proc/dt-logo.png", width=5.4, credit="HKUDS/DeepTutor · assets/figs/logo", csize=15)
            g.move_to(c + UP * 1.35)
        except Exception:
            g = T("DeepTutor", 42, FG, weight=BOLD).move_to(c + UP * 1.35); cap = None
        pills = VGroup(*[chip(s, size=20) for s in ["终身辅导", "学习工作区", "多智能体"]]).arrange(RIGHT, buff=0.12)
        fit(pills, 5.8).move_to(c + UP * 0.15)
        feats = VGroup(*[VGroup(Dot(radius=0.06, color=GREEN), fit(T(s, 20, FG), 5.4)).arrange(RIGHT, buff=0.15)
                         for s in ["Chat / Quiz / Research / Mastery", "桌面版 · Docker · CLI", "论文 arXiv:2604.26962"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        feats.move_to(c + DOWN * 1.15)
        self.P(FadeIn(pan), FadeIn(g), rt=0.5)
        if cap: self.P(FadeIn(cap.next_to(g, DOWN, buff=0.08)), rt=0.3)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in pills], lag_ratio=0.2), rt=0.7)
        self.P(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in feats], lag_ratio=0.25), rt=0.9)

class P5b(Base):
    key = "P5b"
    def construct(self):
        hd = self.header("dt", "工作区结构")
        self.add(hd)
        cols = [
            ("主页", ["Chat · Task Board", "Calendar · 笔记本"], BLUE),
            ("学习", ["Books · Mastery Path", "沉浸阅读 · Practice"], GREEN),
            ("资源", ["知识库 · 题库", "学习日志 · 收藏"], PURPLE),
        ]
        cards = VGroup()
        for title, rows, col in cols:
            bb = box(4.0, 2.6, color=col, fill="#0F141B")
            tt = T(title, 30, col, weight=BOLD)
            rs = VGroup(*[fit(T(r, 22, FG), 3.5) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            inner = VGroup(tt, rs).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
            inner.move_to(bb).align_to(bb.get_left() + RIGHT * 0.3, LEFT)
            cards.add(VGroup(bb, inner))
        cards.arrange(RIGHT, buff=0.28).move_to([0, 0.85, 0])
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.25), rt=1.4)
        self.W(self.cue(1))
        mid = VGroup(
            chip("多种模式共用会话上下文", color=YELLOW, size=22),
            chip("知识库可接多种检索后端", color=YELLOW, size=22),
            chip("阅读引用挂回原文", color=YELLOW, size=22),
        ).arrange(RIGHT, buff=0.2).move_to([0, -1.0, 0])
        self.P(LaggedStart(*[FadeIn(x, scale=0.9) for x in mid], lag_ratio=0.2), rt=1.0)
        self.W(self.cue(2))
        acc = chip("账号层：持久伴侣 · 人格预设 · 跨工作区跟随", color=TEAL, size=24).move_to([0, -2.15, 0])
        self.P(FadeIn(acc, shift=UP * 0.1), rt=0.55)
        cap = note("据 DeepTutor README / docs.deeptutor.info 整理重绘", 15, 10).next_to(acc, DOWN, buff=0.12)
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P5c(Base):
    key = "P5c"
    def construct(self):
        hd = self.header("dt", "界面与入口", GREEN)
        self.add(hd)
        g, cap = picture("assets/proc/dt-overview.png", width=11.5, height=5.2, credit="HKUDS/DeepTutor · assets/figs/web-dev/overview.png", csize=16)
        g.move_to([0, 0.35, 0])
        if cap: cap.next_to(g, DOWN, buff=0.1)
        anims=[FadeIn(g)]
        if cap: anims.append(FadeIn(cap))
        self.P(*anims, rt=0.7)
        self.W(self.cue(1))
        row = VGroup(*[chip(s, size=20) for s in ["桌面版捆绑运行时", "Docker 一键试用", "deeptutor.info", "arXiv 论文"]]).arrange(RIGHT, buff=0.18)
        row.move_to([0, -2.55, 0])
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in row], lag_ratio=0.15), rt=0.9)
        self.finish()

# ───────────────────────────── #4 anthropics/skills
class P4a(IntroScene):
    key = "P4a"; pid = "sk"
    def right(self):
        c = np.array([3.7, 0.4, 0])
        pan = box(6.2, 4.6, fill="#0F141B").move_to(c)
        tt = T("一个技能 = 一个文件夹", 26, MUTED).move_to(c + UP * 1.75)
        folder = node("my-skill/", 3.2, 0.9, ORANGE, 26).move_to(c + UP * 0.7)
        md = node("SKILL.md", 3.2, 0.9, BLUE, 26, "YAML + 指令", 16).move_to(c + DOWN * 0.4)
        ar = Arrow(folder.get_bottom(), md.get_top(), buff=0.1, color=MUTED, stroke_width=3)
        where = VGroup(*[chip(s, size=18) for s in ["Claude.ai", "Claude Code", "Claude API"]]).arrange(RIGHT, buff=0.12)
        fit(where, 5.8).move_to(c + DOWN * 1.55)
        nt = note("仓库未声明 SPDX 许可证；含第三方声明", 15, 5.8).next_to(pan, DOWN, buff=0.15)
        self.P(FadeIn(pan), FadeIn(tt), FadeIn(folder), rt=0.5)
        self.P(GrowArrow(ar), FadeIn(md), rt=0.55)
        self.P(LaggedStart(*[FadeIn(x) for x in where], lag_ratio=0.2), FadeIn(nt), rt=0.8)

class P4b(Base):
    key = "P4b"
    def construct(self):
        hd = self.header("sk", "示例技能分类")
        self.add(hd)
        # Categories with counts on chart, narration names groups only
        cats = [
            ("文档办公", 5, "docx · xlsx · pptx · pdf · 共创", BLUE),
            ("前端与视觉", 6, "frontend · theme · canvas · art…", PURPLE),
            ("接口与测试", 3, "mcp-builder · webapp-testing · API", GREEN),
            ("元技能", 2, "skill-creator · academy-guide", YELLOW),
            ("其他", 3, "internal-comms · brand · discernment", MUTED),
        ]
        rows = VGroup()
        y0 = 2.2
        for i, (name, n, ex, col) in enumerate(cats):
            y = y0 - i * 0.85
            lab = T(name, 26, FG).move_to([-5.8, y, 0], aligned_edge=LEFT)
            bar = Rectangle(width=n / 6 * 4.2, height=0.48, stroke_width=0).set_fill(col, 0.9)
            bar.move_to([-2.6, y, 0], aligned_edge=LEFT)
            num = M(str(n), 24, MUTED).next_to(bar, RIGHT, buff=0.12)
            eg = fit(T(ex, 18, MUTED), 5.5).next_to(num, RIGHT, buff=0.3)
            rows.add(VGroup(lab, bar, num, eg))
        cap = note("按 README 示例目录按用途合并（约数，画面标数量）", 15, 10).move_to([-6.5, -2.2, 0], aligned_edge=LEFT)
        self.P(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), FadeIn(r[3])) for r in rows], lag_ratio=0.25), FadeIn(cap), rt=2.8)
        self.W(self.cue(1))
        self.P(Indicate(rows[0], color=WHITE, scale_factor=1.03), rt=0.7)
        self.W(self.cue(2))
        tip = chip("模板 + 规范 → 自定义技能可上传到 Claude.ai / Code / API", color=GREEN, size=22).move_to([0, -2.7, 0])
        self.P(FadeIn(tip, shift=UP * 0.1), rt=0.5)
        self.finish()

class P4c(Base):
    key = "P4c"
    def construct(self):
        hd = self.header("sk", "使用场景", GREEN)
        self.add(hd)
        L = box(6.2, 3.8, color=PURPLE, fill="#0F141B").move_to([-3.35, 0.2, 0])
        R = box(6.2, 3.8, color=BLUE, fill="#0F141B").move_to([3.35, 0.2, 0])
        lt = T("改一页界面", 28, PURPLE, weight=BOLD).move_to(L.get_corner(UL) + np.array([0.3, -0.4, 0]), aligned_edge=LEFT)
        lr = VGroup(*[VGroup(Dot(radius=0.06, color=PURPLE), fit(T(s, 22, FG), 5.4)).arrange(RIGHT, buff=0.15)
                      for s in ["挂上 frontend-design", "按美学约束出方案", "少堆通用「AI 味」组件"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        lr.next_to(lt, DOWN, buff=0.35).align_to(lt, LEFT)
        rt = T("做季度汇报", 28, BLUE, weight=BOLD).move_to(R.get_corner(UL) + np.array([0.3, -0.4, 0]), aligned_edge=LEFT)
        rr = VGroup(*[VGroup(Dot(radius=0.06, color=BLUE), fit(T(s, 22, FG), 5.4)).arrange(RIGHT, buff=0.15)
                      for s in ["doc-coauthoring 定结构", "pptx 技能出幻灯片", "按公司格式落到可下载文件"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        rr.next_to(rt, DOWN, buff=0.35).align_to(rt, LEFT)
        self.P(FadeIn(L), FadeIn(lt), rt=0.4)
        self.P(LaggedStart(*[FadeIn(x) for x in lr], lag_ratio=0.3), rt=1.2)
        self.W(self.cue(1))
        self.P(FadeIn(R), FadeIn(rt), rt=0.4)
        self.P(LaggedStart(*[FadeIn(x) for x in rr], lag_ratio=0.3), rt=1.2)
        self.W(self.cue(2))
        tip = chip("官方示范：技能怎么写、何时加载 —— 不替代产品能力本身", color=YELLOW, size=22).move_to([0, -2.45, 0])
        self.P(FadeIn(tip, shift=UP * 0.1), rt=0.55)
        self.finish()

# ───────────────────────────── #3 t3code
class P3a(IntroScene):
    key = "P3a"; pid = "t3"
    def right(self):
        c = np.array([3.7, 0.35, 0])
        pan = box(6.2, 4.7, fill="#0F141B").move_to(c)
        try:
            g, _ = picture("assets/proc/t3-icon.png", height=1.6, credit=None)
            g.move_to(c + UP * 1.55)
        except Exception:
            g = T("T3 Code", 40, FG, weight=BOLD).move_to(c + UP * 1.55)
        lab = T("Agent harness control surface", 20, MUTED).move_to(c + UP * 0.55)
        clients = VGroup(*[chip(s, size=20) for s in ["Desktop", "Web", "iOS", "Android"]]).arrange(RIGHT, buff=0.12)
        fit(clients, 5.8).move_to(c + DOWN * 0.15)
        note1 = fit(T("自带订阅 · 开源 MIT · 不另收费", 22, FG), 5.8).move_to(c + DOWN * 0.95)
        note2 = fit(T("周增量本周前五最高；排名按页面顺序", 18, YELLOW), 5.8).move_to(c + DOWN * 1.55)
        self.P(FadeIn(pan), FadeIn(g), FadeIn(lab), rt=0.55)
        self.P(LaggedStart(*[FadeIn(x) for x in clients], lag_ratio=0.15), rt=0.7)
        self.P(FadeIn(note1), FadeIn(note2), rt=0.5)

class P3b(Base):
    key = "P3b"
    def construct(self):
        hd = self.header("t3", "控制面边界")
        self.add(hd)
        srv = node("本机服务器", 3.2, 1.1, GREEN, 26, "工作区 · 终端 · 凭证", 16).move_to([-3.8, 1.3, 0])
        orch = node("编排层", 3.0, 1.0, BLUE, 26, "归一化命令 / 事件", 16).move_to([0, 1.3, 0])
        adp = node("提供商适配器", 3.2, 1.0, PURPLE, 24).move_to([3.8, 1.3, 0])
        a1 = Arrow(srv.get_right(), orch.get_left(), buff=0.12, color=MUTED, stroke_width=3)
        a2 = Arrow(orch.get_right(), adp.get_left(), buff=0.12, color=MUTED, stroke_width=3)
        self.P(FadeIn(srv), GrowArrow(a1), FadeIn(orch), GrowArrow(a2), FadeIn(adp), rt=1.2)
        self.W(self.cue(1))
        clients = VGroup(
            node("网页", 2.2, 0.85, FG, 22),
            node("桌面", 2.2, 0.85, FG, 22),
            node("手机", 2.2, 0.85, FG, 22),
        ).arrange(RIGHT, buff=0.35).move_to([0, -0.5, 0])
        rpc = T("鉴权 RPC · 遥控，不替代本机文件系统", 22, YELLOW).next_to(clients, DOWN, buff=0.35)
        arrows = VGroup(*[Arrow(c.get_top(), orch.get_bottom() + DOWN * 0.05 + RIGHT * (i - 1) * 0.3, buff=0.1, color=MUTED, stroke_width=2)
                          for i, c in enumerate(clients)])
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in clients], lag_ratio=0.2), rt=0.8)
        self.P(*[GrowArrow(a) for a in arrows], FadeIn(rpc), rt=0.7)
        self.W(self.cue(2))
        remote = VGroup(*[chip(s, size=20) for s in ["T3 Connect", "局域网配对", "Tailscale"]]).arrange(RIGHT, buff=0.2)
        remote.move_to([0, -2.35, 0])
        self.P(LaggedStart(*[FadeIn(x) for x in remote], lag_ratio=0.2), rt=0.7)
        cap = note("据 pingdotgg/t3code docs/internals/overview.md 与 FAQ 重绘", 15, 10).next_to(remote, DOWN, buff=0.1)
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P3c(Base):
    key = "P3c"
    def construct(self):
        hd = self.header("t3", "对接与定位", GREEN)
        self.add(hd)
        providers = ["Claude Code", "Codex", "Cursor", "Grok Build", "OpenCode", "Antigravity", "fx"]
        chips_ = VGroup(*[chip(p, size=22) for p in providers]).arrange_in_grid(rows=2, cols=4, buff=(0.25, 0.3))
        chips_.move_to([0, 1.1, 0])
        self.P(LaggedStart(*[FadeIn(c, scale=0.9) for c in chips_], lag_ratio=0.12), rt=1.4)
        self.W(self.cue(1))
        pts = VGroup(
            chip("100% 开源 · MIT", color=GREEN, size=24),
            chip("不向用户另收费（自带订阅）", color=GREEN, size=24),
            chip("很早期 · 大功能暂不接贡献", color=YELLOW, size=24),
        ).arrange(DOWN, buff=0.28).move_to([0, -1.1, 0])
        self.P(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in pts], lag_ratio=0.25), rt=1.1)
        src = note("t3.codes · github.com/pingdotgg/t3code", 16, 8).move_to([0, -2.55, 0])
        self.P(FadeIn(src), rt=0.3)
        self.finish()

# ───────────────────────────── #2 hallmark
class P2a(IntroScene):
    key = "P2a"; pid = "hm"
    def right(self):
        c = np.array([3.65, 0.4, 0])
        pan = box(6.3, 4.6, fill="#0F141B").move_to(c)
        g, cap = picture("assets/proc/hallmark-og.png", width=5.8, credit="Nutlope/hallmark · site/OG-hallmark.png", csize=14)
        g.move_to(c + UP * 0.55)
        if cap: cap.next_to(g, DOWN, buff=0.08)
        harness = VGroup(*[chip(s, size=18) for s in ["Claude Code", "Cursor", "Codex", "OpenCode"]]).arrange(RIGHT, buff=0.1)
        fit(harness, 5.9).move_to(c + DOWN * 1.7)
        self.P(FadeIn(pan), FadeIn(g), rt=0.55)
        if cap: self.add(cap)
        self.P(LaggedStart(*[FadeIn(x) for x in harness], lag_ratio=0.15), rt=0.7)

class P2b(Base):
    key = "P2b"
    def construct(self):
        hd = self.header("hm", "门槛与构建流")
        self.add(hd)
        tiers = VGroup(
            node("Floor 底线", 3.6, 1.15, RED, 26, "永不放行", 18),
            node("Reflex 反射", 3.6, 1.15, ORANGE, 26, "可书面豁免", 18),
            node("Finish 收尾", 3.6, 1.15, GREEN, 26, "只报不挡", 18),
        ).arrange(RIGHT, buff=0.3).move_to([0, 2.0, 0])
        self.P(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in tiers], lag_ratio=0.2), rt=1.0)
        self.W(self.cue(1))
        steps = [("抽主题", "五十材质里抽出三个"), ("按动作铺页", "预订 / 购买 / 订阅…"), ("英雄区过审", "单独渲染再继续"), ("浏览器检测", "sloplint --render")]
        nodes = VGroup(*[node(a, 2.9, 1.05, BLUE, 22, b, 15) for a, b in steps]).arrange(RIGHT, buff=0.25).move_to([0, 0.15, 0])
        ars = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.06, color=MUTED, stroke_width=2.5) for i in range(3)])
        self.P(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.1) for n in nodes], lag_ratio=0.2), rt=1.2)
        self.P(*[GrowArrow(a) for a in ars], rt=0.5)
        self.W(self.cue(2))
        tip = chip("主题 = 材质，不规定版式 → 同主题两个提示会做出两页不同的东西", color=YELLOW, size=22).move_to([0, -1.7, 0])
        self.P(FadeIn(tip, shift=UP * 0.1), rt=0.55)
        cap = note("据 hallmark SKILL.md / references/gates.md 重绘", 15, 10).move_to([0, -2.45, 0])
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P2c(Base):
    key = "P2c"
    def construct(self):
        hd = self.header("hm", "主题样例与动词", GREEN)
        self.add(hd)
        imgs = []
        for name, label in [("hallmark-dusk", "Dusk"), ("hallmark-cobalt", "Cobalt"), ("hallmark-atelier", "Atelier")]:
            g, _ = picture(f"assets/proc/{name}.png", width=4.0, height=2.9)
            lab = T(label, 22, MUTED)
            imgs.append(Group(g, lab).arrange(DOWN, buff=0.12))
        row = Group(*imgs).arrange(RIGHT, buff=0.3).move_to([0, 0.85, 0])
        cred = note("Nutlope/hallmark · docs/screenshots/{dusk,cobalt,atelier}.jpg", 14, 12).next_to(row, DOWN, buff=0.15)
        self.P(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in row], lag_ratio=0.2), FadeIn(cred), rt=1.2)
        self.W(self.cue(1))
        verbs = VGroup(
            chip("custom · 丢掉主题，只留底线", color=PURPLE, size=22),
            chip("redesign · 改旧页保内容", color=BLUE, size=22),
            chip("audit · 只出报告", color=GREEN, size=22),
        ).arrange(RIGHT, buff=0.2).move_to([0, -1.55, 0])
        self.P(LaggedStart(*[FadeIn(v, scale=0.9) for v in verbs], lag_ratio=0.2), rt=0.9)
        self.W(self.cue(2))
        rule = chip("截图、数字、照片来自你 —— 模型不编造", color=YELLOW, size=22).move_to([0, -2.5, 0])
        self.P(FadeIn(rule, shift=UP * 0.1), rt=0.5)
        self.finish()

# ───────────────────────────── #1 claude-mem
class P1a(IntroScene):
    key = "P1a"; pid = "cm"
    def right(self):
        c = np.array([3.7, 0.35, 0])
        pan = box(6.2, 4.7, fill="#0F141B").move_to(c)
        try:
            g, cap = picture("assets/proc/cm-logo.png", width=5.4, credit="thedotmack/claude-mem · docs/public logo", csize=14)
            g.move_to(c + UP * 1.4)
            if cap: cap.next_to(g, DOWN, buff=0.08)
        except Exception:
            g = T("claude-mem", 40, FG, weight=BOLD).move_to(c + UP * 1.4); cap = None
        flow = VGroup(
            chip("捕获观察", color=BLUE, size=20),
            chip("压缩摘要", color=PURPLE, size=20),
            chip("注入下次", color=GREEN, size=20),
        ).arrange(RIGHT, buff=0.15)
        fit(flow, 5.8).move_to(c + DOWN * 0.35)
        more = fit(T("Claude Code / Cursor / OpenCode / T3 Code …", 18, MUTED), 5.8).move_to(c + DOWN * 1.2)
        self.P(FadeIn(pan), FadeIn(g), rt=0.5)
        if cap: self.add(cap)
        self.P(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in flow], lag_ratio=0.2), FadeIn(more), rt=0.9)

class P1b(Base):
    key = "P1b"
    def construct(self):
        hd = self.header("cm", "记忆管线")
        self.add(hd)
        nodes = VGroup(
            node("宿主钩子", 2.6, 1.0, BLUE, 24, "工具事件", 16),
            node("SQLite", 2.4, 1.0, MUTED, 24, "观察入库", 16),
            node("Worker", 2.6, 1.0, PURPLE, 24, "SDK 压缩", 16),
            node("下次会话", 2.6, 1.0, GREEN, 24, "上下文注入", 16),
        ).arrange(RIGHT, buff=0.35).move_to([0, 1.6, 0])
        ars = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.08, color=MUTED, stroke_width=3) for i in range(3)])
        self.P(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.1) for n in nodes], lag_ratio=0.2), rt=1.2)
        self.P(*[GrowArrow(a) for a in ars], rt=0.6)
        self.W(self.cue(1))
        search = VGroup(
            node("搜索", 2.5, 0.95, YELLOW, 22),
            node("时间线", 2.5, 0.95, YELLOW, 22),
            node("取观察", 2.5, 0.95, YELLOW, 22),
        ).arrange(RIGHT, buff=0.4).move_to([0, -0.1, 0])
        sar = VGroup(*[Arrow(search[i].get_right(), search[i + 1].get_left(), buff=0.08, color=YELLOW, stroke_width=2.5) for i in range(2)])
        slab = T("分层披露：先定位，再展开，控制令牌", 22, FG).next_to(search, DOWN, buff=0.3)
        self.P(LaggedStart(*[FadeIn(s) for s in search], lag_ratio=0.2), *[GrowArrow(a) for a in sar], FadeIn(slab), rt=1.1)
        self.W(self.cue(2))
        hosts = VGroup(*[chip(s, size=18) for s in ["Claude Code", "Cursor", "OpenCode", "T3 Code", "OpenClaw", "…"]]).arrange(RIGHT, buff=0.12)
        fit(hosts, 12).move_to([0, -1.9, 0])
        self.P(LaggedStart(*[FadeIn(h) for h in hosts], lag_ratio=0.12), rt=0.8)
        cap = note("据 docs.claude-mem.ai / architecture overview 重绘", 15, 10).move_to([0, -2.55, 0])
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P1c(Base):
    key = "P1c"
    def construct(self):
        hd = self.header("cm", "预览与隐私", GREEN)
        self.add(hd)
        # placeholder frame; gif overlay via assemble
        ph = ImageMobject("assets/proc/cm-preview-frame.png").scale_to_fit_width(11.0)
        fr = SurroundingRectangle(ph, buff=0.02, color=BORDER, stroke_width=2)
        g = Group(ph, fr).move_to([0, 0.45, 0])
        cred = note("thedotmack/claude-mem · docs/public/cm-preview.gif", 15, 10).next_to(g, DOWN, buff=0.1)
        self.P(FadeIn(g), FadeIn(cred), rt=0.6)
        # overlay full gif/mp4
        x, y, w, h = to_px(ph)
        self.ov.append({"clip": "assets/proc/cm-preview.mp4", "t0": 0.6, "dur": min(8.0, self.tm["total"] - 1.2),
                        "ss": 0.0, "speed": 1.0, "x": x, "y": y, "w": w, "h": h})
        self.W(self.cue(1))
        row = VGroup(
            chip("自然语言回查项目历史", color=BLUE, size=22),
            chip("<private> 排除敏感内容", color=ORANGE, size=22),
            chip("截图默认关闭", color=MUTED, size=22),
            chip("本地或托管记忆", color=GREEN, size=22),
        ).arrange(RIGHT, buff=0.15)
        fit(row, 13).move_to([0, -2.45, 0])
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in row], lag_ratio=0.15), rt=0.9)
        self.finish()

# ───────────────────────────── 片尾
class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        title = T("本周 Top 5 回顾", 46, FG, weight=BOLD).to_edge(UP, buff=0.35)
        self.P(FadeIn(title, shift=DOWN * 0.2), rt=0.6)
        tag = {"cm": "跨会话记忆：捕获 → 压缩 → 注入", "hm": "反 AI 味：主题材质 + 浏览器 lint",
               "t3": "编码智能体控制面，自带订阅遥控", "sk": "官方 Agent Skills 示例与模板",
               "dt": "终身个性化辅导工作区"}
        rows = Group()
        for pid in ["cm", "hm", "t3", "sk", "dt"]:
            d = DATA[pid]
            b = box(13.0, 0.78, r=0.1)
            av = avatar(pid, 0.5)
            rk = T(f"#{d['rank']}", 30, YELLOW, weight=BOLD)
            nm = fit(M(REPO[pid], 24, FG), 5.0)
            tg = fit(T(tag[pid], 20, MUTED), 4.2)
            ws = VGroup(gh_star(0.12), M(f"+{d['week']:,}", 24, YELLOW)).arrange(RIGHT, buff=0.1)
            rk.move_to(b.get_left() + RIGHT * 0.45); av.move_to(b.get_left() + RIGHT * 1.05)
            nm.move_to(b.get_left() + RIGHT * 1.45, aligned_edge=LEFT)
            tg.move_to(b.get_left() + RIGHT * 6.7, aligned_edge=LEFT)
            ws.move_to(b.get_right() + LEFT * 0.3, aligned_edge=RIGHT)
            rows.add(Group(b, rk, av, nm, tg, ws))
        rows.arrange(DOWN, buff=0.12).next_to(title, DOWN, buff=0.3)
        self.P(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15), rt=1.4)
        self.W(self.cue(1))
        kw = VGroup(chip("记忆 · 界面 · 编排 · 技能", color=BLUE, size=26),
                    chip("DeepTutor：同思路进终身学习", color=TEAL, size=26)).arrange(RIGHT, buff=0.35)
        kw.next_to(rows, DOWN, buff=0.28)
        self.P(FadeIn(kw[0], scale=0.9), rt=0.55)
        self.W(self.cue(2))
        self.P(FadeIn(kw[1], scale=0.9), rt=0.55)
        self.W(self.cue(3))
        bye = T("下周见", 34, YELLOW).next_to(title, RIGHT, buff=0.5).align_to(title, DOWN)
        self.P(FadeIn(bye), rt=0.5)
        self.finish()
