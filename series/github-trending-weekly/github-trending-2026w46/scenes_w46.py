"""GitHub 本周热榜 Top 5（2026 第 46 周）—— Manim CE 场景。
时间轴由 timing_w46.json（MiniMax 词级时间戳）驱动；动图演示由 assemble_w46.py 用 ffmpeg 叠加到占位图上，
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
TM = json.load(open("timing_w46.json", encoding="utf-8"))
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
        star = gh_star(0.42).move_to(UP * 2.2)
        title = VGroup(T("GitHub 本周热榜", 76, FG, weight=BOLD), T("Top 5", 76, YELLOW, weight=BOLD)).arrange(RIGHT, buff=0.35)
        title.next_to(star, DOWN, buff=0.3)
        date = chip("2026 · 第 46 周 · 11 月 13 日", color=YELLOW, size=26).next_to(title, DOWN, buff=0.3)
        self.P(GrowFromCenter(star), FadeIn(title, shift=UP * 0.3), rt=0.9)
        self.P(Rotate(star, angle=TAU / 5), FadeIn(date, shift=UP * 0.15), rt=0.6)
        order = ["cf", "ao", "ab", "omb", "sk"]
        avs = Group(*[Group(avatar(p, 0.85), M(DATA[p]["owner"], 16, MUTED)).arrange(DOWN, buff=0.1) for p in order]).arrange(RIGHT, buff=0.55)
        avs.next_to(date, DOWN, buff=0.45)
        self.P(LaggedStart(*[FadeIn(a, shift=UP * 0.2) for a in avs], lag_ratio=0.18), rt=1.3)
        self.W(self.sub_start("浏览器"))
        tags = VGroup(
            chip("浏览器", color=BLUE, size=22), chip("电脑", color=PURPLE, size=22),
            chip("数据语义", color=GREEN, size=22), chip("安全审计", color=ORANGE, size=22),
            chip("官方技能库", color=TEAL, size=22),
        ).arrange(RIGHT, buff=0.18).next_to(avs, DOWN, buff=0.4)
        self.P(LaggedStart(*[FadeIn(c, scale=0.85) for c in tags], lag_ratio=0.15), rt=1.6)
        self.finish()

# ───────────────────────────── #5 cloudflare/security-audit-skill
class P5a(IntroScene):
    key = "P5a"; pid = "cf"
    def right(self):
        c = np.array([3.7, 0.35, 0])
        pan = box(6.2, 4.7, fill="#0F141B").move_to(c)
        g, cap = picture("assets/proc/cf-hero.png", width=5.5, credit="图：Cloudflare Blog《Build your own vulnerability harness》", csize=14)
        g.move_to(c + UP * 0.85); cap.next_to(g, DOWN, buff=0.08)
        pills = VGroup(chip("六阶段流程", size=19), chip("发现者 ≠ 确认者", size=19), chip("机读结论", size=19)).arrange(RIGHT, buff=0.12)
        fit(pills, 5.8).next_to(cap, DOWN, buff=0.2)
        n1 = fit(T("10/30 周榜第 1 · 本周前五周增最多（排名按页面顺序）", 17, YELLOW), 5.8).next_to(pills, DOWN, buff=0.18)
        self.P(FadeIn(pan), FadeIn(g), FadeIn(cap), rt=0.6)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in pills], lag_ratio=0.2), rt=0.7)
        self.P(FadeIn(n1), rt=0.4)

class P5b(Base):
    key = "P5b"
    def construct(self):
        hd = self.header("cf", "两本账")
        self.add(hd)
        # ledger 1: coverage
        L = box(5.7, 3.3, color=BLUE, fill="#0F141B").move_to([-3.45, 0.95, 0])
        lt = T("覆盖清单", 28, BLUE, weight=BOLD).move_to(L.get_corner(UL) + np.array([0.3, -0.42, 0]), aligned_edge=LEFT)
        rows = VGroup()
        for unit, st, who, col in [("鉴权中间件", "已查", "猎手 A", GREEN), ("文件上传", "已查", "猎手 B", GREEN),
                                   ("Webhook 回调", "待补", "—", YELLOW), ("部署配置", "待验证", "需负责人确认", ORANGE)]:
            r = VGroup(fit(T(unit, 20, FG), 2.0), chip(st, color=col, size=16), fit(T(who, 17, MUTED), 1.6)).arrange(RIGHT, buff=0.25)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(lt, DOWN, buff=0.28).align_to(lt, LEFT)
        R = box(5.9, 3.3, color=PURPLE, fill="#0F141B").move_to([3.35, 0.95, 0])
        rt_ = T("发现记录", 28, PURPLE, weight=BOLD).move_to(R.get_corner(UL) + np.array([0.3, -0.42, 0]), aligned_edge=LEFT)
        verd = VGroup(
            VGroup(chip("确认", color=GREEN, size=20), fit(T("完整源码追踪 · 才有严重度", 19, FG), 3.7)).arrange(RIGHT, buff=0.2),
            VGroup(chip("待验证", color=YELLOW, size=20), fit(T("写明缺的那一个事实 · 无严重度", 19, FG), 3.7)).arrange(RIGHT, buff=0.2),
            VGroup(chip("已否决", color=RED, size=20), fit(T("被证伪的候选也留档", 19, FG), 3.7)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rt_, DOWN, buff=0.32).align_to(rt_, LEFT)
        self.P(FadeIn(L), FadeIn(lt), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.2), rt=1.4)
        self.W(self.sub_start("发现记录"))
        self.P(FadeIn(R), FadeIn(rt_), LaggedStart(*[FadeIn(v, shift=RIGHT * 0.1) for v in verd], lag_ratio=0.25), rt=1.3)
        self.W(self.cue(1))
        chain = VGroup(node("猎手", 1.9, 0.7, ORANGE, 22, "只提候选", 14), node("全新验证者", 2.5, 0.7, GREEN, 22, "任务是证伪", 14),
                       node("写入记录", 2.1, 0.7, PURPLE, 22)).arrange(RIGHT, buff=0.55).move_to([-0.6, -1.4, 0])
        ars = VGroup(*[arrow(chain[i].get_right(), chain[i + 1].get_left(), sw=2.5) for i in range(2)])
        mc = chip("每次更新 → 机器校验", color=TEAL, size=20).next_to(chain, RIGHT, buff=0.45)
        self.P(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.1) for n in chain], lag_ratio=0.2), *[GrowArrow(a) for a in ars], rt=1.1)
        self.W(self.sub_start("两本账每次"))
        self.P(FadeIn(mc, scale=0.9), rt=0.5)
        self.W(self.cue(2))
        self.P(Indicate(verd[1], color=YELLOW, scale_factor=1.05), Indicate(rows[3], color=ORANGE, scale_factor=1.04), rt=1.0)
        cap = credit("据 cloudflare/security-audit-skill README 与技能说明重绘；单元名为示意").move_to([0, -2.45, 0])
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P5c(Base):
    key = "P5c"
    def construct(self):
        hd = self.header("cf", "攻击手册与社区", GREEN)
        self.add(hd)
        items = [("通用攻击类", 9, None), ("原生代码与本地应用", 10, None), ("Web 与客户端", 10, None),
                 ("云与供应链", 8, None), ("协议与数据", 12, None), ("AI 与智能体", 4, None)]
        cols = [MUTED, ORANGE, BLUE, PURPLE, TEAL, GREEN]
        rows = hbars(items, x_lab=-3.75, x_bar=-3.55, y0=2.35, step=0.72, maxv=12, maxw=2.9, size=21, colors=cols)
        ttl = T("攻击类别组（按目标领域合并）", 20, MUTED).move_to([-3.85, 2.95, 0])
        cap1 = credit("按技能附带的攻击手册统计，画面标数量", 14, 6.0).move_to([-3.85, -1.95, 0])
        self.P(FadeIn(ttl), bar_anim(rows, 2.6), FadeIn(cap1), rt=2.6)
        self.W(self.cue(1))
        cards = []
        for tag, col, title, body in [("PR #141", BLUE, "证据附原文引用", "校验器按行逐字节核对 · 待合并"),
                                      ("PR #145", TEAL, "校验器支持 Windows", "身份校验式安全打开 · 待合并")]:
            b = box(6.2, 1.15, color=col, fill="#0F141B")
            inner = VGroup(VGroup(chip(tag, color=col, size=17, font=MONO), T(title, 23, FG, weight=BOLD)).arrange(RIGHT, buff=0.2),
                           fit(T(body, 18, MUTED), 5.6)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            inner.move_to(b).align_to(b.get_left() + RIGHT * 0.25, LEFT)
            cards.append(VGroup(b, inner))
        cards[0].move_to([3.55, 2.25, 0]); cards[1].next_to(cards[0], DOWN, buff=0.22)
        self.P(FadeIn(cards[0], shift=LEFT * 0.2), rt=0.5)
        self.W(self.sub_start("也有人"))
        self.P(FadeIn(cards[1], shift=LEFT * 0.2), rt=0.5)
        self.W(self.cue(2))
        b = box(6.2, 1.7, color=ORANGE, fill="#0F141B").next_to(cards[1], DOWN, buff=0.22)
        inner = VGroup(VGroup(chip("Issue #130", color=ORANGE, size=17, font=MONO), T("侦察点名，清单漏记", 23, FG, weight=BOLD)).arrange(RIGHT, buff=0.2),
                       fit(T("托管 Postgres 未开行级权限，审计没建覆盖单元", 18, MUTED), 5.6),
                       fit(T("两天后服务商告警：公开表可被匿名读写", 18, YELLOW), 5.6)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        inner.move_to(b).align_to(b.get_left() + RIGHT * 0.25, LEFT)
        self.P(FadeIn(VGroup(b, inner), shift=LEFT * 0.2), rt=0.6)
        cap2 = credit("github.com/cloudflare/security-audit-skill · 社区 PR / Issue（11 月）", 14, 6.2).next_to(b, DOWN, buff=0.12)
        self.P(FadeIn(cap2), rt=0.3)
        self.finish()

# ───────────────────────────── #4 NVIDIA/auto-ontology
class P4a(IntroScene):
    key = "P4a"; pid = "ao"
    def right(self):
        c = np.array([3.7, 0.35, 0])
        pan = box(6.2, 4.7, fill="#0F141B").move_to(c)
        g, cap = picture("assets/proc/ao-graph.png", width=5.6, height=3.3, credit="图：NVIDIA/auto-ontology README · 样例库语义图", csize=14)
        g.move_to(c + UP * 0.6); cap.next_to(g, DOWN, buff=0.08)
        pills = VGroup(chip("MCP · CLI · API", size=19), chip("NIM / Nemotron", size=19), chip("Postgres + pgvector", size=19)).arrange(RIGHT, buff=0.1)
        fit(pills, 5.8).next_to(cap, DOWN, buff=0.18)
        self.P(FadeIn(pan), FadeIn(g), FadeIn(cap), rt=0.6)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in pills], lag_ratio=0.2), rt=0.7)

class P4b(Base):
    key = "P4b"
    def construct(self):
        hd = self.header("ao", "语义层怎么来")
        self.add(hd)
        defs = VGroup(node("业务术语", 4.1, 1.2, BLUE, 28, "客户 · 订单 · 发票明细 + 同义词", 19),
                      node("SQL 指标", 4.1, 1.2, GREEN, 28, "复核过的表达式：毛利 · 滚动合计", 19),
                      node("关联", 4.1, 1.2, PURPLE, 28, "表如何连接 · 含桥接表", 19)).arrange(RIGHT, buff=0.3).move_to([0, 2.15, 0])
        self.P(LaggedStart(*[FadeIn(d, shift=DOWN * 0.1) for d in defs], lag_ratio=0.25), rt=1.2)
        self.W(self.cue(1))
        st = VGroup(node("生成草稿", 3.4, 1.1, BLUE, 26, "读元数据 · 采样列值", 18),
                    node("人来认证", 3.4, 1.1, YELLOW, 26, "测试 · 修订 · 认证", 18),
                    node("回答问题", 3.4, 1.1, GREEN, 26, "只用认证过的定义", 18)).arrange(RIGHT, buff=0.8).move_to([0, 0.5, 0])
        sa = VGroup(*[arrow(st[i].get_right(), st[i + 1].get_left()) for i in range(2)])
        self.P(FadeIn(st[0]), GrowArrow(sa[0]), FadeIn(st[1]), rt=0.9)
        self.W(self.sub_start("认证过的"))
        self.P(GrowArrow(sa[1]), FadeIn(st[2]), rt=0.6)
        self.W(self.cue(2))
        steps = VGroup(chip("检索候选术语", color=BLUE, size=20), chip("写出 SQL", color=BLUE, size=20),
                       chip("用真实数据核对筛选值", color=GREEN, size=20), chip("返回答案 + SQL + 步骤", color=GREEN, size=20)).arrange(RIGHT, buff=0.35)
        fit(steps, 13.2).move_to([0, -0.9, 0])
        sar = VGroup(*[arrow(steps[i].get_right(), steps[i + 1].get_left(), sw=2, buff=0.05) for i in range(3)])
        self.P(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.2), *[GrowArrow(a) for a in sar], rt=1.2)
        self.W(self.sub_start("就直说"))
        no = chip("候选撑不起查询 → 直说「这份数据答不了」", color=ORANGE, size=21).move_to([0, -1.8, 0])
        self.P(FadeIn(no, shift=UP * 0.1), rt=0.5)
        cap = credit("据 NVIDIA/auto-ontology README「How it works」重绘").move_to([0, -2.5, 0])
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P4c(Base):
    key = "P4c"
    def construct(self):
        hd = self.header("ao", "官方示例", GREEN)
        self.add(hd)
        g, cap = picture("assets/proc/ao-qa.png", height=4.5, credit="图：NVIDIA/auto-ontology README · Chat 回答示例", csize=14)
        g.move_to([-4.3, 0.6, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.6)
        q1 = box(7.6, 2.35, color=BLUE, fill="#0F141B").move_to([2.95, 1.75, 0])
        qa = VGroup(fit(T("问：2015 年 6 月，宾州「寿司卷 U 盘」收入多少？", 21, FG), 7.1),
                    fit(T("收入 → 发票明细 · 商品 → 库存品 · 州 → 州省", 18, MUTED), 7.1),
                    fit(T("发票明细 → 发票 → 客户 → 城市 → 州省", 18, TEAL), 7.1),
                    fit(T("答：$588.80，来自 3 条发票明细（附 SQL 与步骤）", 21, GREEN), 7.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        qa.move_to(q1).align_to(q1.get_left() + RIGHT * 0.25, LEFT)
        self.P(FadeIn(q1), FadeIn(qa[0]), rt=0.5)
        self.W(self.sub_start("它把词"))
        self.P(FadeIn(qa[1]), rt=0.4); self.P(FadeIn(qa[2]), rt=0.4)
        self.W(self.sub_start("连同"))
        self.P(FadeIn(qa[3]), rt=0.4)
        self.W(self.cue(1))
        q2 = box(7.6, 1.55, color=ORANGE, fill="#0F141B").next_to(q1, DOWN, buff=0.2)
        qb = VGroup(fit(T("问：这款商品 6 月的广告投入回报？", 21, FG), 7.1),
                    fit(T("覆盖度 0.5：没有术语对应「广告投入」→ 先反问", 19, ORANGE), 7.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        qb.move_to(q2).align_to(q2.get_left() + RIGHT * 0.25, LEFT)
        self.P(FadeIn(q2), FadeIn(qb), rt=0.6)
        self.W(self.cue(2))
        warn = chip("评测仓库只给框架，未公布准确率（MarkTechPost，11/01）", color=YELLOW, size=19)
        fit(warn, 7.6).next_to(q2, DOWN, buff=0.22)
        self.P(FadeIn(warn, shift=UP * 0.1), rt=0.5)
        self.finish()

# ───────────────────────────── #3 vercel-labs/agent-browser
class P3a(IntroScene):
    key = "P3a"; pid = "ab"
    def right(self):
        c = np.array([3.7, 0.35, 0])
        pan = box(6.2, 4.7, fill="#0F141B").move_to(c)
        g, cap = picture("assets/proc/ab-home.png", width=5.6, credit="图：agent-browser.dev 文档首页截图", csize=14)
        g.move_to(c + UP * 0.75); cap.next_to(g, DOWN, buff=0.08)
        rel = VGroup(chip("v0.42 · 11/10", color=GREEN, size=19, font=MONO), chip("v0.43 · 11/13", color=GREEN, size=19, font=MONO)).arrange(RIGHT, buff=0.15)
        fit(rel, 5.8).next_to(cap, DOWN, buff=0.2)
        self.P(FadeIn(pan), FadeIn(g), FadeIn(cap), rt=0.6)
        self.P(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in rel], lag_ratio=0.25), rt=0.6)

class P3b(Base):
    key = "P3b"
    def construct(self):
        hd = self.header("ab", "命令短，状态长驻")
        self.add(hd)
        ag = node("智能体", 2.3, 1.15, FG, 25, "一次一条短命令", 17).move_to([-5.7, 1.6, 0])
        cli = node("CLI", 1.5, 1.15, BLUE, 25).move_to([-3.35, 1.6, 0])
        dm = node("守护进程", 2.9, 1.25, PURPLE, 26, "首条命令启动 · 按会话隔离", 17).move_to([-0.35, 1.6, 0])
        a1 = arrow(ag.get_right(), cli.get_left()); a2 = arrow(cli.get_right(), dm.get_left())
        self.P(FadeIn(ag), GrowArrow(a1), FadeIn(cli), GrowArrow(a2), FadeIn(dm), rt=1.2)
        loop = fit(T("快照 → 按编号操作 → 再快照确认", 20, YELLOW), 5.0).next_to(VGroup(ag, dm), DOWN, buff=0.3)
        self.P(FadeIn(loop), rt=0.4)
        self.W(self.sub_start("通过"))
        engines = VGroup(node("Chrome for Testing", 3.4, 0.62, GREEN, 19), node("轻量引擎", 3.4, 0.62, GREEN, 19, None),
                         node("iOS 模拟器 · Safari", 3.4, 0.62, GREEN, 19), node("云端浏览器服务", 3.4, 0.62, GREEN, 19)).arrange(DOWN, buff=0.14)
        engines.move_to([4.6, 1.15, 0])
        cdp = T("Chrome 调试协议", 17, MUTED).move_to([1.95, 2.45, 0])
        a3 = arrow(dm.get_right(), engines[0].get_left(), sw=2.5)
        self.P(GrowArrow(a3), FadeIn(cdp), FadeIn(engines[0]), rt=0.7)
        self.W(self.cue(1))
        a4 = VGroup(*[arrow(dm.get_right(), e.get_left(), sw=2, col="#3D4550") for e in engines[1:]])
        self.P(LaggedStart(*[FadeIn(e) for e in engines[1:]], lag_ratio=0.2), *[GrowArrow(a) for a in a4], rt=1.0)
        self.W(self.cue(2))
        sk = VGroup(node("技能入口", 2.8, 1.0, ORANGE, 24, "很薄，几乎不变", 17),
                    node("运行时向 CLI 取说明", 3.6, 0.9, ORANGE, 23),
                    node("说明与程序同版本", 3.2, 0.9, GREEN, 23)).arrange(RIGHT, buff=0.6).move_to([0, -1.35, 0])
        sa = VGroup(*[arrow(sk[i].get_right(), sk[i + 1].get_left()) for i in range(2)])
        self.P(LaggedStart(*[FadeIn(s) for s in sk], lag_ratio=0.25), *[GrowArrow(a) for a in sa], rt=1.2)
        cap = credit("据 agent-browser README 与 agent-browser.dev 文档重绘").move_to([0, -2.45, 0])
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P3c(Base):
    key = "P3c"
    def construct(self):
        hd = self.header("ab", "命令分组与安全", GREEN)
        self.add(hd)
        items = [("读取与等待", 9, None), ("交互（含标签页）", 19, None), ("截图录制", 5, None), ("页面与网络状态", 7, None),
                 ("调试与观测", 11, None), ("会话与鉴权", 6, None), ("集成与安装", 12, None)]
        cols = [BLUE, BLUE, PURPLE, PURPLE, TEAL, ORANGE, GREEN]
        rows = hbars(items, x_lab=-3.65, x_bar=-3.45, y0=2.25, step=0.64, maxv=19, maxw=3.0, size=20, colors=cols)
        ttl = T("命令数（按 README 命令表合并）", 19, MUTED).move_to([-3.6, 2.85, 0])
        self.P(FadeIn(ttl), bar_anim(rows, 2.8), rt=2.8)
        self.W(self.cue(1))
        sec = VGroup(chip("域名白名单", color=ORANGE, size=21), chip("动作策略", color=ORANGE, size=21),
                     chip("人工确认", color=ORANGE, size=21)).arrange(RIGHT, buff=0.15)
        vault = chip("本地加密保险库：密码不进模型上下文", color=GREEN, size=20)
        sg = VGroup(sec, vault).arrange(DOWN, buff=0.2).move_to([3.6, 2.05, 0])
        fit(sg, 6.4)
        self.P(LaggedStart(*[FadeIn(x, scale=0.9) for x in sec], lag_ratio=0.2), rt=0.8)
        self.W(self.sub_start("密码"))
        self.P(FadeIn(vault, shift=UP * 0.1), rt=0.45)
        self.W(self.cue(2))
        ft = T("保存流程（v0.42，实验性）：录一次，回放逐级降级", 20, FG, weight=BOLD)
        tiers = VGroup(node("① 直接发 HTTP 请求", 4.6, 0.6, GREEN, 19), node("② 在页面里发同一请求", 4.6, 0.6, YELLOW, 19),
                       node("③ 重放录下的命令", 4.6, 0.6, ORANGE, 19)).arrange(DOWN, buff=0.14)
        fg_ = VGroup(fit(ft, 6.4), tiers).arrange(DOWN, buff=0.22).move_to([3.6, -0.3, 0])
        note2 = credit("成功的那一级会被记住；只向公网地址发请求", 14, 6.2).next_to(fg_, DOWN, buff=0.12)
        self.P(FadeIn(fg_[0]), LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in tiers], lag_ratio=0.3), rt=1.3)
        self.P(FadeIn(note2), rt=0.3)
        self.finish()

# ───────────────────────────── #2 OpenMausBot
class P2a(IntroScene):
    key = "P2a"; pid = "omb"
    def right(self):
        c = np.array([3.7, 0.35, 0])
        pan = box(6.2, 4.7, fill="#0F141B").move_to(c)
        ph = ImageMobject("assets/proc/omb-gif-frame.png").scale_to_fit_width(5.6)
        fr = SurroundingRectangle(ph, buff=0.02, color=BORDER, stroke_width=2)
        g = Group(ph, fr).move_to(c + UP * 0.7)
        cap = fit(T("录屏：milind-soni/OpenMausBot 仓库文档", 14, MUTED), 5.8).next_to(g, DOWN, buff=0.08)
        n1 = fit(T("自称 Grok Bot、Muse、dots、Cue 等产品的开源替代", 17, FG), 5.8).next_to(cap, DOWN, buff=0.16)
        n2 = fit(T("README：与 xAI 等公司无关联；也未发行任何代币", 15, MUTED), 5.8).next_to(n1, DOWN, buff=0.1)
        self.P(FadeIn(pan), FadeIn(g), FadeIn(cap), rt=0.6)
        x, y, w, h = to_px(ph)
        self.ov.append({"clip": "assets/proc/omb-gif.mp4", "t0": round(self.t, 3), "dur": round(self.tm["total"] - self.t - 0.6, 3),
                        "ss": 0.0, "speed": 1.0, "x": x, "y": y, "w": w, "h": h})
        self.P(FadeIn(n1), FadeIn(n2), rt=0.5)

class P2b(Base):
    key = "P2b"
    def construct(self):
        hd = self.header("omb", "两个进程")
        self.add(hd)
        ui = node("聊天界面", 2.5, 1.3, BLUE, 26, "桌面 / 网页 / 手机", 17).move_to([-5.5, 1.3, 0])
        srv = box(4.4, 2.6, color=PURPLE, fill="#0F141B").move_to([-0.1, 1.3, 0])
        st = T("本机调度服务器", 24, PURPLE, weight=BOLD).move_to(srv.get_top() + DOWN * 0.38)
        parts = VGroup(chip("驱动注册表", size=18), chip("事件总线", size=18), chip("权限代理", color=ORANGE, size=18)).arrange(DOWN, buff=0.14)
        parts.next_to(st, DOWN, buff=0.22)
        up = arrow(ui.get_right() + UP * 0.25, srv.get_left() + UP * 0.25, sw=2.5)
        dn = arrow(srv.get_left() + DOWN * 0.25, ui.get_right() + DOWN * 0.25, sw=2.5, col=TEAL)
        l1 = T("命令", 17, MUTED).next_to(up, UP, buff=0.06); l2 = T("一条事件流", 17, TEAL).next_to(dn, DOWN, buff=0.06)
        self.P(FadeIn(ui), FadeIn(srv), FadeIn(st), rt=0.7)
        self.P(LaggedStart(*[FadeIn(p) for p in parts], lag_ratio=0.2), GrowArrow(up), FadeIn(l1), GrowArrow(dn), FadeIn(l2), rt=1.2)
        self.W(self.cue(1))
        clis = VGroup(node("Claude CLI", 2.6, 0.7, FG, 20), node("Codex CLI", 2.6, 0.7, FG, 20), node("Grok CLI", 2.6, 0.7, FG, 20)).arrange(DOWN, buff=0.18)
        clis.move_to([4.6, 1.55, 0])
        ars = VGroup(*[arrow(srv.get_right(), c.get_left(), sw=2) for c in clis])
        login = fit(T("用你已登录的账号与订阅", 17, MUTED), 3.2).next_to(clis, DOWN, buff=0.15)
        self.P(LaggedStart(*[FadeIn(c) for c in clis], lag_ratio=0.2), *[GrowArrow(a) for a in ars], FadeIn(login), rt=1.1)
        self.W(self.sub_start("各家协议"))
        uni = chip("各家原生协议 → 统一的运行时事件", color=TEAL, size=20).move_to([0, -0.75, 0])
        self.P(FadeIn(uni, shift=UP * 0.1), rt=0.5)
        self.W(self.cue(2))
        self.P(Indicate(parts[2], color=ORANGE, scale_factor=1.12), rt=0.7)
        card = chip("执行命令 / 改文件 → 对话内卡片：允许 · 拒绝", color=ORANGE, size=21).move_to([0, -1.6, 0])
        self.P(FadeIn(card, shift=UP * 0.1), rt=0.5)
        cap = credit("据 OpenMausBot README「How it works」重绘").move_to([0, -2.45, 0])
        self.P(FadeIn(cap), rt=0.3)
        self.finish()

class P2c(Base):
    key = "P2c"
    def construct(self):
        hd = self.header("omb", "电脑、应用与团队", GREEN)
        self.add(hd)
        g, cap = picture("assets/proc/omb-computer-panel.png", width=7.4, credit="图：OpenMausBot README · Computer 面板", csize=14)
        g.move_to([-3.1, 0.6, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.6)
        runs = VGroup(chip("云端桌面", color=BLUE, size=21), chip("本地虚拟机", color=BLUE, size=21),
                      chip("这台电脑（需明确授权）", color=ORANGE, size=21)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rl = T("每个机器人的电脑", 22, MUTED)
        rg = VGroup(rl, runs).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.15, 1.9, 0])
        self.P(FadeIn(rl), LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in runs], lag_ratio=0.2), rt=1.0)
        self.W(self.cue(1))
        trg = VGroup(T("触发器", 22, MUTED), chip("定时：工作日 9 点汇总收件箱", color=GREEN, size=19),
                     chip("事件：某人来信 → 起草回复", color=GREEN, size=19)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fit(trg, 5.4).next_to(rg, DOWN, buff=0.35).align_to(rg, LEFT)
        self.P(LaggedStart(*[FadeIn(t, shift=LEFT * 0.1) for t in trg], lag_ratio=0.25), rt=1.0)
        self.W(self.cue(2))
        team = chip("一份 Markdown = 整支团队 · 连接默认关 · 例行任务默认暂停", color=YELLOW, size=21)
        fit(team, 13).move_to([0, -2.5, 0])
        self.P(FadeIn(team, shift=UP * 0.1), rt=0.5)
        self.finish()

# ───────────────────────────── #1 anthropics/skills
class P1a(IntroScene):
    key = "P1a"; pid = "sk"
    def right(self):
        c = np.array([3.7, 0.35, 0])
        pan = box(6.2, 4.7, fill="#0F141B").move_to(c)
        tt = T("周增 Stars", 20, MUTED).move_to(c + UP * 1.95)
        maxw = 3.6
        b1 = Rectangle(width=3072 / 6055 * maxw, height=0.42, stroke_width=0).set_fill(MUTED, 0.9)
        b2 = Rectangle(width=maxw, height=0.42, stroke_width=0).set_fill(YELLOW, 0.95)
        l1 = T("上周（#4）", 18, MUTED); l2 = T("本周（#1）", 18, FG)
        r1 = VGroup(l1, b1, M("3,072", 18, MUTED)).arrange(RIGHT, buff=0.15)
        r2 = VGroup(l2, b2, M("6,055", 18, YELLOW)).arrange(RIGHT, buff=0.15)
        bars = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(tt, DOWN, buff=0.2)
        b1.align_to(b2, LEFT)
        lic = box(5.6, 1.85, color=GREEN, fill="#0F141B").move_to(c + DOWN * 0.95)
        li = VGroup(T("11 月 7 日 · 文档技能许可变更", 20, GREEN, weight=BOLD),
                    fit(T("Word · PDF · 演示文稿 · 表格", 20, FG), 5.2),
                    VGroup(chip("源码可见，不得分发", color=RED, size=17), T("→", 22, FG), chip("Apache 2.0", color=GREEN, size=17)).arrange(RIGHT, buff=0.15)
                    ).arrange(DOWN, buff=0.14).move_to(lic)
        self.P(FadeIn(pan), FadeIn(tt), FadeIn(bars), rt=0.7)
        self.W(self.sub_start("这周最大"))
        self.P(FadeIn(lic), FadeIn(li), rt=0.6)

class P1b(Base):
    key = "P1b"
    def construct(self):
        hd = self.header("sk", "分层加载")
        self.add(hd)
        top = chip("这四个文档技能 = Claude 生成文件功能的底层实现", color=GREEN, size=22).move_to([0, 2.65, 0])
        self.P(FadeIn(top, shift=DOWN * 0.1), rt=0.5)
        self.W(self.cue(1))
        g, cap = picture("assets/proc/an-og.png", width=4.4, credit="图：Anthropic Engineering 博客题图", csize=14)
        g.move_to([-4.6, 0.5, 0]); cap.next_to(g, DOWN, buff=0.08)
        lv = []
        for i, (w, col, a, b, tok) in enumerate([(3.7, "#E7A5D8", "名称 + 描述", "常驻上下文", "约 100 词元"),
                                                  (5.2, "#3BB4E0", "技能正文", "触发后读取", "< 5k 词元"),
                                                  (7.0, GREEN, "参考 · 脚本 · 数据", "用到时再打开", "按需，不设上限")]):
            bar = RoundedRectangle(width=w, height=1.0, corner_radius=0.1, stroke_width=0).set_fill(col, 0.9)
            t1 = T(a, 25, BG, weight=BOLD); t2 = T(f"{b} · {tok}", 19, BG)
            inner = VGroup(t1, t2).arrange(DOWN, buff=0.04)
            fit(inner, w - 0.3).move_to(bar)
            grp = VGroup(bar, inner)
            lv.append(grp)
        L = VGroup(*lv).arrange(DOWN, aligned_edge=LEFT, buff=0.18); L.move_to([0, 0.5, 0]).align_to(np.array([-1.55, 0, 0]), LEFT)
        self.P(FadeIn(g), FadeIn(cap), rt=0.5)
        self.P(FadeIn(lv[0], shift=RIGHT * 0.2), rt=0.5)
        self.W(self.sub_start("只占"))
        self.W(self.sub_start("只占") + 1.2)
        self.P(FadeIn(lv[1], shift=RIGHT * 0.2), rt=0.5)
        self.W(self.sub_start("附带"))
        self.P(FadeIn(lv[2], shift=RIGHT * 0.2), rt=0.5)
        self.W(self.cue(2))
        sc = chip("确定性操作交给脚本：例如抽取 PDF 表单字段", color=YELLOW, size=21).move_to([0, -2.05, 0])
        self.P(FadeIn(sc, shift=UP * 0.1), rt=0.5)
        cr = credit("分层数据据 Anthropic《Equipping agents for the real world with Agent Skills》重绘", 14).move_to([0, -2.6, 0])
        self.P(FadeIn(cr), rt=0.3)
        self.finish()

class P1c(Base):
    key = "P1c"
    def construct(self):
        hd = self.header("sk", "同一种写法", GREEN)
        self.add(hd)
        hub = node("Agent Skills 开放规范", 4.6, 1.05, TEAL, 26, "agentskills.io", 16).move_to([0, 1.95, 0])
        self.P(FadeIn(hub, scale=0.9), rt=0.6)
        users = [("cf", "审计技能（#5）"), ("ao", "三个配套技能（#4）"), ("ab", "运行时技能（#3）")]
        cards = Group()
        for pid, lab in users:
            b = box(4.35, 1.1, color=BORDER, fill="#0F141B")
            inner = Group(avatar(pid, 0.55), VGroup(fit(M(DATA[pid]["repo"], 20, FG), 3.45), T(lab, 19, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)).arrange(RIGHT, buff=0.16)
            inner.move_to(b)
            cards.add(Group(b, inner))
        cards.arrange(RIGHT, buff=0.22).move_to([0, 0.2, 0])
        ars = VGroup(*[arrow(hub.get_bottom(), c.get_top(), sw=2) for c in cards])
        self.W(self.sub_start("本周"))
        self.P(GrowArrow(ars[0]), FadeIn(cards[0]), rt=0.5)
        self.W(self.sub_start("NVIDIA"))
        self.P(GrowArrow(ars[1]), FadeIn(cards[1]), rt=0.5)
        self.W(self.sub_start("还有"))
        self.P(GrowArrow(ars[2]), FadeIn(cards[2]), rt=0.5)
        self.W(self.cue(1))
        more = Group()
        for owner, repo, rk, wk in [("mattpocock", "mattpocock/skills", "#7", "+8,731"), ("google", "google/skills", "#10", "+1,933")]:
            b = box(5.2, 0.85, color=BORDER, fill=PANEL)
            inner = Group(T(rk, 24, YELLOW, weight=BOLD), av_owner(owner, 0.45), M(repo, 19, FG),
                          VGroup(gh_star(0.1), M(wk, 18, YELLOW)).arrange(RIGHT, buff=0.08)).arrange(RIGHT, buff=0.2)
            fit(inner, 4.9); inner.move_to(b)
            more.add(Group(b, inner))
        more.arrange(RIGHT, buff=0.4).move_to([0, -1.35, 0])
        self.P(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in more], lag_ratio=0.3), rt=0.9)
        cr = credit("名次与周增来自同一页 GitHub Trending 周榜（11/13）", 14).move_to([0, -2.25, 0])
        self.P(FadeIn(cr), rt=0.3)
        self.finish()

# ───────────────────────────── 片尾
class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        title = T("本周 Top 5 回顾", 46, FG, weight=BOLD).to_edge(UP, buff=0.35)
        self.P(FadeIn(title, shift=DOWN * 0.2), rt=0.6)
        tag = {"sk": "官方技能库：文档技能转 Apache 2.0", "omb": "聊天软件式智能体团队",
               "ab": "智能体专用浏览器命令行", "ao": "数据智能体的业务语义层",
               "cf": "两本账驱动的可复核安全审计"}
        rows = Group()
        for pid in ["sk", "omb", "ab", "ao", "cf"]:
            d = DATA[pid]
            b = box(13.0, 0.78, r=0.1)
            av = avatar(pid, 0.5)
            rk = T(f"#{d['rank']}", 30, YELLOW, weight=BOLD)
            nm = fit(M(REPO[pid], 24, FG), 5.2)
            tg = fit(T(tag[pid], 20, MUTED), 3.9)
            ws = VGroup(gh_star(0.12), M(f"+{d['week']:,}", 24, YELLOW)).arrange(RIGHT, buff=0.1)
            rk.move_to(b.get_left() + RIGHT * 0.45); av.move_to(b.get_left() + RIGHT * 1.05)
            nm.move_to(b.get_left() + RIGHT * 1.45, aligned_edge=LEFT)
            tg.move_to(b.get_left() + RIGHT * 6.95, aligned_edge=LEFT)
            ws.move_to(b.get_right() + LEFT * 0.3, aligned_edge=RIGHT)
            rows.add(Group(b, rk, av, nm, tg, ws))
        rows.arrange(DOWN, buff=0.12).next_to(title, DOWN, buff=0.3)
        self.P(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15), rt=1.4)
        self.W(self.cue(1))
        kw = VGroup(chip("浏览器 · 电脑 · 语义层 → 能动手", color=BLUE, size=26),
                    chip("账本 · 权限卡片 · 认证 → 先拿证据", color=GREEN, size=26)).arrange(RIGHT, buff=0.35)
        fit(kw, 13).next_to(rows, DOWN, buff=0.28)
        self.P(FadeIn(kw[0], scale=0.9), rt=0.55)
        self.W(self.cue(2))
        self.P(FadeIn(kw[1], scale=0.9), rt=0.55)
        self.W(self.cue(3))
        bye = T("下周见", 34, YELLOW).next_to(title, RIGHT, buff=0.5).align_to(title, DOWN)
        self.P(FadeIn(bye), rt=0.5)
        self.finish()
