#!/usr/bin/env python3
"""Verify paper-inclusive candidate release assets and checksums."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import tarfile

from build_paper_bundle import MEMBERS


ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / "dist" / "release"
PREFIX = "quaternary-covering-code-8-4-upper-bound-v0.1.0"
PDF_NAME = f"{PREFIX}-paper.pdf"
SOURCE_NAME = f"{PREFIX}-paper-source.tar.gz"
CHECKSUM_NAME = "SHA256SUMS"
EXPECTED_NAMES = {PDF_NAME, SOURCE_NAME, CHECKSUM_NAME}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def verify_pdf(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"missing regular PDF: {path}")
    if path.stat().st_size < 1024 or path.read_bytes()[:5] != b"%PDF-":
        raise ValueError(f"invalid PDF: {path}")


def verify_source(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"missing regular source archive: {path}")
    with tarfile.open(path, mode="r:gz") as archive:
        entries = archive.getmembers()
        names = [entry.name for entry in entries]
        expected = [member.as_posix() for member in MEMBERS]
        if names != expected:
            raise ValueError(
                f"source archive members changed: {names}"
            )
        for entry, relative in zip(entries, MEMBERS):
            if not entry.isfile() or entry.issym() or entry.islnk():
                raise ValueError(f"unsafe source member: {entry.name}")
            if (
                entry.mode != 0o644
                or entry.mtime != 0
                or entry.uid != 0
                or entry.gid != 0
            ):
                raise ValueError(
                    f"nondeterministic source metadata: {entry.name}"
                )
            extracted = archive.extractfile(entry)
            if extracted is None:
                raise ValueError(f"unreadable source member: {entry.name}")
            if extracted.read() != (ROOT / relative).read_bytes():
                raise ValueError(f"source content mismatch: {entry.name}")


def verify_checksums(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"missing checksum manifest: {path}")
    entries: dict[str, str] = {}
    for line_number, line in enumerate(
        path.read_text(encoding="ascii").splitlines(),
        start=1,
    ):
        try:
            expected, name = line.split("  ", 1)
        except ValueError as error:
            raise ValueError(
                f"malformed checksum line {line_number}"
            ) from error
        if SHA256_RE.fullmatch(expected) is None:
            raise ValueError(f"invalid checksum line {line_number}")
        candidate = Path(name)
        if (
            candidate.is_absolute()
            or len(candidate.parts) != 1
            or name in entries
        ):
            raise ValueError(f"invalid asset name: {name}")
        entries[name] = expected
    if set(entries) != {PDF_NAME, SOURCE_NAME}:
        raise ValueError(f"checksum asset set changed: {sorted(entries)}")
    for name, expected in entries.items():
        if digest(RELEASE_DIR / name) != expected:
            raise ValueError(f"checksum mismatch: {name}")


def main() -> int:
    if not RELEASE_DIR.is_dir() or RELEASE_DIR.is_symlink():
        raise ValueError(f"missing release directory: {RELEASE_DIR}")
    names = {path.name for path in RELEASE_DIR.iterdir()}
    if names != EXPECTED_NAMES:
        raise ValueError(f"release asset set changed: {sorted(names)}")
    verify_pdf(RELEASE_DIR / PDF_NAME)
    verify_source(RELEASE_DIR / SOURCE_NAME)
    verify_checksums(RELEASE_DIR / CHECKSUM_NAME)
    print(f"verified_release_assets={len(EXPECTED_NAMES)}")
    print(f"paper_sha256={digest(RELEASE_DIR / PDF_NAME)}")
    print(f"source_sha256={digest(RELEASE_DIR / SOURCE_NAME)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
