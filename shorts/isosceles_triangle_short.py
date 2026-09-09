import numpy as np
from manim import *

from shorts.shorts_template import ShortScene


class IsoscelesAreaShort(ShortScene):
    SPEED = 1.15
    VOLUME = 1.1

    def construct(self):
        self.camera.frame.set(width=7, height=12)

        # ===============================
        # Colors
        # ===============================

        BLUE_MAIN = BLUE
        RED_UNKNOWN = RED
        TEAL_LINE = TEAL

        # ===============================
        # Layout
        # ===============================

        GOAL_POS = UP * 4.6
        HERO_POS = DOWN * 0.2

        ACTIVE_EQ_POS = DOWN * 2.8

        # ===============================
        # Goal
        # ===============================

        goal = VGroup(MathTex(r"A=\frac12bh"), MathTex(r"h=?", color=RED_UNKNOWN))

        goal.arrange(DOWN, buff=0.15)

        goal.scale(0.9)
        goal.move_to(GOAL_POS)

        # ===============================
        # Triangle
        # ===============================

        side = 3
        base = 3.6

        h_value = np.sqrt(side**2 - (base / 2) ** 2)

        B = LEFT * base / 2 + DOWN + HERO_POS
        C = RIGHT * base / 2 + DOWN + HERO_POS
        A = UP * h_value + DOWN + HERO_POS
        D = DOWN + HERO_POS

        triangle = Polygon(B, C, A, fill_color=BLUE_MAIN, fill_opacity=0.35, stroke_color=BLUE_MAIN, stroke_width=5)

        label_a_left = MathTex("a").move_to((A + B) / 2 + LEFT * 0.25)

        label_a_right = MathTex("a").move_to((A + C) / 2 + RIGHT * 0.25)

        label_b = MathTex("b").move_to((B + C) / 2 + DOWN * 0.25)

        hero = VGroup(triangle, label_a_left, label_a_right, label_b)

        # ===============================
        # Intro
        # ===============================

        grid = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-12, 12, 1],
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.7,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )

        self.add(grid)

        with self.voiceover(
            text=("We need the area of this isosceles triangle. The base is known, but the height is missing.")
        ) as tracker:
            self.play(Write(goal), Create(hero), run_time=tracker.duration / 2)

        # ===============================
        # Altitude
        # ===============================

        altitude = DashedLine(A, D, color=TEAL_LINE, stroke_width=4)

        # black label
        height_label = MathTex("h").move_to((A + D) / 2 + RIGHT * 0.25)

        with self.voiceover(
            text=("Draw the altitude from the top vertex to the middle of the base. This creates a right triangle.")
        ) as tracker:
            self.play(Create(altitude), Write(height_label), run_time=tracker.duration)

        # ===============================
        # Focus right half
        # ===============================

        right_triangle = Polygon(D, C, A, fill_color=BLUE_MAIN, fill_opacity=0.45, stroke_color=BLUE_MAIN)
        right_angle = RightAngle(Line(D, C), Line(D, A), quadrant=(1, 1), length=0.2, color=BLUE)

        # fade unused left half strongly
        faded_left = Polygon(B, D, A, fill_color=BLUE_MAIN, fill_opacity=0.05, stroke_color=BLUE_MAIN, stroke_opacity=0.1)

        with self.voiceover(text=("Both halves are identical, so we only need the right triangle.")) as tracker:
            self.play(
                FadeIn(right_triangle),
                FadeIn(right_angle),
                FadeIn(faded_left),
                triangle.animate.set_opacity(0.05),
                label_a_left.animate.set_opacity(0.2),
                label_b.animate.set_opacity(0.2),
                run_time=tracker.duration,
            )

        # ===============================
        # Move hero upward
        # ===============================

        shift = UP * 1.1

        self.play(
            hero.animate.shift(shift),
            altitude.animate.shift(shift),
            height_label.animate.shift(shift),
            right_triangle.animate.shift(shift),
            right_angle.animate.shift(shift),
            faded_left.animate.shift(shift),
        )

        C2 = C + shift
        D2 = D + shift

        # labels
        half_base = MathTex(r"\frac b2").move_to((D2 + C2) / 2 + DOWN * 0.25)

        self.play(Write(half_base))

        # ===============================
        # Derivation manager
        # ===============================

        active_derivation = None

        def show_derivation(eq):

            nonlocal active_derivation

            if active_derivation:
                self.play(FadeOut(active_derivation, shift=UP * 0.2), run_time=0.25)

            eq.move_to(ACTIVE_EQ_POS)

            self.play(Write(eq), run_time=0.5)

            active_derivation = eq

        # ===============================
        # Pythagoras
        # ===============================

        pythagoras = MathTex(r"a^2=\left(\frac b2\right)^2+h^2")

        with self.voiceover(text=("From the Pythagoras formula -a- squared equals b over two squared plus h squared.")):
            show_derivation(pythagoras)

        height_formula = MathTex(r"h=\sqrt{a^2-\left(\frac b2\right)^2}")

        with self.voiceover(text=("Solving for H gives: H equals the square root of -a- squared minus B over two squared.")):
            show_derivation(height_formula)

        final_height = MathTex(r"h=\frac{\sqrt{4a^2-b^2}}2")

        with self.voiceover(
            text=("Simplifying the height gives square root of 4A squared minus B squared, divided by two.")
        ):
            show_derivation(final_height)

        # ===============================
        # Area substitution
        # ===============================

        area_formula = MathTex(r"A=\frac12b\left(\frac{\sqrt{4a^2-b^2}}2\right)")

        with self.voiceover(text=("Substituting this height into the area formula gives the area.")):
            show_derivation(area_formula)

        answer = MathTex(r"A=\frac{b\sqrt{4a^2-b^2}}4")

        answer.move_to(ACTIVE_EQ_POS + DOWN * 0.8)

        box = SurroundingRectangle(answer, color=BLUE)
        with self.voiceover(text=("which is b times square root of 4a squared minus b squared upon four.")):
            self.play(FadeOut(area_formula))
            self.play(Write(answer), Create(box))

        self.wait(2)
