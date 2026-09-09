import numpy as np
from manim import *

from shorts.shorts_template import ShortScene


class AreaTriangleShort(ShortScene):
    """
    Area of a Triangle Short (Under 50s)
    """

    def construct(self):
        self.camera.frame.set(width=7, height=12)

        # Zones
        TOP_ZONE = UP * 4.5
        MID_ZONE = UP * 0.5
        BOT_ZONE = DOWN * 4.5

        # Main points
        bl = np.array([-2, -1.5, 0]) + MID_ZONE
        br = np.array([2, -1.5, 0]) + MID_ZONE
        apex = np.array([-0.5, 1.5, 0]) + MID_ZONE
        foot = np.array([-0.5, -1.5, 0]) + MID_ZONE
        tl = np.array([-2, 1.5, 0]) + MID_ZONE
        tr = np.array([2, 1.5, 0]) + MID_ZONE

        # Shapes
        tri = Polygon(bl, br, apex, fill_color=BLUE, fill_opacity=0.5, stroke_color=BLUE, stroke_width=6)

        rect_outline = Polygon(bl, br, tr, tl, fill_opacity=0, stroke_width=6, stroke_color=GREY_D)

        split_line = Line(foot, apex, color=RED, stroke_width=6)

        # Split halves
        left_tri = Polygon(bl, foot, apex, fill_color=BLUE, fill_opacity=0.5, stroke_width=0)

        right_tri = Polygon(br, foot, apex, fill_color=RED, fill_opacity=0.5, stroke_width=0)

        left_rect = Polygon(tl, bl, foot, apex, fill_color=BLUE, fill_opacity=0.15, stroke_width=2, stroke_color=BLUE)

        right_rect = Polygon(tr, br, foot, apex, fill_color=RED, fill_opacity=0.15, stroke_width=2, stroke_color=RED)

        # Captions
        caption = Text("Why is Area = 1/2 bh?", font_size=36, weight=BOLD).move_to(TOP_ZONE)

        caption_rect = Text("Step 1: Enclose in a rectangle.", font_size=36).move_to(TOP_ZONE)

        caption_split = Text("Step 2: Split it.", font_size=36).move_to(TOP_ZONE)

        caption_halves = Text("Each triangle is half its rectangle.", font_size=32).move_to(TOP_ZONE)

        final_formula = MathTex(r"\text{Area}=\frac{1}{2}\times\text{base}\times\text{height}", font_size=40).move_to(
            BOT_ZONE
        )

        # Scene

        with self.voiceover(text="Why is the triangle area one-half base times height? Let's break it down.") as tracker:
            self.play(FadeIn(tri), Write(caption), run_time=tracker.duration)

        with self.voiceover(text="First, enclose it in a rectangle with the same base and height.") as tracker:
            self.play(Transform(caption, caption_rect), Create(rect_outline), run_time=tracker.duration)

        with self.voiceover(
            text="Next, split it down the center. We get two rectangles, each with a triangle inside."
        ) as tracker:
            self.play(
                Transform(caption, caption_split),
                Create(split_line),
                FadeOut(tri),
                FadeIn(left_rect),
                FadeIn(right_rect),
                FadeIn(left_tri),
                FadeIn(right_tri),
                run_time=tracker.duration,
            )

        with self.voiceover(
            text=(
                "See? Each triangle is exactly half of its own rectangle. "
                "So, the whole triangle is half the total rectangle."
            )
        ) as tracker:
            self.play(Transform(caption, caption_halves), run_time=tracker.duration)

        with self.voiceover(text="And that is why the area formula is one-half base times height.") as tracker:
            self.play(
                FadeOut(left_rect),
                FadeOut(right_rect),
                FadeOut(left_tri),
                FadeOut(right_tri),
                FadeOut(split_line),
                FadeOut(rect_outline),
                FadeOut(caption),
                Write(final_formula),
                run_time=tracker.duration,
            )

        self.wait(2)
