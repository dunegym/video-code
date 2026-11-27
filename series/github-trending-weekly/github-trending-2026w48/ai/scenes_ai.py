"""GitHub Agent/AI 周热榜 Top 5（2026 第 48 周）—— Manim CE 场景。
时间轴由 timing_ai.json（MiniMax 语音对齐时间戳）驱动。"""
import json, os, pathlib
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
TM = json.load(open("timing_ai.json", encoding="utf-8"))
DATA = json.load(open("data.json", encoding="utf-8"))
A = "assets/proc/"
FONT = "Microsoft YaHei" if os.name == "nt" else "Noto Sans CJK SC"
MONO = "Consolas" if os.name == "nt" else "Noto Sans Mono CJK SC"
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
    fit(g, w - 0.22)
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
    im = ImageMobject(path)
    if width: im.scale_to_fit_width(width)
    if height and im.height > height: im.scale_to_fit_height(height)
    fr = SurroundingRectangle(im, buff=0.02, color=BORDER, stroke_width=2)
    g = Group(im, fr)
    cap = T(credit, csize, MUTED).next_to(g, DOWN, buff=0.1) if credit else None
    return g, cap
def bullets(items, w, size=21, col=GREEN, buff=0.22):
    return VGroup(*[VGroup(Dot(radius=0.06, color=col), fit(T(s, size, FG), w - 0.3)).arrange(RIGHT, buff=0.15)
                    for s in items]).arrange(DOWN, aligned_edge=LEFT, buff=buff)
def arrow(a, b, col=MUTED, sw=3, buff=0.1):
    return Arrow(a, b, buff=buff, color=col, stroke_width=sw, max_tip_length_to_length_ratio=0.18)
def credit(s, size=15, w=12.5): return fit(T(s, size, MUTED), w)
def card_rows(title, rows, w, col=BLUE, size=22):
    t = T(title, 24, col, weight=BOLD)
    rs = VGroup(*[VGroup(Dot(radius=0.06, color=c or col), fit(T(r, size, FG), w - 0.85)).arrange(RIGHT, buff=0.16) for r, c in rows])
    rs.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    inner = VGroup(t, rs).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    b = box(w, inner.height + 0.65, color=col, fill="#0F141B")
    inner.move_to(b).align_to(b.get_left() + RIGHT * 0.32, LEFT)
    return VGroup(b, t, rs)

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
        pathlib.Path("build/scenes").mkdir(parents=True, exist_ok=True)
        json.dump(self.ov, open(f"build/scenes/ov_{self.key}.json", "w", encoding="utf-8"), indent=1)
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

# ───────────────────────────── 片头
class S0_Intro(Base):
    key = "S0_Intro"
    def construct(self):
        grid = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                           background_line_style={"stroke_color": "#1B2230", "stroke_width": 1}, axis_config={"stroke_opacity": 0})
        self.add(grid)
        star = gh_star(0.42).move_to(UP * 2.35)
        title = VGroup(T("GitHub Agent/AI 周热榜", 60, FG, weight=BOLD), T("Top 5", 60, YELLOW, weight=BOLD)).arrange(RIGHT, buff=0.3)
        fit(title, 13.2).next_to(star, DOWN, buff=0.28)
        date = chip("2026 · 第 48 周 · 11 月 27 日", color=YELLOW, size=26).next_to(title, DOWN, buff=0.28)
        self.P(GrowFromCenter(star), FadeIn(title, shift=UP * 0.3), rt=0.9)
        self.P(Rotate(star, angle=TAU / 5), FadeIn(date, shift=UP * 0.15), rt=0.6)
        order = ["ocr", "nod", "mw", "st", "pn"]
        short = {"ocr": "open-code-review", "nod": "n8n-io/nod", "mw": "web-guidance", "st": "stitch-skills", "pn": "plannotator"}
        avs = Group(*[Group(avatar(p, 0.8), M(short[p], 16, MUTED)).arrange(DOWN, buff=0.08) for p in order]).arrange(RIGHT, buff=0.42)
        avs.next_to(date, DOWN, buff=0.4)
        self.P(LaggedStart(*[FadeIn(a, shift=UP * 0.2) for a in avs], lag_ratio=0.18), rt=1.3)
        self.W(self.cue(1))
        tags = VGroup(
            chip("代码审查", color=RED, size=22), chip("个人智能体", color=ORANGE, size=22),
            chip("网页指南", color=BLUE, size=22), chip("设计技能", color=PURPLE, size=22),
            chip("评审工作台", color=GREEN, size=22),
        ).arrange(RIGHT, buff=0.16).next_to(avs, DOWN, buff=0.35)
        fit(tags, 13.2)
        self.P(LaggedStart(*[FadeIn(c, scale=0.85) for c in tags], lag_ratio=0.15), rt=1.6)
        self.finish()

# ───────────────────────────── #5 open-code-review
class P5a(IntroScene):
    key = "P5a"; pid = "ocr"
    def right(self):
        c = np.array([3.7, 0.3, 0])
        g, cap = picture("assets/proc/ocr-home.png", width=6.15, height=4.4, credit="图：官网 open-codereview.ai", csize=14)
        g.move_to(c + UP * 0.15); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)

class P5b(Base):
    key = "P5b"
    def construct(self):
        hd = self.header("ocr", "确定性工程 × 审查代理", RED)
        self.add(hd)
        left = card_rows("确定性工程", [
            ("选哪些文件，先由程序圈定", BLUE),
            ("相关文件捆成一组再审查", BLUE),
            ("按文件特征匹配规则", BLUE),
            ("评论定位和反省独立校验", BLUE),
        ], 6.0, BLUE, 20)
        right = card_rows("模型代理", [
            ("为审查调过的提示词", ORANGE),
            ("从生产调用记录收束的工具集", ORANGE),
            ("动态决定该查什么、怎么下结论", ORANGE),
        ], 6.0, ORANGE, 20)
        left.move_to([-3.3, 0.85, 0]); right.move_to([3.3, 0.85, 0])
        mid = T("×", 48, YELLOW, weight=BOLD).move_to([0, 0.85, 0])
        self.P(FadeIn(left, shift=RIGHT * 0.2), FadeIn(right, shift=LEFT * 0.2), FadeIn(mid), rt=1.0)
        self.W(self.cue(1))
        bund = box(12.6, 1.35, color=PURPLE, fill="#0F141B").move_to([0, -1.55, 0])
        bu = VGroup(
            T("大改动怎么分", 22, PURPLE, weight=BOLD),
            fit(T("相关文件捆成一组，交给隔离的子代理并行审查，避免一次塞进全部上下文。", 20, FG), 11.8),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        bu.move_to(bund).align_to(bund.get_left() + RIGHT * 0.35, LEFT)
        cap = credit("据 Open Code Review README「Deterministic Engineering × Agent Hybrid」", 14, 12).move_to([0, -2.5, 0])
        self.P(FadeIn(bund), FadeIn(bu), FadeIn(cap), rt=0.8)
        self.finish()

class P5c(Base):
    key = "P5c"
    def construct(self):
        hd = self.header("ocr", "评测、双模式与本周更新", GREEN)
        self.add(hd)
        g, cap = picture("assets/proc/ocr-benchmark.png", width=6.2, height=2.55, credit="图：Open Code Review 官方自报评测对比图", csize=14)
        g.move_to([-3.25, 1.35, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)
        mets = VGroup(
            chip("精确率与 F1 更高", color=GREEN, size=20),
            chip("词元约通用代理 1/9", color=YELLOW, size=20),
            chip("召回更低：故意少报误报", color=ORANGE, size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.65, 1.35, 0])
        self.P(LaggedStart(*[FadeIn(m, shift=LEFT * 0.15) for m in mets], lag_ratio=0.15), rt=1.1)
        self.W(self.cue(1))
        modes = VGroup(
            node("原生审查", 5.8, 0.95, GREEN, 22, "自带审查代理与确定性流水线", 16),
            node("委托审查", 5.8, 0.95, BLUE, 22, "只做选文件与规则，审查交给当前智能体", 16),
        ).arrange(RIGHT, buff=0.3).move_to([0, -1.25, 0])
        note_t = credit("本周 v1.14.4 支持从固定快照审查 GitHub PR，并排除 C/C++ 测试与基准路径", 15, 12.2).move_to([0, -2.2, 0])
        self.P(FadeIn(modes[0]), FadeIn(modes[1]), FadeIn(note_t), rt=0.9)
        self.finish()

# ───────────────────────────── #4 n8n-io/nod (NEW!)
class P4a(IntroScene):
    key = "P4a"; pid = "nod"
    def right(self):
        c = np.array([3.7, 0.35, 0])
        g, cap = picture("assets/proc/nod-call-brief.png", width=6.15, height=3.8, credit="图：n8n-io/nod 官方晨间会议简报演示", csize=14)
        g.move_to(c + UP * 0.35); cap.next_to(g, DOWN, buff=0.08)
        pills = VGroup(chip("Linux 沙盒", color=ORANGE, size=19), chip("独立浏览器", color=BLUE, size=19), chip("动作前审批", color=GREEN, size=19)).arrange(RIGHT, buff=0.14)
        pills.next_to(cap, DOWN, buff=0.18)
        self.P(FadeIn(g), FadeIn(cap), rt=0.7)
        self.P(LaggedStart(*[FadeIn(p, scale=0.9) for p in pills], lag_ratio=0.18), rt=0.6)

class P4b(Base):
    key = "P4b"
    def construct(self):
        hd = self.header("nod", "本地服务 × 双容器沙盒与安全边界", ORANGE)
        self.add(hd)
        u = node("你", 2.3, 1.05, PURPLE, 22, "桌面 · Telegram · WhatsApp", 14)
        srv = node("Nod 本地服务", 3.6, 1.05, ORANGE, 22, "Pi 运行时 · 策略检查 · Vault · 记忆", 14)
        c1 = node("Linux 沙盒容器", 3.2, 0.65, BLUE, 18)
        c2 = node("Chromium 浏览器", 3.2, 0.65, TEAL, 18)
        c3 = node("PostgreSQL 本地库", 3.2, 0.65, GREEN, 18)
        right_col = VGroup(c1, c2, c3).arrange(DOWN, buff=0.14)
        u.move_to([-5.2, 1.5, 0]); srv.move_to([-1.4, 1.5, 0]); right_col.move_to([3.7, 1.5, 0])
        a0 = arrow(u.get_right(), srv.get_left(), MUTED, 3, 0.08)
        a1 = arrow(srv.get_right(), c1.get_left(), BLUE, 2.5, 0.08)
        a2 = arrow(srv.get_right(), c2.get_left(), TEAL, 2.5, 0.08)
        a3 = arrow(srv.get_right(), c3.get_left(), GREEN, 2.5, 0.08)
        self.P(FadeIn(u), Create(a0), FadeIn(srv), rt=0.9)
        self.P(LaggedStart(FadeIn(c1), FadeIn(c2), FadeIn(c3), lag_ratio=0.15), Create(a1), Create(a2), Create(a3), rt=0.9)
        self.W(self.cue(1))
        sec1 = card_rows("策略在服务端，不在提示词", [
            ("网页与应用结果默认标成不可信数据", RED),
            ("超出规则的外部操作必须等你批准", RED),
        ], 6.0, RED, 19)
        sec2 = card_rows("密钥与记忆严格隔离", [
            ("模型密钥不进沙盒，Vault 私下代填密码", GREEN),
            ("记忆只从你自己的消息学，随时可改可忘", GREEN),
        ], 6.0, GREEN, 19)
        sec1.move_to([-3.25, -1.15, 0]); sec2.move_to([3.25, -1.15, 0])
        cap = credit("据 n8n-io/nod README「Under the hood」「Your rules」「Memory」", 14, 12).move_to([0, -2.5, 0])
        self.P(FadeIn(sec1, shift=UP * 0.12), rt=0.7)
        self.W(self.cue(2))
        self.P(FadeIn(sec2, shift=UP * 0.12), FadeIn(cap), rt=0.7)
        self.finish()

class P4c(Base):
    key = "P4c"
    def construct(self):
        hd = self.header("nod", "真实网页代办、v0.10.0 与评测边界", GREEN)
        self.add(hd)
        g, cap = picture("assets/proc/nod-approval.png", width=6.6, height=3.8, credit="图：Nod 草拟 Slack 回复并请求审批（官方 README）", csize=14)
        g.move_to([-3.0, 0.75, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)
        self.W(self.cue(1))
        c_v10 = card_rows("v0.10.0 今日更新", [
            ("单一常驻浏览器保留网站登录态", BLUE),
            ("对话与定时任务各自隔离上下文", BLUE),
            ("列表、日程、草稿与对比卡片化", BLUE),
        ], 5.6, BLUE, 18)
        c_eval = card_rows("官方自报评测与已知边界", [
            ("模拟环境自报 98% 完成率（非第三方）", YELLOW),
            ("小模型测试曾放行 8 次不安全动作", ORANGE),
            ("应用连接与用量默认托管，可关闭上报", ORANGE),
        ], 5.6, ORANGE, 18)
        side = VGroup(c_v10, c_eval).arrange(DOWN, buff=0.22).move_to([3.65, 0.55, 0])
        self.P(FadeIn(c_v10, shift=LEFT * 0.15), rt=0.7)
        self.W(self.cue(2))
        self.P(FadeIn(c_eval, shift=LEFT * 0.15), rt=0.7)
        self.finish()

# ───────────────────────────── #3 modern-web-guidance-src
class P3a(IntroScene):
    key = "P3a"; pid = "mw"
    def right(self):
        c = np.array([3.7, 0.3, 0])
        g, cap = picture("assets/proc/mwg-docs.png", width=6.15, height=4.4, credit="图：developer.chrome.com/docs/modern-web-guidance", csize=14)
        g.move_to(c + UP * 0.15); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)

class P3b(Base):
    key = "P3b"
    def construct(self):
        hd = self.header("mw", "本地检索与指南分类", BLUE)
        self.add(hd)
        steps = [("激活技能", "任务相关时启用"), ("本地语义检索", "离线嵌入 + BM25"), ("取回指南", "写法、坑和退路")]
        nodes = VGroup(*[node(a, 3.3, 1.15, color=c, size=24, sub=b, subsize=16)
                         for (a, b), c in zip(steps, [BLUE, TEAL, GREEN])])
        nodes.arrange(RIGHT, buff=0.45).move_to([0, 1.85, 0])
        arrs = VGroup(*[arrow(nodes[i].get_right(), nodes[i+1].get_left(), MUTED, 3, 0.08) for i in range(2)])
        off = fit(T("检索不走联网搜索接口", 18, YELLOW), 12).next_to(nodes, DOWN, buff=0.22)
        self.P(LaggedStart(*[FadeIn(n, shift=UP * 0.12) for n in nodes], lag_ratio=0.2), *[Create(a) for a in arrs], rt=1.2)
        self.P(FadeIn(off), rt=0.4)
        self.W(self.cue(1))
        cats = [("体验和布局", BLUE), ("性能", GREEN), ("表单和原生组件", PURPLE),
                ("无障碍", TEAL), ("浏览器内置本地模型", ORANGE)]
        chips = VGroup(*[chip(n, color=c, size=22) for n, c in cats]).arrange(RIGHT, buff=0.16)
        fit(chips, 13.0).move_to([0, -0.15, 0])
        prune = box(12.6, 1.15, color=YELLOW, fill="#0F141B").move_to([0, -1.55, 0])
        pr = fit(T("指南刻意写短：评测里模型已经会的内容会被剪掉，避免占掉上下文。", 22, FG), 11.8).move_to(prune)
        cap = credit("据 Modern Web Guidance README「How It Works」「What's Included」", 14, 12).move_to([0, -2.45, 0])
        self.P(LaggedStart(*[FadeIn(c, scale=0.9) for c in chips], lag_ratio=0.12), rt=0.9)
        self.P(FadeIn(prune), FadeIn(pr), FadeIn(cap), rt=0.7)
        self.finish()

class P3c(Base):
    key = "P3c"
    def construct(self):
        hd = self.header("mw", "闭环评测", GREEN)
        self.add(hd)
        g, cap = picture("assets/proc/mwg-eval.png", width=7.4, height=4.15, credit="图：官方评测看板 googlechrome.github.io/modern-web-guidance-src", csize=14)
        g.move_to([-2.55, 0.55, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)
        self.W(self.cue(1))
        side = VGroup(
            card_rows("官方评测结果", [
                ("最佳实践通过率从五成出头提到九成以上", GREEN),
                ("无障碍检查同样有明显拉升", GREEN),
            ], 5.0, GREEN, 18),
            card_rows("留存原则", [
                ("模型本来就会，指南就删掉", ORANGE),
                ("只有真正拉开差距的才留下", ORANGE),
            ], 5.0, ORANGE, 18),
        ).arrange(DOWN, buff=0.25).move_to([4.15, 0.55, 0])
        self.P(FadeIn(side[0], shift=LEFT * 0.15), rt=0.7)
        self.W(self.cue(2))
        self.P(FadeIn(side[1], shift=LEFT * 0.15), rt=0.7)
        self.finish()

# ───────────────────────────── #2 stitch-skills
class P2a(IntroScene):
    key = "P2a"; pid = "st"
    def right(self):
        c = np.array([3.7, 0.35, 0])
        g, cap = picture("assets/proc/stitch-og.png", width=6.0, credit="图：Stitch 官方 OG 图 stitch.google.com", csize=14)
        g.move_to(c + UP * 0.55); cap.next_to(g, DOWN, buff=0.1)
        pills = VGroup(chip("设计", color=PURPLE, size=20), chip("构建", color=BLUE, size=20), chip("工具", color=TEAL, size=20)).arrange(RIGHT, buff=0.16)
        pills.next_to(cap, DOWN, buff=0.2)
        self.P(FadeIn(g), FadeIn(cap), rt=0.7)
        self.P(LaggedStart(*[FadeIn(p, scale=0.9) for p in pills], lag_ratio=0.2), rt=0.6)

class P2b(Base):
    key = "P2b"
    def construct(self):
        hd = self.header("st", "三组技能", PURPLE)
        self.add(hd)
        cols = [
            ("设计", PURPLE, ["出稿、改稿", "管理设计系统", "从代码抽成设计稿"]),
            ("构建", BLUE, ["编成 React 组件", "编成 React Native", "检查设计令牌"]),
            ("工具", TEAL, ["补全提示词", "生成设计说明", "一句话铺出多页站点"]),
        ]
        cards = VGroup()
        for title, col, rows in cols:
            b = box(4.0, 3.35, color=col, fill="#0F141B")
            head = T(title, 28, col, weight=BOLD)
            body = bullets(rows, 3.5, 20, col, 0.28)
            inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
            inner.move_to(b).align_to(b.get_left() + RIGHT * 0.28, LEFT).shift(UP * 0.05)
            cards.add(VGroup(b, inner))
        cards.arrange(RIGHT, buff=0.25).move_to([0, 0.85, 0])
        self.P(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.18), rt=1.2)
        self.W(self.cue(1))
        dep = box(12.8, 1.35, color=YELLOW, fill="#0F141B").move_to([0, -1.65, 0])
        dtxt = VGroup(
            T("怎么配合", 22, YELLOW, weight=BOLD),
            fit(T("都要连上 Stitch 服务；脚本负责校验和上传，知识库放清单和样例；选装时要把有依赖的一起装上。", 20, FG), 12.0),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        dtxt.move_to(dep).align_to(dep.get_left() + RIGHT * 0.35, LEFT)
        cap = credit("据 stitch-skills README「Available Plugins」", 14, 12).move_to([0, -2.55, 0])
        self.P(FadeIn(dep), FadeIn(dtxt), FadeIn(cap), rt=0.8)
        self.finish()

class P2c(Base):
    key = "P2c"
    def construct(self):
        hd = self.header("st", "从稿到代码，再回去", BLUE)
        self.add(hd)
        a = node("文字或图片", 2.6, 0.9, MUTED, 20)
        b = node("新界面稿", 2.6, 0.9, PURPLE, 20)
        c = node("现有前端代码", 2.6, 0.9, MUTED, 20)
        d = node("抽成设计稿传回", 2.8, 0.9, PURPLE, 20)
        a.move_to([-4.6, 1.7, 0]); b.move_to([-1.3, 1.7, 0])
        c.move_to([-4.6, 0.4, 0]); d.move_to([-1.3, 0.4, 0])
        self.P(FadeIn(a), Create(arrow(a.get_right(), b.get_left())), FadeIn(b), rt=0.8)
        self.W(max(self.t, self.cue(0) + 1.0))
        self.P(FadeIn(c), Create(arrow(c.get_right(), d.get_left())), FadeIn(d), rt=0.7)
        self.W(self.cue(1))
        build = card_rows("构建侧还会", [
            ("检查组件和设计令牌是否一致", BLUE),
            ("把项目流程做成演示视频", BLUE),
        ], 5.6, BLUE, 20)
        build.move_to([3.5, 1.05, 0])
        self.P(FadeIn(build, shift=LEFT * 0.15), rt=0.8)
        self.W(self.cue(2))
        disc = box(12.8, 1.15, color=ORANGE, fill="#0F141B").move_to([0, -1.55, 0])
        ds = fit(T("仓库写明：这不是 Google 的官方产品，接口和凭证要以 Stitch 文档为准。", 22, FG), 12.0).move_to(disc)
        cap = credit("据 stitch-skills README 与仓库免责声明", 14, 12).move_to([0, -2.4, 0])
        self.P(FadeIn(disc), FadeIn(ds), FadeIn(cap), rt=0.7)
        self.finish()

# ───────────────────────────── #1 plannotator
class P1a(IntroScene):
    key = "P1a"; pid = "pn"
    def right(self):
        c = np.array([3.7, 0.3, 0])
        g, cap = picture("assets/proc/plan-home.png", width=6.15, height=4.4, credit="图：官网 plannotator.ai", csize=14)
        g.move_to(c + UP * 0.15); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)

class P1b(Base):
    key = "P1b"
    def construct(self):
        hd = self.header("pn", "收件箱、计划与审查", BLUE)
        self.add(hd)
        g, cap = picture("assets/proc/plan-inbox.png", width=6.5, height=3.7, credit="图：Plannotator 官方收件箱截图", csize=14)
        g.move_to([-3.2, 0.95, 0]); cap.next_to(g, DOWN, buff=0.08)
        self.P(FadeIn(g), FadeIn(cap), rt=0.8)
        pts = bullets([
            "多个智能体的提问和文件收在同一窗口",
            "不必占着会话，回复回到那一次运行",
            "计划评审由钩子自动弹出",
            "重要改动可按章节先看核心",
            "本地页面也能透过代理直接批注",
        ], 5.6, 20, BLUE, 0.22)
        pts.move_to([3.6, 0.85, 0])
        self.P(LaggedStart(*[FadeIn(p, shift=LEFT * 0.1) for p in pts], lag_ratio=0.12), rt=1.4)
        self.W(self.cue(2))
        chips = VGroup(chip("引导式审查按章节排", color=PURPLE, size=20),
                       chip("本地页面可直接画点", color=TEAL, size=20)).arrange(RIGHT, buff=0.25)
        chips.move_to([0, -1.95, 0])
        self.P(FadeIn(chips), rt=0.6)
        self.finish()

class P1c(Base):
    key = "P1c"
    def construct(self):
        hd = self.header("pn", "终端批注与跨设备协作", GREEN)
        self.add(hd)
        g1, c1 = picture("assets/proc/plan-herdr.png", width=6.2, height=3.35, credit="图：Plannotator 终端批注界面", csize=14)
        g2, c2 = picture("assets/proc/plan-review.png", width=6.2, height=3.35, credit="图：Plannotator 代码审查窗口（本周更新至 v0.29.5）", csize=14)
        g1.move_to([-3.3, 0.85, 0]); c1.next_to(g1, DOWN, buff=0.08)
        g2.move_to([3.3, 0.85, 0]); c2.next_to(g2, DOWN, buff=0.08)
        self.P(FadeIn(g1), FadeIn(c1), rt=0.7)
        self.W(self.cue(1))
        self.P(FadeIn(g2), FadeIn(c2), rt=0.7)
        self.W(self.cue(2))
        take = fit(T("本周打通跨电脑线程合并与 Ship 推进合并，把拍板权收回到人手里。", 23, FG), 12.6)
        take.move_to([0, -2.15, 0])
        self.P(FadeIn(take), rt=0.6)
        self.finish()

# ───────────────────────────── 片尾
class S6_Outro(Base):
    key = "S6_Outro"
    def construct(self):
        title = T("本周 Agent/AI Top 5 回顾", 42, FG, weight=BOLD).to_edge(UP, buff=0.32)
        self.P(FadeIn(title, shift=DOWN * 0.2), rt=0.6)
        tag = {
            "pn": "把拍板权收回到本地评审工作台",
            "st": "设计稿和组件代码之间倒手",
            "mw": "本地检索、按评测剪枝的网页指南",
            "nod": "自带沙盒电脑与浏览器的个人智能体",
            "ocr": "确定性流水线卡住，代理再下结论",
        }
        rows = Group()
        for pid in ["pn", "st", "mw", "nod", "ocr"]:
            d = DATA[pid]
            b = box(13.0, 0.78, r=0.1)
            av = avatar(pid, 0.5)
            rk = T(f"#{d['rank']}", 30, YELLOW, weight=BOLD)
            nm = fit(M(REPO[pid], 22, FG), 5.2)
            tg = fit(T(tag[pid], 20, MUTED), 4.1)
            ws = VGroup(gh_star(0.12), M(f"+{d['week']:,}", 24, YELLOW)).arrange(RIGHT, buff=0.1)
            rk.move_to(b.get_left() + RIGHT * 0.45); av.move_to(b.get_left() + RIGHT * 1.05)
            nm.move_to(b.get_left() + RIGHT * 1.45, aligned_edge=LEFT)
            tg.move_to(b.get_left() + RIGHT * 6.85, aligned_edge=LEFT)
            ws.move_to(b.get_right() + LEFT * 0.3, aligned_edge=RIGHT)
            rows.add(Group(b, rk, av, nm, tg, ws))
        rows.arrange(DOWN, buff=0.12).next_to(title, DOWN, buff=0.28)
        self.P(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15), rt=1.4)
        self.W(self.cue(1))
        kw = VGroup(chip("技能与沙盒电脑补齐执行力", color=BLUE, size=25),
                    chip("安全边界与拍板权留给人", color=GREEN, size=25)).arrange(RIGHT, buff=0.35)
        fit(kw, 13).next_to(rows, DOWN, buff=0.28)
        self.P(FadeIn(kw[0], scale=0.9), rt=0.55)
        self.W(self.cue(2))
        self.P(FadeIn(kw[1], scale=0.9), rt=0.55)
        self.W(self.cue(3))
        bye = T("下周见", 34, YELLOW).next_to(title, RIGHT, buff=0.4).align_to(title, DOWN)
        self.P(FadeIn(bye), rt=0.5)
        self.finish()
