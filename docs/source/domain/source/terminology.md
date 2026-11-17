(ddd-terminology)=
# Terminology

A quick reference for the vocabulary used throughout these docs. The DDD
*patterns* we use and deliberately defer are catalogued in the repository's root
`CONTEXT.md`, which is the authoritative reference; this page only glosses the
words.

---

{.glossary}
**Aggregate**

: "A cluster of domain objects that can be treated as a single unit."
[Martin Fowler](https://martinfowler.com/bliki/DDD_Aggregate.html) One member,
the aggregate root, is the only way in from outside, so it can keep the whole
consistent.

{.glossary}
**Bounded Context**

: The boundary within which one {term}`Domain Model` and its
{term}`Ubiquitous Language` apply. The same word may mean different things in
different contexts. [Martin Fowler](https://martinfowler.com/bliki/BoundedContext.html)

{.glossary}
**Closure**

: A piece of work together with everything beneath it: an entry point (a META)
that stands for, and closes over, a whole tree of concerns. See
{ref}`the taxonomy <the-process-taxonomy>`.

{.glossary}
**Domain Model**

: "An object model of the domain that incorporates both behavior and data."
[Martin Fowler](https://www.martinfowler.com/eaaCatalog/domainModel.html) Ours is
stated in natural language, in `CONTEXT.md` files, before it is stated in code.

{.glossary}
**Entity**

: An object defined by a continuous identity through time, rather than by its
attributes. [Martin Fowler](https://martinfowler.com/bliki/EvansClassification.html)

{.glossary}
**Invariant**

: A rule that must always hold within its scope, typically enforced by an
{term}`Aggregate`'s root.

{.glossary}
**The Process**

: How work on this system travels from a raw idea to merged code: intake and
triage, scoping into a {term}`Closure`, decisions recorded as ADRs, and delivery
in small reviewed slices. Domain first, implementation after. See
{ref}`the overview <the-process-overview>`.

{.glossary}
**Ubiquitous Language**

: The shared, rigorous language of a {term}`Bounded Context`, used identically in
conversation, documentation and code.

{.glossary}
**Value Object**

: An object that matters only as the combination of its attributes; two with
equal attributes are equal.
[Martin Fowler](https://martinfowler.com/bliki/EvansClassification.html)
