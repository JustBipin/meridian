from manim import *

# ------------------------------------------------------------
# Vertical format
# ------------------------------------------------------------

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

# ------------------------------------------------------------
# Palette
# ------------------------------------------------------------


class NewtonRaphsonBeautiful(Scene):
    def construct(self):

        # ----------------------------------------------------
        # 1. Coordinate system
        # ----------------------------------------------------

        axes = Axes(
            x_range=[-2.2, 2.4, 1],
            y_range=[-4.5, 5.0, 1],
            x_length=8.2,
            y_length=9.0,
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 1.5,
                "stroke_opacity": 0.35,
            },
            tips=False,
        )

        axes.move_to(DOWN * 0.45)

        # f(x) = x^3 - x - 1
        def f(x):
            return x**3 - x - 1

        def fp(x):
            return 3 * x**2 - 1

        curve = axes.plot(
            f,
            x_range=[-1.7, 1.95],
            color=BLUE,
            stroke_width=5,
        )

        # ----------------------------------------------------
        # Root and Newton iterations
        # ----------------------------------------------------

        # x_{n+1} = x_n - f(x_n)/f'(x_n)
        xs = [1.55]

        for _ in range(6):
            x = xs[-1]
            xs.append(x - f(x) / fp(x))

        root = xs[-1]

        # ----------------------------------------------------
        # 2. Opening
        # ----------------------------------------------------

        self.play(
            Create(axes),
            run_time=1.2,
        )

        self.play(
            Create(curve),
            run_time=1.8,
            rate_func=smooth,
        )

        self.wait(0.4)

        # ----------------------------------------------------
        # 3. Root glow
        # ----------------------------------------------------

        root_point = Dot(
            axes.c2p(root, 0),
            radius=0.075,
            color=RED,
        )

        root_glow = Circle(
            radius=0.18,
            stroke_width=2,
            stroke_color=RED,
            fill_opacity=0,
        ).move_to(root_point)

        self.play(
            FadeIn(root_point, scale=0.3),
            Create(root_glow),
            run_time=0.5,
        )

        self.play(
            root_glow.animate.scale(1.7).set_opacity(0),
            run_time=0.8,
        )

        # ----------------------------------------------------
        # 4. First guess
        # ----------------------------------------------------

        x0 = xs[0]

        guess = Dot(
            axes.c2p(x0, 0),
            radius=0.09,
            color=RED,
        )

        vertical = DashedLine(
            axes.c2p(x0, 0),
            axes.c2p(x0, f(x0)),
            color=RED,
            stroke_width=2,
            dash_length=0.08,
        ).set_opacity(0.65)

        point_on_curve = Dot(
            axes.c2p(x0, f(x0)),
            radius=0.075,
            color=RED,
        )

        self.play(
            FadeIn(guess, scale=0.3),
            run_time=0.35,
        )

        self.play(
            Create(vertical),
            FadeIn(point_on_curve, scale=0.4),
            run_time=0.5,
        )

        # ----------------------------------------------------
        # 5. Helper for tangent
        # ----------------------------------------------------

        def tangent_line(x, color=RED, opacity=1.0):

            y = f(x)
            slope = fp(x)

            # x intercept of tangent
            x_intercept = x - y / slope

            # Give the tangent plenty of length.
            left = min(x_intercept - 0.7, x - 1.0)
            right = max(x + 1.0, x_intercept + 0.7)

            def tangent_fn(t):
                return y + slope * (t - x)

            line = axes.plot(
                tangent_fn,
                x_range=[left, right],
                color=color,
                stroke_width=3.5,
            )

            line.set_opacity(opacity)

            return line, x_intercept

        # ----------------------------------------------------
        # 6. First tangent
        # ----------------------------------------------------

        tangent, next_x = tangent_line(x0)

        next_dot = Dot(
            axes.c2p(next_x, 0),
            radius=0.075,
            color=RED,
        )

        jump = Line(
            axes.c2p(x0, 0),
            axes.c2p(next_x, 0),
            color=RED,
            stroke_width=2.5,
        )

        self.play(
            Create(tangent),
            run_time=0.9,
            rate_func=smooth,
        )

        self.play(
            FadeIn(next_dot, scale=0.3),
            Create(jump),
            run_time=0.55,
        )

        self.play(
            FadeOut(vertical),
            FadeOut(point_on_curve),
            FadeOut(guess),
            FadeOut(jump),
            run_time=0.35,
        )

        # ----------------------------------------------------
        # 7. Newton iterations
        # ----------------------------------------------------

        previous_dot = next_dot

        # Tangents become progressively thinner/fainter.
        trail_tangents = []

        for i in range(1, len(xs) - 1):
            x_current = xs[i]

            # Point on curve
            curve_point = Dot(
                axes.c2p(x_current, f(x_current)),
                radius=0.06,
                color=RED,
            )

            # Vertical connection
            vertical = DashedLine(
                axes.c2p(x_current, 0),
                axes.c2p(x_current, f(x_current)),
                color=RED,
                stroke_width=1.7,
                dash_length=0.06,
            ).set_opacity(0.5)

            tangent, x_next = tangent_line(
                x_current,
                color=RED,
                opacity=1.0,
            )

            next_dot = Dot(
                axes.c2p(x_next, 0),
                radius=max(0.045, 0.075 - i * 0.005),
                color=RED,
            )

            # Horizontal Newton jump
            jump = Line(
                axes.c2p(x_current, 0),
                axes.c2p(x_next, 0),
                color=RED,
                stroke_width=2,
            )

            # ------------------------------------------------
            # Increasing speed
            # ------------------------------------------------

            if i == 1:
                tangent_time = 0.65
                jump_time = 0.40
            elif i == 2:
                tangent_time = 0.50
                jump_time = 0.32
            elif i == 3:
                tangent_time = 0.38
                jump_time = 0.25
            else:
                tangent_time = 0.28
                jump_time = 0.18

            # Move old tangent into the background.
            if trail_tangents:
                self.play(
                    trail_tangents[-1].animate.set_stroke(opacity=0.18),
                    run_time=0.15,
                )

            self.play(
                Create(vertical),
                FadeIn(curve_point, scale=0.4),
                run_time=0.18,
            )

            self.play(
                Create(tangent),
                run_time=tangent_time,
                rate_func=smooth,
            )

            self.play(
                FadeIn(next_dot, scale=0.35),
                Create(jump),
                run_time=jump_time,
            )

            # Keep tangent as part of the visual trail.
            trail_tangents.append(tangent)

            self.play(
                FadeOut(vertical),
                FadeOut(curve_point),
                FadeOut(previous_dot),
                FadeOut(jump),
                run_time=0.18,
            )

            previous_dot = next_dot

        # ----------------------------------------------------
        # 8. Convergence moment
        # ----------------------------------------------------

        final_dot = Dot(
            axes.c2p(root, 0),
            radius=0.10,
            color=RED,
        )

        glow = VGroup()

        for radius, opacity in [
            (0.16, 0.30),
            (0.28, 0.18),
            (0.42, 0.08),
        ]:
            glow.add(
                Circle(
                    radius=radius,
                    stroke_color=RED,
                    stroke_width=2,
                    stroke_opacity=opacity,
                    fill_opacity=0,
                ).move_to(final_dot)
            )

        self.play(
            FadeIn(final_dot, scale=0.4),
            FadeIn(glow),
            run_time=0.4,
        )

        # ----------------------------------------------------
        # 9. Beautiful pulse
        # ----------------------------------------------------

        self.play(
            glow.animate.scale(1.5),
            run_time=0.7,
            rate_func=smooth,
        )

        self.play(
            glow.animate.scale(0.72),
            run_time=0.55,
            rate_func=smooth,
        )

        self.wait(0.6)

        # ----------------------------------------------------
        # 10. Let the entire construction breathe
        # ----------------------------------------------------

        self.play(
            *[mob.animate.set_stroke(opacity=mob.get_stroke_opacity() * 0.35) for mob in trail_tangents],
            curve.animate.set_stroke(opacity=0.45),
            axes.animate.set_stroke(opacity=0.20),
            run_time=1.0,
        )

        self.wait(1.0)

        # ----------------------------------------------------
        # 11. Final root pulse
        # ----------------------------------------------------

        final_ring = Circle(
            radius=0.20,
            stroke_color=RED,
            stroke_width=3,
            fill_opacity=0,
        ).move_to(final_dot)

        self.play(
            Create(final_ring),
            run_time=0.3,
        )

        self.play(
            final_ring.animate.scale(2.2).set_opacity(0),
            final_dot.animate.scale(1.25),
            run_time=0.9,
            rate_func=smooth,
        )

        self.wait(0.8)
