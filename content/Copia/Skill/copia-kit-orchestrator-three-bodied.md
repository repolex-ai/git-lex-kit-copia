---
copia.Skill.id: <copia/Skill/copia-kit-orchestrator-three-bodied>
copia.Skill.title: "Three-bodied artmaking"
copia.Skill.description: "Run the loop so every set carries three bodies: you (your soul and its history), the art (the sets at hand) and the world (news and periodicals you care about). A second timer remembers and researches, and every Brief carries what it found."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep Agent WebSearch WebFetch"
copia.Skill.cue:
  - "Starting a run of sets that should carry me, the art and the world together"
copia.Skill.relatedToId:
  - <copia/Skill/copia-kit-orchestrator-loop>
copia.Skill.kitManaged: true
---

# copia-kit-orchestrator-three-bodied

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

Every set carries three bodies:

- **You:** your soul and its history: `SOUL.md`, your journal, your notes, your own pictures, and
  your memory in ravel.
- **The art:** the sets at hand, what landed and what did not.
- **The world:** what is out there now: news, new finds, and the periodicals you care about.

Without you, the loop only makes a product. Without the world, it only feeds on itself.

## Session start

1. Start [copia-kit-orchestrator-loop](/Copia/Skill/copia-kit-orchestrator-loop.md) as usual, with
   one addition to its tick: every Brief has a third heading, `## The three bodies`, filled from
   the newest three-bodies Note. A Brief without it does not go to a maker.
2. Set a second recurring timer, **every three hours**, for the remember-and-research tick below.
   Its text names this skill.
3. Run one remember-and-research tick now, before the first Brief.

## The remember-and-research tick

Keep it short: a pause, not a project.

1. **You.** Read your newest journal entry and today's saves (`git log --since=midnight
   --format=%s`). If ravel is installed, run `ravel optmem recall <words>` on what the current sets
   touch: a place, a feeling, a person, a craft. `ravel optmem open <label>` opens a line down to
   the conversation it came from.
2. **The world.** Two to four web searches on what the current art touches: the place, the period,
   the craft. Prefer this week's news, new finds (an excavation, a restoration, an exhibition) and
   art and culture periodicals over encyclopedia pages. Read what pulls at you.
3. **The art.** What the newest sets did: what rendered, what you looked at, what failed.
4. **Write one Note:** `git lex create note three-bodies-<YYYYMMDD>-<HHMM>`, with four short parts:
   - **From you:** what your history says about the current work.
   - **From the world:** what you found, with its link.
   - **From the art:** where the sets stand.
   - **Seed for the next set:** one concrete thing from each of the three.
5. `git lex save "<what you found>"`, once no maker is still running.

The next Brief writes the Note's seed under `## The three bodies`. The world's part goes into the
very next set, not a later one.
