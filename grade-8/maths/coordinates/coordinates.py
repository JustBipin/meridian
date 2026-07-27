from manim import *
from manim_themes.manim_theme import apply_theme


class CoordinateGeometryIntro(MovingCameraScene):
    """
    Coordinate Geometry Intro Animation
        -----------------------------------
        Concept:
            An intuitive introduction to coordinates, the Cartesian plane,
            reading coordinates, and deriving the distance formula using
            Pythagoras' theorem from first principles.

        Flow:
        1. Mathematical coordinate plane environment setup
        2. X-axis representation and positive/negative distance analysis
        3. Y-axis representation and vertical distance analysis
        4. Reading multiple coordinates across quadrants
        5. Distance from the origin calculated using Pythagoras theorem
        6. Distance between two points using a custom triangle construction
        7. Deriving the general distance formula for points (x1, y1) and (x2, y2)
    """

    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        # Initial setups
        self.camera.frame.save_state()

        # ===================================================
        #  1. Mathematical coordinate plane environment setup
        # ===================================================
        title = Text("Co-ordinate ", font_size=56, weight=BOLD)

        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        self.play(self.camera.frame.animate.scale(3))
        grid = NumberPlane(
            x_range=[-1000, 1000, 1],
            y_range=[-500, 500, 1],
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": 2,
                "stroke_opacity": 0.5,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )
        self.play(FadeIn(grid))
        self.play(self.camera.frame.animate.scale(2 / 3), run_time=1.5)
        self.wait(3)

        origin = grid.c2p(0, 0)
        o_dot = Dot(origin, color=TEAL, radius=0.08)
        o_label = MathTex("Origin").next_to(o_dot, DOWN + RIGHT, buff=0.1)

        self.play(FadeIn(o_dot), Write(o_label))
        self.wait(2)
        self.play(Transform(o_label, MathTex("O").next_to(origin, DOWN + RIGHT)))
        self.wait(2)

        # =========================================================
        # 2. X-axis representation and positive/negative distance analysis
        # =========================================================
        x_axis = DoubleArrow(
            start=grid.c2p(-14, 0),
            end=grid.c2p(14, 0),
            buff=0,
            stroke_width=4,
            color=GRAY_D,
            tip_length=0.2,
        )

        x_label = MathTex("X").next_to(x_axis.get_end(), DOWN, buff=0.15)
        neg_x_label = MathTex("-X").next_to(x_axis.get_start(), DOWN, buff=0.15)

        self.play(Create(x_axis), run_time=2)
        self.wait(2)
        self.play(Write(x_label), Write(neg_x_label))
        self.wait(2)

        x_numbers = VGroup()
        for i in range(-13, 14):
            num = Text("" if i == 0 else str(i), font_size=30)
            num.next_to(grid.c2p(i, 0), DOWN, buff=0.15)
            x_numbers.add(num)

        self.play(LaggedStart(*[Write(num) for num in x_numbers], lag_ratio=0.03))
        self.wait(2)

        origin_circle = Circle(radius=0.25, color=YELLOW_E).move_to(origin)
        self.play(Create(origin_circle))
        self.wait(1)

        # Plot point on positive X-axis
        point_right = grid.c2p(5, 0)
        right_dot = Dot(point_right, color=TEAL)
        right_label = MathTex("A(5,0)", color=TEAL).next_to(right_dot, UP, buff=0.2)

        self.play(FadeIn(right_dot), Write(right_label))
        self.wait(1)

        right_distance = Line(origin, point_right, color=TEAL_E, stroke_width=6)
        right_distance_label = MathTex("5").next_to(right_distance.get_center(), UP, buff=0.15)

        self.play(Create(right_distance), Write(right_distance_label))
        self.wait(2)

        narration = Text("5 units to the right of the origin", font_size=30).to_edge(UP)
        self.play(Write(narration))
        self.wait(2)
        self.play(FadeOut(narration))

        # Plot point on negative X-axis
        point_left = grid.c2p(-5, 0)
        left_dot = Dot(point_left, color=RED)
        left_label = MathTex("(-5,0)", color=RED).next_to(left_dot, UP, buff=0.2)

        self.play(FadeIn(left_dot), Write(left_label))
        self.wait(1)

        left_distance = Line(origin, point_left, color=TEAL_E, stroke_width=6)
        left_distance_label = MathTex("5").next_to(left_distance.get_center(), UP, buff=0.15)

        self.play(Create(left_distance), Write(left_distance_label))
        self.wait(2)

        narration = Text("5 units to the left of the origin", font_size=30).to_edge(UP)
        self.play(Write(narration))
        self.wait(2)
        self.play(FadeOut(narration))

        compare_box = VGroup(
            MathTex("Coordinate:"),
            MathTex("5"),
            MathTex("\\quad \\text{and}\\quad"),
            MathTex("-5"),
        ).arrange(RIGHT, buff=0.25)
        compare_box.to_edge(UP)

        self.play(Write(compare_box))
        self.wait(3)
        self.play(FadeOut(compare_box))

        distance_title = MathTex("\\text{But, Distance is 5 for both.}").to_edge(UP)
        self.play(Write(distance_title))
        self.wait(2)
        abs_title = MathTex("\\text{Distance ignores direction}").to_edge(UP)
        self.play(FadeOut(distance_title))
        self.play(FadeIn(abs_title))
        self.wait(2)

        self.play(
            FadeOut(right_dot),
            FadeOut(left_dot),
            FadeOut(right_label),
            FadeOut(left_label),
            FadeOut(right_distance),
            FadeOut(left_distance),
            FadeOut(right_distance_label),
            FadeOut(left_distance_label),
            FadeOut(abs_title),
            FadeOut(origin_circle),
        )
        self.wait(2)

        # =========================================================
        # 3. Y-axis representation and vertical distance analysis
        # =========================================================
        y_axis = DoubleArrow(
            start=grid.c2p(0, -8),
            end=grid.c2p(0, 8),
            buff=0,
            stroke_width=4,
            color=GRAY_D,
            tip_length=0.2,
        )

        y_label = MathTex("Y").next_to(y_axis.get_end(), RIGHT + DOWN, buff=0.15)
        neg_y_label = MathTex("-Y").next_to(y_axis.get_start(), RIGHT + UP, buff=0.15)

        self.play(Create(y_axis), run_time=2)
        self.wait(2)
        self.play(Write(y_label), Write(neg_y_label))
        self.wait(2)

        y_numbers = VGroup()
        for i in range(-7, 8):
            num = Text("" if i == 0 else str(i), font_size=30)
            num.next_to(grid.c2p(0, i), RIGHT, buff=0.15)
            y_numbers.add(num)

        self.play(LaggedStart(*[Write(num) for num in y_numbers], lag_ratio=0.03))
        self.wait(2)

        point = grid.c2p(5, 3)
        point_dot = Dot(point, color=TEAL)
        point_label = MathTex("(5,3)", color=TEAL).next_to(point_dot, UP, buff=0.2)

        self.play(FadeIn(point_dot), Write(point_label))
        self.wait(2)

        height_text = Text("The y-coordinate tells vertical distance", font_size=32).next_to(point_label, UP)
        self.play(Write(height_text))
        self.wait(2)

        y_projection = DashedLine(start=grid.c2p(5, 3), end=grid.c2p(0, 3), color=TEAL_E, stroke_width=3)
        self.play(Create(y_projection))
        self.wait(2)

        y_value = MathTex("y = 3", color=TEAL_E).next_to(grid.c2p(0, 3), LEFT, buff=0.3)
        self.play(Write(y_value))
        self.wait(2)

        vertical_distance = Line(start=grid.c2p(0, 0), end=grid.c2p(0, 3), color=TEAL_E, stroke_width=6)
        vertical_label = MathTex("3").next_to(vertical_distance, LEFT, buff=0.2)
        self.play(Create(vertical_distance), Write(vertical_label))
        self.wait(2)

        positive_text = Text("3 units above the origin", font_size=30).next_to(y_value, UL)
        self.play(Write(positive_text))
        self.wait(3)

        self.play(FadeOut(positive_text, y_value, vertical_distance, vertical_label, y_projection))

        negative_point = grid.c2p(5, -3)
        negative_dot = Dot(negative_point, color=RED)
        negative_label = MathTex("(5,-3)", color=RED).next_to(negative_dot, DOWN, buff=0.2)

        self.play(Transform(point_dot, negative_dot), Transform(point_label, negative_label))
        self.wait(2)

        negative_projection = DashedLine(start=grid.c2p(5, -3), end=grid.c2p(0, -3), color=RED, stroke_width=3)
        self.play(Create(negative_projection))

        negative_y_value = MathTex("y=-3", color=RED).next_to(grid.c2p(0, -3), LEFT, buff=0.3)
        self.play(Write(negative_y_value))
        self.wait(3)

        negative_text = Text("3 units below the origin", font_size=30).next_to(negative_y_value, LEFT + DOWN)
        self.play(FadeOut(height_text), Write(negative_text))
        self.wait(3)
        self.play(FadeOut(negative_text))

        summary = (
            VGroup(MathTex("x = \\text{horizontal distance}"), MathTex("y = \\text{vertical distance}"))
            .arrange(DOWN, buff=0.4)
            .to_edge(RIGHT + UP)
        )

        self.play(
            FadeOut(negative_projection),
            FadeOut(negative_y_value),
            FadeOut(negative_label),
            FadeOut(negative_dot),
            Write(summary),
        )
        self.wait(4)

        self.play(FadeOut(point_dot), FadeOut(point_label), FadeOut(y_projection), FadeOut(y_value), FadeOut(summary))
        self.wait(2)

        # =========================================================
        # 4. Reading multiple coordinates across quadrants
        # =========================================================
        points = [
            (2, 5),
            (-4, 3),
            (-3, -2),
        ]

        for x, y in points:
            p = Dot(grid.c2p(x, y), color=TEAL, radius=0.1)
            label = MathTex(f"({x},{y})", font_size=36, color=TEAL).next_to(p, UP + RIGHT)

            self.play(FadeIn(p), Write(label))
            self.wait(2)

            px = Line(grid.c2p(0, 0), grid.c2p(x, 0), color=RED)
            px_label = Text(f"{x}", font_size=36, color=RED).next_to(px, UP)

            py = DashedLine(grid.c2p(x, 0), grid.c2p(x, y), color=TEAL)
            py_label = Text(f"{y}", font_size=36, color=TEAL).next_to(py, LEFT)

            self.play(Create(px), Write(px_label))
            self.wait(2)
            self.play(Create(py), Write(py_label))
            self.wait(2)
            self.play(FadeOut(px, py, label, p, px_label, py_label))

        self.wait(2)

        # =========================================================
        # 5. Distance from the origin calculated using Pythagoras theorem
        # =========================================================
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not self.camera.frame])
        self.play(self.camera.frame.animate.move_to(ORIGIN))

        title = Text("Distance from the Origin", font_size=56, weight=BOLD)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        grid = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-10, 10, 1],
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": 2,
                "stroke_opacity": 0.5,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )

        x_axis = Line(grid.c2p(-14, 0), grid.c2p(14, 0), stroke_width=4, color=GRAY_D)
        y_axis = Line(grid.c2p(0, -8), grid.c2p(0, 8), stroke_width=4, color=GRAY_D)

        origin = grid.c2p(0, 0)
        origin_dot = Dot(origin, color=YELLOW_E, radius=0.08)

        self.play(FadeIn(grid, x_axis, y_axis, origin_dot))
        self.wait(1)

        point_a_coords = grid.c2p(4, 3)
        point_a = Dot(point_a_coords, color=RED)
        label_a = MathTex("A(4, 3)", color=RED).next_to(point_a, UP + RIGHT)

        self.play(FadeIn(point_a), Write(label_a))

        dotted_line = DashedLine(origin, point_a_coords)
        question_mark = Text("?", font_size=36).next_to(dotted_line.get_center(), UP, buff=0.1)

        self.play(Create(dotted_line), Write(question_mark))
        self.wait(2)

        red_line = Line(origin, grid.c2p(4, 0), color=RED, stroke_width=5)
        teal_line = Line(grid.c2p(4, 0), grid.c2p(4, 3), color=TEAL, stroke_width=5)

        self.play(Create(red_line))
        self.play(Create(teal_line))

        self.play(FadeOut(grid), FadeOut(x_axis), FadeOut(y_axis), FadeOut(origin_dot))

        label_4 = MathTex("4", color=RED).next_to(red_line, DOWN)
        label_3 = MathTex("3", color=TEAL).next_to(teal_line, RIGHT)
        right_angle = RightAngle(red_line, teal_line, length=0.3, quadrant=(-1, 1))

        self.play(Write(label_4), Write(label_3), Create(right_angle))
        self.wait(2)

        idea_1 = Text("distance = hypotenuse", font_size=48)
        idea_2 = Text("base = 4 units", font_size=48)
        idea_3 = Text("perpendicular = 3 units", font_size=48)

        ideas_group = VGroup(idea_1, idea_2, idea_3).arrange(DOWN, aligned_edge=LEFT)
        ideas_group.move_to(self.camera.frame.get_corner(UL) + DR, aligned_edge=UL)

        self.play(Write(ideas_group))
        self.wait(1)

        pythagoras_text = Text("Using Pythagoras theorem,", font_size=48)
        pythagoras_text.next_to(ideas_group, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Write(pythagoras_text))
        self.wait(1)

        step1 = MathTex("h^2 = p^2 + b^2", font_size=60)
        step1.next_to(pythagoras_text, DOWN, buff=0.5, aligned_edge=LEFT)

        step2 = MathTex("h = \\sqrt{p^2 + b^2}", font_size=60)
        step2.next_to(step1, DOWN, buff=0.3, aligned_edge=LEFT)

        step3 = MathTex("h = \\sqrt{3^2 + 4^2}", font_size=60)
        step3.next_to(step2, DOWN, buff=0.3, aligned_edge=LEFT)

        step4 = MathTex("h = \\sqrt{9 + 16}", font_size=60)
        step4.move_to(step3, aligned_edge=LEFT)

        step5 = MathTex("h = \\sqrt{25}", font_size=60)
        step5.next_to(step4, DOWN, buff=0.3, aligned_edge=LEFT)

        step6 = MathTex("h = 5", font_size=60)
        step6.next_to(step5, DOWN, buff=0.3, aligned_edge=LEFT)

        final_ans = Text("distance = 5 units", font_size=60, color=TEAL_E)
        final_ans.next_to(step6, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(step1))
        self.wait(1)
        self.play(Write(step2))
        self.wait(1)
        self.play(Write(step3))
        self.wait(2)
        self.play(Transform(step3, step4))
        self.wait(1)
        self.play(Write(step5))
        self.wait(1)
        self.play(Write(step6))
        self.wait(1)
        self.play(Write(final_ans))
        self.wait(1)

        final_hypotenuse_label = MathTex("5", font_size=48, color=TEAL_E).move_to(question_mark)
        self.play(Transform(question_mark, final_hypotenuse_label))
        self.wait(3)

        # =========================================================
        # 6. Distance between two points using a custom triangle construction
        # =========================================================
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not self.camera.frame])
        self.wait(1)
        self.play(self.camera.frame.animate.move_to(ORIGIN))

        title_12 = Text("Distance between any Two Points", font_size=56, weight=BOLD)
        self.play(Write(title_12))
        self.wait(1)
        self.play(FadeOut(title_12))

        grid = NumberPlane(
            x_range=[-5, 15, 1],
            y_range=[-5, 10, 1],
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": 2,
                "stroke_opacity": 0.5,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )
        grid.shift(RIGHT * 5)

        x_axis = Line(grid.c2p(-5, 0), grid.c2p(15, 0), stroke_width=4, color=GRAY_D)
        y_axis = Line(grid.c2p(0, -5), grid.c2p(0, 10), stroke_width=4, color=GRAY_D)

        x_labels = VGroup(*[Text(str(i), font_size=24).next_to(grid.c2p(i, 0), DOWN) for i in (2, 10)])
        y_labels = VGroup(*[Text(str(i), font_size=24).next_to(grid.c2p(0, i), LEFT) for i in (1, 7)])

        self.play(FadeIn(grid, x_axis, y_axis, x_labels, y_labels))
        self.wait(1)

        pt_a_coords = grid.c2p(2, 1)
        pt_b_coords = grid.c2p(10, 7)

        dot_a = Dot(pt_a_coords, color=TEAL, radius=0.1)
        label_a = MathTex("A(2, 1)", color=TEAL, font_size=48).next_to(dot_a, UL, buff=0.1)

        dot_b = Dot(pt_b_coords, color=RED, radius=0.1)
        label_b = MathTex("B(10, 7)", color=RED, font_size=48).next_to(dot_b, RIGHT + UP, buff=0.1)

        self.play(FadeIn(dot_a), Write(label_a), FadeIn(dot_b), Write(label_b))
        self.wait(1)

        dist_line = Line(pt_a_coords, pt_b_coords, color=YELLOW_E, stroke_width=5)
        dist_label = MathTex("d = ?", font_size=48).next_to(dist_line.get_center(), UP + LEFT, buff=0.1)

        self.play(Create(dist_line), Write(dist_label))
        self.wait(2)

        vert_drop = DashedLine(pt_b_coords, grid.c2p(10, 0))
        pt_c_coords = grid.c2p(10, 1)
        horiz_line = DashedLine(pt_a_coords, pt_c_coords)

        self.play(Create(vert_drop))
        self.play(Create(horiz_line))

        dot_c = Dot(pt_c_coords, color=TEAL_E)
        label_c = MathTex("C(10, 1)", color=TEAL_E, font_size=48).next_to(dot_c, DOWN + RIGHT, buff=0.1)

        rt_angle = RightAngle(horiz_line, Line(pt_c_coords, pt_b_coords), length=0.4, quadrant=(-1, 1))

        self.play(FadeIn(dot_c), Write(label_c), Create(rt_angle))
        self.wait(1)

        base_label = MathTex("10 - 2 = 8", font_size=48).next_to(horiz_line, DOWN, buff=0.2)
        perp_line_segment = Line(pt_c_coords, pt_b_coords)
        perp_label = MathTex("7 - 1 = 6", font_size=48).next_to(perp_line_segment, RIGHT, buff=0.2)

        self.play(Write(base_label))
        self.play(Write(perp_label))
        self.wait(2)

        self.play(
            FadeOut(grid),
            FadeOut(x_axis),
            FadeOut(y_axis),
            FadeOut(x_labels),
            FadeOut(y_labels),
            FadeOut(Line(grid.c2p(10, 1), grid.c2p(10, 0))),
        )
        self.wait(1)

        eq1 = MathTex("d = h = \\sqrt{p^2 + b^2}", font_size=56)
        eq1.move_to(self.camera.frame.get_corner(UL) + DR, aligned_edge=UL)

        eq2 = MathTex("h = \\sqrt{6^2 + 8^2}", font_size=56)
        eq2.next_to(eq1, DOWN, buff=0.4, aligned_edge=LEFT)

        eq3 = MathTex("h = \\sqrt{36 + 64}", font_size=56)
        eq3.next_to(eq2, DOWN, buff=0.4, aligned_edge=LEFT)

        eq4 = MathTex("h = \\sqrt{100}", font_size=56)
        eq4.move_to(eq3, aligned_edge=LEFT)

        eq5 = MathTex("h = 10", font_size=56)
        eq5.next_to(eq4, DOWN, buff=0.4, aligned_edge=LEFT)

        final_d = Text("so, distance (d) = 10", font_size=56)
        final_d.next_to(eq5, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(eq1))
        self.wait(1)
        self.play(Write(eq2))
        self.wait(1)
        self.play(Write(eq3))
        self.wait(1)
        self.play(Transform(eq3, eq4))
        self.wait(1)
        self.play(Write(eq5))
        self.wait(1)
        self.play(Write(final_d))
        self.wait(1)

        final_dist_label = MathTex("d = 10", font_size=48, color=YELLOW_E).move_to(dist_label)
        self.play(Transform(dist_label, final_dist_label))
        self.wait(4)

        # =========================================================
        # 7. Deriving the general distance formula for points (x1, y1) & (x2, y2)
        # =========================================================
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not self.camera.frame])
        self.wait(1)
        self.play(self.camera.frame.animate.move_to(ORIGIN))

        title_13 = Text("Deriving the Distance Formula", font_size=56, weight=BOLD)
        self.play(Write(title_13))
        self.wait(1)
        self.play(FadeOut(title_13))

        grid = NumberPlane(
            x_range=[-5, 15, 1],
            y_range=[-5, 10, 1],
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": 2,
                "stroke_opacity": 0.5,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=0,
        )
        grid.shift(RIGHT * 5)

        x_axis = Line(grid.c2p(-5, 0), grid.c2p(15, 0), stroke_width=4, color=GRAY_D)
        y_axis = Line(grid.c2p(0, -5), grid.c2p(0, 10), stroke_width=4, color=GRAY_D)

        x_labels = VGroup(
            *[
                MathTex(txt, font_size=30).next_to(grid.c2p(coord, 0), DOWN)
                for coord, txt in zip(
                    [2, 10],
                    ["x_1", "x_2"],
                )
            ]
        )
        y_labels = VGroup(
            *[
                MathTex(txt, font_size=30).next_to(grid.c2p(0, coord), LEFT)
                for coord, txt in zip(
                    [1, 7],
                    ["y_1", "y_2"],
                )
            ]
        )

        self.play(FadeIn(grid, x_axis, y_axis, x_labels, y_labels))
        self.wait(1)

        pt_a_coords = grid.c2p(2, 1)
        pt_b_coords = grid.c2p(10, 7)

        dot_a = Dot(pt_a_coords, color=TEAL, radius=0.1)
        label_a = MathTex("A(x_1, y_1)", color=TEAL, font_size=42, stroke_width=1.5).next_to(dot_a, UL, buff=0.1)

        dot_b = Dot(pt_b_coords, color=RED, radius=0.1)
        label_b = MathTex("B(x_2, y_2)", color=RED, font_size=42, stroke_width=1.5).next_to(dot_b, RIGHT + UP, buff=0.1)

        self.play(FadeIn(dot_a), Write(label_a), FadeIn(dot_b), Write(label_b))
        self.wait(1)

        dist_line = Line(pt_a_coords, pt_b_coords, color=YELLOW_E, stroke_width=5)
        dist_label = MathTex("d = ?", font_size=42, stroke_width=1.5).next_to(dist_line.get_center(), UP + LEFT, buff=0.1)

        self.play(Create(dist_line), Write(dist_label))
        self.wait(2)

        vert_drop = DashedLine(pt_b_coords, grid.c2p(10, 0))
        pt_c_coords = grid.c2p(10, 1)
        horiz_line = DashedLine(pt_a_coords, pt_c_coords)

        self.play(Create(vert_drop))
        self.play(Create(horiz_line))

        dot_c = Dot(pt_c_coords, color=TEAL_E)
        label_c = MathTex("C(x_2, y_1)", color=TEAL, font_size=42, stroke_width=1.5).next_to(dot_c, DOWN + RIGHT, buff=0.1)

        rt_angle = RightAngle(horiz_line, Line(pt_c_coords, pt_b_coords), length=0.4, quadrant=(-1, 1))

        self.play(FadeIn(dot_c), Write(label_c), Create(rt_angle))
        self.wait(1)

        base_label = MathTex("b = x_2 - x_1", font_size=42).next_to(horiz_line, DOWN, buff=0.2)
        perp_line_segment = Line(pt_c_coords, pt_b_coords)
        perp_label = MathTex("p = y_2 - y_1", font_size=42).next_to(perp_line_segment, RIGHT, buff=0.2)

        self.play(Write(base_label))
        self.play(Write(perp_label))
        self.wait(2)

        self.play(
            FadeOut(grid),
            FadeOut(x_axis),
            FadeOut(y_axis),
            FadeOut(x_labels),
            FadeOut(y_labels),
            FadeOut(Line(grid.c2p(10, 1), grid.c2p(10, 0))),
        )
        self.wait(1)

        coord_intro = MathTex("A = (x_1, y_1), \\quad B = (x_2, y_2)", font_size=45)
        coord_intro.move_to(self.camera.frame.get_corner(UL) + DOWN * 2 + RIGHT * 2, aligned_edge=UL)

        triangle_text = Text("In rt. angled triangle ABC,", font_size=40)
        triangle_text.next_to(coord_intro, DOWN, buff=0.4, aligned_edge=LEFT)

        ac_text = MathTex("AC = b = x_2 - x_1", font_size=50)
        ac_text.next_to(triangle_text, DOWN, buff=0.3, aligned_edge=LEFT)

        bc_text = MathTex("BC = p = y_2 - y_1", font_size=50)
        bc_text.next_to(ac_text, DOWN, buff=0.3, aligned_edge=LEFT)

        ab_hyp = MathTex("AB = \\text{hypotenuse} = ?", font_size=50)
        ab_hyp.next_to(bc_text, DOWN, buff=0.4, aligned_edge=LEFT)

        ab_dist = MathTex("\\text{distance } (AB) = ?", font_size=50, stroke_width=1.5)
        ab_dist.next_to(ab_hyp, DOWN, buff=0.3, aligned_edge=LEFT)

        pyth_title = Text("Using Pythagoras theorem:", font_size=40)
        pyth_title.next_to(ab_dist, DOWN, buff=0.5, aligned_edge=LEFT)

        step_h1 = MathTex("h = \\sqrt{b^2 + p^2}", font_size=52)
        step_h1.next_to(pyth_title, DOWN, buff=0.3, aligned_edge=LEFT)

        step_h2 = MathTex("h = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}", font_size=52, stroke_width=1.5)
        step_h2.next_to(step_h1, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(coord_intro))
        self.wait(1)
        self.play(Write(triangle_text))
        self.wait(1)
        self.play(Write(ac_text))
        self.wait(1)
        self.play(Write(bc_text))
        self.wait(1)
        self.play(Write(ab_hyp))
        self.wait(1)
        self.play(Write(ab_dist))
        self.wait(1)
        self.play(Write(pyth_title))
        self.wait(1)
        self.play(Write(step_h1))
        self.wait(1)
        self.play(Write(step_h2))
        self.wait(2)

        self.play(
            FadeOut(
                VGroup(
                    coord_intro,
                    triangle_text,
                    ac_text,
                    bc_text,
                    ab_hyp,
                    ab_dist,
                    pyth_title,
                    step_h1,
                    step_h2,
                )
            ),
            run_time=1.5,
        )

        final_text = MathTex(
            r"\text{Distance between two points: }",
            r"(x_1, y_1)",
            r"\text{ and }",
            r"(x_2, y_2)",
            r"\text{ is:}",
            font_size=60,
        ).move_to(LEFT * 5 + UP * 4)

        final_formula = MathTex(
            "distance = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}",
            font_size=72,
        )

        box = SurroundingRectangle(
            final_formula,
            color=TEAL_E,
            buff=0.35,
            corner_radius=0.15,
        )

        final_group = VGroup(box, final_formula)
        final_group.move_to(LEFT * 5 + UP * 2)

        self.play(Write(final_text))
        self.play(
            Write(final_formula),
            Create(box),
            run_time=2,
        )

        self.wait(3)
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(2)
