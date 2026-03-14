---
title: "Planar Mechanics - Collaboration Guide"
description: "Contributing guide for Planar Mechanics course content"
tableOfContents: true
sidebar:
  order: 999
---

# Planar Mechanics

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Contributors Welcome](https://img.shields.io/badge/contributors-welcome-orange)

A course on kinematic and dynamic analysis of planar mechanisms for mechatronic systems. Covers joint types and constraint analysis, position analysis of linkages, velocity analysis with instantaneous centers, acceleration and dynamic forces, cam-follower systems, and force analysis with mechanism synthesis.

## Lessons

| # | Title |
|---|-------|
| 1 | Kinematic Joints and Constraint Analysis |
| 2 | Position Analysis of Planar Linkages |
| 3 | Velocity Analysis and Instantaneous Centers |
| 4 | Acceleration Analysis and Dynamic Forces |
| 5 | Cam-Follower Systems and Motion Programming |
| 6 | Force Analysis and Mechanism Synthesis |

## File Structure

```
planar-mechanics/
├── index.mdx
├── kinematic-joints-constraint-analysis.mdx
├── position-analysis-planar-linkages.mdx
├── velocity-analysis-instantaneous-centers.mdx
├── acceleration-analysis-dynamic-forces.mdx
├── cam-follower-systems-motion-programming.mdx
├── force-analysis-mechanism-synthesis.mdx
└── README.md
```

## How to Contribute

1. Fork the repository: [SiliconWit/planar-mechanics](https://github.com/SiliconWit/planar-mechanics)
2. Create a feature branch: `git checkout -b feature/your-topic`
3. Make your changes and commit with a clear message
4. Push to your fork and open a Pull Request against `main`
5. Describe what you changed and why in the PR description

## Content Standards

- All lesson files use `.mdx` format
- `<BionicText>` may be used in later content sections but not in lesson intro paragraphs
- Code blocks should include a title attribute:
  ````mdx
  ```python title="linkage_position.py"
  import numpy as np
  theta3 = np.arctan2(B_y, B_x)
  ```
  ````
- Use Starlight components (`<Tabs>`, `<TabItem>`, `<Steps>`, `<Card>`) where appropriate
- Keep paragraphs concise and focused on practical application
- Include working Python examples that readers can run directly
- Mathematical notation uses LaTeX in MDX

## Local Development

Clone the main site repository and initialize submodules:

```bash
git clone --recurse-submodules <main-repo-url>
cd siliconwit-com
npm install
npm run dev
```

To test a production build:

```bash
npm run build
```

## License

This course content is released under the [MIT License](LICENSE).
