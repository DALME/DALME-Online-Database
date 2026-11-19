(the-process-refresh)=
# Keeping a closure true

A decision rarely lands cleanly. It settles questions that tickets were holding
open, replaces reasoning written down elsewhere, and contradicts assumptions
nobody restated. Until someone walks the {term}`Closure` it touches, the tickets
and the decision disagree, and whoever picks up a leaf next builds from the
stale version.

So after any decision lands, and before building from any ticket beneath it,
walk its closure.

## The walk

1. **Start from the META.** Not from a leaf, and not from a filtered issue list:
   pull the whole tree, closed tickets included.
2. **Print the tree with each ticket's type and state.** The shape shows defects
   on its own: a task under the wrong epic, an epic realizing a story it does
   nothing for, a story nothing realizes.
3. **Collect what the decision touches,** and everything that mentions what it
   touches. The second half is where the surprises are.
4. **Read each ticket in full,** not by its title. Its refinement may already
   have settled the question about to be decided, and settling it again
   differently is worse than leaving it.
5. **Classify each against the list below,** and propose every edit together
   before making any.
6. **Make the edits, then read back** what landed.
7. **Reconcile the board,** if the project keeps one: nothing closed left in a
   working column, nothing finished missing from it. Clearing these needs no
   proposal; moving an open ticket does.

## What goes stale

In roughly the order it causes trouble:

- **An answered question still listed as open.** The worst, because it invites
  someone to decide a settled question again.
- **Superseded reasoning.** A ticket arguing for a mechanism that a decision now
  owns. Replace the argument with a link to the decision.
- **A rejected alternative recorded in a ticket.** It belongs in the ADR's
  alternatives, which is where the project remembers what it ruled out.
- **A concrete list as a technical criterion.** "The footer carries links A, B
  and C" on a component ticket accepts a hardcoded list, when the feature is
  that an editor composes the footer. The want belongs in the STORY: as an
  editor, I want to curate the footer, so that when we decide it must carry A, B
  and C, I can compose that. The technical ticket then requires that nothing is
  hardcoded.
- **An unsourced idea presented as a requirement.** Someone's plausible
  instinct, written into a refinement and later read as a stakeholder's ask.
  Mark it unsourced and leave it out of the first delivery. If it is really
  wanted, the request will come back with a reason.
- **Assumed scope.** "Every tenant needs this." Usually unevidenced, and it
  hardens into a model that cannot express absence. Prefer a mechanism any
  participant can adopt, and make absence a state the model can hold.
- **A boundary nobody drew.** Two things treated as one because one consumer
  cannot tell them apart. If they differ under editing, under caching, or under
  the question "why is this here?", they are two concepts and need two names.
  Promoting one to a defined entity is the maintainers' decision.
- **A term coined in a ticket and used as if settled.** Promote it to the
  glossary, or stop using it as a term.
- **One acceptance line covering two mechanisms.** Split it, or narrow it and
  point to the sibling story.
- **A dangling reference.** A ticket number cited with nothing saying what it
  is.
