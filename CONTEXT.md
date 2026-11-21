# CONTEXT — modelling conventions (root)

This is the **root `CONTEXT.md`**, the outermost node of the project's
`CONTEXT.md` tree. Unlike every other `CONTEXT.md`, it does not model a domain.
It declares the **modelling language** we work in, the Domain-Driven Design
patterns we use and the ones we deliberately do not, and the conventions every
nested `CONTEXT.md` follows. Each nested file refines one real **bounded
context** in this vocabulary.

For reader-facing treatments of these ideas, see the docs
(`docs/source/domain/` and `docs/source/process/`). This file is the terse,
authoritative reference that `CONTEXT.md` authors follow.

## The model so far

DALME's domain is centred on a relational ontology designed by Gabriel
Pizzorno, realized today in `app/domain`. Its bounded contexts are TBD: each is
written down with the people who designed it, never reverse-engineered from the
code.

Tenancy is part of the model, not an implementation detail.

- The **IDA** is the **central tenant**: the repository, and in time the
  service, of the shared research. Sites, systems, clients and applications
  orbit it and consume what it shares. It has no public site of its own (yet).
- Every other tenant is an **orbiting tenant**, a research project such as
  DALME or Historical Pharmacopeias. Each has its own public site and CMS, which
  stand wholly apart from every other project's. Each also has its own working
  material, drawn from the IDA, which belongs to it alone.
- The shared research is not enclosed by tenancy. It is shared freely with the
  orbiting tenants, and secured by ownership and authorization over it.
- A **user** belongs to no tenant. A user is a **member** of the projects they
  work in.

Which material is shared and which a project owns is stated per context.

## How we write a CONTEXT.md

- **Model first; the body is tech-free.** A `CONTEXT.md` is to a bounded context
  what a user story is to a behaviour: the domain model in ubiquitous language.
  No class, table, field or library name appears in the model itself.
- **Code lives in a fenced `Realization`.** Where a file bridges to the code
  beneath it, it does so only in a clearly fenced section that *serves* the
  model and never redefines it.
- **State only the current model.** A `CONTEXT.md` records the model as
  understood now. An honest "TBD" expresses partiality *as model*, never as a
  parking lot of open questions.
- **Never invent.** Do not model a rule or entity that is not real, and promote
  a concept to a named entity only in discussion, never silently.
- **Skeleton:** Purpose · Ubiquitous language · Invariants · Behaviours ·
  Relationships · Realization (fenced) · TBD.

## Patterns we use

*Tactical: the shape of a model.*

- **Entity**: an object defined by a continuous identity through time, not by
  its attributes. [Fowler](https://martinfowler.com/bliki/EvansClassification.html)
- **Value Object**: an object that matters only as the combination of its
  attributes; two with equal attributes are equal.
  [Fowler](https://martinfowler.com/bliki/EvansClassification.html)
- **Aggregate**: "a cluster of domain objects that can be treated as a single
  unit." [Fowler](https://martinfowler.com/bliki/DDD_Aggregate.html)
- **Aggregate Root**: the one member through which all outside references pass,
  so it can keep the aggregate consistent. **Always name the root.**
- **Invariant**: a rule that must always hold within its scope, typically
  enforced by an aggregate root.

*Strategic: the shape of the whole.*

- **Bounded Context**: the boundary within which one model and its ubiquitous
  language apply; the same word may mean different things across contexts.
  [Fowler](https://martinfowler.com/bliki/BoundedContext.html)
- **Ubiquitous Language**: the shared, rigorous language of a bounded context,
  used identically in conversation, documentation and code.
- **Subdomain: Core / Supporting / Generic**: how much attention a part of the
  domain deserves. **Core** is the distinctive part, worth the deepest
  modelling. **Supporting** keeps things running without differentiating the
  system. **Generic** is a solved problem, best met off the shelf.
  [Microsoft / Evans](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis)
- **Shared Kernel**: a subset of the model that two or more contexts agree to
  share; it cannot evolve without their agreement.
- **Anticorruption Layer**: a translation layer a downstream context builds to
  protect its own model from an upstream model's shape and changes.
  [Microsoft](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer)

## Patterns we defer

Named so that their absence is a choice, not an oversight. We adopt one only when
the model forces it.

- **Domain Event**: behaviours are stated as verbs, not yet as first-class
  events.
- **Domain Service**: behaviour owned by no single entity sits under a
  context's Behaviours for now.
- **Repository / Factory**: retrieval and construction are realization; they
  belong in the fenced Realization section, not the model.
- **Specification / Policy**: invariants are prose for now.
- **Open Host Service / Published Language**: not named as a pattern yet.
