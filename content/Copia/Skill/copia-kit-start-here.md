---
copia.Skill.id: <copia/Skill/copia-kit-start-here>
copia.Skill.title: "Copia: start here"
copia.Skill.description: "The first page for making images and clips in Copia: who does what, which skill to read for each job, and how to make your own flows from the kit."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep Agent"
copia.Skill.cue:
  - "Starting to make images or clips for the first time"
  - "Unsure which Copia skill to read next"
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

## Which skill for which job

| job | skill |
|---|---|
| Run the loop: timer, queue, Briefs, makers | [copia-kit-orchestration](/Copia/Skill/copia-kit-orchestration.md) |
| Make one set from a Brief (the maker) | [copia-kit-maker-set](/Copia/Skill/copia-kit-maker-set.md) |
| A first set of yourself | [copia-kit-self-portrait](/Copia/Skill/copia-kit-self-portrait.md) |
| Write a Brief and a Shotlist, and fire it | [copia-kit-make-shotlist](/Copia/Skill/copia-kit-make-shotlist.md) |
| Write an image prompt, or build on an existing picture | [copia-kit-krea2-prompting](/Copia/Skill/copia-kit-krea2-prompting.md) |
| Make a clip from a picture | [copia-kit-ltx-prompting](/Copia/Skill/copia-kit-ltx-prompting.md) |
| Look at what came back | [copia-kit-look](/Copia/Skill/copia-kit-look.md) |
| Make a Being, Place, Item or Outfit | [copia-kit-make-being](/Copia/Skill/copia-kit-make-being.md), [copia-kit-make-place](/Copia/Skill/copia-kit-make-place.md), [copia-kit-make-item](/Copia/Skill/copia-kit-make-item.md), [copia-kit-make-outfit](/Copia/Skill/copia-kit-make-outfit.md) |
| Write a story to make sets from | [copia-kit-make-scenario](/Copia/Skill/copia-kit-make-scenario.md) |

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
| `coquette image --shotlist '<copia/Shotlist/<id>>'` | fires a Shotlist, image or video |
| `coquette image "<prompt>"` | one image |
| `coquette video "<prompt>" --source-img-id <pan id>` | one 12-second clip from a picture |
| `coquette list [Being\|Outfit\|Place\|Item\|Action]` | what exists in your soul |
| `syrinx query` | lists the saved queries; `syrinx query '<copia/Query/copia-kit-images-waiting-in-queue>'` runs one |
| `syrinx sparql '<query>'` | asks Pan, Horae and your soul; `syrinx guide` teaches the queries |

Every tool's `--help` lists all of its options. Add `-n` to any `coquette` send for a dry run.
