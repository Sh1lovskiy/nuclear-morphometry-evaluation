"""Explicit safe inputs for one-field masks and compact scalar archives."""

import csv
import hashlib
import io
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

import numpy as np

from .domain import Mask, validate_mask


def load_mask(path: Path) -> Mask:
    """Read a bounded uncompressed NPY mask without pickle execution."""
    if path.suffix.lower() != ".npy" or path.stat().st_size > 9_000_000:
        raise ValueError("Supply one NPY label mask smaller than 9 MB")
    mask = np.load(path, allow_pickle=False, mmap_mode="r")
    return validate_mask(mask)


def result_directory() -> Path:
    return Path(__file__).with_name("results")


def _bounded_regular_bytes(path: Path, bound: int) -> bytes:
    """Reject aliases before opening and bound both metadata and actual reads."""
    path = path.absolute()
    component = Path(path.anchor)
    for part in path.parts[1:]:
        component /= part
        if component.is_symlink():
            raise ValueError("Result input path must not contain symbolic links")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > bound:
            raise ValueError("Result input must be a bounded regular file")
        payload = stream.read(bound + 1)
    if len(payload) != info.st_size or len(payload) > bound:
        raise ValueError("Result input size changed or exceeded its bound")
    return payload


def verified_tables(directory: Path) -> dict[str, list[dict[str, str]]]:
    """Check supplied integrity descriptions; caller manifests are not authentication."""
    raw = _bounded_regular_bytes(directory / "manifest.json", 1_000_000)
    try:
        manifest: dict[str, Any] = json.loads(raw)
    except RecursionError as error:
        raise ValueError("Result manifest nesting is excessive") from error
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), dict):
        raise ValueError("Result manifest must contain a files mapping")
    if not 1 <= len(manifest["files"]) <= 32:
        raise ValueError("Result manifest must describe between one and 32 tables")
    result = {}
    total_bytes = 0
    for name, pin in manifest["files"].items():
        if Path(name).name != name or "\\" in name or not name.endswith(".csv"):
            raise ValueError("Result manifest contains an unsafe filename")
        if (
            not isinstance(pin, dict)
            or type(pin.get("bytes")) is not int
            or not 0 <= pin["bytes"] <= 10_000_000
            or type(pin.get("rows")) is not int
            or not 0 <= pin["rows"] <= 100_000
            or not isinstance(pin.get("sha256"), str)
            or re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]) is None
        ):
            raise ValueError("Result manifest has an invalid table identity")
        total_bytes += pin["bytes"]
        if total_bytes > 32_000_000:
            raise ValueError("Combined scalar input exceeds its 32 MB bound")
        path = directory / name
        payload = _bounded_regular_bytes(path, 10_000_000)
        if len(payload) != pin["bytes"] or hashlib.sha256(payload).hexdigest() != pin["sha256"]:
            raise ValueError(f"Result integrity mismatch: {name}")
        rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8"))))
        if len(rows) != pin["rows"]:
            raise ValueError(f"Result row count mismatch: {name}")
        result[name] = rows
    return result
