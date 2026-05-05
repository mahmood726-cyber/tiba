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
    """Allow occurrences inside docs/papers/** OR the trademark-disclaimer file MANIFESTO.md."""
    try:
        rel = path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return False
    parts = rel.parts
    # Academic-citation context: docs/papers/**
    if len(parts) >= 2 and parts[0] == "docs" and parts[1] == "papers":
        return True
    # Trademark-disclaimer manifesto (intentional disclaimer language).
    if len(parts) == 1 and parts[0] == "MANIFESTO.md":
        return True
    # Guard source: contains the regex literal and docstrings as implementation necessity.
    if len(parts) == 2 and parts[0] == "scripts" and parts[1] == "pre_push_cochrane_guard.py":
        return True
    # Guard installer: names the guard script in comments and hook body.
    if len(parts) == 2 and parts[0] == "scripts" and parts[1] == "install_pre_push_hook.ps1":
        return True
    # Guard test suite: explicitly tests for Cochrane detection by name.
    if len(parts) == 2 and parts[0] == "tests" and parts[1] == "test_cochrane_guard.py":
        return True
    # Renderer test suite: asserts the template's non-affiliation disclaimer text.
    if len(parts) == 2 and parts[0] == "tests" and parts[1] == "test_renderer.py":
        return True
    # Internal design and implementation docs (docs/superpowers/**): trademark posture sections.
    if len(parts) >= 2 and parts[0] == "docs" and parts[1] == "superpowers":
        return True
    # README.md: contains the project-level trademark disclaimer.
    if len(parts) == 1 and parts[0] == "README.md":
        return True
    # Jinja2 templates: site/templates/** — only "Not affiliated" disclaimer in footer.
    if len(parts) >= 2 and parts[0] == "site" and parts[1] == "templates":
        return True
    return False


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
        # Hook mode (pre-push): scan ALL tracked files at HEAD.
        # Pre-push semantics: the staging area is irrelevant; we must check what's
        # actually being shipped. ls-tree is bulletproof for small repos (<1s) and
        # avoids the edge cases of pre-push stdin parsing (first push, force push,
        # branch deletion). Trade-off: scans the whole tree on every push.
        import subprocess

        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "HEAD"],
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
    print("TIBA TRADEMARK GUARD - 'Cochrane' found in non-allowlisted files:", file=sys.stderr)
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
