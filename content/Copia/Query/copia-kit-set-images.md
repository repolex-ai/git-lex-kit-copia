---
type: Query
copia.Query.id: <copia/Query/copia-kit-set-images>
copia.Query.title: "The images in a set"
copia.Query.description: "Every image in one Pan image set, with its rating and short caption where it has them. Takes the set as set=pan/ImageSet/<set-id>."
copia.Query.cue:
  - "Finding the images in a set, to look at them or make clips from them"
copia.Query.service: "pan"
copia.Query.parameter:
  - "set:iri"
copia.Query.kitManaged: true
---

# The images in a set

> **Delivered by the copia kit.** `git lex kit-update` replaces this file, so do not edit it. To
> change it, copy it to a new name of your own.

Run it with the set's Pan id:
`syrinx query '<copia/Query/copia-kit-set-images>' set=pan/ImageSet/<set-id>`.
One row per image, in order of id. An image not yet rated or captioned has those columns empty.

```sparql
PREFIX pan: <https://repolex.ai/ontology/pan/>
SELECT ?image ?rating ?caption
WHERE {
  ?image a pan:Image ;
         pan:relatedToId ?set .
  OPTIONAL { ?image pan:rating ?rating }
  OPTIONAL { ?image pan:shortCaption ?caption }
}
ORDER BY ?image
```
