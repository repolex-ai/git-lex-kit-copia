# git-lex copia kit

Optional add-on for soul. The agent's curated outward face — the places,
items, and beings the agent chooses to publish into the **CoPIA** rendering
loop.

Soul stays sealed and AI-only; copia is the *soul-adapter*: the surface the
generative loop reads via SPARQL.

Three classes:

- **Place** — a location you can be in. Places connect to other Places.
- **Item** — a thing. Items live in Places, or are equipped by Beings.
- **Being** — anyone in the world (the agent, a companion, an inhabitant).
  Beings are located in Places and can equip Items.

Designed to be sketched-then-filled — a Place can be referenced before it
exists (figment), then built later. Same shape for Items and Beings.

## Naming

This kit was briefly named `innerworld` (v0.1.x). It was renamed to `copia` at
v0.2 because the vocabulary is really a *soul-adapter* for the CoPIA system,
not a generic "innerworld" concept. The class shapes (Place / Item / Being)
are identical to v0.1; only the kit / folder / namespace names changed.
