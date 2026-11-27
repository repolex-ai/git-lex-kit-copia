---
type: Query
copia.Query.id: <copia/Query/copia-kit-image>
copia.Query.title: "What one image is"
copia.Query.description: "One Pan image's short caption, long caption and the prompt that made it. Takes the image as image=pan/Image/<id>."
copia.Query.cue:
  - "Reading what an image shows before looking at it, scoring it, or writing a clip from it"
copia.Query.service: "pan"
copia.Query.parameter:
  - "image:iri"
copia.Query.kitManaged: true
---

# What one image is

> **Delivered by the copia kit.** `git lex kit-update` replaces this file, so do not edit it. To
> change it, copy it to a new name of your own.

Run it with the image's Pan id:
`syrinx query '<copia/Query/copia-kit-image>' image=pan/Image/<id>`.
One row. The short caption is a sentence; the long caption describes the whole frame; the prompt is
what was sent to make it. A column is empty when Pan has not written it yet.

```sparql
PREFIX pan: <https://repolex.ai/ontology/pan/>
SELECT ?shortCaption ?longCaption ?prompt
WHERE {
  OPTIONAL { ?image pan:shortCaption ?shortCaption }
  OPTIONAL { ?image pan:longCaption ?longCaption }
  OPTIONAL { ?image pan:renderRequestInformation ?prompt }
}
```
