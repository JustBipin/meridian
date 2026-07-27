import numpy as np
from manim import *
from manim_themes.manim_theme import apply_theme


class QuadraticIntro(Scene):
    def setup(self):
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        # ==================================================================
        # BEAT 1 — The number riddle (~18 s)
        # ==================================================================
        title = Text("I'm thinking of a number...", font_size=40, color=BLACK)
        title.to_edge(UP, buff=1.0)

        box1 = Square(side_length=0.9, color=RED)
        q1 = MathTex("?", color=PURPLE).scale(1.1).move_to(box1)
        b1 = VGroup(box1, q1)
        b2 = b1.copy()
        times = MathTex(r"\times", color=BLACK).scale(1.2)
        eq_sign = MathTex("=", color=BLACK).scale(1.2)
        nine = MathTex("9", color=BLUE).scale(1.6)
        riddle = VGroup(b1, times, b2, eq_sign, nine).arrange(RIGHT, buff=0.6)

        self.play(Write(title))
        self.wait(0.5)
        self.play(
            FadeIn(b1, scale=0.5),
            FadeIn(times),
            FadeIn(b2, scale=0.5),
            FadeIn(eq_sign),
        )
        self.play(FadeIn(nine, shift=DOWN * 0.6))
        self.play(Indicate(b1, color=RED), Indicate(b2, color=RED))
        self.wait(2)

        # ==================================================================
        # BEAT 2 — The confident (incomplete) answer + linear flashback (~20 s)
        # ==================================================================
        three1 = MathTex("3", color=BLACK).scale(1.1).move_to(box1)
        three2 = MathTex("3", color=BLACK).scale(1.1).move_to(b2[0])
        self.play(Transform(q1, three1), Transform(b2[1], three2), run_time=1.5)
        check = MathTex(r"\checkmark", color=GREEN).scale(1.2)
        check.next_to(nine, RIGHT, buff=0.5)
        self.play(FadeIn(check, scale=0.5))
        self.wait(1)

        flashback = (
            VGroup(
                MathTex("x + 5 = 8", color=GRAY),
                MathTex(r"x = 3\ \checkmark", color=GRAY),
                Text("(one answer, as always)", font_size=24, color=GRAY),
            )
            .arrange(DOWN, buff=0.3)
            .scale(0.9)
            .to_corner(DL, buff=0.8)
        )
        self.play(FadeIn(flashback, shift=UP * 0.3))
        self.wait(1)

        banner_txt = Text("Solved!  The only answer: 3", font_size=32, color=RED)
        banner_box = SurroundingRectangle(banner_txt, color=RED, buff=0.25)
        banner = VGroup(banner_box, banner_txt).next_to(riddle, DOWN, buff=0.8)
        banner.rotate(-0.06)
        self.play(FadeIn(banner, scale=1.6), run_time=0.7)
        self.wait(1.5)

        self.play(FadeOut(title), FadeOut(riddle), FadeOut(check), FadeOut(flashback), FadeOut(banner))
        self.wait(0.3)

        # ==================================================================
        # BEAT 3 — The squaring machine: sign annihilation (~45 s)
        # ==================================================================
        mach_box = RoundedRectangle(corner_radius=0.25, width=3.4, height=2.0, color=BLACK)
        mach_lab = Text("× itself", font_size=28, color=BLACK)
        mach_lab.next_to(mach_box.get_top(), DOWN, buff=0.15)
        machine = VGroup(mach_box, mach_lab)
        self.play(Create(mach_box), Write(mach_lab))
        self.wait(0.5)

        def feed_simple(n):
            inp = MathTex(str(n), color=BLUE).scale(1.3).move_to(LEFT * 5)
            self.play(FadeIn(inp, shift=RIGHT * 0.5), run_time=0.6)
            self.play(inp.animate.move_to(mach_box.get_left() + RIGHT * 0.4).scale(0.7), run_time=0.8)
            calc = MathTex(str(n), r"\times", str(n), color=BLACK)
            calc.move_to(mach_box.get_center() + DOWN * 0.15)
            calc[0].set_color(BLUE)
            calc[2].set_color(BLUE)
            self.play(ReplacementTransform(inp, calc), run_time=0.8)
            out = MathTex(str(n * n), color=GREEN).scale(1.3).move_to(RIGHT * 5)
            self.play(ReplacementTransform(calc, out), run_time=1)
            self.wait(0.6)
            self.play(FadeOut(out), run_time=0.4)

        feed_simple(2)
        feed_simple(3)

        # Feed -3: the two minus signs collide and annihilate
        inp = MathTex("-3", color=BLUE).scale(1.3).move_to(LEFT * 5)
        self.play(FadeIn(inp, shift=RIGHT * 0.5), run_time=0.6)
        self.play(inp.animate.move_to(mach_box.get_left() + RIGHT * 0.5).scale(0.7), run_time=0.8)
        calc = MathTex("(", "-", "3", ")", r"\times", "(", "-", "3", ")", color=BLUE)
        calc.move_to(mach_box.get_center() + DOWN * 0.15)
        calc[1].set_color(PURPLE)
        calc[6].set_color(PURPLE)
        self.play(ReplacementTransform(inp, calc), run_time=0.8)
        self.wait(1)

        m1, m2 = calc[1], calc[6]
        mid = (m1.get_center() + m2.get_center()) / 2 + UP * 0.6
        self.play(m1.animate.move_to(mid + LEFT * 0.12), m2.animate.move_to(mid + RIGHT * 0.12), run_time=1.5)
        self.play(Flash(mid, color=PURPLE, flash_radius=0.5), FadeOut(m1), FadeOut(m2))
        cancel_cap = Text("minus minus becomes plus!", font_size=26, color=PURPLE)
        cancel_cap.next_to(mach_box, DOWN, buff=0.5)
        self.play(FadeIn(cancel_cap))
        rest = VGroup(calc[0], calc[2], calc[3], calc[4], calc[5], calc[7], calc[8])
        out9 = MathTex("9", color=GREEN).scale(1.5).move_to(RIGHT * 5)
        self.play(ReplacementTransform(rest, out9), run_time=1.5)
        self.wait(1)

        # The RED banner returns... and cracks apart
        banner2_txt = Text("Only answer: 3", font_size=26, color=RED)
        banner2_box = SurroundingRectangle(banner2_txt, color=RED, buff=0.2)
        banner2 = VGroup(banner2_box, banner2_txt).to_corner(UR, buff=0.7)
        self.play(FadeIn(banner2))
        self.wait(0.5)

        crack = VMobject(stroke_color=RED, stroke_width=5)
        p_top = banner2.get_top() + UP * 0.1
        p_bot = banner2.get_bottom() + DOWN * 0.1
        n_seg = 5
        pts = []
        for i in range(n_seg + 1):
            base = interpolate(p_top, p_bot, i / n_seg)
            off = RIGHT * (0.18 * (1 if i % 2 else -1)) if 0 < i < n_seg else ORIGIN
            pts.append(base + off)
        crack.set_points_as_corners(pts)
        self.play(Create(crack), run_time=0.8)
        self.play(Wiggle(banner2))
        self.play(FadeOut(VGroup(banner2, crack), shift=DOWN * 0.8, scale=0.7))

        answers = (
            VGroup(
                MathTex(r"3\ \checkmark", color=GREEN).scale(1.2),
                MathTex(r"-3\ \checkmark", color=GREEN).scale(1.2),
            )
            .arrange(RIGHT, buff=1.4)
            .next_to(machine, UP, buff=0.8)
        )
        two_txt = Text("Two different inputs  →  the same output 9", font_size=26, color=BLACK).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(answers[0], shift=UP * 0.3), FadeIn(answers[1], shift=UP * 0.3))
        self.play(FadeIn(two_txt))
        self.wait(2)

        self.play(FadeOut(answers), FadeOut(two_txt), FadeOut(cancel_cap), FadeOut(out9))
        self.play(machine.animate.scale(0.5).to_corner(UL, buff=0.5), run_time=1.5)

        # ==================================================================
        # BEAT 4 — Building the curve point by point (~50 s)
        # Includes PREDICT-THEN-REVEAL.
        # ==================================================================
        axes = (
            Axes(
                x_range=[-4, 4, 1],
                y_range=[0, 10, 1],
                x_length=6.0,
                y_length=5.2,
                axis_config={"color": BLACK},
                x_axis_config={"numbers_to_include": [-3, -2, -1, 1, 2, 3]},
                y_axis_config={"numbers_to_include": [1, 4, 9]},
                tips=False,
            )
            .to_edge(RIGHT, buff=0.8)
            .shift(DOWN * 0.4)
        )
        axes.set_color(BLACK)  # axis numbers take the theme foreground too
        self.play(Create(axes), run_time=1.5)
        self.wait(0.5)

        header = MathTex(r"\text{in}", r"\;\rightarrow\;", r"\text{out}", color=BLACK)
        header.move_to(LEFT * 4.8 + UP * 1.8)
        self.play(Write(header))

        rows = VGroup()
        dots_pts = VGroup()

        def add_row(n, i, extra_anims=None):
            row = MathTex(str(n), r"\;\rightarrow\;", str(n * n), color=BLACK).scale(0.85)
            row[0].set_color(BLUE)
            row[2].set_color(GREEN)
            row.move_to(header.get_center() + DOWN * (0.55 * (i + 1)))
            rows.add(row)
            dot = Dot(color=BLACK, radius=0.07).move_to(row.get_center())
            dots_pts.add(dot)
            anims = [FadeIn(row)]
            if extra_anims:
                anims += extra_anims
            self.play(*anims, run_time=0.6)
            self.play(dot.animate.move_to(axes.c2p(n, n * n)), run_time=0.9)

        for i, n in enumerate([0, 1, 2, 3]):
            add_row(n, i)
        self.wait(1)

        # ---- PREDICT-THEN-REVEAL ----
        prompt = Text(
            "Now the negatives: -1, -2, -3.\nWhere will the dots land?", font_size=28, color=PURPLE, line_spacing=1
        )
        prompt.to_edge(UP, buff=0.4).shift(RIGHT * 2)
        ghosts = VGroup(
            Text("?", font_size=36, color=GRAY).move_to(axes.c2p(-1, 2)),
            Text("?", font_size=36, color=GRAY).move_to(axes.c2p(-2, 5)),
            Text("?", font_size=36, color=GRAY).move_to(axes.c2p(-3, 8)),
        )
        self.play(FadeIn(prompt), FadeIn(ghosts))
        self.wait(3)  # hold — let the viewer predict

        mirrors = VGroup()
        for j, n in enumerate([-1, -2, -3]):
            add_row(n, 4 + j, extra_anims=[FadeOut(ghosts[j])])
            mirror = DashedLine(axes.c2p(n, n * n), axes.c2p(-n, n * n), color=PURPLE, stroke_width=3)
            mirrors.add(mirror)
            self.play(Create(mirror), run_time=0.8)
        self.wait(1)
        self.play(FadeOut(mirrors), FadeOut(prompt))

        curve = axes.plot(lambda x: x * x, x_range=[-3.1, 3.1], color=RED)
        self.play(Create(curve), run_time=2.5)
        curve_label = (
            VGroup(
                Text("a U-shaped curve", font_size=28, color=BLACK),
                Text("(a parabola)", font_size=22, color=GRAY),
            )
            .arrange(DOWN, buff=0.15)
            .to_edge(UP, buff=0.5)
            .shift(RIGHT * 2)
        )
        self.play(FadeIn(curve_label))
        self.wait(2)

        self.play(FadeOut(machine), FadeOut(header), FadeOut(rows), FadeOut(curve_label))

        # ==================================================================
        # BEAT 5 — Solving = hunting on the curve; notation as shorthand (~35 s)
        # ==================================================================
        eq1 = MathTex("?", r"\times", "?", "=", "9", color=BLACK).scale(1.1)
        eq1[0].set_color(RED)
        eq1[2].set_color(RED)
        eq1[4].set_color(BLUE)
        eq1.move_to(LEFT * 4.2 + UP * 2.6)
        self.play(Write(eq1))
        self.wait(1)

        eq2 = MathTex("x", r"\cdot", "x", "=", "9", color=BLACK).scale(1.1)
        eq2[0].set_color(RED)
        eq2[2].set_color(RED)
        eq2[4].set_color(BLUE)
        eq2.move_to(eq1)
        self.play(ReplacementTransform(eq1, eq2), run_time=1.5)
        caption1 = Text("we can also write it this way", font_size=24, color=GRAY)
        caption1.next_to(eq2, DOWN, buff=0.35)
        self.play(FadeIn(caption1))
        self.wait(1)

        eq3 = MathTex("x^2", "=", "9", color=BLACK).scale(1.1)
        eq3[0].set_color(RED)
        eq3[2].set_color(BLUE)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3), run_time=1.5)
        self.wait(1.5)

        # Highlight line sweeps up to height 9 — the hunt
        h = ValueTracker(0)
        hline = always_redraw(
            lambda: Line(axes.c2p(-4, h.get_value()), axes.c2p(4, h.get_value()), color=PURPLE, stroke_width=4)
        )
        self.add(hline)
        self.play(h.animate.set_value(9), run_time=3)

        sol_l = Dot(axes.c2p(-3, 9), color=GREEN, radius=0.1)
        sol_r = Dot(axes.c2p(3, 9), color=GREEN, radius=0.1)
        self.play(
            FadeIn(sol_l, scale=3),
            FadeIn(sol_r, scale=3),
            Flash(axes.c2p(-3, 9), color=GREEN),
            Flash(axes.c2p(3, 9), color=GREEN),
        )
        drop_l = DashedLine(axes.c2p(-3, 9), axes.c2p(-3, 0), color=GREEN, stroke_width=3)
        drop_r = DashedLine(axes.c2p(3, 9), axes.c2p(3, 0), color=GREEN, stroke_width=3)
        self.play(Create(drop_l), Create(drop_r), run_time=1.5)
        lab_l = MathTex("x=-3", color=GREEN).scale(0.8)
        lab_l.next_to(axes.c2p(-3, 0), DOWN, buff=0.55)
        lab_r = MathTex("x=3", color=GREEN).scale(0.8)
        lab_r.next_to(axes.c2p(3, 0), DOWN, buff=0.55)
        self.play(Write(lab_l), Write(lab_r))
        self.wait(1.5)

        eq4 = MathTex("x^2", "-", "9", "=", "0", color=BLACK).scale(1.1)
        eq4[0].set_color(RED)
        eq4[2].set_color(BLUE)
        eq4.move_to(eq3)
        self.play(TransformMatchingTex(eq3, eq4), FadeOut(caption1), run_time=1.5)
        caption2 = Text("same question, different way of writing it", font_size=24, color=GRAY)
        caption2.next_to(eq4, DOWN, buff=0.35)
        self.play(FadeIn(caption2))
        self.wait(2)

        # Clear the graph chapter completely before the definition chapter
        hline.clear_updaters()
        self.play(
            FadeOut(eq4),
            FadeOut(caption2),
            FadeOut(hline),
            FadeOut(sol_l),
            FadeOut(sol_r),
            FadeOut(drop_l),
            FadeOut(drop_r),
            FadeOut(lab_l),
            FadeOut(lab_r),
            FadeOut(axes),
            FadeOut(curve),
            FadeOut(dots_pts),
        )
        self.wait(0.3)

        # ==================================================================
        # BEAT 5b — SO WHAT *IS* A QUADRATIC EQUATION? (~30 s)
        # ==================================================================
        def_title = Text("QUADRATIC EQUATION", font_size=42, color=BLACK, weight=BOLD)
        def_title.to_edge(UP, buff=0.8)
        def_body = (
            VGroup(
                Text("= any equation where the unknown", font_size=30, color=BLACK),
                VGroup(
                    Text("is squared:  ", font_size=30, color=BLACK),
                    MathTex("x^2", color=BLACK).scale(1.2),
                ).arrange(RIGHT, buff=0.1),
            )
            .arrange(DOWN, buff=0.25)
            .next_to(def_title, DOWN, buff=0.6)
        )
        self.play(Write(def_title))
        self.play(FadeIn(def_body, shift=UP * 0.2))
        ring = Circle(radius=0.5, color=RED).move_to(def_body[1][1])
        self.play(Create(ring))
        self.wait(2)

        # Sorting: which of these are quadratic?
        ex1 = MathTex("x^2", "=", "9", color=BLACK).scale(0.95)
        ex1[0].set_color(RED)
        ex2 = MathTex("x", "+", "5", "=", "8", color=BLACK).scale(0.95)
        ex3 = MathTex("x^2", "+", "2x", "=", "3", color=BLACK).scale(0.95)
        ex3[0].set_color(RED)
        examples = VGroup(ex1, ex2, ex3).arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        examples.next_to(def_body, DOWN, buff=0.8).shift(LEFT * 1.5)
        self.play(FadeIn(examples))
        self.wait(1)

        tag1 = (
            VGroup(MathTex(r"\checkmark", color=GREEN), Text("quadratic", font_size=24, color=GREEN))
            .arrange(RIGHT, buff=0.2)
            .next_to(ex1, RIGHT, buff=0.8)
        )
        self.play(Circumscribe(ex1[0], color=RED), FadeIn(tag1))
        self.wait(1)

        tag2 = (
            VGroup(MathTex(r"\times", color=RED), Text("no x² — means it has only one solution", font_size=24, color=GRAY))
            .arrange(RIGHT, buff=0.2)
            .next_to(ex2, RIGHT, buff=0.8)
        )
        self.play(ex2.animate.set_color(GRAY), FadeIn(tag2))
        self.wait(1)

        tag3 = (
            VGroup(MathTex(r"\checkmark", color=GREEN), Text("quadratic", font_size=24, color=GREEN))
            .arrange(RIGHT, buff=0.2)
            .next_to(ex3, RIGHT, buff=0.8)
        )
        self.play(Circumscribe(ex3[0], color=RED), FadeIn(tag3))
        self.wait(1)

        punch = Text("the x² is why it can have TWO answers", font_size=28, color=GREEN)
        punch.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(punch, shift=UP * 0.3))
        self.wait(2.5)

        self.play(
            FadeOut(def_title),
            FadeOut(def_body),
            FadeOut(ring),
            FadeOut(examples),
            FadeOut(tag1),
            FadeOut(tag2),
            FadeOut(tag3),
            FadeOut(punch),
        )
        self.wait(0.3)

        # ==================================================================
        # BEAT 6 — The line vs. the U : final memorable image (~40 s)
        # ==================================================================
        axesL = Axes(
            x_range=[-1, 5, 1],
            y_range=[-2, 12, 2],
            x_length=4.4,
            y_length=4.6,
            axis_config={"color": GRAY},
            tips=False,
        ).shift(LEFT * 3.4 + DOWN * 0.3)
        axesL.set_color(GRAY)
        lineL = axesL.plot(lambda x: 2 * x + 1, x_range=[-0.8, 4.8], color=GRAY)
        targL = Line(axesL.c2p(-1, 9), axesL.c2p(5, 9), color=PURPLE, stroke_width=3)
        dotL = Dot(axesL.c2p(4, 9), color=GREEN, radius=0.09)  # 2*4+1 = 9
        labL = Text("1 answer", font_size=28, color=BLACK)
        labL.next_to(axesL, DOWN, buff=0.4)

        axesR = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 12, 2],
            x_length=4.4,
            y_length=4.6,
            axis_config={"color": BLACK},
            tips=False,
        ).shift(RIGHT * 3.4 + DOWN * 0.3)
        axesR.set_color(BLACK)
        curveR = axesR.plot(lambda x: x * x, x_range=[-3.3, 3.3], color=RED)

        hr = ValueTracker(9)
        lineR = always_redraw(
            lambda: Line(axesR.c2p(-4, hr.get_value()), axesR.c2p(4, hr.get_value()), color=PURPLE, stroke_width=3)
        )

        def dots_fn():
            hv = hr.get_value()
            if hv > 0.03:
                r = np.sqrt(hv)
                return VGroup(
                    Dot(axesR.c2p(-r, hv), color=GREEN, radius=0.09),
                    Dot(axesR.c2p(r, hv), color=GREEN, radius=0.09),
                )
            elif hv >= -0.03:
                return VGroup(Dot(axesR.c2p(0, 0), color=GREEN, radius=0.09))
            return VGroup()

        dotsR = always_redraw(dots_fn)
        labR = Text("2 answers", font_size=28, color=GREEN)
        labR.next_to(axesR, DOWN, buff=0.4)

        self.play(Create(axesL), Create(axesR), run_time=1.5)
        self.play(Create(lineL), Create(curveR), run_time=2)
        self.play(Create(targL), FadeIn(lineR))
        self.add(dotsR)
        self.play(FadeIn(dotL, scale=2), FadeIn(labL), FadeIn(labR))
        self.wait(1.5)

        # Continuous slide: 2 answers → merge into 1 → vanish → back to 2
        self.play(FadeOut(labR))
        self.play(hr.animate.set_value(0), run_time=3)
        self.wait(1)
        self.play(hr.animate.set_value(-1.5), run_time=1.5)
        self.wait(1)
        self.play(hr.animate.set_value(9), run_time=2)
        self.play(Flash(axesR.c2p(-3, 9), color=GREEN), Flash(axesR.c2p(3, 9), color=GREEN), FadeIn(labR))

        solLab_l = MathTex("x=-3", color=GREEN).scale(0.75)
        solLab_l.next_to(axesR.c2p(-3, 0), DOWN, buff=0.3)
        solLab_r = MathTex("x=3", color=GREEN).scale(0.75)
        solLab_r.next_to(axesR.c2p(3, 0), DOWN, buff=0.3)
        self.play(Write(solLab_l), Write(solLab_r))

        # FINAL FROZEN IMAGE — hold, then fade
        self.wait(3)
        lineR.clear_updaters()
        dotsR.clear_updaters()
        self.play(
            *[FadeOut(m) for m in [axesL, lineL, targL, dotL, labL, axesR, curveR, lineR, dotsR, labR, solLab_l, solLab_r]],
            run_time=2,
        )
        self.wait(1)
