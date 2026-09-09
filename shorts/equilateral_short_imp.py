from manim import *

from shorts.shorts_template import ShortScene


class EquilateralTriangleAreaShort(ShortScene):
    SPEED = 1.15
    VOLUME = 1.0

    def construct(self):
        self.camera.frame.set(width=8)

        # ===============================
        # SHORTS LAYOUT
        # ===============================

        HOOK = UP * 3.5

        EQUATION_ZONE = RIGHT * 3.2 + DOWN * 0.2

        BLUE = ManimColor("#3B82F6")
        GREEN = ManimColor("#22C55E")
        YELLOW = ManimColor("#FACC15")
        RED = ManimColor("#EF4444")

        # ===============================
        # HOOK
        # ===============================

        hook = Text("A triangle hides a secret...", font_size=38, weight=BOLD).move_to(HOOK)

        A = UP * 2.4
        B = LEFT * 2.2 + DOWN
        C = RIGHT * 2.2 + DOWN

        triangle = Polygon(A, B, C, fill_color=BLUE, fill_opacity=0.35, stroke_width=6)

        side_labels = VGroup(
            MathTex("a").next_to(Line(A, B), LEFT),
            MathTex("a").next_to(Line(A, C), RIGHT),
            MathTex("a").next_to(Line(B, C), DOWN),
        )

        with self.voiceover(text="This triangle looks ordinary. But something surprising is hidden inside.") as tracker:
            self.play(Write(hook), run_time=tracker.duration * 0.4)

            self.play(Create(triangle), run_time=tracker.duration * 0.6)

        self.play(Write(side_labels), run_time=1)

        # ===============================
        # QUESTION MOMENT
        # ===============================

        question = Text("How much space is inside?", font_size=32).move_to(HOOK)

        with self.voiceover(text="Every side is the same length. But how much area does it contain?") as tracker:
            self.play(Transform(hook, question), run_time=tracker.duration)

        # ===============================
        # CREATE HEIGHT
        # ===============================

        D = DOWN

        height_line = DashedLine(A, D, color=RED, stroke_width=6)

        h_label = MathTex("h", color=RED).next_to(height_line, RIGHT)

        with self.voiceover(text="The hidden trick is cutting the triangle perfectly in half.") as tracker:
            self.play(Create(height_line), Write(h_label), run_time=tracker.duration)

        # ===============================
        # SPLIT WITHOUT REMOVING
        # ===============================

        left_piece = Polygon(A, B, D, fill_color=BLUE, fill_opacity=0.25, stroke_width=0)

        right_piece = Polygon(A, D, C, fill_color=GREEN, fill_opacity=0.35, stroke_width=0)

        with self.voiceover(text="One triangle becomes two identical right triangles.") as tracker:
            self.play(FadeIn(left_piece), FadeIn(right_piece), run_time=tracker.duration)

        # ===============================
        # LABEL THE NEW INFORMATION
        # ===============================

        half_base = MathTex(r"\frac a2", color=GREEN).next_to(Line(D, C), DOWN)

        hyp = MathTex("a", color=BLUE).next_to(Line(A, C), RIGHT)

        with self.voiceover(text="The diagonal is still a, but the base has become half of a.") as tracker:
            self.play(Write(half_base), Write(hyp), run_time=tracker.duration)

        # ===============================
        # MOVE CAMERA INTO DISCOVERY
        # ===============================

        with self.voiceover(text="Now the hidden relationship appears.") as tracker:
            self.play(self.camera.frame.animate.scale(0.8), run_time=tracker.duration)

        # ===============================
        # PYTHAGORAS APPEARS BESIDE OBJECT
        # ===============================

        pythagoras = MathTex(r"a^2=h^2+\left(\frac a2\right)^2", font_size=42).move_to(EQUATION_ZONE)

        with self.voiceover(text="This tiny right triangle follows Pythagoras.") as tracker:
            self.play(Write(pythagoras), run_time=tracker.duration)

        self.wait(2)

        # ===============================
        # SOLVE HEIGHT VISUALLY
        # ===============================

        step1 = MathTex(r"a^2=h^2+\frac{a^2}{4}", font_size=42).move_to(EQUATION_ZONE)

        with self.voiceover(text="The small base removes one quarter of a squared.") as tracker:
            self.play(TransformMatchingTex(pythagoras, step1), run_time=tracker.duration)

        step2 = MathTex(r"h^2=\frac{3a^2}{4}", font_size=48, color=YELLOW).move_to(EQUATION_ZONE)

        with self.voiceover(text="Only three quarters of a squared remains.") as tracker:
            self.play(TransformMatchingTex(step1, step2), run_time=tracker.duration)

        height_result = MathTex(r"h=\frac{\sqrt3}{2}a", font_size=55, color=YELLOW).move_to(EQUATION_ZONE)

        with self.voiceover(text="The hidden height is root three over two times a.") as tracker:
            self.play(TransformMatchingTex(step2, height_result), run_time=tracker.duration)

        # ===============================
        # RETURN TO WHOLE TRIANGLE
        # ===============================

        with self.voiceover(text="Now watch this hidden height unlock the area.") as tracker:
            self.play(
                self.camera.frame.animate.scale(1.25),
                FadeOut(left_piece),
                FadeOut(right_piece),
                FadeOut(half_base),
                FadeOut(hyp),
                run_time=tracker.duration,
            )

        # Keep height line visible
        self.play(FadeOut(height_result), run_time=0.5)

        # ===============================
        # AREA FORMULA APPEARS ON OBJECT
        # ===============================

        area_formula = MathTex(r"A=\frac12 bh", font_size=52).move_to(RIGHT * 3 + UP * 0.5)

        with self.voiceover(text="Every triangle is half of a rectangle.") as tracker:
            self.play(Write(area_formula), run_time=tracker.duration)

        # ===============================
        # BASE AND HEIGHT ENTER
        # ===============================

        substitution = MathTex(r"A=\frac12(a)\left(\frac{\sqrt3}{2}a\right)", font_size=42).move_to(RIGHT * 3 + UP * 0.5)

        with self.voiceover(text="For this triangle, the base is a and the height is the value we discovered.") as tracker:
            self.play(TransformMatchingTex(area_formula, substitution), run_time=tracker.duration)

        # ===============================
        # FINAL SIMPLIFICATION
        # ===============================

        final = MathTex(r"\boxed{A=\frac{\sqrt3}{4}a^2}", font_size=65, color=YELLOW).move_to(RIGHT * 3 + UP * 0.5)

        with self.voiceover(text="And the secret formula appears.") as tracker:
            self.play(TransformMatchingTex(substitution, final), run_time=tracker.duration)

        # ===============================
        # VISUAL MEMORY
        # ===============================

        with self.voiceover(text="A simple triangle was hiding a square relationship all along.") as tracker:
            self.play(triangle.animate.set_fill(YELLOW, opacity=0.45), run_time=tracker.duration)

        self.wait(1)

        # ===============================
        # LOOP ENDING
        # ===============================

        teaser = Text("What happens if the angle changes?", font_size=32).move_to(HOOK)

        with self.voiceover(text="But this only worked because every angle was sixty degrees.") as tracker:
            self.play(Transform(question, teaser), run_time=tracker.duration)

        self.wait(2)

        # Leave viewer with moving object

        with self.voiceover(text="Next, the triangle breaks the rule.") as tracker:
            self.play(triangle.animate.rotate(15 * DEGREES), run_time=tracker.duration)

        self.wait(2)
