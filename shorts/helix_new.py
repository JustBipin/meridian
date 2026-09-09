import numpy as np
from manim import *

from shorts.shorts_template import ThreeDShortScene, apply_vertical_config

apply_vertical_config()


class HelixArcLength(ThreeDShortScene):
    """
    Helix Arc Length (Under 45s)
    Uses KokoroService for high-quality TTS.
    """

    # Vertical layout zones
    TOP_Y = 3.2
    HERO_Y = 0.3
    BOTTOM_Y = -2.6
    OLD_Y = -1.7

    def construct(self):
        # Constants for layout and colors
        DARK_TEXT = "#222222"
        MAIN_BLUE = BLUE
        MAIN_RED = RED
        MAIN_TEAL = TEAL

        title = Text("Arc length of a helix", font_size=34, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.6)

        with self.voiceover(text="Here's how you find the arc length of this helix.") as tracker:
            self.play(FadeIn(title, shift=DOWN * 0.2), run_time=tracker.duration)

        ref_formula = MathTex(r"\vec{r}(t) = (\cos t,\ \sin t,\ t)", color=DARK_TEXT, font_size=30)
        goal = MathTex(r"L = \,?", color=MAIN_RED, font_size=32)
        top_group = VGroup(ref_formula, goal).arrange(DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(top_group)
        top_group.move_to(self.top_zone)

        with self.voiceover(text="represented by the equation, r of t equals, cosine t, sine t, t.") as tracker:
            self.play(
                FadeOut(title),
                Write(ref_formula),
                FadeIn(goal, shift=UP * 0.1),
                run_time=tracker.duration,
            )

        helix = ParametricFunction(
            lambda t: np.array([np.cos(t), np.sin(t), t * 0.55 - 1.7]),
            t_range=[0, 4 * PI, 0.01],
            color=MAIN_BLUE,
            stroke_width=5,
        )
        hero = VGroup(helix).move_to(self.hero_zone)

        with self.voiceover(text="Take a look at this helix.") as tracker:
            self.play(
                Create(hero),
                Rotate(hero, angle=PI / 6, axis=UP, about_point=hero.get_center()),
                run_time=tracker.duration,
            )

        t0 = 2.4
        p_point = hero.get_center() + np.array([np.cos(t0), np.sin(t0), t0 * 0.55 - 1.7])
        dot = Dot3D(point=p_point, color=MAIN_RED, radius=0.06)
        pos_vec = Arrow3D(start=hero.get_center(), end=p_point, color=MAIN_RED, thickness=0.02)

        vec_label = MathTex(r"\vec{r}(t)", color=MAIN_RED, font_size=26)
        self.add_fixed_in_frame_mobjects(vec_label)
        vec_label.next_to(dot, RIGHT, buff=0.3)

        with self.voiceover(text="Suppose you have a point on the helix, and its position vector is r of t.") as tracker:
            self.play(
                FadeIn(dot),
                Create(pos_vec),
                Write(vec_label),
                run_time=tracker.duration,
            )

        t1 = t0 + 0.35
        p1 = hero.get_center() + np.array([np.cos(t1), np.sin(t1), t1 * 0.55 - 1.7])
        dl_seg = Line3D(start=p_point, end=p1, color=MAIN_TEAL, thickness=0.02)
        dl_label = MathTex(r"d\ell", color=MAIN_TEAL, font_size=26)
        self.add_fixed_in_frame_mobjects(dl_label)
        dl_label.next_to((p_point + p1) / 2, RIGHT, buff=0.3)

        with self.voiceover(
            text=(
                "If you integrate the small distances traveled by the point, along the entire path, "
                "you get the length of the helix."
            )
        ) as tracker:
            self.play(Create(dl_seg), Write(dl_label), run_time=tracker.duration)

        step1 = MathTex(r"L = \int d\ell", font_size=30)
        with self.voiceover(text="L equals the integral of d l.") as tracker:
            self.play_step(step1, run_time=tracker.duration)

        step2 = MathTex(r"d\ell = |\vec{v}|\, dt", font_size=30)
        with self.voiceover(text="The small length is just its speed, times a small time, d t.") as tracker:
            self.play_step(step2, active=step1, run_time=tracker.duration)

        step3 = MathTex(r"|\vec{v}| = |\vec{r}\,'(t)|", font_size=30)
        with self.voiceover(
            text="But speed is the magnitude of velocity, which is the derivative of position, r prime."
        ) as tracker:
            self.play_step(step3, active=step2, old=step1, run_time=tracker.duration)

        tangent_vec = Arrow3D(
            start=p_point,
            end=p_point + np.array([-np.sin(t0), np.cos(t0), 0.55]) * 0.6,
            color=MAIN_BLUE,
            thickness=0.02,
        )

        step4 = MathTex(r"\vec{r}\,'(t) = (-\sin t,\ \cos t,\ 1)", font_size=28)
        with self.voiceover(text="which is, negative sine t, cosine t, one.") as tracker:
            self.play_step(
                step4,
                active=step3,
                old=step2,
                run_time=tracker.duration,
                extra_anims=[
                    pos_vec.animate.set_opacity(0.5),
                    dl_seg.animate.set_opacity(0.5),
                    dl_label.animate.set_opacity(0.5),
                    Create(tangent_vec),
                ],
            )

        step5a = MathTex(r"|\vec{r}\,'(t)| = \sqrt{\sin^2 t + \cos^2 t + 1^2}", font_size=26)
        with self.voiceover(text="So the speed is, square root of sine squared plus cosine squared plus one.") as tracker:
            self.play_step(step5a, active=step4, old=step3, scale=0.7, run_time=tracker.duration)

        step5b = MathTex(r"|\vec{r}\,'(t)| = \sqrt{2}", font_size=30)
        self.add_fixed_in_frame_mobjects(step5b)
        step5b.move_to(self.active_zone)

        with self.voiceover(text="which simplifies to, square root of two.") as tracker:
            self.play(Transform(step5a, step5b), run_time=tracker.duration)

        step6 = MathTex(r"d\ell = \sqrt{2}\, dt", font_size=30)
        with self.voiceover(text="Substituting this back: d l equals square root of two, d t.") as tracker:
            self.play_step(step6, active=step5a, old=step4, run_time=tracker.duration)

        step7 = MathTex(r"L = \int_0^{4\pi} \sqrt{2}\, dt", font_size=28)
        with self.voiceover(text="Integrating from zero to four pi.") as tracker:
            self.play_step(step7, active=step6, old=step5a, run_time=tracker.duration)

        answer = MathTex(r"L = 4\pi\sqrt{2}", color=MAIN_RED, font_size=34)
        self.add_fixed_in_frame_mobjects(answer)
        answer.move_to(self.active_zone)

        answer_top = MathTex(r"L = 4\pi\sqrt{2}", color=MAIN_RED, font_size=32)
        self.add_fixed_in_frame_mobjects(answer_top)
        answer_top.move_to(goal.get_center())

        with self.voiceover(text="and you get, four pi root two.") as tracker:
            self.resolve_step(step7, answer, goal=goal, goal_answer=answer_top, fade_out=step6, run_time=tracker.duration)
