"""Public adaptation of Morgenstern's media validator. Standard library only.

The private configuration adapter is removed. This sample adds strict report
validation, finite duration checks and a subprocess timeout. See PROVENANCE.md.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path
from typing import Any


class MediaValidationError(ValueError):
    """The artifact cannot pass the selected delivery gate."""


def validate_report(data: Any, kind: str, minimum: float = 0.0) -> float:
    """Validate an ffprobe report, returning a finite duration in seconds.

    Video delivery here requires an audio track. Silent video is rejected by
    policy, even though it may be a perfectly valid media file.
    """
    if kind not in {"audio", "video"}:
        raise MediaValidationError("kind must be audio or video")
    if not math.isfinite(minimum) or minimum < 0:
        raise MediaValidationError("minimum must be finite and non-negative")
    if not isinstance(data, dict) or not isinstance(data.get("streams"), list):
        raise MediaValidationError("missing or invalid stream report")
    streams = data["streams"]
    if any(not isinstance(stream, dict) for stream in streams):
        raise MediaValidationError("invalid stream entry")
    types = {stream.get("codec_type") for stream in streams if isinstance(stream.get("codec_type"), str)}
    required = {"audio"} if kind == "audio" else {"audio", "video"}
    if not required <= types:
        raise MediaValidationError("required streams missing: " + ", ".join(sorted(required - types)))
    try:
        raw = data["format"]["duration"]
        if isinstance(raw, bool):
            raise ValueError("boolean duration")
        duration = float(raw)
    except (KeyError, TypeError, ValueError) as exc:
        raise MediaValidationError("missing or invalid duration") from exc
    if not math.isfinite(duration) or duration <= minimum:
        raise MediaValidationError("duration must be finite and exceed minimum")
    return duration


def probe_media(path: Path, kind: str, minimum: float = 0.0, ffprobe: str = "ffprobe") -> dict:
    """Probe one local artifact. No shell, providers, credentials or network."""
    if not path.is_file() or path.stat().st_size == 0:
        raise MediaValidationError("file missing or empty")
    try:
        result = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration:stream=codec_type",
             "-of", "json", str(path.resolve())],
            capture_output=True, text=True, check=False, timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise MediaValidationError("ffprobe unavailable or timed out") from exc
    if result.returncode:
        raise MediaValidationError("ffprobe rejected the artifact")
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise MediaValidationError("ffprobe returned invalid JSON") from exc
    duration = validate_report(report, kind, minimum)
    return {"ok": True, "kind": kind, "duration_seconds": duration, "bytes": path.stat().st_size}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--kind", choices=["audio", "video"], default="audio")
    parser.add_argument("--minimum", type=float, default=0)
    parser.add_argument("--ffprobe", default="ffprobe")
    args = parser.parse_args()
    try:
        print(json.dumps(probe_media(args.path, args.kind, args.minimum, args.ffprobe), sort_keys=True))
        return 0
    except MediaValidationError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
