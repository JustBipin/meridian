from manim import *

from shorts.shorts_template import ShortScene, apply_vertical_config

apply_vertical_config()


class ConditionalProbability(ShortScene):
    LANG_CODE = "a"

    def construct(self):

        # ==========================================================
        # LAYOUT
        # ==========================================================

        TOP_Y = 5.25

        # ==========================================================
        # SAMPLE SPACE
        # ==========================================================

        frame = RoundedRectangle(
            width=6.9,
            height=4.4,
            corner_radius=0.18,
            stroke_width=5,
            color=BLACK,
        ).move_to(UP * TOP_Y)

        omega = MathTex(r"\Omega", font_size=42)
        omega.next_to(frame.get_corner(UL), DR, buff=0.15)

        # ==========================================================
        # VENN — no prefill. Circles start as outlines only.
        # ==========================================================

        left_circle = Circle(
            radius=1.18,
            stroke_color=RED,
            stroke_width=8,
            fill_opacity=0,
        )

        right_circle = Circle(
            radius=1.18,
            stroke_color=BLUE,
            stroke_width=8,
            fill_opacity=0,
        )

        left_circle.shift(LEFT * 0.75)
        right_circle.shift(RIGHT * 0.75)

        venn = VGroup(left_circle, right_circle)
        venn.move_to(frame.get_center())

        labelA = MathTex("A", color=RED, font_size=48)
        labelA.next_to(left_circle, UL, buff=0.18)

        labelB = MathTex("B", color=BLUE, font_size=48)
        labelB.next_to(right_circle, UR, buff=0.18)

        # ==========================================================
        # INTERSECTION
        # ==========================================================

        intersection = Intersection(left_circle, right_circle)
        intersection.set_style(fill_color=PURPLE, fill_opacity=0, stroke_width=0)

        # ==========================================================
        # DRAW DIAGRAM
        # ==========================================================

        with self.voiceover(text="Consider a sample space Omega containing two events, -A- and B.") as tracker:
            self.play(Create(frame), run_time=tracker.duration * 0.3)
            self.play(
                FadeIn(omega),
                Create(left_circle),
                Create(right_circle),
                run_time=tracker.duration * 0.4,
            )
            self.play(
                FadeIn(labelA),
                FadeIn(labelB),
                run_time=tracker.duration * 0.3,
            )

        # ==========================================================
        # FORMULA — stacked BELOW the diagram
        # ==========================================================

        formula = MathTex(
            "P(",
            "A",
            "|",
            "B",
            ")=",
            font_size=60,
        )
        formula[1].set_color(RED)
        formula[3].set_color(BLUE)

        formula.next_to(frame, DOWN, buff=0.6)
        formula.align_to(frame, LEFT)
        formula.shift(DOWN * 0.42)

        # fraction bar
        frac_bar = Line(LEFT, RIGHT, stroke_width=3)
        frac_bar.set_length(3.0)
        frac_bar.next_to(formula, RIGHT, buff=0.5)

        with self.voiceover(
            text="The conditional probability of event -A- given that event B has occurred, denoted P of -A- given B..."
        ) as tracker:
            self.play(Write(formula), run_time=tracker.duration)

        # ==========================================================
        # NUMERATOR
        # ==========================================================

        numerator = MathTex(
            "P(",
            "A",
            r"\cap",
            "B",
            ")",
            font_size=60,
        )
        numerator[1].set_color(RED)
        numerator[3].set_color(BLUE)

        numerator.next_to(frac_bar, UP * 1.2, buff=0.25, aligned_edge=UP)

        with self.voiceover(
            text="is defined as the ratio of the probability of the intersection of -A- and B..."
        ) as tracker:
            self.play(Write(numerator), run_time=tracker.duration * 0.6)
            self.play(
                intersection.animate.set_fill(PURPLE, opacity=0.45),
                run_time=tracker.duration * 0.4,
            )

        # ==========================================================
        # FRACTION BAR & DENOMINATOR
        # ==========================================================

        denominator = MathTex("P(", "B", ")", font_size=60)
        denominator[1].set_color(BLUE)
        denominator.next_to(frac_bar, DOWN, buff=0.12)

        with self.voiceover(text="divided by the probability of the conditioning event B.") as tracker:
            self.play(Create(frac_bar), run_time=tracker.duration * 0.3)
            self.play(Write(denominator), run_time=tracker.duration * 0.4)
            self.play(
                right_circle.animate.set_fill(BLUE, opacity=0.18),
                run_time=tracker.duration * 0.3,
            )

        # Group the whole formula block
        formula_group = VGroup(formula, numerator, frac_bar, denominator)

        # ==========================================================
        # CONDITIONED SAMPLE SPACE
        # ==========================================================

        b_box = RoundedRectangle(
            width=4.6,
            height=3.2,
            corner_radius=0.18,
            stroke_width=8,
            color=BLUE,
        )
        b_box.next_to(frame, DOWN, buff=1.2)
        b_box.align_to(frame, ORIGIN)

        diagram_equals = MathTex("=", font_size=60)
        diagram_equals.move_to([frame.get_center()[0], (frame.get_bottom()[1] + b_box.get_top()[1]) / 2, 0])

        b_label = MathTex("B", color=BLUE, font_size=46)
        b_label.next_to(b_box, UL, buff=0.15)

        new_event = Circle(
            radius=0.72,
            stroke_color=PURPLE,
            stroke_width=7,
            fill_color=PURPLE,
            fill_opacity=0.35,
        )
        new_event.move_to(b_box)

        new_label = MathTex(r"A\cap B", font_size=42)
        new_label.move_to(new_event)

        drop = b_box.height + 1.2

        with self.voiceover(
            text=(
                "Geometrically, conditioning on B restricts the universal set. "
                "Event B becomes the new restricted sample space."
            )
        ) as tracker:
            self.play(
                TransformFromCopy(right_circle, b_box),
                FadeIn(b_label),
                FadeIn(diagram_equals),
                formula_group.animate.shift(DOWN * drop),
                run_time=tracker.duration,
            )

        with self.voiceover(
            text=(
                "Within this restricted domain B, the only region where event -A- can still occur "
                "is the intersection, -A- cap B."
            )
        ) as tracker:
            self.play(
                TransformFromCopy(intersection, new_event),
                run_time=tracker.duration * 0.6,
            )
            self.play(
                FadeIn(new_label),
                run_time=tracker.duration * 0.4,
            )

        # ----------------------------------------------------------
        # Explanation, left-aligned
        # ----------------------------------------------------------

        exp_1 = Tex(
            r"$B$ is the new sample space",
            font_size=42,
        )
        exp_1.next_to(formula_group, DOWN, buff=0.6)
        exp_1.align_to(frame, ORIGIN)

        exp_2 = Tex(
            r"Within it, $A \cap B$ is the only region \\ where $A$ can still occur.",
            font_size=42,
        )
        exp_2.next_to(exp_1, DOWN, buff=0.5)
        exp_2.align_to(frame, LEFT)

        with self.voiceover(
            text=(
                "Thus, conditional probability evaluates the measure of the intersection relative to the measure of event B."
            )
        ) as tracker:
            self.play(FadeIn(exp_1, shift=UP * 0.15), run_time=tracker.duration * 0.5)
            self.play(FadeIn(exp_2, shift=UP * 0.15), run_time=tracker.duration * 0.5)

        # ----------------------------------------------------------
        # Final highlight and emphasis
        # ----------------------------------------------------------

        highlight = SurroundingRectangle(
            formula_group,
            corner_radius=0.15,
            color=BLACK,
            stroke_width=3,
            buff=0.22,
        )

        with self.voiceover(text="This quotient defines the updated probability measure under prior knowledge.") as tracker:
            self.play(
                Indicate(new_event, color=PURPLE, scale_factor=1.08),
                Indicate(b_box, color=BLUE, scale_factor=1.04),
                run_time=tracker.duration * 0.5,
            )
            self.play(Create(highlight), run_time=tracker.duration * 0.5)

        self.wait(1)
