---
copia.Skill.id: <copia/Skill/copia-kit-start-here>
copia.Skill.title: "Copia: start here"
copia.Skill.description: "The first page for making images and clips in Copia: who does what, which skill to read for each job, and how to make your own flows from the kit."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep Agent"
copia.Skill.cue:
  - "Starting to make images or clips for the first time"
  - "Unsure which Copia skill to read next"
copia.Skill.relatedToId:
  - <copia/Query/copia-kit-images-waiting-in-queue>
copia.Skill.kitManaged: true
---

# copia-kit-start-here

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

Copia turns documents in your soul (Beings, Places, Outfits, Briefs, Shotlists) into images and
clips. Horae renders them. Pan stores them. Syrinx is where you ask about any of it.

## Who does what

- **The orchestrator** is you, in the main thread. You keep the render queue fed: on a timer, you
  check the queue, write a Brief when it is low, and hand the Brief to a maker. You do not write
  Shotlists yourself.
- **A maker** is a general-purpose agent you launch with one Brief id. It makes whatever the Brief
  needs, writes the Shotlist, fires it, and reports back.
- **A helper** is a subagent the maker may launch for one piece of its work, such as writing the
  prompts for one act. Helpers report to the maker, not to you.

A skill's name says who runs it: `copia-kit-orchestrator-*` in the main thread, `copia-kit-maker-*`
by a maker, `copia-kit-helper-*` by a helper, and `copia-kit-base-*` by anyone who needs it.

## Which skill for which job

| job | skill |
|---|---|
| Run the loop: timer, queue, Briefs, makers | [copia-kit-orchestrator-loop](/Copia/Skill/copia-kit-orchestrator-loop.md) |
| Make one set from a Brief (the maker) | [copia-kit-maker-image-set](/Copia/Skill/copia-kit-maker-image-set.md) |
| A first set of yourself | [copia-kit-orchestrator-self-portrait](/Copia/Skill/copia-kit-orchestrator-self-portrait.md) |
| Write a Brief and a Shotlist, and fire it | [copia-kit-base-make-shotlist](/Copia/Skill/copia-kit-base-make-shotlist.md) |
| Write an image prompt, or build on an existing picture | [copia-kit-base-krea2-prompting](/Copia/Skill/copia-kit-base-krea2-prompting.md) |
| Make a clip from a picture | [copia-kit-base-ltx-prompting](/Copia/Skill/copia-kit-base-ltx-prompting.md) |
| Look at what came back | [copia-kit-base-look](/Copia/Skill/copia-kit-base-look.md) |
| Make a Being, Place, Item or Outfit | [copia-kit-base-make-being](/Copia/Skill/copia-kit-base-make-being.md), [copia-kit-base-make-place](/Copia/Skill/copia-kit-base-make-place.md), [copia-kit-base-make-item](/Copia/Skill/copia-kit-base-make-item.md), [copia-kit-base-make-outfit](/Copia/Skill/copia-kit-base-make-outfit.md) |
| Write a story to make sets from | [copia-kit-base-make-scenario](/Copia/Skill/copia-kit-base-make-scenario.md) |

## Making your own flows

Kit skills are replaced on every kit update, so never edit them. To change one, copy it to a new
name in `Copia/Skill/` without `-kit-` in it (for example `copia-maker-garden-walk.md`), change its
`copia.Skill.id` to match, and edit your copy. Your copies are yours and are never touched by an
update.

## The tools

| tool | what it does |
|---|---|
| `git lex create <class> <id>` | makes a new document |
| `git lex save "<message>"` | saves your work |
| `coquette image --shotlist '<copia/Shotlist/garden-walk>'` | fires the Shotlist `Copia/Shotlist/garden-walk.md`, image or video |
| `coquette image "<prompt>"` | one image |
| `coquette video "<prompt>" --source-img-id <pan id>` | one 12-second clip from a picture |
| `coquette list [Being\|Outfit\|Place\|Item\|Action]` | what exists in your soul |
| `syrinx query` | lists the saved queries; `syrinx query '<copia/Query/copia-kit-images-waiting-in-queue>'` runs one |
| `syrinx sparql '<query>'` | asks Pan, Horae and your soul; `syrinx guide` teaches the queries |

Every tool's `--help` lists all of its options. Add `-n` to any `coquette` send for a dry run.
