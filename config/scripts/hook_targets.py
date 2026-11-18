"""Check that the targets CI invokes make no interactive assumptions.

CI runs the same `make` targets a developer runs, deliberately: one entry
point means a green pipeline is evidence about the command people actually
use. The cost is that a target written on a laptop can quietly depend on the
laptop.

`docker compose run` allocates a pseudo-TTY when the service asks for one, and
the app service sets `tty: true`. A developer has a terminal, so the target
works; a runner has none, so it dies with `the input device is not a TTY` and
says nothing about the check it was meant to perform.

So any target reachable from a prek hook must pass `-T`. The set is derived
from the hook entries rather than listed here, because a list would need
maintaining and would omit the hook somebody adds tomorrow. Targets that are
interactive by design, `db.psql` or `app.shell`, are not in that set and are
none of this script's business.

"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / ".pre-commit-config.yaml"

TARGET = re.compile(r"\bmake\s+([A-Za-z_][\w.-]*)")
INTERACTIVE = re.compile(r"docker compose (run|exec)\b")


def hook_targets() -> list[str]:
    """Return every make target a prek hook invokes."""
    config = yaml.safe_load(CONFIG.read_text())
    entries = [
        hook.get("entry", "") for repo in config["repos"] for hook in repo["hooks"]
    ]
    targets = {match for entry in entries for match in TARGET.findall(entry)}
    return sorted(targets)


def recipe(target: str) -> tuple[str, str | None]:
    """Expand a target's recipe without running it.

    Returns the expanded commands, and an error if make could not expand them.

    """
    result = subprocess.run(  # noqa: S603
        ["make", "--dry-run", "--no-print-directory", target],  # noqa: S607
        capture_output=True,
        cwd=ROOT,
        text=True,
    )

    if result.returncode != 0:
        return "", result.stderr.strip()

    # A recipe is printed as it is written, so a command spanning several lines
    # has to be rejoined before its flags can be read.
    return result.stdout.replace("\\\n", " "), None


def main() -> int:
    """Check every hook-invoked target for an interactive compose call."""
    problems: list[str] = []

    for target in hook_targets():
        commands, error = recipe(target)

        if error:
            problems.append(f"{target}: make could not expand this target\n    {error}")
            continue

        for command in commands.splitlines():
            collapsed = " ".join(command.split())
            if INTERACTIVE.search(collapsed) and " -T" not in collapsed:
                problems.append(f"{target}: needs -T\n    {collapsed}")

    for problem in problems:
        print(problem, file=sys.stderr)

    if problems:
        print(
            "\nA target the pipeline invokes cannot ask for a terminal: CI has "
            "none, and the failure names the TTY rather than the check.",
            file=sys.stderr,
        )

    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
