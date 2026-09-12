#!/usr/bin/env python3
"""Verify the closed-world SHA-256 manifest for the tracked repository."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess


LINE_RE = re.compile(r"^([0-9a-f]{64})  (.+)$")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("release-manifest.sha256"),
    )
    parser.add_argument("--require-git-completeness", action="store_true")
    arguments = parser.parse_args()
    try:
        manifest = arguments.manifest.resolve()
        root = manifest.parent
        entries: dict[str, str] = {}
        for line_number, line in enumerate(
            manifest.read_text(encoding="ascii").splitlines(),
            start=1,
        ):
            match = LINE_RE.fullmatch(line)
            if match is None:
                raise ValueError(f"malformed manifest line {line_number}")
            expected, relative = match.groups()
            candidate = Path(relative)
            if candidate.is_absolute() or ".." in candidate.parts:
                raise ValueError(f"nonportable path: {relative}")
            if relative == manifest.name or relative in entries:
                raise ValueError(f"invalid manifest path: {relative}")
            entries[relative] = expected
        if not entries:
            raise ValueError("manifest is empty")
        for relative, expected in entries.items():
            path = root / relative
            if not path.is_file() or digest(path) != expected:
                raise ValueError(f"manifest mismatch: {relative}")
        if arguments.require_git_completeness:
            completed = subprocess.run(
                ["git", "-C", str(root), "ls-files", "-z"],
                capture_output=True,
                check=True,
            )
            tracked = {
                Path(os.fsdecode(item)).as_posix()
                for item in completed.stdout.split(b"\0")
                if item
            }
            tracked.discard(manifest.name)
            if set(entries) != tracked:
                raise ValueError("manifest inventory does not match Git")
    except (
        OSError,
        UnicodeError,
        ValueError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"error={error}")
        return 2
    print(f"verified_manifest={arguments.manifest}")
    print(f"verified_files={len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
