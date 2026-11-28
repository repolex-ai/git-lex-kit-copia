---
copia.Skill.id: <copia/Skill/copia-kit-base-make-outfit>
copia.Skill.title: "Make an Outfit"
copia.Skill.description: "How to make an Outfit: a named set of garment Items worn together."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep"
copia.Skill.cue:
  - "Making a new Outfit"
copia.Skill.kitManaged: true
---

# copia-kit-base-make-outfit

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

An Outfit is a named set of garments worn together. Each garment is its own Item.

## 1 · Check what exists

```bash
coquette list Outfit
```

## 2 · Make the Items

Make one Item for each garment, with `affordance: wearable`. See
[copia-kit-base-make-item](/Copia/Skill/copia-kit-base-make-item.md).

## 3 · Create the Outfit

```bash
git lex create outfit <outfit-id>
```

## 4 · Fill the fields

| field | what it holds |
|---|---|
| `copia.Outfit.id` | `<copia/Outfit/<outfit-id>>` |
| `copia.Outfit.outfitId` | `"<outfit-id>"` |
| `copia.Outfit.outfitName` | the name written in prompts, in capitals |
| `copia.Outfit.outfitDescription` | the outfit as worn, outermost layer first |
| `copia.Outfit.relatedToId` | each Item, one per line: `<copia/Item/<item-id>>` |
| `copia.Outfit.cue` | optional: when the outfit is worn |
| `copia.Outfit.renderRule` | optional: a correction for prompts that name this Outfit |

## 5 · Write the description

- Name each garment's colour, fabric and cut.
- Keep the torso to two layers. When more torso layers are named in one prompt, usually only the
  outermost renders.

Example:

```yaml
copia.Outfit.outfitName: "THE GARDEN DAY"
copia.Outfit.outfitDescription: "a mustard-yellow wool cardigan over a white cotton t-shirt, faded blue jeans rolled at the ankle, and white canvas shoes"
copia.Outfit.relatedToId:
  - <copia/Item/mustard-cardigan>
  - <copia/Item/white-cotton-tshirt>
  - <copia/Item/faded-blue-jeans>
  - <copia/Item/white-canvas-shoes>
```

## 6 · Save

```bash
git lex save "made <outfit-id>"
```

A maker skips this step; the orchestrator saves.
