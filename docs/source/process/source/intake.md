(the-process-intake)=
# Intake and triage

Not all work starts as a tidy story. Much of it starts as someone noticing
something (a bug, an awkward flow, a wish) and saying so. We want that to be
easy, and we want it to feed the model rather than bypass it.

## One door

The rolling **INTAKE** ticket,
[#49](https://github.com/DALME/DALME-Online-Database/issues/49), is the single
place to raise anything, with no need to understand the rest of the taxonomy.
Items are filed as sub-issues of it; the **Feature** and **Bug** templates start
there by default. The intake is untriaged by design: an inbox awaiting
processing.

## Triage

Every intake item resolves in one of three ways:

- **A bug** means some STORY's outcome is not true in the running system: a
  failed acceptance criterion. It becomes a TASK, FIX or small EPIC filed under
  the relevant META and linked to the story it violates. A bug with no domain
  narrative to serve, such as a broken build, can stand alone.
- **A wish** is a user story in raw form: "I wish I could…" is one edit away
  from "as a *…*, I want to *…*, so that *…*". It is promoted to a STORY under the
  appropriate META. This is the channel through which the people who use the
  system feed its domain model.
- **Noise, duplicates and won't-fixes** are closed.

## Keep it light

The intake is a queue, and that is the whole mechanism. Triage either refiles an
item or promotes it. We add machinery only when the work forces us to.
