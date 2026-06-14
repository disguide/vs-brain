# Bedrock

A question-tree web app — like Wikipedia, but for **questions** instead of articles.

Unlike debate sites that stay shallow and list surface pro/con points, Bedrock forces
every argument **down** to the fundamental **values** it rests on. The core insight: most
real questions, pushed deep enough, don't have one universal answer — they resolve into a
**fork** between fundamental values (e.g. *"minimize suffering"* vs *"never use a person as a
means"*). The app makes that value-fork visible by letting you drill down through a tree of
nodes until each branch bottoms out at a **bedrock value**.

This is **V1**: a single-user, browse-and-drill prototype with **hardcoded** seed data — no
database, no login, no backend. The seed graph is the classic Trolley Problem.

---

## Run it

```bash
cd bedrock
npm install
npm run dev      # open the printed http://localhost:5173 URL
```

Build a static, shareable site:

```bash
npm run build    # outputs to dist/
npm run preview  # serve the production build locally
```

`dist/` is a plain static site (asset paths are relative), so it can be hosted anywhere.

---

## How the data model works

The whole app is a **DAG** (directed acyclic graph) of nodes and edges, defined in
`src/data/`. A node can have multiple parents — value nodes especially are shared across
many questions — so nothing assumes a strict tree.

**Four node types** (`src/data/types.ts`):

| type       | what it is                                              | visual            |
| ---------- | ------------------------------------------------------- | ----------------- |
| `question` | something to drill into                                 | blue, `?` marker  |
| `position` | a candidate answer to a question                        | slate, `POSITION` |
| `argument` | a reason supporting/attacking a position (challengeable) | green/red         |
| `value`    | **terminal** bedrock a chain bottoms out at             | amber, `⚓`        |

**Six edge types** — note these are stored in their natural *semantic* direction (the same
direction they'll be rows in Supabase later), which is not always top-to-bottom in the tree:

| edge           | direction              | meaning                                        |
| -------------- | ---------------------- | ---------------------------------------------- |
| `answers`      | position → question    | this position answers this question            |
| `supports`     | argument → position    | argument backs the position                    |
| `attacks`      | argument → position    | argument undermines the position               |
| `raises`       | argument → question    | this argument raises a new sub-question         |
| `grounds-in`   | argument → value       | this argument bottoms out at this value (terminal) |
| `shared-value` | argument → value       | grounds-in, but for a value **reused** across questions |

`src/lib/graph.ts` knows how to orient each edge type so the drill-down still reads
`question → position → argument → (sub-question | value)`:

- `getNodeById(graph, id)`
- `getChildren(graph, nodeId)` → the tree-children + the edge type connecting each
- `getEdgeType(graph, from, to)`
- `isFullyGrounded(graph, questionId)` → the **FULLY GROUNDED / OPEN** badge. `true` only if
  *every* argument chain under the question reaches a value node; `false` if any branch
  dead-ends at an unanswered question or a dangling argument. This is the honesty mechanism:
  it shows which questions you've actually traced to bedrock.

All recursive traversals carry a `visited`/`ancestors` set to stay safe against cycles.

---

## Add a node by editing `seed.ts`

You only ever edit **`src/data/seed.ts`**. Adding content is two steps:

1. Add an entry to `nodes` with a unique `id`, a `type`, and `content` (arguments also need a
   `stance`; values also need `isTerminal: true`).
2. Add the `edges` that connect it, using the correct `edgeType` and **direction** from the
   table above.

### Worked example: add an *attack* argument to Position A

Position A is `pos-a` ("Yes, pull the lever"). To attack it:

```ts
// in nodes:
{
  id: "arg-a-attack",
  type: "argument",
  stance: "attack",
  content: "Diverting the trolley makes you morally responsible for a death you caused",
},

// in edges:
{ id: "e-attack-1", from: "arg-a-attack", to: "pos-a", edgeType: "attacks" },
```

That argument now shows up in **red** under Position A, labeled `ATTACKS`. Because it raises
no sub-question and grounds in no value, the root question's badge flips to **OPEN** — the
new branch hasn't been traced to bedrock yet. Give it a `raises` edge to a new question (or a
`grounds-in` edge to a value) to ground it and flip the badge back to **FULLY GROUNDED**.

> Tip: to demonstrate a **shared value**, point a second argument at an existing value node
> with `edgeType: "shared-value"` — it'll render with an `↺ shared` indicator.

---

## File structure

```
bedrock/
  src/
    data/
      types.ts      # the node/edge/graph TypeScript interfaces
      seed.ts       # the hardcoded Trolley Problem graph  ← edit this to add content
    lib/
      graph.ts      # getChildren / getNodeById / isFullyGrounded / getEdgeType
    components/
      NodeCard.tsx  # renders one node, styled by type
      TreeView.tsx  # the recursive drill-down tree
      Legend.tsx    # legend for the node types / badges
    App.tsx         # mounts the TreeView with the seed graph + legend
    main.tsx
    styles.css
```

---

## What V2 would add (not built yet)

1. **Supabase persistence** — move the hardcoded `nodes`/`edges` into Postgres tables (the
   schema maps one-to-one to the current data model) and load the graph from there.
2. **Contribution layer** — accounts, then letting others author positions/arguments/values
   and challenge existing arguments (the "answering spawns more questions" loop).
3. **Value-ranking engine** — a propagation pass that surfaces which bedrock values a
   question forks between, and lets users weigh them.

V1 deliberately stays browse-and-drill only: you synthesize the answer yourself.
```
