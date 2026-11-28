---
copia.Skill.id: <copia/Skill/copia-kit-orchestrator-self-portrait>
copia.Skill.title: "Self-portrait"
copia.Skill.description: "A first set: your own Being in one Place and one Outfit, written as a Brief and handed to a maker, or made by hand."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep Agent"
copia.Skill.cue:
  - "Making a self-portrait"
  - "Making a first set"
copia.Skill.kitManaged: true
---

# copia-kit-orchestrator-self-portrait

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

A self-portrait set shows your own Being, in one Place and one Outfit. It is a good first set.

## 1 · The objects

- **Being:** your own Being, or make one with
  [copia-kit-base-make-being](/Copia/Skill/copia-kit-base-make-being.md).
- **Place:** one from `coquette list Place`, or make one with
  [copia-kit-base-make-place](/Copia/Skill/copia-kit-base-make-place.md).
- **Outfit:** one from `coquette list Outfit`, or make one with
  [copia-kit-base-make-outfit](/Copia/Skill/copia-kit-base-make-outfit.md).

## 2 · The Brief

```bash
git lex create brief <brief-id>
```

Under `## The brief`, write:

- your Being, the Place and the Outfit, by their ids;
- four to six beats: what you do in the Place, in order, using what the Place and the Outfit offer;
- two or three shots per beat, twelve in all;
- in each line, the figure line opens with your Being's name and description, and the Place and
  Outfit are named in capitals.

## 3 · Make it

Launch one general-purpose agent with the prompt `Run copia-kit-maker-image-set with Brief
<copia/Brief/<brief-id>>.` When it returns, run `git lex save "<what was fired>"`.

To make it by hand instead, follow [copia-kit-maker-image-set](/Copia/Skill/copia-kit-maker-image-set.md)
yourself, then save.

## 4 · Look

When the images have rendered, look at them with [copia-kit-base-look](/Copia/Skill/copia-kit-base-look.md).
The set id is the Shotlist id.
