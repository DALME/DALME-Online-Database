"""Check that every prek hook is assigned to an integrate job.

`integrate.yml` runs the whole hook set in each job and narrows it with a
`SKIP` list. Because a `SKIP` list is written by subtraction, a hook nobody
remembered to exclude runs everywhere, which is invisible until a job fails on
a toolchain it has no use for.

`.github/hook-jobs.yml` states the intent positively. This script holds the
three files to it:

1. Every hook in `.pre-commit-config.yaml` is classified exactly once.
2. Nothing is classified that is not a hook.
3. Each `SKIP` list is exactly the complement of the job it belongs to.

"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / ".pre-commit-config.yaml"
JOBS = ROOT / ".github" / "hook-jobs.yml"
WORKFLOW = ROOT / ".github" / "workflows" / "integrate.yml"

SKIP_LISTS = {"app": "SKIP_APP", "terraform": "SKIP_TF", "ui": "SKIP_UI"}
JOB_NAMES = (*SKIP_LISTS, "shared", "local")


def configured_hooks() -> set[str]:
    """Return every hook id declared in the prek configuration."""
    config = yaml.safe_load(CONFIG.read_text())
    return {hook["id"] for repo in config["repos"] for hook in repo["hooks"]}


def classified_hooks() -> dict[str, list[str]]:
    """Return the declared job for every hook."""
    jobs = yaml.safe_load(JOBS.read_text())
    return {name: list(jobs.get(name) or []) for name in JOB_NAMES}


def skip_lists() -> dict[str, set[str]]:
    """Return the SKIP list each integrate job is run with."""
    env = yaml.safe_load(WORKFLOW.read_text())["env"]
    return {
        job: {hook for hook in env[var].split(",") if hook}
        for job, var in SKIP_LISTS.items()
    }


def report(problems: list[str]) -> int:
    """Print each problem and return the exit status."""
    for problem in problems:
        print(problem, file=sys.stderr)

    if problems:
        print(
            f"\nClassify each hook in {JOBS.relative_to(ROOT)} and keep the "
            f"SKIP lists in {WORKFLOW.relative_to(ROOT)} as their complement.",
            file=sys.stderr,
        )

    return 1 if problems else 0


def main() -> int:
    """Check the hook classification against the config and the workflow."""
    configured = configured_hooks()
    classified = classified_hooks()
    problems: list[str] = []

    seen: dict[str, str] = {}
    for job, hooks in classified.items():
        for hook in hooks:
            if hook in seen:
                problems.append(
                    f"{hook}: classified twice, as {seen[hook]} and as {job}"
                )
            seen[hook] = job

    for hook in sorted(configured - set(seen)):
        problems.append(
            f"{hook}: a hook with no job. Add it to one of {', '.join(JOB_NAMES)}"
        )

    for hook in sorted(set(seen) - configured):
        problems.append(f"{hook}: classified but not a hook in the prek config")

    # An unclassified hook makes every complement check downstream of it fail
    # as well, which buries the one problem worth reading under noise.
    if problems:
        return report(problems)

    # A job runs everything except the hooks belonging to the other jobs and
    # the ones that never run in CI at all.
    expected = {
        job: set(classified["local"]).union(
            *(classified[other] for other in SKIP_LISTS if other != job)
        )
        for job in SKIP_LISTS
    }

    for job, skip in skip_lists().items():
        for hook in sorted(expected[job] - skip):
            problems.append(f"{hook}: runs in the {job} job but is not declared for it")
        for hook in sorted(skip - expected[job]):
            problems.append(f"{hook}: skipped in the {job} job but declared for it")

    return report(problems)


if __name__ == "__main__":
    raise SystemExit(main())
