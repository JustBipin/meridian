from manim import *

from shorts.shorts_template import ShortScene


class AreaIntroduction(ShortScene):
    """
    Area Short (Under 30s) - Hook & Reveal
    --------------------------------------
    Fast-paced visual explanation of area using a 1x1 unit square
    expanding into a 5x3 rectangle."""

    SPEED = 1.05
    VOLUME = 1.1

    def construct(self):
        DARK_TEXT = "#222222"
        MAIN_BLUE = BLUE
        MAIN_RED = RED
        MAIN_GREEN = GREEN

        # =========================================================
        # GRID (Background)
        # =========================================================
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

        # =========================================================
        # BEAT 1: THE HOOK (0-5s) — WHAT IS AREA?
        # =========================================================
        square = Polygon(
            grid.c2p(0, 0),
            grid.c2p(1, 0),
            grid.c2p(1, 1),
            grid.c2p(0, 1),
            fill_color=MAIN_BLUE,
            fill_opacity=0.5,
            stroke_color=MAIN_BLUE,
            stroke_width=4,
        )

        # Instant zoom into the unit square
        self.camera.frame.move_to(square.get_center()).set(width=6)

        with self.voiceover(text="What actually is area? Let's start with a single square block.") as tracker:
            self.play(FadeIn(square), run_time=tracker.duration)

        # Dimensions for unit square
        length_arrow = DoubleArrow(grid.c2p(0, 0) + DOWN * 0.35, grid.c2p(1, 0) + DOWN * 0.35, buff=0, color=MAIN_RED)
        length_text = MathTex("1\\\\ \\\\mathrm{unit}", color=DARK_TEXT).next_to(length_arrow, DOWN, buff=0.15)

        breadth_arrow = DoubleArrow(grid.c2p(0, 0) + LEFT * 0.35, grid.c2p(0, 1) + LEFT * 0.35, buff=0, color=MAIN_RED)
        breadth_text = (
            MathTex("1\\\\ \\\\mathrm{unit}", color=DARK_TEXT).rotate(PI / 2).next_to(breadth_arrow, LEFT, buff=0.15)
        )

        area_formula = VGroup(
            MathTex(r"\text{Area} = 1 \times 1", color=DARK_TEXT),
            MathTex(r"= 1\\\\ \mathrm{unit}^2", color=MAIN_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT)
        area_formula.to_edge(DOWN, buff=0.8)

        with self.voiceover(text="One unit wide, one unit tall. Length times breadth gives us one square unit!") as tracker:
            t = tracker.duration
            self.play(
                GrowArrow(length_arrow), Write(length_text), GrowArrow(breadth_arrow), Write(breadth_text), run_time=t * 0.5
            )
            self.play(Write(area_formula), run_time=t * 0.5)

        # =========================================================
        # BEAT 2: THE EXPANSION (5-15s) — GROWING TO 5x3
        # =========================================================
        rectangle = Polygon(
            grid.c2p(0, 0),
            grid.c2p(5, 0),
            grid.c2p(5, 3),
            grid.c2p(0, 3),
            fill_color=MAIN_BLUE,
            fill_opacity=0.5,
            stroke_color=MAIN_BLUE,
            stroke_width=4,
        )

        new_length_arrow = DoubleArrow(grid.c2p(0, 0) + DOWN * 0.35, grid.c2p(5, 0) + DOWN * 0.35, buff=0, color=MAIN_RED)
        new_length_text = MathTex("5\\\\ \\\\mathrm{ft}", color=DARK_TEXT).next_to(new_length_arrow, DOWN, buff=0.15)

        new_breadth_arrow = DoubleArrow(grid.c2p(0, 0) + LEFT * 0.35, grid.c2p(0, 3) + LEFT * 0.35, buff=0, color=MAIN_RED)
        new_breadth_text = (
            MathTex("3\\\\ \\\\mathrm{ft}", color=DARK_TEXT).rotate(PI / 2).next_to(new_breadth_arrow, LEFT, buff=0.15)
        )

        rectangle_formula = VGroup(
            MathTex(r"\text{Area} = 5 \times 3", color=DARK_TEXT),
            MathTex(r"= 15\\\\ \mathrm{ft}^2", color=MAIN_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT)
        rectangle_formula.to_edge(DOWN, buff=0.8)

        with self.voiceover(text="Now, stretch it out! Five feet long, three feet wide...") as tracker:
            t = tracker.duration
            # Smoothly pan camera to track the growing rectangle
            self.play(
                self.camera.frame.animate.move_to(rectangle.get_center()).set(width=9),
                Transform(square, rectangle),
                Transform(length_arrow, new_length_arrow),
                Transform(length_text, new_length_text),
                Transform(breadth_arrow, new_breadth_arrow),
                Transform(breadth_text, new_breadth_text),
                run_time=t,
            )

        # =========================================================
        # BEAT 3: THE PAYOFF (15-20s) — THE FINAL ANSWER
        # =========================================================
        with self.voiceover(text="Multiply them together... and you get fifteen square feet!") as tracker:
            self.play(Transform(area_formula, rectangle_formula), run_time=tracker.duration)

        # =========================================================
        # BEAT 4: OUTRO (20-25s) — THE TAKEAWAY
        # =========================================================
        # Caption placed safely at the very top edge to prevent overlapping
        caption = Text("Area is just how many squares fit inside.", font_size=32, weight=BOLD, color=DARK_TEXT)
        caption.to_edge(UP, buff=0.4)

        with self.voiceover(text="Area is simply counting how many squares fit inside.") as tracker:
            t = tracker.duration
            self.play(
                self.camera.frame.animate.scale(1.2),
                FadeIn(caption, shift=DOWN),
                run_time=t,
            )

        self.wait(1.5)
