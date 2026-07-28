import numpy as np
from manim import *
from manim_themes.manim_theme import apply_theme


class AreaIntroduction(MovingCameraScene):
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
    """

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
            MathTex(r"\text{Area}" r"=\text{Length}\times\text{Breadth}"),
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
            MathTex(r"\text{Area}" r"=\text{Length}\times\text{Breadth}"),
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

        caption = Text("Area is the number of square units inside a shape.", font_size=34)

        caption.to_edge(UP)

        self.play(FadeIn(caption))

        self.wait(3)


class AreaRightAngledTriangle(MovingCameraScene):
    """
    Area of Right Angled Triangles
    ---------------------------
    Concept:
        A scene demonstrating that the area of a right-angled triangle
        is exactly half the area of its bounding rectangle.

    Flow:
    1. Displays a static b x h rectangle, centered, with braces.
    2. Slices the rectangle diagonally.
    3. Separates both halves and labels them.
    4. Proves congruency by rotating the red triangle onto the blue one.
    5. Once the red triangle fades away, labels the base and height of
        the remaining blue triangle.
    6. Concludes with the classic 1/2 * b * h formula.
    """

    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        # =========================================================
        # TITLE
        # =========================================================

        title = Text("Area of Triangles", font_size=64, weight=BOLD)

        self.play(Write(title))

        self.wait(1)
        self.play(FadeOut(title))

        # =========================================================
        # 1. ENVIRONMENT & GRID SETUP
        # =========================================================
        grid = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-12, 12, 1],
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )
        self.add(grid)

        # =========================================================
        # 2. GEOMETRY DEFINITION (centered, room above AND below)
        # =========================================================
        bottom_left = grid.c2p(-3, -1.5)
        bottom_right = grid.c2p(3, -1.5)
        top_right = grid.c2p(3, 1.5)
        top_left = grid.c2p(-3, 1.5)

        rect = Polygon(
            bottom_left,
            bottom_right,
            top_right,
            top_left,
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_color=BLUE,
            stroke_width=4,
        )

        # =========================================================
        # 3. DIMENSIONS
        # =========================================================
        base_brace = Brace(Line(bottom_left, bottom_right), direction=DOWN, color=GREY_D, buff=0.15)
        base_label = base_brace.get_text("b").set_color(GREY_D)

        height_brace = Brace(Line(bottom_right, top_right), direction=RIGHT, color=GREY_D, buff=0.15)
        height_label = height_brace.get_text("h").set_color(GREY_D)

        # =========================================================
        # 4. INITIAL DISPLAY & STATIC FORMULA HOLD
        # =========================================================
        #
        intro_text = Text(
            "Take any rectangle with base b and height h.",
            font_size=30,
        ).to_edge(UP, buff=0.6)

        rect_formula = MathTex(r"\text{Rectangle Area} = b \times h").to_edge(DOWN, buff=0.6)

        self.play(FadeIn(rect), run_time=1)
        self.play(FadeIn(base_brace), Write(base_label), run_time=1)
        self.play(FadeIn(height_brace), Write(height_label), run_time=1)
        self.play(Write(intro_text))
        self.wait(1)

        self.play(Write(rect_formula), run_time=1)

        self.wait(2)
        self.play(FadeOut(intro_text), FadeOut(rect_formula))

        # =========================================================
        # 5. THE DIAGONAL SPLIT
        # =========================================================
        cut_text = Text("Now slice it along the diagonal.", font_size=28).to_edge(DOWN, buff=0.6)
        self.play(Write(cut_text))

        diagonal = Line(bottom_left, top_right, stroke_color=GREEN, stroke_width=4)
        self.play(Create(diagonal), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(cut_text))

        # Two complementary right-angled triangles (second one is now RED)
        t1 = Polygon(
            bottom_left, bottom_right, top_right, fill_color=BLUE, fill_opacity=0.7, stroke_color=BLUE, stroke_width=2
        )
        t2 = Polygon(bottom_left, top_right, top_left, fill_color=RED, fill_opacity=0.5, stroke_color=RED, stroke_width=2)

        # Hot-swap the rectangle+diagonal for the two individual triangles
        self.play(FadeIn(t1, t2), FadeOut(rect, diagonal))
        self.wait(0.5)

        # =========================================================
        # 6. SMALL, SAFE SEPARATION (stays well inside the frame)
        # =========================================================
        self.play(
            t1.animate.shift(RIGHT * 0.9 + DOWN * 0.5),
            t2.animate.shift(LEFT * 0.9 + UP * 0.5),
            FadeOut(base_brace),
            FadeOut(base_label),
            FadeOut(height_brace),
            FadeOut(height_label),
            run_time=1.5,
        )
        self.wait(1)

        t1_label = Text("Triangle 1", font_size=24, color=BLUE).next_to(t1, DOWN, buff=0.3)
        t2_label = Text("Triangle 2", font_size=24, color=RED).next_to(t2, UP, buff=0.3)
        self.play(Write(t1_label), Write(t2_label))
        self.wait(1.5)

        # =========================================================
        # 7. PROVE CONGRUENCY BY ROTATING THE RED TRIANGLE ONTO THE BLUE
        # =========================================================
        congruent_text = Text(
            "Let's check: Are these two triangles really identical?",
            font_size=28,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(congruent_text))
        self.wait(1.5)

        self.play(FadeOut(congruent_text), FadeOut(t1_label), FadeOut(t2_label))

        # The second triangle flips (rotates 180 degrees) about its own center...
        self.play(
            Rotate(t2, angle=PI, about_point=t2.get_center()),
            run_time=1.5,
        )
        # ...then slides down to land exactly on the blue triangle.
        self.play(t2.animate.move_to(t1.get_center()), run_time=1.2)
        self.wait(0.5)

        match_text = Text("Perfect match: same shape, same size.", font_size=28).to_edge(DOWN, buff=0.6)
        self.play(Write(match_text))
        self.wait(2)

        # fade the red copy, leaving the blue one.
        self.play(FadeOut(t2), FadeOut(match_text))

        # =========================================================
        # 8. MOVE THE BLUE TRIANGLE TO THE CENTER
        # =========================================================
        self.play(t1.animate.move_to(UP * 0.6), run_time=1.2)
        self.wait(0.5)

        # Complete the "ghost" rectangle with dotted lines for the two
        # sides the triangle doesn't have (top and left), unfilled.
        bl, br, tr = t1.get_vertices()[0], t1.get_vertices()[1], t1.get_vertices()[2]
        tl = bl + (tr - br)

        dashed_top = DashedLine(tl, tr, color=GREY_D, stroke_width=2)
        dashed_left = DashedLine(bl, tl, color=GREY_D, stroke_width=2)

        self.play(FadeIn(dashed_top), FadeIn(dashed_left), run_time=1.2)
        self.wait(0.5)

        # =========================================================
        # 9. LABEL THE TRIANGLE'S BASE AND HEIGHT
        # =========================================================
        base_edge = Line(t1.get_vertices()[0], t1.get_vertices()[1])
        height_edge = Line(t1.get_vertices()[1], t1.get_vertices()[2])

        tri_base_brace = Brace(base_edge, direction=DOWN, color=GREY_D, buff=0.15)
        tri_base_label = tri_base_brace.get_text("b").set_color(GREY_D)

        tri_height_brace = Brace(height_edge, direction=RIGHT, color=GREY_D, buff=0.15)
        tri_height_label = tri_height_brace.get_text("h").set_color(GREY_D)

        self.play(
            FadeIn(tri_base_brace),
            Write(tri_base_label),
            FadeIn(tri_height_brace),
            Write(tri_height_label),
        )
        self.wait(1.5)

        # =========================================================
        # 10. FINAL GEOMETRIC TAKEAWAY, WRITTEN BELOW THE TRIANGLE
        # =========================================================
        triangle_group = VGroup(
            t1,
            dashed_top,
            dashed_left,
            tri_base_brace,
            tri_base_label,
            tri_height_brace,
            tri_height_label,
        )

        final_formula = (
            MathTex(
                r"\text{Area of Right Angled Triangle} = \frac{1}{2} \times b \times h",
            )
            .scale(0.9)
            .next_to(triangle_group, DOWN, buff=0.6)
        )

        # Create a rectangle around the formula
        box = SurroundingRectangle(
            final_formula,
            color=BLUE,
            buff=0.2,  # Space between text and rectangle
            corner_radius=0.1,  # Optional: rounded corners
        )

        self.play(Write(final_formula), Create(box))

        self.wait(6)

        # =========================================================
        # 11. ISOSCELES RIGHT-ANGLED TRIANGLE EXTENSION
        # =========================================================
        iso_intro = Text("For an Isosceles Right-Angled Triangle:", font_size=28).to_edge(UP, buff=0.6)

        self.wait(0.5)

        # Shrink the base to match the height (3 units)
        current_bl = t1.get_vertices()[0]
        new_br = current_bl + RIGHT * 3
        new_tr = new_br + UP * 3

        # Create the target triangle and move it to ORIGIN first
        iso_t1 = Polygon(
            current_bl, new_br, new_tr, fill_color=BLUE, fill_opacity=0.7, stroke_color=BLUE, stroke_width=2
        ).move_to((ORIGIN + (UP * 0.5)))

        # Extract the freshly centered vertices to build the dashed lines
        iso_bl = iso_t1.get_vertices()[0]
        iso_br = iso_t1.get_vertices()[1]
        iso_tr = iso_t1.get_vertices()[2]
        iso_tl = iso_bl + (iso_tr - iso_br)  # Top-left vertex relative to the centered triangle

        iso_dashed_top = DashedLine(iso_tl, iso_tr, color=GREY_D, stroke_width=2)
        iso_dashed_left = DashedLine(iso_bl, iso_tl, color=GREY_D, stroke_width=2)

        # Build braces using the perfectly centered edges
        iso_base_edge = Line(iso_bl, iso_br)
        iso_height_edge = Line(iso_br, iso_tr)

        iso_base_brace = Brace(iso_base_edge, direction=DOWN, color=GREY_D, buff=0.15)
        iso_base_label = iso_base_brace.get_text("b").set_color(GREY_D)

        iso_height_brace = Brace(iso_height_edge, direction=RIGHT, color=GREY_D, buff=0.15)
        iso_height_label = iso_height_brace.get_text("b").set_color(GREY_D)

        # Morph everything smoothly into the center layout
        self.play(
            FadeOut(final_formula),
            FadeOut(box),
            Transform(t1, iso_t1),
            Transform(dashed_top, iso_dashed_top),
            Transform(dashed_left, iso_dashed_left),
            Transform(tri_base_brace, iso_base_brace),
            Transform(tri_base_label, iso_base_label),
            Transform(tri_height_brace, iso_height_brace),
            Transform(tri_height_label, iso_height_label),
            run_time=2,
        )
        self.wait(1)

        self.play(
            Write(iso_intro),
        )
        self.wait()

        # Simplified formula group
        iso_triangle_group = VGroup(
            t1, dashed_top, dashed_left, tri_base_brace, tri_base_label, tri_height_brace, tri_height_label
        )

        iso_formula = (
            MathTex(
                r"\text{Area} = \frac{1}{2} \times b \times b = \frac{1}{2} b^2",
            )
            .scale(0.9)
            .next_to(iso_triangle_group, DOWN, buff=0.6)
        )

        iso_box = SurroundingRectangle(
            iso_formula,
            color=BLUE,
            buff=0.2,
            corner_radius=0.1,
        )

        # Final reveal
        self.play(Write(iso_formula), run_time=1.5)
        self.play(Create(iso_box), run_time=1)
        self.wait(3)


class ShadedTriangleAreaQuestion(MovingCameraScene):
    """Shaded Area of Two Right-Angled Triangles (Practice Question)

    ---------------------------------------------------------------
    Features:
    - Pure Vanilla Manim.
    - Positioned nicely in the top-right quadrant below the text.
    - Scaled down to be more compact.
    - Unfilled dark outlines for the rectangles.
    - Accurately proportioned base segments (2 vs 3).
    - Dark-colored braces and numerical text.
    - Blue text hint positioned on the left below the question.
    """

    def setup(self):
        """Initializes scene configurations."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        # =========================================================
        # 1. THE QUESTION (top of frame)
        # =========================================================
        question = Text(
            "Find the area of the shaded region inside the rectangle in the figure below.",
            font_size=35,
        ).to_edge(UP, buff=0.6)

        if question.width > config.frame_width * 0.9:
            question.width = config.frame_width * 0.9

        self.play(Write(question), run_time=1.5)

        # =========================================================
        # 2. GEOMETRY DEFINITION (Top Right & Compact Scale)
        # =========================================================
        # Global controls for positioning shifted to the top-right
        cx, cy = 3.5, 1.0
        scale_factor = 0.8  # Shrinks the overall footprint

        # Accurate math scaling: height = 2, left_width = 2, right_width = 3
        h_val = 2.0 * scale_factor
        w1_val = 2.0 * scale_factor
        w2_val = 3.0 * scale_factor

        # Standard Cartesian vectors for pure positioning without a grid object
        center_point = np.array([cx, cy, 0])

        bottom_left = center_point + np.array([-w1_val, -h_val / 2, 0])
        foot_m = center_point + np.array([0, -h_val / 2, 0])
        bottom_right = center_point + np.array([w2_val, -h_val / 2, 0])
        apex = center_point + np.array([0, h_val / 2, 0])
        top_left = center_point + np.array([-w1_val, h_val / 2, 0])
        top_right = center_point + np.array([w2_val, h_val / 2, 0])

        # Bounding rectangle outline (UNFILLED, dark stroke)
        outline_rect = Polygon(
            bottom_left,
            bottom_right,
            top_right,
            top_left,
            fill_opacity=0.0,
            stroke_width=4,
        )

        # Faint inner vertical dividing line (dark stroke)
        divider = Line(foot_m, apex, stroke_width=3)

        # The two RED right-angled triangles
        tri_left = Polygon(
            bottom_left,
            foot_m,
            apex,
            fill_color=RED,
            fill_opacity=0.85,
            stroke_width=2,
        )
        tri_right = Polygon(
            foot_m,
            bottom_right,
            apex,
            fill_color=RED,
            fill_opacity=0.85,
            stroke_width=2,
        )

        # Small right-angle marker at the foot of the divider
        ra_side = 0.20 * scale_factor
        right_angle = Square(side_length=ra_side, stroke_width=2, fill_opacity=0)
        right_angle.move_to(foot_m + UP * (ra_side / 2) + RIGHT * (ra_side / 2))

        # Layered from background structural lines to foreground red fills
        diagram_shapes = VGroup(outline_rect, divider, tri_left, tri_right, right_angle)

        # =========================================================
        # 3. DARK DIMENSIONS & BRACES
        # =========================================================
        # Left base segment (2)
        left_base_brace = Brace(Line(bottom_left, foot_m), direction=DOWN, buff=0.15)
        left_base_label = left_base_brace.get_text("2")

        # Right base segment (3) - visibly longer
        right_base_brace = Brace(Line(foot_m, bottom_right), direction=DOWN, buff=0.15)
        right_base_label = right_base_brace.get_text("3")

        # Height brace (2) - only on the left side
        height_brace = Brace(Line(bottom_left, top_left), direction=LEFT, buff=0.15)
        height_label = height_brace.get_text("2")

        dims = VGroup(
            left_base_brace,
            left_base_label,
            right_base_brace,
            right_base_label,
            height_brace,
            height_label,
        )

        # =========================================================
        # 4. ANIMATION DISPLAY
        # =========================================================
        self.play(FadeIn(diagram_shapes), run_time=1.5)
        self.play(FadeIn(dims), run_time=1)

        self.wait(4)

        # =========================================================
        # 3. THE HINT (Blue, below question, aligned left)
        # =========================================================
        hint = Text(
            "Hint: Notice there are two right-angled triangles.",
            font_size=24,
            color=BLUE,
        )
        # Position it dynamically below the question, aligned with the left edge of the question
        hint.next_to(question, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(FadeIn(hint), run_time=1.0)

        # ---- 3 second gap before the diagram appears ----
        self.wait(3)


class AreaArbitraryTriangle(MovingCameraScene):
    """
    Area of an Arbitrary Triangle Animation
    --------------------------------------
    Concept:
        Deriving the area formula of an arbitrary triangle by enclosing it in a
        rectangle and splitting it into two simpler right-angled triangles.

    Flow:
    1. Title: "Area of Arbitrary Triangle"
    2. Environment & Grid Setup: Faded infinite coordinate grid.
    3. Intro Diagram: Display an arbitrary triangle with external height and base markers.
    4. Bounding Rectangle: Enclose the triangle in a 5x2 bounding rectangle.
    5. Splitting: Split the rectangle and triangle vertically from the triangle's apex.
    6. Separation: Physically separate the two resulting right-angled triangle/rectangle pairs ($R_1, T_1$ and $R_2, T_2$).
    7. Algebraic Link: Show that each right triangle is exactly half of its bounding sub-rectangle.
    8. Recomposition: Merge the sub-rectangles and sub-triangles back into a unified shape.
    9. Final Substitution: Substitute $R = b \times h$ to arrive at $\text{Area} = \frac{1}{2} \times b \times h$.
    """

    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        # =========================================================
        # TITLE
        # =========================================================

        title = Text("Area of an Arbitrary Triangle", font_size=64, weight=BOLD)

        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # =========================================================
        # 1. ENVIRONMENT & GRID SETUP
        # =========================================================
        grid = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-12, 12, 1],
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )
        self.add(grid)

        # =========================================================
        # 2. INTRO DIAGRAM: a normal (non-right) triangle with base,
        #    height marked OUTSIDE on the right, and "Area = ?"
        # =========================================================
        intro_bl = grid.c2p(-2, -1.2)
        intro_br = grid.c2p(2, -1.2)
        intro_apex = grid.c2p(-0.5, 1.6)

        intro_tri = Polygon(
            intro_bl,
            intro_br,
            intro_apex,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        # Height mark: a vertical dotted line rising straight up from the
        # triangle's lower-right point to the apex's height, tied back to the
        # apex with a dotted horizontal line so it's clearly the same height.
        height_top = grid.c2p(2, 1.6)  # directly above intro_br, level with the apex
        apex_connector = DashedLine(intro_apex, height_top, color=GREY_D, stroke_width=2)
        height_line = DashedLine(intro_br, height_top, color=GREY_D, stroke_width=2)

        intro_base_brace = Brace(Line(intro_bl, intro_br), direction=DOWN, color=GREY_D, buff=0.15)
        intro_base_label = intro_base_brace.get_text("b").set_color(GREY_D)

        intro_height_brace = Brace(height_line, direction=RIGHT, color=GREY_D, buff=0.15)
        intro_height_label = intro_height_brace.get_text("h").set_color(GREY_D)

        area_q = MathTex(r"\text{Area} = \, ?").next_to(intro_base_label, DOWN, buff=0.6)

        self.play(FadeIn(intro_tri), run_time=1)
        self.play(FadeIn(intro_base_brace), Write(intro_base_label), run_time=1)
        self.play(Create(apex_connector), run_time=0.8)
        self.play(FadeIn(intro_height_brace), Write(intro_height_label), run_time=1)
        self.play(Write(area_q))
        self.wait(2)

        intro_group = VGroup(
            intro_tri,
            apex_connector,
            intro_base_brace,
            intro_base_label,
            intro_height_brace,
            intro_height_label,
            area_q,
        )
        self.play(FadeOut(intro_group), run_time=1)

        # =========================================================
        # 3. THE TRIANGLE, DRAWN FIRST
        #    (same geometry the rectangle will later wrap around: the
        #    apex sits 3 units left of the rectangle's top-right point)
        # =========================================================
        r_bl = grid.c2p(-2.5, -0.2)
        r_br = grid.c2p(2.5, -0.2)
        r_tr = grid.c2p(2.5, 1.8)
        r_tl = grid.c2p(-2.5, 1.8)
        apex = grid.c2p(-0.5, 1.8)  # top_right is at x=2.5, so apex_x = 2.5 - 3 = -0.5
        foot = grid.c2p(-0.5, -0.2)  # foot of the apex on the base

        main_tri = Polygon(
            r_bl,
            r_br,
            apex,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        self.play(FadeIn(main_tri), run_time=1.2)
        self.wait(1)

        # =========================================================
        # 4. NOW BRING IN A RECTANGLE AROUND IT (black), 5 x 2 —
        #    and only once it's there, label it b (bottom) and h (right side)
        # =========================================================
        rect_caption = Text("Let's draw a rectangle around the triangle.", font_size=28).to_edge(UP, buff=0.6)

        rect_outline = Polygon(
            r_bl,
            r_br,
            r_tr,
            r_tl,
            fill_opacity=0,
            stroke_width=4,
        )

        self.play(Write(rect_caption))
        self.play(Create(rect_outline), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(rect_caption))

        base_brace = Brace(Line(r_bl, r_br), direction=DOWN, color=GREY_D, buff=0.15)
        base_label = base_brace.get_text("b").set_color(GREY_D)

        height_brace = Brace(Line(r_br, r_tr), direction=RIGHT, color=GREY_D, buff=0.15)
        height_label = height_brace.get_text("h").set_color(GREY_D)

        self.play(FadeIn(base_brace), Write(base_label), run_time=1)
        self.play(FadeIn(height_brace), Write(height_label), run_time=1)
        self.wait(1.5)

        # =========================================================
        # 5. SPLIT THE RECTANGLE WHERE THE APEX SITS
        #    Left piece: 2 x 2   |   Right piece: 3 x 2
        #    The pieces are PHYSICALLY pulled apart, each one keeping
        #    its right-angled triangle inside it.
        # =========================================================
        split_text = Text("Split the rectangle right where the apex sits.", font_size=28).to_edge(DOWN, buff=0.6)
        self.play(Write(split_text))

        split_line = Line(foot, apex, color=BLACK, stroke_width=3)
        self.play(Create(split_line), run_time=1)
        self.wait(1)
        self.play(FadeOut(split_text))

        # The whole-rectangle braces no longer describe a single piece, so retire them.
        self.play(
            FadeOut(base_brace),
            FadeOut(base_label),
            FadeOut(height_brace),
            FadeOut(height_label),
            run_time=0.8,
        )

        # Rebuild the same two regions as self-contained, separable pieces.

        tri_1 = Polygon(
            r_bl,
            foot,
            apex,
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_color=BLUE,
            stroke_width=3,
        )
        tri_2 = Polygon(
            foot,
            r_br,
            apex,
            fill_color=RED,
            fill_opacity=0.6,
            stroke_color=RED,
            stroke_width=3,
        )

        rect_1 = Polygon(
            r_bl,
            foot,
            apex,
            r_tl,
            stroke_width=3,
        )

        rect_2 = Polygon(
            foot,
            r_br,
            r_tr,
            apex,
            stroke_width=3,
        )

        self.play(
            FadeOut(rect_outline),
            FadeOut(main_tri),
            FadeOut(split_line),
            FadeIn(tri_1),
            FadeIn(rect_1),
            FadeIn(tri_2),
            FadeIn(rect_2),
            run_time=1,
        )
        self.wait(0.5)

        r1_shapes = VGroup(tri_1, rect_1)
        r2_shapes = VGroup(tri_2, rect_2)

        split_shift = 0.8
        split_lift = 0.5
        self.play(
            r1_shapes.animate.shift(LEFT * split_shift + UP * split_lift),
            r2_shapes.animate.shift(RIGHT * split_shift + UP * split_lift),
            run_time=1.5,
        )
        self.wait(0.5)

        # Labels sit OUTSIDE each piece: R above, T below.
        r1_label = MathTex("R_1").next_to(rect_1, UP, buff=0.25)
        t1_label = MathTex("T_1", color=BLUE).next_to(rect_1, DOWN, buff=0.25)
        r2_label = MathTex("R_2").next_to(rect_2, UP, buff=0.25)
        t2_label = MathTex("T_2", color=RED).next_to(rect_2, DOWN, buff=0.25)

        self.play(Write(r1_label), Write(r2_label))
        self.wait(0.5)
        self.play(Write(t1_label), Write(t2_label))
        self.wait(1.5)

        # =========================================================
        # A quick index/key for what each label means, before the algebra.
        # =========================================================
        figure_group = VGroup(r1_shapes, r2_shapes, r1_label, r2_label, t1_label, t2_label)

        index_text = Text(
            "R\u2081 = rectangle      T\u2081 = right-angled triangle inside R\u2081\n"
            "R\u2082 = rectangle      T\u2082 = right-angled triangle inside R\u2082",
            font_size=24,
            line_spacing=1.2,
        ).next_to(figure_group, DOWN, buff=0.6)

        self.play(Write(index_text))
        self.wait(2.5)
        self.play(FadeOut(index_text))

        # =========================================================
        # 6. THE ALGEBRA: EACH RIGHT TRIANGLE IS HALF ITS RECTANGLE
        # =========================================================
        eq1 = MathTex(r"T_1", r"=", r"\frac{1}{2}", r"R_1").set_color_by_tex_to_color_map({"T_1": BLUE})
        eq2 = MathTex(r"T_2", r"=", r"\frac{1}{2}", r"R_2").set_color_by_tex_to_color_map({"T_2": RED})

        eq_group = VGroup(eq1, eq2).arrange(RIGHT, buff=1.2).next_to(figure_group, DOWN, buff=0.7)

        self.play(Write(eq1))
        self.wait(0.5)
        self.play(Write(eq2))
        self.wait(1.5)

        sum_eq = MathTex(
            r"T_1", r"+", r"T_2", r"=", r"\frac{1}{2}", r"(", r"R_1", r"+", r"R_2", r")"
        ).set_color_by_tex_to_color_map({"T_1": BLUE, "T_2": RED})
        sum_eq.next_to(eq_group, DOWN, buff=0.5)

        self.play(Write(sum_eq), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(eq1), FadeOut(eq2), sum_eq.animate.move_to(eq_group.get_center()))
        self.wait(1)

        # =========================================================
        # 7. RECOGNIZE THE WHOLE: R1 + R2 = R, T1 + T2 = T
        #    Physically JOIN the two rectangle pieces back together
        #    (staying at the same lifted height — no dropping back down)
        #    while the equation collapses to T = 1/2 R. The two split
        #    triangle halves are retired and replaced by one fresh,
        #    single triangle inside the reunited rectangle.
        # =========================================================
        note_text = Text(
            "R\u2081 + R\u2082 is just the original rectangle, R.\nT\u2081 + T\u2082 is just the original triangle, T.",
            font_size=26,
            line_spacing=1.2,
        ).next_to(sum_eq, DOWN, buff=0.6)

        self.play(Write(note_text))
        self.wait(2.5)

        # Strip the color from the bare rectangle pieces, leaving plain frames.
        self.play(
            FadeOut(r1_label),
            FadeOut(t1_label),
            FadeOut(r2_label),
            FadeOut(t2_label),
            FadeOut(note_text),
            rect_1.animate.set_fill(opacity=0).set_stroke(color=GREY_D, width=3),
            rect_2.animate.set_fill(opacity=0).set_stroke(color=GREY_D, width=3),
            run_time=1,
        )
        self.wait(0.3)

        # Slide the two rectangle+triangle pieces back together — horizontally
        # only, so the whole figure stays up at the lifted height.

        # Label the reunited rectangle's base and height.
        merged_shift = UP * split_lift
        m_bl = r_bl + merged_shift
        m_br = r_br + merged_shift
        m_tr = r_tr + merged_shift
        m_apex = apex + merged_shift

        merged_base_brace = Brace(Line(m_bl, m_br), direction=DOWN, color=GREY_D, buff=0.15)
        merged_base_label = merged_base_brace.get_text("b").set_color(GREY_D)

        merged_height_brace = Brace(Line(m_br, m_tr), direction=RIGHT, color=GREY_D, buff=0.15)
        merged_height_label = merged_height_brace.get_text("h").set_color(GREY_D)

        VGroup(
            rect_1,
            rect_2,
            tri_1,
            tri_2,
            merged_base_brace,
            merged_base_label,
            merged_height_brace,
            merged_height_label,
        )

        self.play(
            r1_shapes.animate.shift(RIGHT * split_shift),
            r2_shapes.animate.shift(LEFT * split_shift),
            run_time=1.8,
        )
        self.wait(0.5)

        # =========================================================
        # 8. FINAL REVEAL: SUBSTITUTE R = b x h
        #    Swap the two triangle halves for one single, seamless
        #    triangle right as the final formula appears.
        # =========================================================
        merged_tri = Polygon(
            m_bl,
            m_br,
            m_apex,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        self.play(
            FadeOut(tri_1),
            FadeOut(tri_2),
            FadeIn(merged_tri),
        )

        self.play(FadeIn(merged_base_brace), Write(merged_base_label), run_time=1)
        self.play(FadeIn(merged_height_brace), Write(merged_height_label), run_time=1)
        self.wait(1.5)

        final_eq = MathTex(r"T", r"=", r"\frac{1}{2}", r"R").set_color_by_tex_to_color_map({"T": BLUE})
        final_eq.move_to(sum_eq.get_center())

        self.play(ReplacementTransform(sum_eq, final_eq))

        # conclusion
        rectangle_formula = (
            MathTex(
                r"\text{We know, Area of R} = b \times h",
            )
            .scale(0.9)
            .next_to(final_eq, DOWN, buff=0.5)
        )
        self.play(Write(rectangle_formula))
        self.wait(3)

        final_formula = (
            MathTex(
                r"\text{Area of Triangle} = \frac{1}{2} \times b \times h",
            )
            .scale(0.9)
            .next_to(merged_base_brace, DOWN, buff=1.5)
        )

        box = SurroundingRectangle(
            final_formula,
            color=BLUE,
            buff=0.2,
            corner_radius=0.1,
        )

        self.play(
            FadeOut(final_eq),
            FadeOut(rectangle_formula),
        )

        self.play(
            FadeIn(final_formula),
            Create(box),
        )
        self.wait(6)


class AreaEquilateralTriangle(MovingCameraScene):
    """
    Area of an Equilateral Triangle
    -------------------------------
    Concept:
        Derive the area formula of an equilateral triangle by expressing
        its height using the Pythagorean theorem and substituting it into
        the general triangle area formula.

    Flow:
    1. Title
    2. Introduce an equilateral triangle
    3. Label all three sides as a
    4. Pose the area problem
    5. Recall the general area formula
    6. Substitute the base (b = a)
    7. Split the triangle along its altitude
    8. Form a right triangle
    9. Label hypotenuse, base, and height
    10. Apply the Pythagorean theorem
    11. Solve for the height
    12. Substitute the height into the area formula
    13. Simplify to A = (√3/4)a²
    14. Highlight the final formula
    15. End with the complete equilateral triangle and derived result

    Author:
        Bipin Thapa
    """

    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        # =========================================================
        # TITLE
        # =========================================================

        title = Text("Area of Equilateral Triangle", font_size=56, weight=BOLD)

        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # =========================================================
        # 1. ENVIRONMENT & GRID SETUP
        # =========================================================
        grid = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-12, 12, 1],
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )
        self.add(grid)

        # Shared geometry for an equilateral triangle of side length "a"
        side = 3.4
        half_base = side / 2
        height_val = (3**0.5) / 2 * side

        # =========================================================
        # 2. INTRO: EQUILATERAL TRIANGLE, ALL SIDES LABELED a
        # =========================================================
        B = grid.c2p(-half_base, -1)
        C = grid.c2p(half_base, -1)
        A = grid.c2p(0, -1 + height_val)

        main_tri = Polygon(
            B,
            C,
            A,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        mid_BA = (B + A) / 2
        mid_AC = (A + C) / 2
        mid_BC = (B + C) / 2

        label_a_left = MathTex("a").move_to(mid_BA + LEFT * 0.4)
        label_a_right = MathTex("a").move_to(mid_AC + RIGHT * 0.4)
        label_a_bottom = MathTex("a").move_to(mid_BC + DOWN * 0.4)

        area_q = MathTex(r"\text{Area} = \, ?").next_to(main_tri, DOWN, buff=1.0)

        self.play(FadeIn(main_tri), run_time=1)
        self.play(Write(label_a_left), Write(label_a_right), Write(label_a_bottom), run_time=1)
        self.wait(1)
        self.play(Write(area_q))
        self.wait(2)

        intro_group = VGroup(main_tri, label_a_left, label_a_right, label_a_bottom, area_q)
        self.play(FadeOut(intro_group), run_time=1)

        # =========================================================
        # 3. GENERIC FORMULA, THEN SUBSTITUTE b = a  (h STILL UNKNOWN)
        #    This becomes the first line of a running derivation
        #    stacked down the right side of the frame.
        # =========================================================
        generic_formula = MathTex("A", "=", r"\frac{1}{2}", r"\times", "b", r"\times", "h")
        self.play(Write(generic_formula))
        self.wait(1)

        note_b = MathTex("b = a").next_to(generic_formula, DOWN, buff=0.5)
        note_h = MathTex(r"h = \, ?").next_to(note_b, DOWN, buff=0.3)
        self.play(Write(note_b))
        self.wait(0.5)
        self.play(Write(note_h))
        self.wait(1.5)

        substituted_formula = MathTex("A", "=", r"\frac{1}{2}", r"\times", "a", r"\times", "h")
        substituted_formula.move_to(generic_formula)
        self.play(ReplacementTransform(generic_formula, substituted_formula), FadeOut(note_b))
        self.wait(1)

        self.play(
            substituted_formula.animate.scale(0.75).move_to(UP * 3 + RIGHT * 3.3),
            FadeOut(note_h),
            run_time=1,
        )
        self.wait(0.5)

        # =========================================================
        # 4. FIND h: SPLIT THE TRIANGLE ALONG ITS ALTITUDE
        #    Shifted to the LEFT side of the frame, leaving the right
        #    side free for the growing derivation stack.
        # =========================================================
        tri_x_shift = -3.3
        row2_y = -0.3  # shift this one number to move the diagram up/down
        B2 = grid.c2p(tri_x_shift - half_base, row2_y)
        C2 = grid.c2p(tri_x_shift + half_base, row2_y)
        A2 = grid.c2p(tri_x_shift, row2_y + height_val)
        D2 = grid.c2p(tri_x_shift, row2_y)

        tri2 = Polygon(
            B2,
            C2,
            A2,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(tri2), run_time=1)
        self.wait(0.5)

        altitude = DashedLine(A2, D2, color=GREY_D, stroke_width=2)
        self.play(Create(altitude), run_time=1)
        self.wait(1)

        left_half = Polygon(
            B2,
            D2,
            A2,
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_color=BLUE,
            stroke_width=4,
        )
        right_half = Polygon(
            D2,
            C2,
            A2,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        self.play(FadeOut(tri2), FadeOut(altitude), FadeIn(left_half), FadeIn(right_half), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(right_half), run_time=1.2)
        self.wait(0.5)

        right_angle = RightAngle(Line(D2, B2), Line(D2, A2), length=0.25, color=GREY_D)
        self.play(Create(right_angle), run_time=0.8)
        self.wait(0.5)

        # Label the right triangle's three sides: hypotenuse a, base a/2, height h
        mid_BA2 = (B2 + A2) / 2
        label_hyp = MathTex("a").move_to(mid_BA2 + LEFT * 0.4)

        base_brace2 = Brace(Line(B2, D2), direction=DOWN, color=GREY_D, buff=0.15)
        base_label2 = base_brace2.get_tex(r"\frac{a}{2}").set_color(GREY_D)

        height_brace2 = Brace(Line(D2, A2), direction=RIGHT, color=GREY_D, buff=0.15)
        height_label2 = height_brace2.get_tex("h").set_color(GREY_D)

        self.play(Write(label_hyp), run_time=0.8)
        self.play(FadeIn(base_brace2), Write(base_label2), run_time=1)
        self.play(FadeIn(height_brace2), Write(height_label2), run_time=1)
        self.wait(1.5)

        triangle_group = VGroup(left_half, right_angle, label_hyp, base_brace2, base_label2, height_brace2, height_label2)

        # =========================================================
        # 5. PYTHAGORAS: SOLVE FOR h
        #    Each new line is WRITTEN below the previous one and stays
        #    on screen — nothing is replaced/transformed in place.
        # =========================================================
        eq_font = 30

        eq1 = MathTex("H^2 = P^2 + B^2", font_size=eq_font)
        eq1.next_to(substituted_formula, DOWN, buff=0.35)
        self.play(Write(eq1))
        self.wait(1)

        eq2 = MathTex(r"a^2 = \left(\frac{a}{2}\right)^2 + h^2", font_size=eq_font)
        eq2.next_to(eq1, DOWN, buff=0.25)
        self.play(Write(eq2))
        self.wait(1)

        eq3 = MathTex(r"h^2 = a^2 - \left(\frac{a}{2}\right)^2", font_size=eq_font)
        eq3.next_to(eq2, DOWN, buff=0.25)
        self.play(Write(eq3))
        self.wait(1)

        eq4 = MathTex(r"h^2 = a^2 - \frac{a^2}{4}", font_size=eq_font)
        eq4.next_to(eq3, DOWN, buff=0.25)
        self.play(Write(eq4))
        self.wait(1)

        eq5 = MathTex(r"h^2 = \frac{3a^2}{4}", font_size=eq_font)
        eq5.next_to(eq4, DOWN, buff=0.25)
        self.play(Write(eq5))
        self.wait(1)

        eq6 = MathTex(r"h = \frac{\sqrt{3}}{2}\,a", font_size=eq_font)
        eq6.next_to(eq5, DOWN, buff=0.25)
        self.play(Write(eq6))
        self.wait(0.5)

        box_h = SurroundingRectangle(eq6, color=BLUE, buff=0.12, corner_radius=0.06)
        self.play(Create(box_h))
        self.wait(1.5)

        # =========================================================
        # 6. PLUG h BACK INTO THE AREA FORMULA
        #    The triangle and the derivation stack both stay on screen;
        #    the final result is highlighted separately, front and center.
        # =========================================================
        final1 = MathTex(r"A = \frac{1}{2} \times a \times \frac{\sqrt{3}}{2}a", font_size=eq_font)
        final1.next_to(box_h, DOWN, buff=0.35)
        self.play(Write(final1))
        self.wait(1.5)

        final2 = MathTex(r"A = \frac{\sqrt{3}}{4}a^2", font_size=44).move_to(ORIGIN)
        self.play(Write(final2))
        self.wait(1)

        final_box = SurroundingRectangle(final2, color=BLUE, buff=0.2, corner_radius=0.1)
        self.play(Create(final_box))
        self.wait(2)

        # =========================================================
        # 7. FRESH CLOSING SCENE: THE WHOLE TRIANGLE, LABELED,
        #    WITH THE RESULT WRITTEN BELOW IT
        # =========================================================
        self.play(
            FadeOut(triangle_group),
            FadeOut(substituted_formula),
            FadeOut(eq1),
            FadeOut(eq2),
            FadeOut(eq3),
            FadeOut(eq4),
            FadeOut(eq5),
            FadeOut(eq6),
            FadeOut(box_h),
            FadeOut(final1),
            FadeOut(final2),
            FadeOut(final_box),
            run_time=1,
        )
        self.wait(0.5)

        Bf = grid.c2p(-half_base, -1)
        Cf = grid.c2p(half_base, -1)
        Af = grid.c2p(0, -1 + height_val)

        final_tri = Polygon(
            Bf,
            Cf,
            Af,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        mid_BAf = (Bf + Af) / 2
        mid_ACf = (Af + Cf) / 2
        mid_BCf = (Bf + Cf) / 2

        label_a_left_f = MathTex("a").move_to(mid_BAf + LEFT * 0.4)
        label_a_right_f = MathTex("a").move_to(mid_ACf + RIGHT * 0.4)
        label_a_bottom_f = MathTex("a").move_to(mid_BCf + DOWN * 0.4)

        self.play(FadeIn(final_tri), run_time=1)
        self.play(Write(label_a_left_f), Write(label_a_right_f), Write(label_a_bottom_f), run_time=1)
        self.wait(1)

        final_result = MathTex(r"A = \frac{\sqrt{3}}{4}a^2", font_size=40).next_to(final_tri, DOWN, buff=0.8)
        result_box = SurroundingRectangle(final_result, color=BLUE, buff=0.2, corner_radius=0.1)

        self.play(Write(final_result), Create(result_box))
        self.wait(6)


class AreaIsoscelesTriangle(MovingCameraScene):
    """
    Area of an Isosceles Triangle
    -----------------------------
    Concept:
        Derive the area formula of an isosceles triangle by expressing
        its height using the Pythagorean theorem and substituting it into
        the general triangle area formula.

    Flow:
    1. Title
    2. Introduce an isosceles triangle
    3. Label equal sides as a and base as b
    4. Pose the area problem
    5. Recall the general area formula
    6. Identify the unknown height
    7. Split the triangle along its altitude
    8. Form a right triangle
    9. Label hypotenuse, half-base, and height
    10. Apply the Pythagorean theorem
    11. Solve for the height
    12. Substitute the height into the area formula
    13. Simplify to A = b√(4a² − b²)/4
    14. Highlight the derived formula
    15. End with the complete isosceles triangle and final result

    """

    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        # =========================================================
        # TITLE
        # =========================================================

        title = Text("Area of Isosceles Triangle", font_size=56, weight=BOLD)

        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # =========================================================
        # 1. ENVIRONMENT & GRID SETUP
        # =========================================================
        grid = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-12, 12, 1],
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )
        self.add(grid)

        # Shared geometry: isosceles triangle with equal legs AB = AC = a,
        # and base BC = b.
        base_val = 3.0
        leg_val = 3.3
        half_base = base_val / 2
        height_val = (leg_val**2 - half_base**2) ** 0.5

        # =========================================================
        # 2. INTRO: ISOSCELES TRIANGLE, LEGS LABELED a, BASE LABELED b
        # =========================================================
        B = grid.c2p(-half_base, -1)
        C = grid.c2p(half_base, -1)
        A = grid.c2p(0, -1 + height_val)

        main_tri = Polygon(
            B,
            C,
            A,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        mid_BA = (B + A) / 2
        mid_AC = (A + C) / 2
        mid_BC = (B + C) / 2

        label_a_left = MathTex("a").move_to(mid_BA + LEFT * 0.4)
        label_a_right = MathTex("a").move_to(mid_AC + RIGHT * 0.4)
        label_b_bottom = MathTex("b").move_to(mid_BC + DOWN * 0.4)

        area_q = MathTex(r"\text{Area} = \, ?").next_to(main_tri, DOWN, buff=1.0)

        self.play(FadeIn(main_tri), run_time=1)
        self.play(Write(label_a_left), Write(label_a_right), Write(label_b_bottom), run_time=1)
        self.wait(1)
        self.play(Write(area_q))
        self.wait(2)

        intro_group = VGroup(main_tri, label_a_left, label_a_right, label_b_bottom, area_q)
        self.play(FadeOut(intro_group), run_time=1)

        # =========================================================
        # 3. GENERIC FORMULA  (base is already b; only h is unknown)
        #    This becomes the first line of a running derivation
        #    stacked down the right side of the frame.
        # =========================================================
        generic_formula = MathTex("A", "=", r"\frac{1}{2}", r"\times", "b", r"\times", "h")
        self.play(Write(generic_formula))
        self.wait(1)

        note_h = MathTex(r"h = \, ?").next_to(generic_formula, DOWN, buff=0.4)
        self.play(Write(note_h))
        self.wait(1.5)

        self.play(
            generic_formula.animate.scale(0.65).to_edge(UP).shift(RIGHT * 3.3),
            FadeOut(note_h),
            run_time=1,
        )
        self.wait(0.5)
        substituted_formula = generic_formula

        # =========================================================
        # 4. FIND h: SPLIT THE TRIANGLE ALONG ITS ALTITUDE
        #    Shifted to the LEFT side of the frame, leaving the right
        #    side free for the growing derivation stack.
        # =========================================================
        tri_x_shift = -3.3
        row2_y = -0.3  # shift this one number to move the diagram up/down
        B2 = grid.c2p(tri_x_shift - half_base, row2_y)
        C2 = grid.c2p(tri_x_shift + half_base, row2_y)
        A2 = grid.c2p(tri_x_shift, row2_y + height_val)
        D2 = grid.c2p(tri_x_shift, row2_y)

        tri2 = Polygon(
            B2,
            C2,
            A2,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(tri2), run_time=1)
        self.wait(0.5)

        altitude = DashedLine(A2, D2, color=GREY_D, stroke_width=2)
        self.play(Create(altitude), run_time=1)
        self.wait(1)

        left_half = Polygon(
            B2,
            D2,
            A2,
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_color=BLUE,
            stroke_width=4,
        )
        right_half = Polygon(
            D2,
            C2,
            A2,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        self.play(FadeOut(tri2), FadeOut(altitude), FadeIn(left_half), FadeIn(right_half), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(right_half), run_time=1.2)
        self.wait(0.5)

        right_angle = RightAngle(Line(D2, B2), Line(D2, A2), length=0.25, color=GREY_D)
        self.play(Create(right_angle), run_time=0.8)
        self.wait(0.5)

        # Label the right triangle's three sides: hypotenuse a, base b/2, height h
        mid_BA2 = (B2 + A2) / 2
        label_hyp = MathTex("a").move_to(mid_BA2 + LEFT * 0.4)

        base_brace2 = Brace(Line(B2, D2), direction=DOWN, color=GREY_D, buff=0.15)
        base_label2 = base_brace2.get_tex(r"\frac{b}{2}").set_color(GREY_D)

        height_brace2 = Brace(Line(D2, A2), direction=RIGHT, color=GREY_D, buff=0.15)
        height_label2 = height_brace2.get_tex("h").set_color(GREY_D)

        self.play(Write(label_hyp), run_time=0.8)
        self.play(FadeIn(base_brace2), Write(base_label2), run_time=1)
        self.play(FadeIn(height_brace2), Write(height_label2), run_time=1)
        self.wait(1.5)

        triangle_group = VGroup(left_half, right_angle, label_hyp, base_brace2, base_label2, height_brace2, height_label2)

        # =========================================================
        # 5. PYTHAGORAS: SOLVE FOR h
        #    Each new line is WRITTEN below the previous one and stays
        #    on screen — nothing is replaced/transformed in place.
        # =========================================================
        eq_font = 30

        eq1 = MathTex("H^2 = P^2 + B^2", font_size=eq_font)
        eq1.next_to(substituted_formula, DOWN, buff=0.35)
        self.play(Write(eq1))
        self.wait(1)

        eq2 = MathTex(r"a^2 = \left(\frac{b}{2}\right)^2 + h^2", font_size=eq_font)
        eq2.next_to(eq1, DOWN, buff=0.25)
        self.play(Write(eq2))
        self.wait(1)

        eq3 = MathTex(r"h^2 = a^2 - \left(\frac{b}{2}\right)^2", font_size=eq_font)
        eq3.next_to(eq2, DOWN, buff=0.25)
        self.play(Write(eq3))
        self.wait(1)

        eq4 = MathTex(r"h^2 = a^2 - \frac{b^2}{4}", font_size=eq_font)
        eq4.next_to(eq3, DOWN, buff=0.25)
        self.play(Write(eq4))
        self.wait(1)

        eq5 = MathTex(r"h^2 = \frac{4a^2 - b^2}{4}", font_size=eq_font)
        eq5.next_to(eq4, DOWN, buff=0.25)
        self.play(Write(eq5))
        self.wait(1)

        eq6 = MathTex(r"h = \frac{\sqrt{4a^2 - b^2}}{2}", font_size=eq_font)
        eq6.next_to(eq5, DOWN, buff=0.25)
        self.play(Write(eq6))
        self.wait(0.5)

        box_h = SurroundingRectangle(eq6, color=BLUE, buff=0.12, corner_radius=0.06)
        self.play(Create(box_h))

        box_substituted_formula = SurroundingRectangle(substituted_formula, color=BLUE, corner_radius=0.06)
        self.play(Create(box_substituted_formula))
        self.wait(1.5)

        # =========================================================
        # 6. PLUG h BACK INTO THE AREA FORMULA
        #    The triangle and the derivation stack both stay on screen;
        #    the final result is highlighted separately, front and center.
        # =========================================================
        final1 = MathTex(r"A = \frac{1}{2} \times b \times \frac{\sqrt{4a^2 - b^2}}{2}", font_size=eq_font).move_to(ORIGIN)
        # final1.next_to(box_h, DOWN, buff=0.35)
        self.play(Write(final1))

        # final2 = MathTex(r"A = \frac{b\sqrt{4a^2 - b^2}}{4}", font_size=44).move_to(ORIGIN)
        # self.play(Write(final2))
        # self.wait(1)

        final_box = SurroundingRectangle(final1, color=BLUE, buff=0.2, corner_radius=0.1)
        self.play(Create(final_box))
        self.wait(2)

        # =========================================================
        # 7. FRESH CLOSING SCENE: THE WHOLE TRIANGLE, LABELED,
        #    WITH THE RESULT WRITTEN BELOW IT
        # =========================================================
        self.play(
            FadeOut(triangle_group),
            FadeOut(substituted_formula),
            FadeOut(eq1),
            FadeOut(eq2),
            FadeOut(eq3),
            FadeOut(eq4),
            FadeOut(eq5),
            FadeOut(eq6),
            FadeOut(box_h),
            FadeOut(final1),
            FadeOut(box_substituted_formula),
            FadeOut(final_box),
            run_time=1,
        )
        self.wait(0.5)

        Bf = grid.c2p(-half_base, -1)
        Cf = grid.c2p(half_base, -1)
        Af = grid.c2p(0, -1 + height_val)

        final_tri = Polygon(
            Bf,
            Cf,
            Af,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )

        mid_BAf = (Bf + Af) / 2
        mid_ACf = (Af + Cf) / 2
        mid_BCf = (Bf + Cf) / 2

        label_a_left_f = MathTex("a").move_to(mid_BAf + LEFT * 0.4)
        label_a_right_f = MathTex("a").move_to(mid_ACf + RIGHT * 0.4)
        label_b_bottom_f = MathTex("b").move_to(mid_BCf + DOWN * 0.4)

        final_tri_group = Group(final_tri, label_a_left_f, label_a_right_f, label_b_bottom_f).to_edge(UP * 0.3)

        self.play(FadeIn(final_tri_group), run_time=1)
        # self.play(Write(label_a_left_f), Write(label_a_right_f), Write(label_b_bottom_f), run_time=1)
        self.wait(1)

        final_result = MathTex(r"A = \frac{b\sqrt{4a^2 - b^2}}{4}", font_size=40).next_to(final_tri, DOWN, buff=1.5)
        result_box = SurroundingRectangle(final_result, color=BLUE, buff=0.2, corner_radius=0.1)

        self.play(Write(final_result), Create(result_box))
        self.wait(6)
