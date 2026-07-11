"""
Area Introduction Animation
---------------------------
Concept:
    Area is introduced as counting square units.

Flow:
1. Title
2. Definition
3. Infinite grid
4. Unit square
5. Length and breadth
6. Area of unit square
7. Unit conversion
8. Expand square into 5 x 3 rectangle
9. Calculate rectangle area
10. Zoom out

Author:
    Bipin Thapa
"""

from manim import *
from manim_themes.manim_theme import apply_theme


class AreaIntroduction(MovingCameraScene):
    def setup(self):
        super().setup()

        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):

        # =========================================================
        # TITLE
        # =========================================================

        title = Text("Area", font_size=64, weight=BOLD)

        self.play(Write(title))

        self.wait()

        # =========================================================
        # DEFINITION
        # =========================================================

        definition = Text("The amount of surface covered\nby a two-dimensional shape.", font_size=34)

        definition.next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(definition))

        self.wait(3)

        self.play(FadeOut(title), FadeOut(definition))

        # =========================================================
        # GRID
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
        # UNIT SQUARE
        # =========================================================

        square = Polygon(
            grid.c2p(0, 0),
            grid.c2p(1, 0),
            grid.c2p(1, 1),
            grid.c2p(0, 1),
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        self.play(FadeIn(square))

        # zoom in

        self.play(self.camera.frame.animate.move_to(square.get_bottom()).scale(1), run_time=0.5)

        # =========================================================
        # DIMENSIONS
        # =========================================================

        length_arrow = DoubleArrow(grid.c2p(0, 0) + DOWN * 0.35, grid.c2p(1, 0) + DOWN * 0.35, buff=0)

        length_text = MathTex("1\\ \\text{unit}")

        length_text.next_to(length_arrow, DOWN)

        breadth_arrow = DoubleArrow(grid.c2p(0, 0) + LEFT * 0.35, grid.c2p(0, 1) + LEFT * 0.35, buff=0)

        breadth_text = MathTex("1\\ \\text{unit}")

        breadth_text.rotate(PI / 2)

        breadth_text.next_to(breadth_arrow, LEFT)

        self.play(GrowArrow(length_arrow), Write(length_text), GrowArrow(breadth_arrow), Write(breadth_text))

        self.wait(2)

        # =========================================================
        # AREA FORMULA
        # =========================================================

        area_formula = VGroup(
            MathTex(
                r"\text{Area}"
                r"=\text{Length}\times\text{Breadth}"
            ),
            MathTex(r"=1\times1"),
            MathTex(r"=1\ \text{unit}^{2}", color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT)

        area_formula.to_edge(DOWN)

        for item in area_formula:
            self.play(Write(item))
            self.wait(0.5)

        self.wait(2)

        # =========================================================
        # CHANGE UNITS
        # =========================================================

        # diagram units

        metre_length = MathTex("1\\ \\mathrm{m}")

        metre_length.move_to(length_text)

        metre_breadth = MathTex("1\\ \\mathrm{m}")

        metre_breadth.rotate(PI / 2)

        metre_breadth.move_to(breadth_text)

        metre_square = MathTex(r"=1\ \mathrm{m}^{2}", color=GREEN)

        metre_square.move_to(area_formula[2])

        self.play(
            Transform(length_text, metre_length),
            Transform(breadth_text, metre_breadth),
            Transform(area_formula[2], metre_square),
        )

        self.wait(2)

        feet_length = MathTex("1\\ \\mathrm{ft}")

        feet_length.move_to(length_text)

        feet_breadth = MathTex("1\\ \\mathrm{ft}")

        feet_breadth.rotate(PI / 2)

        feet_breadth.move_to(breadth_text)

        # formula units

        feet_square = MathTex(r"=1\ \mathrm{ft}^{2}", color=GREEN)

        feet_square.move_to(area_formula[2])

        self.play(
            Transform(length_text, feet_length),
            Transform(breadth_text, feet_breadth),
            Transform(area_formula[2], feet_square),
        )

        self.wait(2)

        # =========================================================
        # GROW INTO 5 x 3 RECTANGLE
        # =========================================================

        rectangle = Polygon(
            grid.c2p(0, 0),
            grid.c2p(5, 0),
            grid.c2p(5, 3),
            grid.c2p(0, 3),
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        # NEW DIMENSIONS

        new_length_arrow = DoubleArrow(grid.c2p(0, 0) + DOWN * 0.35, grid.c2p(5, 0) + DOWN * 0.35, buff=0)

        new_length_text = MathTex("5\\ \\mathrm{ft}")

        new_length_text.next_to(new_length_arrow, DOWN)

        new_breadth_arrow = DoubleArrow(grid.c2p(0, 0) + LEFT * 0.35, grid.c2p(0, 3) + LEFT * 0.35, buff=0)

        new_breadth_text = MathTex("3\\ \\mathrm{ft}")

        new_breadth_text.rotate(PI / 2)

        new_breadth_text.next_to(new_breadth_arrow, LEFT)

        # NEW FORMULA

        rectangle_formula = VGroup(
            MathTex(
                r"\text{Area}"
                r"=\text{Length}\times\text{Breadth}"
            ),
            MathTex(r"=5\times3"),
            MathTex(r"=15\ \mathrm{ft}^{2}", color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT)

        rectangle_formula.to_edge(DOWN)

        self.play(
            self.camera.frame.animate.move_to(rectangle.get_bottom()),
            Transform(square, rectangle),
            Transform(length_arrow, new_length_arrow),
            Transform(length_text, new_length_text),
            Transform(breadth_arrow, new_breadth_arrow),
            Transform(breadth_text, new_breadth_text),
            Transform(area_formula, rectangle_formula),
        )

        self.wait(3)

        # =========================================================
        # ZOOM OUT
        # =========================================================

        self.play(self.camera.frame.animate.scale(1.3), run_time=2)

        caption = Text("Simply put, area is the number of square units inside a shape.", font_size=34)

        caption.to_edge(UP)

        self.play(FadeIn(caption))

        self.wait(3)
