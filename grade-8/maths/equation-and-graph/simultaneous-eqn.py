from manim import *
from manim_themes.manim_theme import apply_theme

# ============================================================================
# ESTABLISH LONDON THEME COLORS & CONSTANTS (Synchronized with plist specs)
# ============================================================================
BG_COLOR = "#F8F5EC"
INK = "#1F3A2F"
DIM = "#756A55"
GOLD = "#E5AA2C"
PINK = "#C461C4"
TEAL = "#5AC2A0"
GREEN = "#6E903A"
RED = "#C14A4A"


# ============================================================================
# FRUIT VECTOR GRAPHICS HELPERS
# ============================================================================
def make_apple(scale_factor=1.0):
    """Draws a stylized vector apple."""
    apple = VGroup()

    # Apple Body (Two overlapping lobes merged together)
    left_lobe = Ellipse(width=0.45, height=0.5, color=RED, fill_opacity=0.9).shift(LEFT * 0.1)
    right_lobe = Ellipse(width=0.45, height=0.5, color=RED, fill_opacity=0.9).shift(RIGHT * 0.1)
    body = Union(left_lobe, right_lobe, color=RED, fill_opacity=0.9, stroke_width=1.5)

    # Stem
    stem = CubicBezier(
        start_anchor=ORIGIN + UP * 0.22,
        start_handle=ORIGIN + UP * 0.35 + RIGHT * 0.05,
        end_handle=ORIGIN + UP * 0.45 + RIGHT * 0.1,
        end_anchor=ORIGIN + UP * 0.48 + RIGHT * 0.15,
        color="#704214",
        stroke_width=3,
    )

    # Leaf
    leaf = Ellipse(width=0.2, height=0.1, color=GREEN, fill_opacity=1.0)
    leaf.rotate(PI / 6).move_to(ORIGIN + UP * 0.42 + RIGHT * 0.2)

    apple.add(body, stem, leaf)
    return apple.scale(scale_factor)


def make_banana(scale_factor=1.0):
    """Draws a stylized vector banana."""
    banana = VGroup()

    # Curved Banana Body (Smooth path outlining a crescent)
    body = VMobject(color=GOLD, fill_opacity=0.95, stroke_width=1.5)
    body.set_points_as_corners(
        [
            LEFT * 0.35 + UP * 0.25,
            LEFT * 0.1 + DOWN * 0.25,
            RIGHT * 0.3 + DOWN * 0.1,
            RIGHT * 0.45 + UP * 0.2,
            RIGHT * 0.35 + UP * 0.15,
            LEFT * 0.05 + DOWN * 0.15,
            LEFT * 0.3 + UP * 0.22,
            LEFT * 0.35 + UP * 0.25,  # close path
        ]
    )
    body.make_smooth()

    # Banana stem/cap
    tip = Line(start=LEFT * 0.35 + UP * 0.25, end=LEFT * 0.4 + UP * 0.3, color="#5C4033", stroke_width=4)

    banana.add(body, tip)
    return banana.scale(scale_factor * 1.1).rotate(-PI / 12)


# ============================================================================
# MAIN SCENE
# ============================================================================
class SimultaneousEquations(Scene):
    def setup(self):
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        # ============================================================
        # BEAT 0 — TITLE: introduce the topic
        # ============================================================
        title = Text("Simultaneous Equations", color=INK, font_size=54)
        sub = Text("two variables, one solution", color=DIM, font_size=28)
        VGroup(title, sub).arrange(DOWN, buff=0.5)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=1)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(sub), run_time=1)

        # ============================================================
        # BEAT 1 — MOTIVATION: the fruit shopping story
        # ============================================================
        setup = Text("You buy some fruit...", color=INK, font_size=34).to_edge(UP, buff=0.7)
        self.play(FadeIn(setup), run_time=1)
        self.wait(1)

        lbl1 = Text("Trip 1:", color=DIM, font_size=28)
        r1 = VGroup(make_apple(), make_apple(), make_banana(), MathTex("=", color=INK), MathTex("8", color=TEAL)).arrange(
            RIGHT, buff=0.32
        )
        row1 = VGroup(lbl1, r1).arrange(RIGHT, buff=0.6)

        lbl2 = Text("Trip 2:", color=DIM, font_size=28)
        r2 = VGroup(make_apple(), make_banana(), MathTex("=", color=INK), MathTex("5", color=TEAL)).arrange(RIGHT, buff=0.32)
        row2 = VGroup(lbl2, r2).arrange(RIGHT, buff=0.6)

        VGroup(row1, row2).arrange(DOWN, buff=0.9, aligned_edge=LEFT).move_to(UP * 1.0)

        # trip 1: fruits pop in ONE AT A TIME
        self.play(FadeIn(lbl1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in r1[:3]], lag_ratio=0.6), run_time=2)
        self.play(FadeIn(r1[3]), FadeIn(r1[4], shift=LEFT * 0.2), run_time=1)
        self.wait(1)

        # trip 2
        self.play(FadeOut(setup), FadeIn(lbl2), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in r2[:2]], lag_ratio=0.6), run_time=1.5)
        self.play(FadeIn(r2[2]), FadeIn(r2[3], shift=LEFT * 0.2), run_time=1)
        self.wait(1)

        # the mission: how much is ONE apple?
        q = (
            VGroup(make_apple(), MathTex("=", color=INK), MathTex("?", color=GOLD).scale(1.4))
            .arrange(RIGHT, buff=0.3)
            .move_to(DOWN * 1.5)
        )
        qtext = Text("How much is one apple?", color=INK, font_size=32).move_to(DOWN * 2.5)

        self.play(FadeOut(lbl1), FadeOut(lbl2), FadeIn(q, scale=0.7), FadeIn(qtext), run_time=1.2)
        self.play(Indicate(q[2], color=GOLD, scale_factor=1.4), run_time=1.5)
        self.wait(1.5)

        # icons morph into shorthand symbols  (2x + y = 8 ,  x + y = 5)
        hint = Text("In algebra:", color=DIM, font_size=30).to_edge(UP, buff=0.7)
        self.play(FadeIn(hint), FadeOut(qtext), run_time=1)
        self.wait(0.5)

        txt = Text("Let x = apple, y = banana", color=INK, font_size=30).to_edge(UP, buff=0.7)
        self.play(ReplacementTransform(hint, txt), run_time=1)
        self.wait(1)

        eq1 = MathTex("2x", "+", "y", "=", "8")
        eq1[0].set_color(GOLD)
        eq1[1].set_color(INK)
        eq1[2].set_color(PINK)
        eq1[3].set_color(INK)
        eq1[4].set_color(TEAL)
        eq1.move_to(r1)

        eq2 = MathTex("x", "+", "y", "=", "5")
        eq2[0].set_color(GOLD)
        eq2[1].set_color(INK)
        eq2[2].set_color(PINK)
        eq2[3].set_color(INK)
        eq2[4].set_color(TEAL)
        eq2.move_to(r2)

        self.play(ReplacementTransform(r1, eq1), run_time=2)
        self.play(ReplacementTransform(r2, eq2), run_time=2)
        self.wait(1.5)

        # ============================================================
        # BEAT 2 — MISCONCEPTION: "one equation has one answer"
        # ============================================================
        self.play(FadeOut(eq1), FadeOut(q), FadeOut(txt), eq2.animate.scale(1.15).move_to(UP * 2.9), run_time=1.5)
        self.wait(0.5)

        guess_data = [
            (r"x=2,\;y=3", UP * 1.5),
            (r"x=1,\;y=4", UP * 0.5),
            (r"x=4,\;y=1", DOWN * 0.5),
            (r"x=0.5,\;y=4.5", DOWN * 1.5),
        ]
        gvs = []
        for tex, pos in guess_data:
            g = MathTex(tex, color=INK).scale(0.95)
            c = MathTex(r"\checkmark", color=GREEN).scale(0.95)
            gv = VGroup(g, c).arrange(RIGHT, buff=0.35).move_to(pos)
            gvs.append(gv)

        # first guess: slow, feels like "the" answer
        self.play(FadeIn(gvs[0][0], shift=RIGHT * 0.5), run_time=1)
        self.play(Write(gvs[0][1]), run_time=0.8)
        self.wait(1)
        # then checks multiply
        for gv in gvs[1:]:
            self.play(FadeIn(gv[0], shift=RIGHT * 0.4), run_time=0.5)
            self.play(Write(gv[1]), run_time=0.4)
        self.wait(0.5)

        q2 = Text("Which one is right?", color=INK, font_size=34).move_to(DOWN * 2.7)
        self.play(FadeIn(q2), run_time=1)
        self.wait(2)
        q3 = Text("All of them.", color=GREEN, font_size=36).move_to(DOWN * 2.7)
        self.play(ReplacementTransform(q2, q3), run_time=1)
        self.wait(1.5)

        # ============================================================
        # BEAT 3 — an equation is a LINE of answers
        # ============================================================
        self.play(FadeOut(q3), run_time=0.8)

        axes = Axes(
            x_range=[0, 8.5, 2],
            y_range=[0, 8.5, 2],
            x_length=5.4,
            y_length=5.4,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 2},
        )
        axes.shift(LEFT * 2.6 + DOWN * 0.3)
        axes.add_coordinates()
        for ax in axes.axes:
            ax.numbers.set_color(DIM)
        xlab = MathTex("x", color=INK).scale(0.8).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        ylab = MathTex("y", color=INK).scale(0.8).next_to(axes.y_axis.get_end(), UP, buff=0.2)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=2)
        self.wait(0.5)

        # each verified guess flies to its point
        pts = [(2, 3), (1, 4), (4, 1), (0.5, 4.5)]
        dots = VGroup(*[Dot(axes.c2p(x, y), color=TEAL, radius=0.07) for x, y in pts])
        self.play(LaggedStart(*[ReplacementTransform(gv, d) for gv, d in zip(gvs, dots)], lag_ratio=0.25), run_time=2.5)
        self.wait(1)

        # more solutions rain in
        extra = [(0, 5), (3, 2), (5, 0), (1.5, 3.5), (2.5, 2.5), (4.5, 0.5)]
        extra_dots = VGroup(*[Dot(axes.c2p(x, y), color=TEAL, radius=0.06) for x, y in extra])
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.4) for d in extra_dots], lag_ratio=0.15), run_time=2)
        self.wait(0.5)

        # dots smear into the line x + y = 5
        line1 = Line(axes.c2p(0, 5), axes.c2p(5, 0), color=TEAL, stroke_width=5)
        self.play(Create(line1), run_time=2)
        self.play(FadeOut(dots), FadeOut(extra_dots), eq2.animate.scale(0.6).move_to(axes.c2p(6.1, 0.9)), run_time=1.5)
        self.wait(1)

        # ============================================================
        # BEAT 4 — the second condition enters: a second line
        # ============================================================
        eq1.scale(0.9).move_to(UP * 3.3 + LEFT * 2.6)
        self.play(FadeIn(eq1, shift=DOWN * 0.5), run_time=1)

        pts2 = [(0, 8), (2, 4), (4, 0)]
        d2 = VGroup(*[Dot(axes.c2p(x, y), color=PINK, radius=0.07) for x, y in pts2])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in d2], lag_ratio=0.3), run_time=1.5)

        line2 = Line(axes.c2p(0, 8), axes.c2p(4, 0), color=PINK, stroke_width=5)
        self.play(Create(line2), run_time=2)
        self.play(FadeOut(d2), eq1.animate.scale(0.75).move_to(axes.c2p(2.4, 6.6)), run_time=1.5)
        self.wait(1.5)

        # ============================================================
        # BEAT 5 — PREDICT-THEN-REVEAL: which point obeys BOTH?
        # ============================================================
        q4 = Text("Which point obeys BOTH?", color=INK, font_size=34).to_edge(UP, buff=0.5)
        self.play(FadeIn(q4), run_time=1)

        dA = Dot(axes.c2p(1, 4), color=GOLD, radius=0.10)  # on teal line only
        dB = Dot(axes.c2p(2, 4), color=GOLD, radius=0.10)  # on pink line only
        dC = Dot(axes.c2p(3, 2), color=GOLD, radius=0.10)  # intersection
        self.play(
            LaggedStart(FadeIn(dA, scale=0.4), FadeIn(dB, scale=0.4), FadeIn(dC, scale=0.4), lag_ratio=0.3), run_time=1.5
        )
        self.play(LaggedStart(*[Indicate(d, color=GOLD, scale_factor=1.6) for d in (dA, dB, dC)], lag_ratio=0.3), run_time=2)
        self.wait(3)  # --- prediction hold ---

        # candidate A fails
        tA = MathTex(r"2(1)+4=6\neq 8", color=RED).scale(0.9)
        tA.move_to(RIGHT * 3.9 + UP * 1.4)
        self.play(dA.animate.set_color(RED), FadeIn(tA, shift=LEFT * 0.4), Indicate(eq1, color=RED), run_time=1.5)
        self.wait(1.2)
        self.play(FadeOut(dA), FadeOut(tA), run_time=0.8)

        # candidate B fails
        tB = MathTex(r"2+4=6\neq 5", color=RED).scale(0.9)
        tB.move_to(RIGHT * 3.9 + UP * 1.4)
        self.play(dB.animate.set_color(RED), FadeIn(tB, shift=LEFT * 0.4), Indicate(eq2, color=RED), run_time=1.5)
        self.wait(1.2)
        self.play(FadeOut(dB), FadeOut(tB), run_time=0.8)

        # candidate C obeys BOTH
        tC1 = MathTex(r"3+2=5\;\checkmark", color=GREEN).scale(0.95)
        tC2 = MathTex(r"2(3)+2=8\;\checkmark", color=GREEN).scale(0.95)
        tC = VGroup(tC1, tC2).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        tC.move_to(RIGHT * 3.9 + UP * 1.2)
        self.play(dC.animate.set_color(GREEN), FadeIn(tC1, shift=LEFT * 0.4), Indicate(eq2, color=GREEN), run_time=1.5)
        self.play(FadeIn(tC2, shift=LEFT * 0.4), Indicate(eq1, color=GREEN), run_time=1.5)
        self.play(Flash(dC, color=GREEN, flash_radius=0.45), run_time=1)
        self.wait(1.5)

        # ============================================================
        # BEAT 6 — back to the fruit: the shorthand paid off
        # ============================================================
        sol = MathTex(r"x=3,\;y=2", color=GREEN).scale(1.1)
        sol.move_to(RIGHT * 3.9 + DOWN * 0.6)
        self.play(Write(sol), run_time=1.5)
        self.wait(1)

        self.play(FadeOut(q4), FadeOut(tC), run_time=0.8)

        # receipts return...
        i1 = (
            VGroup(make_apple(0.8), make_apple(0.8), make_banana(0.8), MathTex("=", color=INK), MathTex("8", color=TEAL))
            .arrange(RIGHT, buff=0.25)
            .move_to(RIGHT * 3.9 + UP * 2.3)
        )
        i2 = (
            VGroup(make_apple(0.8), make_banana(0.8), MathTex("=", color=INK), MathTex("5", color=TEAL))
            .arrange(RIGHT, buff=0.25)
            .move_to(RIGHT * 3.9 + UP * 1.3)
        )
        self.play(FadeIn(i1), FadeIn(i2), run_time=1)
        self.wait(0.5)

        # ...and fruits become numbers
        n1 = MathTex("3", "+", "3", "+", "2", "=", "8").scale(0.9)
        n1.set_color(INK)
        n1[0].set_color(GOLD)
        n1[2].set_color(GOLD)
        n1[4].set_color(PINK)
        n1[6].set_color(TEAL)
        n1.move_to(i1)
        n2 = MathTex("3", "+", "2", "=", "5").scale(0.9)
        n2.set_color(INK)
        n2[0].set_color(GOLD)
        n2[2].set_color(PINK)
        n2[4].set_color(TEAL)
        n2.move_to(i2)

        self.play(ReplacementTransform(i1, n1), ReplacementTransform(i2, n2), run_time=2)
        c1 = MathTex(r"\checkmark", color=GREEN).scale(0.9).next_to(n1, RIGHT, buff=0.3)
        c2 = MathTex(r"\checkmark", color=GREEN).scale(0.9).next_to(n2, RIGHT, buff=0.3)
        self.play(Write(c1), Write(c2), run_time=1)
        self.wait(1)

        # the original mission, answered
        payoff = (
            VGroup(make_apple(), MathTex("=", color=INK), MathTex("3", color=GREEN).scale(1.2))
            .arrange(RIGHT, buff=0.3)
            .move_to(RIGHT * 3.9 + DOWN * 1.9)
        )
        self.play(FadeIn(payoff, scale=0.7), run_time=1)
        self.play(Indicate(payoff, color=GREEN), run_time=1.2)
        self.wait(1.5)

        # ============================================================
        # BEAT 7 — FINAL IMAGE: two constraints trap one point
        # ============================================================
        self.play(
            FadeOut(n1),
            FadeOut(c1),
            FadeOut(n2),
            FadeOut(c2),
            FadeOut(payoff),
            FadeOut(axes),
            FadeOut(xlab),
            FadeOut(ylab),
            FadeOut(eq1),
            FadeOut(eq2),
            run_time=1.5,
        )

        self.play(sol.animate.next_to(dC, DOWN, buff=0.45), run_time=1.5)
        self.play(dC.animate.scale(1.6), rate_func=there_and_back, run_time=1.5)
        self.play(Flash(dC, color=GREEN, flash_radius=0.5, line_length=0.3), run_time=1)
        self.wait(2)

        self.play(FadeOut(line1), FadeOut(line2), FadeOut(dC), FadeOut(sol), run_time=1.5)
        self.wait(0.5)

        # ============================================================
        # BEAT 8 — SIMPLE EXAMPLE AT THE END
        # ============================================================
        ex_title = Text("Your Turn: A Simple Example", color=INK, font_size=36).to_edge(UP, buff=0.7)
        self.play(FadeIn(ex_title), run_time=1)

        # Present system of equations on the left side
        ex_eq1 = MathTex("x", "+", "y", "=", "6").scale(1.2)
        ex_eq1[0].set_color(TEAL)
        ex_eq1[1].set_color(INK)
        ex_eq1[2].set_color(PINK)
        ex_eq1[3].set_color(INK)
        ex_eq1[4].set_color(INK)

        ex_eq2 = MathTex("x", "-", "y", "=", "2").scale(1.2)
        ex_eq2[0].set_color(TEAL)
        ex_eq2[1].set_color(INK)
        ex_eq2[2].set_color(PINK)
        ex_eq2[3].set_color(INK)
        ex_eq2[4].set_color(INK)

        ex_system = VGroup(ex_eq1, ex_eq2).arrange(DOWN, buff=0.6).shift(LEFT * 3)
        self.play(Write(ex_system), run_time=1.5)
        self.wait(1.5)

        # Build a visual mini-graph on the right side
        ex_axes = Axes(
            x_range=[0, 8, 2],
            y_range=[0, 8, 2],
            x_length=4.0,
            y_length=4.0,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 2.0},
        )
        ex_axes.shift(RIGHT * 3 + DOWN * 0.5)
        ex_axes.add_coordinates()
        for ax in ex_axes.axes:
            ax.numbers.set_color(DIM).scale(0.8)

        self.play(Create(ex_axes), run_time=1.5)

        # Draw visual constraint lines: x + y = 6 (Teal) and x - y = 2 (Pink)
        ex_line1 = Line(ex_axes.c2p(0, 6), ex_axes.c2p(6, 0), color=TEAL, stroke_width=4)
        ex_line2 = Line(ex_axes.c2p(2, 0), ex_axes.c2p(8, 6), color=PINK, stroke_width=4)

        self.play(Create(ex_line1), run_time=1.5)
        self.play(Create(ex_line2), run_time=1.5)
        self.wait(1.5)

        # Highlight the single intersection answer point: (4, 2)
        ex_dot = Dot(ex_axes.c2p(4, 2), color=GREEN, radius=0.09)
        self.play(FadeIn(ex_dot, scale=0.5), run_time=0.8)
        self.play(Flash(ex_dot, color=GREEN, flash_radius=0.4), run_time=0.8)

        # State final visual solution
        ex_sol = MathTex("x=4", ",\n", "y=2", color=GREEN).scale(1.2).shift(LEFT * 3 + DOWN * 1.8)
        self.play(Write(ex_sol), run_time=1.2)
        self.wait(3.0)

        # Final cleanup fadeout
        self.play(
            FadeOut(ex_title),
            FadeOut(ex_system),
            FadeOut(ex_axes),
            FadeOut(ex_line1),
            FadeOut(ex_line2),
            FadeOut(ex_dot),
            FadeOut(ex_sol),
            run_time=1.5,
        )
        self.wait(0.5)
