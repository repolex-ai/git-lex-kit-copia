# git-lex copia kit

Optional add-on for soul. The agent's curated outward face — the places,
items, beings, and outfits the agent chooses to publish into the **CoPIA**
rendering loop.

Soul stays sealed and AI-only; copia is the *soul-adapter*: the surface the
generative loop reads via SPARQL.

Four classes:

- **Place** — a location you can be in. Places connect to other Places.
- **Item** — a thing. Items live in Places, or are equipped by Beings.
- **Being** — anyone in the world (the agent, a companion, an inhabitant).
  Beings are located in Places, can equip Items, and wear Outfits.
- **Outfit** — a named set of garments a Being wears. Switchable across scenes;
  attire is scene-variable, not being-fixed.

Designed to be sketched-then-filled — a Place can be referenced before it
exists (figment), then built later. Same shape for Items, Beings, and Outfits.

## Scene fields (the keystone)

Every CoPIA **Moment** (a rendered PNG) is stamped with 15 `Scene*` parameters.
Ten of them are *stable* properties of a canon entity, so the kit gives each
class the subset it owns — named to match the Moment predicates, so a canon
entity answers the observer in the same vocabulary a Moment is stamped in
(field-overlap, no translation):

- **Place** → `sceneLocation` `sceneLighting` `sceneMood` `sceneStyle` `sceneObjects`
- **Being** → `sceneCharacters` `scenePosture` `sceneExpression` `sceneGaze`
- **Outfit** → `sceneAttire` `sceneStyle`
- **Item** → `sceneObjects`

The remaining five — `framing` `camera` `energy` `action` `medium` — are
per-Moment / compositional. The observer sets them from the live conversation
and `>>chevrons<<`; they are **not** stored on canon entities.

## Naming

This kit was briefly named `innerworld` (v0.1.x). It was renamed to `copia` at
v0.2 because the vocabulary is really a *soul-adapter* for the CoPIA system,
not a generic "innerworld" concept. The class shapes (Place / Item / Being)
were identical to v0.1; only the kit / folder / namespace names changed.

**v0.3** adds the Scene fields (above) and the **Outfit** class — the point at
which copia stops being a generic world-vocabulary and becomes a true adapter
to CoPIA's 15-field Moment protocol.
