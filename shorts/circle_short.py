import numpy as np
from manim import *

from shorts.shorts_template import ShortScene, apply_vertical_config

apply_vertical_config()


class CircleArcLength(ShortScene):
    SPEED = 1.2
    VOLUME = 1.1

    def construct(self):
        BLUE_MAIN = BLUE
        RED_MAIN = RED

        # Initial Positions
        TOP_Y = 6.5
        HERO_Y = 0.5  # Starts lower, will be shifted up later
        DERIV_START_Y = -1.0  # Safely below the shifted diagram
        LINE_BUFF = 0.6  # Spacing between stacked formulas

        title = Text("Arc length of a circle", font_size=55, weight=BOLD).move_to(UP * TOP_Y)

        axes = Axes(
            x_range=[-2.8, 2.8],
            y_range=[-2.8, 2.8],
            x_length=5.0,
            y_length=5.0,
            axis_config={"stroke_width": 2, "color": GREY, "include_tip": True},
        ).move_to(UP * HERO_Y)

        labels = VGroup(
            MathTex("x").next_to(axes.x_axis.get_end(), RIGHT),
            MathTex("-x").next_to(axes.x_axis.get_start(), LEFT),
            MathTex("y").next_to(axes.y_axis.get_end(), UP),
            MathTex("-y").next_to(axes.y_axis.get_start(), DOWN),
        ).set_color(GREY)

        R = 2.0
        circle = Circle(radius=R, color=BLUE_MAIN, stroke_width=4).move_to(axes.c2p(0, 0))

        # Radius line and label for initial intro
        radius_intro_line = Line(axes.c2p(0, 0), axes.c2p(R, 0), color=RED_MAIN, stroke_width=3)
        r_label = MathTex("R", font_size=32, color=RED_MAIN).next_to(radius_intro_line, DOWN, buff=0.1)

        diagram_group = VGroup(axes, labels, circle)

        # --- FAST CIRCLE INTRODUCTION ---
        with self.voiceover(text="Consider a circle of radius R centered at the origin.") as tracker:
            self.play(FadeIn(title), FadeIn(diagram_group, run_time=0.6))
            self.play(Create(radius_intro_line), Write(r_label), run_time=max(0.1, tracker.duration - 0.6))

        # --- LAYOUT SHIFT ---
        self.play(
            FadeOut(title), FadeOut(radius_intro_line), FadeOut(r_label), diagram_group.animate.shift(UP * 2.0), run_time=1.2
        )

        # --- POINT, ANGLE & POSITION VECTOR SETUP ---
        t0 = PI / 3
        center = circle.get_center()
        pt_coord = center + np.array([R * np.cos(t0), R * np.sin(t0), 0])
        dot = Dot(pt_coord, color=RED_MAIN)

        # Position Vector (Arrow)
        radius_vec = Arrow(center, pt_coord, buff=0, color=RED_MAIN, stroke_width=4, max_tip_length_to_length_ratio=0.15)

        # Angle t arc from x-axis
        line_x = Line(center, center + RIGHT * 1.5)
        angle_arc = Angle(line_x, radius_vec, radius=0.6, color=BLACK)
        angle_label = MathTex("t", font_size=32, color=BLACK).next_to(angle_arc, RIGHT, buff=0.05).shift(UP * 0.1)

        with self.voiceover(
            text="We pick a point on the circle, drawing a position vector r at an angle t from the x axis."
        ) as tracker:
            self.play(Create(radius_vec), FadeIn(dot), Create(angle_arc), Write(angle_label), run_time=tracker.duration)

        # --- FORMULA & COMPONENTS WITH BOOKMARKS ---
        formula = MathTex(r"\vec r(t) = (", r"R\cos t", r",", r"R\sin t", r")", font_size=45).move_to(UP * TOP_Y)

        # Projection lines on graph for geometric visual feedback
        x_proj_pt = center + np.array([R * np.cos(t0), 0, 0])
        x_proj = Line(center, x_proj_pt, color=BLUE, stroke_width=4)
        y_proj = Line(x_proj_pt, pt_coord, color=BLUE, stroke_width=4)

        # Formula appears
        with self.voiceover(text="The position vector r of t is given by the following equation.") as tracker:
            self.play(Write(formula), run_time=tracker.duration)

        # x component
        with self.voiceover(text="The x component is R cosine t.") as tracker:
            self.play(
                formula[1].animate.set_color(BLUE),
                Create(x_proj),
                run_time=tracker.duration,
            )

        # y component
        with self.voiceover(text="The y component is R sine t.") as tracker:
            self.play(
                formula[3].animate.set_color(BLUE),
                Create(y_proj),
                run_time=tracker.duration,
            )

        # Arc length element ds
        small_arc = Arc(radius=R, arc_center=center, start_angle=t0, angle=0.2, color=RED_MAIN, stroke_width=6)
        ds_label = MathTex("ds", color=RED_MAIN, font_size=40).next_to(small_arc, UR, buff=0.1)

        with self.voiceover(text="The length of a tiny movement along the curve is d s.") as tracker:
            self.play(Create(small_arc), Write(ds_label), run_time=tracker.duration)

        # --- DERIVATION PART 1: Velocity and Magnitude ---

        step_ds = MathTex(r"ds = |\vec v(t)| dt", font_size=40).move_to(UP * DERIV_START_Y)
        with self.voiceover(
            text="This tiny distance is simply the velocity at that point times the small time d t."
        ) as tracker:
            self.play(Write(step_ds), run_time=tracker.duration)

        step_v = MathTex(r"\vec v(t) = \vec r'(t) = (-R\sin t, R\cos t)", font_size=40).next_to(
            step_ds, DOWN, buff=LINE_BUFF
        )
        with self.voiceover(
            text="Velocity is the derivative of position, r prime of t, which gives us minus R sine t and R cosine t."
        ) as tracker:
            self.play(Write(step_v), run_time=tracker.duration)

        # Base magnitude formula
        step_mag_1 = MathTex(r"|\vec v(t)| = \sqrt{(-R\sin t)^2 + (R\cos t)^2}", font_size=40).next_to(
            step_v, DOWN, buff=LINE_BUFF
        )
        with self.voiceover(text="The magnitude of velocity is the square root of the sum of squares.") as tracker:
            self.play(Write(step_mag_1), run_time=tracker.duration)

        # Factoring out R^2
        step_mag_2 = MathTex(r"|\vec v(t)| = \sqrt{R^2(\sin^2 t + \cos^2 t)}", font_size=40).move_to(
            step_mag_1, aligned_edge=LEFT
        )
        with self.voiceover(text="We expand and factor out the R squared.") as tracker:
            self.play(TransformMatchingShapes(step_mag_1, step_mag_2), run_time=tracker.duration)

        # Applying trig identity
        step_mag_3 = MathTex(r"|\vec v(t)| = \sqrt{R^2(1)}", font_size=40).move_to(step_mag_2, aligned_edge=LEFT)
        with self.voiceover(text="Since sine squared plus cosine squared is one, we swap that part for a one.") as tracker:
            self.play(TransformMatchingShapes(step_mag_2, step_mag_3), run_time=tracker.duration)

        # Final conclusion for velocity
        step_r = MathTex(r"|\vec v(t)| = R", font_size=45).move_to(step_mag_3, aligned_edge=LEFT)
        with self.voiceover(text="Which simply gives us a velocity magnitude of R.") as tracker:
            self.play(TransformMatchingShapes(step_mag_3, step_r), run_time=tracker.duration)

        # --- DERIVATION PART 2: Clear old derivations, move conclusion up, start Integration ---

        self.play(
            FadeOut(VGroup(step_ds, step_v, x_proj, y_proj)),
            step_r.animate.move_to(UP * DERIV_START_Y).scale(0.85).set_color(BLACK),
            run_time=1.5,
        )

        step_int_1 = MathTex(r"L = \int_0^{2\pi} |\vec v(t)| dt", font_size=40).next_to(step_r, DOWN, buff=0.8)
        with self.voiceover(
            text="To find the total arc length, we integrate the velocity magnitude from zero to two pi."
        ) as tracker:
            self.play(Write(step_int_1), run_time=tracker.duration)

        step_int_2 = MathTex(r"L = \int_0^{2\pi} R \, dt", font_size=40).next_to(step_int_1, DOWN, buff=LINE_BUFF)
        with self.voiceover(text="Substituting our result, we integrate R with respect to t.") as tracker:
            self.play(Write(step_int_2), run_time=tracker.duration)

        step_int_3 = MathTex(r"L = R \int_0^{2\pi} dt", font_size=40).move_to(step_int_2, aligned_edge=LEFT)
        with self.voiceover(
            text="Since the radius R is a constant, we can pull it completely outside the integral."
        ) as tracker:
            self.play(TransformMatchingShapes(step_int_2, step_int_3), run_time=tracker.duration)

        step_int_4 = MathTex(r"L = R \Big[ t \Big]_0^{2\pi}", font_size=40).move_to(step_int_3, aligned_edge=LEFT)
        with self.voiceover(text="The integral of d t is simply t, evaluated from zero to two pi.") as tracker:
            self.play(TransformMatchingShapes(step_int_3, step_int_4), run_time=tracker.duration)

        step_int_5 = MathTex(r"L = R (2\pi - 0)", font_size=40).move_to(step_int_4, aligned_edge=LEFT)
        with self.voiceover(text="Plugging in our limits, we get two pi minus zero.") as tracker:
            self.play(TransformMatchingShapes(step_int_4, step_int_5), run_time=tracker.duration)

        final_answer = MathTex(r"L = 2\pi R", font_size=55, color=RED_MAIN).move_to(step_int_5, aligned_edge=LEFT)
        with self.voiceover(text="Leaving us with the final answer. The circumference of a circle is two pi R.") as tracker:
            self.play(TransformMatchingShapes(step_int_5, final_answer), run_time=tracker.duration)

        # --- SURROUNDING RECTANGLE HIGHLIGHT ---
        self.box_final(final_answer, color=RED_MAIN)
        self.wait(1.5)
