"""
Tests for tools/corpus_cli.py.

Covers:
- validate: passes on valid metadata, fails on invalid
- check: passes when consistent, exits 1 on drift
- sync: idempotency (run twice, output identical)
- sync: drift detection (add unregistered artifact, check fails)
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CLI = REPO_ROOT / "tools" / "corpus_cli.py"
PYTHON = sys.executable


def run_cli(*args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, str(CLI)] + list(args),
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


# ─────────────────────────────────────────────
# validate
# ─────────────────────────────────────────────

def test_validate_passes_on_real_corpus():
    result = run_cli("validate")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "All" in result.stdout
    assert "valid" in result.stdout


def test_validate_fails_on_invalid_metadata(tmp_path):
    """Write a bad metadata.json into a temp corpus-like tree and validate it."""
    seed_dir = tmp_path / "corpus" / "seeds" / "bad-seed"
    seed_dir.mkdir(parents=True)
    bad_meta = {"schema_version": "1.0.0"}  # missing required 'metadata' block
    (seed_dir / "metadata.json").write_text(json.dumps(bad_meta))

    import tools.corpus_cli as cli_module
    import types

    # Redirect both CORPUS_DIR and REPO_ROOT so relative_to() resolves correctly
    orig_corpus = cli_module.CORPUS_DIR
    orig_root = cli_module.REPO_ROOT
    cli_module.CORPUS_DIR = tmp_path / "corpus"
    cli_module.REPO_ROOT = tmp_path
    try:
        args = types.SimpleNamespace()
        rc = cli_module.cmd_validate(args)
    finally:
        cli_module.CORPUS_DIR = orig_corpus
        cli_module.REPO_ROOT = orig_root

    assert rc == 1


# ─────────────────────────────────────────────
# check
# ─────────────────────────────────────────────

def test_check_passes_on_consistent_corpus():
    result = run_cli("check")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "consistent" in result.stdout


def test_check_detects_unregistered_artifact(tmp_path):
    """Adding a metadata.json not in the index causes check to exit 1."""
    import tools.corpus_cli as cli_module
    import types

    # Copy the real index to temp discovery
    real_index_path = REPO_ROOT / "discovery" / "substrate-index.json"
    tmp_discovery = tmp_path / "discovery"
    tmp_discovery.mkdir()
    (tmp_discovery / "substrate-index.json").write_text(real_index_path.read_text())

    # Add a new artifact to corpus that isn't in the copied index
    new_dir = REPO_ROOT / "corpus" / "primitives" / "_test-unregistered-artifact"
    new_dir.mkdir()
    (new_dir / "metadata.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "metadata": {
            "id": "_test-unregistered-artifact",
            "name": "Test",
            "description": "temp",
            "version": "0.0.1",
            "technology": "cloudformation"
        }
    }))

    try:
        orig_discovery = cli_module.DISCOVERY_DIR
        cli_module.DISCOVERY_DIR = tmp_discovery
        args = types.SimpleNamespace()
        rc = cli_module.cmd_check(args)
    finally:
        cli_module.DISCOVERY_DIR = orig_discovery
        import shutil
        shutil.rmtree(new_dir, ignore_errors=True)

    assert rc == 1


# ─────────────────────────────────────────────
# sync — idempotency
# ─────────────────────────────────────────────

def test_sync_is_idempotent():
    """Running sync twice produces identical discovery output."""
    def capture_discovery() -> dict:
        snapshots = {}
        discovery = REPO_ROOT / "discovery"
        for f in sorted(discovery.rglob("*.json")):
            snapshots[str(f.relative_to(discovery))] = f.read_text()
        for f in sorted(discovery.rglob("*.yaml")):
            snapshots[str(f.relative_to(discovery))] = f.read_text()
        return snapshots

    r1 = run_cli("sync")
    assert r1.returncode == 0, r1.stdout + r1.stderr
    snap1 = capture_discovery()

    r2 = run_cli("sync")
    assert r2.returncode == 0, r2.stdout + r2.stderr
    snap2 = capture_discovery()

    assert snap1 == snap2, "sync is not idempotent — discovery output differs between runs"


# ─────────────────────────────────────────────
# list
# ─────────────────────────────────────────────

def test_list_returns_all_artifacts():
    result = run_cli("list")
    assert result.returncode == 0
    assert "reference-webapp" in result.stdout
    assert "static-site-delivery" in result.stdout


def test_list_json_is_valid():
    result = run_cli("list", "--json")
    assert result.returncode == 0
    entries = json.loads(result.stdout)
    assert isinstance(entries, list)
    assert len(entries) == 7


def test_list_type_filter():
    result = run_cli("list", "--type", "seed", "--json")
    assert result.returncode == 0
    entries = json.loads(result.stdout)
    assert all(e["type"] == "seed" for e in entries)
