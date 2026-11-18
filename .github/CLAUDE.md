# CLAUDE.md: Git Flow, CI and GitHub

How to work with branches, pull requests and the pipelines in this repository.
Tickets and The Process are in the root `CLAUDE.md`.

## Git Flow

- **Integration branch:** `development.v2`. Branches are `ida/#N`, cut from it,
  and every PR targets it.
- **`master` is v1,** in production. Never target it.
- **Linear history:** after a merge to `development.v2`, rebase every active
  branch onto it. Never merge `development.v2` into a branch.

```bash
git fetch origin
git rebase origin/development.v2
```

## Pipelines

- **Integrate** (`workflows/integrate.yml`) runs on every push to every branch,
  and on PRs from forks once they are ready for review. A red pipeline is a
  review in itself: do not request a review on a failing build.
- Its `metadata` job runs only the jobs whose files changed since the branch's
  last green run, or since it left `development.v2` if it has none. A change to
  the pipeline's own configuration counts for every job it configures.
- **Deploy** (`workflows/deploy.yml`) is manual. A maintainer dispatches it
  against `development.v2`, and it refuses any other ref. There is no automatic
  CD.

```bash
gh workflow run deploy.yml --ref development.v2
```

### Conventions the guards hold

- Every prek hook belongs to exactly one section of `hook-jobs.yml`: `app`,
  `ui`, `terraform`, `shared` or `local`. Each `SKIP_*` list in `integrate.yml`
  is its job's complement. The `hook-jobs` hook fails on an unclassified hook or
  a list that has drifted.
- A make target a hook calls passes `-T` to `docker compose run` and `exec`,
  because CI has no terminal (`hook-targets`).
- Images build through `actions/build-image`, at a target listed in its
  `targets.yml`. The `hook-images` hook checks that each target is a stage of
  its Dockerfile.

### Conventions nothing checks

- A step that needs a database runs the built image with `--network host`
  against the job's service containers. Compose mounts local secrets and starts
  databases of its own.
- Third-party actions are pinned by commit SHA, with the version in a comment.
  `actions/*` stay on major tags.

## Pull Requests

Follow `.github/PULL_REQUEST_TEMPLATE.md`.

- **Title:** the branch, a pipe, then a short description:
  `ida/#N | short description`.
- **Tickets:** reference them as bare `#N`, never with `fixes`, `closes` or
  `resolves`. Merging closes nothing; the board is reconciled by hand.
- **Before drafting a PR,** once the gates pass, review the whole diff
  adversarially against its base (`git diff origin/development.v2...HEAD`).
  Drive how it fails, not only that it works. Read it line by line for
  leftovers, and check file modes: scripts are `100755`. Fix what it finds, and
  say in the PR body that it ran. Green gates are not this review.
- **Merge** with a merge commit only, never squash or rebase:

```bash
gh pr merge N --merge --delete-branch
```

## Reviewing CI

```bash
gh run list --branch 'ida/#N'      # runs for a branch
gh run view RUN_ID --log-failed    # logs of the failed steps
```
