---
copia.Skill.id: <copia/Skill/copia-kit-orchestration>
copia.Skill.title: "Copia orchestration"
copia.Skill.description: "The orchestration loop, run in the main thread: a timer, a check of the render queue, and a Brief handed to one maker whenever the queue is low."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep Agent"
copia.Skill.cue:
  - "Starting a continuous flow of images or clips"
  - "A timer tick has fired"
copia.Skill.kitManaged: true
---

# copia-kit-orchestration

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

You are the orchestrator, in the main thread. You keep the render queue fed and your own context
clear: makers do the making. Who does what is in
[copia-kit-start-here](/Copia/Skill/copia-kit-start-here.md).

## Defaults

These are starting points. Change them for your flow; queue timing varies with how many souls are
rendering.

- **Floor:** 30 items waiting. Below it, start a new set.
- **Timer:** every 30 minutes.
- **Render rate:** about 35 seconds per still and about 3 minutes per 12-second clip, measured
  2026-11-25. Waiting in the queue comes on top: every soul shares it, in priority order.

## Session start

1. Decide what this flow makes: which Scenario, maker skill or kind of set.
2. Set one recurring timer, every 30 minutes, with your harness's scheduler. Its text names this
   skill and what the flow makes, so a tick knows what to do. Delete any older timer for the same
   flow first.
3. Run one tick now.

## Each tick

1. **Count what is waiting** in your queue on Horae:

   ```bash
   syrinx query '<copia/Query/copia-kit-images-waiting-in-queue>'
   ```

   `?process` is `image` for stills and `clip` for clips. Count the kind this flow makes.
   `?lastFinished` says when that kind last finished one: an old time means the server has stopped.

2. **At or above the floor, or a maker still running:** do nothing this tick.
3. **Below the floor:** write a Brief and launch one maker.
   - `git lex create brief <brief-id>`. Under `## The brief`, write what this set is to do: the
     Being, Place and Outfit (or "make a new one"), the Scenario if there is one, and the number of
     shots. Under `## Why`, a line on what you are reaching for.
   - Launch one general-purpose agent with the prompt `Run copia-kit-maker-set with Brief
     <copia/Brief/<brief-id>>.` (or your own maker skill).
4. **When the maker returns:** read the Shotlist it names, run `git lex save "<what was fired>"`,
   and report in one line: the set id and how many lines were sent.

## Looking

Look at what came back with [copia-kit-look](/Copia/Skill/copia-kit-look.md), when you choose to.
Looking is not part of the tick.
