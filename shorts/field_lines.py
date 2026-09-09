"""Electric field lines of two charges — a vertical 9:16 voiceover short.

Story: a lone positive charge shows dense radial field lines; a negative
charge far beyond the frame slowly approaches, bending the field lines until
every one of them sweeps from "+" and terminates on "-"; finally a positive
test charge placed on a field line feels a force F = qE and accelerates along
the curve toward the negative charge.

The field lines are the integral curves of the dipole electric field, traced
numerically and resampled to a fixed anchor count, so ``Transform`` morphs
them smoothly while the negative charge moves.  Directional arrowheads are
re-created every frame from each line's *current* anchors via ``always_redraw``
so they stay glued to the line and rotate with the local tangent.

See docs/SHORTS_TEMPLATE.md for the template conventions used here.
"""

import numpy as np
from manim import *

from shorts.shorts_template import ShortScene, apply_vertical_config

apply_vertical_config()

# ---------------------------------------------------------------------------
# Physics / layout constants
# ---------------------------------------------------------------------------

CHARGE_R = 0.38  # radius of the drawn charge circles
START_R = 0.48  # where field lines begin (just outside the + charge)
N_ANCHORS = 90  # anchor points per field line (identical across all states)
STEP = 0.02  # field-line integration step (units of arc length)
MAX_LEN = 130.0  # integration budget before giving up on a line
ESCAPE_R = 65.0  # stop once a line is this far from + (it has left the frame)
CAPTURE_R = CHARGE_R  # a line is considered to have "reached" the - charge
FRAME_HW = 4.5  # frame half-width (for arrow placement on the visible part)
FRAME_HH = 8.0  # frame half-height (for arrow placement on the visible part)

# Field lines leave the + charge at these angles (degrees from the +x axis,
# which points at the - charge); mirrored to +/- this is a dense 17-line fan
# covering every direction around the + charge (verified numerically by
# trace_field_line).  EVERY line terminates on the - charge in the final
# dipole: the near lines connect directly, the +-100..+-120 lines loop inside
# the frame, and the far-backward lines (+-140, +-160) swing in big loops far
# beyond the frame and re-enter it to terminate on the - charge from above.
# The exactly-backward direction is excluded because such a line can never
# return to the - charge (it is the degenerate axis line that goes to
# infinity).
START_ANGLES = (0, 20, 40, 60, 80, 100, 120, 140, 160)  # mirrored to +/-

# The curved line a positive test charge rides in the final act (80 deg
# swings over the top of the dipole, so the force vector rotates a lot as
# the particle accelerates along it).
TEST_LINE_ANGLE = 80

# Arrowheads embedded in each field line at these fractions of the line's
# length; a shared phase ValueTracker drifts them outward along the line to
# communicate the field direction ("+" toward "-").
ARROW_FRACS = (0.42, 0.72)
ARROW_SIZE = 0.07
FLOW_SPEED = 0.05  # line-length fractions travelled per unit of phase


# ---------------------------------------------------------------------------
# Physics helpers (pure numpy, no Manim needed)
# ---------------------------------------------------------------------------


def _e_field(r, p_plus, p_minus):
    """Electric field at ``r`` — only the direction matters for field lines.

    Charges are equal and opposite; the minus sign of the second term is the
    negative charge itself.
    """
    d_plus = r - p_plus
    d_minus = r - p_minus
    return d_plus / np.linalg.norm(d_plus) ** 3 - d_minus / np.linalg.norm(d_minus) ** 3


def trace_field_line(p_plus, p_minus, angle_deg):
    """Trace one electric field line leaving +q at ``angle_deg`` from +x.

    Integrates the (normalised) electric field until the line reaches the
    - charge, leaves the visible scene, or runs out of budget.  Returns the
    raw polyline; see ``resample`` for turning it into a smooth curve.
    """
    theta = np.deg2rad(angle_deg)
    pos = p_plus + START_R * np.array([np.cos(theta), np.sin(theta), 0.0])
    pts = [pos.copy()]
    for _ in range(int(MAX_LEN / STEP)):
        e = _e_field(pos, p_plus, p_minus)
        norm = np.linalg.norm(e)
        if norm < 1e-9:
            break
        pos = pos + STEP * e / norm
        pts.append(pos.copy())
        if np.linalg.norm(pos - p_minus) < CAPTURE_R:  # reached the - charge
            break
        if np.linalg.norm(pos - p_plus) > ESCAPE_R:  # left the frame
            break
    return np.array(pts)


def resample(points, n=N_ANCHORS):
    """Resample a traced polyline to ``n`` anchors, bunched near the start.

    Anchor ``k`` sits at arc length ``total * (k/n)**1.5``, so the visible
    part of a line (near the charges) gets most of the resolution.  Every
    field-line state uses the same anchor count and spacing law, which is
    what lets ``Transform`` morph a line smoothly as the negative charge
    moves instead of jumping between differently-shaped curves.
    """
    pts = np.asarray(points, dtype=float)
    if len(pts) < 2:
        return np.tile(pts[0], (n, 1))
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    total = cum[-1]
    if total < 1e-9:
        return np.tile(pts[0], (n, 1))
    # Power-law arc-length spacing: anchors bunch up near the start of the
    # line (the part visible in the frame), so the far off-frame loops of the
    # backward lines do not starve the visible parts of resolution.
    s = total * (np.linspace(0.0, 1.0, n) ** 1.5)
    idx = np.clip(np.searchsorted(cum, s, side="right") - 1, 0, len(pts) - 2)
    t = (s - cum[idx]) / np.maximum(seg[idx], 1e-12)
    return pts[idx] + t[:, None] * (pts[idx + 1] - pts[idx])


def ray_to_frame(origin, angle_deg, half_w=4.5, half_h=8.0):
    """Where the ray from ``origin`` at ``angle_deg`` exits the 9:16 frame.

    Used for the initial "lone positive charge" state, where the field lines
    are straight radial rays reaching the edge of the scene.
    """
    theta = np.deg2rad(angle_deg)
    dx, dy = np.cos(theta), np.sin(theta)
    ts = []
    if abs(dx) > 1e-9:
        ts.append((half_w - origin[0]) / dx if dx > 0 else (-half_w - origin[0]) / dx)
    if abs(dy) > 1e-9:
        ts.append((half_h - origin[1]) / dy if dy > 0 else (-half_h - origin[1]) / dy)
    t = min(t for t in ts if t > 1e-9)
    return origin + t * np.array([dx, dy, 0.0])


# ---------------------------------------------------------------------------
# Manim geometry helpers
# ---------------------------------------------------------------------------


def curve_from_points(points, color=BLUE, stroke_width=3):
    """A smooth Manim curve through ``points`` (used for each field line)."""
    curve = VMobject(stroke_color=color, stroke_width=stroke_width)
    curve.set_points_smoothly(points)
    return curve


def curve_length(curve):
    """Total arc length of ``curve`` computed from its current anchors."""
    pts = np.asarray(curve.get_anchors(), dtype=float)
    return float(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum())


def visible_prefix_len(curve):
    """Arc length of ``curve``'s in-frame part, contiguous from its start.

    Lines that loop far beyond the frame (the backward fan angles) are only
    visible for their first stretch; arrowheads are placed on that stretch so
    they never end up floating in the invisible off-frame part of a loop.
    """
    pts = np.asarray(curve.get_anchors(), dtype=float)
    inside = (np.abs(pts[:, 0]) <= FRAME_HW + 0.05) & (np.abs(pts[:, 1]) <= FRAME_HH + 0.05)
    n = int(np.argmin(inside)) if not inside.all() else len(pts)
    if n < 2:
        return 0.0
    seg = np.linalg.norm(np.diff(pts[:n], axis=0), axis=1)
    return float(seg.sum())


def point_and_tangent(curve, s):
    """Position + unit tangent on ``curve`` at arc length ``s`` from its start.

    Re-evaluated from the curve's anchors every frame, so anything attached to
    the curve — field-line arrows, the test charge, the force vector — follows
    it automatically while the curve is being transformed.
    """
    pts = np.asarray(curve.get_anchors(), dtype=float)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    s = np.clip(s, 0.0, cum[-1])
    idx = np.clip(np.searchsorted(cum, s, side="right") - 1, 0, len(pts) - 2)
    t = (s - cum[idx]) / max(seg[idx], 1e-12)
    pos = pts[idx] + t * (pts[idx + 1] - pts[idx])
    d = pts[idx + 1] - pts[idx]
    norm = np.linalg.norm(d)
    tangent = d / norm if norm > 1e-9 else np.array([1.0, 0.0, 0.0])
    return pos, tangent


def flow_arrowhead(curve, base_frac, phase, fade, color=BLUE_E, size=ARROW_SIZE):
    """A small arrowhead embedded on ``curve``, drifting along it with the flow.

    ``always_redraw`` re-creates it every frame from the curve's *current*
    anchors, so it stays glued to the line and rotates with the local tangent
    even while the line itself is being transformed.  ``phase`` is a
    ValueTracker: increasing it moves the arrowhead outward along the line
    (from the "+" charge toward the "-" charge); ``fade`` fades the arrowheads
    in as a group when the lines are first drawn.
    """

    def getter():
        vis_len = visible_prefix_len(curve)
        if vis_len < 1e-6:
            tip = Triangle(color=color, fill_color=color, fill_opacity=1.0, stroke_width=1.0)
            return tip.scale(size).set_opacity(0.0)
        frac = (base_frac + phase.get_value() * FLOW_SPEED) % 1.0
        pos, tangent = point_and_tangent(curve, frac * vis_len)
        theta = np.arctan2(tangent[1], tangent[0])
        # Triangle() points up by default; rotate it onto the local tangent.
        tip = Triangle(color=color, fill_color=color, fill_opacity=1.0, stroke_width=1.0)
        tip.scale(size).move_to(pos).rotate(theta - PI / 2)
        tip.set_opacity(fade.get_value())
        return tip

    return always_redraw(getter)


def charge_circle(pos, sign, color):
    """A filled charge circle with a white "+/-" sign on top.

    The sign follows the circle via an updater, so the label travels with the
    negative charge as it slides across the scene.
    """
    circle = Circle(radius=CHARGE_R, fill_color=color, fill_opacity=0.95, stroke_width=0).move_to(pos)
    sign_mob = MathTex(sign, color=WHITE, font_size=44).move_to(pos)
    sign_mob.add_updater(lambda m: m.move_to(circle.get_center()))
    return circle, sign_mob


class ElectricFieldLines(ShortScene):
    """Positive charge -> radial field -> dipole -> test charge accelerating."""

    # Vertical layout zones (the template defaults suit derivation shorts;
    # this scene keeps the hero diagram centered with a title above and a
    # formula slot below).
    TOP_Y = 6.7  # title zone
    HERO_Y = 0.5  # hero diagram center
    BOTTOM_Y = -3.5  # formula slot (F = qE)

    def construct(self):
        # Colours follow the project style guide: blue for primary objects,
        # red for the positive charge / final highlight, purple for the test
        # charge.  The force vector is deliberately uncoloured (black).
        field_color = BLUE
        arrow_color = BLUE_E
        pos_color = RED
        neg_color = BLUE
        test_color = PURPLE
        force_color = BLACK

        # Charge positions: "+" at center-left, "-" starts far beyond the
        # frame (fully off-screen) and slides to a symmetric dipole spot.
        p_plus = self.hero_zone + LEFT * 1.3
        p_minus_far = self.hero_zone + RIGHT * 7.0
        p_minus_near = self.hero_zone + RIGHT * 1.3
        angles = sorted({-a for a in START_ANGLES} | set(START_ANGLES))

        # Field lines for every approach step of the - charge.  All lines of
        # all states share N_ANCHORS anchors, which is what lets Transform
        # bend them continuously instead of redrawing the field.  A power-law
        # spacing keeps the steps fine while the charge is still off-screen.
        t_grid = np.linspace(0.0, 1.0, 16)
        approach_xs = p_minus_near[0] + (p_minus_far[0] - p_minus_near[0]) * (1.0 - t_grid) ** 1.4
        state_points = []
        for x in approach_xs:
            p_minus = self.hero_zone + RIGHT * x
            state_points.append([resample(trace_field_line(p_plus, p_minus, a)) for a in angles])

        # State 0 of the story: the lone positive charge, whose field lines
        # are straight radial rays reaching the edge of the frame.
        radial_points = []
        for a in angles:
            theta = np.deg2rad(a)
            start = p_plus + START_R * np.array([np.cos(theta), np.sin(theta), 0.0])
            radial_points.append(resample(np.array([start, ray_to_frame(p_plus, a)])))

        lines = [curve_from_points(radial_points[i], color=field_color) for i in range(len(angles))]
        state_curves = [[curve_from_points(p, color=field_color) for p in state] for state in state_points]

        # Directional arrowheads: two per line, drifting along it with the
        # shared flow phase.  They are added immediately but stay invisible
        # until the shared fade tracker is animated.
        phase = ValueTracker(0.0)
        fade = ValueTracker(0.0)
        arrows = VGroup()
        for line in lines:
            for frac in ARROW_FRACS:
                arrows.add(flow_arrowhead(line, frac, phase, fade, color=arrow_color))
        self.add(arrows)

        # The charges themselves.
        pos_circle, pos_sign = charge_circle(p_plus, "+", pos_color)
        neg_circle, neg_sign = charge_circle(p_minus_far, "-", neg_color)

        title = Text("Electric field lines", font_size=48, weight=BOLD).move_to(self.top_zone)

        # --- ACT 1: a lone positive charge, radial field lines ----------------
        with self.voiceover(
            text="A positive charge creates an electric field, pointing radially outward from the charge."
        ) as tracker:
            self.play(FadeIn(title), FadeIn(pos_circle), Write(pos_sign), run_time=tracker.duration * 0.35)
            # The title leaves as the lines arrive (steep lines span the full
            # frame height, so they must not overlap the title text).
            self.play(FadeOut(title), *[Create(line) for line in lines], lag_ratio=0.5, run_time=tracker.duration * 0.65)

        with self.voiceover(text="The arrows embedded in the lines always point away from the positive charge.") as tracker:
            self.play(fade.animate.set_value(1.0), phase.animate.increment_value(0.5), run_time=tracker.duration)

        # --- ACT 2: the negative charge is introduced, far beyond the frame --
        # The charge stays fully off-screen ("way beyond the frame"); only the
        # narration introduces it, and the field still looks radial.
        with self.voiceover(
            text="Now suppose a negative charge sits very far away, beyond the frame on the right."
        ) as tracker:
            self.play(phase.animate.increment_value(0.4), run_time=tracker.duration)
        self.add(neg_circle, neg_sign)  # off-screen; it slides into view in Act 3

        # --- ACT 3: the negative charge approaches, field lines bend ---------
        def approach_step(k, run_time):
            p_minus = self.hero_zone + RIGHT * approach_xs[k]
            # ``rate_func=linear`` keeps the charge moving at constant speed
            # with no easing stop between steps: one continuous approach
            # instead of stop-motion.
            self.play(
                neg_circle.animate.move_to(p_minus),
                *[Transform(lines[i], state_curves[k][i]) for i in range(len(angles))],
                phase.animate.increment_value(0.08),
                rate_func=linear,
                run_time=run_time,
            )

        with self.voiceover(
            text="As it moves closer, the field lines begin to bend toward it, even the ones pointing away."
        ) as tracker:
            for k in range(0, 8):
                approach_step(k, tracker.duration / 8)

        with self.voiceover(
            text="Watch: even the lines on the left swing around and flow into the negative charge."
        ) as tracker:
            for k in range(8, 16):
                approach_step(k, tracker.duration / 8)

        # --- ACT 4: final dipole, arrows still point from "+" to "-" ---------
        with self.voiceover(
            text=(
                "The field lines now curve around and sweep into the negative charge, "
                "and the arrows still point from plus to minus."
            )
        ) as tracker:
            self.play(phase.animate.increment_value(0.7), run_time=tracker.duration)

        # --- ACT 5: a positive test charge accelerates along a field line ----
        # Ride the curved 80-degree line: the dot and the force arrow re-read
        # the line's position/tangent at the tracked arc length every frame,
        # so the force stays tangent and rotates as the particle moves.
        chosen = lines[angles.index(TEST_LINE_ANGLE)]
        s_total = curve_length(chosen)
        # The ride stops well short of the - charge so it never crowds it.
        s_start, s_end = 1.0, 0.75 * s_total
        s_tc = ValueTracker(s_start)

        tc_dot = Circle(radius=0.14, fill_color=test_color, fill_opacity=1.0, stroke_width=0)
        tc_dot.add_updater(lambda m: m.move_to(point_and_tangent(chosen, s_tc.get_value())[0]))
        tc_label = MathTex("+q", color=test_color, font_size=30)
        tc_label.add_updater(lambda m: m.next_to(tc_dot, UP, buff=0.08))

        force_vec = Arrow(ORIGIN, RIGHT, color=force_color, stroke_width=10, buff=0, max_tip_length_to_length_ratio=0.3)
        force_vec.add_updater(lambda m: m.put_start_and_end_on(*_force_span(chosen, s_tc.get_value())))
        f_label = MathTex(r"\vec F", color=force_color, font_size=34)
        f_label.add_updater(lambda m: m.next_to(force_vec.get_end(), UP * 0.1 + RIGHT * 0.12))

        with self.voiceover(text="Now place a small positive test charge here, right on a field line.") as tracker:
            self.play(FadeIn(tc_dot), FadeIn(tc_label), run_time=tracker.duration)
        self.wait(0.5)  # brief pause so the test charge is clearly visible

        f_eq = MathTex(r"\vec F = q\vec E", color=force_color, font_size=44).move_to(self.active_zone)
        with self.voiceover(
            text=(
                "The electric field at this point is tangent to the field line, "
                "so the positive charge feels a force F, equal to q times E, pointing along the field."
            )
        ) as tracker:
            self.play(Create(force_vec), FadeIn(f_label), run_time=tracker.duration * 0.6)
            self.play(FadeIn(f_eq), run_time=tracker.duration * 0.4)

        # Arc length grows quadratically (rate t^2): the charge accelerates
        # along the field line instead of moving at constant speed.
        with self.voiceover(
            text=("The test charge accelerates along the field line, following the curve toward the negative charge.")
        ) as tracker:
            self.play(
                s_tc.animate.set_value(s_end),
                rate_func=lambda t: t * t,
                run_time=tracker.duration,
            )

        self.box_final(f_eq, color=RED)
        self.wait(1.5)


def _force_span(curve, s):
    """Start/end points of the force vector at arc length ``s`` on ``curve``.

    The force on a positive charge points along the local tangent of the
    electric field line, i.e. along E itself.
    """
    pos, tangent = point_and_tangent(curve, s)
    return pos, pos + 0.7 * tangent
