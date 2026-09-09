from manim import *

from shorts.shorts_template import ShortScene


class PiIntroduction(ShortScene):
    """
    Introduction to Pi (π)
    ----------------------
    Explains:
    - Circle
    - Diameter
    - Circumference
    - Why circumference becomes 3.14 times the diameter
    - Scaling circles to show the constant ratio (Part 2)
    - Final definition of Pi (Part 3)
    """

    VOICE = "af_sarah"
    SPEED = 0.95
    VOLUME = 1.1

    def construct(self):
        # =========================================================
        # PART 1 — CIRCLE, DIAMETER & CIRCUMFERENCE
        # =========================================================

        title = Text("What is π?", font_size=64, weight=BOLD)
        with self.voiceover(text="Pi is one of the most famous numbers in mathematics. But what exactly is it?") as tracker:
            self.play(Write(title), run_time=tracker.duration)
        self.play(FadeOut(title))

        # Circle
        circle = Circle(radius=1.5, color=BLUE)
        center = Dot(circle.get_center(), color=WHITE)
        with self.voiceover(text="Let's begin with a simple circle.") as tracker:
            self.play(Create(circle), FadeIn(center), run_time=tracker.duration)

        # Diameter
        diameter = Line(circle.get_left(), circle.get_right(), color=YELLOW, stroke_width=5)
        diameter_label = MathTex("1").set_color(YELLOW)
        diameter_label.next_to(diameter, DOWN)
        with self.voiceover(text="Suppose this circle has a diameter, or width, of exactly one unit.") as tracker:
            self.play(Create(diameter), Write(diameter_label), run_time=tracker.duration)

        # Circumference
        circumference_text = Text("Circumference", font_size=32, color=BLUE)
        circumference_text.to_edge(UP, buff=0.5)
        with self.voiceover(text="The distance all the way around the circle is called the circumference.") as tracker:
            self.play(
                Indicate(circle),
                Write(circumference_text),
                run_time=tracker.duration,
            )

        # Unwrap Circumference
        unwrapped_line = Line(LEFT * 3.2, RIGHT * 3.2, color=BLUE, stroke_width=6)
        unwrapped_line.next_to(circle, DOWN, buff=1)
        circumference_value = MathTex("3.14").set_color(BLUE)
        circumference_value.next_to(unwrapped_line, DOWN)

        with self.voiceover(
            text=(
                "If we could unwrap the circumference into a straight line, "
                "its length would be about three point one four units."
            )
        ) as tracker:
            self.play(
                TransformFromCopy(circle, unwrapped_line),
                run_time=tracker.duration * 0.75,
            )
            self.play(Write(circumference_value), run_time=tracker.duration * 0.25)

        # Introduce Pi Symbol
        pi_symbol = MathTex(r"\pi").scale(2)
        pi_symbol.set_color(RED)
        with self.voiceover(text="This special number, three point one four, is called pi.") as tracker:
            self.play(FadeIn(pi_symbol), run_time=tracker.duration)

        self.wait(1)

        # Clean up Part 1 objects before Part 2
        self.play(
            FadeOut(
                VGroup(
                    circle,
                    center,
                    diameter,
                    diameter_label,
                    circumference_text,
                    unwrapped_line,
                    circumference_value,
                    pi_symbol,
                )
            )
        )

        # =========================================================
        # PART 2 — SCALING CIRCLES & CONSTANT RATIO
        # =========================================================

        question = Text("What if we change the size of the circle?", font_size=38).to_edge(UP, buff=0.6)

        with self.voiceover(text="But what happens if we change the size of the circle?") as tracker:
            self.play(Write(question), run_time=tracker.duration)

        # Table/List of Ratios for different diameters (using \mathrm to avoid LaTeX text-mode errors)
        ratios = VGroup(
            MathTex(r"\mathrm{Diameter} = 1 \rightarrow \frac{3.14}{1} = 3.14"),
            MathTex(r"\mathrm{Diameter} = 2 \rightarrow \frac{6.28}{2} = 3.14"),
            MathTex(r"\mathrm{Diameter} = 3 \rightarrow \frac{9.42}{3} = 3.14"),
        ).arrange(DOWN, buff=0.4)

        with self.voiceover(
            text=(
                "If we double the diameter to two, the circumference doubles to six point two eight. "
                "If we triple it to three, the circumference triples as well."
            )
        ) as tracker:
            self.play(Write(ratios[0]), run_time=tracker.duration * 0.3)
            self.play(Write(ratios[1]), run_time=tracker.duration * 0.35)
            self.play(Write(ratios[2]), run_time=tracker.duration * 0.35)

        self.wait(1)

        # =========================================================
        # PART 3 — FINAL DEFINITION OF PI
        # =========================================================

        constant_text = Text("The answer is always the same.", font_size=36, weight=BOLD)
        constant_text.to_edge(UP, buff=0.5)

        with self.voiceover(text="Even though the circle becomes larger, the answer is always the same.") as tracker:
            self.play(FadeOut(question), Write(constant_text), run_time=tracker.duration)

        # Show Pi Symbol
        pi_final = MathTex(r"\pi = 3.14159265\ldots").scale(1.3)
        pi_final.set_color(RED)
        pi_final.move_to(ORIGIN)

        with self.voiceover(text="That constant number is pi, approximately three point one four one five nine.") as tracker:
            self.play(FadeOut(ratios), Write(pi_final), run_time=tracker.duration)

        # Definition Formula
        definition = MathTex(r"\pi = ", r"\frac{\mathrm{Circumference}}{\mathrm{Diameter}}").scale(1.2)
        definition.next_to(pi_final, DOWN, buff=0.8)
        box = SurroundingRectangle(definition, color=BLUE, buff=0.2)

        with self.voiceover(text="Pi is defined as the circumference of a circle divided by its diameter.") as tracker:
            self.play(Write(definition), run_time=tracker.duration * 0.8)
            self.play(Create(box), run_time=tracker.duration * 0.2)

        # Final Message
        final_text = Text("Every circle shares this ratio.", font_size=38, weight=BOLD)
        final_text.to_edge(DOWN, buff=0.7)

        with self.voiceover(
            text="No matter how big or small a circle is, every circle in the universe shares this same ratio."
        ) as tracker:
            self.play(Write(final_text), run_time=tracker.duration)

        # End hold
        self.wait(3)
