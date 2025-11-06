"""Simple utility to bump the patch version in pyproject.toml.

Usage:
    python tools/bump_version.py --part patch
    python tools/bump_version.py --part minor
    python tools/bump_version.py --part major
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"

RE = re.compile(r'^(version\s*=\s*")([0-9]+)\.([0-9]+)\.([0-9]+)(".*)$')


def bump_version(part: str) -> str:
    txt = PYPROJECT.read_text(encoding="utf8")
    lines = txt.splitlines()
    for i, ln in enumerate(lines):
        m = RE.match(ln)
        if m:
            major, minor, patch = int(m.group(2)), int(m.group(3)), int(m.group(4))
            if part == "patch":
                patch += 1
            elif part == "minor":
                minor += 1
                patch = 0
            elif part == "major":
                major += 1
                minor = 0
                patch = 0
            new = f'{m.group(1)}{major}.{minor}.{patch}{m.group(5)}'
            lines[i] = new
            PYPROJECT.write_text("\n".join(lines), encoding="utf8")
            return f"{major}.{minor}.{patch}"
    raise RuntimeError("version not found in pyproject.toml")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--part", choices=("patch", "minor", "major"), default="patch")
    args = p.parse_args()
    new = bump_version(args.part)
    print("Bumped version to", new)
