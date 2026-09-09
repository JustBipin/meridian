from manim import *
from manim_themes.manim_theme import apply_theme


class GeometricSeriesCute(Scene):
    def construct(self):

        # ============================================================
        # LONDON THEME
        # ============================================================

        apply_theme(self, "london")

        # ============================================================
        # SETTINGS
        # ============================================================

        SCALE = 5.5
        ORIGIN_X = -SCALE / 2
        ORIGIN_Y = -SCALE / 2

        def P(x, y):
            return np.array([ORIGIN_X + SCALE * x, ORIGIN_Y + SCALE * y, 0])

        # ============================================================
        # COLORS
        # ============================================================

        bright_colors = [
            "#A8DADC",
            "#FF9AA2",
            "#CDB4DB",
            "#FFD6A5",
            "#BDE0FE",
            "#FFC8DD",
            "#95D5B2",
            "#A2D2FF",
            "#F28482",
            "#B8A0D9",
            "#72D6C9",
            "#FFB4A2",
            "#89B4E8",
            "#E8A0BF",
            "#A8CFA8",
            "#F6BD60",
            "#9AD1D4",
            "#D5A6E6",
            "#FF8FA3",
            "#8EC5E8",
            "#B5E2A8",
            "#F4A6A6",
            "#A9B5E8",
            "#F7C59F",
        ]

        text_color = "#202124"
        frame_color = "#202124"

        # ============================================================
        # SOUND EFFECT
        # ============================================================

        POP_SOUND = "pop.mp3"

        # ============================================================
        # BUILD RECTANGLE GEOMETRY
        # ============================================================

        rectangles = []

        x = 0
        y = 0
        width = 0.5
        height = 1.0

        rectangles.append({
            "x": x,
            "y": y,
            "w": width,
            "h": height,
            "power": 1,
        })

        # ============================================================
        # REMAINING RECTANGLES
        # ============================================================

        for power in range(2, 16):
            if power % 2 == 0:
                # EVEN:
                # Move right and halve height.

                x = x + width
                height = height / 2

            else:
                # ODD:
                # Move up and halve width.

                y = y + height
                width = width / 2

            rectangles.append({
                "x": x,
                "y": y,
                "w": width,
                "h": height,
                "power": power,
            })

        # ============================================================
        # SLIDE DIRECTIONS
        # ============================================================

        directions = []

        for i, data in enumerate(rectangles):
            if i == 0:
                directions.append(None)

            elif data["power"] % 2 == 0:
                directions.append(LEFT)

            else:
                directions.append(DOWN)

        # ============================================================
        # CREATE RECTANGLES + LABELS
        # ============================================================

        rects = []
        labels = []

        for i, data in enumerate(rectangles):
            width = data["w"] * SCALE
            height = data["h"] * SCALE

            center = P(
                data["x"] + data["w"] / 2,
                data["y"] + data["h"] / 2,
            )

            # --------------------------------------------------------
            # RECTANGLE
            # --------------------------------------------------------

            rect = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=min(
                    0.08,
                    width / 8,
                    height / 8,
                ),
                stroke_width=0,
                fill_color=bright_colors[i],
                fill_opacity=0.92,
            )

            rect.move_to(center)

            # --------------------------------------------------------
            # LABEL SIZE
            # --------------------------------------------------------

            power = data["power"]

            if power <= 3:
                label_scale = 0.60

            elif power <= 5:
                label_scale = 0.42

            elif power <= 7:
                label_scale = 0.30

            elif power <= 9:
                label_scale = 0.23

            elif power <= 11:
                label_scale = 0.18

            elif power <= 13:
                label_scale = 0.14

            else:
                label_scale = 0.11

            # --------------------------------------------------------
            # FORMULA
            # --------------------------------------------------------

            label = MathTex(
                rf"\frac{{1}}{{{2**power}}}",
                color=text_color,
            ).scale(label_scale)

            label.move_to(center)

            rects.append(rect)
            labels.append(label)

        # ============================================================
        # ANIMATE RECTANGLES
        # ============================================================

        for i in range(len(rects)):
            rect = rects[i]
            label = labels[i]

            # ========================================================
            # FIRST RECTANGLE
            # ========================================================

            if i == 0:
                rect.set_opacity(0)

                self.play(
                    rect.animate.set_opacity(0.92),
                    run_time=0.65,
                    rate_func=smooth,
                )

                # Pop exactly when the first rectangle appears.
                self.add_sound(POP_SOUND)

                self.play(
                    FadeIn(
                        label,
                        scale=0.90,
                    ),
                    run_time=0.30,
                )

            # ========================================================
            # REMAINING RECTANGLES
            # ========================================================

            else:
                direction = directions[i]

                slide_distance = 0.40

                # Start displaced in exactly ONE direction.

                rect.shift(direction * slide_distance)
                label.shift(direction * slide_distance)

                rect.set_opacity(0)
                label.set_opacity(0)

                self.add(
                    rect,
                    label,
                )

                # ----------------------------------------------------
                # SLIDE + FADE
                # ----------------------------------------------------

                self.play(
                    rect.animate.shift(-direction * slide_distance).set_opacity(0.92),
                    label.animate.shift(-direction * slide_distance).set_opacity(1),
                    run_time=max(
                        0.28,
                        0.62 - i * 0.018,
                    ),
                    rate_func=smooth,
                )

                # Pop exactly when the rectangle reaches its position.
                self.add_sound(POP_SOUND)

                # ----------------------------------------------------
                # CUTE LABEL POP
                #
                # Only while labels are still large enough to read.
                # ----------------------------------------------------

                if data["power"] <= 8:
                    self.play(
                        label.animate.scale(1.05),
                        run_time=0.10,
                        rate_func=smooth,
                    )

                    self.play(
                        label.animate.scale(1 / 1.05),
                        run_time=0.10,
                        rate_func=smooth,
                    )

            self.wait(0.07)

        # ============================================================
        # PAUSE
        # ============================================================

        self.wait(0.65)

        # ============================================================
        # OUTER UNIT SQUARE
        # ============================================================

        outer = Square(
            side_length=SCALE,
            stroke_width=3,
            stroke_color=frame_color,
            fill_opacity=0,
        )

        self.play(
            Create(outer),
            run_time=0.9,
            rate_func=smooth,
        )

        self.wait(0.6)

        # ============================================================
        # SUM
        # ============================================================

        sum_text = MathTex(
            r"""
            \frac12+
            \frac14+
            \frac18+
            \frac1{16}+
            \frac1{32}+
            \frac1{64}+
            \cdots+
            \frac{1}{2^n-1}
            +
            \frac{1}{2^n}
            """,
            color=text_color,
        ).scale(0.68)

        sum_text.to_edge(
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(sum_text),
            run_time=1.15,
        )

        self.wait(0.55)

        # ============================================================
        # FINAL VALUE
        # ============================================================

        equals_one = MathTex(
            r"= 1",
            color=text_color,
        ).scale(1.05)

        equals_one.next_to(
            sum_text,
            RIGHT,
            buff=0.18,
        )

        self.play(
            FadeIn(
                equals_one,
                scale=0.80,
            ),
            run_time=0.45,
        )

        # ============================================================
        # CUTE FINAL EMPHASIS
        # ============================================================

        self.play(
            equals_one.animate.scale(1.08),
            run_time=0.16,
            rate_func=smooth,
        )

        self.play(
            equals_one.animate.scale(1 / 1.08),
            run_time=0.16,
            rate_func=smooth,
        )

        self.wait(2)
