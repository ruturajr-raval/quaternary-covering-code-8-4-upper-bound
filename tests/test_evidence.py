from __future__ import annotations

import unittest

import audit_evidence


class EvidenceTests(unittest.TestCase):
    def test_committed_evidence_matches_computation(self) -> None:
        self.assertEqual(audit_evidence.main(), 0)


if __name__ == "__main__":
    unittest.main()
