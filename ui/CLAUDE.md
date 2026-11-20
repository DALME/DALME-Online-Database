# ui/CLAUDE.md

Frontend guidance. The root `CLAUDE.md` holds the project-wide rules, gates and
commands.

## Stack

Quasar 2 on Vite, with Vue 3, in JavaScript. State lives in Pinia, with
pinia-orm models in `src/models/`. XState machines run inside Pinia stores
through `src/use/xstore.js`, and the OAuth machine is `src/stores/auth.js`.
The boot files are `axios`, `markdown` and `openLayers` (`quasar.config.js`).

Run everything through make: `make ui.lint`, `make ui.format` and `make ui.test`.
After changing a dependency, run `make ui.sync`.

## Tests

Vitest, through the Quasar extension (`vitest.config.js`). Tests live in two
places: specs under `test/vitest/__tests__/`, mirroring `src/`, and inline in a
source module under `if (import.meta.vitest)`. CI runs the suite in the built
image, without coverage.

New behaviour arrives with its tests, and a bug gets a failing regression test
before its fix.

## Retired code

`src/use/editing-bak.js` is the retired windowing system (`provideEditing`).
Nothing imports it. It stays as the reference for extracting that system, so
leave it alone.
