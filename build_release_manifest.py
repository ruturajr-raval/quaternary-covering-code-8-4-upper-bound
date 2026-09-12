#!/usr/bin/env python3
"""Build the closed-world SHA-256 manifest from Git-tracked files."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "release-manifest.sha256"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    paths = sorted(
        Path(item.decode("utf-8")).as_posix()
        for item in completed.stdout.split(b"\0")
        if item
    )
    paths = [path for path in paths if path != MANIFEST.name]
    if not paths:
        raise ValueError("no tracked files are available for the manifest")
    MANIFEST.write_text(
        "\n".join(f"{digest(ROOT / path)}  {path}" for path in paths) + "\n",
        encoding="ascii",
    )
    print(f"manifest_files={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
