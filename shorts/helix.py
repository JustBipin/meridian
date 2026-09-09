import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from shorts.shorts_template import set_kokoro_voice


class HelixArcLength(ThreeDScene, VoiceoverScene):
    """
    Helix Arc Length Short (~60s) — Rediscovering the Formula
    -----------------------------------------------------------
    Three fixed screen panels (matching the storyboard wireframe):
        TOP    (~16%)  — persistent goal r(t), + last "settled" result
        MIDDLE (~54%)  — the 3D helix, axes, single moving point
        BOTTOM (~30%)  — the currently-active derivation / caption

    The camera is set ONCE at the start and never moves or rotates
    again. All "spin" comes from rotating the hero geometry (axes +
    helix) itself — a full 2*pi turn in Scene 1, so the net transform
    is identity and every later scene can still use raw r(t)
    coordinates. Formulas and captions are added via
    add_fixed_in_frame_mobjects, so they render as a flat, undistorted
    HUD regardless of the hero's orientation — they never rotate with
    the diagram. Keeping the camera itself static (instead of using
    begin_ambient_camera_rotation) avoids the tearing/z-fighting
    artifacts that show up when a moving 3D camera and fixed-in-frame
    overlays are composited together in the same frame.
    Only ONE point ever exists on the helix; it slides along the
    curve rather than multiple markers appearing at once.
    The ending uncurls the helix into a straight segment (radius
    shrinks to zero while position walks out to true arc length)
    instead of flattening/squashing it.
    """

    def setup(self):
        super().setup()
        # apply_theme(manim_scene=self, theme_name="london")

    def construct(self):
        # =========================================================
        # VOICE CONFIGURATION
        # =========================================================
        set_kokoro_voice(self, speed=1.05)

        DARK_TEXT = "#222222"
        MAIN_BLUE = BLUE
        MAIN_RED = RED
        AXIS_COLOR = GREY_C
        BG = config.background_color

        # =========================================================
        # PANEL GEOMETRY (screen-space, fixed-in-frame)
        # =========================================================
        FW, FH = config.frame_width, config.frame_height
        TOP_H = FH * 0.16
        BOTTOM_H = FH * 0.30
        # middle band spans from  (FH/2 - TOP_H)  down to  (-FH/2 + BOTTOM_H)

        top_bar = Rectangle(width=FW, height=TOP_H, fill_color=BG, fill_opacity=1, stroke_width=0)
        top_bar.move_to(UP * (FH / 2 - TOP_H / 2))
        bottom_bar = Rectangle(width=FW, height=BOTTOM_H, fill_color=BG, fill_opacity=1, stroke_width=0)
        bottom_bar.move_to(DOWN * (FH / 2 - BOTTOM_H / 2))

        top_divider = Line(LEFT * FW / 2, RIGHT * FW / 2, stroke_color=AXIS_COLOR, stroke_width=1.5)
        top_divider.move_to(UP * (FH / 2 - TOP_H))
        bottom_divider = Line(LEFT * FW / 2, RIGHT * FW / 2, stroke_color=AXIS_COLOR, stroke_width=1.5)
        bottom_divider.move_to(DOWN * (FH / 2 - BOTTOM_H))

        panels = VGroup(top_bar, bottom_bar, top_divider, bottom_divider)
        self.add_fixed_in_frame_mobjects(panels)

        def in_top(mobj, buff=0.22):
            mobj.move_to(top_bar.get_center())
            mobj.to_edge(UP, buff=buff)
            return mobj

        def in_bottom(mobj, buff=0.35):
            mobj.move_to(bottom_bar.get_center())
            mobj.to_edge(DOWN, buff=buff)
            return mobj

        # =========================================================
        # CAMERA — set ONCE, never moved or rotated again. All motion
        # in this scene comes from rotating the hero geometry itself,
        # not the camera — this is what keeps the fixed-in-frame HUD
        # (panels + formulas) from tearing against the 3D render.
        # =========================================================
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES, zoom=1.5)

        # =========================================================
        # HELIX GEOMETRY
        # =========================================================
        DISPLAY_R = 1.5  # visual radius (bigger than before)
        Z_SCALE = 0.42  # visual z compression so one turn fits the middle band
        t_max = 2 * PI

        def r(t):
            return np.array([DISPLAY_R * np.cos(t), DISPLAY_R * np.sin(t), t * Z_SCALE])

        def r_raw(t):
            # TRUE r(t) = <cos t, sin t, t> — used only for the actual math/arc-length
            return np.array([np.cos(t), np.sin(t), t])

        # true cumulative arc length, sampled finely, for later use in the ending
        samples = np.linspace(0, t_max, 400)
        raw_pts = np.array([r_raw(tt) for tt in samples])
        seg_lens = np.linalg.norm(np.diff(raw_pts, axis=0), axis=1)
        cum_len = np.concatenate([[0], np.cumsum(seg_lens)])
        total_length = cum_len[-1]  # ~ 2*pi*sqrt(2)

        def arclen_at(t):
            return np.interp(t, samples, cum_len)

        helix = ParametricFunction(r, t_range=[0, t_max], color=MAIN_BLUE, stroke_width=6)

        # =========================================================
        # AXES — x, y, z reference lines with endpoint markers only,
        # no numeric labels (per note: show the range, not numbers).
        # =========================================================
        ax_pad = 0.6
        x_end = DISPLAY_R + ax_pad
        y_end = DISPLAY_R + ax_pad
        z_top = t_max * Z_SCALE + ax_pad * 0.5

        x_axis = Line3D(np.array([-x_end, 0, 0]), np.array([x_end, 0, 0]), color=AXIS_COLOR, thickness=0.012)
        y_axis = Line3D(np.array([0, -y_end, 0]), np.array([0, y_end, 0]), color=AXIS_COLOR, thickness=0.012)
        z_axis = Line3D(np.array([0, 0, -ax_pad * 0.5]), np.array([0, 0, z_top]), color=AXIS_COLOR, thickness=0.012)

        endpoint_dots = VGroup(*[
            Dot3D(point=p, radius=0.045, color=AXIS_COLOR)
            for p in [
                (-x_end, 0, 0),
                (x_end, 0, 0),
                (0, -y_end, 0),
                (0, y_end, 0),
                (0, 0, -ax_pad * 0.5),
                (0, 0, z_top),
            ]
        ])
        axes = VGroup(x_axis, y_axis, z_axis, endpoint_dots)

        # =========================================================
        # TOP PANEL — persistent goal + "settled" result from
        # whichever derivation just finished (replaced each scene)
        # =========================================================
        title = Text("How Long is this Helix?", font_size=32, color=DARK_TEXT, weight=BOLD)
        eq_goal = MathTex(r"r(t)=\langle \cos t,\ \sin t,\ t\rangle", color=DARK_TEXT, font_size=32)
        header = VGroup(title, eq_goal).arrange(DOWN, buff=0.12)
        in_top(header)
        self.add_fixed_in_frame_mobjects(header)
        header.set_opacity(0)

        # placeholder that will hold the "settled" secondary line once title is gone
        # (an invisible Dot, not an empty MathTex — empty TeX strings fail to compile)
        settled = Dot(radius=0.001, fill_opacity=0)
        settled.move_to(eq_goal.get_center() + DOWN * 0.55)

        def settle(new_content_mobj, run_time=0.5):
            """Promote a finished derivation's last line into the top panel."""
            nonlocal settled
            new_content_mobj.move_to(eq_goal.get_center() + DOWN * 0.55)
            if new_content_mobj.width > FW * 0.4:
                new_content_mobj.scale_to_fit_width(FW * 0.4)
                new_content_mobj.move_to(eq_goal.get_center() + DOWN * 0.55)
            self.add_fixed_in_frame_mobjects(new_content_mobj)
            self.play(ReplacementTransform(settled, new_content_mobj), run_time=run_time)
            settled = new_content_mobj

        # =========================================================
        # BOTTOM PANEL — the single "active" derivation / caption
        # =========================================================
        active = Dot(radius=0.001, fill_opacity=0)  # inert placeholder to transform from first
        in_bottom(active)
        self.add_fixed_in_frame_mobjects(active)

        def show_step(new_mobj, run_time=1.0, caption=False):
            """Replace the bottom panel's content in place (no stacking)."""
            nonlocal active
            in_bottom(new_mobj, buff=0.5 if caption else 0.6)
            self.add_fixed_in_frame_mobjects(new_mobj)
            self.play(ReplacementTransform(active, new_mobj), run_time=run_time)
            active = new_mobj

        # =========================================================
        # SCENE 1 — HOOK
        # =========================================================
        hero = VGroup(axes, helix)  # everything that's allowed to rotate as "the diagram"

        with self.voiceover(
            text="Here's how you find the arc length of this helix, represented by the equation, "
            "r of t equals cosine t, sine t, comma t."
        ) as tracker:
            t = tracker.duration
            self.play(
                header.animate.set_opacity(1),
                Create(axes),
                Create(helix),
                run_time=t * 0.55,
            )
            # one full revolution: net transform is identity, so every later
            # scene can keep using r(t) coordinates directly without drift
            self.play(
                Rotate(hero, angle=TAU, axis=OUT, about_point=ORIGIN),
                run_time=t * 0.45,
                rate_func=linear,
            )

        self.play(FadeOut(title), run_time=0.5)
        eq_goal.generate_target()
        in_top(eq_goal, buff=0.28)
        self.play(MoveToTarget(eq_goal), run_time=0.4)
        settled.move_to(eq_goal.get_center() + DOWN * 0.55)

        # =========================================================
        # SCENE 2 — THE MOVING POINT (single point, reused everywhere)
        # =========================================================
        point = Dot3D(point=r(0), color=MAIN_RED, radius=0.09)
        position_vec = always_redraw(lambda: Line3D(ORIGIN, point.get_center(), color=MAIN_BLUE, thickness=0.02))

        cap2 = Text("Position Vector", font_size=26, color=DARK_TEXT)
        in_bottom(cap2, buff=0.5)
        self.add_fixed_in_frame_mobjects(cap2)
        self.play(ReplacementTransform(active, cap2), run_time=0.01)
        active = cap2

        with self.voiceover(
            text="Suppose you have a point moving along the helix, and its position vector is r of t."
        ) as tracker:
            t = tracker.duration
            self.play(
                FadeIn(point),
                Create(position_vec),
                helix.animate.set_opacity(0.5),
                run_time=t,
            )

        # =========================================================
        # SCENE 3 — TINY PIECES (single point sliding, leaving a trail)
        # =========================================================
        cap3 = Text("Add Tiny Distances", font_size=26, color=DARK_TEXT)
        show_step(cap3, run_time=0.4, caption=True)

        trail = TracedPath(point.get_center, stroke_color=MAIN_RED, stroke_width=6)
        self.add(trail)

        dl_label = MathTex("dl", color=MAIN_RED, font_size=30)

        with self.voiceover(
            text="Now imagine breaking the helix into tiny pieces. If you could add every small distance "
            "travelled by the point, you would get the total length of the helix."
        ) as tracker:
            t = tracker.duration
            eps = 0.22
            small_arc = ParametricFunction(r, t_range=[0, eps])
            dl_label.next_to(small_arc.point_from_proportion(0.5), RIGHT, buff=0.15)
            self.add_fixed_orientation_mobjects(dl_label)

            self.play(MoveAlongPath(point, small_arc), run_time=t * 0.15)
            self.play(FadeIn(dl_label), run_time=t * 0.1)
            self.play(
                MoveAlongPath(point, ParametricFunction(r, t_range=[eps, t_max])),
                run_time=t * 0.75,
                rate_func=linear,
            )

        self.play(FadeOut(dl_label), helix.animate.set_opacity(1), run_time=0.4)
        settle(MathTex("dl", color=DARK_TEXT, font_size=30), run_time=0.4)
        self.play(FadeOut(trail), helix.animate.set_opacity(0.5), FadeOut(position_vec), FadeOut(point), run_time=0.4)

        # =========================================================
        # SCENE 4 — WHAT IS dl?
        # =========================================================
        eq4 = MathTex(r"dl = \text{speed} \times dt", color=DARK_TEXT, font_size=32)
        with self.voiceover(text="The small distance travelled is simply the speed multiplied by a small time.") as tracker:
            show_step(eq4, run_time=tracker.duration)

        # =========================================================
        # SCENE 5 — REPLACE SPEED
        # =========================================================
        eq5a = MathTex(r"\text{speed} = |v|", color=DARK_TEXT, font_size=32)
        eq5b = MathTex(r"v = r'(t)", color=DARK_TEXT, font_size=32)
        eq5c = MathTex(r"dl = |r'(t)|\, dt", color=DARK_TEXT, font_size=32)
        with self.voiceover(
            text="But speed is just the magnitude of velocity. And velocity is simply the first derivative "
            "of the position vector."
        ) as tracker:
            t = tracker.duration
            show_step(eq5a, run_time=t * 0.3)
            in_bottom(eq5b, buff=0.6)
            self.play(ReplacementTransform(active, eq5b), run_time=t * 0.3)
            active = eq5b
            in_bottom(eq5c, buff=0.6)
            self.play(ReplacementTransform(active, eq5c), run_time=t * 0.4)
            active = eq5c
        settle(eq5c.copy(), run_time=0.5)

        # =========================================================
        # SCENE 6 — DIFFERENTIATE
        # =========================================================
        eq6 = MathTex(r"r'(t) = \langle -\sin t,\ \cos t,\ 1\rangle", color=DARK_TEXT, font_size=30)
        with self.voiceover(text="Taking the derivative gives us negative sine t, cosine t, one.") as tracker:
            show_step(eq6, run_time=tracker.duration)
        settle(eq6.copy(), run_time=0.5)

        # =========================================================
        # SCENE 7 — FIND THE SPEED
        # =========================================================
        eq7a = MathTex(r"|r'(t)| = \sqrt{(-\sin t)^2 + (\cos t)^2 + 1^2}", color=DARK_TEXT, font_size=26)
        eq7b = MathTex(r"|r'(t)| = \sqrt{\sin^2 t + \cos^2 t + 1}", color=DARK_TEXT, font_size=28)
        eq7c = MathTex(r"|r'(t)| = \sqrt{2}", color=DARK_TEXT, font_size=32)
        with self.voiceover(
            text="The speed is the magnitude of the velocity vector. That is the square root of negative "
            "sine squared t, plus cosine squared t, plus one squared. Since sine squared plus cosine "
            "squared equals one, the speed simplifies to the square root of two."
        ) as tracker:
            t = tracker.duration
            show_step(eq7a, run_time=t * 0.4)
            in_bottom(eq7b, buff=0.6)
            self.play(ReplacementTransform(active, eq7b), run_time=t * 0.3)
            active = eq7b
            in_bottom(eq7c, buff=0.6)
            self.play(ReplacementTransform(active, eq7c), run_time=t * 0.3)
            active = eq7c
        settle(eq7c.copy(), run_time=0.5)

        # =========================================================
        # SCENE 8 — SUBSTITUTE BACK
        # =========================================================
        eq8 = MathTex(r"dl = \sqrt{2}\, dt", color=DARK_TEXT, font_size=34)
        with self.voiceover(
            text="So every tiny distance travelled is simply the square root of two times a small time."
        ) as tracker:
            show_step(eq8, run_time=tracker.duration)
        settle(eq8.copy(), run_time=0.5)

        # =========================================================
        # SCENE 9 — ADD EVERY TINY DISTANCE (single point re-slides)
        # =========================================================
        eq9a = MathTex(r"L = \int dl", color=DARK_TEXT, font_size=32)
        eq9b = MathTex(r"L = \int_0^{2\pi} \sqrt{2}\, dt", color=DARK_TEXT, font_size=32)

        point.move_to(r(0))
        self.add(point)

        with self.voiceover(
            text="Now add every tiny distance from zero to two pi, one complete turn of the helix."
        ) as tracker:
            t = tracker.duration
            show_step(eq9a, run_time=t * 0.25)
            in_bottom(eq9b, buff=0.6)
            self.play(
                ReplacementTransform(active, eq9b),
                MoveAlongPath(point, ParametricFunction(r, t_range=[0, t_max]), rate_func=linear),
                helix.animate.set_opacity(1),
                run_time=t * 0.75,
            )
            active = eq9b
        self.play(FadeOut(point), helix.animate.set_opacity(0.5), run_time=0.3)
        settle(eq9b.copy(), run_time=0.5)

        # =========================================================
        # SCENE 10 — EVALUATE
        # =========================================================
        eq10a = MathTex(r"L = \sqrt{2}\int_0^{2\pi} dt", color=DARK_TEXT, font_size=32)
        eq10b = MathTex(r"L = \sqrt{2}\,[t]_0^{2\pi}", color=DARK_TEXT, font_size=32)
        eq10c = MathTex(r"L = \sqrt{2}(2\pi)", color=DARK_TEXT, font_size=32)
        eq_final = MathTex(r"L = 2\pi\sqrt{2}", color=DARK_TEXT, font_size=38)
        with self.voiceover(
            text="The square root of two is constant, so it comes outside the integral. The integral of one "
            "with respect to t is simply t. Evaluating from zero to two pi gives two pi times the square "
            "root of two."
        ) as tracker:
            t = tracker.duration
            show_step(eq10a, run_time=t * 0.22)
            in_bottom(eq10b, buff=0.6)
            self.play(ReplacementTransform(active, eq10b), run_time=t * 0.22)
            active = eq10b
            in_bottom(eq10c, buff=0.6)
            self.play(ReplacementTransform(active, eq10c), run_time=t * 0.22)
            active = eq10c
            in_bottom(eq_final, buff=0.6)
            self.play(ReplacementTransform(active, eq_final), run_time=t * 0.34)
            active = eq_final

        self.wait(0.3)

        # =========================================================
        # ENDING — HELIX UNCURLS INTO A STRAIGHT SEGMENT
        # (radius -> 0 while position walks out to true arc length;
        # NOT a flatten/squash — the coil visibly unwinds)
        # =========================================================
        self.play(FadeOut(header), FadeOut(active), FadeOut(axes), run_time=0.4)

        line_label = MathTex(r"2\pi\sqrt{2}", color=DARK_TEXT, font_size=32)
        cap_end = Text("Arc Length", font_size=26, color=DARK_TEXT)
        in_bottom(cap_end, buff=0.5)
        self.add_fixed_in_frame_mobjects(cap_end)
        cap_end.set_opacity(0)

        n_pts = 160
        ts = np.linspace(0, t_max, n_pts)

        def uncurl(mobj, alpha):
            pts = []
            for tt in ts:
                rad = DISPLAY_R * (1 - alpha)
                theta = tt * (1 - alpha)
                x = rad * np.cos(theta)
                y = rad * np.sin(theta)
                # position along the unwound axis: blend visual-z toward
                # the true-arclength position (centered), scaled for display
                unwound = (arclen_at(tt) - total_length / 2) * DISPLAY_R * 0.55
                z = (1 - alpha) * (tt * Z_SCALE) + alpha * unwound
                pts.append([x, y, z])
            mobj.set_points_smoothly(pts)

        with self.voiceover(text="And that's the arc length of one complete turn of the helix.") as tracker:
            t = tracker.duration
            self.play(
                UpdateFromAlphaFunc(helix, uncurl),
                cap_end.animate.set_opacity(1),
                run_time=t * 0.75,
                rate_func=smooth,
            )
            line_label.next_to(helix, DOWN, buff=0.3)
            self.add_fixed_orientation_mobjects(line_label)
            self.play(Write(line_label), run_time=t * 0.25)

        self.wait(1.2)
