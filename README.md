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

**Read this course at:** [https://siliconwit.com/education/planar-mechanics/](https://siliconwit.com/education/planar-mechanics/)

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

All commands below work on Linux, macOS, and Windows (using Git Bash, PowerShell, or Command Prompt with Git installed).

### For Team Members (with push access)

**First time setup (clone the repo once):**

```bash
git clone https://github.com/SiliconWit/planar-mechanics.git
cd planar-mechanics
```

**Every time you start working:**

```bash
git pull origin main
```

Always pull before making changes. This avoids conflicts with other contributors.

**After making your changes:**

```bash
git add .
git commit -m "Brief description of what you changed"
git push origin main
```

**If you get a push error** (someone pushed before you):

```bash
git pull origin main
```

Git will merge the changes automatically in most cases. If there is a conflict, Git will mark the conflicting lines in the file. Open the file, choose which version to keep, then:

```bash
git add .
git commit -m "Resolve merge conflict"
git push origin main
```

**Tips to avoid conflicts:**

- Always `git pull origin main` before you start working
- Push your changes as soon as you are done, do not hold onto uncommitted work for long
- Coordinate with other contributors so two people are not editing the same file at the same time

### For External Contributors (without push access)

1. Fork the repository: [SiliconWit/planar-mechanics](https://github.com/SiliconWit/planar-mechanics)
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/planar-mechanics.git
   cd planar-mechanics
   ```
3. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Brief description of what you changed"
   git push origin main
   ```
4. Open a Pull Request against `main` on the original repository
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
