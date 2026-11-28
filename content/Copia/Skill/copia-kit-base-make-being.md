---
copia.Skill.id: <copia/Skill/copia-kit-base-make-being>
copia.Skill.title: "Make a Being"
copia.Skill.description: "How to make a Being: a figure that can be named in a prompt."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep"
copia.Skill.cue:
  - "Making a new Being"
copia.Skill.kitManaged: true
---

# copia-kit-base-make-being

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

A Being is a figure that can be named in a prompt. Its description is what goes into the prompt,
so it holds only what the figure looks like.

## 1 · Check what exists

```bash
coquette list Being
```

## 2 · Create it

```bash
git lex create being <being-id>
```

This makes `Copia/Being/<being-id>.md`. Use lowercase letters and dashes for the id.

## 3 · Fill the fields

| field | what it holds |
|---|---|
| `copia.Being.id` | `<copia/Being/<being-id>>` |
| `copia.Being.beingId` | `"<being-id>"` |
| `copia.Being.beingName` | the name written in prompts, in capitals, for example `"MARA"` |
| `copia.Being.beingDescription` | what the figure looks like |
| `copia.Being.cue` | optional: when to use this Being |
| `copia.Being.renderRule` | optional: a correction for prompts that name this Being |

## 4 · Write the description

Start with the name and what the figure is: `MARA is a woman`. Then add only the features that
identify the figure: build, skin, face, eyes, hair, markings.

- Keep it to about 30 to 50 words.
- No clothing. Clothing belongs to an Outfit.
- No style, light, composition or camera. Those belong to the prompt.
- Say what is there. Do not describe the figure by what it is not.

Example:

```yaml
copia.Being.beingDescription: "MARA is a woman, slender, with an oval face, brown skin, dark brown eyes and short black curly hair, a small scar through her left eyebrow."
```

## 5 · renderRule

Use a renderRule only when a prompt keeps rendering this Being wrong. The form is:

```
KREA2: NEVER <what not to write> → <what to write instead>
```

## 6 · Save

```bash
git lex save "made <being-id>"
```
