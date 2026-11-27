---
type: Query
copia.Query.id: <copia/Query/copia-kit-waiting>
copia.Query.title: "What is waiting to render"
copia.Query.description: "How many renders are queued or running on Horae, by kind (image for stills, clip for clips), and when each kind last finished one."
copia.Query.cue:
  - "Deciding whether the render queue needs more work"
copia.Query.service: "horae"
copia.Query.kitManaged: true
---

# What is waiting to render

> **Delivered by the copia kit.** `git lex kit-update` replaces this file, so do not edit it. To
> change it, copy it to a new name of your own.

Run it as `syrinx query '<copia/Query/copia-kit-waiting>'`. One row per kind of render:
`image` for stills, `clip` for clips. `?waiting` is how many are queued or running; `?lastFinished`
is when that kind last finished one, so a count that is not falling with an old time means the
server has stopped. It counts only renders you sent (`origin "direct"`); items Horae makes for
itself while it talks are not renders.

```sparql
PREFIX horae: <https://repolex.ai/ontology/horae/>
SELECT ?process (SUM(?open) AS ?waiting) (MAX(?done) AS ?lastFinished)
WHERE {
  ?item a horae:QueueItem ;
        horae:process ?process ;
        horae:status ?status ;
        horae:origin "direct" .
  BIND(IF(?status IN ("queued", "running"), 1, 0) AS ?open)
  OPTIONAL { ?item horae:updatedDate ?date }
  BIND(IF(?status = "completed", STR(?date), "") AS ?done)
}
GROUP BY ?process
```
