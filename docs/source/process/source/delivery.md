(the-process-delivery)=
# From ticket to merge

Once a ticket is scoped, delivery follows a fixed curriculum. The order is not
administrative: we do not argue about what we have not first written down,
which is why tests come before the implementation they specify.

1. **Scope the ticket.** A vague ticket makes everything downstream vague. A
   well-scoped ticket is already most of the raw material for a decision.
2. **Record the decision**, when there is one worth defending (see below).
3. **Plan.** Turn the decisions into an ordered slice map: prerequisites first,
   integration last. The plan evolves as the work teaches us things.
4. **Slice.** Each slice is one coherent commit that is reviewable on its own,
   passes every quality gate, and leaves nothing broken. If a slice touches more
   than about five files, or needs more explanation than a commit message, split
   it.
5. **Tests first.** For new behaviour, failing tests come before the
   implementation. For a refactor of load-bearing code, the first slice pins the
   current behaviour with regression tests.
6. **Execute** one slice at a time: gates, review, commit, update the plan, next.

## Decisions

We record a decision as an **architectural decision record** (ADR) when it has
real alternatives and is expensive to reverse, touches several components,
changes a public contract, or matters within one module. Bug fixes, local
refactors and temporary workarounds do not need one.

An ADR has four sections: **Context** (why now, citing code), **Decisions**
(numbered, each with what it costs), **Consequences** (predictions, both
positive and negative) and **Alternatives considered and rejected** (with
reasons, so the same debate does not recur).

Its status moves through two gates:

- **proposed**: under argument. Nothing is built.
- **agreed**: settled enough to build. Still editable, because building is what
  finds the corrections.
- **accepted**: the last slice has landed and the record has been made true of
  the code. From here it is immutable, and a change of mind is a new ADR that
  supersedes it.
- **rejected** or **withdrawn**: kept, with the reason.

Where ADRs are kept in the repository is TBD. Each has an **ADR** tracking
ticket, linked from the METAs it constrains.

## Branches, commits and pull requests

- Work happens on a branch named for its ticket, `ida/#N`, cut from
  `development.v2`.
- Commit messages are a single line: a capitalised imperative verb, short, no
  trailing period, no ticket number. The pull request carries the context.
- A pull request names the ticket it closes, and a red pipeline is a review in
  itself.
