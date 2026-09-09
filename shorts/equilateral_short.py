from manim import *

from shorts.shorts_template import ShortScene


class EquilateralTriangleAreaShort(ShortScene):
    """
    Equilateral Triangle Area Formula Short

    Flow:
    1. What is the area?
    2. Show area formula
    3. Find height by splitting triangle
    4. Use Pythagoras
    5. Substitute height
    6. Final formula
    """

    SPEED = 1.15
    VOLUME = 1.0

    def construct(self):
        self.camera.frame.set(width=7, height=12)

        TITLE = UP * 4.7
        DIAGRAM = UP * 0.4
        EQUATION = DOWN * 3.8

        # =====================================================
        # SCENE 1: HOOK
        # =====================================================

        title = Text("What is the area of\nan equilateral triangle?", font_size=34, weight=BOLD).move_to(TITLE)

        A = UP * 2 + DIAGRAM
        B = LEFT * 2 + DOWN * 1 + DIAGRAM
        C = RIGHT * 2 + DOWN * 1 + DIAGRAM

        triangle = Polygon(B, C, A, fill_color=BLUE, fill_opacity=0.45, stroke_color=BLUE, stroke_width=6)

        side_left = MathTex("a").next_to(Line(B, A).get_center(), LEFT)
        side_right = MathTex("a").next_to(Line(A, C).get_center(), RIGHT)
        side_bottom = MathTex("a").next_to(Line(B, C).get_center(), DOWN)

        labels = VGroup(side_left, side_right, side_bottom)

        with self.voiceover(text="What is the area of an equilateral triangle? Every side has length a.") as tracker:
            self.play(Write(title), FadeIn(triangle), Write(labels), run_time=tracker.duration)

        # =====================================================
        # SCENE 2: AREA FORMULA
        # =====================================================

        area_formula = MathTex(r"A=\frac12 bh", font_size=48).move_to(EQUATION)

        with self.voiceover(text="The area of any triangle is one half times base times height.") as tracker:
            self.play(Write(area_formula), run_time=tracker.duration)

        self.wait(0.5)

        self.play(FadeOut(area_formula), run_time=0.5)

        # =====================================================
        # SCENE 3: SPLIT TRIANGLE
        # =====================================================

        D = DOWN * 1 + DIAGRAM

        height_line = DashedLine(A, D, color=RED, stroke_width=6)

        left_half_label = MathTex(r"\frac a2", color=RED).next_to(Line(B, D), DOWN)

        right_half_label = MathTex(r"\frac a2", color=RED).next_to(Line(D, C), DOWN)

        h_label = MathTex("h", color=RED).next_to(height_line, RIGHT)

        with self.voiceover(
            text="To find the height, split the triangle in half. The base becomes two equal parts, each a over two."
        ) as tracker:
            self.play(
                Create(height_line),
                Write(left_half_label),
                Write(right_half_label),
                Write(h_label),
                run_time=tracker.duration,
            )

        # =====================================================
        # SCENE 4: RIGHT TRIANGLE + PYTHAGORAS
        # =====================================================

        right_triangle = Polygon(B, D, A, fill_color=BLUE, fill_opacity=0.35, stroke_color=BLUE, stroke_width=4)

        self.play(
            FadeOut(triangle),
            FadeOut(side_left),
            FadeOut(side_right),
            FadeOut(side_bottom),
            FadeOut(right_half_label),
            FadeIn(right_triangle),
            run_time=0.8,
        )

        hyp_label = MathTex("a").next_to(Line(B, A), LEFT)

        pythagoras = MathTex(r"a^2=h^2+\left(\frac a2\right)^2", font_size=42).move_to(EQUATION)

        with self.voiceover(
            text="Now we have a right triangle. Using Pythagoras, the hypotenuse squared equals the two sides squared."
        ) as tracker:
            self.play(Write(hyp_label), Write(pythagoras), run_time=tracker.duration)

        # Solve height

        height_result = MathTex(r"h=\frac{\sqrt3}{2}a", font_size=50, color=RED).move_to(EQUATION)

        with self.voiceover(text="Solving for the height gives root three over two times a.") as tracker:
            self.play(FadeOut(pythagoras), run_time=0.5)

            self.wait(0.2)

            self.play(Write(height_result), run_time=tracker.duration - 0.7)

        # =====================================================
        # SCENE 5: FINAL FORMULA
        # =====================================================

        substitution = MathTex(r"A=\frac12 a\left(\frac{\sqrt3}{2}a\right)", font_size=42).move_to(EQUATION)

        final = MathTex(r"\boxed{A=\frac{\sqrt3}{4}a^2}", font_size=58, color=RED).move_to(EQUATION)

        with self.voiceover(text="Put the height into the area formula, and simplify.") as tracker:
            self.play(FadeOut(height_result), run_time=0.5)

            self.wait(0.2)

            self.play(Write(substitution), run_time=tracker.duration - 0.7)

        self.wait(0.5)

        with self.voiceover(text="The area of an equilateral triangle is root three over four times a squared.") as tracker:
            self.play(FadeOut(substitution), run_time=0.5)

            self.wait(0.2)

            self.play(Write(final), run_time=tracker.duration - 0.7)

        self.wait(3)
