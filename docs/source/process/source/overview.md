(the-process-overview)=
# Overview

{term}`The Process` is domain-driven design in its most practical form: the
conversation, before any code, in which we decide *what* is worth building and
*why*, in terms that a stakeholder and a developer can both hold in their heads
at once.

## Domain first

We describe behaviour in plain domain terms *before* we describe any
implementation. We work out what happens, for whom, and why it matters, and only
then descend towards tables, endpoints and components.

This is not a stylistic preference. Nobody using the system thinks "a record has
a generic foreign key to a page node". They think "a researcher traces an object
listed in an inventory back to the page of the source that records it". That
second sentence is what scoping exists to capture. A subsystem conceived
directly in implementation terms, as a data model written straight into a
ticket, is one that nobody has thought about as part of the domain.

## Two registers, one descent

Work runs along a gradient. At the top it is entirely stakeholder-facing: plain
language, {term}`Ubiquitous Language` terms, no jargon. At the bottom it is
entirely technical: the concrete change a developer makes. Nothing technical is
permitted at the top, and nothing vague at the bottom.

## Stories compose

A STORY reads "as an *actor*, I want an *intention*, so that an *outcome*", and
each part takes its meaning from the language of one {term}`Bounded Context`.
That is why a STORY lives in exactly one context: fix the context and you fix the
meaning of its parts, and only then can the whole be built from them. The same
holds up the tree. A META's meaning is a function of the stories beneath it.

## Why it outlives us

Code only ever tells you *how* a system does what it does, never *why*. A
newcomer can reconstruct the mechanism and still not know which details are
essential and which are accidents of the day they were written. A domain model
stated in the domain's own terms does not rot when the technology does. That is
the deepest reason The Process is worth the trouble, and it matters most on a
project whose maintainers come and go in bursts.

The mechanics (the issue types, the templates, the shape of the tree) are set
out in {ref}`the taxonomy <the-process-taxonomy>`.
