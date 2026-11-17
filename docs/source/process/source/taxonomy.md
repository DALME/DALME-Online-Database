(the-process-taxonomy)=
# The taxonomy

Every piece of work is a {term}`Closure`: an entry point that stands for, and
closes over, a whole tree of concerns. Most issue types are not separate *kinds*
of thing but **positions** in that one recursive shape.

## The shape

A **META** heads a closure. Beneath it, two trees hang side by side: the STORY
tree (domain) and the EPIC tree (technical). Dotted lines are `Realizes` links
across them.

```{mermaid}
graph TD
  M[META] --> S1[STORY]
  M --> E1[EPIC]
  S1 --> S2[STORY]
  S1 --> S3[STORY]
  E1 --> E2[EPIC]
  E1 --> T1[TASK]
  E2 --> T2[TASK]
  M --> FX[FIX]
  E1 -. realizes .-> S2
  FX -. realizes .-> S3
```

- **META**: the head of a closure. It has a behavioural face, a tech-free
  narrative of who does what and why, and a structural face, a link to the
  `CONTEXT.md` whose language governs it. Keep METAs general: most live inside an
  existing context and point at its `CONTEXT.md` rather than owning one.
- **STORY**: a unit of domain behaviour. A theme plus one or more lines of the
  form "as an *actor*, I want an *intention*, so that an *outcome*", held as an
  acceptance checklist. A STORY lives in exactly one {term}`Bounded Context`;
  when the actor or context changes, write a sibling STORY. A STORY's children are
  only ever STORYs.
- **EPIC**: a technical composite of EPICs and TASKs that realizes a STORY.
- **TASK**: a single leaf of technical work, usually under an EPIC.

## The META is a briefing

A well-formed META is enough, on its own, to put a capable worker to work on its
whole closure. Someone arriving cold, a new contributor or an agent, should be
able to read that one entry point and the `CONTEXT.md` it points at, and start
delivering. If they have to reach for context they cannot find there, the META
is underspecified, and that is a defect in the scoping, not in the worker.

## The two halves do not mix

Technical work does not live *under* a story. It **realizes** one, recorded as a
plain link (`Realizes #N`). Three rules keep the domain tree in the domain
register:

1. **The STORY template has nowhere to put technical content.** It has a theme,
   an actor, an intention, an outcome and a situation; there is no field for a
   table, a key or an endpoint.
2. **Behaviour comes first.** No EPIC or TASK is worked until there is a STORY it
   realizes.
3. **STORYs contain only STORYs**, so the domain tree stays pure all the way down.

Process and tooling work, which has no domain behaviour of its own, says so
explicitly (`Realizes: none`) rather than inventing a story to hang from.

## Acceptance

"All the child tickets are closed" is never the criterion; the sub-issue
progress bar tracks that for free.

- A **TASK** is done when the unit works and is merged by PR.
- An **EPIC** is done when the STORY it realizes is true end to end. The
  interesting failures of a composite live in the seams between its tasks, which
  no single task owns.
- A **META** is realized when its whole closure is.

## Issue types

The types are organisation-level GitHub issue types, so each ticket carries its
type as a badge.

| Type | Colour | Role |
|---|---|---|
| **Meta** | purple | Head of a closure: domain narrative and the governing ubiquitous language. |
| **Story** | green | Tech-free domain behaviour, scoped to one bounded context. |
| **Epic** | orange | Technical composite of epics and tasks that realizes a story. |
| **Task** | yellow | A single leaf of technical work. |
| **Fix** | pink | A focused change to a known issue. May hang off a META, or stand alone. |
| **Bug** | red | An unexpected problem or behaviour. |
| **Feature** | blue | A request or idea not yet scoped into a closure. |
| **Intake** | gray | The rolling triage inbox. Sits before everything else. |
| **ADR** | gray | Tracking ticket for an architectural decision record. |

## Templates, titles and branches

Each type has a template under `.github/ISSUE_TEMPLATE/`, which sets the type
and gives the right shape to fill in. What the STORY template omits is as
deliberate as what it includes.

- **Titles** of the tickets that structure the work carry a prefix: a META names
  its area (`META | Transcription`), a STORY or EPIC names the topic it belongs
  to (`Transcription | Marking up an entity`), and an ADR names itself
  (`ADR | Search and indexing architecture`). Leaf tickets (TASK, FIX, FEATURE
  and BUG) have plain titles; their type shows as a badge.
- **Bodies** open with the ticket's code, `` `ida/#N` ``.
- **Branches** take the same name, `ida/#N`.

## Labels

Labels are facets, independent of where a ticket sits in the tree: who owns it,
which part of the stack it touches, and whether it still needs refinement. The
label set is TBD.

The {term}`Bounded Context` a ticket belongs to is never a label. Contexts nest
and labels are flat, so it is carried structurally instead, by the nearest
`CONTEXT.md` and the one-context-per-STORY rule.
