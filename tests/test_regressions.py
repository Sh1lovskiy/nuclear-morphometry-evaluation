import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from nuclear_morphometry.adapters import result_directory
from nuclear_morphometry.analysis import explain_deletions
from nuclear_morphometry.evaluation import evaluate
from nuclear_morphometry.replay import reproduce


class MaskRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mask = np.repeat(
            np.repeat(np.array([[2**53, 2**53 + 1]], dtype=np.uint64), 4, axis=0), 4, axis=1
        )

    def test_identical_masks_match_distinct_unsigned_ids(self) -> None:
        result = evaluate(self.mask, self.mask)
        self.assertEqual(result["matched_count"], 2)
        self.assertEqual(result["pq"], 1.0)
        self.assertEqual(result["instance_f1"], 1.0)

    def test_explain_deletes_one_large_unsigned_id(self) -> None:
        result = explain_deletions(self.mask, [2**53 + 1])
        reference = self.mask.astype(np.int64)
        expected = explain_deletions(reference, [2**53 + 1])
        self.assertEqual(result, expected)
        self.assertEqual(result["omitted_area_pixels_squared"], 16)

    def test_rejects_unsigned_ids_that_would_overflow(self) -> None:
        invalid = np.array([[2**63]], dtype=np.uint64)
        with self.assertRaisesRegex(ValueError, "nonnegative int64 range"):
            evaluate(invalid, invalid, min_area=1)


class ScalarReplayRegressionTests(unittest.TestCase):
    def test_accepts_a_complete_copy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "results"
            shutil.copytree(result_directory(), bundle)
            replay = reproduce(bundle)
        effects = replay["paired_effects"]
        self.assertIsInstance(effects, list)
        self.assertEqual(len(effects), 6)
        self.assertEqual(replay["margin_rows_verified"], 24)

    def test_rejects_incomplete_or_duplicate_tables_with_matching_caller_hashes(self) -> None:
        for change in ("missing", "headers only", "duplicate effect", "duplicate margin"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                bundle = Path(directory) / "results"
                shutil.copytree(result_directory(), bundle)
                path = bundle / "manifest.json"
                manifest = json.loads(path.read_text(encoding="utf-8"))
                files = manifest["files"]
                if change == "missing":
                    (bundle / "exact_ties.csv").unlink()
                    del files["exact_ties.csv"]
                else:
                    names = (
                        ("field_contrasts.csv", "paired_effects.csv", "margin_sensitivity.csv")
                        if change == "headers only"
                        else (
                            "paired_effects.csv"
                            if change == "duplicate effect"
                            else "margin_sensitivity.csv",
                        )
                    )
                    for name in names:
                        table = bundle / name
                        lines = table.read_bytes().splitlines(keepends=True)
                        lines = lines[:1] if change == "headers only" else lines + lines[1:2]
                        payload = b"".join(lines)
                        table.write_bytes(payload)
                        files[name].update(
                            bytes=len(payload),
                            rows=len(lines) - 1,
                            sha256=hashlib.sha256(payload).hexdigest(),
                        )
                path.write_text(json.dumps(manifest), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "canonical manifest"):
                    reproduce(bundle)
