#!/usr/bin/env python3
"""Build a deterministic source archive for the technical report."""

from __future__ import annotations

import argparse
import gzip
from io import BytesIO
from pathlib import Path
import tarfile


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT
    / "dist"
    / "paper"
    / "quaternary-covering-code-8-4-upper-bound-v0.1.0-paper-source.tar.gz"
)
MEMBERS = (
    Path("paper/main.tex"),
    Path("paper/ARXIV_METADATA.md"),
    Path("README.md"),
    Path("CITATION.cff"),
    Path("LICENSE"),
)


def add_member(archive: tarfile.TarFile, relative: Path) -> None:
    data = (ROOT / relative).read_bytes()
    info = tarfile.TarInfo(relative.as_posix())
    info.size = len(data)
    info.mode = 0o644
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    archive.addfile(info, fileobj=BytesIO(data))


def build_bundle(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=raw,
            mtime=0,
        ) as compressed:
            with tarfile.open(
                fileobj=compressed,
                mode="w",
                format=tarfile.USTAR_FORMAT,
            ) as archive:
                for member in MEMBERS:
                    add_member(archive, member)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    build_bundle(arguments.output)
    print(f"output={arguments.output}")
    print(f"members={len(MEMBERS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
