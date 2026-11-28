---
copia.Skill.id: <copia/Skill/copia-kit-base-make-item>
copia.Skill.title: "Make an Item"
copia.Skill.description: "How to make an Item: one garment or one object."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep"
copia.Skill.cue:
  - "Making a new Item"
copia.Skill.kitManaged: true
---

# copia-kit-base-make-item

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

An Item is one garment or one object. Garments are grouped into Outfits.

## 1 · Check what exists

```bash
coquette list Item
```

## 2 · Create it

```bash
git lex create item <item-id>
```

## 3 · Fill the fields

| field | what it holds |
|---|---|
| `copia.Item.id` | `<copia/Item/<item-id>>` |
| `copia.Item.itemId` | `"<item-id>"` |
| `copia.Item.itemName` | the short name |
| `copia.Item.itemDescription` | what it looks like |
| `copia.Item.affordance` | `wearable` (a garment), `holdable` (carried in the hand) or `prop` (stays in place) |
| `copia.Item.renderRule` | optional: a correction for prompts that name this Item |

## 4 · Write the description

Name the colour, the material, the cut or shape, and any fastenings. A vague description renders
as a vague object.

Example:

```yaml
copia.Item.itemDescription: "a mustard-yellow wool cardigan, hip length, with five brown wooden buttons and two patch pockets"
```

## 5 · Save

```bash
git lex save "made <item-id>"
```
