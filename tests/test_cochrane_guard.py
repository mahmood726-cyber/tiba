"""Tests for the Cochrane-trademark pre-push guard (R1 mitigation, spec §8)."""
from pathlib import Path

import pytest

from scripts.pre_push_cochrane_guard import find_violations, main


def test_clean_text_passes(tmp_path: Path) -> None:
    f = tmp_path / "README.md"
    f.write_text("Tiba is an evidence synthesis framework.\n", encoding="utf-8")
    assert find_violations([f]) == []


def test_cochrane_in_readme_violates(tmp_path: Path) -> None:
    f = tmp_path / "README.md"
    f.write_text("Tiba is the African Cochrane.\n", encoding="utf-8")
    violations = find_violations([f])
    assert len(violations) == 1
    assert violations[0].path == f
    assert violations[0].line_no == 1
    assert "cochrane" in violations[0].matched_text.lower()


def test_case_insensitive(tmp_path: Path) -> None:
    f = tmp_path / "README.md"
    f.write_text("See COCHRANE handbook.\n", encoding="utf-8")
    assert len(find_violations([f])) == 1


def test_paper_citation_is_allowlisted(tmp_path: Path) -> None:
    papers_dir = tmp_path / "docs" / "papers" / "diagnostic"
    papers_dir.mkdir(parents=True)
    f = papers_dir / "draft.md"
    f.write_text("Higgins JPT, Thomas J, eds. Cochrane Handbook v6.5.\n", encoding="utf-8")
    assert find_violations([f], repo_root=tmp_path) == []


def test_outside_papers_dir_still_blocks(tmp_path: Path) -> None:
    # site/index.html is now allowlisted (generated artifact); use a different
    # file to verify the guard still fires for non-allowlisted site files.
    other_dir = tmp_path / "site"
    other_dir.mkdir()
    f = other_dir / "about.html"
    f.write_text("Cochrane reviews are great\n", encoding="utf-8")
    assert len(find_violations([f], repo_root=tmp_path)) == 1


def test_manifesto_disclaimer_is_allowlisted(tmp_path: Path) -> None:
    f = tmp_path / "MANIFESTO.md"
    f.write_text("Not affiliated with the Cochrane Collaboration.\n", encoding="utf-8")
    assert find_violations([f], repo_root=tmp_path) == []


def test_guard_source_is_allowlisted(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    f = scripts / "pre_push_cochrane_guard.py"
    f.write_text("PATTERN = re.compile(r'cochrane', re.IGNORECASE)\n", encoding="utf-8")
    assert find_violations([f], repo_root=tmp_path) == []


def test_guard_test_file_is_allowlisted(tmp_path: Path) -> None:
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    f = tests_dir / "test_cochrane_guard.py"
    f.write_text("f.write_text('Cochrane review\\n')\n", encoding="utf-8")
    assert find_violations([f], repo_root=tmp_path) == []


def test_install_hook_script_is_allowlisted(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    f = scripts / "install_pre_push_hook.ps1"
    f.write_text("# Tiba Cochrane-trademark guard\n", encoding="utf-8")
    assert find_violations([f], repo_root=tmp_path) == []


def test_superpowers_docs_are_allowlisted(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs" / "superpowers" / "specs"
    docs_dir.mkdir(parents=True)
    f = docs_dir / "2026-05-05-tiba-design.md"
    f.write_text("Cochrane trademark posture: independent organisation.\n", encoding="utf-8")
    assert find_violations([f], repo_root=tmp_path) == []


def test_readme_trademark_section_is_allowlisted(tmp_path: Path) -> None:
    f = tmp_path / "README.md"
    f.write_text("**Not affiliated with the Cochrane Collaboration.**\n", encoding="utf-8")
    assert find_violations([f], repo_root=tmp_path) == []


def test_hook_mode_uses_ls_tree_not_diff_cached(tmp_path: Path, monkeypatch) -> None:
    """Regression: hook mode must use git ls-tree HEAD (pre-push semantics),
    not git diff --cached (pre-commit semantics)."""
    import subprocess

    captured: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        captured.append(list(cmd))
        return subprocess.CompletedProcess(
            args=cmd, returncode=0, stdout="", stderr=""
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    rc = main([])
    assert captured, "hook mode should have invoked subprocess.run"
    cmd = captured[0]
    assert "ls-tree" in cmd, f"hook mode must use git ls-tree, got: {cmd}"
    assert "--cached" not in cmd, f"hook mode must NOT use --cached: {cmd}"
    assert rc == 0  # empty file list -> no violations


def test_index_template_is_allowlisted(tmp_path: Path) -> None:
    d = tmp_path / "site" / "templates"
    d.mkdir(parents=True)
    f = d / "index.html.j2"
    f.write_text("Not affiliated with the Cochrane Collaboration.\n", encoding="utf-8")
    assert find_violations([f], repo_root=tmp_path) == []


def test_renderer_test_file_is_allowlisted(tmp_path: Path) -> None:
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    f = tests_dir / "test_renderer.py"
    f.write_text('assert "Not affiliated with the Cochrane Collaboration" in html\n', encoding="utf-8")
    assert find_violations([f], repo_root=tmp_path) == []


def test_generated_index_html_is_allowlisted(tmp_path: Path) -> None:
    d = tmp_path / "site"
    d.mkdir()
    f = d / "index.html"
    f.write_text("Not affiliated with the Cochrane Collaboration.\n", encoding="utf-8")
    assert find_violations([f], repo_root=tmp_path) == []
