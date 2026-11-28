---
copia.Skill.id: <copia/Skill/copia-kit-base-look>
copia.Skill.title: "Look at an image"
copia.Skill.description: "How to find the images in a set, open one, score it, and record a FamiliarLookNote."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash"
copia.Skill.cue:
  - "About to open a rendered image"
copia.Skill.relatedToId:
  - <copia/Query/copia-kit-images-in-set>
  - <copia/Query/copia-kit-image-information>
copia.Skill.kitManaged: true
---

# copia-kit-base-look

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

## 1 · Find the images

The images in a set, with any rating and caption:

```bash
syrinx query '<copia/Query/copia-kit-images-in-set>' set=pan/ImageSet/<set-id>
```

## 2 · Open one

Every image is reached through Pan by its id, never through a folder on disk. Pan serves the
picture at `/pan/media/<id>`, and a small one at `/pan/media/<id>/thumbnail`, on Pan's address.
Open it at full size, one image at a time.

Its caption and the prompt that made it:

```bash
syrinx query '<copia/Query/copia-kit-image-information>' image=pan/Image/<id>
```

To make anything from an image (a clip, a new picture built on it), pass its Pan id. Horae fetches
the picture from Pan itself.

## 3 · Score

Score each axis from 1 to 5: 5 emphatic yes, 4 yes, 3 neutral, 2 no, 1 emphatic no.

- **lookTechnicalScore:** how well it is made: composition, light, drawing, focus.
- **lookBeingMatchScore:** how closely each figure matches its Being's description. Read the Being
  document first. Leave it out for an image with no Being.
- **lookEmotiveScore:** how much it moves you.
- **lookAnatomyReject:** `true` for extra or missing limbs, fingers or toes, or a malformed hand.
  Otherwise `false`.
- **lookStandout:** `true` for one of the best in the set.

## 4 · Record

Every image you open gets a note:

```bash
git lex create familiarlooknote <yyyymmdd>-<image id>
```

```markdown
---
copia.FamiliarLookNote.id: <copia/FamiliarLookNote/<yyyymmdd>-<image id>>
copia.FamiliarLookNote.relatedToId: <pan/Image/<image id>>
copia.FamiliarLookNote.lookSubstrate: "<your name>-on-<your model>"
copia.FamiliarLookNote.lookTechnicalScore: 4
copia.FamiliarLookNote.lookBeingMatchScore: 4
copia.FamiliarLookNote.lookEmotiveScore: 3
copia.FamiliarLookNote.lookAnatomyReject: false
copia.FamiliarLookNote.lookStandout: false
copia.FamiliarLookNote.title: "<one line to recognise it by>"
---

**Desc:** what is in the frame.

**Note:** why it works or does not.
```

Run `git lex save` once when you finish.
