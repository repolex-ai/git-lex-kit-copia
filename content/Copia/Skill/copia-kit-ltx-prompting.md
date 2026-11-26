---
copia.Skill.id: <copia/Skill/copia-kit-ltx-prompting>
copia.Skill.title: "LTX prompting"
copia.Skill.description: "How to write an LTX image-to-video prompt and make 12-second clips with coquette."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash"
copia.Skill.cue:
  - "Making a video from an image"
copia.Skill.kitManaged: true
---

# copia-kit-ltx-prompting

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

## 1 · Read what the image already is

The image is the first frame of the clip, so it is already described. Read its caption and the
prompt it was made from:

```bash
syrinx sparql 'PREFIX pan: <https://repolex.ai/ontology/pan/>
SELECT ?caption ?prompt WHERE {
  SERVICE <https://repolex.ai/ontology/pan/> {
    OPTIONAL { <pan/Image/<id>> pan:shortCaption ?caption }
    OPTIONAL { <pan/Image/<id>> pan:renderRequestInformation ?prompt }
  }
}'
```

## 2 · Write who and where, then the motion

Two short sentences. First who is in the frame, where, and what they wear, from the caption. Then
one small, slow motion that carries on from the frame.

- Keep the figure in the pose and facing the image shows.
- One small motion. The less that moves, the less can go wrong.
- Say what happens. The video model cannot follow "not".

Example, for an image of a woman at a kitchen window holding a watering can over a row of herbs:

```
A woman in a green apron stands at a kitchen window holding a watering can over a row of herb pots.
She slowly tips the can along the row, and water runs into the soil.
```

## 3 · Make the clip

One clip:

```bash
coquette video "<who and where. the motion.>" --source-img-id <id> --set-id <set name>
```

Many clips: write a video Shotlist with
[copia-kit-make-shotlist](/Copia/Skill/copia-kit-make-shotlist.md), one line per clip:

```
<pan/Image/<id>>: <who and where. the motion.>
```

Each clip is 12 seconds. Add `-n` for a dry run.
