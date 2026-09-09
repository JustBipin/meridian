"""Reusable scaffolding for the root-level voiceover "shorts".

Extracts the conventions shared by every vertical 9:16 short animation in the
project root (pi.py, circle_short.py, helix_new.py, area_short.py, the
triangle shorts, probability.py, ...):

* the vertical 1080x1920 (9:16) render config
* the light "london" theme
* Kokoro TTS setup with a consistent default voice profile
* named vertical layout zones (top / hero / active derivation / retired)
* goal -> derive -> resolve helpers
* a final-answer highlight helper

Quick start
-----------
    from manim import *
    from shorts_template import ShortScene, apply_vertical_config

    apply_vertical_config()  # module level, before the scene is instantiated

    class MyShort(ShortScene):
        SPEED = 1.15          # optional voice tweaks
        TOP_Y = 3.2           # optional zone overrides

        def construct(self):
            with self.voiceover(text="Here is the plan.") as tracker:
                self.play(Create(something), run_time=tracker.duration)

See docs/SHORTS_TEMPLATE.md for the full guide.
"""

from kokoro_mv import KokoroService
from manim import *
from manim_themes.manim_theme import apply_theme
from manim_voiceover import VoiceoverScene

# ---------------------------------------------------------------------------
# Vertical 9:16 render config
# ---------------------------------------------------------------------------

PIXEL_WIDTH = 1080
PIXEL_HEIGHT = 1920
FRAME_WIDTH = 9.0
FRAME_HEIGHT = 16.0


def apply_vertical_config():
    """Switch the render canvas to the standard vertical 1080x1920 (9:16) format.

    Call it at module level (where the old ``config.pixel_width = ...`` lines
    lived), because the canvas is fixed when the scene is instantiated.
    """
    config.pixel_width = PIXEL_WIDTH
    config.pixel_height = PIXEL_HEIGHT
    config.frame_width = FRAME_WIDTH
    config.frame_height = FRAME_HEIGHT


# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------


def apply_london_theme(scene):
    """Apply the project's light "london" visual theme to a scene."""
    apply_theme(manim_scene=scene, theme_name="london")


# ---------------------------------------------------------------------------
# Kokoro TTS
# ---------------------------------------------------------------------------

DEFAULT_VOICE = "af_heart"
DEFAULT_LANG = "en-us"
DEFAULT_SPEED = 1.1
DEFAULT_VOLUME = 1.1


def set_kokoro_voice(
    scene, voice=DEFAULT_VOICE, lang=DEFAULT_LANG, speed=DEFAULT_SPEED, volume=DEFAULT_VOLUME, lang_code=None
):
    """Attach the Kokoro TTS service to ``scene`` with the shorts' voice profile.

    Pass ``lang_code`` (instead of ``lang``) for the rare case where only a
    language code is used (see probability.py). Note that when ``lang_code`` is
    set, ``speed`` and ``volume`` are not forwarded (Kokoro's defaults apply) -
    that mirrors probability.py's original call.
    """
    if lang_code is not None:
        scene.set_speech_service(KokoroService(voice=voice, lang_code=lang_code))
    else:
        scene.set_speech_service(KokoroService(voice=voice, lang=lang, speed=speed, volume=volume))


# ---------------------------------------------------------------------------
# Base scenes
# ---------------------------------------------------------------------------


class _ShortBase:
    """Shared voice / layout-zone / goal-derive-resolve behaviour for shorts.

    Not a Scene by itself — mix it into a ``VoiceoverScene`` subclass. It
    applies the london theme and the Kokoro TTS service in ``setup()``.
    """

    # --- voice profile (override per scene) --------------------------------
    VOICE = DEFAULT_VOICE
    LANG = DEFAULT_LANG
    SPEED = DEFAULT_SPEED
    VOLUME = DEFAULT_VOLUME
    LANG_CODE = None  # when set, overrides LANG (passed through to Kokoro)

    # --- vertical layout zones (override per scene) -------------------------
    TOP_Y = 3.2        # pinned goal / title zone
    HERO_Y = 0.3       # hero diagram center
    BOTTOM_Y = -2.6    # active derivation slot
    OLD_Y = None       # where a retiring line parks; None -> BOTTOM_Y + 0.9

    @property
    def top_zone(self):
        return UP * self.TOP_Y

    @property
    def hero_zone(self):
        return UP * self.HERO_Y

    @property
    def active_zone(self):
        return UP * self.BOTTOM_Y

    @property
    def old_zone(self):
        return UP * (self.OLD_Y if self.OLD_Y is not None else self.BOTTOM_Y + 0.9)

    def setup(self):
        super().setup()
        apply_london_theme(self)
        set_kokoro_voice(
            self,
            voice=self.VOICE,
            lang=self.LANG,
            speed=self.SPEED,
            volume=self.VOLUME,
            lang_code=self.LANG_CODE,
        )

    # --- goal ----------------------------------------------------------------

    def make_goal(self, tex, font_size=32, color=RED):
        """Pinned "what we are solving for" formula in the top zone."""
        return MathTex(tex, color=color, font_size=font_size).move_to(self.top_zone)

    def resolve_goal(self, goal, answer, run_time=1.0):
        """Morph the pinned top goal into the final answer."""
        self.play(Transform(goal, answer), run_time=run_time)

    # --- derive ---------------------------------------------------------------

    def play_step(self, new_step, active=None, old=None, extra_anims=(), run_time=1.0, scale=0.75):
        """Write a new derivation line at the active slot.

        - ``active`` (the previous line) slides up to the retired zone, shrinks
          to ``scale`` and fades to 50% opacity.
        - ``old`` (the line before ``active``) fades out entirely.
        - ``extra_anims`` run alongside (e.g. dimming hero annotations).

        In 3D scenes the step is pinned to the screen via
        ``add_fixed_in_frame_mobjects`` so it never rotates with the hero.
        """
        if isinstance(self, ThreeDScene):
            self.add_fixed_in_frame_mobjects(new_step)
        new_step.move_to(self.active_zone)
        anims = list(extra_anims)
        if old is not None:
            anims.append(FadeOut(old))
        if active is not None:
            anims.append(active.animate.move_to(self.old_zone).scale(scale).set_opacity(0.5))
        anims.append(Write(new_step))
        self.play(*anims, run_time=run_time)
        return new_step

    # --- resolve ---------------------------------------------------------------

    def resolve_step(self, step, answer, goal=None, goal_answer=None, fade_out=None, run_time=1.0):
        """Morph the active derivation ``step`` into the final ``answer``.

        Optionally fades ``fade_out`` (the retired line) and/or resolves the
        pinned top ``goal`` into ``goal_answer`` in the same play.
        """
        anims = []
        if fade_out is not None:
            anims.append(FadeOut(fade_out))
        anims.append(Transform(step, answer))
        if goal is not None and goal_answer is not None:
            anims.append(Transform(goal, goal_answer))
        self.play(*anims, run_time=run_time)

    def box_final(self, answer, color=RED, buff=0.15, stroke_width=3, run_time=1.0):
        """Draw a surrounding-rectangle highlight around the final answer."""
        rect = SurroundingRectangle(answer, color=color, buff=buff, stroke_width=stroke_width)
        self.play(Create(rect), run_time=run_time)
        return rect


class ShortScene(_ShortBase, VoiceoverScene, MovingCameraScene):
    """A 2D vertical voiceover short.

    Applies the london theme and the Kokoro TTS service in ``setup()``.
    Override the ``VOICE`` / ``SPEED`` / ... and ``TOP_Y`` / ``HERO_Y`` /
    ``BOTTOM_Y`` class attributes to customise a scene.
    """


class ThreeDShortScene(_ShortBase, ThreeDScene, VoiceoverScene):
    """A 3D vertical voiceover short (same helpers as ShortScene, 3D-aware).

    ``play_step`` pins every new formula to the screen with
    ``add_fixed_in_frame_mobjects``, so derivations stay readable while the
    hero geometry rotates.
    """
