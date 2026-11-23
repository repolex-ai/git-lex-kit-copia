# git-lex copia kit

Optional add-on for soul. The agent's curated outward face **+ the data model**
for the **CoPIA** rendering loop. Soul stays sealed and AI-only; copia is the
*soul-adapter*: the surface the generative loop reads via SPARQL.

## Canon (authored, foldered under `/Copia/`)

- **Place** — a location you can be in. Connects to other Places. Carries scene
  defaults (`sceneLocation/Lighting/Mood/Style/Objects`).
- **Item** — the atomic thing. `affordance ∈ {wearable, holdable, prop}` says how
  it appears in a scene. Its "look" is its description.
- **Being** — anyone in the world (the agent, a companion, an inhabitant).
  Located in a Place, may equip Items, may `wears` an Outfit by default. Carries
  scene defaults (`sceneCharacters/Posture/Expression/Gaze`).
- **Outfit** — a convenience **join over Items** (`outfitIncludes → Item[]`): a
  named, reusable bundle/look you can summon as one. Owns no scene fields — the
  look comes from its member Items. A single garment needs no Outfit; it's just
  an `Item(wearable)`.

Sketch-then-fill: anything can be referenced before it exists (`figment`), then
built later.

## Moment (graph-only — not foldered)

A **Moment** is a rendered PNG + its metadata, the one persisted render artifact.
It is **not** authored as a file — the render pipeline instantiates it directly
in the CoPIA oxigraph. A Moment stores:

- the observer's realized **SceneIntent** — 10 scene-level fields
  (`location/lighting/mood/style/objects` + the per-render `framing/camera/energy/
  action/medium`) + `promptFragment` (the resolved text, which holds the
  who-wears-what binding);
- **flat presence-links** — `intentPlace` / `intentBeing` / `intentItem` /
  `intentOutfit` (repeated properties, so they're graph-traversable); these answer
  presence queries ("Moments with Selkie + Rob + the staff");
- **provenance** — `seed`, `promptModel`, `renderTimestamp`, `sessionId`,
  `sourceUuids`, etc.

No nested binding node: recall queries *presence* (flat links), and the
who-wears-what binding is preserved as text in `promptFragment`.

## Scene fields

The 15 `Scene*` parameters that describe a render. Canon entities hold the
**defaults** (`Place` 5, `Being` 4); the **Moment** records the **realized**
values. The same predicate carries both roles via two `rdfs:domain` triples
(Place + Moment). The 5 dynamic fields (`framing/camera/energy/action/medium`)
are Moment-only; the 4 Being fields' realized values fold into `promptFragment`.

## Naming / versions

Renamed from `innerworld` → `copia` at **v0.2** (it's a soul-adapter, not a
generic world). **v0.3** added the Scene fields + an Outfit class. **v0.4** is
the data-model lock: `Outfit` becomes a join over Items, `Item` gains
`affordance`, scene-field ownership moves to Place/Being defaults, and a
graph-only `Moment` records the realized render. Spec:
`copia-studio/docs/2026_06_06_COPIA_DATA_MODEL_SPEC.md`.
