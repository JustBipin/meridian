import numpy as np
from manim import *

# ============================================================
# CONFIG
# ============================================================

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16


class LCRResonance(Scene):
    def construct(self):

        # ====================================================
        # COLORS
        # ====================================================

        BLUE = "#4D8DFF"
        RED = "#FF4D5A"
        PURPLE = "#A970FF"
        WHITE = "#F5F5F5"

        # ====================================================
        # PARAMETERS
        # ====================================================

        freq = ValueTracker(1.0)
        phase = ValueTracker(0)

        # ====================================================
        # CIRCUIT
        # ====================================================

        circuit_y = 2.8

        source_center = LEFT * 3.0 + UP * circuit_y

        # ----------------------------------------------------
        # AC SOURCE
        # ----------------------------------------------------

        source = Circle(
            radius=0.55,
            stroke_color=BLUE,
            stroke_width=4,
        ).move_to(source_center)

        sine = FunctionGraph(
            lambda x: 0.12 * np.sin(10 * x),
            x_range=[-0.35, 0.35],
            color=BLUE,
            stroke_width=2.5,
        ).move_to(source_center)

        # ----------------------------------------------------
        # WIRES
        # ----------------------------------------------------

        left_wire = Line(
            source_center + RIGHT * 0.55,
            RIGHT * 3.2 + UP * circuit_y,
            color=WHITE,
            stroke_width=3,
        )

        right_wire = Line(
            LEFT * 3.0 + DOWN * 0.55 + UP * circuit_y,
            LEFT * 3.0 + DOWN * 2.0,
            color=WHITE,
            stroke_width=3,
        )

        bottom_wire = Line(
            LEFT * 3.0 + DOWN * 2.0,
            RIGHT * 3.2 + DOWN * 2.0,
            color=WHITE,
            stroke_width=3,
        )

        right_vertical = Line(
            RIGHT * 3.2 + DOWN * 2.0,
            RIGHT * 3.2 + UP * circuit_y,
            color=WHITE,
            stroke_width=3,
        )

        # ====================================================
        # RESISTOR
        # ====================================================

        resistor = VGroup()

        points = [
            RIGHT * 0.0,
            RIGHT * 0.18 + UP * 0.18,
            RIGHT * 0.36 + DOWN * 0.18,
            RIGHT * 0.54 + UP * 0.18,
            RIGHT * 0.72 + DOWN * 0.18,
            RIGHT * 0.90 + UP * 0.18,
            RIGHT * 1.08,
        ]

        for a, b in zip(points[:-1], points[1:]):
            resistor.add(
                Line(
                    a,
                    b,
                    color=RED,
                    stroke_width=4,
                )
            )

        resistor.move_to(RIGHT * 0.1 + UP * circuit_y)

        # ====================================================
        # INDUCTOR
        # ====================================================

        coil = VGroup()

        for i in range(4):
            arc = Arc(
                radius=0.18,
                start_angle=0,
                angle=PI,
                color=BLUE,
                stroke_width=4,
            )

            arc.shift(RIGHT * i * 0.36)

            coil.add(arc)

        coil.move_to(RIGHT * 1.55 + UP * circuit_y)

        # ====================================================
        # CAPACITOR
        # ====================================================

        cap_left = Line(
            UP * 0.45,
            DOWN * 0.45,
            color=PURPLE,
            stroke_width=7,
        )

        cap_right = Line(
            UP * 0.45,
            DOWN * 0.45,
            color=PURPLE,
            stroke_width=7,
        )

        cap = VGroup(
            cap_left,
            cap_right,
        )

        cap.arrange(
            RIGHT,
            buff=0.22,
        )

        cap.move_to(RIGHT * 2.65 + UP * circuit_y)

        circuit = VGroup(
            source,
            sine,
            left_wire,
            right_wire,
            bottom_wire,
            right_vertical,
            resistor,
            coil,
            cap,
        )

        # ====================================================
        # CURRENT PARTICLES
        # ====================================================

        particle_group = VGroup()

        particle_xs = np.linspace(
            -2.3,
            2.8,
            13,
        )

        for x in particle_xs:
            dot = Dot(
                radius=0.045,
                color=BLUE,
            )

            dot.move_to(
                np.array([
                    x,
                    circuit_y,
                    0,
                ])
            )

            particle_group.add(dot)

        # ====================================================
        # OPENING
        # ====================================================

        self.play(
            Create(circuit),
            run_time=1.6,
            rate_func=smooth,
        )

        self.wait(0.25)

        # ====================================================
        # CURRENT PARTICLES
        # ====================================================

        def update_particles(mob):

            t = phase.get_value()

            for i, dot in enumerate(mob):
                x = particle_xs[i]

                displacement = 0.10 * np.sin(2 * PI * freq.get_value() * t + x * 1.2)

                dot.move_to(
                    np.array([
                        x + displacement,
                        circuit_y,
                        0,
                    ])
                )

        particle_group.add_updater(update_particles)

        self.add(particle_group)

        self.play(
            phase.animate.set_value(2),
            run_time=3,
            rate_func=linear,
        )

        # ====================================================
        # CAPACITOR CHARGING
        # ====================================================

        def update_capacitor(mob):

            q = np.sin(2 * PI * freq.get_value() * phase.get_value())

            gap = 0.22 + 0.18 * abs(q)

            mob[0].move_to(cap.get_center() + LEFT * gap / 2)

            mob[1].move_to(cap.get_center() + RIGHT * gap / 2)

        cap.add_updater(update_capacitor)

        self.play(
            phase.animate.set_value(5),
            run_time=3,
            rate_func=linear,
        )

        # ====================================================
        # TRANSITION TO PHASORS
        # ====================================================

        particle_group.clear_updaters()
        cap.clear_updaters()

        self.play(
            FadeOut(particle_group),
            FadeOut(circuit),
            run_time=0.7,
        )

        # ====================================================
        # PHASOR SPACE
        # ====================================================

        center = DOWN * 1.0

        axis = Line(
            LEFT * 3.2 + center,
            RIGHT * 3.2 + center,
            color=WHITE,
            stroke_width=2,
        ).set_stroke(opacity=0.35)

        self.play(
            Create(axis),
            run_time=0.5,
        )

        # ====================================================
        # ROTATING PHASORS
        # ====================================================

        theta = ValueTracker(0)

        # ----------------------------------------------------
        # Resistor voltage
        # ----------------------------------------------------

        resistor_vector = Arrow(
            center,
            center + RIGHT * 2.2,
            buff=0,
            color=RED,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.12,
        )

        # ----------------------------------------------------
        # Inductor phasor
        # Voltage leads current by 90 degrees
        # ----------------------------------------------------

        inductive_vector = always_redraw(
            lambda: Arrow(
                center,
                center
                + 1.5
                * np.array([
                    np.cos(theta.get_value() + PI / 2),
                    np.sin(theta.get_value() + PI / 2),
                    0,
                ]),
                buff=0,
                color=BLUE,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.12,
            )
        )

        # ----------------------------------------------------
        # Capacitor phasor
        # Voltage lags current by 90 degrees
        # ----------------------------------------------------

        capacitive_vector = always_redraw(
            lambda: Arrow(
                center,
                center
                + 1.5
                * np.array([
                    np.cos(theta.get_value() - PI / 2),
                    np.sin(theta.get_value() - PI / 2),
                    0,
                ]),
                buff=0,
                color=PURPLE,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.12,
            )
        )

        self.play(
            GrowArrow(resistor_vector),
            run_time=0.6,
        )

        self.play(
            Create(inductive_vector),
            Create(capacitive_vector),
            run_time=0.8,
        )

        # ====================================================
        # PHASOR ROTATION
        # ====================================================

        self.play(
            theta.animate.set_value(2 * PI),
            run_time=3,
            rate_func=linear,
        )

        # ====================================================
        # RESONANCE
        # ====================================================

        # Freeze the rotating phase at the point
        # where L and C are opposite.

        self.play(
            theta.animate.set_value(0),
            run_time=0.8,
            rate_func=smooth,
        )

        self.wait(0.3)

        # ====================================================
        # RESONANCE RING
        # ====================================================

        resonance_ring = Circle(
            radius=0.8,
            stroke_color=BLUE,
            stroke_width=3,
            fill_opacity=0,
        ).move_to(center)

        self.play(
            Create(resonance_ring),
            run_time=0.5,
        )

        self.play(
            resonance_ring.animate.scale(2.5).set_stroke(opacity=0),
            run_time=1.0,
            rate_func=smooth,
        )

        self.wait(0.8)
