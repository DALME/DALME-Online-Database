(ddd)=
# Domain-Driven Design

[Domain-driven design](https://en.wikipedia.org/wiki/Domain-driven_design)
(DDD) is an approach to *software design*. It is less about writing software
than about deciding what software needs to be written at all, and then refining
those decisions in a loop where idea meets implementation.

DDD happens in the conversation between the people who build a system and the
people who know its subject: here, historians working with late-medieval
documentary sources. Out of that conversation comes a shared language, the
{term}`Ubiquitous Language`, and a {term}`Domain Model` stated in it. The model
tells us what to build and why. The code is one realization of it, and a
replaceable one.

:::{important}
DALME's domain model is older than **{term}`The Process`**. At its heart is a
relational ontology designed by Gabriel Pizzorno and realized today in the
`domain` Django app. We are writing that model down with the people who designed
it, one {term}`Bounded Context` at a time, rather than reverse-engineering it
from the code. Until a context has its own `CONTEXT.md`, the code is the only
record of it, and code records *how*, never *why*.

This labour should help propel us towards any envisaged IDA implementation, which
we intend to begin work on soon.
:::

## Where the model lives

The model of record is a tree of `CONTEXT.md` files in the repository:

- The **root `CONTEXT.md`** does not model a domain. It declares the modelling
  language we work in: the DDD patterns we use, the ones we deliberately defer,
  and the skeleton every other `CONTEXT.md` follows.
- Each **nested `CONTEXT.md`** models one {term}`Bounded Context`: the closure of
  files at and below its position in the tree. A nested file refines its
  ancestors and never contradicts them.

These pages explain the ideas. The `CONTEXT.md` files are terse and
authoritative; when the two disagree, the `CONTEXT.md` is right and the page is
stale.

:::{note}
The *domain*, in the abstract, is not the same thing as `domain`, the Django
app. The app is where much of the domain is realized in code today, but the
domain is the subject itself, and it outlives any app that implements it.
:::

## Further reading

The original and best source is Eric Evans,
[*Domain-Driven Design: Tackling Complexity in the Heart of Software*](https://www.oreilly.com/library/view/domain-driven-design-tackling/0321125215).
The {ref}`terminology <ddd-terminology>` page glosses the vocabulary we use most.
