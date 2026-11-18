"""Check that every target CI builds is a stage of its image's Dockerfile.

The `build-image` action reads the targets each image is built at from
`.github/actions/build-image/targets.yml`, and names its cache scopes after
them. The stages themselves live in the Dockerfiles. Two files stating the
same fact drift apart, and a stage renamed in a Dockerfile would otherwise
surface only as a failed build on CI, or as a cache scope nothing reads.

So the list is held to the Dockerfiles: every image has one, and every listed
target is a stage in it. A stage CI never builds is not a problem; the
Dockerfile is allowed to serve local development as well.

"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
TARGETS = ROOT / ".github" / "actions" / "build-image" / "targets.yml"
DOCKERFILES = ROOT / "config" / "docker"

STAGE = re.compile(r"^\s*FROM\s+\S+\s+AS\s+(\S+)", re.IGNORECASE | re.MULTILINE)


def listed_targets() -> dict[str, list[str]]:
    """Return the targets each image is built at."""
    return {
        image: list(targets or [])
        for image, targets in yaml.safe_load(TARGETS.read_text()).items()
    }


def stages(dockerfile: Path) -> set[str]:
    """Return the name of every stage a Dockerfile declares."""
    return set(STAGE.findall(dockerfile.read_text()))


def main() -> int:
    """Check the listed targets against the Dockerfiles."""
    problems: list[str] = []

    for image, targets in listed_targets().items():
        dockerfile = DOCKERFILES / f"Dockerfile.{image}"
        if not dockerfile.is_file():
            problems.append(f"{image}: no {dockerfile.relative_to(ROOT)}")
            continue

        declared = stages(dockerfile)
        for target in targets:
            if target not in declared:
                problems.append(
                    f"{image}: '{target}' is not a stage of {dockerfile.relative_to(ROOT)} "
                    f"({', '.join(sorted(declared))})"
                )

    for problem in problems:
        print(problem, file=sys.stderr)

    if problems:
        print(
            f"\nKeep {TARGETS.relative_to(ROOT)} to stages the Dockerfiles declare.",
            file=sys.stderr,
        )

    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
