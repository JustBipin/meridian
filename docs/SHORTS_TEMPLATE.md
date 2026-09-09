# Shorts Template

A reusable scaffold for the project's **vertical 9:16 voiceover "shorts"** — the
fast, narrated animations living at the repository root (`pi.py`,
`circle_short.py`, `helix_new.py`, `area_short.py`, the triangle shorts,
`probability.py`, ...).

It centralises the conventions those files shared:

- the vertical **1080×1920 (9:16)** render config
- the light **"london"** theme
- **Kokoro TTS** setup with a consistent default voice profile
- named **vertical layout zones** (top / hero / active derivation / retired)
- **goal → derive → resolve** helpers
- a **final-answer highlight** helper

See also [`ANIMATION_STYLE.md`](./ANIMATION_STYLE.md) for the general style
guide this template follows.

---

## Quick start

```python
from manim import *
from shorts_template import ShortScene, apply_vertical_config

apply_vertical_config()  # module level, before the scene is instantiated

class MyShort(ShortScene):
    SPEED = 1.15        # optional voice tweaks (defaults: af_heart @ 1.1)
    TOP_Y = 3.2         # optional zone overrides (defaults shown below)

    def construct(self):
        with self.voiceover(text="Here is the plan.") as tracker:
            self.play(Create(something), run_time=tracker.duration)
```

Render it like any other short:

```bash
uv run manim render -q my_short.py MyShort
```

---

## Vertical config

| Constant     | Value  |
| ------------ | ------ |
| `PIXEL_WIDTH`  | 1080 |
| `PIXEL_HEIGHT` | 1920 |
| `FRAME_WIDTH`  | 9.0  |
| `FRAME_HEIGHT` | 16.0 |

Call `apply_vertical_config()` **at module level** — right where the old
`config.pixel_width = ...` lines used to live — because the canvas is fixed
when Manim instantiates the scene.

> **Note for 3D shorts:** `ThreeDShortScene` behaves like the original
> `ThreeDScene` scenes and was validated on the default (Cairo) renderer.
> The project installs `manim[opengl]`; if you ever render with
> `--renderer=opengl`, the fixed-in-frame / camera behaviour can differ and
> the template has not been validated there.

---

## Voice (Kokoro TTS)

`ShortScene` / `ThreeDShortScene` attach the speech service automatically in
`setup()`. Default profile:

```python
VOICE = "af_heart"
LANG = "en-us"
SPEED = 1.1
VOLUME = 1.1
```

Override any of them as class attributes:

```python
class PiIntroduction(ShortScene):
    VOICE = "af_sarah"
    SPEED = 0.95
    VOLUME = 1.1
```

`LANG_CODE` overrides `LANG` for the rare case that only a language code is
used (see `probability.py`):

```python
class ConditionalProbability(ShortScene):
    LANG_CODE = "a"
```

If you need the service outside the base classes (e.g. an experimental scene
that keeps its own `setup`), call the module-level helper directly:

```python
from shorts_template import set_kokoro_voice

set_kokoro_voice(self, speed=1.05)
```

Narrations always follow the existing pattern:

```python
with self.voiceover(text="Here is the plan.") as tracker:
    self.play(..., run_time=tracker.duration)
```

Use fractions of `tracker.duration` (`* 0.4`, `* 0.6`, ...) when one narration
spans several `self.play` calls.

---

## Layout zones

Shorts lay the frame out vertically. The base classes provide the named zones:

| Attribute | Default | Meaning |
| --------- | ------- | ------- |
| `TOP_Y`    | `3.2`   | pinned goal / title zone |
| `HERO_Y`   | `0.3`   | hero diagram center |
| `BOTTOM_Y` | `-2.6`  | active derivation slot |
| `OLD_Y`    | `None`  | retired line parking spot (`BOTTOM_Y + 0.9` when `None`) |

Access them as vectors via the properties `top_zone`, `hero_zone`,
`active_zone`, `old_zone` — e.g. `self.top_zone` is `UP * 3.2` = `[0, 3.2, 0]`.

Override them per scene:

```python
class CircleArcLength(ShortScene):
    TOP_Y = 6.5
    HERO_Y = 0.5
    BOTTOM_Y = -1.0
```

If a scene needs a different geometry (e.g. the triangle shorts' local
`TOP_ZONE` / `MID_ZONE` / `BOT_ZONE`), it can simply keep its own constants —
the properties are a convenience, not a requirement.

---

## Goal → derive → resolve

The canonical short tells a three-act story:

1. **Goal** — pin the unknown at the top (`L = ?`).
2. **Derive** — write the derivation one line at a time in the active slot.
3. **Resolve** — morph the active line into the boxed answer, and resolve the
   goal.

### `make_goal(tex, font_size=32, color=RED)`

Pinned "what we are solving for" formula in the top zone.

```python
goal = self.make_goal(r"L = \,?")
```

### `resolve_goal(goal, answer, run_time=1.0)`

Morph the pinned top goal into the final answer.

```python
self.resolve_goal(goal, answer_top)
```

### `play_step(new_step, active=None, old=None, extra_anims=(), run_time=1.0, scale=0.75)`

Writes `new_step` at the active slot while:

- `active` (the previous line) slides up to `old_zone`, shrinks to `scale` and
  fades to 50% opacity;
- `old` (the line before `active`) fades out entirely;
- `extra_anims` play alongside (e.g. dimming hero annotations).

```python
step1 = MathTex(r"L = \int d\ell", font_size=30)
self.play_step(step1, run_time=tracker.duration)

step2 = MathTex(r"d\ell = |\vec{v}|\, dt", font_size=30)
self.play_step(step2, active=step1, run_time=tracker.duration)

step3 = MathTex(r"|\vec{v}| = |\vec{r}\,'(t)|", font_size=30)
self.play_step(step3, active=step2, old=step1, run_time=tracker.duration)
```

The old "manual" equivalent of the `step3` call:

```python
self.add_fixed_in_frame_mobjects(step3)  # 3D scenes only
step3.move_to([0, BOTTOM_Y, 0])
self.play(FadeOut(step1), step2.animate.move_to([0, OLD_Y, 0]).scale(0.75).set_opacity(0.5), Write(step3))
```

In 3D scenes `play_step` pins every new formula to the screen with
`add_fixed_in_frame_mobjects` automatically, so derivations stay readable
while the hero rotates.

### `resolve_step(step, answer, goal=None, goal_answer=None, fade_out=None, run_time=1.0)`

Morph the active derivation `step` into the final `answer`; optionally fades
`fade_out` (the retired line) and/or resolves the top `goal` in the same play.

```python
self.resolve_step(step7, answer, goal=goal, goal_answer=answer_top, fade_out=step6, run_time=tracker.duration)
```

### `box_final(answer, color=RED, buff=0.15, stroke_width=3, run_time=1.0)`

Draws the classic `SurroundingRectangle` highlight around the final answer.

```python
self.box_final(final_answer, color=RED_MAIN)
```

---

## Base classes

| Class | Bases | Use for |
| ----- | ----- | ------- |
| `ShortScene` | `VoiceoverScene, MovingCameraScene` | 2D vertical voiceover shorts |
| `ThreeDShortScene` | `ThreeDScene, VoiceoverScene` | 3D vertical voiceover shorts |

Both apply the london theme and the Kokoro TTS service in `setup()`, and expose
the layout zones and goal/derive/resolve helpers above.

---

## Full example

```python
from manim import *
from shorts_template import ShortScene, apply_vertical_config

apply_vertical_config()


class MyShort(ShortScene):
    TOP_Y = 4.0
    HERO_Y = 0.5
    BOTTOM_Y = -2.0
    OLD_Y = -1.2

    def construct(self):
        goal = self.make_goal(r"L = \,?")

        with self.voiceover(text="Let's find the length of this arc.") as tracker:
            self.play(Write(goal), run_time=tracker.duration)

        hero = Arc(radius=2, angle=TAU / 3, color=BLUE, stroke_width=6).move_to(self.hero_zone)

        with self.voiceover(text="Here is the arc.") as tracker:
            self.play(Create(hero), run_time=tracker.duration)

        step1 = MathTex(r"L = \int ds", font_size=32)
        with self.voiceover(text="Length is the integral of a tiny piece d s.") as tracker:
            self.play_step(step1, run_time=tracker.duration)

        step2 = MathTex(r"L = 2\pi R \cdot \frac{1}{3}", font_size=32)
        with self.voiceover(text="One third of a full circle gives us the answer.") as tracker:
            self.play_step(step2, active=step1, run_time=tracker.duration)

        answer = MathTex(r"L = \frac{2\pi R}{3}", color=RED, font_size=36)
        with self.voiceover(text="Length equals two pi R over three.") as tracker:
            self.resolve_step(step2, answer, goal=goal, goal_answer=answer.copy(), run_time=tracker.duration)

        self.box_final(answer, color=RED)
        self.wait(1)
```

---

## Migration notes

The root shorts now use the template as follows:

| File | Base class | Voice overrides | Config |
| ---- | ---------- | --------------- | ------ |
| `pi.py` | `ShortScene` | `af_sarah`, speed 0.95 | — |
| `pi_shorts.py` | `ShortScene` | speed 1.05 | — |
| `circle_short.py` | `ShortScene` | speed 1.2 | `apply_vertical_config()` |
| `general_triangle_short.py` | `ShortScene` | defaults | — |
| `equilateral_short.py` | `ShortScene` | speed 1.15, volume 1.0 | — |
| `equilateral_short_imp.py` | `ShortScene` | speed 1.15, volume 1.0 | — |
| `isosceles_triangle_short.py` | `ShortScene` | speed 1.15 | — |
| `probability.py` | `ShortScene` | `LANG_CODE = "a"` | `apply_vertical_config()` |
| `helix_new.py` | `ThreeDShortScene` | defaults | `apply_vertical_config()` |
| `area_short.py` | `ThreeDShortScene` | defaults | `apply_vertical_config()` |
| `helix.py` | (kept `ThreeDScene`) | uses `set_kokoro_voice(self, speed=1.05)` | — |

Two small intentional fixes were applied while migrating:

1. `helix_new.py` previously set `pixel_height` / frame size but **not**
   `pixel_width`, which would render a square 1920×1920 canvas. It now uses the
   standard 1080×1920 vertical config.
2. `area_short.py` documented itself as "vertical 9:16 frame" but set no
   config at all; it now uses `apply_vertical_config()`.

`helix.py` is a divergent experimental variant (dark background, bespoke panel
system, theme intentionally disabled) and was left on `ThreeDScene` — it only
reuses the voice helper.

---

## Checklist for a new short

- [ ] `apply_vertical_config()` at module level (unless deliberately not 9:16)
- [ ] Inherit `ShortScene` (2D) or `ThreeDShortScene` (3D)
- [ ] Override `VOICE` / `SPEED` / `VOLUME` only when different from defaults
- [ ] Override `TOP_Y` / `HERO_Y` / `BOTTOM_Y` / `OLD_Y` for the layout
- [ ] Wrap narration in `with self.voiceover(...) as tracker:` and time plays
      with `tracker.duration`
- [ ] Use `make_goal` → `play_step` → `resolve_step` for the derive chain
- [ ] End with `box_final(...)` or an equivalent highlight
- [ ] Passes `ruff check`
