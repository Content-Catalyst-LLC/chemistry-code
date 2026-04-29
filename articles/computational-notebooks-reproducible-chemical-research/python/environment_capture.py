#!/usr/bin/env python3
"""
Capture a lightweight Python environment manifest for a reproducible
chemical notebook workflow.
"""

from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "outputs" / "manifests"
OUT_DIR.mkdir(parents=True, exist_ok=True)

manifest = {
    "python_version": sys.version,
    "python_executable": sys.executable,
    "platform": platform.platform(),
    "machine": platform.machine(),
    "processor": platform.processor(),
    "responsible_use": "Environment metadata support reproducibility but do not validate chemical conclusions.",
}

with (OUT_DIR / "python_environment_manifest.json").open("w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("Wrote Python environment manifest.")
