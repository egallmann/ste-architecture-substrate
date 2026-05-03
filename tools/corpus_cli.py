#!/usr/bin/env python3
"""
corpus_cli.py — Corpus maintenance CLI for ste-architecture-substrate.

Commands:
  sync      Regenerate discovery/ from corpus/ metadata files.
  validate  Validate all corpus metadata files against JSON Schemas.
  check     Bidirectional integrity check (index ↔ filesystem). Exits 1 on drift.
  list      List registered artifacts (table or JSON).

Usage (from repo root):
  python tools/corpus_cli.py sync
  python tools/corpus_cli.py validate
  python tools/corpus_cli.py check
  python tools/corpus_cli.py list [--type seed|building_block|primitive] [--json]
"""

import argparse
import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

CORPUS_DIR = REPO_ROOT / "corpus"
DISCOVERY_DIR = REPO_ROOT / "discovery"
SCHEMAS_DIR = REPO_ROOT / "schemas"

SEED_SCHEMA = SCHEMAS_DIR / "seed.schema.json"
BUNDLE_SCHEMA = SCHEMAS_DIR / "building-block-bundle.schema.json"
PRIMITIVE_SCHEMA = SCHEMAS_DIR / "primitive-block.schema.json"

TYPE_MAP = {
    "seeds": "seed",
    "building-blocks": "building_block",
    "primitives": "primitive",
}
SCHEMA_MAP = {
    "seed": SEED_SCHEMA,
    "building_block": BUNDLE_SCHEMA,
    "primitive": PRIMITIVE_SCHEMA,
}


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def _write_json_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    tmp.replace(path)


def _write_yaml_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=True, allow_unicode=True)
    tmp.replace(path)


def _walk_corpus() -> list[dict]:
    """Walk corpus/ and return a list of artifact dicts ordered deterministically."""
    artifacts = []
    for type_dir_name, artifact_type in sorted(TYPE_MAP.items()):
        type_dir = CORPUS_DIR / type_dir_name
        if not type_dir.is_dir():
            continue
        for artifact_dir in sorted(type_dir.iterdir()):
            metadata_path = artifact_dir / "metadata.json"
            if not artifact_dir.is_dir() or not metadata_path.exists():
                continue
            try:
                meta = _load_json(metadata_path)
            except Exception as exc:
                print(f"  ERROR reading {metadata_path.relative_to(REPO_ROOT)}: {exc}", file=sys.stderr)
                continue
            artifacts.append({
                "artifact_type": artifact_type,
                "dir": artifact_dir,
                "metadata": meta,
                "metadata_rel": str(metadata_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            })
    return artifacts


def _entry_from_artifact(artifact: dict) -> dict:
    meta = artifact["metadata"]
    m = meta.get("metadata", {})
    entry = {
        "dependencies": meta.get("dependencies", []),
        "domains": m.get("domains", []),
        "id": m.get("id", ""),
        "metadata_file": artifact["metadata_rel"],
        "name": m.get("name", ""),
        "path": str(artifact["dir"].relative_to(REPO_ROOT)).replace("\\", "/"),
        "tags": m.get("tags", []),
        "technology": m.get("technology", ""),
        "type": artifact["artifact_type"],
        "version": m.get("version", ""),
    }
    if not m.get("domains"):
        entry.pop("domains")
    if not m.get("tags"):
        entry.pop("tags")
    if not meta.get("dependencies"):
        entry.pop("dependencies")
    if artifact["artifact_type"] == "seed":
        comp = meta.get("composition", [])
        if comp:
            entry["composition"] = [c.get("block_id", c) if isinstance(c, dict) else c for c in comp]
    return entry


# ─────────────────────────────────────────────
# sync
# ─────────────────────────────────────────────

def cmd_sync(args) -> int:
    print("Syncing discovery/ from corpus/...")
    artifacts = _walk_corpus()
    if not artifacts:
        print("  WARNING: no artifacts found in corpus/", file=sys.stderr)

    today = str(date.today())
    entries = [_entry_from_artifact(a) for a in artifacts]

    seeds = [a for a in artifacts if a["artifact_type"] == "seed"]
    bundles = [a for a in artifacts if a["artifact_type"] == "building_block"]
    primitives = [a for a in artifacts if a["artifact_type"] == "primitive"]

    technologies: set[str] = set()
    for a in artifacts:
        tech = a["metadata"].get("metadata", {}).get("technology")
        if tech:
            technologies.add(tech)

    # substrate-index.json
    index = {
        "counts": {
            "building_blocks": len(bundles),
            "primitives": len(primitives),
            "seeds": len(seeds),
            "total": len(artifacts),
        },
        "entries": entries,
        "generated_at": today,
        "schema_version": "1.0.0",
        "source_branch": _git_branch(),
        "source_repository": "ste-architecture-substrate",
        "version": "1.0.0",
    }
    _write_json_atomic(DISCOVERY_DIR / "substrate-index.json", index)
    print(f"  Wrote discovery/substrate-index.json ({len(entries)} entries)")

    # substrate-manifest.yaml
    manifest = {
        "building_blocks": [
            _manifest_entry(a) for a in bundles
        ],
        "description": (
            "Architecture seeds, building block bundles, and primitives owned by "
            "ste-architecture-substrate. Provides opinionated, governed CloudFormation "
            "patterns for use by agents, humans, and downstream systems."
        ),
        "discovery_index": "discovery/substrate-index.json",
        "generated_at": today,
        "name": "STE Architecture Substrate",
        "primitives": [_manifest_entry(a) for a in primitives],
        "schema_version": "1.0.0",
        "seeds": [_manifest_entry(a, include_composition=True) for a in seeds],
        "source_repository": "ste-architecture-substrate",
        "technologies_present": sorted(technologies),
    }
    _write_yaml_atomic(DISCOVERY_DIR / "substrate-manifest.yaml", manifest)
    print("  Wrote discovery/substrate-manifest.yaml")

    # registries
    _write_registry("seeds", seeds)
    _write_registry("bundles", bundles)
    _write_registry("primitives", primitives)
    _write_technologies_registry(technologies)
    print("  Wrote discovery/registries/{seeds,bundles,primitives,technologies}.json")

    print(f"Done. {len(artifacts)} artifacts registered.")
    return 0


def _manifest_entry(artifact: dict, include_composition: bool = False) -> dict:
    meta = artifact["metadata"]
    m = meta.get("metadata", {})
    entry = {
        "id": m.get("id", ""),
        "name": m.get("name", ""),
        "path": str(artifact["dir"].relative_to(REPO_ROOT)).replace("\\", "/"),
        "technology": m.get("technology", ""),
        "version": m.get("version", ""),
    }
    if m.get("domains"):
        entry["domains"] = m["domains"]
    if meta.get("dependencies"):
        entry["dependencies"] = meta["dependencies"]
    if include_composition and meta.get("composition"):
        comp = meta["composition"]
        entry["composition"] = [c.get("block_id", c) if isinstance(c, dict) else c for c in comp]
    if m.get("tags"):
        entry["tags"] = m["tags"]
    return {k: entry[k] for k in sorted(entry)}


def _write_registry(name: str, artifacts: list[dict]) -> None:
    entries = []
    for a in artifacts:
        meta = a["metadata"]
        m = meta.get("metadata", {})
        cfn = meta.get("cloudformation", {})
        entry = {
            "id": m.get("id", ""),
            "metadata_file": a["metadata_rel"],
            "name": m.get("name", ""),
            "technology": m.get("technology", ""),
            "version": m.get("version", ""),
        }
        # template / construct path
        if "template" in cfn:
            entry["template"] = str((a["dir"] / cfn["template"]).relative_to(REPO_ROOT)).replace("\\", "/")
        elif "construct" in cfn:
            entry["template"] = str((a["dir"] / cfn["construct"]).relative_to(REPO_ROOT)).replace("\\", "/")
        # seed template list
        if "templates" in cfn:
            for t in cfn["templates"]:
                if "path" in t:
                    entry["template"] = str((a["dir"] / t["path"]).relative_to(REPO_ROOT)).replace("\\", "/")
                    break
        if meta.get("mutation_rules"):
            entry["mutation_rules"] = str((a["dir"] / meta["mutation_rules"]).relative_to(REPO_ROOT)).replace("\\", "/")
        if meta.get("dependencies"):
            entry["dependencies"] = meta["dependencies"]
        if meta.get("composition"):
            comp = meta["composition"]
            entry["composition"] = [c.get("block_id", c) if isinstance(c, dict) else c for c in comp]
        entries.append({k: entry[k] for k in sorted(entry)})

    registry_path = DISCOVERY_DIR / "registries" / f"{name}.json"
    _write_json_atomic(registry_path, {
        "entries": entries,
        "registry": name,
        "schema_version": "1.0.0",
    })


def _write_technologies_registry(technologies: set[str]) -> None:
    SCHEMA_REF_MAP = {
        "cloudformation": {
            "building_block": "schemas/building-block-bundle.schema.json",
            "building_block_extension": "schemas/cloudformation/bundle-extension.schema.json",
            "mutation_rules": "schemas/mutation-rules.schema.json",
            "mutation_rules_extension": "schemas/cloudformation/mutation-rules-extension.schema.json",
            "primitive": "schemas/primitive-block.schema.json",
            "primitive_extension": "schemas/cloudformation/primitive-extension.schema.json",
            "seed": "schemas/seed.schema.json",
            "seed_extension": "schemas/cloudformation/seed-extension.schema.json",
        }
    }
    entries = []
    for tech in sorted(technologies):
        entry = {"id": tech}
        if tech in SCHEMA_REF_MAP:
            entry["schemas"] = SCHEMA_REF_MAP[tech]
        entries.append(entry)
    _write_json_atomic(DISCOVERY_DIR / "registries" / "technologies.json", {
        "entries": entries,
        "registry": "technologies",
        "schema_version": "1.0.0",
    })


def _git_branch() -> str:
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


# ─────────────────────────────────────────────
# validate
# ─────────────────────────────────────────────

def cmd_validate(args) -> int:
    try:
        import jsonschema
    except ImportError:
        print("ERROR: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
        return 1

    print("Validating corpus metadata files...")
    artifacts = _walk_corpus()
    errors = 0

    for artifact in artifacts:
        schema_path = SCHEMA_MAP[artifact["artifact_type"]]
        if not schema_path.exists():
            print(f"  WARN  schema not found: {schema_path}", file=sys.stderr)
            continue
        schema = _load_json(schema_path)
        validator = jsonschema.Draft7Validator(schema)
        errs = list(validator.iter_errors(artifact["metadata"]))
        if errs:
            errors += 1
            label = artifact["metadata_rel"]
            for e in errs:
                path_str = ".".join(str(p) for p in e.absolute_path) or "(root)"
                print(f"  FAIL  {label}")
                print(f"        {path_str}: {e.message}")
        else:
            print(f"  OK    {artifact['metadata_rel']}")

    if errors:
        print(f"\n{errors} validation error(s).")
        return 1
    print(f"\nAll {len(artifacts)} metadata files valid.")
    return 0


# ─────────────────────────────────────────────
# check
# ─────────────────────────────────────────────

def cmd_check(args) -> int:
    index_path = DISCOVERY_DIR / "substrate-index.json"
    if not index_path.exists():
        print(f"ERROR: discovery index not found at {index_path}", file=sys.stderr)
        print("Run: python tools/corpus_cli.py sync", file=sys.stderr)
        return 1

    index = _load_json(index_path)
    index_entries = {e["id"]: e for e in index.get("entries", [])}

    # Walk actual corpus
    corpus_artifacts = _walk_corpus()
    corpus_ids = {a["metadata"].get("metadata", {}).get("id"): a for a in corpus_artifacts}

    drift = False

    # (a) Every index entry must resolve to a real path
    for artifact_id, entry in sorted(index_entries.items()):
        meta_path = REPO_ROOT / entry.get("metadata_file", "")
        if not meta_path.exists():
            print(f"  ORPHAN  index entry '{artifact_id}' → file not found: {entry.get('metadata_file')}")
            drift = True
        # Check referenced files exist
        for field in ("template", "mutation_rules"):
            ref = entry.get(field)
            if ref and not (REPO_ROOT / ref).exists():
                print(f"  MISSING {artifact_id}.{field} → {ref}")
                drift = True

    # (b) Every corpus artifact must appear in the index
    for artifact_id, artifact in sorted(corpus_ids.items()):
        if not artifact_id:
            print(f"  WARN  artifact at {artifact['metadata_rel']} has no id in metadata.metadata.id")
            continue
        if artifact_id not in index_entries:
            print(f"  UNREGISTERED  corpus artifact '{artifact_id}' not in discovery index")
            drift = True

    if drift:
        print("\nCORPUS DRIFT DETECTED. Run: python tools/corpus_cli.py sync")
        return 1

    print(f"OK. {len(corpus_ids)} corpus artifacts, {len(index_entries)} index entries — consistent.")
    return 0


# ─────────────────────────────────────────────
# list
# ─────────────────────────────────────────────

def cmd_list(args) -> int:
    index_path = DISCOVERY_DIR / "substrate-index.json"
    if not index_path.exists():
        print("ERROR: no discovery index. Run: python tools/corpus_cli.py sync", file=sys.stderr)
        return 1

    entries = _load_json(index_path).get("entries", [])
    if args.type:
        entries = [e for e in entries if e.get("type") == args.type]

    if args.json:
        print(json.dumps(entries, indent=2))
        return 0

    if not entries:
        print("No artifacts found.")
        return 0

    col_w = {"type": 14, "id": 30, "version": 9, "technology": 14}
    header = f"{'TYPE':<{col_w['type']}} {'ID':<{col_w['id']}} {'VERSION':<{col_w['version']}} {'TECH':<{col_w['technology']}} NAME"
    print(header)
    print("-" * (len(header) + 20))
    for e in entries:
        print(
            f"{e.get('type',''):<{col_w['type']}} "
            f"{e.get('id',''):<{col_w['id']}} "
            f"{e.get('version',''):<{col_w['version']}} "
            f"{e.get('technology',''):<{col_w['technology']}} "
            f"{e.get('name','')}"
        )
    return 0


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Corpus maintenance CLI for ste-architecture-substrate"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("sync", help="Regenerate discovery/ from corpus/ metadata files")
    sub.add_parser("validate", help="Validate all metadata files against JSON Schemas")
    sub.add_parser("check", help="Bidirectional corpus ↔ index integrity check (contract guard)")

    list_p = sub.add_parser("list", help="List registered artifacts")
    list_p.add_argument("--type", choices=["seed", "building_block", "primitive"], help="Filter by type")
    list_p.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    handlers = {
        "sync": cmd_sync,
        "validate": cmd_validate,
        "check": cmd_check,
        "list": cmd_list,
    }
    sys.exit(handlers[args.command](args))


if __name__ == "__main__":
    main()
