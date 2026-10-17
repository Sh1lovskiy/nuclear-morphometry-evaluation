"""Small CPU-only interface with no implicit data download or model loading."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .adapters import load_mask
from .analysis import explain_deletions
from .evaluation import evaluate
from .examples import synthetic_masks
from .replay import reproduce


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Population-aware nuclear morphometry evaluation")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Run a labeled synthetic mask example offline")
    demo.add_argument(
        "--write-masks", type=Path, help="Write new NPY fixture masks in this directory"
    )
    evaluate_parser = commands.add_parser("evaluate", help="Evaluate one pair of NPY label masks")
    evaluate_parser.add_argument("reference", type=Path)
    evaluate_parser.add_argument("prediction", type=Path)
    evaluate_parser.add_argument("--min-area", type=int, default=16)
    explain = commands.add_parser("explain", help="Recompute a specified joint object deletion")
    explain.add_argument("reference", type=Path)
    explain.add_argument("--remove", type=int, nargs="+", required=True)
    explain.add_argument("--min-area", type=int, default=16)
    replay = commands.add_parser("reproduce", help="Verify and replay included scalar tables only")
    replay.add_argument(
        "--results", type=Path, help="Canonical scalar directory with manifest.json"
    )
    args = parser.parse_args(argv)
    result: Any
    try:
        if args.command == "demo":
            reference, square, rectangle = synthetic_masks()
            if args.write_masks is not None:
                import numpy as np

                args.write_masks.mkdir(parents=True, exist_ok=True)
                for name, mask in [
                    ("reference", reference),
                    ("square_deleted", square),
                    ("rectangle_deleted", rectangle),
                ]:
                    with (args.write_masks / f"{name}.npy").open("xb") as handle:
                        np.save(handle, mask, allow_pickle=False)
            result = {
                "scope": "Synthetic fixture: two squares and one rectangle, not microscopy",
                "delete_square": evaluate(reference, square),
                "delete_rectangle": evaluate(reference, rectangle),
            }
        elif args.command == "evaluate":
            result = evaluate(load_mask(args.reference), load_mask(args.prediction), args.min_area)
        elif args.command == "explain":
            result = explain_deletions(load_mask(args.reference), args.remove, args.min_area)
        else:
            result = reproduce(args.results)
    except (ValueError, TypeError, OSError, KeyError) as error:
        print(f"Input or scientific integrity error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
