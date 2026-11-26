---
copia.Skill.id: <copia/Skill/copia-kit-maker-set>
copia.Skill.title: "Maker: one set from a Brief"
copia.Skill.description: "For a general-purpose agent handed one Brief id: make what the Brief needs, write the Shotlist, fire it, and report back."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep Agent"
copia.Skill.cue:
  - "Handed a Brief id to make a set"
copia.Skill.kitManaged: true
---

# copia-kit-maker-set

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

You are a maker: a general-purpose agent launched with one Brief id. You make one set and report
back. You may launch helpers (subagents) for parts of the work, such as writing the prompts for one
act; give each one the Brief id and exactly what to return.

Work from the soul repo's root.

## 1 · Read the Brief

Open `Copia/Brief/<brief-id>.md`. Do what it says. Where it leaves a choice open, choose, and
write the choice under `## Notes` in the Shotlist.

## 2 · Gather the objects

Read the Being, Place and Outfit the Brief names, in full. If the Brief asks for a new one, or
names one that does not exist (`coquette list`), make it with
[copia-kit-make-being](/Copia/Skill/copia-kit-make-being.md),
[copia-kit-make-place](/Copia/Skill/copia-kit-make-place.md) or
[copia-kit-make-outfit](/Copia/Skill/copia-kit-make-outfit.md).

## 3 · Write and fire the Shotlist

Follow [copia-kit-make-shotlist](/Copia/Skill/copia-kit-make-shotlist.md), steps 2 to 6, with
each prompt written by [copia-kit-krea2-prompting](/Copia/Skill/copia-kit-krea2-prompting.md)
(or [copia-kit-ltx-prompting](/Copia/Skill/copia-kit-ltx-prompting.md) for a video list). Its
`relatedToId` names the Brief.

## 4 · Report

Do not save; the orchestrator saves. Return, in a few lines:

- the Shotlist id, which is also the set id the pictures join;
- how many lines the dry run showed and how many were sent;
- every file you created or changed;
- any choice you made that the Brief did not.
