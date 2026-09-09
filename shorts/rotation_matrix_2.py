import numpy as np
from manim import *

# =============================================================
# Frame & Format Tokens
# =============================================================

PIXEL_WIDTH = 1080
PIXEL_HEIGHT = 1920
FRAME_RATE = 60

FRAME_SHORT_SIDE = 8.0
FRAME_HEIGHT = FRAME_SHORT_SIDE * (PIXEL_HEIGHT / PIXEL_WIDTH)

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.frame_height = 16
config.frame_width = 9


class RotationMatrices3D(Scene):
    def construct(self):

        # =============================================================
        # 1. Title Header
        # =============================================================

        axis_mode = ValueTracker(0.0)

        # 0 = Rx
        # 1 = Ry
        # 2 = Rz

        def get_title():

            mode = int(round(axis_mode.get_value()))

            labels = [
                "Rotation Matrix R_x",
                "Rotation Matrix R_y",
                "Rotation Matrix R_z",
            ]

            return Text(
                labels[min(mode, 2)],
                font_size=38,
                color="#F8F8F2",
            )

        title = always_redraw(lambda: get_title().to_edge(UP, buff=0.4))

        # =============================================================
        # 2. Theta Slider
        # =============================================================

        theta_tracker = ValueTracker(0.0)

        slider_line = NumberLine(
            x_range=[0, 2 * np.pi, np.pi / 2],
            length=6.0,
            color=GRAY,
            include_numbers=False,
        )

        ticks_labels = VGroup(
            MathTex("0", font_size=26),
            MathTex(r"\frac{\pi}{2}", font_size=26),
            MathTex(r"\pi", font_size=26),
            MathTex(r"\frac{3\pi}{2}", font_size=26),
            MathTex(r"2\pi", font_size=26),
        )

        for i, label in enumerate(ticks_labels):
            pos = slider_line.number_to_point(i * np.pi / 2)

            label.next_to(pos, DOWN, buff=0.14)

        slider_pointer = Triangle(
            color="#8BE9FD",
            fill_opacity=1.0,
        ).scale(0.12)

        slider_pointer.rotate(np.pi)

        def update_pointer(mob):

            val = theta_tracker.get_value()

            pos = slider_line.number_to_point(val)

            mob.move_to(pos + np.array([0, 0.2, 0]))

        slider_pointer.add_updater(update_pointer)

        def get_theta_tex():

            val = theta_tracker.get_value()

            deg = int(round(np.degrees(val)))

            rad_val = val / np.pi

            return MathTex(
                rf"\theta = {deg:3d}^\circ"
                rf"\quad "
                rf"({rad_val:.2f}\pi\text{{ rad}})",
                font_size=30,
                color="#8BE9FD",
            )

        theta_text = always_redraw(lambda: get_theta_tex().next_to(slider_line, UP, buff=0.22))

        slider_group = VGroup(
            slider_line,
            ticks_labels,
            slider_pointer,
            theta_text,
        )

        slider_group.next_to(title, DOWN, buff=0.3)

        # =============================================================
        # 3. Dynamic General Formula
        # =============================================================

        def get_formula_tex():

            mode = int(round(axis_mode.get_value()))

            if mode == 0:
                mat_str = (
                    r"\begin{bmatrix}"
                    r"1 & 0 & 0 \\"
                    r"0 & \cos\theta & -\sin\theta \\"
                    r"0 & \sin\theta & \cos\theta"
                    r"\end{bmatrix}"
                )

            elif mode == 1:
                mat_str = (
                    r"\begin{bmatrix}"
                    r"\cos\theta & 0 & \sin\theta \\"
                    r"0 & 1 & 0 \\"
                    r"-\sin\theta & 0 & \cos\theta"
                    r"\end{bmatrix}"
                )

            else:
                mat_str = (
                    r"\begin{bmatrix}"
                    r"\cos\theta & -\sin\theta & 0 \\"
                    r"\sin\theta & \cos\theta & 0 \\"
                    r"0 & 0 & 1"
                    r"\end{bmatrix}"
                )

            return MathTex(
                r"\begin{bmatrix}"
                r"x' \\ y' \\ z'"
                r"\end{bmatrix}"
                r" = " + mat_str + r"\begin{bmatrix}"
                r"x \\ y \\ z"
                r"\end{bmatrix}",
                font_size=28,
            )

        formula_tex = always_redraw(lambda: get_formula_tex().next_to(slider_group, DOWN, buff=0.3))

        # =============================================================
        # 4. Live Numeric Matrix
        # =============================================================

        def get_matrix_mobject():

            th = theta_tracker.get_value()

            c = np.cos(th)
            s = np.sin(th)

            c_str = f"{c:.2f}"
            s_str = f"{s:.2f}"
            neg_s_str = f"{-s:.2f}"

            mode = int(round(axis_mode.get_value()))

            if mode == 0:
                name = "R_x"

                m_body = (
                    rf"1.00 & 0.00 & 0.00 \\ "
                    rf"0.00 & {c_str} & {neg_s_str} \\ "
                    rf"0.00 & {s_str} & {c_str}"
                )

            elif mode == 1:
                name = "R_y"

                m_body = (
                    rf"{c_str} & 0.00 & {s_str} \\ "
                    rf"0.00 & 1.00 & 0.00 \\ "
                    rf"{neg_s_str} & 0.00 & {c_str}"
                )

            else:
                name = "R_z"

                m_body = (
                    rf"{c_str} & {neg_s_str} & 0.00 \\ "
                    rf"{s_str} & {c_str} & 0.00 \\ "
                    rf"0.00 & 0.00 & 1.00"
                )

            tex_str = (
                rf"{name}(\theta)"
                rf" = "
                rf"\begin{{bmatrix}}"
                rf"{m_body}"
                rf"\end{{bmatrix}}"
            )

            res = MathTex(
                tex_str,
                font_size=28,
            )

            res.next_to(formula_tex, DOWN, buff=0.2)

            return res

        live_matrix = always_redraw(get_matrix_mobject)

        # =============================================================
        # 5. Custom Isometric 3D Projection
        # =============================================================

        center = np.array([0.0, -1.8, 0.0])

        r_scale = 1.35

        ux = r_scale * np.array([np.cos(7 * np.pi / 6), np.sin(7 * np.pi / 6), 0.0])

        uy = r_scale * np.array([np.cos(-np.pi / 6), np.sin(-np.pi / 6), 0.0])

        uz = r_scale * np.array([0.0, 1.0, 0.0])

        def proj(x, y, z):

            return center + x * ux + y * uy + z * uz

        # =============================================================
        # 6. XY Grid
        # =============================================================

        grid = VGroup()

        for i in np.linspace(-0.5, 2.0, 6):
            l_y = Line(
                proj(i, -0.5, 0),
                proj(i, 2.0, 0),
                color=GRAY,
                stroke_width=1.0,
                stroke_opacity=0.3,
            )

            l_x = Line(
                proj(-0.5, i, 0),
                proj(2.0, i, 0),
                color=GRAY,
                stroke_width=1.0,
                stroke_opacity=0.3,
            )

            grid.add(l_y, l_x)

        # =============================================================
        # 7. Coordinate Axes
        # =============================================================

        axis_x = Line(
            proj(-0.5, 0, 0),
            proj(2.2, 0, 0),
            color=RED,
            stroke_width=3.0,
        )

        axis_y = Line(
            proj(0, -0.5, 0),
            proj(0, 2.2, 0),
            color=GREEN,
            stroke_width=3.0,
        )

        axis_z = Line(
            proj(0, 0, -0.5),
            proj(0, 0, 2.2),
            color=BLUE,
            stroke_width=3.0,
        )

        x_label = MathTex(
            "X",
            color=RED,
            font_size=26,
        ).next_to(proj(2.2, 0, 0), DL, buff=0.1)

        y_label = MathTex(
            "Y",
            color=GREEN,
            font_size=26,
        ).next_to(proj(0, 2.2, 0), DR, buff=0.1)

        z_label = MathTex(
            "Z",
            color=BLUE,
            font_size=26,
        ).next_to(proj(0, 0, 2.2), UP, buff=0.12)

        axes_group = VGroup(
            grid,
            axis_x,
            axis_y,
            axis_z,
            x_label,
            y_label,
            z_label,
        )

        # =============================================================
        # 8. Cube
        # =============================================================

        raw_corners = [np.array([x, y, z]) for x in [0, 1] for y in [0, 1] for z in [0, 1]]

        faces_indices = [
            [0, 1, 3, 2],  # x = 0
            [4, 5, 7, 6],  # x = 1
            [0, 1, 5, 4],  # y = 0
            [2, 3, 7, 6],  # y = 1
            [0, 2, 6, 4],  # z = 0
            [1, 3, 7, 5],  # z = 1
        ]

        cube_faces = VGroup()

        for f_idx in faces_indices:
            pts = [proj(*raw_corners[i]) for i in f_idx]

            face = Polygon(
                *pts,
                fill_color=BLUE,
                fill_opacity=0.45,
                stroke_color=GREEN,
                stroke_width=2.2,
            )

            cube_faces.add(face)

        def update_cube(mob):

            th = theta_tracker.get_value()

            c = np.cos(th)
            s = np.sin(th)

            mode = int(round(axis_mode.get_value()))

            rot_corners = []

            for pt in raw_corners:
                px = pt[0]
                py = pt[1]
                pz = pt[2]

                if mode == 0:
                    # =================================================
                    # Rx
                    # =================================================

                    rx = px

                    ry = py * c - pz * s

                    rz = py * s + pz * c

                elif mode == 1:
                    # =================================================
                    # Ry
                    # =================================================

                    rx = px * c + pz * s

                    ry = py

                    rz = -px * s + pz * c

                else:
                    # =================================================
                    # Rz
                    # =================================================

                    rx = px * c - py * s

                    ry = px * s + py * c

                    rz = pz

                rot_corners.append(proj(rx, ry, rz))

            for face_poly, f_idx in zip(mob, faces_indices):
                pts = [rot_corners[i] for i in f_idx]

                face_poly.set_points_as_corners([*pts, pts[0]])

        cube_faces.add_updater(update_cube)

        # =============================================================
        # 9. GROWING CIRCULAR ROTATION ARC
        # =============================================================

        rotation_arc = VMobject()

        rotation_arrow = VGroup(
            rotation_arc,
        )

        # Size of the rotation circle
        rotation_radius = 1.45

        def update_rotation_arrow(mob):

            th = theta_tracker.get_value()

            mode = int(round(axis_mode.get_value()))

            # ---------------------------------------------------------
            # Nothing visible at theta = 0
            # ---------------------------------------------------------

            if th < 0.015:
                rotation_arc.clear_points()

                return

            # ---------------------------------------------------------
            # Limit to one full revolution
            # ---------------------------------------------------------

            th = min(th, 2 * np.pi)

            # ---------------------------------------------------------
            # Generate arc
            # ---------------------------------------------------------

            angles = np.linspace(0, th, 120)

            points = []

            for a in angles:
                if mode == 0:
                    # =================================================
                    # Rx
                    #
                    # Rotation axis: X
                    # Circle plane: YZ
                    #
                    # Positive Rx:
                    #
                    # y = cos(theta)
                    # z = sin(theta)
                    # =================================================

                    x = 0.0

                    y = rotation_radius * np.cos(a)

                    z = rotation_radius * np.sin(a)

                elif mode == 1:
                    # =================================================
                    # Ry
                    #
                    # Rotation axis: Y
                    # Circle plane: XZ
                    #
                    # IMPORTANT:
                    #
                    # The minus sign on z matches the exact Ry
                    # matrix used by the cube:
                    #
                    # x' = x cos(theta) + z sin(theta)
                    # z' = -x sin(theta) + z cos(theta)
                    #
                    # Therefore a point starting at:
                    #
                    # (r, 0, 0)
                    #
                    # moves toward:
                    #
                    # (0, 0, -r)
                    #
                    # when theta = pi/2.
                    # =================================================

                    x = rotation_radius * np.cos(a)

                    y = 0.0

                    z = -rotation_radius * np.sin(a)

                else:
                    # =================================================
                    # Rz
                    #
                    # Rotation axis: Z
                    # Circle plane: XY
                    #
                    # Positive Rz:
                    #
                    # x = cos(theta)
                    # y = sin(theta)
                    # =================================================

                    x = rotation_radius * np.cos(a)

                    y = rotation_radius * np.sin(a)

                    z = 0.0

                points.append(proj(x, y, z))

            # ---------------------------------------------------------
            # Draw the growing arc
            # ---------------------------------------------------------

            rotation_arc.set_points_smoothly(points)

        rotation_arc.set_stroke(
            color="#FFD166",
            width=5,
            opacity=0.95,
        )

        rotation_arrow.add_updater(update_rotation_arrow)

        # =============================================================
        # 10. UI Group
        # =============================================================

        all_ui = VGroup(
            title,
            slider_group,
            formula_tex,
            live_matrix,
            axes_group,
        )

        # =============================================================
        # 11. Intro
        # =============================================================

        self.play(FadeIn(all_ui, run_time=1.2))

        self.wait(0.2)

        # Put rotation arc behind cube
        self.add(rotation_arrow)

        self.play(FadeIn(cube_faces, run_time=1.0))

        self.wait(0.3)

        # =============================================================
        # 12. Phase 1 — Rx
        # =============================================================

        self.play(
            theta_tracker.animate.set_value(2 * np.pi),
            run_time=6.0,
            rate_func=linear,
        )

        self.wait(0.5)

        # =============================================================
        # 13. Transition — Rx -> Ry
        # =============================================================

        theta_tracker.set_value(0.0)

        axis_mode.set_value(1.0)

        self.wait(0.5)

        # =============================================================
        # 14. Phase 2 — Ry
        # =============================================================

        self.play(
            theta_tracker.animate.set_value(2 * np.pi),
            run_time=6.0,
            rate_func=linear,
        )

        self.wait(0.5)

        # =============================================================
        # 15. Transition — Ry -> Rz
        # =============================================================

        theta_tracker.set_value(0.0)

        axis_mode.set_value(2.0)

        self.wait(0.5)

        # =============================================================
        # 16. Phase 3 — Rz
        # =============================================================

        self.play(
            theta_tracker.animate.set_value(2 * np.pi),
            run_time=6.0,
            rate_func=linear,
        )

        self.wait(1.5)
