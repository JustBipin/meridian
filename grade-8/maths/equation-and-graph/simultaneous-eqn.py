from manim import *

# ---------- COLOR SEMANTICS ----------
BG    = "#F8F5EC"   # background
INK   = "#1F3A2F"   # default elements
GOLD  = "#D4A82C"   # unknowns / variables (apples, x)
TEAL  = "#3A7A8A"   # givens / inputs (prices, line 1)
GREEN = "#5A8A3A"   # results / answers
RED   = "#C14A4A"   # errors
PINK  = "#C45F8A"   # secondary highlight (bananas, y, line 2)
DIM   = "#756A55"   # de-emphasized

config.background_color = BG

def make_apple(scale=1.0):
    body = Circle(radius=0.28, fill_color=GOLD, fill_opacity=1.0,
                  stroke_color=INK, stroke_width=2.5)
    stem = ArcBetweenPoints(body.get_top() + DOWN * 0.02,
                            body.get_top() + UP * 0.16 + RIGHT * 0.05,
                            angle=-PI / 4).set_stroke(INK, width=4)
    leaf = Ellipse(width=0.20, height=0.10,
                   fill_color=INK, fill_opacity=1.0, stroke_width=0)
    leaf.rotate(35 * DEGREES)
    leaf.move_to(body.get_top() + UP * 0.10 + RIGHT * 0.16)
    return VGroup(body, stem, leaf).scale(scale)


def make_banana(scale=1.0):
    # a solid curved crescent (bottom arc of an annulus) = banana shape
    b = AnnularSector(inner_radius=0.22, outer_radius=0.42,
                      angle=150 * DEGREES, start_angle=195 * DEGREES,
                      fill_color=PINK, fill_opacity=1.0,
                      stroke_color=INK, stroke_width=2.5)
    return VGroup(b).scale(scale)


class SimultaneousEquations(Scene):
    def construct(self):

        # ============================================================
        # BEAT 0 — TITLE: introduce the topic
        # ============================================================
        title = Text("Simultaneous Equations", color=INK, font_size=54)
        sub = Text("two unknowns, one answer", color=DIM, font_size=28)
        VGroup(title, sub).arrange(DOWN, buff=0.5)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=1)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(sub), run_time=1)

        # ============================================================
        # BEAT 1 — MOTIVATION: the fruit shopping story
        # ============================================================
        setup = Text("You buy some fruit...", color=INK,
                     font_size=34).to_edge(UP, buff=0.7)
        self.play(FadeIn(setup), run_time=1)
        self.wait(1)

        lbl1 = Text("Trip 1:", color=DIM, font_size=28)
        r1 = VGroup(make_apple(), make_apple(), make_banana(),
                    MathTex("=", color=INK),
                    MathTex("8", color=TEAL)).arrange(RIGHT, buff=0.32)
        row1 = VGroup(lbl1, r1).arrange(RIGHT, buff=0.6)

        lbl2 = Text("Trip 2:", color=DIM, font_size=28)
        r2 = VGroup(make_apple(), make_banana(),
                    MathTex("=", color=INK),
                    MathTex("5", color=TEAL)).arrange(RIGHT, buff=0.32)
        row2 = VGroup(lbl2, r2).arrange(RIGHT, buff=0.6)

        VGroup(row1, row2).arrange(DOWN, buff=0.9,
                                   aligned_edge=LEFT).move_to(UP * 1.0)

        # trip 1: fruits pop in ONE AT A TIME (the "suppose we bought..." feel)
        self.play(FadeIn(lbl1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in r1[:3]],
                              lag_ratio=0.6), run_time=2)
        self.play(FadeIn(r1[3]), FadeIn(r1[4], shift=LEFT * 0.2), run_time=1)
        self.wait(1)

        # trip 2
        self.play(FadeOut(setup), FadeIn(lbl2), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in r2[:2]],
                              lag_ratio=0.6), run_time=1.5)
        self.play(FadeIn(r2[2]), FadeIn(r2[3], shift=LEFT * 0.2), run_time=1)
        self.wait(1)

        # the mission: how much is ONE apple?
        q = VGroup(make_apple(),
                   MathTex("=", color=INK),
                   MathTex("?", color=GOLD).scale(1.4)
                   ).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.5)
        qtext = Text("How much is one apple?", color=INK,
                     font_size=32).move_to(DOWN * 2.5)

        self.play(FadeOut(lbl1), FadeOut(lbl2),
                  FadeIn(q, scale=0.7), FadeIn(qtext), run_time=1.2)
        self.play(Indicate(q[2], color=GOLD, scale_factor=1.4), run_time=1.5)
        self.wait(1.5)

        # icons morph into shorthand symbols  (2x + y = 8 ,  x + y = 5)
        hint = Text("In algebra:", color=DIM, font_size=30).to_edge(UP, buff=0.7)
        self.play(FadeIn(hint), FadeOut(qtext), run_time=1)

        eq1 = MathTex("2x", "+", "y", "=", "8")
        eq1[0].set_color(GOLD); eq1[1].set_color(INK); eq1[2].set_color(PINK)
        eq1[3].set_color(INK);  eq1[4].set_color(TEAL)
        eq1.move_to(r1)

        eq2 = MathTex("x", "+", "y", "=", "5")
        eq2[0].set_color(GOLD); eq2[1].set_color(INK); eq2[2].set_color(PINK)
        eq2[3].set_color(INK);  eq2[4].set_color(TEAL)
        eq2.move_to(r2)

        self.play(ReplacementTransform(r1, eq1), run_time=2)
        self.play(ReplacementTransform(r2, eq2), run_time=2)
        self.wait(1.5)

        # ============================================================
        # BEAT 2 — MISCONCEPTION: "one equation has one answer"
        # ============================================================
        self.play(FadeOut(eq1), FadeOut(q), FadeOut(hint),
                  eq2.animate.scale(1.15).move_to(UP * 2.9), run_time=1.5)
        self.wait(0.5)

        guess_data = [(r"x=2,\;y=3",     UP * 1.5),
                      (r"x=1,\;y=4",     UP * 0.5),
                      (r"x=4,\;y=1",     DOWN * 0.5),
                      (r"x=0.5,\;y=4.5", DOWN * 1.5)]
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
        # then checks multiply alarmingly
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

        axes = Axes(x_range=[0, 8.5, 2], y_range=[0, 8.5, 2],
                    x_length=5.4, y_length=5.4, tips=False,
                    axis_config={"color": DIM, "stroke_width": 2})
        axes.shift(LEFT * 2.6 + DOWN * 0.3)
        axes.add_coordinates()
        for ax in axes.axes:
            ax.numbers.set_color(DIM)
        xlab = MathTex("x", color=INK).scale(0.8).next_to(
            axes.x_axis.get_end(), RIGHT, buff=0.2)
        ylab = MathTex("y", color=INK).scale(0.8).next_to(
            axes.y_axis.get_end(), UP, buff=0.2)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab), run_time=2)
        self.wait(0.5)

        # each verified guess flies to its point:  guesses BECOME points
        pts = [(2, 3), (1, 4), (4, 1), (0.5, 4.5)]
        dots = VGroup(*[Dot(axes.c2p(x, y), color=TEAL, radius=0.07)
                        for x, y in pts])
        self.play(LaggedStart(
            *[ReplacementTransform(gv, d) for gv, d in zip(gvs, dots)],
            lag_ratio=0.25), run_time=2.5)
        self.wait(1)

        # more solutions rain in along the same invisible line
        extra = [(0, 5), (3, 2), (5, 0), (1.5, 3.5), (2.5, 2.5), (4.5, 0.5)]
        extra_dots = VGroup(*[Dot(axes.c2p(x, y), color=TEAL, radius=0.06)
                              for x, y in extra])
        self.play(LaggedStart(
            *[FadeIn(d, shift=DOWN * 0.4) for d in extra_dots],
            lag_ratio=0.15), run_time=2)
        self.wait(0.5)

        # dots smear into the full continuous line x + y = 5
        line1 = Line(axes.c2p(0, 5), axes.c2p(5, 0), color=TEAL, stroke_width=5)
        self.play(Create(line1), run_time=2)
        self.play(FadeOut(dots), FadeOut(extra_dots),
                  eq2.animate.scale(0.6).move_to(axes.c2p(6.1, 0.9)),
                  run_time=1.5)
        self.wait(1)

        # ============================================================
        # BEAT 4 — the second condition enters: a second line
        # ============================================================
        eq1.scale(0.9).move_to(UP * 3.3 + LEFT * 2.6)
        self.play(FadeIn(eq1, shift=DOWN * 0.5), run_time=1)

        pts2 = [(0, 8), (2, 4), (4, 0)]
        d2 = VGroup(*[Dot(axes.c2p(x, y), color=PINK, radius=0.07)
                      for x, y in pts2])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in d2],
                              lag_ratio=0.3), run_time=1.5)

        line2 = Line(axes.c2p(0, 8), axes.c2p(4, 0), color=PINK, stroke_width=5)
        self.play(Create(line2), run_time=2)
        self.play(FadeOut(d2),
                  eq1.animate.scale(0.75).move_to(axes.c2p(2.4, 6.6)),
                  run_time=1.5)
        self.wait(1.5)

        # ============================================================
        # BEAT 5 — PREDICT-THEN-REVEAL: which point obeys BOTH?
        # ============================================================
        q4 = Text("Which point obeys BOTH?", color=INK,
                  font_size=34).to_edge(UP, buff=0.5)
        self.play(FadeIn(q4), run_time=1)

        dA = Dot(axes.c2p(1, 4), color=GOLD, radius=0.10)  # on teal line only
        dB = Dot(axes.c2p(2, 4), color=GOLD, radius=0.10)  # on pink line only
        dC = Dot(axes.c2p(3, 2), color=GOLD, radius=0.10)  # intersection
        self.play(LaggedStart(FadeIn(dA, scale=0.4),
                              FadeIn(dB, scale=0.4),
                              FadeIn(dC, scale=0.4), lag_ratio=0.3), run_time=1.5)
        self.play(LaggedStart(
            *[Indicate(d, color=GOLD, scale_factor=1.6) for d in (dA, dB, dC)],
            lag_ratio=0.3), run_time=2)
        self.wait(3)  # --- prediction hold ---

        # candidate A fails the pink equation:  2(1)+4 = 6 != 8
        tA = MathTex(r"2(1)+4=6\neq 8", color=RED).scale(0.9)
        tA.move_to(RIGHT * 3.9 + UP * 1.4)
        self.play(dA.animate.set_color(RED),
                  FadeIn(tA, shift=LEFT * 0.4),
                  Indicate(eq1, color=RED), run_time=1.5)
        self.wait(1.2)
        self.play(FadeOut(dA), FadeOut(tA), run_time=0.8)

        # candidate B fails the teal equation:  2+4 = 6 != 5
        tB = MathTex(r"2+4=6\neq 5", color=RED).scale(0.9)
        tB.move_to(RIGHT * 3.9 + UP * 1.4)
        self.play(dB.animate.set_color(RED),
                  FadeIn(tB, shift=LEFT * 0.4),
                  Indicate(eq2, color=RED), run_time=1.5)
        self.wait(1.2)
        self.play(FadeOut(dB), FadeOut(tB), run_time=0.8)

        # candidate C obeys BOTH:  3+2=5  and  2(3)+2=8
        tC1 = MathTex(r"3+2=5\;\checkmark", color=GREEN).scale(0.95)
        tC2 = MathTex(r"2(3)+2=8\;\checkmark", color=GREEN).scale(0.95)
        tC = VGroup(tC1, tC2).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        tC.move_to(RIGHT * 3.9 + UP * 1.2)
        self.play(dC.animate.set_color(GREEN),
                  FadeIn(tC1, shift=LEFT * 0.4),
                  Indicate(eq2, color=GREEN), run_time=1.5)
        self.play(FadeIn(tC2, shift=LEFT * 0.4),
                  Indicate(eq1, color=GREEN), run_time=1.5)
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
        i1 = VGroup(make_apple(0.8), make_apple(0.8), make_banana(0.8),
                    MathTex("=", color=INK), MathTex("8", color=TEAL)
                    ).arrange(RIGHT, buff=0.25).move_to(RIGHT * 3.9 + UP * 2.3)
        i2 = VGroup(make_apple(0.8), make_banana(0.8),
                    MathTex("=", color=INK), MathTex("5", color=TEAL)
                    ).arrange(RIGHT, buff=0.25).move_to(RIGHT * 3.9 + UP * 1.3)
        self.play(FadeIn(i1), FadeIn(i2), run_time=1)
        self.wait(0.5)

        # ...and the fruits become their prices:  3+3+2=8 ,  3+2=5
        n1 = MathTex("3", "+", "3", "+", "2", "=", "8").scale(0.9)
        n1.set_color(INK)
        n1[0].set_color(GOLD); n1[2].set_color(GOLD)
        n1[4].set_color(PINK); n1[6].set_color(TEAL)
        n1.move_to(i1)
        n2 = MathTex("3", "+", "2", "=", "5").scale(0.9)
        n2.set_color(INK)
        n2[0].set_color(GOLD); n2[2].set_color(PINK); n2[4].set_color(TEAL)
        n2.move_to(i2)

        self.play(ReplacementTransform(i1, n1),
                  ReplacementTransform(i2, n2), run_time=2)
        c1 = MathTex(r"\checkmark", color=GREEN).scale(0.9).next_to(n1, RIGHT, buff=0.3)
        c2 = MathTex(r"\checkmark", color=GREEN).scale(0.9).next_to(n2, RIGHT, buff=0.3)
        self.play(Write(c1), Write(c2), run_time=1)
        self.wait(1)

        # the original mission, answered
        payoff = VGroup(make_apple(),
                        MathTex("=", color=INK),
                        MathTex("3", color=GREEN).scale(1.2)
                        ).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.9 + DOWN * 1.9)
        self.play(FadeIn(payoff, scale=0.7), run_time=1)
        self.play(Indicate(payoff, color=GREEN), run_time=1.2)
        self.wait(1.5)

        # ============================================================
        # BEAT 7 — FINAL IMAGE: two constraints trap one point
        # ============================================================
        self.play(FadeOut(n1), FadeOut(c1), FadeOut(n2), FadeOut(c2),
                  FadeOut(payoff), FadeOut(axes), FadeOut(xlab), FadeOut(ylab),
                  FadeOut(eq1), FadeOut(eq2), run_time=1.5)

        self.play(sol.animate.next_to(dC, DOWN, buff=0.45), run_time=1.5)
        self.play(dC.animate.scale(1.6), rate_func=there_and_back, run_time=1.5)
        self.play(Flash(dC, color=GREEN, flash_radius=0.5, line_length=0.3),
                  run_time=1)
        self.wait(2)

        self.play(FadeOut(line1), FadeOut(line2), FadeOut(dC), FadeOut(sol),
                  run_time=1.5)
        self.wait(0.5)