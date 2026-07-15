import numpy as np
from manim import *
from manim_themes.manim_theme import apply_theme


class PiIntroduction(MovingCameraScene):
    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):

        # =========================================================
        # TITLE
        # =========================================================

        title = Text("What is Pi?", font_size=64, weight=BOLD)
        self.play(Write(title))
        self.wait(1.5)
        self.play(FadeOut(title))

        # =========================================================
        # ENVIRONMENT
        # =========================================================
        grid = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-12, 12, 1],
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )
        self.add(grid)

        # =========================================================
        # 1. SET UP THE GROWABLE GEOMETRY
        #    `d_tracker` holds the TRUE diameter (1 at the start), which is
        #    what every label reads from — so the math stays honest (a
        #    diameter of 1 really does give a circumference of pi).
        #    SCALE inflates only the on-screen geometry, so the circle
        #    reads as a comfortable size without touching any numbers.
        #    Everything is a pure function of d_tracker, so one
        #    ValueTracker animation later can grow OR shrink the whole
        #    diagram — circle, guides, arrow, both labels, the unwrapped
        #    line, and eventually the ratio readout — all in sync.
        # =========================================================
        d_tracker = ValueTracker(1.0)  # true diameter; starts at 1
        SCALE = 1.8  # visual-only inflation factor

        CENTER = np.array([0.0, 1.3, 0.0])
        ARROW_Y = CENTER[1] - SCALE * 1.0 - 0.35  # clears the circle even at max size (true r = 1)
        DLABEL_Y = ARROW_Y - 0.45
        FLAT_Y = DLABEL_Y - 1.0
        CLABEL_Y = FLAT_Y - 0.55
        RATIO_Y = CLABEL_Y - 0.65

        def true_diam():
            return d_tracker.get_value()

        def true_radius():
            return true_diam() / 2

        def true_circumference():
            return true_diam() * PI

        def vis_radius():
            return SCALE * true_radius()

        def vis_circumference():
            return SCALE * true_circumference()

        # =========================================================
        # 2. CIRCLE, CENTER, AND DIAMETER GUIDES
        # =========================================================
        circle = always_redraw(lambda: Circle(radius=vis_radius(), color=BLUE, stroke_width=4).move_to(CENTER))
        center_dot = Dot(CENTER, color=RED, radius=0.03)

        self.play(Create(circle), FadeIn(center_dot))

        left_line = always_redraw(
            lambda: DashedLine(
                [CENTER[0] - vis_radius(), CENTER[1] + 0.1, 0],
                [CENTER[0] - vis_radius(), ARROW_Y, 0],
                color=BLUE,
            )
        )
        right_line = always_redraw(
            lambda: DashedLine(
                [CENTER[0] + vis_radius(), CENTER[1] + 0.1, 0],
                [CENTER[0] + vis_radius(), ARROW_Y, 0],
                color=BLUE,
            )
        )
        self.play(Create(left_line), Create(right_line))

        # =========================================================
        # 3. DIAMETER ARROW + LABEL
        # =========================================================
        diameter_arrow = always_redraw(
            lambda: DoubleArrow(
                start=[CENTER[0] - vis_radius(), ARROW_Y, 0],
                end=[CENTER[0] + vis_radius(), ARROW_Y, 0],
                buff=0,
            )
        )

        diameter_label = always_redraw(
            lambda: (
                VGroup(
                    Text("d \u2248 ", font_size=32),
                    DecimalNumber(true_diam(), num_decimal_places=2, font_size=32),
                )
                .arrange(RIGHT, buff=0.05)
                .move_to([CENTER[0], DLABEL_Y, 0])
            )
        )

        self.play(FadeIn(diameter_arrow), Write(diameter_label))
        self.wait()

        term_d = Text("Diameter (d) = width of a circle", font_size=25).to_edge(RIGHT + UP)
        self.play(Write(term_d))
        self.wait(1.5)
        self.play(FadeOut(term_d))

        # VGroup(term_c, term_d).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        # =========================================================
        # 4. UNWRAP THE CIRCUMFERENCE
        # =========================================================
        circumference_static = circle.copy()

        flat_line_static = Line(
            [-vis_circumference() / 2, FLAT_Y, 0],
            [vis_circumference() / 2, FLAT_Y, 0],
            color=BLUE,
        )

        self.play(
            Transform(circumference_static, flat_line_static),
            run_time=2,
        )

        term_c = Text("Circumference (C) = perimeter of a circle", font_size=25).to_edge(RIGHT + UP)
        self.play(Write(term_c))
        self.wait(1)
        self.play(FadeOut(term_c))
        self.wait(0.3)

        self.remove(circumference_static)

        # From here on the unwrapped line is itself a live function of
        # d_tracker, so it can grow or shrink later along with everything else.
        flat_line = always_redraw(
            lambda: Line(
                [-vis_circumference() / 2, FLAT_Y, 0],
                [vis_circumference() / 2, FLAT_Y, 0],
                color=BLUE,
                stroke_width=4,
            )
        )
        self.add(flat_line)

        # =========================================================
        # 5. LABEL THE CIRCUMFERENCE — BRACE + P ≈ 3.14
        # =========================================================
        brace = always_redraw(
            lambda: Brace(
                Line([-vis_circumference() / 2, FLAT_Y, 0], [vis_circumference() / 2, FLAT_Y, 0]),
                direction=DOWN,
                color=GREY_D,
                buff=0.15,
            )
        )

        circumference_label = always_redraw(
            lambda: (
                VGroup(
                    Text("C \u2248 ", font_size=32),
                    DecimalNumber(true_circumference(), num_decimal_places=2, font_size=32),
                )
                .arrange(RIGHT, buff=0.05)
                .move_to([0, CLABEL_Y, 0])
            )
        )

        self.play(FadeIn(brace), Write(circumference_label))
        self.wait(1.5)

        # =========================================================
        # 6. GROW THE CIRCLE — DIAMETER 1 → 2
        #    Every mobject above is already wired to d_tracker, so this
        #    single animation grows the circle, slides the guides and
        #    arrow outward, ticks both numeric labels upward, and
        #    stretches the unwrapped line — all in sync.
        # =========================================================
        self.wait(0.5)
        self.play(
            self.camera.frame.animate.scale(1.2),
            d_tracker.animate.set_value(2.0),
            run_time=4,
            rate_func=smooth,
        )
        self.wait(2)

        # =========================================================
        # 7. THE RATIO — P / D = pi, no matter the size
        # =========================================================
        def ratio_row():
            C = true_circumference()
            d = true_diam()
            bar = Line(LEFT * 0.55, RIGHT * 0.55, stroke_width=3)
            num = DecimalNumber(C, num_decimal_places=2, font_size=30).next_to(bar, UP, buff=0.06)
            den = DecimalNumber(d, num_decimal_places=2, font_size=30).next_to(bar, DOWN, buff=0.06)
            frac = VGroup(bar, num, den)
            # Use f-strings to inject the rounded values directly into a single Tex object
            row = MathTex(r"\frac{C}{d} = \frac{" f"{C:.2f}" r"}{" f"{d:.2f}" r"} = 3.14", font_size=32)
            row.next_to(circle, RIGHT, buff=1.2)
            return row

        ratio_display = always_redraw(ratio_row)
        self.play(Write(ratio_display))
        self.wait(2)

        # =========================================================
        # 8. SHRINK BACK — DIAMETER 2 → 1
        #    P and D both fall as the circle shrinks, but their ratio
        #    in the readout above stays locked on pi the whole time.
        # =========================================================
        self.play(d_tracker.animate.set_value(1.0), self.camera.frame.animate.scale(1 / 1.2), run_time=4, rate_func=smooth)
        self.wait(2)

        # =========================================================
        # 9. CLEAR THE DIAGRAM
        # =========================================================
        diagram_group = VGroup(
            circle,
            center_dot,
            left_line,
            right_line,
            diameter_arrow,
            diameter_label,
            flat_line,
            brace,
            circumference_label,
            ratio_display,
        )
        self.play(FadeOut(diagram_group), FadeOut(grid), run_time=1.5)
        self.wait(0.3)

        # =========================================================
        # 10. THE MATHEMATICIAN NAMES IT
        # =========================================================
        mathematician = ImageMobject("./assets/william-jones.png")
        mathematician.scale_to_fit_height(4.5)
        mathematician.to_edge(LEFT, buff=1.0)

        self.play(FadeIn(mathematician), run_time=1)
        self.wait(0.3)

        bubble = RoundedRectangle(
            width=6.6,
            height=3.0,
            corner_radius=0.3,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=0.95,
            stroke_color=BLACK,
            stroke_width=2,
        )
        bubble.next_to(mathematician, RIGHT, buff=1.1).shift(UP * 1.0)

        # Approximate aim point near the character's head — nudge this once
        # the real image is in place and its proportions are known.
        tail_tip = mathematician.get_center() + UP * 1.2 + RIGHT * 0.2
        tail = Polygon(
            bubble.get_left() + UP * 0.35,
            bubble.get_left() + DOWN * 0.35,
            tail_tip,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=0.95,
            stroke_color=BLACK,
            stroke_width=2,
        )

        self.play(Create(bubble), Create(tail), run_time=0.8)

        speech_text = Text(
            "Let's call this ratio of the\nCircumference of a circle to its width...\nPi (\u03c0).",
            font_size=25,
            color=BLACK,
            line_spacing=1.3,
        ).move_to(bubble.get_center())

        self.play(Write(speech_text))
        self.wait(2)

        footnote = (
            Text(
                'Pi is just "P" in Greek.',
                font_size=24,
                slant=ITALIC,
            )
            .next_to(bubble, DOWN, buff=0.4)
            .align_to(bubble, LEFT)
        )

        self.play(Write(footnote))
        self.wait(2)

        # =========================================================
        # 11. CONCLUSION
        # =========================================================
        char_group = Group(mathematician, bubble, tail, speech_text, footnote)
        self.play(FadeOut(char_group), run_time=1.5)
        self.wait(0.3)

        conclusion_1 = Text(
            "Pi is the perimeter(circumference) of a circle\nwhose width is 1 unit.",
            font_size=36,
            weight=BOLD,
            line_spacing=1.3,
        ).move_to(UP * 0.6)

        conclusion_2 = Text(
            "It's also expressed as the ratio of\nthe circumference and diameter of a circle.",
            font_size=30,
            line_spacing=1.3,
        ).next_to(conclusion_1, DOWN, buff=0.6)

        self.play(Write(conclusion_1))
        self.wait(1.5)
        self.play(Write(conclusion_2))
        self.wait(3)

        # =========================================================
        # 12. TECHNICAL VOCABULARY
        # =========================================================
        self.play(FadeOut(conclusion_1), FadeOut(conclusion_2), run_time=1)
        self.wait(0.3)

        # =========================================================
        # 13. A CIRCLE OF DIAMETER D
        # =========================================================
        CIRCLE_CENTER2 = RIGHT * 3.3 + UP * 1.8
        CIRCLE_R = 1.4
        TEXT_X = -3.3

        circle2 = Circle(radius=CIRCLE_R, color=BLUE, stroke_width=4).move_to(CIRCLE_CENTER2)
        diam_line2 = Line(CIRCLE_CENTER2 + LEFT * CIRCLE_R, CIRCLE_CENTER2 + RIGHT * CIRCLE_R, color=BLUE, stroke_width=2)
        d_label2 = MathTex("d", font_size=32).next_to(diam_line2, UP, buff=0.1)

        self.play(Create(circle2))
        self.play(Create(diam_line2), Write(d_label2))
        self.wait(1)

        intro_line1 = Text("If d is known, C can be calculated as:", font_size=26).move_to([TEXT_X, 1.9, 0])
        formula_C_D = MathTex("C", "=", "\\pi", "d", font_size=40).move_to([TEXT_X, 1.2, 0])

        self.play(Write(intro_line1))
        self.play(Write(formula_C_D))
        self.wait(2)

        # =========================================================
        # 14. INTRODUCING RADIUS
        # =========================================================
        radius_transition = Text("But mathematicians like to use radius instead:", font_size=24).move_to([TEXT_X, 0.2, 0])
        self.play(Write(radius_transition))
        self.wait(1.5)
        self.play(FadeOut(radius_transition))

        radius_def = Text(
            "Radius (r) = distance from the center\nto a point on the circle.",
            font_size=24,
            line_spacing=1.2,
        ).move_to([TEXT_X, 0.2, 0])

        point_on_circle = CIRCLE_CENTER2 + CIRCLE_R * np.array([np.cos(40 * DEGREES), np.sin(40 * DEGREES), 0])
        radius_line2 = Line(CIRCLE_CENTER2, point_on_circle, color=RED, stroke_width=3)
        r_label2 = MathTex("r", font_size=30).move_to(CIRCLE_CENTER2 + (point_on_circle - CIRCLE_CENTER2) * 0.55 + UP * 0.2)

        self.play(Write(radius_def), Create(radius_line2))
        self.play(Write(r_label2))
        self.wait(1.5)

        formula_d_2r = MathTex("d = 2r", font_size=40).move_to([TEXT_X, -0.7, 0])
        self.play(Write(formula_d_2r))
        self.wait(1)

        circle_figure = VGroup(circle2, diam_line2, d_label2, radius_line2, r_label2)
        self.play(FadeOut(radius_def), FadeOut(intro_line1), FadeOut(circle_figure), run_time=1)
        self.wait(0.3)

        # =========================================================
        # 15. COMBINING INTO THE FINAL FORMULA
        # =========================================================
        self.play(
            formula_C_D.animate.move_to(UP * 0.6),
            formula_d_2r.animate.move_to(DOWN * 0.3),
            run_time=1,
        )
        self.wait(0.5)

        combined = MathTex("C", "=", "\\pi", "2r", font_size=42).move_to(ORIGIN)
        self.play(TransformMatchingTex(Group(formula_C_D, formula_d_2r), combined), FadeOut(formula_d_2r), run_time=1.3)
        self.wait(1)

        final_formula = MathTex("Circumference", "=", "2", "\\pi", "r", font_size=52).move_to(ORIGIN)

        self.play(TransformMatchingTex(combined, final_formula), run_time=1.2)
        self.wait(0.5)

        final_box = SurroundingRectangle(final_formula, color=BLUE, buff=0.25, corner_radius=0.1)
        self.play(Create(final_box))
        self.wait(3)


class CircleArea(MovingCameraScene):
    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):

        # =========================================================
        # TITLE
        # =========================================================
        title = Text("Area of a Circle", font_size=56, weight=BOLD)

        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # =========================================================
        # 1. ENVIRONMENT & GRID SETUP
        # =========================================================
        grid = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-12, 12, 1],
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )
        self.add(grid)

        RADIUS = 2.3
        # Circle sits in the upper-left; wedges/row/rectangle live to the
        # right and lower down, so the two never overlap.
        CENTER = grid.c2p(-4.0, 3.2)
        ROW_ORIGIN = grid.c2p(1.5, -2.6)  # baseline the wedge strip/row/rectangle sit on

        def make_wedges(n, fill_color=BLUE, fill_opacity=0.5, stroke_color=BLUE_E):
            """n equal circular sectors ('wedges') that together make up the
            whole circle, starting at angle 0 and sweeping counter-clockwise.
            Each wedge's apex sits exactly at CENTER."""
            wedge_angle = TAU / n
            wedges = VGroup()
            for i in range(n):
                sector = Sector(
                    radius=RADIUS,
                    angle=wedge_angle,
                    start_angle=i * wedge_angle,
                    fill_color=fill_color,
                    fill_opacity=fill_opacity,
                    stroke_color=stroke_color,
                    stroke_width=2,
                ).shift(CENTER)
                wedges.add(sector)
            return wedges

        def arrange_wedges_in_row(n, wedges, row_origin, interlock=True):
            """Target layout for the n wedges, all lined up so consecutive wedges
            share a full straight edge (no gaps, no overlap).

            interlock=False: every wedge keeps its natural apex-down orientation
            -> flat saw-tooth comb. Adjacent teeth meet at their arc-tip vertices;
            apex spacing is the full chord width.

            interlock=True: every other wedge is flipped apex-up and folded in
            to interlock with its neighbors. Each wedge only advances HALF the
            chord width before the next starts, and flipped wedges sit at height
            R*cos(half_angle) above the baseline (not a flat R) - that's the
            exact height that makes wedge B's apex land on wedge A's arc-tip,
            so the shared edge is literally the same segment for both wedges.
            As n grows, half_angle -> 0, cos(half_angle) -> 1, dx and dy both
            shrink, and the shape converges to a rectangle of height R.
            """
            wedge_angle = TAU / n
            half_angle = wedge_angle / 2

            if interlock:
                dx = RADIUS * np.sin(half_angle)  # half the chord width
                dy = RADIUS * np.cos(half_angle)  # exact fold-in height
            else:
                dx = 2 * RADIUS * np.sin(half_angle)  # full chord width
                dy = 0

            row = VGroup()
            for i, wedge in enumerate(wedges):
                bisector = (i + 0.5) * wedge_angle
                apex_up = interlock and (i % 2 == 1)
                target_dir = -PI / 2 if apex_up else PI / 2
                rotated = wedge.copy().rotate(target_dir - bisector, about_point=CENTER)

                target_x = row_origin[0] + (i - (n - 1) / 2) * dx
                target_y = row_origin[1] + (dy if apex_up else 0)
                shift_vec = np.array([target_x, target_y, 0]) - CENTER
                rotated.shift(shift_vec)
                row.add(rotated)
            return row

        # =========================================================
        # 2. THE CIRCLE, WITH ITS RADIUS
        # =========================================================
        circle = Circle(
            radius=RADIUS,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE_E,
            stroke_width=4,
        ).move_to(CENTER)
        self.play(
            self.camera.frame.animate.scale(1.2).move_to(circle.get_center() + DOWN),
            run_time=1.2,
        )

        self.play(FadeIn(circle), run_time=1)
        self.wait(0.3)

        radius_line = Line(CENTER, CENTER + RADIUS * RIGHT, stroke_width=4)
        radius_label = MathTex("r", font_size=32).next_to(radius_line, UP, buff=0.1)
        self.play(Create(radius_line), Write(radius_label), run_time=1)
        self.wait(1)
        self.play(FadeOut(radius_line), FadeOut(radius_label))

        # =========================================================
        # 3. CUT INTO 8 SLICES
        # =========================================================
        cut_caption = Text(
            "Cut the circle into equal wedges.",
            font_size=26,
        ).next_to(circle, DOWN, buff=0.8)
        self.play(Write(cut_caption))

        circle_wedges = make_wedges(8)
        self.play(FadeOut(circle), FadeIn(circle_wedges), run_time=1.5)
        self.wait(0.5)

        # Highlight one wedge: its two straight edges (radius) and its
        # curved outer edge (a slice of the circumference).
        wedge_angle_8 = TAU / 8
        a0, a1 = 0, wedge_angle_8

        edge_start = Line(
            CENTER,
            CENTER + RADIUS * np.array([np.cos(a0), np.sin(a0), 0]),
            stroke_width=6,
        )
        edge_end = Line(
            CENTER,
            CENTER + RADIUS * np.array([np.cos(a1), np.sin(a1), 0]),
            stroke_width=6,
        )
        arc_highlight = Arc(
            radius=RADIUS,
            start_angle=a0,
            angle=wedge_angle_8,
            arc_center=CENTER,
            stroke_width=8,
        )

        mid_angle = (a0 + a1) / 2
        r_label_1 = (
            MathTex("r", font_size=28)
            .move_to(CENTER + 0.55 * RADIUS * np.array([np.cos(a0), np.sin(a0), 0]))
            .shift(UP * 0.2)
        )
        r_label_2 = (
            MathTex("r", font_size=28)
            .move_to(CENTER + 0.55 * RADIUS * np.array([np.cos(a1), np.sin(a1), 0]))
            .shift(RIGHT * 0.25)
        )
        arc_label = Text(
            "circumference",
            font_size=20,
        ).move_to(CENTER + 1.18 * RADIUS * np.array([np.cos(mid_angle), np.sin(mid_angle), 0] + RIGHT * 0.3))

        self.play(Create(edge_start), Create(edge_end), Create(arc_highlight), run_time=1)
        self.play(Write(r_label_1), Write(r_label_2), Write(arc_label), run_time=1)
        self.wait(1.5)

        self.play(
            FadeOut(edge_start),
            FadeOut(edge_end),
            FadeOut(arc_highlight),
            FadeOut(r_label_1),
            FadeOut(r_label_2),
            FadeOut(arc_label),
            FadeOut(cut_caption),
            run_time=0.8,
        )

        # =========================================================
        # 4. LAY THE WEDGES IN A STRIP, THEN FLIP HALF TO INTERLOCK THEM
        # =========================================================
        strip_caption = Text(
            "Lay the wedges out in a strip,\nlike the teeth of a saw.",
            font_size=26,
            line_spacing=1.2,
        ).next_to(circle_wedges, DOWN, buff=0.8)

        self.play(Write(strip_caption))
        self.wait(0.5)
        self.play(FadeOut(strip_caption))

        # Single camera move for the rest of the scene: pull back so the
        # circle (top left), the wedge strip/row (right, mid-low), and the
        # derivation text that appears later all fit comfortably.
        # (Estimated for this layout - nudge scale/shift if anything clips.)
        self.play(
            self.camera.frame.animate.scale(1.3).move_to(np.array([1.3, 0, 0])),
            run_time=1.2,
        )

        # 4a. Saw-tooth strip: every wedge keeps its apex-down orientation,
        # so consecutive wedges' straight edges touch exactly.
        row_wedges = arrange_wedges_in_row(8, circle_wedges, ROW_ORIGIN, interlock=False)
        self.play(TransformFromCopy(circle_wedges, row_wedges), run_time=2)
        self.wait(1)

        # ---- Label the row: slanted radius edge + total unrolled length ----
        # Leftmost wedge's outer (unshared) straight edge runs from its apex,
        # on the baseline, up to its arc-tip - that segment is one radius.
        half_angle_8 = wedge_angle_8 / 2
        dx_flat = 2 * RADIUS * np.sin(half_angle_8)
        apex0 = np.array([ROW_ORIGIN[0] - 3.5 * dx_flat, ROW_ORIGIN[1], 0])
        left_tip0 = apex0 + RADIUS * np.array([np.cos(PI / 2 + half_angle_8), np.sin(PI / 2 + half_angle_8), 0])

        row_r_brace = BraceBetweenPoints(left_tip0, apex0)
        row_r_label = row_r_brace.get_tex("r")

        row_width_brace = Brace(row_wedges, UP, buff=0.2)
        row_width_label = row_width_brace.get_tex(r"2\pi r")

        self.play(
            FadeIn(row_r_brace),
            Write(row_r_label),
            FadeIn(row_width_brace),
            Write(row_width_label),
            run_time=1,
        )
        self.wait(1.5)
        self.play(
            FadeOut(row_r_brace),
            FadeOut(row_r_label),
            FadeOut(row_width_brace),
            FadeOut(row_width_label),
            run_time=0.6,
        )

        interlock_caption = Text(
            "Split the strip in half, flip every\nother wedge, and join them together.",
            font_size=26,
            line_spacing=1.2,
        ).next_to(row_wedges, DOWN, buff=1.5)
        self.play(Write(interlock_caption))
        self.wait(0.5)
        self.play(FadeOut(interlock_caption))

        # 4b. Flip every other wedge up so they interlock with their
        # neighbors - this is the shape that approaches a rectangle as
        # the wedge count grows.
        interlocked_wedges = arrange_wedges_in_row(8, circle_wedges, ROW_ORIGIN, interlock=True)
        self.play(Transform(row_wedges, interlocked_wedges), run_time=2)
        self.wait(1)

        # ---- Label the interlocked shape: height r, length pi*r ----
        # Folding in half halves the strip's length (2*pi*r -> pi*r) while
        # its wavy height settles toward a full radius r.
        fold_height_brace = row_r_brace.next_to(interlocked_wedges, LEFT, buff=-0.5)
        # fold_height_brace = Brace(row_wedges, buff=0.2)
        fold_height_label = fold_height_brace.get_tex("r")

        # 1. Find the absolute lowest Y-coordinate of the shape
        lowest_y = row_wedges.get_bottom()[1]

        # 2. Filter out only the wedges resting on this bottom floor
        # (We use a tiny tolerance like 0.05 to handle float variances safely)
        bottom_row = VGroup(*[wedge for wedge in row_wedges if abs(wedge.get_bottom()[1] - lowest_y) < 0.05])

        # 3. Create the brace using ONLY those bottom pieces
        fold_width_brace = Brace(bottom_row, DOWN, buff=0.2)
        fold_width_label = fold_width_brace.get_tex(r"\pi r")

        # fold_width_brace = Brace(row_wedges, DOWN, buff=0.2)
        # fold_width_label = fold_width_brace.get_tex(r"\pi r")

        self.play(
            FadeIn(fold_height_brace),
            Write(fold_height_label),
            FadeIn(fold_width_brace),
            Write(fold_width_label),
            run_time=1,
        )
        self.wait(1.5)
        self.play(
            FadeOut(fold_height_brace),
            FadeOut(fold_height_label),
            FadeOut(fold_width_brace),
            FadeOut(fold_width_label),
            run_time=0.6,
        )

        # =========================================================
        # 5. MORE SLICES — 30 WEDGES, CIRCLE AND ROW UPDATE TOGETHER
        # =========================================================
        refine_caption = Text(
            "More wedges, less waviness.",
            font_size=26,
        ).next_to(interlocked_wedges, DOWN, buff=1.5)
        self.play(Write(refine_caption))

        circle_wedges_30 = make_wedges(30)
        row_wedges_30 = arrange_wedges_in_row(30, circle_wedges_30, ROW_ORIGIN)

        self.play(
            Transform(circle_wedges, circle_wedges_30),
            Transform(row_wedges, row_wedges_30),
            run_time=2.5,
        )
        self.wait(1)

        # =========================================================
        # 6. A LOT OF SLICES — THE ROW BECOMES A RECTANGLE
        # =========================================================
        N_FINAL = 90
        circle_wedges_final = make_wedges(N_FINAL)
        row_wedges_final = arrange_wedges_in_row(N_FINAL, circle_wedges_final, ROW_ORIGIN)

        self.play(
            Transform(circle_wedges, circle_wedges_final),
            Transform(row_wedges, row_wedges_final),
            run_time=2.5,
        )
        self.wait(0.5)
        self.play(FadeOut(refine_caption))

        # Snap the (now nearly-flat) row into a perfect rectangle.
        # circle_wedges (now a fine 90-wedge circle) is left on screen as
        # a quiet reference in the corner - it is no longer faded out.
        rect_width = PI * RADIUS
        rect_height = RADIUS
        clean_rect = Rectangle(
            width=rect_width,
            height=rect_height,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE_E,
            stroke_width=4,
        ).move_to(ROW_ORIGIN + UP * (RADIUS / 2))

        self.play(
            FadeOut(circle_wedges),
            FadeIn(circle),
            ReplacementTransform(row_wedges, clean_rect),
            run_time=1.5,
        )
        self.wait(1)

        # =========================================================
        # 7. LABEL THE RECTANGLE'S SIDES
        # (No further camera move - we already zoomed out in section 4.)
        # =========================================================
        height_brace = Brace(clean_rect, direction=LEFT, color=GREY_D, buff=0.15)
        height_label = height_brace.get_tex("r").set_color(GREY_D)

        width_brace = Brace(clean_rect, direction=DOWN, color=GREY_D, buff=0.15)
        width_label = width_brace.get_tex(r"\pi r").set_color(GREY_D)

        self.play(FadeIn(height_brace), Write(height_label), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(width_brace), Write(width_label), run_time=0.8)
        self.wait(1.5)

        # =========================================================
        # 8. BUILD THE AREA FORMULA, STEP BY STEP
        # =========================================================
        diagram_group = VGroup(clean_rect, height_brace, height_label, width_brace, width_label)

        line1 = MathTex(r"\text{Area} = \text{width} \times \text{height}", font_size=40)
        line1.next_to(diagram_group, DOWN, buff=0.5).set_x(clean_rect.get_x())
        self.play(Write(line1))
        self.wait(1)

        line2 = MathTex(r"\text{Area} = (\pi r) \times r", font_size=40)
        line2.next_to(line1, DOWN, buff=0.3).set_x(clean_rect.get_x())
        self.play(Write(line2))
        self.wait(1)

        line3 = MathTex(r"\text{Area of a Circle} = \pi r^2", font_size=46)
        line3.next_to(line2, DOWN, buff=0.4).set_x(clean_rect.get_x())

        final_box = SurroundingRectangle(line3, color=BLUE, buff=0.2, corner_radius=0.1)

        final_formula_group = VGroup(final_box, line3)

        self.play(Write(line3), Create(final_box))
        self.wait(2)

        # Final show case of circle and Area formula
        self.play(
            FadeIn(radius_line, radius_label),
            FadeOut(line1, line2, diagram_group),
        )

        self.play(
            self.camera.frame.animate.scale(1 / 1.2).move_to(circle.get_right() + RIGHT),
            final_formula_group.animate.next_to(circle, RIGHT, buff=2),
        )

        self.wait(6)
