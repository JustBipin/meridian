import numpy as np
from manim import *
from manim_themes.manim_theme import apply_theme


class ParallelogramArea(MovingCameraScene):
    """
    Area of Parallelogram Animation
    -------------------------------
    Concept:
        The area of a parallelogram is shown by transforming it into a
        rectangle and by viewing it as two congruent triangles.

    Flow:
    1. Title
    2. Definition
    3. Highlight opposite sides
    4. Pose the area question
    5. Method One: Construct the parallelogram
    6. Label the base and height
    7. Identify the true height
    8. Rearrange into a rectangle
    9. Show the area is unchanged
    10. Derive the formula A = b × h
    11. Method Two: Split into two triangles
    12. Derive the area using triangle areas
    13. Present the final formula
    """

    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):

        # =========================================================
        # TITLE
        # =========================================================

        title = Text("Area of Parallelogram", font_size=56, weight=BOLD)

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

        def make_ticks(p1, p2, count, color=GREY_D, tick_length=0.16, spacing=0.09):
            """Small perpendicular dash marks across a segment, used to show congruent sides."""
            direction = p2 - p1
            length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
            unit = direction / length
            perp = unit.copy()
            perp[0] = -unit[1]
            perp[1] = unit[0]
            perp = perp * (tick_length / 2)
            mid = (p1 + p2) / 2
            ticks = VGroup()
            for i in range(count):
                center = mid + unit * spacing * (i - (count - 1) / 2)
                ticks.add(Line(center - perp, center + perp, color=color, stroke_width=3))
            return ticks

        # =========================================================
        # 2 & 3. INTRO DIAGRAM + DEFINITION
        #    Opposite sides are highlighted together, pair by pair,
        #    while the definition is on screen.
        # =========================================================
        IB = grid.c2p(-2.2, -1)
        IC = grid.c2p(1.8, -1)
        ID = grid.c2p(2.7, 1)
        IA = grid.c2p(-1.3, 1)

        intro_para = Polygon(
            IB,
            IC,
            ID,
            IA,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(intro_para), run_time=1)
        self.wait(0.5)

        definition_text = Text(
            "A four-sided shape (quadrilateral) whose\nopposite sides are equal in length and parallel.",
            font_size=28,
            line_spacing=1.2,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(definition_text))

        highlight_bottom = Line(IB, IC, color=RED, stroke_width=6)
        highlight_top = Line(IA, ID, color=RED, stroke_width=6)
        highlight_left = Line(IB, IA, color=GREEN, stroke_width=6)
        highlight_right = Line(IC, ID, color=GREEN, stroke_width=6)

        self.play(Create(highlight_bottom), Create(highlight_top), run_time=1)
        self.wait(1)
        self.play(Create(highlight_right), Create(highlight_left), run_time=1)
        self.wait(1.5)

        self.play(
            FadeOut(highlight_bottom),
            FadeOut(highlight_top),
            FadeOut(highlight_right),
            FadeOut(highlight_left),
            run_time=0.8,
        )
        self.wait(0.5)

        # =========================================================
        # 4. SWAP THE DEFINITION FOR THE QUESTION
        # =========================================================
        question_text = Text("How do you find the area?", font_size=30).move_to(definition_text.get_center())
        self.play(FadeOut(definition_text))
        self.play(Write(question_text))
        self.wait(2)

        self.play(FadeOut(question_text), FadeOut(intro_para), run_time=1)
        self.wait(0.5)

        # =========================================================
        # 5. NEW SCENE: METHOD ONE
        # =========================================================
        method_header = Text("Method One", font_size=35, weight=BOLD).to_edge(UP, buff=0.6)
        self.play(Write(method_header))
        self.wait(1)

        # =========================================================
        # 6. BUILD THE PARALLELOGRAM: base = 5, height = 3, slant = 60°
        # =========================================================
        base_len = 5
        height_len = 3
        offset = height_len / (3**0.5)  # tan(60°) = sqrt(3)

        center_x = (base_len + offset) / 2
        center_y = height_len / 2

        P1 = grid.c2p(0 - center_x, 0 - center_y)  # bottom-left
        P2 = grid.c2p(base_len - center_x, 0 - center_y)  # bottom-right
        P3 = grid.c2p(base_len + offset - center_x, height_len - center_y)  # top-right
        P4 = grid.c2p(offset - center_x, height_len - center_y)  # top-left
        G = grid.c2p(base_len - center_x, height_len - center_y)  # foot of the true height, on the top edge

        para = Polygon(
            P1,
            P2,
            P3,
            P4,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(para), run_time=1)
        self.wait(0.5)

        para_caption = Text("Take a parallelogram of base b and height h.", font_size=28).next_to(para, DOWN, buff=0.8)
        self.play(Write(para_caption))
        self.wait(1.5)
        self.play(FadeOut(para_caption))

        base_brace = Brace(Line(P1, P2), direction=DOWN, color=GREY_D, buff=0.15)
        base_label = base_brace.get_tex("b").set_color(GREY_D)
        self.play(FadeIn(base_brace), Write(base_label), run_time=1)
        self.wait(1)

        # =========================================================
        # 7. WARNING: THE SLANTED SIDE IS NOT THE HEIGHT
        # =========================================================
        mid_slant = (P2 + P3) / 2
        warning_text = Text("Not the height!", font_size=24, color=RED).next_to(mid_slant, RIGHT, buff=0.9)
        warning_arrow = Arrow(start=warning_text.get_left(), end=mid_slant, color=RED, buff=0.15, stroke_width=3)
        self.play(Write(warning_text), GrowArrow(warning_arrow), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(warning_text), FadeOut(warning_arrow), run_time=0.8)
        self.wait(0.3)

        # The TRUE height: perpendicular from the bottom-right vertex up to the top edge.
        height_line = DashedLine(P2, G, color=GREY_D, stroke_width=2)
        self.play(Create(height_line), run_time=1)

        height_brace = Brace(height_line, direction=RIGHT, color=GREY_D, buff=0.12)
        height_label = height_brace.get_tex("h").set_color(GREY_D)
        self.play(FadeIn(height_brace), Write(height_label), run_time=1)
        self.wait(1.5)

        # =========================================================
        # 8. CHOP THE RIGHT TRIANGLE OFF AND SLIDE IT TO THE LEFT
        # =========================================================
        trapezoid = Polygon(
            P1,
            P2,
            G,
            P4,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        cut_tri = Polygon(
            P2,
            G,
            P3,
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_color=BLUE,
            stroke_width=4,
        )

        cut_caption = Text("Cut vertically from the bottom-right vertex to form a triangle.", font_size=26).next_to(
            para, DOWN, buff=1.5
        )
        self.play(Write(cut_caption))
        self.wait(1)

        self.play(
            FadeOut(para),
            FadeOut(height_line),
            FadeOut(cut_caption),
            FadeIn(trapezoid),
            FadeIn(cut_tri),
            run_time=0.8,
        )
        self.wait(1)

        # Preview the empty space waiting on the left, as a dotted triangle.
        top_left = grid.c2p(0 - center_x, height_len - center_y)
        gap_vertical = DashedLine(P1, top_left, color=GREY_D, stroke_width=2)
        gap_horizontal = DashedLine(top_left, P4, color=GREY_D, stroke_width=2)
        self.play(Create(gap_vertical), Create(gap_horizontal), run_time=1)
        self.wait(1)

        # Show that corresponding sides of the two triangles are equal.
        congruence_caption = Text("Corresponding sides are equal.", font_size=26).to_edge(DOWN, buff=0.3)
        self.play(Write(congruence_caption))

        ticks_vertical_cut = make_ticks(P2, G, 1)
        ticks_vertical_gap = make_ticks(P1, top_left, 1)
        ticks_top_cut = make_ticks(G, P3, 2)
        ticks_top_gap = make_ticks(top_left, P4, 2)
        ticks_hyp_cut = make_ticks(P3, P2, 3)
        ticks_hyp_gap = make_ticks(P4, P1, 3)

        self.play(Create(ticks_vertical_cut), Create(ticks_vertical_gap), run_time=0.6)
        self.play(Create(ticks_top_cut), Create(ticks_top_gap), run_time=0.6)
        self.play(Create(ticks_hyp_cut), Create(ticks_hyp_gap), run_time=0.6)
        self.wait(1.5)

        self.play(
            FadeOut(gap_vertical),
            FadeOut(gap_horizontal),
            FadeOut(congruence_caption),
            FadeOut(ticks_vertical_cut),
            FadeOut(ticks_vertical_gap),
            FadeOut(ticks_top_cut),
            FadeOut(ticks_top_gap),
            FadeOut(ticks_hyp_cut),
            FadeOut(ticks_hyp_gap),
            run_time=0.8,
        )
        self.wait(0.3)

        shift_vector = P1 - P2  # slides P2 -> P1, G -> top-left corner, P3 -> P4

        self.play(cut_tri.animate.shift(UP * 0.5), run_time=0.6)
        self.wait(0.3)
        self.play(cut_tri.animate.shift(shift_vector - UP * 0.5), run_time=1.5)
        self.wait(1)

        # =========================================================
        # 9. NOW A RECTANGLE — MARK THE RIGHT ANGLES
        # =========================================================
        corner_marks = VGroup(
            RightAngle(Line(P1, P2), Line(P1, top_left), length=0.22, color=GREY_D),
            RightAngle(Line(P2, G), Line(P2, P1), length=0.22, color=GREY_D),
            RightAngle(Line(G, top_left), Line(G, P2), length=0.22, color=GREY_D),
            RightAngle(Line(top_left, P1), Line(top_left, G), length=0.22, color=GREY_D),
        )
        self.play(Create(corner_marks), run_time=1)
        self.wait(1.5)

        rectangle_group = VGroup(trapezoid, cut_tri, corner_marks, base_brace, base_label, height_brace, height_label)

        rectangle_caption = Text(
            "This is now a rectangle — the area hasn't changed,\njust the placement of the shapes.",
            font_size=26,
            line_spacing=1.2,
        ).next_to(rectangle_group, DOWN, buff=0.3)
        self.play(Write(rectangle_caption))
        self.wait(2)
        self.play(FadeOut(rectangle_caption))

        # =========================================================
        # 10. FINAL FORMULA
        # =========================================================
        final_formula = MathTex("A", "=", "b", r"\times", "h").scale(1.1).next_to(rectangle_group, DOWN, buff=0.7)
        final_box = SurroundingRectangle(final_formula, color=BLUE, buff=0.2, corner_radius=0.1)

        self.play(Write(final_formula), Create(final_box))
        self.wait(6)

        # =========================================================
        # METHOD TWO: SAME PARALLELOGRAM, SPLIT DIAGONALLY
        # =========================================================
        self.play(
            FadeOut(rectangle_group),
            FadeOut(final_formula),
            FadeOut(final_box),
            FadeOut(method_header),
            run_time=1,
        )
        self.wait(0.5)

        method2_header = Text("Method Two", font_size=35, weight=BOLD).to_edge(UP, buff=0.6)
        self.play(Write(method2_header))
        self.wait(1)

        # Rebuild the same parallelogram (base = 5, height = 3, 60° slant)
        para2 = Polygon(
            P1,
            P2,
            P3,
            P4,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(para2), run_time=1)
        self.wait(0.5)

        # Label base and height, same as before.
        base_brace2 = Brace(Line(P1, P2), direction=DOWN, color=GREY_D, buff=0.15)
        base_label2 = base_brace2.get_tex("b").set_color(GREY_D)
        self.play(FadeIn(base_brace2), Write(base_label2), run_time=1)

        height_line2 = DashedLine(P2, G, color=GREY_D, stroke_width=2)
        self.play(Create(height_line2), run_time=1)
        height_brace2 = Brace(height_line2, direction=RIGHT, color=GREY_D, buff=0.12)
        height_label2 = height_brace2.get_tex("h").set_color(GREY_D)
        self.play(FadeIn(height_brace2), Write(height_label2), run_time=1)
        self.wait(1.5)

        self.play(
            FadeOut(base_brace2),
            FadeOut(base_label2),
            FadeOut(height_brace2),
            FadeOut(height_label2),
            run_time=0.8,
        )

        # Split diagonally, then physically separate the two halves.
        diagonal2 = Line(P1, P3, color=BLACK, stroke_width=3)
        self.play(Create(diagonal2), run_time=1)
        self.wait(1)

        tri_A = Polygon(
            P1,
            P2,
            P3,
            fill_color=BLUE,
            fill_opacity=0.6,
            stroke_color=BLUE,
            stroke_width=4,
        )
        tri_B = Polygon(
            P1,
            P3,
            P4,
            fill_color=RED,
            fill_opacity=0.5,
            stroke_color=RED,
            stroke_width=4,
        )

        self.play(
            FadeOut(para2),
            FadeOut(height_line2),
            FadeOut(diagonal2),
            FadeIn(tri_A),
            FadeIn(tri_B),
            run_time=0.8,
        )
        self.wait(1)

        # =========================================================
        # MODIFICATION: Zoom out and align horizontally with MORE space
        # =========================================================
        self.play(
            # Scale > 1 zooms out. Shift DOWN to leave room for text at the bottom.
            self.camera.frame.animate.scale(1.3).shift(DOWN * 1.2),
            # Increased spacing from 3.5 to 4.5
            tri_A.animate.move_to(LEFT * 4.5 + UP * 1),
            tri_B.animate.move_to(RIGHT * 4.5 + UP * 1),
            run_time=1.5,
        )
        self.wait(1)
        # =========================================================

        # Label triangle A: base P1-P2, apex P3.
        a1, a2, a3 = tri_A.get_vertices()
        base_brace_A = Brace(Line(a1, a2), direction=DOWN, color=GREY_D, buff=0.15)
        base_label_A = base_brace_A.get_tex("b").set_color(GREY_D)

        foot_A = a3.copy()
        foot_A[1] = a1[1]
        height_line_A = DashedLine(a3, foot_A, color=GREY_D, stroke_width=2)
        height_brace_A = Brace(height_line_A, direction=RIGHT, color=GREY_D, buff=0.12)
        height_label_A = height_brace_A.get_tex("h").set_color(GREY_D)

        self.play(FadeIn(base_brace_A), Write(base_label_A), run_time=0.8)
        self.play(Create(height_line_A), run_time=0.8)
        self.play(FadeIn(height_brace_A), Write(height_label_A), run_time=0.8)
        self.wait(1)

        # Label triangle B: base P4-P3, apex P1.
        b1, b2, b3 = tri_B.get_vertices()
        base_brace_B = Brace(Line(b3, b2), direction=UP, color=GREY_D, buff=0.15)
        base_label_B = base_brace_B.get_tex("b").set_color(GREY_D)

        # Draw height on the RIGHT side by dropping down from the top-right vertex (b2)
        foot_B = b2.copy()
        foot_B[1] = b1[1]  # Match the Y-coordinate of the apex
        height_line_B = DashedLine(b2, foot_B, color=GREY_D, stroke_width=2)
        height_brace_B = Brace(height_line_B, direction=RIGHT, color=GREY_D, buff=0.12)
        height_label_B = height_brace_B.get_tex("h").set_color(GREY_D)

        self.play(FadeIn(base_brace_B), Write(base_label_B), run_time=0.8)
        self.play(Create(height_line_B), run_time=0.8)
        self.play(FadeIn(height_brace_B), Write(height_label_B), run_time=0.8)
        self.wait(1.5)

        triangle_A_group = VGroup(tri_A, base_brace_A, base_label_A, height_line_A, height_brace_A, height_label_A)
        triangle_B_group = VGroup(tri_B, base_brace_B, base_label_B, height_line_B, height_brace_B, height_label_B)
        both_group = VGroup(triangle_A_group, triangle_B_group)

        # Derive the total area.
        eq_font2 = 40

        each_tri_eq = MathTex(r"\text{Area of each triangle} = \frac{1}{2} \times b \times h", font_size=eq_font2).next_to(
            both_group, DOWN, buff=0
        )
        self.play(Write(each_tri_eq))
        self.wait(1.5)

        two_note = Text("But there are two such triangles.", font_size=26)
        two_note.next_to(each_tri_eq, DOWN, buff=0.3)
        self.play(Write(two_note))
        self.wait(1)

        total_eq = MathTex(
            r"\text{Total Area} = 2 \times \frac{1}{2} \times b \times h = b \times h",
            font_size=eq_font2,
        )
        total_eq.next_to(two_note, DOWN, buff=0.35)
        self.play(Write(total_eq))
        self.wait(1.5)

        final_formula2 = MathTex(r"\text{Area of Parallelogram} = b \times h", font_size=45)
        final_formula2.next_to(total_eq, DOWN, buff=0.5)
        final_box2 = SurroundingRectangle(final_formula2, color=BLUE, buff=0.2, corner_radius=0.1)

        self.play(Write(final_formula2), Create(final_box2))
        self.wait(6)


class RhombusArea(MovingCameraScene):
    """
    Area of Rhombus Animation
    -------------------------
    Concept:
        The area of a rhombus is obtained by treating one side as the base
        and using its perpendicular height.

    Flow:
    1. Title
    2. Definition
    3. Highlight the equal sides
    4. Pose the area question
    5. Construct the rhombus
    6. Label all sides
    7. Retain the chosen base
    8. Identify the true height
    9. Derive the formula A = b × h
    """

    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):

        # =========================================================
        # TITLE
        # =========================================================

        title = Text("Area of Rhombus", font_size=56, weight=BOLD)

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

        def rhombus_points(side, angle_deg):
            """Vertices of a rhombus (all sides = side) tilted by angle_deg, centered near the origin.
            Also returns G, the point on the top edge directly above the bottom-right vertex —
            i.e. the foot of the true (vertical) height."""
            angle = angle_deg * DEGREES
            dx = side * np.cos(angle)
            dy = side * np.sin(angle)
            cx = (side + dx) / 2
            cy = dy / 2
            p1 = grid.c2p(0 - cx, 0 - cy)  # bottom-left
            p2 = grid.c2p(side - cx, 0 - cy)  # bottom-right
            p3 = grid.c2p(side + dx - cx, dy - cy)  # top-right
            p4 = grid.c2p(dx - cx, dy - cy)  # top-left
            g = grid.c2p(side - cx, dy - cy)  # foot of the true height, on the top edge
            return p1, p2, p3, p4, g

        def make_tick(p1, p2, color=GREY_D, tick_length=0.2):
            """A single congruency tick: a short line perpendicular to the segment, centered on its midpoint."""
            direction = p2 - p1
            length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
            unit = direction / length
            perp = np.array([-unit[1], unit[0], 0]) * (tick_length / 2)
            mid = (p1 + p2) / 2
            return Line(mid - perp, mid + perp, color=color, stroke_width=3)

        def outward_normal(p1, p2, center):
            """Unit vector perpendicular to segment p1->p2, pointing away from `center`.
            Passing this as a Brace's `direction` makes the brace hug a slanted side
            at the correct angle, instead of snapping to a fixed axis."""
            direction = p2 - p1
            length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
            unit = direction / length
            perp = np.array([-unit[1], unit[0], 0])
            mid = (p1 + p2) / 2
            if np.dot(perp, mid - center) < 0:
                perp = -perp
            return perp

        # =========================================================
        # 2 & 3. INTRO DIAGRAM + DEFINITION
        #    All four sides carry the same perpendicular congruency
        #    tick, since in a rhombus every side is equal.
        # =========================================================
        IB, IC, ID, IA, _ = rhombus_points(2.6, 65)

        intro_rhombus = Polygon(
            IB,
            IC,
            ID,
            IA,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(intro_rhombus), run_time=1)
        self.wait(0.5)

        definition_text = Text(
            "A special parallelogram whose\nfour sides are all equal in length.",
            font_size=28,
            line_spacing=1.2,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(definition_text))

        tick_bottom = make_tick(IB, IC)
        tick_right = make_tick(IC, ID)
        tick_top = make_tick(ID, IA)
        tick_left = make_tick(IA, IB)

        self.play(Create(tick_bottom), run_time=0.6)
        self.play(Create(tick_right), run_time=0.6)
        self.play(Create(tick_top), run_time=0.6)
        self.play(Create(tick_left), run_time=0.6)
        self.wait(1.5)

        self.play(
            FadeOut(tick_bottom),
            FadeOut(tick_right),
            FadeOut(tick_top),
            FadeOut(tick_left),
            run_time=0.8,
        )
        self.wait(0.5)

        # =========================================================
        # 4. SWAP THE DEFINITION FOR THE QUESTION
        # =========================================================
        question_text = Text("Area = ?", font_size=34, weight=BOLD).move_to(definition_text.get_center())
        self.play(FadeOut(definition_text))
        self.play(Write(question_text))
        self.wait(2)

        self.play(FadeOut(question_text), FadeOut(intro_rhombus), run_time=1)
        self.wait(0.5)

        # =========================================================
        # 5. BUILD THE RHOMBUS: side = b, tilt = 65°
        # =========================================================
        R1, R2, R3, R4, G = rhombus_points(3, 65)

        rhombus = Polygon(
            R1,
            R2,
            R3,
            R4,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(rhombus), run_time=1)
        self.wait(0.5)

        rhombus_caption = Text("Take a rhombus with side length b.", font_size=28).next_to(rhombus, DOWN, buff=0.8)
        self.play(Write(rhombus_caption))
        self.wait(1.5)
        self.play(FadeOut(rhombus_caption))

        # =========================================================
        # 6. LABEL ALL FOUR SIDES AS b
        # =========================================================
        shape_center = (R1 + R2 + R3 + R4) / 4

        bottom_brace = Brace(Line(R1, R2), direction=outward_normal(R1, R2, shape_center), color=GREY_D, buff=0.15)
        bottom_label = bottom_brace.get_tex("b").set_color(GREY_D)

        right_brace = Brace(Line(R2, R3), direction=outward_normal(R2, R3, shape_center), color=GREY_D, buff=0.15)
        right_label = right_brace.get_tex("b").set_color(GREY_D)

        top_brace = Brace(Line(R4, R3), direction=outward_normal(R4, R3, shape_center), color=GREY_D, buff=0.15)
        top_label = top_brace.get_tex("b").set_color(GREY_D)

        left_brace = Brace(Line(R1, R4), direction=outward_normal(R1, R4, shape_center), color=GREY_D, buff=0.15)
        left_label = left_brace.get_tex("b").set_color(GREY_D)

        self.play(FadeIn(bottom_brace), Write(bottom_label), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(right_brace), Write(right_label), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(top_brace), Write(top_label), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(left_brace), Write(left_label), run_time=0.8)
        self.wait(1.5)

        # =========================================================
        # 7. KEEP ONLY THE BASE LABEL
        # =========================================================
        self.play(
            FadeOut(right_brace),
            FadeOut(right_label),
            FadeOut(top_brace),
            FadeOut(top_label),
            FadeOut(left_brace),
            FadeOut(left_label),
            run_time=0.8,
        )
        self.wait(0.5)

        # =========================================================
        # 8. THE TRUE HEIGHT — PERPENDICULAR FROM THE BOTTOM-RIGHT
        #    VERTEX UP TO THE TOP EDGE
        # =========================================================
        mid_slant = (R2 + R3) / 2
        warning_text = Text("Not the height!", font_size=24, color=RED).next_to(mid_slant, RIGHT, buff=0.9)
        warning_arrow = Arrow(start=warning_text.get_left(), end=mid_slant, color=RED, buff=0.15, stroke_width=3)
        self.play(Write(warning_text), GrowArrow(warning_arrow), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(warning_text), FadeOut(warning_arrow), run_time=0.8)
        self.wait(0.3)

        height_line = DashedLine(R2, G, color=GREY_D, stroke_width=2)
        self.play(Create(height_line), run_time=1)

        height_brace = Brace(height_line, direction=RIGHT, color=GREY_D, buff=0.12)
        height_label = height_brace.get_tex("h").set_color(GREY_D)
        self.play(FadeIn(height_brace), Write(height_label), run_time=1)
        self.wait(1.5)

        # =========================================================
        # 9. FINAL FORMULA
        # =========================================================
        final_group = VGroup(rhombus, bottom_brace, bottom_label, height_line, height_brace, height_label)

        final_formula = MathTex("A", "=", "b", r"\times", "h").scale(1.1).next_to(final_group, DOWN, buff=0.7)
        final_box = SurroundingRectangle(final_formula, color=BLUE, buff=0.2, corner_radius=0.1)

        self.play(Write(final_formula), Create(final_box))
        self.wait(6)


class TrapeziumArea(MovingCameraScene):
    """
    Area of Trapezium Animation
    ---------------------------
    Concept:
        The area of a trapezium is derived by splitting it into two triangles
        and adding their individual areas.

    Flow:
    1. Title
    2. Definition
    3. Highlight the pair of parallel sides
    4. Pose the area question
    5. Construct the trapezium
    6. Label the parallel sides and height
    7. Draw the height
    8. Split the trapezium with a diagonal
    9. Label the two triangles
    10. Derive the area of each triangle
    11. Add the two triangle areas
    12. Factorise the expression
    13. Present the final formula
    """

    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):

        # =========================================================
        # TITLE
        # =========================================================

        title = Text("Area of Trapezium", font_size=56, weight=BOLD)

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

        def trapezium_points(bottom, top, height, left_offset):
            """Vertices of a trapezium with parallel sides `bottom` (b, at the base) and
            `top` (a, above), height `height` (h), centered near the origin.
            E and G are the feet of the perpendiculars dropped from A and B onto the base —
            used later to show the true height."""

            cx = bottom / 2
            cy = height / 2
            D = grid.c2p(0 - cx, 0 - cy)  # bottom-left
            C = grid.c2p(bottom - cx, 0 - cy)  # bottom-right
            B = grid.c2p(left_offset + top - cx, height - cy)  # top-right
            A = grid.c2p(left_offset - cx, height - cy)  # top-left
            E = grid.c2p(left_offset - cx, 0 - cy)  # foot of perpendicular from A
            G = grid.c2p(left_offset + top - cx, 0 - cy)  # foot of perpendicular from B
            return D, C, B, A, E, G

        def make_parallel_mark(p1, p2, color=GREY_D, size=0.4):
            """A single chevron placed at a segment's midpoint, pointing from p1 to p2 —
            the standard notation for 'this side is parallel to the matching one'
            (as opposed to a perpendicular tick, which would mean 'equal length')."""

            direction = p2 - p1
            length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
            unit = direction / length
            mid = (p1 + p2) / 2
            mark = Line(mid - unit * size / 2, mid + unit * size / 2, color=color, stroke_width=4)
            mark.add_tip(tip_length=0.18)
            return mark

        # =========================================================
        # 2 & 3. INTRO DIAGRAM + DEFINITION
        #    The two parallel sides are highlighted together, with
        #    matching chevrons to mark them as parallel (not equal).
        # =========================================================
        ID, IC, IB, IA, _, _ = trapezium_points(4, 2.2, 2, 0.7)

        intro_trap = Polygon(
            ID,
            IC,
            IB,
            IA,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(intro_trap), run_time=1)
        self.wait(0.5)

        definition_text = Text(
            "A quadrilateral with exactly\none pair of parallel sides.",
            font_size=28,
            line_spacing=1.2,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(definition_text))

        highlight_top = Line(IA, IB, color=ORANGE, stroke_width=6)
        highlight_bottom = Line(ID, IC, color=ORANGE, stroke_width=6)
        self.play(Create(highlight_top), Create(highlight_bottom), run_time=1)
        self.wait(1)

        mark_top = make_parallel_mark(IA, IB, color=ORANGE)
        mark_bottom = make_parallel_mark(ID, IC, color=ORANGE)
        self.play(Create(mark_top), Create(mark_bottom), run_time=0.8)
        self.wait(1.5)

        self.play(
            FadeOut(highlight_top),
            FadeOut(highlight_bottom),
            FadeOut(mark_top),
            FadeOut(mark_bottom),
            run_time=0.8,
        )
        self.wait(0.5)

        # =========================================================
        # 4. SWAP THE DEFINITION FOR THE QUESTION
        # =========================================================
        question_text = Text("Area = ?", font_size=34, weight=BOLD).move_to(definition_text.get_center())
        self.play(FadeOut(definition_text))
        self.play(Write(question_text))
        self.wait(2)

        self.play(FadeOut(question_text), FadeOut(intro_trap), run_time=1)
        self.wait(0.5)

        # =========================================================
        # 5. BUILD THE TRAPEZIUM: parallel sides b (bottom) and a (top), height h
        # =========================================================
        D, C, B, A, E, G = trapezium_points(6, 3.2, 3, 1.0)

        trapezium = Polygon(
            D,
            C,
            B,
            A,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(trapezium), run_time=1)
        self.wait(0.5)

        trap_caption = Text(
            "Take a trapezium with parallel sides a and b,\nand height h.",
            font_size=28,
            line_spacing=1.2,
        ).next_to(trapezium, DOWN, buff=0.8)
        self.play(Write(trap_caption))
        self.wait(1.5)
        self.play(FadeOut(trap_caption))

        # =========================================================
        # 6. LABEL THE TWO PARALLEL SIDES
        # =========================================================
        bottom_brace = Brace(Line(D, C), direction=DOWN, color=GREY_D, buff=0.15)
        bottom_label = bottom_brace.get_tex("b").set_color(GREY_D)

        top_brace = Brace(Line(A, B), direction=UP, color=GREY_D, buff=0.15)
        top_label = top_brace.get_tex("a").set_color(GREY_D)

        self.play(FadeIn(bottom_brace), Write(bottom_label), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(top_brace), Write(top_label), run_time=0.8)
        self.wait(1.5)

        # =========================================================
        # 7. THE HEIGHT — PERPENDICULAR FROM THE TOP-RIGHT VERTEX
        #    DOWN TO THE BASE
        # =========================================================
        height_line = DashedLine(B, G, color=GREY_D, stroke_width=2)
        self.play(Create(height_line), run_time=1)

        height_brace = Brace(height_line, direction=RIGHT, color=GREY_D, buff=0.11)
        height_label = height_brace.get_tex("h").set_color(GREY_D)
        self.play(FadeIn(height_brace), Write(height_label), run_time=1)
        self.wait(1.5)

        # =========================================================
        # 8. SPLIT INTO TWO TRIANGLES WITH DIAGONAL AC
        # =========================================================
        split_caption = Text(
            "Draw diagonal AC to split the trapezium\ninto two triangles.",
            font_size=26,
            line_spacing=1.2,
        ).next_to(trapezium, DOWN, buff=1.3)
        self.play(Write(split_caption))
        self.wait(1)

        diagonal = Line(A, C, color=WHITE, stroke_width=3)
        tri1 = Polygon(A, D, C, fill_color=RED, fill_opacity=0.6, stroke_color=RED, stroke_width=4)
        tri2 = Polygon(A, B, C, fill_color=BLUE, fill_opacity=0.6, stroke_color=BLUE, stroke_width=4)

        self.play(
            FadeOut(trapezium),
            FadeOut(split_caption),
            FadeIn(tri1),
            FadeIn(tri2),
            Create(diagonal),
            run_time=1,
        )
        self.wait(1)

        # =========================================================
        # 9. ZOOM OUT TO MAKE ROOM FOR THE DERIVATION BELOW
        #    (estimated for this exact layout — nudge scale/shift if
        #    anything clips near the top or bottom edge once rendered)
        # =========================================================
        self.play(self.camera.frame.animate.scale(1.3).move_to(np.array([0, -2.0, 0])), run_time=1.2)
        self.wait(0.3)

        # =========================================================
        # 10. LABEL THE TWO TRIANGLES
        # =========================================================
        t1_pos = (A + D + C) / 3
        t2_pos = (A + B + C) / 3
        t1_label = MathTex("t_1", font_size=36).move_to(t1_pos)
        t2_label = MathTex("t_2", font_size=36).move_to(t2_pos)
        self.play(Write(t1_label), Write(t2_label), run_time=1)
        self.wait(1.5)

        # =========================================================
        # 11. BUILD THE AREA FORMULA, STEP BY STEP
        # =========================================================
        diagram_group = VGroup(
            tri1,
            tri2,
            diagonal,
            bottom_brace,
            bottom_label,
            top_brace,
            top_label,
            height_line,
            height_brace,
            height_label,
            t1_label,
            t2_label,
        )
        # Create line 1 and line 2
        line1 = MathTex(r"A_{t_1} = \frac{1}{2} \, b \, h", font_size=38)
        line2 = MathTex(r"A_{t_2} = \frac{1}{2} \, a \, h", font_size=38)

        # Group them, arrange side by side, place below diagram_group, and center on y-axis
        top_lines = VGroup(line1, line2).arrange(RIGHT, buff=2.0).next_to(diagram_group, DOWN, buff=0.3).set_x(0)

        self.play(Write(line1))
        self.wait(1)
        self.play(Write(line2))
        self.wait(1)

        # Place line 3 below the top group and center on y-axis
        line3 = MathTex(r"A = A_{t_1} + A_{t_2}", font_size=38)
        line3.next_to(top_lines, DOWN, buff=0.4).set_x(0)

        self.play(Write(line3))
        self.wait(1)

        # Place line 4 below line 3 and center on y-axis
        line4 = MathTex(r"A = \frac{1}{2} \, b \, h + \frac{1}{2} \, a \, h", font_size=38)
        line4.next_to(line3, DOWN, buff=0.3).set_x(0)

        self.play(Write(line4))
        self.wait(1)

        # Place line 5 below line 4 and center on y-axis
        line5 = MathTex(r"\text{Area of a Trapezium} = \frac{1}{2} \, h \, (a + b)", font_size=42)
        line5.next_to(line4, DOWN, buff=0.4).set_x(0)

        final_box = SurroundingRectangle(line5, color=BLUE, buff=0.2, corner_radius=0.1)

        self.play(Write(line5), Create(final_box))
        self.wait(6)


class QuadrilateralArea(MovingCameraScene):
    """
    Area of Quadrilateral Animation
    -------------------------------
    Concept:
        The area of a quadrilateral is derived by dividing it into two
        triangles along a diagonal and summing their areas.

    Flow:
    1. Title
    2. Definition
    3. Highlight the four sides and vertices
    4. Pose the area question
    5. Construct the quadrilateral
    6. Label the vertices
    7. Draw and label the diagonal
    8. Draw the perpendicular heights to the diagonal
    9. Split into two triangles
    10. Label the triangles
    11. Derive the area of each triangle
    12. Add and simplify the expressions
    13. Present the final formula
    """

    def setup(self):
        """Initializes scene configurations and applies the 'london' visual theme."""
        super().setup()
        apply_theme(manim_scene=self, theme_name="london")

    def construct(self):

        # =========================================================
        # TITLE
        # =========================================================

        title = Text("Area of Quadrilateral", font_size=56, weight=BOLD)

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

        def foot_of_perpendicular(point, line_a, line_b):
            """Foot of the perpendicular dropped from `point` onto the infinite
            line through `line_a` and `line_b`."""
            ap = point - line_a
            ab = line_b - line_a
            t = np.dot(ap, ab) / np.dot(ab, ab)
            return line_a + t * ab

        def right_angle_marker(foot, along_dir, perp_dir, size=0.22, color=GREY_D):
            """Small square marking a right angle at `foot`, built from the unit
            vector `along_dir` (running along the diagonal) and `perp_dir`
            (running toward the vertex the perpendicular was dropped from)."""
            p1 = foot + along_dir * size
            p2 = p1 + perp_dir * size
            p3 = foot + perp_dir * size
            return Polygon(foot, p1, p2, p3, color=color, stroke_width=2, fill_opacity=0)

        # =========================================================
        # 2 & 3. INTRO DIAGRAM + DEFINITION
        #    A generic quadrilateral with its four edges and four
        #    vertices highlighted, to anchor the definition.
        # =========================================================
        iA, iB, iC, iD = (
            grid.c2p(-2.1, 1.1),
            grid.c2p(-1.7, -1.6),
            grid.c2p(1.0, -0.4),
            grid.c2p(2.4, 1.8),
        )

        intro_quad = Polygon(
            iA,
            iB,
            iC,
            iD,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(intro_quad), run_time=1)
        self.wait(0.5)

        definition_text = Text(
            "A four-sided polygon that has\nfour edges and four vertices.",
            font_size=28,
            line_spacing=1.2,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(definition_text))
        self.wait(1)

        edges = VGroup(
            Line(iA, iB, color=ORANGE, stroke_width=6),
            Line(iB, iC, color=ORANGE, stroke_width=6),
            Line(iC, iD, color=ORANGE, stroke_width=6),
            Line(iD, iA, color=ORANGE, stroke_width=6),
        )
        vertex_dots = VGroup(*[Dot(p, color=ORANGE, radius=0.07) for p in (iA, iB, iC, iD)])
        self.play(Create(edges), FadeIn(vertex_dots), run_time=1.2)
        self.wait(1.5)

        self.play(FadeOut(edges), FadeOut(vertex_dots), run_time=0.8)
        self.wait(0.3)

        # =========================================================
        # 4. SWAP THE DEFINITION FOR THE QUESTION
        # =========================================================
        question_text = Text("Area = ?", font_size=34, weight=BOLD).move_to(definition_text.get_center())
        self.play(FadeOut(definition_text))
        self.play(Write(question_text))
        self.wait(2)

        self.play(FadeOut(question_text), FadeOut(intro_quad), run_time=1)
        self.wait(0.5)

        # =========================================================
        # 5. BUILD THE QUADRILATERAL ABCD
        # =========================================================
        A = grid.c2p(-2.1, 2.0)
        B = grid.c2p(-1.8, -0.7)
        C = grid.c2p(0.9, 0.0)
        D = grid.c2p(2.3, 2.6)

        quad = Polygon(
            A,
            B,
            C,
            D,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_color=BLUE,
            stroke_width=4,
        )
        self.play(FadeIn(quad), run_time=1)
        self.wait(0.5)

        quad_caption = Text(
            "Take a quadrilateral ABCD with\ndiagonal BD.",
            font_size=28,
            line_spacing=1.2,
        ).next_to(quad, DOWN, buff=0.8)
        self.play(Write(quad_caption))
        self.wait(1.5)

        # =========================================================
        # 6. LABEL THE FOUR VERTICES
        # =========================================================
        vertex_labels = VGroup(
            MathTex("A", font_size=34).next_to(A, UL, buff=0.15),
            MathTex("B", font_size=34).next_to(B, DL, buff=0.15),
            MathTex("C", font_size=34).next_to(C, DR, buff=0.15),
            MathTex("D", font_size=34).next_to(D, UR, buff=0.15),
        )
        self.play(Write(vertex_labels), run_time=1)
        self.wait(1)

        # =========================================================
        # 7. DRAW & LABEL THE DIAGONAL BD (= d)
        # =========================================================
        diagonal = Line(B, D, color=BLACK, stroke_width=3)
        self.play(Create(diagonal), run_time=1)

        d_label = MathTex("d", font_size=32, color=GREY_D).next_to(diagonal.get_center(), RIGHT, buff=0.15)
        self.play(Write(d_label))
        self.play(FadeOut(quad_caption))

        self.wait(1.5)

        # =========================================================
        # 8. THE HEIGHTS — PERPENDICULARS FROM A AND C ONTO DIAGONAL BD
        # =========================================================
        F = foot_of_perpendicular(A, B, D)
        E = foot_of_perpendicular(C, B, D)

        along = (D - B) / np.linalg.norm(D - B)
        dir_to_A = (A - F) / np.linalg.norm(A - F)
        dir_to_C = (C - E) / np.linalg.norm(C - E)

        height1_line = DashedLine(A, F, color=GREY_D, stroke_width=2)
        height2_line = DashedLine(C, E, color=GREY_D, stroke_width=2)

        marker_F = right_angle_marker(F, -along, dir_to_A)
        marker_E = right_angle_marker(E, along, dir_to_C)

        self.play(Create(height1_line), Create(height2_line), run_time=1)
        self.play(Create(marker_F), Create(marker_E), run_time=0.6)

        h1_label = MathTex("h_1", font_size=30, color=GREY_D).next_to(height1_line.get_center(), LEFT, buff=0.15)
        h2_label = MathTex("h_2", font_size=30, color=GREY_D).next_to(height2_line.get_center(), RIGHT, buff=0.15)
        self.play(Write(h1_label), Write(h2_label))
        self.wait(1.5)

        # =========================================================
        # 9. SPLIT INTO TWO TRIANGLES ALONG THE DIAGONAL BD
        #    (same base BD, different heights h1 and h2)
        # =========================================================
        split_caption = Text(
            "Diagonal BD splits ABCD into two\ntriangles sharing the same base.",
            font_size=26,
            line_spacing=1.2,
        ).next_to(quad, DOWN, buff=1.3)
        self.play(Write(split_caption))
        self.wait(1)

        tri1 = Polygon(A, B, D, fill_color=RED, fill_opacity=0.6, stroke_color=RED, stroke_width=4)
        tri2 = Polygon(B, C, D, fill_color=BLUE, fill_opacity=0.6, stroke_color=BLUE, stroke_width=4)

        self.play(
            FadeOut(quad),
            FadeOut(split_caption),
            FadeIn(tri1),
            FadeIn(tri2),
            run_time=1,
        )
        self.wait(1)

        # =========================================================
        # 10. ZOOM OUT TO MAKE ROOM FOR THE DERIVATION BELOW
        #    (estimated for this exact layout — nudge scale/shift if
        #    anything clips near the top or bottom edge once rendered)
        # =========================================================
        self.play(self.camera.frame.animate.scale(1.14).move_to(np.array([0, -1.3, 0])), run_time=1.2)
        self.wait(0.3)

        # =========================================================
        # 11. LABEL THE TWO TRIANGLES
        # =========================================================
        t1_pos = (A + B + D) / 3
        t2_pos = (B + C + D) / 3
        t1_label = MathTex("t_1", font_size=36).move_to(t1_pos)
        t2_label = MathTex("t_2", font_size=36).move_to(t2_pos)
        self.play(Write(t1_label), Write(t2_label), run_time=1)
        self.wait(2.5)

        # =========================================================
        # 12. BUILD THE AREA FORMULA, STEP BY STEP
        # =========================================================
        diagram_group = VGroup(
            tri1,
            tri2,
            diagonal,
            d_label,
            vertex_labels,
            height1_line,
            height2_line,
            marker_F,
            marker_E,
            h1_label,
            h2_label,
            t1_label,
            t2_label,
        )

        # Area of each triangle (same base d, different heights)
        line1 = MathTex(r"A_{t_1} = \frac{1}{2} \, d \, h_1", font_size=40)
        line2 = MathTex(r"A_{t_2} = \frac{1}{2} \, d \, h_2", font_size=40)

        top_lines = VGroup(line1, line2).arrange(RIGHT, buff=2.0).next_to(diagram_group, DOWN, buff=0.3).set_x(0)

        self.play(Write(line1))
        self.wait(1)
        self.play(Write(line2))
        self.wait(1)

        # Total area = sum of the two triangles
        line3 = MathTex(r"A = A_{t_1} + A_{t_2}", font_size=40)
        line3.next_to(top_lines, DOWN, buff=0.4).set_x(0)

        self.play(Write(line3))
        self.wait(1)

        # Substitute the individual triangle areas
        line4 = MathTex("A", "=", r"\frac12", "d", "h_1", "+", r"\frac12", "d", "h_2", font_size=40)
        line4.next_to(line3, DOWN, buff=0.5).set_x(0)

        self.play(Write(line4))
        self.wait(1)

        # Factor out the common term 1/2 * d
        line5 = MathTex("A", "=", r"\frac12", "d", "(", "h_1", "+", "h_2", ")", font_size=40)
        line5.next_to(line3, DOWN, buff=0.5).set_x(0)

        self.play(TransformMatchingTex(line4, line5), run_time=1.25)
        # self.play(Write(line5))
        self.wait(2)

        # =========================================================
        # 13. LET THE WHOLE DERIVATION VANISH, REVEAL THE FINAL FORMULA
        # =========================================================
        final_formula = MathTex(
            r"\text{Area of a Quadrilateral}", "=", r"\frac12", "d", "(", "h_1", "+", "h_2", ")", font_size=46
        )
        final_formula.next_to(diagram_group, DOWN, buff=1)
        # final_formula.move_to(self.camera.frame.get_center())

        self.play(
            FadeOut(t1_label, t2_label, line1, line2, line3, line4),
            ReplacementTransform(line5, final_formula),
            run_time=1.5,
        )

        final_box = SurroundingRectangle(final_formula, color=BLUE, buff=0.2, corner_radius=0.1)
        self.play(Create(final_box))
        self.wait(6)
