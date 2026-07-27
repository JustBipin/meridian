# Contributing to Plot

Thank you for helping build open-source educational materials for Nepal's NEB curriculum.

Whether you are a teacher, student, animator, or developer, your contribution can help make learning more visual and accessible.

---

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Creating Animations](#creating-animations)
- [Animation Guidelines](#animation-guidelines)
- [Code Style](#code-style)
- [Contribution Workflow](#contribution-workflow)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Types of Contributions](#types-of-contributions)

---

## Development Setup

### Requirements

- Python 3.12+
- uv

Clone the repository:

```bash
git clone https://github.com/<your-username>/plot.git
cd plot
```

Install dependencies:

```bash
uv sync
```

---

## Project Structure

Animations follow this structure:

```
grade/
└── subject/
    └── chapter/
        └── lesson.py
```

Example:

```
grade-8/
└── maths/
    └── area/
        └── triangle.py
```

Keep animations organized according to:

```
Grade → Subject → Chapter → Lesson
```

---

## Creating Animations

When adding a new lesson:

1. Place it in the correct curriculum location.
2. Use meaningful file and scene names.
3. Keep explanations suitable for students.
4. Follow the animation style guidelines.
5. Test the animation before submitting.

Example render:

```bash
uv run manim path/to/file.py SceneName
```

Preview:

```bash
uv run manim -pql path/to/file.py SceneName
```

---

## Animation Guidelines

All animations should follow the conventions described in:

[ANIMATION_STYLE.md](./docs/ANIMATION_STYLE.md)

Important guidelines include:

- Use a consistent light theme.
- Avoid low-contrast colors.
- Save the camera frame state at the start of scenes.
- Keep narration text at the bottom of the frame.
- Place formulas and derivations on the left side.
- Keep visual demonstrations clear and focused.
- Use animations to explain concepts, not as decoration.

---

## Code Style

This project uses Ruff.

Check code:

```bash
uv run ruff check .
```

Fix automatically:

```bash
uv run ruff check . --fix
```

Keep code:

- Readable
- Consistent
- Easy for other contributors to modify

---

## Contribution Workflow

Create a branch:

```bash
git checkout -b add-new-lesson
```

Make your changes.

Check your code:

```bash
uv run ruff check .
```

Render and test your animation:

```bash
uv run manim path/to/file.py SceneName
```

Commit:

```bash
git add .
git commit -m "Add Grade 8 geometry animation"
```

Push:

```bash
git push origin add-new-lesson
```

Open a Pull Request.

---

## Pull Request Guidelines

A good pull request should:

- Explain what was added or changed.
- Reference the related curriculum topic.
- Follow `ANIMATION_STYLE.md`.
- Include screenshots or rendered examples when possible.
- Keep changes focused.

---

## Types of Contributions

You can contribute by:

### Educational Content

- Adding new lessons
- Improving explanations
- Creating new animations
- Suggesting curriculum improvements

### Development

- Improving animation code
- Fixing bugs
- Improving project structure
- Creating reusable components

### Documentation

- Improving guides
- Adding examples
- Fixing mistakes

---

Thank you for helping create better visual learning resources.