import manim as m
import numpy as np

# ============================================================
# Portrait / Vertical 9:16 configuration
# ============================================================

PIXEL_WIDTH = 1080
PIXEL_HEIGHT = 1920
FRAME_RATE = 60

FRAME_SHORT_SIDE = 8.0

FRAME_HEIGHT = FRAME_SHORT_SIDE * max(1.0, PIXEL_HEIGHT / PIXEL_WIDTH)


# ============================================================
# Design Tokens & Palette
# ============================================================

BRIGHT_COLORS = [
    "#53A5D8",  # Muted Blue (1/2)
    "#EE829A",  # Soft Rose / Pink (1/4)
    "#F4B266",  # Soft Orange / Amber (1/8)
    "#BDB2FF",  # Muted Lavender (1/16)
    "#C0E8D5",  # Muted Mint (1/32)
    "#90E0EF",  # Soft Ice Blue (1/64)
    "#E8AEB7",  # Soft Dusty Pink (1/128)
    "#A0C4FF",  # Soft Sky Blue (1/256)
    "#52B788",  # Muted Green
    "#7400B8",  # Deep Muted Purple
]

TEXT_COLOR = "#FFFFFF"
FRAME_COLOR = "#FFFFFF"


class GeometricSeriesCute(m.Scene):
    # ========================================================
    # Camera setup
    # ========================================================

    def setup(self):

        self.camera.pixel_width = PIXEL_WIDTH
        self.camera.pixel_height = PIXEL_HEIGHT
        self.camera.frame_rate = FRAME_RATE
        self.camera.frame_height = FRAME_HEIGHT

    # ========================================================
    # Main scene
    # ========================================================

    def construct(self):

        # m.apply_theme(self, "Dracula")

        SCALE = 6.0

        # ====================================================
        # Position the unit square
        # ====================================================

        ORIGIN_X = -SCALE / 2
        ORIGIN_Y = -SCALE / 2 + 1.2

        def P(x, y):

            return np.array([ORIGIN_X + SCALE * x, ORIGIN_Y + SCALE * y, 0])

        # ====================================================
        # Generate recursive rectangle geometry
        # ====================================================

        rectangles = []

        x, y = 0.0, 0.0
        width, height = 0.5, 1.0

        rectangles.append({"x": x, "y": y, "w": width, "h": height, "power": 1})

        for power in range(2, 17):
            if power % 2 == 0:
                x = x + width
                height = height / 2.0

            else:
                y = y + height
                width = width / 2.0

            rectangles.append({"x": x, "y": y, "w": width, "h": height, "power": power})

        # ====================================================
        # Directions for entrance animation
        # ====================================================

        directions = []

        for i, data in enumerate(rectangles):
            if i == 0:
                directions.append(None)

            elif data["power"] % 2 == 0:
                directions.append(m.LEFT)

            else:
                directions.append(m.DOWN)

        # ====================================================
        # Create rectangles and labels
        # ====================================================

        rects = []
        labels = []

        RECT_GAP = 0.030

        for i, data in enumerate(rectangles):
            w_val = data["w"] * SCALE
            h_val = data["h"] * SCALE

            center = P(data["x"] + data["w"] / 2.0, data["y"] + data["h"] / 2.0)

            # ------------------------------------------------
            # Visual padding
            # ------------------------------------------------

            padding_x = min(RECT_GAP, max(0.005, w_val / 2.0 - 0.01))

            padding_y = min(RECT_GAP, max(0.005, h_val / 2.0 - 0.01))

            visual_width = max(0.02, w_val - 2 * padding_x)

            visual_height = max(0.02, h_val - 2 * padding_y)

            # ------------------------------------------------
            # Colors
            # ------------------------------------------------

            fill_c = BRIGHT_COLORS[i % len(BRIGHT_COLORS)]

            stroke_c = m.interpolate_color(m.ManimColor(fill_c), m.ManimColor("#FFFFFF"), 0.25)

            # ------------------------------------------------
            # Rectangle
            # ------------------------------------------------

            rect = m.RoundedRectangle(
                width=visual_width,
                height=visual_height,
                corner_radius=min(0.045, visual_width / 8, visual_height / 8),
                stroke_width=(1.8 if data["power"] <= 8 else 0.7),
                stroke_color=stroke_c,
                fill_color=fill_c,
                fill_opacity=0.95,
            )

            rect.move_to(center)

            # ------------------------------------------------
            # Fraction label
            # ------------------------------------------------

            power = data["power"]

            if power <= 3:
                label_scale = 0.72

            elif power <= 5:
                label_scale = 0.50

            elif power <= 7:
                label_scale = 0.36

            elif power <= 8:
                label_scale = 0.22

            else:
                label_scale = 0.0

            if label_scale > 0:
                label = m.MathTex(rf"\mathbf{{\frac{{1}}{{{2**power}}}}}", color="#111111").scale(label_scale)

                label.move_to(center)

            else:
                label = m.VMobject()

            rects.append(rect)
            labels.append(label)

        # ====================================================
        # Equation configuration
        # ====================================================

        sum_container = m.VGroup()

        TERM_BUFF = 0.08

        SUM_Y = -3.5

        # ====================================================
        # Animate rectangles + equation
        # ====================================================

        for i in range(len(rects)):
            rect = rects[i]

            label = labels[i]

            power = rectangles[i]["power"]

            # =================================================
            # Determine equation terms
            # =================================================

            if power <= 8:
                if i == 0:
                    term_strings = [rf"\frac{{1}}{{{2**power}}}"]

                else:
                    term_strings = [rf"+\frac{{1}}{{{2**power}}}"]

            elif power == 9:
                term_strings = [r"+\cdots+", r"\frac{1}{2^{n-1}}"]

            elif power == 10:
                term_strings = [r"+", r"\frac{1}{2^n}"]

            else:
                term_strings = []

            # =================================================
            # Create new equation terms
            # =================================================

            new_terms = []

            for term_string in term_strings:
                t_color = TEXT_COLOR

                if "2^{n-1}" in term_string:
                    t_color = "#FFD166"

                elif "2^n" in term_string:
                    t_color = "#FF85A1"

                term = m.MathTex(term_string, color=t_color).scale(0.70)

                new_terms.append(term)

            # =================================================
            # CRITICAL PART
            #
            # Make COPIES of existing terms.
            #
            # Never arrange the real sum_container terms.
            # =================================================

            old_terms = list(sum_container)

            old_count = len(old_terms)

            target_old_terms = [term.copy() for term in old_terms]

            # =================================================
            # Build temporary target group
            #
            # These are ONLY copies.
            # Therefore this cannot cause a jump.
            # =================================================

            target_group = m.VGroup(*target_old_terms, *new_terms)

            target_group.arrange(m.RIGHT, buff=TERM_BUFF)

            target_group.move_to(np.array([0, SUM_Y, 0]))

            # =================================================
            # Calculate target positions for existing terms
            # =================================================

            old_targets = []

            for idx in range(old_count):
                old_targets.append(target_group[idx].get_center())

            # =================================================
            # Calculate target positions for new terms
            # =================================================

            new_targets = []

            for idx in range(len(new_terms)):
                new_targets.append(target_group[old_count + idx].get_center())

            # =================================================
            # Move new terms to their final locations BEFORE
            # Write().
            #
            # They are invisible/not yet added, so this does
            # NOT cause a visible jump.
            # =================================================

            for idx, term in enumerate(new_terms):
                term.move_to(new_targets[idx])

            # =================================================
            # Rectangle entrance
            # =================================================

            if i == 0:
                rect.set_opacity(0)

                label.set_opacity(0)

                self.add(rect, label)

                rectangle_animations = [
                    rect.animate.set_opacity(0.95),
                    label.animate.set_opacity(1),
                ]

            else:
                direction = directions[i]

                slide_distance = 0.25

                rect.shift(direction * slide_distance)

                label.shift(direction * slide_distance)

                rect.set_opacity(0)

                label.set_opacity(0)

                self.add(rect, label)

                rectangle_animations = [
                    rect.animate.shift(-direction * slide_distance).set_opacity(0.95),
                    label.animate.shift(-direction * slide_distance).set_opacity(1),
                ]

            # =================================================
            # Equation animations
            # =================================================

            equation_animations = []

            # -------------------------------------------------
            # Move EVERY existing term individually.
            #
            # This is the important difference.
            #
            # We do NOT do:
            #
            # sum_container.animate.move_to(...)
            #
            # because the equation may change its width.
            # -------------------------------------------------

            for idx, term in enumerate(old_terms):
                equation_animations.append(term.animate.move_to(old_targets[idx]))

            # =================================================
            # Write new terms
            # =================================================

            for term in new_terms:
                equation_animations.append(m.Write(term))

            # =================================================
            # SINGLE SIMULTANEOUS PLAY
            #
            # Rectangle
            #       +
            # Label
            #       +
            # Existing equation movement
            #       +
            # New equation term
            #
            # ALL happen at exactly the same time.
            # =================================================

            self.play(
                *rectangle_animations,
                *equation_animations,
                run_time=0.75,
                rate_func=m.smooth,
            )

            # =================================================
            # Commit new terms
            # =================================================

            for term in new_terms:
                sum_container.add(term)

            # Very small pause between steps
            self.wait(0.02)

        # ====================================================
        # Finish equation
        # ====================================================

        self.wait(0.2)

        # ====================================================
        # OUTER UNIT-SQUARE FRAME
        # ====================================================

        outer_square = m.Square(
            side_length=(SCALE + RECT_GAP * 3),
            stroke_width=6.0,
            stroke_color=FRAME_COLOR,
            fill_opacity=0,
        )

        outer_square.move_to(P(0.5, 0.5))

        self.play(m.Create(outer_square), run_time=0.7, rate_func=m.smooth)

        self.wait(0.15)

        # ====================================================
        # DIMENSION ARROWS
        # ====================================================

        BASE_GAP = 0.4

        base_y = outer_square.get_bottom()[1] - BASE_GAP

        base_arrow = m.DoubleArrow(
            np.array([outer_square.get_left()[0], base_y, 0]),
            np.array([outer_square.get_right()[0], base_y, 0]),
            buff=0,
            stroke_width=2.8,
            tip_length=0.13,
            color=FRAME_COLOR,
        )

        base_label = m.MathTex(r"\mathbf{1}", color=TEXT_COLOR).scale(0.55)

        base_label.next_to(base_arrow, m.DOWN, buff=0.08)

        # ----------------------------------------------------
        # HEIGHT = 1
        # ----------------------------------------------------

        HEIGHT_GAP = 0.4

        height_x = outer_square.get_left()[0] - HEIGHT_GAP

        height_arrow = m.DoubleArrow(
            np.array([height_x, outer_square.get_bottom()[1], 0]),
            np.array([height_x, outer_square.get_top()[1], 0]),
            buff=0,
            stroke_width=2.8,
            tip_length=0.13,
            color=FRAME_COLOR,
        )

        height_label = m.MathTex(r"\mathbf{1}", color=TEXT_COLOR).scale(0.55)

        height_label.next_to(height_arrow, m.LEFT, buff=0.10)

        # ====================================================
        # Draw dimensions
        # ====================================================

        self.play(
            m.Create(base_arrow),
            m.Create(height_arrow),
            m.FadeIn(base_label),
            m.FadeIn(height_label),
            run_time=0.5,
            rate_func=m.smooth,
        )

        self.wait(0.2)

        # ====================================================
        # "= 1"
        # ====================================================

        equals_one = m.MathTex(r"= 1", color=TEXT_COLOR).scale(1.10)

        equals_one.next_to(sum_container, m.DOWN, buff=0.35)

        equals_one.move_to(np.array([sum_container.get_center()[0], equals_one.get_center()[1], 0]))

        self.play(
            m.FadeIn(equals_one, scale=0.8),
            run_time=0.4,
        )

        # ====================================================
        # Final emphasis
        # ====================================================

        self.play(
            equals_one.animate.scale(1.12),
            run_time=0.10,
            rate_func=m.smooth,
        )

        self.play(
            equals_one.animate.scale(1 / 1.12),
            run_time=0.10,
            rate_func=m.smooth,
        )

        self.wait(0.6)

        self.play(
            equals_one.animate.scale(1.12),
            run_time=0.10,
            rate_func=m.smooth,
        )

        self.play(
            equals_one.animate.scale(1 / 1.12),
            run_time=0.10,
            rate_func=m.smooth,
        )

        self.wait(0.8)
