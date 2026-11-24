"""GitHub 本周热榜 Top 5（2026 第 44 周）—— Manim CE 场景。
时间轴由 timing_w44.json（TTS 词边界实测）驱动；GIF 演示由 assemble_w44.py 用 ffmpeg 叠加到占位图上，
叠加参数由各场景写入 build_w44/ov_<scene>.json。"""
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
TM = json.load(open("timing_w44.json", encoding="utf-8"))
DATA = json.load(open("data.json", encoding="utf-8"))
A = "assets/proc/"
FONT, MONO = "Noto Sans CJK SC", "Noto Sans Mono CJK SC"
BG, PANEL, BORDER = "#0D1117", "#161B22", "#30363D"
FG, MUTED = "#E6EDF3", "#8B949E"
BLUE, GREEN, YELLOW, PURPLE, ORANGE, RED = "#2F81F7", "#3FB950", "#E3B341", "#A371F7", "#F0883E", "#F85149"
LANG_COLOR = {"JavaScript": "#F1E05A", "Python": "#3572A5", "C": "#A8B9CC", "Rust": "#DEA584"}
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
        json.dump(self.ov, open(f"build_w44/ov_{self.key}.json", "w"), indent=1)
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
        date = chip("2026 · 第 44 周 · 10 月 30 日", color=YELLOW, size=26).next_to(title, DOWN, buff=0.3)
        self.P(GrowFromCenter(star), FadeIn(title, shift=UP * 0.3), rt=0.9)
        self.P(Rotate(star, angle=TAU / 5), FadeIn(date, shift=UP * 0.15), rt=0.6)
        order = ["kp", "imp", "seo", "php", "cf"]
        avs = Group(*[Group(avatar(p, 0.85), M(DATA[p]["owner"], 17, MUTED)).arrange(DOWN, buff=0.1) for p in order]).arrange(RIGHT, buff=0.8)
        avs.next_to(date, DOWN, buff=0.5)
        self.P(LaggedStart(*[FadeIn(a, shift=UP * 0.2) for a in avs], lag_ratio=0.2), rt=1.4)
        self.W(self.cue(1))
        b1 = BraceBetweenPoints(avs[0].get_corner(DL) + DOWN * 0.08, avs[2].get_corner(DR) + DOWN * 0.08, direction=DOWN, color=BLUE)
        b2 = BraceBetweenPoints(avs[3].get_corner(DL) + DOWN * 0.08, avs[4].get_corner(DR) + DOWN * 0.08, direction=DOWN, color=RED)
        l1 = T("给智能体立规矩、补专业", 24, BLUE).next_to(b1, DOWN, buff=0.1)
        l2 = T("AI 时代的漏洞攻防", 24, RED).next_to(b2, DOWN, buff=0.1)
        self.P(GrowFromCenter(b1), FadeIn(l1), rt=0.6)
        self.W(self.sub_start("另一半"))
        self.P(GrowFromCenter(b2), FadeIn(l2), rt=0.6)
        self.finish()

# ───────────────────────────── #5 andrej-karpathy-skills
class P5a(IntroScene):
    key = "P5a"; pid = "kp"
    def right(self):
        c = np.array([3.85, 0.35, 0])
        pan = box(6.0, 4.6, fill="#0F141B").move_to(c)
        fl = VGroup(M("CLAUDE.md", 30, FG, weight=BOLD), T("一份文件", 22, MUTED)).arrange(RIGHT, buff=0.3).move_to(c + UP * 1.6)
        big = VGroup(M("65", 96, YELLOW, weight=BOLD), T("行", 30, FG), M("4", 96, GREEN, weight=BOLD), T("条原则", 30, FG)).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        big.move_to(c + UP * 0.35)
        q = fit(T("源自 Andrej Karpathy 2026 年 1 月 26 日的 X 帖子", 20, MUTED), 5.9).move_to(c + DOWN * 0.75)
        fm = VGroup(*[chip(s, size=19) for s in ["Claude Code 插件", "Cursor 规则", "中文 README"]]).arrange(RIGHT, buff=0.12)
        fit(fm, 5.9).move_to(c + DOWN * 1.5)
        nt = VGroup(note("注：原仓库 forrestchang/andrej-karpathy-skills 已转入 multica-ai", 17, 6.0),
                    note("最近一次提交为 4 月 20 日", 17, 6.0)).arrange(DOWN, buff=0.06).next_to(pan, DOWN, buff=0.15)
        self.P(FadeIn(pan), FadeIn(fl), rt=0.5)
        self.P(FadeIn(big, shift=UP * 0.2), FadeIn(q), rt=0.7)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in fm], lag_ratio=0.2), FadeIn(nt), rt=0.9)

class P5b(Base):
    key = "P5b"
    def construct(self):
        hd = self.header("kp", "问题与原则")
        self.add(hd)
        probs = [("擅自假设", "“wrong assumptions… don't seek clarifications”"),
                 ("过度复杂", "“1000 lines when 100 would do”"),
                 ("顺手乱改", "“change/remove… code… orthogonal to the task”")]
        prin = [("先想清楚再写", "说出假设 · 有歧义就问 · 摆出取舍", BLUE), ("简单优先", "不加没要求的功能和抽象", BLUE),
                ("精确修改", "只动必须动的，每行改动都能追溯到需求", BLUE), ("目标驱动执行", "把任务改写成可验证的成功标准", YELLOW)]
        ys = [2.3, 1.05, -0.2, -1.45]
        pl = VGroup()
        for (a, b), y in zip(probs, ys):
            bb = box(4.9, 1.0, color=RED, fill="#1A1215", r=0.1).move_to([-4.15, y, 0])
            g = VGroup(T(a, 26, RED, weight=BOLD), fit(T(b, 18, MUTED, slant=ITALIC), 4.5)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            g.move_to(bb).align_to(bb.get_left() + RIGHT * 0.25, LEFT)
            pl.add(VGroup(bb, g))
        cap = note("Karpathy 原帖摘句（README 引用）", 15, 4.9).next_to(pl, DOWN, buff=0.1).align_to(pl, LEFT)
        rl = VGroup()
        for (a, b, col), y in zip(prin, ys):
            bb = box(6.2, 1.0, color=col, fill="#0F141B", r=0.1).move_to([3.3, y, 0])
            g = VGroup(T(a, 26, col, weight=BOLD), fit(T(b, 18, FG), 5.8)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            g.move_to(bb).align_to(bb.get_left() + RIGHT * 0.25, LEFT)
            rl.add(VGroup(bb, g))
        ar = VGroup(*[Arrow(pl[i].get_right(), rl[i].get_left(), buff=0.1, color=MUTED, stroke_width=3) for i in range(3)])
        self.P(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.15) for p in pl], lag_ratio=0.5), FadeIn(cap), rt=3.0)
        self.W(self.cue(1))
        for i in range(3):
            self.P(GrowArrow(ar[i]), FadeIn(rl[i], shift=LEFT * 0.15), rt=0.55)
            self.W(self.t + 0.5)
        self.P(FadeIn(rl[3], shift=LEFT * 0.15), rt=0.55)
        # 杠杆：模糊任务 → 可验证目标
        self.W(self.cue(2))
        self.P(FadeOut(VGroup(pl, cap, ar)), rl[3][0].animate.set_stroke(YELLOW, 4), rt=0.5)
        a = chip("“修好这个 bug”", color=MUTED, size=26).move_to([-4.15, 2.0, 0])
        b1 = chip("写复现测试", color=YELLOW, size=26); b2 = chip("让测试通过", color=GREEN, size=26)
        bg = VGroup(b1, b2).arrange(RIGHT, buff=0.9).move_to([-4.15, 0.45, 0])
        ar1 = Arrow(a.get_bottom(), b1.get_top(), buff=0.12, color=YELLOW, stroke_width=3)
        ar2 = Arrow(b1.get_right(), b2.get_left(), buff=0.08, color=MUTED, stroke_width=3)
        lp = CurvedArrow(b2.get_bottom() + DOWN * 0.05, b1.get_bottom() + DOWN * 0.05, angle=-TAU / 4, color=GREEN, stroke_width=3)
        lpt = T("自行循环，直到验证通过", 22, GREEN).next_to(lp, DOWN, buff=0.12)
        lev = VGroup(T("杠杆", 24, YELLOW, weight=BOLD), T("把模糊任务改写成可验证的目标", 20, FG)).arrange(RIGHT, buff=0.2).move_to([-4.15, -1.45, 0])
        self.P(FadeIn(a), rt=0.5)
        self.W(self.cue(2) + 1.6)
        self.P(GrowArrow(ar1), FadeIn(b1, shift=UP * 0.1), rt=0.6)
        self.P(GrowArrow(ar2), FadeIn(b2), rt=0.5)
        self.P(Create(lp), FadeIn(lpt), rt=0.7)
        self.P(FadeIn(lev, shift=UP * 0.1), rt=0.5)
        self.finish()

class P5c(Base):
    key = "P5c"
    def construct(self):
        hd = self.header("kp", "例子", GREEN)
        self.add(hd)
        req = chip("用户：“加个导出用户数据的功能”", color=FG, size=26).move_to([0, 2.45, 0])
        L = box(6.3, 3.6, color=RED, fill="#1A1215").move_to([-3.4, 0.0, 0])
        R = box(6.3, 3.6, color=GREEN, fill="#0F1A14").move_to([3.4, 0.0, 0])
        lt = T("✗ 常见做法：默默假设", 26, RED, weight=BOLD).move_to(L.get_corner(UL) + np.array([0.3, -0.45, 0]), aligned_edge=LEFT)
        lr = VGroup(*[VGroup(Dot(radius=0.06, color=RED), T(s, 22, FG)).arrange(RIGHT, buff=0.18) for s in
                      ["直接导出全部用户（分页？隐私？）", "自己决定导出哪些字段", "自己决定文件存在哪里", "照着猜的结构写表头"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        lr.next_to(lt, DOWN, buff=0.35).align_to(lt, LEFT)
        rt_ = T("✓ 先把假设摆出来", 26, GREEN, weight=BOLD).move_to(R.get_corner(UL) + np.array([0.3, -0.45, 0]), aligned_edge=LEFT)
        qs = [("范围", "全部用户，还是筛选后的一部分？"), ("格式", "浏览器下载、后台任务，还是接口？"),
              ("字段", "哪些字段？是否涉及敏感信息？"), ("数据量", "一般有多少用户？")]
        rr = VGroup(*[VGroup(T(a, 21, GREEN, weight=BOLD), T(b, 21, FG)).arrange(RIGHT, buff=0.2) for a, b in qs]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rr.next_to(rt_, DOWN, buff=0.3).align_to(rt_, LEFT)
        fit(rr, 5.8)
        simp = chip("最简单的方案：返回分页 JSON 的接口", color=GREEN, size=21).next_to(rr, DOWN, buff=0.25).align_to(rr, LEFT)
        src = note("据项目 EXAMPLES 示例重绘（multica-ai/andrej-karpathy-skills）", 15, 7).next_to(L, DOWN, buff=0.12).align_to(L, LEFT)
        self.P(FadeIn(req, shift=DOWN * 0.1), rt=0.5)
        self.P(FadeIn(L), FadeIn(lt), rt=0.4)
        self.P(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in lr], lag_ratio=0.4), FadeIn(src), rt=1.8)
        self.W(self.cue(1))
        self.P(FadeIn(R), FadeIn(rt_), rt=0.4)
        self.P(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in rr], lag_ratio=0.35), rt=1.6)
        self.P(FadeIn(simp, shift=UP * 0.1), rt=0.5)
        self.W(self.cue(2))
        tr = chip("取舍：谨慎优先于速度 · 琐碎小改不必走全套", color=YELLOW, size=24).move_to([0, -2.45, 0])
        self.P(FadeIn(tr, shift=UP * 0.15), rt=0.6)
        self.finish()

# ───────────────────────────── #4 impeccable
class P4a(IntroScene):
    key = "P4a"; pid = "imp"
    def right(self):
        c = np.array([3.6, 0.45, 0])
        pan = box(6.4, 4.5, fill="#0F141B").move_to(c)
        tt = T("README 点名的“AI 味”", 24, MUTED).move_to(c + UP * 1.85)
        # 简化示意的“AI 味”页面
        hero = Rectangle(width=5.4, height=1.0, stroke_width=0).set_fill(color=[PURPLE, BLUE], opacity=1).move_to(c + UP * 0.95)
        hero.set_sheen_direction(RIGHT)
        ht = T("Build faster with AI", 24, WHITE, font="Inter" if False else FONT).move_to(hero)
        cards = VGroup()
        for k in range(3):
            ob = box(1.7, 1.2, color=BORDER, fill="#1F2633", r=0.12)
            ic = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.08, stroke_width=0).set_fill(PURPLE, 1).move_to(ob.get_top() + DOWN * 0.3)
            ib = box(1.35, 0.42, color=BORDER, fill="#2A3242", r=0.08).move_to(ob.get_center() + DOWN * 0.25)
            cards.add(VGroup(ob, ic, ib))
        cards.arrange(RIGHT, buff=0.15).move_to(c + DOWN * 0.35)
        tells = VGroup(*[chip(s, color=RED, size=17) for s in ["全站 Inter", "紫蓝渐变", "卡片套卡片", "彩底灰字", "标题上的圆角图标"]]).arrange(RIGHT, buff=0.08)
        fit(tells, 6.1).move_to(c + DOWN * 1.45)
        nt = fit(T("检测器：62 条确定性规则 · 不用大模型、不需 API key", 21, FG), 6.4).next_to(pan, DOWN, buff=0.2)
        cap = note("示意图（本片绘制）· 语言标为 Rust：检测引擎由 Rust 编写", 15, 6.4).next_to(nt, DOWN, buff=0.1)
        self.P(FadeIn(pan), FadeIn(tt), FadeIn(hero), FadeIn(ht), rt=0.6)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in cards], lag_ratio=0.2), rt=0.7)
        self.P(LaggedStart(*[FadeIn(x, scale=0.8) for x in tells], lag_ratio=0.15), rt=1.0)
        self.P(FadeIn(nt), FadeIn(cap), rt=0.5)

class P4b(Base):
    key = "P4b"
    def construct(self):
        hd = self.header("imp", "命令分布与设计")
        self.add(hd)
        items = [("调方向", 9, "bolder · quieter · typeset · layout"), ("收尾打磨", 6, "polish · harden · adapt"),
                 ("规划与设计系统", 4, "shape · init · document"), ("评审", 2, "critique · audit"), ("实时迭代", 2, "live · generate")]
        rows = hbars(items, -3.7, -3.55, 2.3, 0.86, 9, 2.7, size=26, hl=1)
        for r in rows:
            if len(r) > 3: r[3].scale(17 / 21); fit(r[3], 3.1)
        rows2 = VGroup()
        for r in rows:
            if len(r) > 3: r[3].next_to(r[0], DOWN, buff=0.04).align_to(r[0], RIGHT)
        cap = note("README 命令表，另有 1 个已弃用（本片按用途合并）", 16, 6).move_to([-6.8, -1.75, 0], aligned_edge=LEFT)
        self.P(bar_anim(rows, 3.5), FadeIn(cap), rt=3.5)
        self.W(self.sub_start("其次"))
        self.P(Indicate(VGroup(rows[0][0], rows[0][1]), color=WHITE, scale_factor=1.04), rt=0.8)
        # 三层配合
        self.W(self.cue(1))
        x = 3.75
        ly = [("上下文", "产品说明 · 设计规范：为谁设计", PURPLE, 2.2), ("命令", "每条加载一种动作的打法", BLUE, 0.95)]
        Ls = VGroup()
        for a, b, col, y in ly:
            bb = box(5.6, 1.0, color=col, fill="#0F141B", r=0.1).move_to([x, y, 0])
            g = VGroup(T(a, 24, col, weight=BOLD), fit(T(b, 19, FG), 4.0)).arrange(RIGHT, buff=0.3).move_to(bb)
            Ls.add(VGroup(bb, g))
        ag = node("智能体改界面", 2.5, 0.85, MUTED, 22).move_to([x - 1.5, -0.45, 0])
        dt = node("检测器", 2.5, 0.85, GREEN, 22, "62 条规则 · 无 LLM", 15).move_to([x + 1.5, -0.45, 0])
        a1 = CurvedArrow(ag.get_top() + RIGHT * 0.3, dt.get_top() + LEFT * 0.3, angle=-TAU / 6, color=MUTED, stroke_width=3)
        a2 = CurvedArrow(dt.get_bottom() + LEFT * 0.3, ag.get_bottom() + RIGHT * 0.3, angle=-TAU / 6, color=GREEN, stroke_width=3)
        lb = T("每次修改后自动扫描，问题退回重改", 18, GREEN).next_to(VGroup(ag, dt), DOWN, buff=0.45)
        ar = VGroup(Arrow(Ls[0].get_bottom(), Ls[1].get_top(), buff=0.05, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.4),
                    Arrow(Ls[1].get_bottom(), VGroup(ag, dt).get_top() + UP * 0.25, buff=0.05, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.4))
        self.P(FadeIn(Ls[0], shift=DOWN * 0.1), rt=0.5)
        self.W(self.sub_start("命令加载") if any(s["text"].startswith("命令加载") for s in self.tm["subs"]) else self.t + 2.5)
        self.P(GrowArrow(ar[0]), FadeIn(Ls[1], shift=DOWN * 0.1), rt=0.5)
        self.W(self.cue(2))
        self.P(GrowArrow(ar[1]), FadeIn(ag), FadeIn(dt), rt=0.5)
        self.P(Create(a1), rt=0.5)
        self.P(Create(a2), FadeIn(lb), rt=0.6)
        self.W(self.cue(3))
        tk = VGroup(chip("审美 ← 词汇与上下文", color=PURPLE, size=24), chip("底线 ← 确定性规则", color=GREEN, size=24)).arrange(RIGHT, buff=0.4).move_to([0, -2.5, 0])
        self.P(FadeIn(tk, shift=UP * 0.15), rt=0.6)
        self.finish()

class P4c(Base):
    key = "P4c"
    def construct(self):
        hd = self.header("imp", "应用", GREEN)
        self.add(hd)
        g1, _ = picture(A + "imp_without.png", height=4.1); g1.move_to([-3.55, 0.45, 0])
        g2, _ = picture(A + "imp_with.png", height=4.1); g2.move_to([3.15, 0.45, 0])
        t1 = T("不用 Impeccable", 24, MUTED).next_to(g1, UP, buff=0.12)
        t2 = T("用了 Impeccable", 24, GREEN, weight=BOLD).next_to(g2, UP, buff=0.12)
        cap = note("图片来源：pbakaus/impeccable README（Apache-2.0）· 同一模型、同一需求：利古里亚海边民宿 Villa Castagneto", 16, 13).move_to([0, -2.5, 0])
        self.P(FadeIn(g1), FadeIn(t1), rt=0.6)
        self.P(FadeIn(g2), FadeIn(t2), FadeIn(cap), rt=0.6)
        self.W(self.cue(1))
        c1 = VGroup(*[chip(s, size=19) for s in ["奶油底", "细衬线", "胶囊按钮"]]).arrange(RIGHT, buff=0.1).next_to(g1, DOWN, buff=0.12)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in c1], lag_ratio=0.2), rt=0.8)
        self.W(self.cue(2))
        c2 = VGroup(*[chip(s, color=GREEN, size=19) for s in ["夜景主图", "整页围绕一张图展开"]]).arrange(RIGHT, buff=0.1).next_to(g2, DOWN, buff=0.12)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in c2], lag_ratio=0.2), rt=0.6)
        # 社区争议
        self.W(self.cue(3))
        self.P(FadeOut(VGroup(c1, c2, t1, t2, cap)), Group(g1, g2).animate.scale(0.5).move_to([-3.6, 0.6, 0]), rt=0.7)
        cap2 = note("图片来源：pbakaus/impeccable README（Apache-2.0）", 15, 6).next_to(Group(g1, g2), DOWN, buff=0.1)
        hn = box(6.0, 2.9, color=ORANGE, fill="#0F141B").move_to([3.6, 0.6, 0])
        h1 = VGroup(Square(0.46, stroke_width=0).set_fill(ORANGE, 1), T("Hacker News · 2026 年 1 月首发", 24, FG, weight=BOLD)).arrange(RIGHT, buff=0.2)
        h1[0].add(T("Y", 24, WHITE, weight=BOLD).move_to(h1[0]))
        h3 = VGroup(M("103", 32, ORANGE, weight=BOLD), T("points", 19, MUTED), M("64", 32, FG, weight=BOLD), T("comments", 19, MUTED)).arrange(RIGHT, buff=0.15)
        h4 = VGroup(fit(T("评论：当时的前后对比案例并不更好", 19, FG), 5.5),
                    fit(T("作者随后撤下那批案例，并调低宣传口径", 19, FG), 5.5)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        hh = VGroup(h1, h3, h4).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(hn)
        hcap = note("来源：news.ycombinator.com/item?id=46587284", 15, 6).next_to(hn, DOWN, buff=0.1)
        self.P(FadeIn(cap2), FadeIn(hn), FadeIn(hh, shift=UP * 0.1), FadeIn(hcap), rt=0.8)
        self.finish()

# ───────────────────────────── #3 claude-seo
class P3a(IntroScene):
    key = "P3a"; pid = "seo"
    def right(self):
        g, cap = picture(A + "seo_cmd_3.png", width=6.2, credit="图片来源：AgriciDaniel/claude-seo 演示录屏（MIT）")
        g.move_to([3.85, 1.05, 0]); cap.next_to(g, DOWN, buff=0.1)
        ch = VGroup(*[chip(s, color=c, size=21) for s, c in [("26 个子技能", BLUE), ("19 个专职智能体", PURPLE), ("最多 17 个并行", GREEN)]]).arrange(RIGHT, buff=0.12)
        fit(ch, 6.2).next_to(cap, DOWN, buff=0.25)
        n2 = note("完整审计约 10–15 分钟（README）· v2.5.0 于 10 月 22 日发布", 17, 6.2).next_to(ch, DOWN, buff=0.2)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        self.P(LaggedStart(*[FadeIn(x, scale=0.85) for x in ch], lag_ratio=0.2), FadeIn(n2), rt=1.0)

class P3b(Base):
    key = "P3b"
    def construct(self):
        hd = self.header("seo", "审计编排")
        self.add(hd)
        orc = node("总控技能", 3.6, 0.85, YELLOW, 26, "先判断网站的业务类型", 16).move_to([0, 2.35, 0])
        always = [("技术", 0), ("内容", 1), ("结构化数据", 0), ("站点地图", 0), ("性能", 0), ("视觉", 0), ("AI 搜索", 1), ("搜索体验", 1)]
        cond = [("本地商家", 0), ("地图", 0), ("电商", 0), ("外链", 0), ("Google 数据", 0), ("选题集群", 1), ("变化监测", 1)]
        A1 = VGroup(*[node(n, 1.52, 0.72, BLUE, 21) for n, _ in always]).arrange(RIGHT, buff=0.12).move_to([0, 0.95, 0])
        A2 = VGroup()
        for n, _ in cond:
            b = DashedVMobject(box(1.68, 0.72, color=MUTED, fill="#0D1117"), num_dashes=28)
            A2.add(VGroup(b, fit(T(n, 20, FG), 1.5).move_to(b)))
        A2.arrange(RIGHT, buff=0.12).move_to([0, -0.4, 0])
        l1 = T("全面审计时同时派出", 16, MUTED).next_to(A1, UP, buff=0.08).align_to(A1, LEFT)
        l2 = T("按检测到的信号加入", 16, MUTED).next_to(A2, UP, buff=0.08).align_to(A2, LEFT)
        fan = VGroup(*[Line(orc.get_bottom(), n.get_top(), color=BORDER, stroke_width=2) for n in A1])
        self.P(FadeIn(orc, shift=DOWN * 0.1), rt=0.5)
        self.W(self.t + 1.0)
        self.P(LaggedStart(*[Create(f) for f in fan], lag_ratio=0.05), LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in A1], lag_ratio=0.12), FadeIn(l1), rt=1.6)
        self.W(self.sub_start("本地") if any(s["text"].startswith("本地") for s in self.tm["subs"]) else self.t + 2)
        self.P(LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in A2], lag_ratio=0.12), FadeIn(l2), rt=1.3)
        # 模型分配
        self.W(self.cue(1))
        op = [A1[i][0] for i, (_, o) in enumerate(always) if o] + [A2[i][0] for i, (_, o) in enumerate(cond) if o]
        leg = VGroup(VGroup(Square(0.26, stroke_width=0).set_fill(PURPLE, 1), T("Opus：5 个需要判断力的智能体", 19, FG)).arrange(RIGHT, buff=0.12),
                     VGroup(Square(0.26, stroke_width=0).set_fill(BLUE, 1), T("Sonnet：其余 14 个", 19, FG)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.6)
        leg.move_to([0, -1.25, 0])
        self.P(*[m.animate.set_stroke(PURPLE, 4) for m in op], FadeIn(leg), rt=0.8)
        # 汇总
        self.W(self.cue(2))
        agg = node("健康分 + 行动计划", 4.4, 0.8, GREEN, 24).move_to([-2.3, -2.3, 0])
        ck = chip("每条建议：怎样确认它见效", color=GREEN, size=20).next_to(agg, RIGHT, buff=0.35)
        self.P(FadeIn(agg, shift=UP * 0.1), rt=0.5)
        self.P(FadeIn(ck, shift=LEFT * 0.1), rt=0.5)
        cap = note("据 README 与架构文档重绘 · 名称为本片意译", 15, 6).move_to([6.9, -2.95, 0], aligned_edge=RIGHT)
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P3c(Base):
    key = "P3c"
    def construct(self):
        hd = self.header("seo", "应用", GREEN)
        self.add(hd)
        im = ImageMobject(A + "seo_audit_last.png").scale_to_fit_width(7.9).move_to([-2.65, 0.45, 0])
        fr = SurroundingRectangle(im, buff=0.02, color=BORDER, stroke_width=2)
        t0 = 0.5; dur = self.cue(1) - 0.3 - t0
        sp = 10.19 / dur
        cap = fit(T(f"演示来源：AgriciDaniel/claude-seo README（MIT）· {sp:.1f}× 速度", 16, MUTED), 7.9).next_to(fr, DOWN, buff=0.08).align_to(fr, LEFT)
        self.P(FadeIn(im), Create(fr), FadeIn(cap), rt=0.5)
        self.overlay("assets/seo-audit-demo.gif", im, t0, dur, ss=0.0, speed=sp)
        steps = step_list([("抓取首页", "判断业务类型"), ("并行专项分析", "技术 · 内容 · 结构化数据 · 视觉"),
                           ("汇总健康分", None), ("排出行动计划", "按优先级")], 4.0, size=23, color=GREEN)
        steps.move_to([4.6, 0.55, 0])
        marks = [t0 + dur * 0.45, t0 + dur * 0.62, t0 + dur * 0.78, t0 + dur * 0.9]
        for k, tt in enumerate(marks):
            self.W(max(tt, self.t)); self.P(FadeIn(steps[k], shift=LEFT * 0.2), rt=0.45)
        # 命令分布
        self.W(self.cue(1))
        self.P(FadeOut(Group(im, fr, cap, steps)), rt=0.4)
        items = [("技术", 7, None), ("内容与 E-E-A-T", 6, None), ("审计与规划", 5, None), ("扩展数据源", 5, None),
                 ("本地 · 外链 · 电商", 4, None), ("结构化数据与 AI 搜索", 3, None)]
        rows = hbars(items, -1.2, -1.05, 2.3, 0.62, 7, 4.6, size=24, hl=1)
        cc = note("README 命令表，按用途归类（本片整理）", 15, 6).next_to(rows, DOWN, buff=0.2).align_to(rows, LEFT)
        self.P(bar_anim(rows, 3.0), FadeIn(cc), rt=3.0)
        self.W(self.cue(2))
        nt = VGroup(chip("被分析的页面内容会发送给 Claude", color=ORANGE, size=22),
                    chip("公开版 MIT 免费 · 付费社区另有抢先版", color=MUTED, size=22)).arrange(RIGHT, buff=0.3).move_to([0, -2.4, 0])
        fit(nt, 13.2)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in nt], lag_ratio=0.4), rt=0.9)
        self.finish()

# ───────────────────────────── #2 php/php-src
class P2a(IntroScene):
    key = "P2a"; pid = "php"
    def right(self):
        g, cap = picture(A + "phpf_share.png", width=6.0, credit="图片来源：PHP 基金会博客（2026-10-21）")
        g.move_to([3.6, 1.55, 0]); cap.next_to(g, DOWN, buff=0.1)
        rel = VGroup(*[chip(v, color=GREEN, size=19, font=MONO) for v in ["8.5.12", "8.4.27", "8.3.36", "8.2.35"]]).arrange(RIGHT, buff=0.1)
        rel.next_to(cap, DOWN, buff=0.25)
        cv = VGroup()
        for a, b in [("CVE-2026-109618", "内存超限破坏状态 → RCE"), ("CVE-2026-109619", "残留全局状态 → RCE")]:
            cv.add(VGroup(M(a, 19, RED), T(b, 19, FG), chip("CVSS 9.2", color=RED, size=16)).arrange(RIGHT, buff=0.2))
        cv.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(rel, DOWN, buff=0.25)
        fit(cv, 6.6)
        nt = note("注：名次按页面顺序；本项目本周新增星数低于第 3–5 名", 16, 6.6).next_to(cv, DOWN, buff=0.22)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        self.P(LaggedStart(*[FadeIn(x, scale=0.85) for x in rel], lag_ratio=0.15), rt=0.7)
        self.P(FadeIn(cv, shift=UP * 0.1), FadeIn(nt), rt=0.7)

class P2b(Base):
    key = "P2b"
    def construct(self):
        hd = self.header("php", "漏洞在哪")
        self.add(hd)
        sp = VGroup(T("受影响的运行方式", 18, MUTED), *[chip(s, size=18) for s in ["Apache mod_php", "PHP-FPM", "php-cgi", "FrankenPHP", "LiteSpeed"]]).arrange(RIGHT, buff=0.12)
        sp.move_to([0, 2.62, 0])
        wk = box(13.6, 3.7, color=BORDER, fill="#0F141B").move_to([0, 0.0, 0])
        wl = T("同一个工作进程", 18, MUTED).move_to(wk.get_corner(UL) + np.array([0.25, -0.25, 0]), aligned_edge=LEFT)
        st = ["初始化请求", "执行脚本", "清理收尾"]
        la = VGroup(*[node(s, 2.6, 0.8, BLUE, 22) for s in st]).arrange(RIGHT, buff=0.7).move_to([-1.15, 0.45, 0])
        lb = VGroup(*[node(s, 2.6, 0.8, BLUE, 22) for s in st]).arrange(RIGHT, buff=0.7).move_to([-1.15, -0.95, 0])
        ta = T("请求 A", 20, FG).next_to(la, LEFT, buff=0.25); tb = T("请求 B", 20, FG).next_to(lb, LEFT, buff=0.25)
        aa = VGroup(*[Arrow(la[i].get_right(), la[i + 1].get_left(), buff=0.06, color=MUTED, stroke_width=3) for i in range(2)])
        ab = VGroup(*[Arrow(lb[i].get_right(), lb[i + 1].get_left(), buff=0.06, color=MUTED, stroke_width=3) for i in range(2)])
        mm = Rectangle(width=13.0, height=0.34, stroke_width=0).set_fill("#21262D", 1).move_to([0, -1.58, 0])
        mt = T("内存管理与错误处理：贯穿每个请求", 17, MUTED).move_to(mm)
        self.P(FadeIn(sp), rt=0.5)
        self.P(FadeIn(wk), FadeIn(wl), FadeIn(ta), LaggedStart(*[FadeIn(n) for n in la], lag_ratio=0.3), *[GrowArrow(a) for a in aa], FadeIn(mm), FadeIn(mt), rt=1.4)
        # 漏洞一：内存超限 → 长跳转
        self.W(self.cue(1))
        bolt = VGroup(T("内存超限", 20, RED, weight=BOLD)).next_to(la[0], DOWN, buff=0.08)
        half = Rectangle(width=1.25, height=0.8, stroke_width=0).set_fill(RED, 0.35).align_to(la[0], LEFT).align_to(la[0], UP)
        jump = CurvedArrow(la[0].get_top() + RIGHT * 0.6, la[2].get_top() + LEFT * 0.6, angle=-TAU / 7, color=RED, stroke_width=4)
        jl = T("长跳转：直接中止", 18, RED).move_to(jump.point_from_proportion(0.5) + DOWN * 0.32)
        self.P(la[0][0].animate.set_stroke(RED, 4), FadeIn(half), FadeIn(bolt), rt=0.6)
        self.P(Create(jump), FadeIn(jl), FadeOut(bolt), rt=0.8)
        hl = T("状态只初始化一半 → 残缺数据被当成有效", 18, RED).next_to(la, RIGHT, buff=0.25)
        fit(hl, 3.0)
        hl = VGroup(*[T(s, 18, RED) for s in ["状态只初始化一半", "残缺数据被当成有效"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(la, RIGHT, buff=0.25)
        self.P(la[2][0].animate.set_stroke(RED, 4), FadeIn(hl), rt=0.6)
        # 漏洞二：跨请求的释放后使用
        self.W(self.cue(2))
        self.P(FadeIn(tb), LaggedStart(*[FadeIn(n) for n in lb], lag_ratio=0.3), *[GrowArrow(a) for a in ab], rt=1.0)
        uaf = DashedLine(la[2].get_bottom(), lb[1].get_top() + RIGHT * 0.3, color=ORANGE, stroke_width=4)
        ul = VGroup(*[T(s, 18, ORANGE) for s in ["状态仍指向 A 已释放的内存", "被 B 误用"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(lb, RIGHT, buff=0.25)
        self.P(Create(uaf), lb[1][0].animate.set_stroke(ORANGE, 4), FadeIn(ul), rt=0.8)
        self.W(self.cue(3))
        fx = chip("修复：改为安全退出并重置全局状态 · 改动 423 个文件（提交 31c0ea7）", color=GREEN, size=22).move_to([0, -2.42, 0])
        self.P(FadeIn(fx, shift=UP * 0.15), rt=0.6)
        cap = note("据 PHP 安全公告 GHSA-w8hw-w9fx-j79w / GHSA-6wmf-4rv5-p3rp 简化重绘", 15, 8).next_to(fx, DOWN, buff=0.08)
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P2c(Base):
    key = "P2c"
    def construct(self):
        hd = self.header("php", "时间线", GREEN)
        self.add(hd)
        ev = [("2024", "外部审计发现苗头", "Quarkslab · 修复几度停滞", MUTED),
              ("2026-08-11", "Calif 报告无条件 RCE", "OpenAI 独立报告同一根因", ORANGE),
              ("8 – 9 月", "Wiz、OpenAI 补充路径", "Trail of Bits 同期审计", ORANGE),
              ("10-20", "CVE 编号提前泄露", "CVSS 被误标为 10.0", RED),
              ("10-21", "提前发布修复版本", "原定时间之前公开", GREEN),
              ("10-26", "CISA 列入已被利用目录", "KEV · “php2shell”", RED)]
        y = 0.3
        ln = Line([-6.6, y, 0], [6.6, y, 0], color=BORDER, stroke_width=4)
        xs = np.linspace(-5.7, 5.7, len(ev))
        items = []
        for i, ((d, a, b, col), x) in enumerate(zip(ev, xs)):
            dot = Dot([x, y, 0], radius=0.12, color=col)
            dt = M(d, 24, col, weight=BOLD)
            ta = fit(T(a, 23, FG, weight=BOLD), 3.4); tb = fit(T(b, 18, MUTED), 3.4)
            if i % 2 == 0:
                dt.next_to(dot, UP, buff=0.2)
                g = VGroup(ta, tb).arrange(DOWN, buff=0.08).next_to(dt, UP, buff=0.15)
            else:
                dt.next_to(dot, DOWN, buff=0.2)
                g = VGroup(ta, tb).arrange(DOWN, buff=0.08).next_to(dt, DOWN, buff=0.15)
            if g.get_left()[0] < -6.9: g.shift(RIGHT * (-6.9 - g.get_left()[0]))
            if g.get_right()[0] > 6.9: g.shift(LEFT * (g.get_right()[0] - 6.9))
            items.append(VGroup(dot, dt, g))
        cues = [self.cue(0) + 0.6, self.cue(1), self.sub_start("随后") if any(s["text"].startswith("随后") for s in self.tm["subs"]) else self.cue(1) + 2.8, self.cue(2), self.cue(2) + 1.6, self.cue(3)]
        self.P(Create(ln), rt=0.5)
        for it, c in zip(items, cues):
            self.W(max(c, self.t)); self.P(FadeIn(it, shift=UP * 0.1), rt=0.5)
        self.W(self.cue(4))
        q = box(12.6, 0.95, color=YELLOW, fill="#0F141B").move_to([0, -2.25, 0])
        qt = fit(VGroup(T("PHP 基金会", 22, YELLOW, weight=BOLD), T("7 月以来发布 15 个 CVE，另处理了 100 多份无效报告；AI 辅助研究让报告量大增", 21, FG)).arrange(RIGHT, buff=0.3), 12.2).move_to(q)
        src = note("来源：PHP 基金会博客（10-21）· CISA KEV · CERT-EU；日期为 UTC", 15, 8).next_to(q, DOWN, buff=0.08)
        self.P(FadeIn(q), FadeIn(qt), FadeIn(src), rt=0.6)
        self.finish()

# ───────────────────────────── #1 cloudflare/security-audit-skill
class P1a(IntroScene):
    key = "P1a"; pid = "cf"
    def right(self):
        g, cap = picture(A + "cf_blog_hero.png", width=6.2, credit="图片来源：Cloudflare 博客《Build your own vulnerability harness》")
        g.move_to([3.85, 1.35, 0]); fit(cap, 6.2).next_to(g, DOWN, buff=0.1)
        ch = VGroup(chip("6 月 18 日随博客开源", color=ORANGE, size=21), chip("最近一次推送：9 月 14 日", size=21)).arrange(RIGHT, buff=0.15)
        fit(ch, 6.2).next_to(cap, DOWN, buff=0.25)
        nt = note("第三方文章记录：10 月 24 日约 4.34 万星，与本周增量大致吻合", 16, 6.2).next_to(ch, DOWN, buff=0.22)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        self.P(FadeIn(ch, shift=UP * 0.1), FadeIn(nt), rt=0.8)

class P1b(Base):
    key = "P1b"
    def construct(self):
        hd = self.header("cf", "审计流程")
        self.add(hd)
        ph = [("侦察", "架构 · 信任边界\n输入面 → 覆盖清单", BLUE), ("猎手", "彼此隔离\n按清单逐块找", ORANGE),
              ("验证者", "全新上下文\n任务是证伪", RED), ("结构化记录", "按规范\n机器校验", PURPLE),
              ("独立复核", "新智能体\n对照源码", PURPLE), ("报告", "不针对\n特定目标", GREEN)]
        ns = VGroup()
        for a, b, col in ph:
            bb = box(2.0, 1.55, color=col, fill="#0F141B", r=0.12)
            g = VGroup(T(a, 24, col, weight=BOLD), T(b, 16, FG, line_spacing=0.8)).arrange(DOWN, buff=0.12).move_to(bb)
            fit(g, 1.85)
            ns.add(VGroup(bb, g))
        ns.arrange(RIGHT, buff=0.28).move_to([0, 1.45, 0])
        ar = VGroup(*[Arrow(ns[i].get_right(), ns[i + 1].get_left(), buff=0.03, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.5) for i in range(5)])
        nums = VGroup(*[M(str(i + 1), 18, MUTED).next_to(ns[i], UP, buff=0.08) for i in range(6)])
        crit = node("覆盖评审", 2.0, 0.6, ORANGE, 19).next_to(ns[1], DOWN, buff=0.55)
        ca = CurvedArrow(crit.get_left(), ns[0].get_bottom() + RIGHT * 0.3, angle=-TAU / 6, color=ORANGE, stroke_width=2.5)
        cl = T("找没覆盖到的空白", 15, ORANGE).next_to(crit, DOWN, buff=0.08)
        vd = VGroup(chip("确认", color=GREEN, size=17), chip("待验证", color=YELLOW, size=17), chip("驳回", color=RED, size=17)).arrange(DOWN, buff=0.08)
        vd.next_to(ns[2], DOWN, buff=0.25)
        # 时间轴
        self.P(FadeIn(ns[0], shift=RIGHT * 0.1), FadeIn(nums[0]), rt=0.5)
        self.W(self.cue(1))
        self.P(GrowArrow(ar[0]), FadeIn(ns[1], shift=RIGHT * 0.1), FadeIn(nums[1]), rt=0.5)
        self.W(self.sub_start("另有") if any(s["text"].startswith("另有") for s in self.tm["subs"]) else self.t + 1.5)
        self.P(FadeIn(crit), Create(ca), FadeIn(cl), rt=0.6)
        self.W(self.cue(2))
        self.P(GrowArrow(ar[1]), FadeIn(ns[2], shift=RIGHT * 0.1), FadeIn(nums[2]), rt=0.5)
        self.P(LaggedStart(*[FadeIn(v) for v in vd], lag_ratio=0.3), rt=0.7)
        self.W(self.cue(3))
        for k in (3, 4, 5):
            self.P(GrowArrow(ar[k - 1]), FadeIn(ns[k], shift=RIGHT * 0.1), FadeIn(nums[k]), rt=0.45)
        self.W(self.cue(4))
        sep = VGroup(ns[1][0].copy().set_fill(opacity=0).set_stroke(YELLOW, 5), ns[2][0].copy().set_fill(opacity=0).set_stroke(YELLOW, 5))
        rule = chip("发现者 ≠ 确认者", color=YELLOW, size=30).move_to([2.6, -1.0, 0])
        pr = VGroup(*[chip(s, size=18) for s in ["严重性必须有实际影响", "纵深防御缺口不算漏洞", "要求系统级沙箱运行"]]).arrange(RIGHT, buff=0.12).move_to([0, -2.3, 0])
        self.P(Create(sep), FadeIn(rule, scale=0.9), rt=0.6)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in pr], lag_ratio=0.25), rt=0.9)
        cap = note("据 cloudflare/security-audit-skill 技能说明简化重绘", 15, 6).next_to(pr, DOWN, buff=0.1)
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P1c(Base):
    key = "P1c"
    def construct(self):
        hd = self.header("cf", "攻击手册与实战数据", GREEN)
        self.add(hd)
        items = [("内存安全与二进制", 20), ("Web 协议与认证", 20), ("桌面 / 移动 / IPC", 16), ("云与部署", 15), ("数据隔离与生命周期", 15),
                 ("AI 与 LLM 智能体", 14), ("客户端", 14), ("协议 / RPC / 消息", 14), ("资源耗尽", 13), ("供应链与发布", 12)]
        cols = [GREEN, GREEN] + [BLUE] * 3 + [PURPLE] + [BLUE] * 4
        rows = hbars(items, -3.65, -3.5, 2.55, 0.43, 20, 2.6, size=19, colors=cols)
        gen = note("另有通用核心类别 9 类：注入、越权、文件处理、密钥与加密……", 16, 6.4).move_to([-6.9, -1.85, 0], aligned_edge=LEFT)
        cc = note("各目标手册的攻击类别数（按小标题计，约数）", 15, 6.4).next_to(gen, DOWN, buff=0.08).align_to(gen, LEFT)
        self.P(bar_anim(rows, 3.0), rt=3.0)
        self.P(FadeIn(gen), FadeIn(cc), rt=0.5)
        self.W(self.sub_start("最广") if any(s["text"].startswith("最广") for s in self.tm["subs"]) else self.t)
        self.P(Indicate(VGroup(rows[0], rows[1]), color=WHITE, scale_factor=1.03), rt=0.9)
        # 漏斗（据博客数据重绘）
        self.W(self.cue(1))
        tt = T("内部系统 · 覆盖 128 个代码库 · 约 6 周", 22, FG, weight=BOLD).move_to([3.75, 2.55, 0])
        fz = [(20799, "原始候选", ORANGE), (12057, "通过对抗验证", YELLOW), (7245, "去重研判后交给工程团队", GREEN)]
        fb = VGroup()
        for i, (v, lab, col) in enumerate(fz):
            r = Rectangle(width=5.6 * v / 20799, height=0.55, stroke_width=0).set_fill(col, 0.85).move_to([1.0, 1.7 - i * 0.95, 0], aligned_edge=LEFT)
            n = M(f"{v:,}", 24, BG if v > 9000 else FG, weight=BOLD)
            n.move_to(r) if v > 9000 else n.next_to(r, RIGHT, buff=0.12)
            l = T(lab, 18, MUTED).next_to(r, DOWN, buff=0.06).align_to(r, LEFT)
            fb.add(VGroup(r, n, l))
        sev = fit(T("其中可从公网利用 396 · 严重 41 / 高 777 / 中低 6,427", 18, FG), 5.9).move_to([3.85, -1.3, 0])
        src = note("数据：Cloudflare 博客（2026-06-18），交付数含另一套系统的 1,784 条", 15, 5.9).next_to(sev, DOWN, buff=0.1)
        self.P(FadeIn(tt), rt=0.4)
        self.P(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], LEFT), FadeIn(b[1]), FadeIn(b[2])) for b in fb], lag_ratio=0.5), rt=2.0)
        self.P(FadeIn(sev), FadeIn(src), rt=0.5)
        self.W(self.cue(2))
        tk = chip("单次运行 ≈ 多次运行总量的一半 → 每轮盯着上一轮的空白补查", color=YELLOW, size=24).move_to([0, -2.6, 0])
        self.P(FadeOut(VGroup(gen, cc)), FadeIn(tk, shift=UP * 0.15), rt=0.6)
        self.finish()

# ───────────────────────────── 片尾
class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        title = T("本周 Top 5 回顾", 46, FG, weight=BOLD).to_edge(UP, buff=0.35)
        self.P(FadeIn(title, shift=DOWN * 0.2), rt=0.6)
        tag = {"cf": "对抗式安全审计：发现者不确认", "php": "两个 RCE · 10 月 21 日紧急修复", "seo": "多智能体并行的 SEO 审计",
               "imp": "设计词汇 + 62 条检测规则", "kp": "一份文件，四条编码原则"}
        rows = Group()
        for pid in ["cf", "php", "seo", "imp", "kp"]:
            d = DATA[pid]
            b = box(13.0, 0.78, r=0.1)
            av = avatar(pid, 0.5)
            rk = T(f"#{d['rank']}", 30, YELLOW, weight=BOLD)
            nm = fit(M(REPO[pid], 24, FG), 5.2)
            tg = fit(T(tag[pid], 22, MUTED), 4.0)
            ws = VGroup(gh_star(0.12), M(f"+{d['week']:,}", 24, YELLOW)).arrange(RIGHT, buff=0.1)
            rk.move_to(b.get_left() + RIGHT * 0.45); av.move_to(b.get_left() + RIGHT * 1.05)
            nm.move_to(b.get_left() + RIGHT * 1.45, aligned_edge=LEFT)
            tg.move_to(b.get_left() + RIGHT * 6.9, aligned_edge=LEFT)
            ws.move_to(b.get_right() + LEFT * 0.3, aligned_edge=RIGHT)
            rows.add(Group(b, rk, av, nm, tg, ws))
        rows.arrange(DOWN, buff=0.12).next_to(title, DOWN, buff=0.3)
        self.P(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15), rt=1.4)
        self.W(self.cue(1))
        kw = VGroup(chip("规则 · 词汇 · 流程：约束智能体", color=BLUE, size=26), chip("AI 找得更快 · 验证与修复靠人", color=RED, size=26)).arrange(RIGHT, buff=0.4)
        kw.next_to(rows, DOWN, buff=0.3)
        self.P(FadeIn(kw[0], scale=0.9), rt=0.6)
        self.W(self.cue(2))
        self.P(FadeIn(kw[1], scale=0.9), rt=0.6)
        self.W(self.cue(3))
        bye = T("下周见", 34, YELLOW).next_to(title, RIGHT, buff=0.5).align_to(title, DOWN)
        self.P(FadeIn(bye), rt=0.5)
        self.finish()
