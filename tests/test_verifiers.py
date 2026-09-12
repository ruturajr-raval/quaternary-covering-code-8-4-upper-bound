from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from independent_verify import verify as independent_verify
from verify_code import parse_code, verify_path


ROOT = Path(__file__).resolve().parents[1]


class VerifierTests(unittest.TestCase):
    def test_27_word_code_covers(self) -> None:
        path = ROOT / "data" / "code-27.txt"
        primary = verify_path(path, expected_size=27)
        independent = independent_verify(path, 27)
        self.assertTrue(primary["valid"])
        self.assertEqual(primary["exact_covering_radius"], 4)
        self.assertEqual(primary["hole_count"], 0)
        self.assertEqual(primary["holes"], independent["holes"])
        self.assertEqual(
            primary["distance_distribution"],
            independent["distance_distribution"],
        )

    def test_26_word_frontier_has_five_holes(self) -> None:
        path = ROOT / "data" / "near-cover-26-5-holes.txt"
        primary = verify_path(path, expected_size=26)
        independent = independent_verify(path, 26)
        self.assertFalse(primary["valid"])
        self.assertEqual(primary["exact_covering_radius"], 5)
        self.assertEqual(primary["hole_count"], 5)
        self.assertEqual(primary["holes"], independent["holes"])
        self.assertEqual(
            primary["distance_distribution"],
            independent["distance_distribution"],
        )

    def test_duplicate_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.txt"
            path.write_text("00000000\n00000000\n", encoding="ascii")
            with self.assertRaises(ValueError):
                parse_code(path)

    def test_bad_symbol_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.txt"
            path.write_text("00000004\n", encoding="ascii")
            with self.assertRaises(ValueError):
                parse_code(path)


if __name__ == "__main__":
    unittest.main()
