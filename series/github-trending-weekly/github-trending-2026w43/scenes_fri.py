"""GitHub 本周热门 Top 5（v4：功能分布 + 具体案例，去掉常识介绍和生硬过渡）—— Manim CE 场景。
时间轴由 timing_v5.json（TTS 词边界实测）驱动；GIF 演示由 assemble_v2.py 用 ffmpeg 叠加到占位图上，
叠加参数由各场景写入 build5/ov_<scene>.json。"""
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
TM = json.load(open("timing_fri.json", encoding="utf-8"))
DATA = json.load(open("data.json", encoding="utf-8"))
A = "assets/proc/"
FONT, MONO = "Noto Sans CJK SC", "Noto Sans Mono CJK SC"
BG, PANEL, BORDER = "#0D1117", "#161B22", "#30363D"
FG, MUTED = "#E6EDF3", "#8B949E"
BLUE, GREEN, YELLOW, PURPLE, ORANGE, RED = "#2F81F7", "#3FB950", "#E3B341", "#A371F7", "#F0883E", "#F85149"
LANG_COLOR = {"TypeScript": "#3178C6", "Python": "#3572A5", "Kotlin": "#A97BFF"}
REPO = {"android": "android/skills", "ruflo": "ruvnet/ruflo", "science": "K-Dense-AI/scientific-agent-skills",
        "plugins": "anthropics/claude-plugins-official", "rea": "morluto/rea"}
OWNER_AV = {"android": "android", "ruflo": "ruvnet", "science": "K-Dense-AI", "plugins": "anthropics", "rea": "morluto"}

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
        json.dump(self.ov, open(f"build_fri/ov_{self.key}.json", "w"), indent=1)
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
        rank_lab = T("本周热门", 24, MUTED).next_to(rank, RIGHT, buff=0.25).align_to(rank, DOWN).shift(UP * 0.18)
        av = avatar(self.pid, 0.46)
        owner = M(d["owner"] + " /", 28, MUTED)
        og = Group(av, owner).arrange(RIGHT, buff=0.15).next_to(rank, DOWN, buff=0.25).align_to(rank, LEFT)
        repo = fit(M(d["repo"], 44, FG, weight=BOLD), 6.1).next_to(og, DOWN, buff=0.12).align_to(rank, LEFT)
        chips = VGroup(chip(d["language"], dot=LANG_COLOR.get(d["language"], MUTED), size=22),
                       chip(d["license"], size=22), chip("创建于 " + d["created"][:7], size=22)).arrange(RIGHT, buff=0.16)
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

class P4a(IntroScene):
    key = "P4a"; pid = "ruflo"
    def right(self):
        g, cap = picture(A + "ruflo_capabilities.png", width=7.0, credit="图片来源：ruvnet/ruflo README（MIT）")
        g.move_to([3.5, 1.3, 0]); cap.next_to(g, DOWN, buff=0.1)
        l1 = T("前身：Claude Flow（2025-06-02 首次提交）", 22, MUTED)
        l2 = VGroup(T("Agent =", 30, FG), T("Model", 30, PURPLE), T("+", 30, FG), T("Harness", 30, BLUE, weight=BOLD)).arrange(RIGHT, buff=0.18)
        gg = VGroup(l1, l2).arrange(DOWN, buff=0.3).move_to([3.55, -1.55, 0])
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        self.P(FadeIn(gg, shift=UP * 0.15), rt=0.7)

class P3a(IntroScene):
    key = "P3a"; pid = "science"
    def right(self):
        g, cap = picture(A + "kd_scanpy.png", width=6.5, credit="图片来源：K-Dense-AI/scientific-agent-skills docs/images（MIT）")
        g.move_to([3.6, 0.75, 0]); cap.next_to(g, DOWN, buff=0.1)
        doms = VGroup(*[chip(s, color=GREEN, size=20) for s in ["生物", "化学", "医学", "物理", "工程", "地球科学"]]).arrange(RIGHT, buff=0.1)
        fit(doms, 6.5).next_to(cap, DOWN, buff=0.25)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        self.P(LaggedStart(*[FadeIn(x, scale=0.8) for x in doms], lag_ratio=0.12), rt=1.2)
        nt = fit(T("注：名次按 GitHub 榜单页面顺序，本项目本周新增星数高于第三、四名", 17, MUTED), 6.6).next_to(doms, DOWN, buff=0.3)
        self.P(FadeIn(nt), rt=0.5)

class P1a(IntroScene):
    key = "P1a"; pid = "rea"
    def right(self):
        g, cap = picture(A + "rea_showcases.png", width=6.6, credit="图片来源：morluto/rea README（MIT）")
        g.move_to([3.6, 1.6, 0]); cap.next_to(g, DOWN, buff=0.1)
        cs = VGroup(*[T(s, 18, MUTED) for s in ["DX-Ball：还原声像计算", "Notion：追踪剪贴板桥接", "东方 TH04：还原弹幕环计算"]]).arrange(RIGHT, buff=0.35)
        fit(cs, 6.6).next_to(cap, DOWN, buff=0.2)
        note = T("分析在本地运行 · 最新版本 6.7.0（10 月 18 日）", 22, FG).move_to([3.6, -1.1, 0])
        cmd = T("注：本周新增星数远高于同榜其他项目，数据以 GitHub 页面为准", 17, MUTED).next_to(note, DOWN, buff=0.3)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(cap), rt=0.8)
        self.P(FadeIn(cs), rt=0.6)
        self.P(FadeIn(note), FadeIn(cmd), rt=0.8)

# ───────────────────────────── 片头 / 片尾
# ───────────────────────────── #5 android/skills
# ───────────────────────────── #4 ruflo
# ───────────────────────────── #3 K-Dense-AI/scientific-agent-skills
class P3c(Base):
    key = "P3c"
    def construct(self):
        hd = self.header("science", "应用", GREEN)
        self.P(FadeIn(hd), rt=0.4)
        ttl = T("示例：EGFR 抑制剂药物发现（README 示例提示词）", 26, FG).move_to([0, 2.6, 0])
        st = [("ChEMBL 检索", "IC50 < 50 nM 的 EGFR 抑制剂", "database-lookup"),
              ("构效关系", "RDKit 分析 SAR", "rdkit"),
              ("生成类似物", "datamol 改造结构", "datamol"),
              ("分子对接", "DiffDock + AlphaFold EGFR", "diffdock"),
              ("文献与突变", "PubMed · COSMIC", "paper-lookup"),
              ("出图与报告", "可视化 + 汇总", "scientific-visualization")]
        nodes = VGroup()
        for a, b, k in st:
            n = node(a, 3.7, 1.15, BLUE, 24, b, 17)
            kc = fit(chip(k, color=PURPLE, size=16, font=MONO), 3.5)
            nodes.add(VGroup(n, kc.next_to(n, DOWN, buff=0.1)))
        row1 = VGroup(*nodes[:3]).arrange(RIGHT, buff=0.75); row2 = VGroup(nodes[5], nodes[4], nodes[3]).arrange(RIGHT, buff=0.75)
        VGroup(row1, row2).arrange(DOWN, buff=0.55).move_to([0, 0.05, 0])
        ar = VGroup()
        for i in range(5):
            a, b = nodes[i][0], nodes[i + 1][0]
            if i == 2:
                ar.add(Arrow(nodes[i][1].get_bottom(), b.get_top(), buff=0.06, color=MUTED, stroke_width=3))
            elif i < 2:
                ar.add(Arrow(a.get_right(), b.get_left(), buff=0.06, color=MUTED, stroke_width=3))
            else:
                ar.add(Arrow(a.get_left(), b.get_right(), buff=0.06, color=MUTED, stroke_width=3))
        self.P(FadeIn(ttl), rt=0.5)
        for i in range(6):
            an = [FadeIn(nodes[i], shift=RIGHT * 0.15)]
            if i: an.append(GrowArrow(ar[i - 1]))
            self.P(*an, rt=0.55)
            self.W(self.t + 0.6)
        # 官方流程图
        self.W(self.cue(1))
        g, cap = picture(A + "kd_rdkit.png", width=8.9, credit="图片来源：K-Dense-AI/scientific-agent-skills docs/images（MIT）", csize=16)
        g.move_to([0, 0.3, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeOut(VGroup(ttl, nodes, ar)), rt=0.4)
        self.P(FadeIn(g, scale=0.95), FadeIn(cap), rt=0.7)
        watch = SurroundingRectangle(g[0], color=RED, stroke_width=3).stretch_to_fit_height(g.height * 0.17)
        watch.move_to(g[0].get_bottom() + UP * g.height * 0.105)
        self.W(self.cue(1) + 3.0)
        self.P(Create(watch), rt=0.6)
        self.W(self.sub_start("正是通用"))
        self.P(Indicate(watch, color=YELLOW, scale_factor=1.02), rt=0.9)
        self.finish()

# ───────────────────────────── #2 anthropics/claude-plugins-official
# ───────────────────────────── #1 morluto/rea
# ───────────────────────────── 片头 / 片尾
class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        title = T("本周 Top 5 回顾", 46, FG, weight=BOLD).to_edge(UP, buff=0.5)
        self.P(FadeIn(title, shift=DOWN * 0.2), rt=0.6)
        arch = {"rea": "智能体 + 本地逆向工具", "plugins": "315 个插件，开发类最多", "science": "177 个科研技能",
                "ruflo": "模型外的编排外壳", "android": "33 个技能，分 8 类"}
        rows = Group()
        for pid in ["rea", "plugins", "ruflo", "android", "science"]:
            d = DATA[pid]
            b = box(13.0, 0.78, r=0.1)
            av = avatar(pid, 0.5)
            rk = T(f"#{d['rank']}", 30, YELLOW, weight=BOLD)
            nm = fit(M(REPO[pid], 24, FG), 5.2)
            tag = fit(T(arch[pid], 22, MUTED), 3.2)
            ws = VGroup(gh_star(0.12), M(f"+{d['week']:,}", 24, YELLOW)).arrange(RIGHT, buff=0.1)
            rk.move_to(b.get_left() + RIGHT * 0.45); av.move_to(b.get_left() + RIGHT * 1.05)
            nm.move_to(b.get_left() + RIGHT * 1.45, aligned_edge=LEFT)
            tag.move_to(b.get_left() + RIGHT * 7.2, aligned_edge=LEFT)
            ws.move_to(b.get_right() + LEFT * 0.3, aligned_edge=RIGHT)
            rows.add(Group(b, rk, av, nm, tag, ws))
        rows.arrange(DOWN, buff=0.16).next_to(title, DOWN, buff=0.4)
        self.P(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15), rt=1.4)
        self.W(self.cue(1))
        kw = VGroup(*[chip(s, color=GREEN, size=28) for s in ["技能 Skills", "插件 Plugins", "MCP"]]).arrange(RIGHT, buff=0.3)
        kw.next_to(rows, DOWN, buff=0.4)
        self.P(LaggedStart(*[FadeIn(k, scale=0.8) for k in kw], lag_ratio=0.25), rt=1.2)
        self.W(self.cue(2))
        bye = T("下周见", 32, FG).next_to(kw, DOWN, buff=0.3)
        self.P(FadeIn(bye), rt=0.5)
        self.finish()

# ───────────────────────────── #5 android/skills
SK5 = ["AGP 9 升级", "CameraX 相机", "边到边显示", "XML 迁移到 Compose", "R8 配置分析"]
# ───────────────────────────── #4 ruflo
class P4b(Base):
    key = "P4b"
    def construct(self):
        hd = self.header("ruflo", "设计思路")
        self.P(FadeIn(hd), rt=0.4)
        X = -3.4
        layers = [("编排层", "决定交给谁、怎么做", BLUE),
                  ("蜂群协调", "“女王”智能体分派任务", PURPLE),
                  ("专职智能体", "编码 · 测试 · 审查 · 架构 …", ORANGE),
                  ("记忆与学习", "存下成功经验，先回忆再执行", GREEN),
                  ("模型", "可换用不同厂商（含本地模型）", MUTED)]
        user = VGroup(box(6.3, 0.55, color=BORDER, r=0.1), T("用户请求（Claude Code / 命令行）", 22, FG))
        user[1].move_to(user[0])
        L = VGroup()
        for i, (a, b, col) in enumerate(layers):
            bb = box(6.3, 0.86, color=col, fill="#0F141B", r=0.1)
            ta = T(a, 24, col, weight=BOLD).move_to(bb.get_left() + RIGHT * 0.25, aligned_edge=LEFT)
            tb = fit(T(b, 20, FG), 3.9).move_to(bb.get_right() + LEFT * 0.25, aligned_edge=RIGHT)
            L.add(VGroup(bb, ta, tb))
        stack = VGroup(user, *L).arrange(DOWN, buff=0.14).move_to([X, 0.0, 0])
        cap = T("据 ruvnet/ruflo README 架构图重绘（简化）", 15, MUTED).next_to(stack, DOWN, buff=0.1).align_to(stack, LEFT)
        harness = SurroundingRectangle(VGroup(*L[:4]), color=BLUE, buff=0.1, stroke_width=2, corner_radius=0.12)
        hl = T("外壳 Harness", 22, BLUE, weight=BOLD).next_to(harness, RIGHT, buff=0.15).align_to(harness, UP).shift(DOWN * 0.05)
        self.add(user, cap)
        # 右侧：形象说明
        dc = np.array([3.7, 0.3, 0])
        def detail(title, lines, col):
            return card_rows(title, [(l, None) for l in lines], 6.0, col, 24).move_to(dc)
        D = [detail("编排层", ["接收请求，拆解任务", "选择合适的智能体", "在关键节点插入检查"], BLUE),
             detail("蜂群协调", ["“女王”负责分派与汇总", "多个专职智能体并行工作", "按任务选择协作方式"], PURPLE),
             detail("记忆与学习", ["记录做得好的过程", "遇到类似任务先回忆", "再决定怎么执行"], GREEN),
             detail("模型", ["Claude、GPT、Gemini", "也可接本地模型", "上层流程保持不变"], MUTED)]
        cur = None
        plan = [(0, [0], 0), (1, [1, 2], 1), (2, [3], 2), (3, [4], 3)]
        for ci, idx, di in plan:
            self.W(self.cue(ci))
            an = [FadeIn(L[k], shift=DOWN * 0.15) for k in idx]
            if cur is not None: an.append(FadeOut(cur))
            cur = D[di]
            self.P(*an, FadeIn(cur, shift=LEFT * 0.2), rt=0.7)
        # 为什么：模型只管思考 + 官方学习循环图
        self.W(self.cue(4))
        g, c2 = picture(A + "ruflo_learning.png", width=6.6, credit="图片来源：ruvnet/ruflo README（MIT）· 图中注明：不保证一定提升", csize=15)
        g.move_to([3.65, -0.15, 0]); c2.next_to(g, DOWN, buff=0.08)
        self.P(FadeOut(cur), Create(harness), FadeIn(hl), FadeIn(g, shift=LEFT * 0.2), FadeIn(c2), rt=0.9)
        self.finish()

class P4c(Base):
    key = "P4c"
    def construct(self):
        hd = self.header("ruflo", "应用", GREEN)
        self.P(FadeIn(hd), rt=0.4)
        im = ImageMobject(A + "ruflo_console_first.png").scale_to_fit_height(5.15).move_to([-2.2, 0.2, 0])
        fr = SurroundingRectangle(im, buff=0.02, color=BORDER, stroke_width=2)
        steps = step_list([("设定任务", "“add a dark mode toggle”"), ("打开控制台页面", "Learning / Secure / Overview"),
                           ("停止蜂群被拒绝", "删除操作需要更高权限"), ("开发者收回控制", "之后的请求同样被拒绝")], 4.4, size=23)
        steps.move_to([4.65, 0.55, 0])
        note = fit(T("README 注明：创建任务 ≠ 功能已实现", 18, YELLOW), 4.3).next_to(steps, DOWN, buff=0.35).align_to(steps, LEFT)
        SS, SE = 4.0, 30.0
        t0 = 0.4 + 0.6; dur = self.cue(2) - t0 - 0.6
        sp = (SE - SS) / dur
        cap = T(f"录屏来源：ruvnet/ruflo docs/assets（MIT）· 节选，约 {sp:.1f}× 速度", 16, MUTED).next_to(fr, DOWN, buff=0.08).align_to(fr, LEFT)
        self.P(FadeIn(im), Create(fr), FadeIn(cap), rt=0.6)
        self.overlay("assets/ruflo_console.gif", im, t0, dur, ss=SS, speed=sp)
        marks = [(0, t0 + 0.3), (1, t0 + (14.5 - SS) / sp), (2, t0 + (25.0 - SS) / sp)]
        for k, tt in marks:
            self.W(max(tt, self.t))
            self.P(FadeIn(steps[k], shift=LEFT * 0.2), rt=0.5)
        self.W(t0 + dur)
        last = ImageMobject(A + "ruflo_console_last.png").scale_to_fit_height(5.15).move_to(im)
        self.remove(im); self.add(last); self.bring_to_front(fr)
        self.P(FadeIn(steps[3], shift=LEFT * 0.2), FadeIn(note), rt=0.5)
        # 场景二：联邦
        self.W(self.cue(2))
        self.P(*[FadeOut(m) for m in [last, fr, steps, note, cap]], rt=0.5)
        chips = VGroup(*[chip(s, color=BLUE, size=22) for s in ["加密互信", "个人信息先剥离", "全程审计"]]).arrange(RIGHT, buff=0.25)
        chips.move_to([0, 2.7, 0])
        g, c2 = picture(A + "ruflo_federation.png", width=9.4, credit="图片来源：ruvnet/ruflo README（MIT）· 示例：两个团队共享风控信号", csize=16)
        g.move_to([0, 0.4, 0]); c2.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g, shift=UP * 0.2), FadeIn(c2), rt=0.7)
        self.P(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in chips], lag_ratio=0.2), rt=0.8)
        self.W(self.sub_start("权限和审计"))
        self.P(LaggedStart(*[Indicate(c, color=BLUE, scale_factor=1.06) for c in chips], lag_ratio=0.2), rt=1.0)
        self.finish()

# ───────────────────────────── #3 K-Dense-AI/scientific-agent-skills
# ───────────────────────────── #2 anthropics/claude-plugins-official
# ───────────────────────────── #1 morluto/rea
class P1b(Base):
    key = "P1b"
    def construct(self):
        hd = self.header("rea", "设计思路")
        self.P(FadeIn(hd), rt=0.4)
        g, cap = picture(A + "rea_flow.png", width=11.4, credit="图片来源：morluto/rea · REA investigation flow（MIT）", csize=16)
        g.move_to([0, 0.1, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g, scale=0.96), FadeIn(cap), rt=0.8)
        self.P(g.animate.scale(1.04), rt=self.cue(1) - self.t - 0.6, rate_func=linear)
        self.W(self.cue(1) - 0.5)
        self.P(FadeOut(g), FadeOut(cap), rt=0.5)
        X = -1.9
        def layer(title, items, col, y, h=1.25, isz=22):
            b = box(9.4, h, color=col, fill="#0F141B", r=0.1).move_to([X, y, 0])
            t = T(title, 26, col, weight=BOLD).move_to(b.get_left() + RIGHT * 0.25, aligned_edge=LEFT)
            cs = VGroup(*[chip(s, color=BORDER, size=isz) for s in items]).arrange(RIGHT, buff=0.14)
            fit(cs, 6.8).move_to(b.get_left() + RIGHT * 2.3, aligned_edge=LEFT)
            return VGroup(b, t, cs)
        L1 = layer("统一入口", ["命令行", "MCP（给智能体）", "同一套流程"], BLUE, 1.75)
        L2 = layer("调查流程", ["结论", "+ 证据", "查不清 → 标成未知"], PURPLE, 0.25)
        L3 = layer("适配器", ["Ghidra", "Hopper", "IDA", "JADX", "浏览器", ".NET", "固件工具"], ORANGE, -1.25)
        cap2 = T("据 morluto/rea 架构文档重绘（简化）", 15, MUTED).next_to(L3, DOWN, buff=0.08).align_to(L3, LEFT)
        agent = node("AI 智能体", 2.3, 1.0, BLUE, 26, "Claude Code / Codex …", 15).move_to([5.3, 1.75, 0])
        me = Arrow(agent.get_left(), L1[0].get_right(), buff=0.06, color=BLUE, stroke_width=4)
        ml = M("MCP", 18, BLUE).next_to(me, UP, buff=0.05)
        self.P(FadeIn(L1, shift=DOWN * 0.15), FadeIn(agent), GrowArrow(me), FadeIn(ml), FadeIn(cap2), rt=0.8)
        self.W(self.cue(2))
        ev = CurvedArrow(L2[0].get_right() + UP * 0.1, agent.get_bottom(), angle=PI / 3, color=GREEN, stroke_width=3)
        evl = T("证据 + 未知项", 20, GREEN).next_to(ev, RIGHT, buff=0.05).shift(DOWN * 0.3)
        self.P(FadeIn(L2, shift=DOWN * 0.15), rt=0.6)
        self.P(Create(ev), FadeIn(evl), rt=0.7)
        self.W(self.cue(3))
        self.P(FadeIn(L3, shift=DOWN * 0.15), rt=0.6)
        self.P(LaggedStart(*[Indicate(c, color=ORANGE, scale_factor=1.08) for c in L3[2]], lag_ratio=0.12), rt=1.4)
        self.W(self.cue(3) + 5.5)
        why = VGroup(chip("换工具，上层流程不用改", color=YELLOW, size=22), chip("分析在本地运行", color=GREEN, size=22),
                     chip("⚠ 不是沙箱", color=RED, size=22)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        why.move_to([5.2, -0.9, 0])
        self.P(LaggedStart(*[FadeIn(c, scale=0.85) for c in why], lag_ratio=0.3), rt=1.0)
        self.finish()

class P1c(Base):
    key = "P1c"
    def construct(self):
        hd = self.header("rea", "应用", GREEN)
        self.P(FadeIn(hd), rt=0.4)
        ttl = T("官网案例：Notion 桌面版如何复制文本与 HTML", 30, FG).move_to([0, 2.5, 0])
        st = [("01 页面接口", "页面调用“复制”"), ("02 预加载层", "转成跨进程调用"),
              ("03 主进程", "校验发送方"), ("04 系统剪贴板", "写入文本与 HTML")]
        ns = VGroup(*[node(a, 3.1, 1.25, BLUE, 26, b, 18) for a, b in st]).arrange(RIGHT, buff=0.42).move_to([0, 0.95, 0])
        ar = VGroup(*[Arrow(ns[i].get_right(), ns[i + 1].get_left(), buff=0.04, color=MUTED, stroke_width=3) for i in range(3)])
        self.P(FadeIn(ttl), rt=0.5)
        self.P(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.15) for n in ns], lag_ratio=0.2), *[GrowArrow(a) for a in ar], rt=1.4)
        self.W(self.cue(0) + 2.6)
        f1 = VGroup(T("① REA 定位", 22, GREEN, weight=BOLD), T("页面暴露的复制接口 + 跨进程调用", 22, FG)).arrange(RIGHT, buff=0.25)
        f1.next_to(ns, DOWN, buff=0.55).align_to(ns, LEFT)
        self.P(*[ns[k][0].animate.set_stroke(GREEN, 3) for k in (0, 1)], FadeIn(f1, shift=UP * 0.1), rt=0.7)
        self.W(self.cue(1))
        br = BraceBetweenPoints(ns[1].get_corner(UL) + UP * 0.05, ns[2].get_corner(UR) + UP * 0.05, direction=UP, color=YELLOW)
        chan = VGroup(T("同一个通道名", 18, MUTED), M("notion:clipboard:write", 20, YELLOW)).arrange(RIGHT, buff=0.2).next_to(br, UP, buff=0.06)
        f2 = VGroup(T("② 智能体顺藤摸瓜", 22, YELLOW, weight=BOLD), T("在主进程找到写入剪贴板的代码", 22, FG)).arrange(RIGHT, buff=0.25)
        f2.next_to(f1, DOWN, buff=0.3).align_to(f1, LEFT)
        self.P(FadeOut(ttl), GrowFromCenter(br), FadeIn(chan), *[ns[k][0].animate.set_stroke(YELLOW, 3) for k in (2, 3)], FadeIn(f2, shift=UP * 0.1), rt=0.8)
        src = T("案例来源：rea.tools/showcase/notion（简化示意）", 17, MUTED).next_to(f2, DOWN, buff=0.35).align_to(f1, LEFT)
        self.P(FadeIn(src), rt=0.4)
        # Hopper 截图
        self.W(self.cue(2))
        self.P(FadeOut(VGroup(ns, ar, br, chan, f1, f2, src)), rt=0.4)
        g, cap = picture(A + "rea_hopper.png", width=9.6, credit="图片来源：morluto/rea docs/assets（MIT）· 用 Hopper 分析 macOS 程序", csize=16)
        g.move_to([0, 0.15, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g, scale=0.96), FadeIn(cap), rt=0.7)
        # 社区反响
        self.W(self.cue(3))
        self.P(Group(g).animate.scale(0.6).move_to([-3.5, 0.75, 0]), cap.animate.scale(0.85).move_to([-3.5, -1.15, 0]), rt=0.7)
        hn = box(6.4, 2.9, color=ORANGE, fill="#0F141B").move_to([3.45, 0.75, 0])
        h1 = VGroup(Square(0.46, stroke_width=0).set_fill(ORANGE, 1), T("Hacker News", 26, FG, weight=BOLD)).arrange(RIGHT, buff=0.2)
        h1[0].add(T("Y", 24, WHITE, weight=BOLD).move_to(h1[0]))
        h2 = fit(T("REA Reverse – Engineer Anything（rea.tools）", 21, FG), 5.9)
        h3 = VGroup(M("814", 32, ORANGE, weight=BOLD), T("points", 19, MUTED), M("340", 32, FG, weight=BOLD), T("comments", 19, MUTED)).arrange(RIGHT, buff=0.15)
        h4 = VGroup(fit(T("HN：有人称赞反编译质量，也有人担心冲击爱好者社区", 17, MUTED), 5.9),
                    fit(T("InfoQ 援引 Reddit：独立开发者担心作品被复制", 17, MUTED), 5.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        hh = VGroup(h1, h2, h3, h4).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(hn)
        hcap = fit(T("来源：news.ycombinator.com/item?id=50028275（2026-10-23 数据）· InfoQ 2026-10-17", 15, MUTED), 6.4).next_to(hn, DOWN, buff=0.08)
        self.P(FadeIn(hn), FadeIn(hh, shift=UP * 0.1), FadeIn(hcap), rt=0.8)
        self.W(self.cue(4))
        tk = chip("官方安全说明：不是沙箱 · 仅限自有或已获授权的软件", color=RED, size=22).move_to([0, -2.35, 0])
        self.P(FadeIn(tk, shift=UP * 0.2), rt=0.6)
        self.finish()

# ───────────────────────────── v4 新场景
TEAL, SKY = "#39C5CF", "#79C0FF"
class S0_Intro(Base):
    key = "S0_Intro"
    def construct(self):
        grid = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                           background_line_style={"stroke_color": "#1B2230", "stroke_width": 1}, axis_config={"stroke_opacity": 0})
        self.add(grid)
        star = gh_star(0.42).move_to(UP * 2.3)
        title = VGroup(T("GitHub 本周热门", 76, FG, weight=BOLD), T("Top 5", 76, YELLOW, weight=BOLD)).arrange(RIGHT, buff=0.35)
        title.next_to(star, DOWN, buff=0.35)
        date = chip("2026 年 10 月第四周", color=YELLOW, size=26).next_to(title, DOWN, buff=0.35)
        self.P(GrowFromCenter(star), FadeIn(title, shift=UP * 0.3), rt=0.9)
        self.P(Rotate(star, angle=TAU / 5), FadeIn(date, shift=UP * 0.15), rt=0.6)
        avs = Group(*[Group(avatar(p, 0.85), M(REPO[p].split("/")[0], 17, MUTED)).arrange(DOWN, buff=0.1)
                      for p in ["science", "android", "ruflo", "plugins", "rea"]]).arrange(RIGHT, buff=0.75)
        avs.next_to(date, DOWN, buff=0.6)
        self.P(LaggedStart(*[FadeIn(a, shift=UP * 0.2) for a in avs], lag_ratio=0.2), rt=1.4)
        self.finish()

class P5a(IntroScene):
    key = "P5a"; pid = "android"
    def right(self):
        c = np.array([3.6, 0.25, 0])
        pan = box(6.4, 5.0, fill="#0F141B").move_to(c)
        big = VGroup(M("33", 120, YELLOW, weight=BOLD), T("个官方技能", 34, FG)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        big.move_to(c + UP * 1.2)
        rel = T("v1.0.16（10 月 21 日）新增：", 24, MUTED)
        new = VGroup(*[chip(s, color=GREEN, size=22, font=MONO) for s in ["litert-lm", "anr-audit-and-fix", "projected-hardware"]]).arrange(DOWN, buff=0.14)
        g2 = VGroup(rel, new).arrange(DOWN, buff=0.22).move_to(c + DOWN * 0.95)
        self.P(FadeIn(pan), FadeIn(big, shift=UP * 0.2), rt=0.7)
        self.P(FadeIn(rel), LaggedStart(*[FadeIn(x, shift=LEFT * 0.2) for x in new], lag_ratio=0.25), rt=1.2)

CATS5 = [("界面与 Compose", 7, "XML→Compose 迁移 · 自适应布局 · Navigation 3", BLUE),
         ("多设备适配", 6, "车机 · 电视 · Wear OS · XR 眼镜", PURPLE),
         ("端侧 AI", 4, "LiteRT · ML Kit · AppFunctions", GREEN),
         ("性能与稳定性", 4, "ANR · R8 · Profiler", ORANGE),
         ("安全与身份", 4, "Intent / 权限安全 · 凭据恢复", RED),
         ("Google Play", 3, "结算库升级 · 政策审计", YELLOW),
         ("构建与测试", 3, "AGP 9 · CLI · 测试搭建", SKY),
         ("媒体与相机", 2, "CameraX · Media3 投射", TEAL)]
def tile(name, n, ex, col, w, h):
    b = box(w, h, color=col, fill="#0F141B", r=0.1)
    num = M(str(n), 44, col, weight=BOLD).move_to(b.get_corner(UL) + np.array([0.22, -0.42, 0]), aligned_edge=LEFT)
    nm = fit(T(name, 24, FG, weight=BOLD), w - 1.1).next_to(num, RIGHT, buff=0.2)
    e = fit(T(ex, 18, MUTED), w - 0.4).move_to(b.get_corner(DL) + np.array([0.22, 0.32, 0]), aligned_edge=LEFT)
    return VGroup(b, num, nm, e)

class P5b(Base):
    key = "P5b"
    def construct(self):
        hd = self.header("android", "功能分布")
        self.add(hd)
        W, gap = 13.6, 0.12
        rows = [CATS5[:4], CATS5[4:]]
        tiles = VGroup()
        for r, (row, y) in enumerate(zip(rows, [1.95, 0.42])):
            tot = sum(c[1] + 4 for c in row); avail = W - gap * (len(row) - 1)
            x = -W / 2
            for name, n, ex, col in row:
                w = avail * (n + 4) / tot
                t = tile(name, n, ex, col, w, 1.4).move_to([x + w / 2, y, 0]); tiles.add(t); x += w + gap
        cap = T("按 33 个技能的名称与描述归类（本片整理）", 15, MUTED).move_to([-6.8, -0.45, 0], aligned_edge=LEFT)
        # 旁白依次点到各大类，色块随之逐个出现
        self.P(LaggedStart(*[FadeIn(t, scale=0.95) for t in tiles], lag_ratio=0.5), FadeIn(cap), rt=5.6)
        self.W(self.sub_start("其中界面"))
        self.P(Indicate(tiles[0], color=WHITE, scale_factor=1.03), rt=1.0)
        # 四个层面
        self.W(self.cue(1))
        lv = [("迁移与升级", "AGP 9 · XML→Compose · 结算库", BLUE), ("审计与诊断", "ANR · R8 · 权限安全 · Play 政策", ORANGE),
              ("接入新能力", "端侧 AI · CameraX · 凭据", GREEN), ("测试与验证", "测试策略 · 小组件验证", PURPLE)]
        cards = VGroup()
        for a, b, col in lv:
            bb = box(3.3, 1.05, color=col, fill="#0F141B", r=0.1)
            g = VGroup(T(a, 24, col, weight=BOLD), fit(T(b, 16, FG), 3.0)).arrange(DOWN, buff=0.1).move_to(bb)
            cards.add(VGroup(bb, g))
        cards.arrange(RIGHT, buff=0.13).move_to([0, -1.25, 0])
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.25), rt=1.4)
        q = chip("官方：选题集中在评测中大模型表现欠佳的场景", color=YELLOW, size=24).move_to([0, -2.35, 0])
        self.W(self.cue(2))
        self.P(FadeIn(q, shift=UP * 0.15), rt=0.6)
        self.finish()

class P5c(Base):
    key = "P5c"
    def construct(self):
        hd = self.header("android", "应用", GREEN)
        self.add(hd)
        im = ImageMobject(A + "android_gemini_skills_demo_first.png").scale_to_fit_height(4.85)
        im.move_to([-2.25, 0.62, 0])
        fr = SurroundingRectangle(im, buff=0.02, color=BORDER, stroke_width=2)
        steps = step_list([("提出需求", "把 XML 布局迁移到 Compose"), ("激活迁移技能", "智能体先申请，再使用"),
                           ("读取迁移指南", "技能附带的参考资料"), ("检查并改写", "检查项目、改写界面")], 3.9, size=23)
        steps.move_to([4.85, 0.75, 0])
        t0 = 0.5; dur = self.tm["total"] - t0 - 0.8
        sp = 21.75 / dur
        cap = fit(T(f"演示来源：developer.android.com · Android 官方文档（CC BY 2.5）· {sp:.1f}× 速度", 16, MUTED), 8.0)
        cap.next_to(fr, DOWN, buff=0.08).align_to(fr, LEFT)
        self.P(FadeIn(im), Create(fr), FadeIn(cap), rt=0.5)
        self.overlay("assets/android_gemini_skills_demo.gif", im, t0, dur, ss=0.0, speed=sp)
        marks = [self.cue(0) + 0.6, t0 + dur * 0.38, t0 + dur * 0.55, t0 + dur * 0.75]   # 与 GIF 进度大致对应
        for k, tt in enumerate(marks):
            self.W(max(tt, self.t))
            self.P(FadeIn(steps[k], shift=LEFT * 0.2), rt=0.5)
        self.W(self.cue(2))
        tk = fit(chip("迁移规则来自官方指南", color=GREEN, size=22), 4.4).next_to(steps, DOWN, buff=0.45).align_to(steps, LEFT)
        self.P(FadeIn(tk, shift=UP * 0.15), rt=0.6)
        self.finish()

KD = [("生物信息与基因组", 32), ("科研写作与交流", 23), ("数据分析与可视化", 18), ("机器学习与 AI", 14),
      ("数据库与数据访问", 13), ("研究方法与规划", 13), ("基础设施与平台", 12), ("化学信息学与药物发现", 11),
      ("工程与仿真", 9), ("临床研究", 8), ("材料 / 化学 / 物理", 8)]
class P3b(Base):
    key = "P3b"
    def construct(self):
        hd = self.header("science", "功能分布")
        self.add(hd)
        rows = VGroup()
        for i, (n, v) in enumerate(KD):
            lab = T(n, 20, FG)
            bar = Rectangle(width=v / 32 * 3.4, height=0.3, stroke_width=0).set_fill(GREEN if i == 0 else BLUE, 0.9)
            num = M(str(v), 19, MUTED)
            rows.add(VGroup(lab, bar, num))
        for i, r in enumerate(rows):
            y = 2.75 - i * 0.43
            r[0].move_to([-3.6, y, 0], aligned_edge=RIGHT); r[1].move_to([-3.45, y, 0], aligned_edge=LEFT); r[2].next_to(r[1], RIGHT, buff=0.12)
        rest = T("其余 9 类：实验自动化、显微与医学影像、多组学、蛋白设计、神经科学等", 16, MUTED).move_to([-6.8, 2.75 - 11 * 0.43, 0], aligned_edge=LEFT)
        note = T("README 分类，类别有重叠，各类之和大于 177", 15, MUTED).next_to(rest, DOWN, buff=0.12).align_to(rest, LEFT)
        self.P(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows], lag_ratio=0.3), rt=6.0)
        self.P(FadeIn(rest), FadeIn(note), rt=0.6)
        self.W(self.sub_start("其中生物"))
        self.P(Indicate(VGroup(rows[0][0], rows[0][1]), color=WHITE, scale_factor=1.04), rt=1.0)
        # 五个层面
        self.W(self.cue(1))
        lv = [("查数据库", "100+ 个数据库 · 13 个技能", YELLOW), ("调计算包", "70+ 个 Python 科学计算包", BLUE),
              ("对接实验平台", "9 个：Benchling 等", PURPLE), ("文献与写作", "30+ 个分析与交流工具", GREEN),
              ("研究与临床", "10+ 个：假设生成等", ORANGE)]
        cards = VGroup()
        for a, b, col in lv:
            bb = box(6.0, 0.86, color=col, fill="#0F141B", r=0.1)
            ta = T(a, 24, col, weight=BOLD).move_to(bb.get_left() + RIGHT * 0.25, aligned_edge=LEFT)
            tb = fit(T(b, 19, FG), 3.0).move_to(bb.get_right() + LEFT * 0.25, aligned_edge=RIGHT)
            cards.add(VGroup(bb, ta, tb))
        cards.arrange(DOWN, buff=0.14).move_to([3.8, 0.35, 0])
        cc = T("数量摘自 README “What's Included”", 15, MUTED).next_to(cards, DOWN, buff=0.1).align_to(cards, LEFT)
        self.P(LaggedStart(*[FadeIn(c, shift=LEFT * 0.15) for c in cards], lag_ratio=0.2), FadeIn(cc), rt=1.8)
        self.finish()

class P2a(IntroScene):
    key = "P2a"; pid = "plugins"
    def right(self):
        c = np.array([3.6, 0.75, 0])
        tot, a = 315, 40
        ang = a / tot * TAU
        s1 = AnnularSector(inner_radius=1.05, outer_radius=1.75, angle=ang, start_angle=PI / 2, color=BLUE, fill_opacity=1, stroke_width=0).shift(c)
        s2 = AnnularSector(inner_radius=1.05, outer_radius=1.75, angle=TAU - ang, start_angle=PI / 2 + ang, color=GREEN, fill_opacity=0.85, stroke_width=0).shift(c)
        mid = VGroup(M("315", 46, FG, weight=BOLD), T("个插件", 20, MUTED)).arrange(DOWN, buff=0.05).move_to(c)
        lg = VGroup(VGroup(Square(0.26, stroke_width=0).set_fill(BLUE, 1), T("Anthropic 维护  40", 24, FG)).arrange(RIGHT, buff=0.18),
                    VGroup(Square(0.26, stroke_width=0).set_fill(GREEN, 1), T("合作方与社区  275", 24, FG)).arrange(RIGHT, buff=0.18)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        lg.arrange(RIGHT, buff=0.45).move_to([3.1, c[1] - 2.35, 0])
        self.P(Create(s1), FadeIn(mid), rt=0.6)
        self.P(Create(s2), FadeIn(lg), rt=1.0)

CATS2 = [("开发", 123), ("效率工具", 69), ("数据库", 39), ("监控", 22), ("安全", 18), ("未分类", 14), ("部署", 9), ("设计", 8), ("其他 6 类", 13)]
class P2b(Base):
    key = "P2b"
    def construct(self):
        hd = self.header("plugins", "功能分布")
        self.add(hd)
        ttl = T("315 个插件，按目录分类", 24, MUTED).move_to([-3.4, 2.75, 0])
        rows = VGroup()
        for i, (n, v) in enumerate(CATS2):
            lab = T(n, 22, FG if i < 8 else MUTED)
            bar = Rectangle(width=v / 123 * 4.3, height=0.34, stroke_width=0).set_fill(YELLOW if i == 0 else BLUE, 0.9 if i < 8 else 0.4)
            num = M(str(v), 20, MUTED)
            rows.add(VGroup(lab, bar, num))
        for i, r in enumerate(rows):
            y = 2.2 - i * 0.5
            r[0].move_to([-5.0, y, 0], aligned_edge=RIGHT); r[1].move_to([-4.85, y, 0], aligned_edge=LEFT); r[2].next_to(r[1], RIGHT, buff=0.12)
        cap = T("数据：claude-plugins-official 插件目录（2026-10-23 拉取）· 其他 6 类含学习、自动化、测试等", 15, MUTED).move_to([-6.8, -2.35, 0], aligned_edge=LEFT)
        self.P(FadeIn(ttl), LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows], lag_ratio=0.25), FadeIn(cap), rt=3.6)
        self.P(Indicate(VGroup(rows[0][0], rows[0][1]), color=WHITE, scale_factor=1.04), rt=1.0)
        # 外部服务接入
        self.W(self.cue(1))
        pb = box(5.6, 4.6, color=GREEN, fill="#0F141B").move_to([3.85, 0.3, 0])
        pt = T("外部服务的官方接入（举例）", 22, GREEN, weight=BOLD).move_to(pb.get_top() + DOWN * 0.4)
        names = ["aws-core", "azure", "atlassian", "github", "gitlab", "linear", "stripe", "supabase", "vercel",
                 "datadog", "sentry", "figma", "notion", "slack", "mongodb"]
        cs = VGroup(*[chip(n, color=BORDER, size=19, font=MONO) for n in names]).arrange_in_grid(5, 3, buff=(0.14, 0.16))
        fit(cs, 5.2).next_to(pt, DOWN, buff=0.3)
        self.P(FadeIn(pb), FadeIn(pt), rt=0.4)
        self.P(LaggedStart(*[FadeIn(x, scale=0.85) for x in cs], lag_ratio=0.06), rt=1.6)
        self.finish()

class P2c(Base):
    key = "P2c"
    def construct(self):
        hd = self.header("plugins", "插件举例", GREEN)
        self.add(hd)
        src = T("流程摘自各插件 README（Apache-2.0）", 15, MUTED).move_to([6.8, 3.5, 0], aligned_edge=RIGHT)
        def card(title, sub, steps, col, x):
            b = box(4.35, 4.5, color=col, fill="#0F141B").move_to([x, 0.55, 0])
            t = M(title, 24, col, weight=BOLD).move_to(b.get_top() + DOWN * 0.38)
            st = T(sub, 17, MUTED).next_to(t, DOWN, buff=0.08)
            items = VGroup()
            for k, s_ in enumerate(steps):
                items.add(VGroup(T(f"{k + 1}", 16, col, weight=BOLD), fit(T(s_, 22, FG), 3.5)).arrange(RIGHT, buff=0.15))
            items.arrange(DOWN, aligned_edge=LEFT, buff=0.17 if len(steps) > 5 else (0.3 if len(steps) > 3 else 0.5)).next_to(st, DOWN, buff=0.28).align_to(b.get_left() + RIGHT * 0.3, LEFT)
            return VGroup(b, t, st, items)
        c1 = card("code-review", "自动审查 PR", ["4 个审查智能体并行", "两个查 CLAUDE.md 规范", "一个找缺陷，一个看 git 历史", "每个问题打 0–100 置信分", "≥80 分才写进 PR 评论"], PURPLE, -4.55)
        c2 = card("feature-dev", "七步开发新功能", ["弄清需求", "探索现有代码", "追问细节", "设计架构", "实现", "质量审查", "总结"], BLUE, 0.0)
        c3 = card("security-guidance", "三层安全把关", ["编辑时：提醒危险写法", "每轮结束：模型审查改动", "提交时：跨文件安全审查"], RED, 4.55)
        cs = [c1, c2, c3]
        self.add(src)
        for k, c in enumerate(cs):
            self.W(self.cue(k))
            others = [cs[j][0].animate.set_stroke(BORDER) for j in range(k) ]
            self.P(FadeIn(c[0]), FadeIn(c[1]), FadeIn(c[2]), *others, rt=0.5)
            self.P(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.1) for i in c[3]], lag_ratio=0.18), rt=min(2.0, 0.35 * len(c[3])))
        self.W(self.cue(3))
        tk = chip("⚠ 官方提醒：插件内容不受 Anthropic 控制，安装前先确认可信", color=YELLOW, size=22).move_to([0, -2.3, 0])
        self.P(FadeIn(tk, shift=UP * 0.2), rt=0.6)
        self.finish()
