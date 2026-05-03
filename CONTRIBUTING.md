# Contributing to ste-architecture-substrate

This repository is fork-friendly by design. Organizations are expected to fork it and add their own patterns. The guidelines below apply to both upstream contributions and private forks.

---

## Principles

- **ADR-first**: every new artifact type or governance change needs an ADR before code.
- **Corpus is authoritative**: `corpus/*/metadata.json` files are the source of truth. `discovery/` is derived — never hand-edit it.
- **Discovery is generated**: run `corpus sync` after any corpus change. The pre-push hook enforces this.
- **Structural validity**: all CloudFormation templates must be structurally valid CFN YAML (not just well-formed YAML).

---

## Adding a new building block

1. **Create the directory** under `corpus/building-blocks/<your-block-id>/`.

2. **Write `metadata.json`** — must validate against `schemas/building-block-bundle.schema.json`:
   ```json
   {
     "schema_version": "1.0.0",
     "metadata": {
       "id": "your-block-id",
       "name": "Human Name",
       "description": "...",
       "version": "1.0.0",
       "technology": "cloudformation",
       "domains": ["..."],
       "tags": ["..."]
     },
     "adr_bundle": ["ADR-L-XXXX"],
     "mutation_rules": "mutation-rules.yaml",
     "dependencies": [],
     "cloudformation": {
       "template": "template.yaml",
       "fragment_type": "resources"
     }
   }
   ```

3. **Write `template.yaml`** — a standalone CloudFormation stack template. Must include `AWSTemplateFormatVersion: '2010-09-09'`.

4. **Write `mutation-rules.yaml`** — at minimum declare `required:` resources. See `corpus/building-blocks/static-site-delivery/mutation-rules.yaml` for an example.

5. **Validate and sync:**
   ```bash
   python tools/corpus_cli.py validate
   python tools/corpus_cli.py sync
   python tools/corpus_cli.py check
   ```

6. **Validate ADRs** if you added or modified governance:
   ```bash
   adr validate --scope .
   ```

---

## Adding a new seed

Same workflow as a building block, but under `corpus/seeds/<seed-id>/` and validated against `schemas/seed.schema.json`. Seeds reference their component building blocks via `composition`.

---

## Adding a primitive

Under `corpus/primitives/<primitive-id>/`. Validate against `schemas/primitive-block.schema.json`. Primitives do not have mutation rules — they are minimal constructs.

---

## Corpus maintenance commands

| Command | When to run |
|---|---|
| `python tools/corpus_cli.py validate` | Before committing any metadata change |
| `python tools/corpus_cli.py sync` | After adding or modifying any corpus artifact |
| `python tools/corpus_cli.py check` | Before pushing (also run by pre-push hook) |
| `python tools/corpus_cli.py list` | Any time — browse registered artifacts |

Install the pre-push hook to enforce `check` automatically:
```bash
bash tools/install-hooks.sh
```

---

## ADR authoring

All governance changes (new capabilities, changed decisions, new invariants) need ADRs.

**Before writing IDs**, read `.adr-id-allocation.yaml` `entity_allocation` to find the next available IDs for each prefix (CAP, DEC, INV, etc.). Update the file after authoring.

```bash
adr validate --scope .
adr generate-manifest --scope .
adr generate-architecture-index --scope .
adr generate-rendered-docs --scope .
```

---

## Fork guidance

This repo is intentionally fork-friendly. When forking for your organization:

1. Fork the repo and rename it (e.g., `acme-architecture-substrate`).
2. Update `PROJECT.yaml` with your org name and description.
3. Add your patterns to `corpus/` following the workflows above.
4. The `discovery/substrate-index.json` auto-updates via `corpus sync`.
5. Schemas in `schemas/` are stable — do not modify them in your fork unless you intend to diverge the schema contract.
6. The `adrs/` corpus defines the governance for your fork's patterns — extend, do not replace.

---

## What not to do

- Do not hand-edit `discovery/` files — run `corpus sync` instead.
- Do not commit `fixtures/` vendor templates — they are gitignored by design.
- Do not add ADR content to `corpus/` artifact files — ADR context belongs in `adr-context.md` or the ADR corpus under `adrs/`.
- Do not use suffixed entity IDs like `IMPL-0009-A` — use sequential integers.
