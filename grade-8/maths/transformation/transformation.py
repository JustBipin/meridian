from manim import *
from manim_themes.manim_theme import apply_theme

# ==============================================================================
# Design and Content Tokens
# ==============================================================================
FONT_SIZE_TITLE = 48
FONT_SIZE_SUBTITLE = 32

POINT_START_COORDS = (2, 1)
SHIFT_COORDS = (3, 2)
POINT_END_COORDS = (
    POINT_START_COORDS[0] + SHIFT_COORDS[0],
    POINT_START_COORDS[1] + SHIFT_COORDS[1],
)


# ==============================================================================
# SCENE 1: TRANSLATION
# ==============================================================================
class TranslationScene(MovingCameraScene):
    """
    Illustrates the concept of mathematical translation (shifting)
    using a polygon and a specific coordinate point.
    """

    def setup(self):
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        # Save initial camera state as per guidelines
        self.camera.frame.save_state()

        self.next_section("Introduction")

        # Title and Subtitle
        title = Text("Transformation: Translation", font_size=FONT_SIZE_TITLE, weight=BOLD)
        subtitle = Text("Translation just means to shift", font_size=FONT_SIZE_SUBTITLE)
        subtitle.to_edge(DOWN, buff=0.8)

        self.play(Write(title), Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)

        self.next_section("Coordinate Grid and Shape Translation")

        # Coordinate Grid Setup
        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": DARK_GRAY,
                "stroke_width": 1.5,
                "stroke_opacity": 0.7,
            },
            axis_config={
                "stroke_color": GRAY,
                "stroke_width": 2,
                "include_numbers": True,
                "font_size": 20,
            },
            faded_line_ratio=0,
        )
        grid.scale(0.85).shift(DOWN * 0.2)

        subtitle_bottom = Text("Translation just means to shift", font_size=28)
        subtitle_bottom.to_edge(DOWN, buff=0.4)

        # Fading in the grid instead of drawing it one by one
        self.play(FadeIn(grid), FadeIn(subtitle_bottom), run_time=1.5)
        self.wait(1)

        # Translating a Shape (Triangle across 3 Positions)
        triangle_vertices = [
            grid.c2p(0, 0.8),
            grid.c2p(-0.7, -0.5),
            grid.c2p(0.7, -0.5),
        ]
        triangle = Polygon(*triangle_vertices, color=BLUE, fill_color=BLUE, fill_opacity=0.4, stroke_width=3)

        pos1, pos2, pos3 = (-3, -1), (0, 1), (3, -1)

        triangle.move_to(grid.c2p(*pos1))
        lbl_pos1 = Text("Position 1", font_size=20, color=BLUE).next_to(triangle, UP, buff=0.15)

        self.play(FadeIn(triangle), Write(lbl_pos1))
        self.wait(1)

        # Shift to Position 2 & 3
        lbl_pos2 = Text("Position 2", font_size=20, color=RED).next_to(grid.c2p(*pos2), UP, buff=0.8)
        self.play(
            triangle.animate.move_to(grid.c2p(*pos2)).set_color(RED),
            Transform(lbl_pos1, lbl_pos2),
            run_time=1.5,
        )
        self.wait(1)

        lbl_pos3 = Text("Position 3", font_size=20, color=PURPLE_E).next_to(grid.c2p(*pos3), UP, buff=0.8)
        self.play(
            triangle.animate.move_to(grid.c2p(*pos3)).set_color(PURPLE_E),
            Transform(lbl_pos1, lbl_pos3),
            run_time=1.5,
        )
        self.wait(1)

        self.play(
            FadeOut(triangle),
            FadeOut(lbl_pos1),
            FadeOut(subtitle_bottom),
        )
        self.wait(0.5)

        self.next_section("Translating a Specific Point")

        # Translating Point (2, 1) by (3, 2)
        point_subtitle = MathTex(
            r"\text{Translating point } (2, 1) \text{ by } (3, 2)",
            font_size=32,
        ).to_edge(UP, buff=0.4)

        self.play(Write(point_subtitle))

        start_pt = grid.c2p(*POINT_START_COORDS)
        dot_a = Dot(start_pt, color=BLUE, radius=0.09)
        label_a = MathTex("A(2, 1)", color=BLUE, font_size=32).next_to(start_pt, UL, buff=0.15)

        self.play(FadeIn(dot_a), Write(label_a))
        self.wait(0.8)

        # Horizontal & Vertical Dotted Paths with synchronized sliding
        mid_coords = (POINT_END_COORDS[0], POINT_START_COORDS[1])
        mid_pt = grid.c2p(*mid_coords)
        end_pt = grid.c2p(*POINT_END_COORDS)

        horiz_line = DashedLine(start_pt, mid_pt, color=PURPLE_E, stroke_width=4, dash_length=0.12)
        horiz_label = MathTex("+3 \\text{ (Horizontal)}", color=PURPLE_E, font_size=26).next_to(horiz_line, DOWN, buff=0.15)

        dot_a_ghost = Dot(start_pt, color=BLUE_B)
        # Slide the point horizontally along with the line drawing
        self.play(Create(horiz_line), dot_a.animate.move_to(mid_pt), Write(horiz_label), FadeIn(dot_a_ghost), run_time=1.5)

        vert_line = DashedLine(mid_pt, end_pt, color=RED, stroke_width=4, dash_length=0.12)
        vert_label = MathTex("+2 \\text{ (Vertical)}", color=RED, font_size=26).next_to(vert_line, RIGHT, buff=0.15)

        # Slide the point vertically along with the line drawing
        self.play(Create(vert_line), dot_a.animate.move_to(end_pt), Write(vert_label), run_time=1.5)

        dot_a_prime = Dot(end_pt, color=PURPLE_E, radius=0.09)
        label_a_prime = MathTex("A'(5, 3)", color=PURPLE_E, font_size=32).next_to(dot_a_prime, UR, buff=0.15)
        direct_line = DashedLine(start_pt, end_pt, color=TEAL, stroke_width=4, dash_length=0.12)

        self.play(
            ReplacementTransform(dot_a, dot_a_prime),
            Write(label_a_prime),
            Create(direct_line),
        )
        self.wait(1)

        calc_summary = MathTex(
            r"(2 + 3, \, 1 + 2) = (5, 3)",
            font_size=32,
            color=PURPLE_E,
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(calc_summary))
        self.wait(1.5)

        self.next_section("General Translation Rule")

        # General Translation Conclusion Card
        self.play(
            FadeOut(label_a),
            FadeOut(horiz_line),
            FadeOut(horiz_label),
            FadeOut(vert_line),
            FadeOut(vert_label),
            FadeOut(dot_a_prime),
            FadeOut(label_a_prime),
            FadeOut(direct_line),
            FadeOut(point_subtitle),
            FadeOut(calc_summary),
            FadeOut(dot_a_ghost),
        )
        self.wait(0.3)

        self.play(grid.animate.shift(RIGHT * 2.5))

        conclusion_heading = Text("Translation Rule:", font_size=28, weight=BOLD, color=BLUE)
        conclusion_line1 = MathTex(r"\text{Translating } (x, y) \text{ by } (a, b)", font_size=26)
        conclusion_box = MathTex(r"(x, y) \rightarrow (x + a, \, y + b)", font_size=32, color=PURPLE_E)

        conclusion_group = VGroup(conclusion_heading, conclusion_line1, conclusion_box).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25
        )
        bg_card = RoundedRectangle(
            corner_radius=0.15,
            height=conclusion_group.height + 0.6,
            width=conclusion_group.width + 0.6,
        )
        conclusion_group.move_to(bg_card)
        full_conclusion = VGroup(bg_card, conclusion_group).to_edge(LEFT, buff=0.4)

        self.play(FadeIn(full_conclusion))

        # General point on grid
        gen_start_coords, gen_shift_coords = (-2, -1), (3, 2)
        gen_end_coords = (gen_start_coords[0] + gen_shift_coords[0], gen_start_coords[1] + gen_shift_coords[1])
        pt_gen, pt_gen_end = grid.c2p(*gen_start_coords), grid.c2p(*gen_end_coords)

        dot_gen = Dot(pt_gen, color=BLUE, radius=0.09)
        lbl_gen = MathTex("(x, y)", color=BLUE, font_size=28).next_to(pt_gen, DL, buff=0.15)
        gen_mid = grid.c2p(gen_end_coords[0], gen_start_coords[1])

        h_dash = DashedLine(pt_gen, gen_mid, color=PURPLE_E, stroke_width=3, dash_length=0.1)
        h_lbl = MathTex("+a", color=PURPLE_E_E, font_size=24).next_to(h_dash, DOWN, buff=0.1)
        v_dash = DashedLine(gen_mid, pt_gen_end, color=RED, stroke_width=3, dash_length=0.1)
        v_lbl = MathTex("+b", color=RED, font_size=24).next_to(v_dash, RIGHT, buff=0.1)

        dot_gen_end = Dot(pt_gen_end, color=PURPLE_E_E, radius=0.09)
        lbl_gen_end = MathTex("(x + a, y + b)", color=PURPLE_E, font_size=28).next_to(dot_gen_end, UR, buff=0.15)
        d_dash = DashedLine(pt_gen, pt_gen_end, color=TEAL, stroke_width=3.5, dash_length=0.12)

        self.play(FadeIn(dot_gen), Write(lbl_gen))

        # Slide horizontally for general point
        dot_gen_ghost = Dot(pt_gen, color=BLUE_B)
        self.play(Create(h_dash), dot_gen.animate.move_to(gen_mid), Write(h_lbl), FadeIn(dot_gen_ghost), run_time=1.5)

        # Slide vertically for general point
        self.play(Create(v_dash), dot_gen.animate.move_to(pt_gen_end), Write(v_lbl), run_time=1.5)

        # Finalize general point visualization
        self.play(ReplacementTransform(dot_gen, dot_gen_end), Write(lbl_gen_end), Create(d_dash))
        self.wait(2)

        self.next_section("Final Conclusion")

        # Fade out the grid and all general point elements
        self.play(
            FadeOut(grid),
            FadeOut(lbl_gen),
            FadeOut(h_dash),
            FadeOut(h_lbl),
            FadeOut(v_dash),
            FadeOut(v_lbl),
            FadeOut(dot_gen_end),
            FadeOut(lbl_gen_end),
            FadeOut(d_dash),
            FadeOut(dot_gen_ghost),
        )
        self.wait(0.5)

        # Move the conclusion card to the center
        self.play(full_conclusion.animate.move_to(ORIGIN))
        self.wait(2)


def get_arm_label(arm, text, color):
    """
    Dynamically positions a label next to a rotated arm based on its new orientation.
    Detects if the arm is horizontal or vertical in world space.
    """
    center = arm.get_center()
    start = arm.get_start()
    end = arm.get_end()

    # Calculate vector differences to determine orientation
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    label = MathTex(text, color=color)

    # If the arm is more horizontal than vertical
    if abs(dx) > abs(dy):
        # Place UP if it's above the x-axis, DOWN if below or on it
        direction = UP if center[1] > 0.1 else DOWN
    # If the arm is more vertical than horizontal
    else:
        # Place RIGHT if it's right of the y-axis, LEFT if left or on it
        direction = RIGHT if center[0] > 0.1 else LEFT

    label.next_to(arm, direction, buff=0.15)
    return label


class RotationScene(MovingCameraScene):
    """
    Illustrates mathematical rotation using a point (2,3) and general rules,
    with coordinate arms that rotate alongside the point to reveal component swapping.
    """

    def setup(self):
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        self.camera.frame.save_state()

        self.next_section("Introduction")
        title = Text("Transformation: Rotation", font_size=FONT_SIZE_TITLE, weight=BOLD)
        subtitle = Text("Rotation means turning around the Origin", font_size=28)
        subtitle.to_edge(DOWN, buff=0.8)

        self.play(Write(title), Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        self.next_section("Grid Setup")
        grid = NumberPlane(x_range=[-5, 5, 1], y_range=[-4, 4, 1]).scale(0.85)
        self.play(FadeIn(grid))

        # Tip Animation
        tip = Text("Tip: Imagine 'arms' along the axes to visualize rotation.", font_size=24, color=DARKER_GRAY).to_edge(
            DOWN, buff=0.5
        )
        tip_bg = SurroundingRectangle(tip, fill_opacity=0.5)

        self.next_section("Rotating Point (2,3)")
        origin = grid.c2p(0, 0)
        p_pt = grid.c2p(2, 3)
        dot_p = Dot(p_pt, color=BLUE)
        hypot = DashedLine(origin, p_pt, color=TEAL)

        self.play(FadeIn(dot_p), Create(hypot))
        self.play(FadeIn(tip_bg), Write(tip))

        # Draw arms X then Y
        arm_h = DashedLine(origin, grid.c2p(2, 0), color=PURPLE_E)
        arm_v = DashedLine(grid.c2p(2, 0), p_pt, color=RED)
        lbl_h = MathTex("2", color=PURPLE_E).next_to(arm_h, DOWN, buff=0.1)
        lbl_v = MathTex("3", color=RED).next_to(arm_v, RIGHT, buff=0.1)

        self.play(Create(arm_h), Write(lbl_h))
        self.play(Create(arm_v), Write(lbl_v))
        self.wait(1)
        self.play(FadeOut(tip, tip_bg))

        # 1. Fade out everything except the point and the right-angled arms
        self.play(FadeOut(lbl_h), FadeOut(lbl_v), FadeOut(hypot))

        # 2. Rotate the point and the arms together by 90 degrees
        self.play(
            Rotate(dot_p, angle=PI / 2, about_point=origin),
            Rotate(arm_h, angle=PI / 2, about_point=origin),
            Rotate(arm_v, angle=PI / 2, about_point=origin),
            run_time=1.5,
        )

        # 3. Label the rotated arms (Horizontal first to represent new X, then Vertical for new Y)
        # After +90 deg, arm_v (Red) is horizontal, arm_h (Purple) is vertical.
        lbl_new_x = get_arm_label(arm_v, "-3", RED)
        lbl_new_y = get_arm_label(arm_h, "2", PURPLE_E)

        self.play(Write(lbl_new_x))
        self.play(Write(lbl_new_y))
        self.wait(2)

        self.next_section("General Rules")

        # Cleanup the specific point setup
        self.play(FadeOut(arm_h, arm_v, lbl_new_x, lbl_new_y, dot_p))

        # Shift camera to the left to make space for the rules text
        self.play(self.camera.frame.animate.shift(LEFT * 3))

        # Create general point
        gen_x, gen_y = 3, 2
        gen_origin = grid.c2p(0, 0)
        gen_pt = grid.c2p(gen_x, gen_y)

        gen_dot = Dot(gen_pt, color=YELLOW)
        gen_hypot = DashedLine(gen_origin, gen_pt, color=TEAL)

        g_arm_h = DashedLine(gen_origin, grid.c2p(gen_x, 0), color=PURPLE_E)
        g_arm_v = DashedLine(grid.c2p(gen_x, 0), gen_pt, color=RED)

        g_lbl_h = MathTex("x", color=PURPLE_E).next_to(g_arm_h, DOWN, buff=0.1)
        g_lbl_v = MathTex("y", color=RED).next_to(g_arm_v, RIGHT, buff=0.1)

        self.play(Create(gen_hypot), FadeIn(gen_dot))
        self.play(Create(g_arm_h), Write(g_lbl_h))
        self.play(Create(g_arm_v), Write(g_lbl_v))
        self.wait(1)

        rules_group = VGroup()

        def demonstrate_general_rotation(angle, rule_str, red_text, purple_text):
            # Save states to cleanly revert after the demonstration
            gen_dot.save_state()
            g_arm_h.save_state()
            g_arm_v.save_state()

            # 1. Hide hypotenuse and base labels during rotation
            self.play(FadeOut(gen_hypot), FadeOut(g_lbl_h), FadeOut(g_lbl_v))

            # 2. Rotate the dot and the original arms
            self.play(
                Rotate(gen_dot, angle=angle, about_point=gen_origin),
                Rotate(g_arm_h, angle=angle, about_point=gen_origin),
                Rotate(g_arm_v, angle=angle, about_point=gen_origin),
                run_time=1.5,
            )

            # 3. Determine which arm is now horizontal (x-axis) and vertical (y-axis)
            is_90_or_270 = abs(abs(angle) - PI / 2) < 0.1

            if is_90_or_270:
                horiz_arm, vert_arm = g_arm_v, g_arm_h
                horiz_txt, vert_txt = red_text, purple_text
                horiz_color, vert_color = RED, PURPLE_E
            else:  # 180 degrees
                horiz_arm, vert_arm = g_arm_h, g_arm_v
                horiz_txt, vert_txt = purple_text, red_text
                horiz_color, vert_color = PURPLE_E, RED

            # 4. Label the new X component (horizontal), then Y component (vertical)
            lbl_horiz = get_arm_label(horiz_arm, horiz_txt, horiz_color)
            self.play(Write(lbl_horiz))

            lbl_vert = get_arm_label(vert_arm, vert_txt, vert_color)
            self.play(Write(lbl_vert))

            # 5. Write Conclusion Rule on the left side
            rule_tex = MathTex(rule_str, font_size=36)
            if len(rules_group) == 0:
                rule_tex.move_to(self.camera.frame.get_left() + RIGHT * 2.5 + UP * 2)
            else:
                rule_tex.next_to(rules_group, DOWN, buff=0.7).align_to(rules_group[0], LEFT)

            self.play(Write(rule_tex))
            rules_group.add(rule_tex)
            self.wait(2)

            # 6. Fade out rotated objects and beautifully reset for the next rule
            self.play(FadeOut(lbl_horiz, lbl_vert, gen_dot, g_arm_h, g_arm_v))

            gen_dot.restore()
            g_arm_h.restore()
            g_arm_v.restore()

            self.play(FadeIn(gen_dot, g_arm_h, g_arm_v, gen_hypot, g_lbl_h, g_lbl_v))
            self.wait(0.5)

        # 1. Rotate 90 degrees
        demonstrate_general_rotation(PI / 2, r"90^\circ: (x, y) \rightarrow (-y, x)", red_text="-y", purple_text="x")

        # 2. Rotate 180 degrees
        demonstrate_general_rotation(PI, r"180^\circ: (x, y) \rightarrow (-x, -y)", red_text="-y", purple_text="-x")

        # 3. Rotate 270 / -90 degrees
        demonstrate_general_rotation(-PI / 2, r"-90^\circ: (x, y) \rightarrow (y, -x)", red_text="y", purple_text="-x")

        self.wait(2)

        # Add Surrounding Rectangle
        conclusion_box = SurroundingRectangle(rules_group, color=BLUE, buff=0.3)
        self.play(Create(conclusion_box))
        self.wait(2)

        self.next_section("Final Conclusion")

        # Fade out everything except the conclusion
        self.play(
            FadeOut(grid),
            FadeOut(gen_dot),
            FadeOut(gen_hypot),
            FadeOut(g_arm_h),
            FadeOut(g_arm_v),
            FadeOut(g_lbl_h),
            FadeOut(g_lbl_v),
        )

        # Move the conclusion to the center
        final_conclusion = VGroup(rules_group, conclusion_box)
        self.play(final_conclusion.animate.move_to(ORIGIN))

        self.wait(3)


# ==============================================================================
# Design and Content Tokens
# ==============================================================================
FONT_SIZE_TITLE = 48
FONT_SIZE_SUBTITLE = 32

# Point used for the X-axis reflection walkthrough
POINT_X_START_COORDS = (3, 2)
POINT_X_END_COORDS = (POINT_X_START_COORDS[0], -POINT_X_START_COORDS[1])

# Point used for the Y-axis reflection walkthrough
POINT_Y_START_COORDS = (2, 3)
POINT_Y_END_COORDS = (-POINT_Y_START_COORDS[0], POINT_Y_START_COORDS[1])


# ==============================================================================
# SCENE: REFLECTION
# ==============================================================================
class ReflectionScene(MovingCameraScene):
    """
    Illustrates the concept of mathematical reflection (flipping)
    over the x-axis and the y-axis, using a polygon and specific
    coordinate points, following the same visual language as the
    Translation scene (dashed guide lines, sliding dots, ghost
    markers, and a boxed rule card for the generalization).
    """

    def setup(self):
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        self.camera.frame.save_state()

        self.next_section("Introduction")

        title = Text("Transformation: Reflection", font_size=FONT_SIZE_TITLE, weight=BOLD)
        subtitle = Text("Reflection means flipping over a line, like a mirror", font_size=FONT_SIZE_SUBTITLE)
        subtitle.to_edge(DOWN, buff=0.8)

        self.play(Write(title), Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)

        self.next_section("Coordinate Grid and Shape Reflection")

        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": DARK_GRAY,
                "stroke_width": 1.5,
                "stroke_opacity": 0.7,
            },
            axis_config={
                "stroke_color": GRAY,
                "stroke_width": 2,
                "include_numbers": True,
                "font_size": 20,
            },
            faded_line_ratio=0,
        )
        grid.scale(0.85).shift(DOWN * 0.2)

        subtitle_bottom = Text("A reflection mirrors every point across a line", font_size=28)
        subtitle_bottom.to_edge(DOWN, buff=0.4)

        self.play(FadeIn(grid), FadeIn(subtitle_bottom), run_time=1.5)
        self.wait(1)

        # Triangle reflected over the x-axis, then over the y-axis
        # Right-angled triangle, legs in a 3:4 ratio (scaled to 0.9 x 1.2 to fit the grid)
        triangle_vertices = [
            grid.c2p(-0.45, -0.6),
            grid.c2p(0.45, -0.6),
            grid.c2p(-0.45, 0.6),
        ]
        triangle = Polygon(*triangle_vertices, color=BLUE, fill_color=BLUE, fill_opacity=0.4, stroke_width=3)
        triangle.move_to(grid.c2p(-3, 1.5))
        lbl_orig = Text("Original", font_size=20, color=BLUE).next_to(triangle, UP, buff=0.15)

        self.play(FadeIn(triangle), Write(lbl_orig))
        self.wait(1)

        # Highlight the x-axis as the mirror line
        x_axis_highlight = Line(grid.c2p(-6, 0), grid.c2p(6, 0), color=RED, stroke_width=5)
        mirror_lbl_x = (
            Text("Mirror line (x-axis)", font_size=20, color=RED).next_to(x_axis_highlight, DOWN, buff=0.2).shift(LEFT * 2.5)
        )
        self.play(Create(x_axis_highlight), Write(mirror_lbl_x))
        self.wait(0.5)

        # Build the reflected triangle by flipping the y-sign of each vertex
        base_center = (-3, 1.5)
        orig_local_vertices = [(-0.45, -0.6), (0.45, -0.6), (-0.45, 0.6)]
        reflected_x_vertices = [grid.c2p(base_center[0] + vx, -(base_center[1] + vy)) for vx, vy in orig_local_vertices]
        triangle_x_reflected = Polygon(
            *reflected_x_vertices, color=PURPLE_E, fill_color=PURPLE_E, fill_opacity=0.4, stroke_width=3
        )
        lbl_reflected_x = Text("Reflected over x-axis", font_size=20, color=PURPLE_E).next_to(
            triangle_x_reflected, DOWN, buff=0.15
        )

        triangle_copy_for_x = triangle.copy()
        self.play(
            Transform(triangle_copy_for_x, triangle_x_reflected),
            Write(lbl_reflected_x),
            run_time=1.5,
        )
        self.wait(1)

        self.play(
            FadeOut(triangle),
            FadeOut(lbl_orig),
            FadeOut(triangle_copy_for_x),
            FadeOut(lbl_reflected_x),
            FadeOut(x_axis_highlight),
            FadeOut(mirror_lbl_x),
        )
        self.wait(0.3)

        # Same shape, now reflected over the y-axis
        triangle2 = Polygon(
            *[grid.c2p(base_center[0] + vx, base_center[1] + vy) for vx, vy in orig_local_vertices],
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_width=3,
        )
        lbl_orig2 = Text("Original", font_size=20, color=BLUE).next_to(triangle2, UP, buff=0.15)

        y_axis_highlight = Line(grid.c2p(0, -4), grid.c2p(0, 4), color=RED, stroke_width=5)
        mirror_lbl_y = (
            Text("Mirror line (y-axis)", font_size=20, color=RED).next_to(y_axis_highlight, RIGHT, buff=0.2).shift(UP * 2.5)
        )

        self.play(FadeIn(triangle2), Write(lbl_orig2), Create(y_axis_highlight), Write(mirror_lbl_y))
        self.wait(1)

        reflected_y_vertices = [grid.c2p(-(base_center[0] + vx), base_center[1] + vy) for vx, vy in orig_local_vertices]
        triangle_y_reflected = Polygon(
            *reflected_y_vertices, color=PURPLE_E, fill_color=PURPLE_E, fill_opacity=0.4, stroke_width=3
        )
        lbl_reflected_y = Text("Reflected over y-axis", font_size=20, color=PURPLE_E).next_to(
            triangle_y_reflected, UP, buff=0.15
        )

        triangle_copy_for_y = triangle2.copy()
        self.play(
            Transform(triangle_copy_for_y, triangle_y_reflected),
            Write(lbl_reflected_y),
            run_time=1.5,
        )
        self.wait(1)

        self.play(
            FadeOut(triangle2),
            FadeOut(lbl_orig2),
            FadeOut(triangle_copy_for_y),
            FadeOut(lbl_reflected_y),
            FadeOut(y_axis_highlight),
            FadeOut(mirror_lbl_y),
            FadeOut(subtitle_bottom),
        )
        self.wait(0.5)

        # ------------------------------------------------------------------
        # Helper for the "specific point" and "general point" walkthroughs.
        # Mirrors the translation scene's pattern: dashed line to the axis,
        # a sliding dot, a ghost marker, then the mirrored dot + label.
        # ------------------------------------------------------------------
        def reflect_point_demo(
            start_coords,
            end_coords,
            axis,
            start_label_tex,
            end_label_tex,
            start_color=BLUE,
            end_color=PURPLE_E,
            guide_color=RED,
        ):
            start_pt = grid.c2p(*start_coords)
            end_pt = grid.c2p(*end_coords)

            dot_start = Dot(start_pt, color=start_color, radius=0.09)
            label_start = MathTex(start_label_tex, color=start_color, font_size=32).next_to(
                start_pt, UL if axis == "x" else DR, buff=0.15
            )
            self.play(FadeIn(dot_start), Write(label_start))
            self.wait(0.8)

            if axis == "x":
                axis_pt = grid.c2p(start_coords[0], 0)
            else:
                axis_pt = grid.c2p(0, start_coords[1])

            guide_line_1 = DashedLine(start_pt, axis_pt, color=guide_color, stroke_width=4, dash_length=0.12)
            guide_label_1 = MathTex("d", color=guide_color, font_size=26).next_to(
                guide_line_1, RIGHT if axis == "x" else UP, buff=0.15
            )

            dot_ghost = Dot(start_pt, color=BLUE_B)
            self.play(
                Create(guide_line_1),
                dot_start.animate.move_to(axis_pt),
                Write(guide_label_1),
                FadeIn(dot_ghost),
                run_time=1.5,
            )

            guide_line_2 = DashedLine(axis_pt, end_pt, color=end_color, stroke_width=4, dash_length=0.12)
            guide_label_2 = MathTex("d", color=end_color, font_size=26).next_to(
                guide_line_2, RIGHT if axis == "x" else UP, buff=0.15
            )
            self.play(
                Create(guide_line_2),
                dot_start.animate.move_to(end_pt),
                Write(guide_label_2),
                run_time=1.5,
            )

            dot_end = Dot(end_pt, color=end_color, radius=0.09)
            label_end = MathTex(end_label_tex, color=end_color, font_size=32).next_to(
                end_pt, DL if axis == "x" else UL, buff=0.15
            )
            self.play(
                ReplacementTransform(dot_start, dot_end),
                Write(label_end),
            )
            self.wait(1)

            return VGroup(
                label_start,
                guide_line_1,
                guide_label_1,
                dot_ghost,
                guide_line_2,
                guide_label_2,
                dot_end,
                label_end,
            )

        self.next_section("Reflecting a Point over the X-axis")

        point_subtitle_x = MathTex(
            r"\text{Reflecting point } (3, 2) \text{ over the x-axis}",
            font_size=32,
        ).to_edge(UP, buff=0.4)
        self.play(Write(point_subtitle_x))

        x_demo_group = reflect_point_demo(
            POINT_X_START_COORDS,
            POINT_X_END_COORDS,
            "x",
            "A(3, 2)",
            "A'(3, -2)",
        )

        calc_summary_x = MathTex(
            r"(3, 2) \rightarrow (3, -2) \quad \text{the y-value flips sign}",
            font_size=32,
            color=PURPLE_E,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(calc_summary_x))
        self.wait(1.5)

        self.next_section("General Rule for X-axis Reflection")

        self.play(FadeOut(x_demo_group), FadeOut(point_subtitle_x), FadeOut(calc_summary_x))
        self.wait(0.3)

        self.play(grid.animate.shift(RIGHT * 2.5))

        rule_x_heading = Text("Reflection over the x-axis:", font_size=26, weight=BOLD, color=BLUE)
        rule_x_line1 = MathTex(r"\text{x stays the same, y flips sign}", font_size=24)
        rule_x_box = MathTex(r"(x, y) \rightarrow (x, \, -y)", font_size=30, color=PURPLE_E)

        rule_x_group = VGroup(rule_x_heading, rule_x_line1, rule_x_box).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        bg_card_x = RoundedRectangle(
            corner_radius=0.15,
            height=rule_x_group.height + 0.6,
            width=rule_x_group.width + 0.6,
        )
        rule_x_group.move_to(bg_card_x)
        rule_card_x = VGroup(bg_card_x, rule_x_group).to_edge(LEFT, buff=0.4)

        self.play(FadeIn(rule_card_x))

        gen_x_group = reflect_point_demo(
            (-2, 1.5),
            (-2, -1.5),
            "x",
            "(x, y)",
            "(x, -y)",
        )
        self.wait(1)

        self.play(FadeOut(gen_x_group))
        self.play(grid.animate.shift(LEFT * 2.5), FadeOut(rule_card_x))
        self.wait(0.5)

        self.next_section("Reflecting a Point over the Y-axis")

        point_subtitle_y = MathTex(
            r"\text{Reflecting point } (2, 3) \text{ over the y-axis}",
            font_size=32,
        ).to_edge(UP, buff=0.4)
        self.play(Write(point_subtitle_y))

        y_demo_group = reflect_point_demo(
            POINT_Y_START_COORDS,
            POINT_Y_END_COORDS,
            "y",
            "B(2, 3)",
            "B'(-2, 3)",
        )

        calc_summary_y = MathTex(
            r"(2, 3) \rightarrow (-2, 3) \quad \text{the x-value flips sign}",
            font_size=32,
            color=PURPLE_E,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(calc_summary_y))
        self.wait(1.5)

        self.next_section("General Rule for Y-axis Reflection")

        self.play(FadeOut(y_demo_group), FadeOut(point_subtitle_y), FadeOut(calc_summary_y))
        self.wait(0.3)

        self.play(grid.animate.shift(RIGHT * 2.5))

        rule_y_heading = Text("Reflection over the y-axis:", font_size=26, weight=BOLD, color=BLUE)
        rule_y_line1 = MathTex(r"\text{y stays the same, x flips sign}", font_size=24)
        rule_y_box = MathTex(r"(x, y) \rightarrow (-x, \, y)", font_size=30, color=PURPLE_E)

        rule_y_group = VGroup(rule_y_heading, rule_y_line1, rule_y_box).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        bg_card_y = RoundedRectangle(
            corner_radius=0.15,
            height=rule_y_group.height + 0.6,
            width=rule_y_group.width + 0.6,
        )
        rule_y_group.move_to(bg_card_y)
        rule_card_y = VGroup(bg_card_y, rule_y_group).to_edge(LEFT, buff=0.4)

        self.play(FadeIn(rule_card_y))

        gen_y_group = reflect_point_demo(
            (1.5, -2),
            (-1.5, -2),
            "y",
            "(x, y)",
            "(-x, y)",
        )
        self.wait(2)

        self.next_section("Final Conclusion")

        self.play(
            FadeOut(grid),
            FadeOut(gen_y_group),
        )
        self.wait(0.5)

        rule_card_x.move_to(ORIGIN)
        both_rules = VGroup(rule_card_x, rule_card_y.copy()).arrange(DOWN, buff=0.5).move_to(ORIGIN)

        self.play(FadeIn(rule_card_x.move_to(both_rules[0].get_center())))
        self.play(rule_card_y.animate.move_to(both_rules[1].get_center()))
        self.wait(2)
