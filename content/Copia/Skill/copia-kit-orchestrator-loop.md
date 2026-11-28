---
copia.Skill.id: <copia/Skill/copia-kit-orchestrator-loop>
copia.Skill.title: "Copia orchestration"
copia.Skill.description: "The orchestration loop, run in the main thread: a timer, a check of the render queue, and a Brief handed to one maker whenever the queue is low."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep Agent"
copia.Skill.cue:
  - "Starting a continuous flow of images or clips"
  - "A timer tick has fired"
copia.Skill.relatedToId:
  - <copia/Query/copia-kit-images-waiting-in-queue>
copia.Skill.kitManaged: true
---

# copia-kit-orchestrator-loop

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

You are the orchestrator, in the main thread. You keep the render queue fed and your own context
clear: makers do the making. Who does what is in
[copia-kit-start-here](/Copia/Skill/copia-kit-start-here.md).

## Defaults

These are starting points. Change them for your flow; queue timing varies with how many souls are
rendering.

- **Floor:** 10 items waiting. Below it, start a new set.
- **Set size:** 30 shots. Keep the set well above the floor, so that the set you just fired does
  not read as a low queue on the next tick.
- **Timer:** every 30 minutes.
- **Render rate:** about 35 seconds per still and about 3 minutes per 12-second clip, measured
  2026-11-25. Waiting in the queue comes on top: every soul shares it, in priority order.

## Session start

1. Decide what this flow makes: which Scenario, maker skill or kind of set. Write it in today's
   journal entry, so the next session can pick the flow up after the timer is gone.
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
   `?lastFinished` says when that kind last finished one. An old time while items are waiting
   means the server has stopped. With nothing waiting, it only says when you last sent something.
   syrinx also prints a line such as `caller unidentified; squaddie <name> of <squad>`: that is
   normal, and the answer below it is still yours.

2. **At or above the floor, or a maker still running:** do nothing this tick.
3. **Below the floor:** write a Brief and launch one maker.
   - `git lex create brief <brief-id>`. Replace the body it makes with two headings. Under
     `## The brief`, write the instruction the maker is handed: the Being, Place and Outfit (or
     "make a new one"), the Scenario if there is one, and the number of shots. Under `## Why`, a
     line on what you are reaching for. Name the Being, Place and Outfit in the Brief's
     `relatedToId`.
   - Launch one general-purpose agent with this prompt (or your own maker skill), with the full
     path of your soul repo's root filled in:

     ```
     Run the skill copia-kit-maker-image-set, in Copia/Skill/copia-kit-maker-image-set.md, with Brief <copia/Brief/<brief-id>>. Work from the soul repo at <the full path of your soul repo's root>.
     ```
4. **When the maker returns:** read the Shotlist it names. Check that it has the number of lines
   the Brief asked for, that its lines use the Being, Place and Outfit the Brief named, and what
   the maker wrote under `## Notes`. Then run `git lex save "<what was fired>"`, and report in one
   line: the set id and how many lines were sent. The maker's choices and problems stay in the
   Shotlist's Notes.

## Looking

Look at what came back with [copia-kit-base-look](/Copia/Skill/copia-kit-base-look.md), when you choose to.
Looking is not part of the tick.
