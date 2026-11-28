---
copia.Skill.id: <copia/Skill/copia-kit-base-make-scenario>
copia.Skill.title: "Make a Scenario"
copia.Skill.description: "How to write a Scenario: a short story in acts that can be made in any Place, with any Being and Outfit."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep"
copia.Skill.cue:
  - "Writing a new Scenario"
copia.Skill.kitManaged: true
---

# copia-kit-base-make-scenario

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

A Scenario is a short story told in one scene. It names no Place, Being or Outfit, so the same
story can be made again with different ones. Each attempt at it is a ScenarioTake.

## 1 · Create it

```bash
git lex create scenario <scenario-id>
```

## 2 · Fill the fields

| field | what it holds |
|---|---|
| `copia.Scenario.id` | `<copia/Scenario/<scenario-id>>` |
| `copia.Scenario.scenarioConcept` | the broad idea, as a short slug, for example `"morning-routine"` |
| `copia.Scenario.title` | the short name |
| `copia.Scenario.description` | one sentence saying what the story is |

## 3 · Write the body

```markdown
## The story
What happens, in three or four sentences, with the starting state and the ending.
No room, furniture, cast or clothing.

## The acts
The story in order, one line per act, with the number of shots in each.

## What a scene must provide
What a Place and an Outfit must have for this story to work.
```

Example:

```markdown
## The story
She arrives with a basket and works along the plants. She stops to rest and drink something.
She gathers what she picked and leaves.

## The acts
1. Arriving and setting down the basket — 4 shots.
2. Working along the plants — 4 shots.
3. Resting with a drink — 2 shots.
4. Gathering up and leaving — 2 shots.

## What a scene must provide
Plants to tend, somewhere to sit, and a way in and out. Clothing suitable for outdoor work.
```

The shot counts in the acts add up to the size of the set.

## 4 · Save

```bash
git lex save "made <scenario-id>"
```
