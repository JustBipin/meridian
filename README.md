# Meridian

> Open-source animated learning materials for Nepal's NEB curriculum.

Meridian is a community-driven project that creates educational animations using [**Manim**](https://www.manim.community/).

The goal is to help teachers and students understand concepts visually through clear, engaging animations aligned with the **Nepal National Examination Board (NEB) curriculum**.

🌐 **Project Meridian:** https://projectmeridian.me/

---

## Table of Contents

- [About](#about)
- [Learning Resources](#learning-resources)
- [Curriculum](#curriculum)
- [Source Code](#source-code)
- [Contributing](#contributing)
- [Technology](#technology)
- [License](#license)

---

## About

Traditional textbooks often explain concepts using static diagrams and text.

Meridian uses animation to make abstract ideas easier to understand through:

- Visual explanations of mathematical concepts
- Step-by-step problem solving
- Geometric transformations
- Dynamic graphs and equations

The project is designed for:

- Teachers creating lessons
- Students learning concepts
- Developers contributing educational content

---

## Learning Resources

All completed animations are available on:

🌐 **Project Meridian**
https://projectmeridian.me/

The website provides the learner-facing experience, while this repository contains the source code used to create the animations.

---

## Curriculum

Currently, Meridian focuses on:

- Nepal NEB Curriculum
- Grade 8 Mathematics

More grades and subjects will be added as the project grows.

Detailed curriculum index:

```
docs/
└── curriculum/
    └── grade_8.md
```

---

## Source Code

Animation source files are organized by:

```
Grade → Subject → Chapter → Lesson
```

Example:

```
grade-8/
└── maths/
    └── area/
        └── triangle.py
```

The complete lesson and source code index is available here:

[Grade 8 Mathematics Curriculum](./docs/curriculum/grade_8.md)

---

## Contributing

Meridian welcomes contributions from:

- Teachers
- Students
- Developers
- Educational content creators

You can contribute by:

- Creating new animations
- Improving existing lessons
- Fixing issues
- Improving documentation

See:

[CONTRIBUTING.md](./CONTRIBUTING.md)

---

## Technology

Built using:

- Python
- Manim Community
- uv
- Ruff

---

## License

See [LICENSE](./LICENSE).
