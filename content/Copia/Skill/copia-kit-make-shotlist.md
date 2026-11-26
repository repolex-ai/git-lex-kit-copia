---
copia.Skill.id: <copia/Skill/copia-kit-make-shotlist>
copia.Skill.title: "Make a Shotlist"
copia.Skill.description: "How to write a Brief and a Shotlist, image or video, and fire it with coquette."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep"
copia.Skill.cue:
  - "Writing a Shotlist"
  - "Firing a set of images or clips"
copia.Skill.kitManaged: true
---

# copia-kit-make-shotlist

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

A Shotlist is the list of prompts for one set, one shot per line. Every Shotlist names the Brief
it was written from.

## 1 · Write the Brief

```bash
git lex create brief <brief-id>
```

Under `## The brief`, write what this set is to do: the Being, Place and Outfit, the number of
shots, and the acts if it follows a Scenario. Under `## Why`, a line on what you are reaching for.
A maker is handed a Brief that already exists and skips this step.

## 2 · Plan the shots

Divide the shots evenly across the acts or beats. Within a beat, change one thing per shot: the
pose, the action, the facing or the crop. Keep the camera position steady across the set.

## 3 · Write the prompts

Image prompts follow [copia-kit-krea2-prompting](/Copia/Skill/copia-kit-krea2-prompting.md);
clip prompts follow [copia-kit-ltx-prompting](/Copia/Skill/copia-kit-ltx-prompting.md).

## 4 · Create the Shotlist

```bash
git lex create shotlist <shotlist-id>
```

```markdown
---
copia.Shotlist.id: <copia/Shotlist/<shotlist-id>>
copia.Shotlist.title: "<name>"
copia.Shotlist.shotlistMedium: image
copia.Shotlist.relatedToId:
  - <copia/Brief/<brief-id>>
---

## The lines
SUBJECT: An image of a woman in THE BACK GARDEN. WOMAN: MARA. ... CROP: [13:16] portrait.
<pan/Image/ab12cd34> denoising_strength=0.4: SUBJECT: An image of a woman in THE BACK GARDEN. ...

## Notes
```

Under `## The lines`, one shot per line and nothing else: no numbers, no bullets, no code fence.
Each line is one of two forms:

- `prompt`: the whole line is the prompt, sent exactly as written.
- `<pan/Image/ID> setting=value ...: prompt`: built from that picture in Pan, keeping its shape.
  Settings are optional: `denoising_strength` (0 to 1, lower keeps more of the picture; the server
  default is 0.75), `seed`, `subseed`, `subseed_strength`, `batch_size` (1 to 4).

**A video list** sets `copia.Shotlist.shotlistMedium: video`. Every line uses the second form and
makes one 12-second clip from its picture; the only setting is `seed`. An Action is optional: put
`<copia/Action/<id>>` before the colon, and name it in `relatedToId` too.

Under `## Notes`, anything about this firing: what departed from the Brief, and why.

## 5 · Read it back

Read the whole list from the top. Check that each shot follows from the one before, and fix any
line that jumps.

## 6 · Fire it

From the repo root, do a dry run first and check that it shows the number of lines you wrote:

```bash
coquette image -n --shotlist '<copia/Shotlist/<shotlist-id>>' --aspect portrait
```

Then the same command without `-n`. The same command fires a video list.

- The pictures join a set named after the Shotlist. Add `--set-id <name>`, once or more, to put
  them in other sets too.
- `--aspect` is `portrait` (1664x2048), `square` (1856x1856) or `landscape` (2048x1664), and the
  `CROP:` in every line matches it. Leave `--aspect` off when any line starts from a picture.
- `--batch N` makes N images per shot. `--variation` (0.0 to 1.0) sets how far they differ.

## 7 · Save

```bash
git lex save "fired <shotlist-id>"
```

A maker skips this step; the orchestrator saves.
