---
copia.Skill.id: <copia/Skill/copia-kit-make-place>
copia.Skill.title: "Make a Place"
copia.Skill.description: "How to make a Place: a location that can be named in a prompt."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep"
copia.Skill.cue:
  - "Making a new Place"
copia.Skill.kitManaged: true
---

# copia-kit-make-place

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

A Place is a location that can be named in a prompt.

## 1 · Check what exists

```bash
coquette list Place
```

## 2 · Create it

```bash
git lex create place <place-id>
```

## 3 · Fill the fields

| field | what it holds |
|---|---|
| `copia.Place.id` | `<copia/Place/<place-id>>` |
| `copia.Place.placeId` | `"<place-id>"` |
| `copia.Place.placeName` | the name written in prompts, in capitals |
| `copia.Place.placeDescription` | where it is, what is in it, and the light |
| `copia.Place.cue` | optional: what happens here |
| `copia.Place.renderRule` | optional: a correction for prompts that name this Place |

## 4 · Write the description

- Describe the place itself. No artist, medium or style words; style belongs to the prompt.
- Name only what is fixed in the place. Objects someone carries are Items.
- Include somewhere to sit, lean or lie.
- Describe the light by colour, direction and quality only. Do not name a lamp or window as the
  source, or it will be drawn in the image.

Example:

```yaml
copia.Place.placeName: "THE BACK GARDEN"
copia.Place.placeDescription: "a small walled back garden with a brick path, raised beds of herbs and tomatoes, a wooden bench against the wall and a round iron table, soft warm light from the left"
```

## 5 · Save

```bash
git lex save "made <place-id>"
```
