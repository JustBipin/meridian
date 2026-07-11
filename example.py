from manim import *
from manim_themes.manim_theme import apply_theme


class DerivativeIntro(Scene):
    def setup(self):
        theme = "london"
        apply_theme(manim_scene=self, theme_name=theme)

    def construct(self):
        # Title
        title = Text("What is a Derivative?", font_size=42)
        self.play(FadeIn(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        # Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 9, 2],
            x_length=7,
            y_length=4,
            tips=False,
        )

        labels = axes.get_axis_labels(
            MathTex("x"),
            MathTex("y"),
        )

        graph = axes.plot(
            lambda x: x**2,
            x_range=[-3, 3],
            color=BLUE,
        )

        self.play(Create(axes), Write(labels))
        self.play(Create(graph))

        tracker = ValueTracker(-2)

        # Moving point
        point = always_redraw(
            lambda: Dot(
                axes.c2p(
                    tracker.get_value(),
                    tracker.get_value() ** 2,
                ),
                color=YELLOW,
            )
        )

        # Tangent approximation
        tangent = always_redraw(
            lambda: axes.get_secant_slope_group(
                x=tracker.get_value(),
                graph=graph,
                dx=0.001,
                secant_line_color=RED,
            )
        )

        slope_label = Text("Slope =", font_size=28).to_corner(UL)

        slope_value = always_redraw(
            lambda: DecimalNumber(
                2 * tracker.get_value(),
                num_decimal_places=1,
            ).next_to(slope_label, RIGHT)
        )

        explanation = Text(
            "Derivative = slope of the tangent",
            font_size=28,
        ).to_edge(DOWN)

        self.play(FadeIn(point), FadeIn(tangent))
        self.play(Write(explanation))
        self.play(FadeIn(slope_label), FadeIn(slope_value))

        self.play(
            tracker.animate.set_value(2),
            run_time=8,
            rate_func=linear,
        )

        formula = MathTex(r"\frac{d}{dx}(x^2)=2x").scale(1.3)

        self.play(
            FadeOut(explanation),
            FadeOut(point),
            FadeOut(tangent),
            FadeOut(slope_label),
            FadeOut(slope_value),
        )

        self.play(Write(formula))
        self.wait(2)
