from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from tools.build_paper_bundle import build_bundle


class ReleaseAssetTests(unittest.TestCase):
    def test_paper_source_bundle_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.tar.gz"
            second = Path(directory) / "second.tar.gz"
            build_bundle(first)
            build_bundle(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())


if __name__ == "__main__":
    unittest.main()
