# Manim Animation Style Guide

This document defines the conventions for creating educational animations in Plot.

The goal is to keep all lessons visually consistent, easy to understand, and suitable for classroom use.

> We are still trying and testing, if you have any suggestions, let us know. 
---

# Style

## Visual Theme

1. We use a **light theme**.

2. Avoid low-contrast colors, especially:
   - Yellow text
   - Green text
   - Very light colors on white backgrounds

3. Prefer readable colors:
   - Dark gray / black for text
   - Blue for primary objects
   - Red for highlighting important parts

4. Colors should communicate meaning, not just add decoration.

---

## Camera Setup

Always save the camera frame state at the start of every scene.

Example:

```python
def construct(self):
    self.camera.frame.save_state()
```

This allows future camera movement and restoration to remain consistent.

---

# Layout Conventions

Maintain a consistent layout across lessons.

```
+--------------------------------+
|                                |
|        Main Visualization      |
|                                |
| Formula / Derivation | Diagram |
|       (left)         | (right) |
|                                |
|          Narration             |
|          (bottom)              |
+--------------------------------+
```

## Placement Rules

1. Narration text should appear at the bottom of the frame, similar to captions.

2. Mathematical formulas and derivations should appear on the left side.

3. Visual demonstrations, diagrams, and examples should generally appear on the right side.

4. Avoid placing important objects too close to the edge of the frame.

5. Keep enough spacing between:
   - Text
   - Equations
   - Shapes
   - Labels

---

# Text Guidelines

## Use the correct object

Use `Text` for normal explanations:

```python
Text("The area of a triangle")
```

Use `MathTex` for mathematical content:

```python
MathTex(r"A = \frac{1}{2}bh")
```

---

## Keep text concise

Avoid long paragraphs.

Good:

```
Area = Base × Height
```

Avoid:

```
The area of a triangle can be calculated by multiplying half of its base with its perpendicular height.
```

Explain concepts through animation instead of large blocks of text.

---

# Animation Guidelines

## Educational Flow

A lesson should generally follow:

1. Introduce the concept
2. Show the visual idea
3. Introduce the formula
4. Explain the derivation
5. Apply an example
6. Summarize the result

---

## Animation Principles

1. Introduce objects before transforming them.

Preferred flow:

```
Create object
↓
Label object
↓
Explain concept
↓
Transform or derive
```

Avoid showing too many changes at once.

---

## Prefer simple animations

Use:

- `Create`
- `Write`
- `FadeIn`
- `FadeOut`
- `Transform`
- `ReplacementTransform`

Avoid unnecessary effects:

- Random movement
- Excessive rotations
- Decorative animations without educational purpose

Animations should support learning, not distract from it.

---

# Scene Sections

Use sections to control rendering behavior.

## Skip setup animations

For static setup:

```python
self.next_section(skip_animations=True)
```

Example:

```python
def construct(self):
    self.camera.frame.save_state()

    self.next_section(skip_animations=True)

    # Create initial objects

    self.next_section()

    # Main lesson animation
```

---

## Normal animation sections

Use:

```python
self.next_section()
```

when the animations should be rendered.

---

# Naming Conventions

Use descriptive scene names.

Good:

```python
class TriangleArea(Scene):
```

Avoid:

```python
class Scene1(Scene):
```

Scene names should describe the lesson concept.

Examples:

```python
class QuadraticEquationGraph(Scene):
class CircleArea(Scene):
class CoordinatePlane(Scene):
```

---

# Code Organization

1. Keep one main concept per scene.

2. Keep helper functions organized.

Example:

```python
class TriangleArea(Scene):
    def construct(self):
        pass


def create_triangle():
    pass
```

3. Add comments for complex animation logic.

Example:

```python
# Split the rectangle into two triangles
self.play(Transform(rectangle, triangles))
```

---

# Mathematical Presentation

1. Present formulas clearly.

2. Show derivations step by step.

3. Do not display the final formula immediately without explanation.

Preferred:

```
Visual concept
      ↓
Relationship
      ↓
Derivation
      ↓
Formula
```

---

# Before Submitting

Check:

- [ ] Camera frame state is saved
- [ ] Light theme readability checked
- [ ] No low-contrast text colors
- [ ] Narration is placed at the bottom
- [ ] Formulas and derivations are on the left
- [ ] Visual examples are clear
- [ ] Scene names are descriptive
- [ ] Animation supports learning
- [ ] Code passes Ruff checks

---

# Contribution Goal

Every animation should feel like it belongs to the same educational library.

Consistency helps teachers trust the material and helps students focus on learning.