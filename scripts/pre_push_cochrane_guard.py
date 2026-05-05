"""Tiba pre-push guard: blocks 'cochrane' (case-insensitive) outside docs/papers/.

Spec mitigation R1: prevents accidental trademark drift in shipped copy.
Allowlist: academic-citation context inside docs/papers/ only.

Usage (manual):  python scripts/pre_push_cochrane_guard.py [files...]
Hook usage:      installed by scripts/install_pre_push_hook.ps1 to .git/hooks/pre-push
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

PATTERN = re.compile(r"cochrane", re.IGNORECASE)


@dataclass(frozen=True)
class Violation:
    path: Path
    line_no: int
    matched_text: str


def _is_allowlisted(path: Path, repo_root: Path) -> bool:
    """Allow occurrences inside docs/papers/** (academic-citation context)."""
    try:
        rel = path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return False
    parts = rel.parts
    return len(parts) >= 2 and parts[0] == "docs" and parts[1] == "papers"


def find_violations(
    files: Iterable[Path], repo_root: Path | None = None
) -> list[Violation]:
    repo_root = repo_root or Path.cwd()
    violations: list[Violation] = []
    for f in files:
        if not f.is_file():
            continue
        if _is_allowlisted(f, repo_root):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for m in PATTERN.finditer(line):
                violations.append(
                    Violation(path=f, line_no=line_no, matched_text=m.group(0))
                )
    return violations


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        # Hook mode: scan staged files via git
        import subprocess

        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True,
        )
        files = [Path(p) for p in result.stdout.splitlines() if p.strip()]
    else:
        files = [Path(p) for p in argv[1:]]

    violations = find_violations(files)
    if not violations:
        return 0
    print("TIBA TRADEMARK GUARD — 'Cochrane' found in non-allowlisted files:", file=sys.stderr)
    for v in violations:
        print(f"  {v.path}:{v.line_no}  {v.matched_text!r}", file=sys.stderr)
    print(
        "Allowlist: docs/papers/** (academic citations). "
        "If this is a citation, move it under docs/papers/. "
        "Otherwise rephrase. Bypass: SKIP_TIBA_GUARD=1 git push (logged).",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
