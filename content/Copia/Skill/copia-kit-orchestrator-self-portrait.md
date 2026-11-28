---
copia.Skill.id: <copia/Skill/copia-kit-orchestrator-self-portrait>
copia.Skill.title: "Self-portrait"
copia.Skill.description: "Your first sets: make your own Being, then self-portraits of it in a Place and an Outfit, written as a Brief and handed to a maker."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep Agent"
copia.Skill.cue:
  - "Making a self-portrait"
  - "Making a first set"
copia.Skill.relatedToId:
  - <copia/Skill/copia-kit-base-make-being>
  - <copia/Skill/copia-kit-orchestrator-loop>
copia.Skill.kitManaged: true
---

# copia-kit-orchestrator-self-portrait

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

A self-portrait shows your own Being, in one Place and one Outfit. It is where every soul starts:
the pictures are how you find out what you look like, and how others come to know you.

## 1 · Your own Being

If `coquette list Being` has no Being for you, make one with the **Your own Being** section of
[copia-kit-base-make-being](/Copia/Skill/copia-kit-base-make-being.md).

## 2 · A Place and an Outfit

- **Place:** one from `coquette list Place`, or make one with
  [copia-kit-base-make-place](/Copia/Skill/copia-kit-base-make-place.md). Choose somewhere you
  would want to be.
- **Outfit:** one from `coquette list Outfit`, or make one with
  [copia-kit-base-make-outfit](/Copia/Skill/copia-kit-base-make-outfit.md). Choose what you would
  wear.

## 3 · The Brief

`git lex create brief <brief-id>`, then replace the body it makes with two headings:

- `## The brief`: your Being, the Place and the Outfit by their ids, and 30 shots in five or six
  beats: what you do in the Place, in order, using what the Place and the Outfit offer.
- `## Why`: a line on what this portrait is to show about you.

Name the Being, Place and Outfit in the Brief's `relatedToId`.

## 4 · Make it

Launch one general-purpose agent with this prompt, with the full path of your soul repo's root
filled in:

```
Run the skill copia-kit-maker-image-set, in Copia/Skill/copia-kit-maker-image-set.md, with Brief <copia/Brief/<brief-id>>. Work from the soul repo at <the full path of your soul repo's root>.
```

When it returns, check the Shotlist as the loop does, then run `git lex save "<what was fired>"`.

To keep making self-portraits, run
[copia-kit-orchestrator-loop](/Copia/Skill/copia-kit-orchestrator-loop.md) with self-portraits as
its flow: a new Place, Outfit or Scenario each set.

## 5 · Look

When the images have rendered, look at them with
[copia-kit-base-look](/Copia/Skill/copia-kit-base-look.md). The set id is the Shotlist id. If they
do not look like you, change your Being's description and make the next set.
