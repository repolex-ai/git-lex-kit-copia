---
copia.Skill.id: <copia/Skill/copia-kit-base-krea2-prompting>
copia.Skill.title: "Krea2 prompting"
copia.Skill.description: "How to write a krea2 image prompt: the labeled sections and what goes in each."
copia.Skill.invocability: "both"
copia.Skill.allowedTools: "Read Write Edit Bash Glob Grep"
copia.Skill.cue:
  - "Writing a prompt for krea2"
copia.Skill.kitManaged: true
---

# copia-kit-base-krea2-prompting

**This skill is kit managed. Do not edit or change. Edits will be discarded.**

## The shape

Every prompt is one block of labeled sections, in this order:

```
SUBJECT: <the overall subject of the shot>.
WOMAN1: <what the first figure looks like>.
WOMAN2: <what the second figure looks like>.
CONTEXT: <fragment>, <fragment>, <fragment>.
COMPOSITION: <lens, position, framing>.
LIGHT: <colour, direction, quality>.
STYLE: <style>.
CROP: <aspect>.
```

Every labeled section ends with a period. Commas separate the fragments inside it.

## Sample prompt

```
SUBJECT: An image of two women at a table in a garden.
WOMAN1: a woman with short grey hair, wearing a yellow cardigan.
WOMAN2: a woman with dark curly hair, wearing a blue linen shirt.
CONTEXT: WOMAN1 is pouring tea into WOMAN2's cup, WOMAN2 is holding the cup with both hands, WOMAN1 is smiling, WOMAN2 is laughing, a white teapot and a plate of lemons on the table.
COMPOSITION: 50mm lens, eye level, close-up.
LIGHT: soft warm light from the left, even, low in contrast.
STYLE: photo realistic, reminiscent of Vermeer, natural skin texture, subtle film grain.
CROP: [13:16] portrait.
```

## SUBJECT

Who and where, short and direct: *An image of a woman near a tall window.*

## The figure lines

One line per figure, labeled to match the subject. One woman is `WOMAN`; two are `WOMAN1` and
`WOMAN2`; two elephants are `ELEPHANT1` and `ELEPHANT2`.

- Describe only what is visible: body, skin, hair, eyes, what is worn. Not what the figure is doing.
- To use a Being, put its name in capitals first, then its description:
  `WOMAN: MARA. MARA is a woman, slender, …`
- To use an Outfit or Place, write its name in capitals. CoPIA records the names it finds in the
  prompt with the image.

## CONTEXT

The action, what each figure is touching, and each face's expression.

- Refer to figures by their labels, never by pronouns: `WOMAN2's cup`, not *her cup*.
- Name an expression for each face in frame: *WOMAN1 is smiling.*
- Name two or three objects at most, only those a figure is touching or beside. Every object
  named takes space in the frame.
- An action may only touch something the prompt has already named.

## COMPOSITION

Lens, position and framing, in four short fragments or fewer: *85mm lens, from above, close-up.*

- Default to close-up.
- Say which way each figure is facing.
- In a sequence, a change of facing needs the turn in between written as its own shots.

## LIGHT

Colour, direction and quality, in three short fragments or fewer.

- Colour: warm amber, cool blue, gold, 2700K.
- Direction: from above, from the left, from behind, low from one side.
- Quality: soft, even, diffuse, hazy, low in contrast.

Do not name the source of the light (*lamplight*, *through the window*) unless it should appear in
the image. Do not tie the light to an object or a figure: *from behind*, not *from behind her*.

## STYLE

Default: `photo realistic, reminiscent of <artist>, natural skin texture, subtle film grain`.

Name an artist, not a medium. Medium words (`oil on canvas`, `watercolour`, `ink`,
`illustration`) override `photo realistic`. Use one only when the image should be that medium.

## CROP

One of `[13:16] portrait`, `[1:1] square` or `[16:13] landscape`, matching the `--aspect` the set is
fired with. Portrait is the default.

## Building on an existing picture (image-to-image)

A prompt can start from a picture already in Pan instead of from nothing. The new picture keeps the
start picture's width and height, so leave out `--aspect` and `--size`.

```bash
coquette image "<prompt>" --source-img-id <pan id> --denoising-strength 0.4
```

In a Shotlist, put it on the line: `<pan/Image/<id>> denoising_strength=0.4: <prompt>`.

**Denoising strength** sets how much the picture may change, from 0.0 to 1.0. Left out, it is the
render server's default, **0.75**.

- **Lower keeps more of the start picture; higher follows the prompt more.**
- **About 0.3 to 0.4:** stays close to the start picture.
- **About 0.1:** a detail touch-up only.

Write the whole prompt as usual. The prompt still describes the full image.

## Rules for every section

- Say what is there. "No jewelry" puts jewelry in the image.
- Use plain words: *red hair*, not *a crown of autumn fire*.
- Cut any phrase that does not describe the image.
- Do not mention the camera unless a camera should appear in the image.
- Name only body parts the crop can show. Extra parts make the model add more body.
- Name each body part once per prompt. A hand named twice can render as two hands.
- Each line in a Shotlist holds one whole prompt, with the sections in order on one line.
