<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: 8988027caecc7cef87958f2e0219b084fb743937ce6a40c5379dd4b0d57018bc
rendered_hash: cd25f7ce40c76e4661d06e4bcc6928de81e7335f492329b6bd962e90780b239b
-->

# ADR-PC-0009: Corpus Maintenance CLI Tooling

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** tooling, governance  

**Implements Logical:** ADR-L-0005  
**Technologies:** 


---

## Context

ADR-L-0005 defines the corpus maintenance capability (sync, validate, check).
ADR-PC-0001 defines the substrate CLI for artifact retrieval and search.
This component implements the maintenance side: keeping the discovery surface
consistent with the corpus as the corpus evolves.

The implementation is a standalone Python script (tools/corpus_cli.py) executable
without package installation, satisfying the ADR-L-0005 decision for zero-ceremony
fork usage. It also serves as the contract guard command required by AGENTS.md.


## Technology Stack

### Python (language)

**Version:** 3.10+

**Rationale:**
Consistent with adr-architecture-kit and STE ecosystem tooling

### jsonschema (library)

**Version:** 4.x

**Rationale:**
Schema validation for metadata.json files (already used in tests)

### PyYAML (library)

**Version:** 6.x

**Rationale:**
YAML read/write for substrate-manifest.yaml and mutation-rules.yaml



## Component Specifications

### COMP-0009: corpus_cli (service)

**Responsibilities:**
- Walk corpus/ tree and build artifact inventory from metadata.json files
- Validate metadata files against JSON Schemas (seed, bundle, primitive)
- Regenerate discovery surface (substrate-index.json, substrate-manifest.yaml, registries)
- Verify bidirectional integrity (index ↔ filesystem) and exit non-zero on drift
- Provide human-readable listing of registered artifacts


**Interfaces:**
- **IFACE-0009** (CLI): Entry point: tools/corpus_cli.py

Commands:

1. python tools/corpus_cli.py sync
   Walk corpus/, rea...

**Implementation Identifiers:**
- Module Path: `tools/corpus_cli.py`


## Deployment Model




## Implementation Decisions

### IMPL-0014: Single-file standalone script (tools/corpus_cli.py)

**Rationale:**
Zero-installation requirement (ADR-L-0005 DEC-0028). A single file is trivially
portable — fork and run. No build step, no virtualenv assumption beyond the
standard Python environment already used for adr-kit and schema tests.




### IMPL-0015: Corpus traversal uses directory naming convention to infer artifact type:
corpus/seeds/* → seed, corpus/building-blocks/* → building_block,
corpus/primitives/* → primitive.


**Rationale:**
Convention over configuration. No extra type discriminator required in metadata.json
— the path encodes the type. This matches the discoverable directory structure
defined in ADR-L-0004 and reinforced by the corpus/ restructure.




### IMPL-0016: Sync writes all discovery files atomically (write to temp, rename)

**Rationale:**
Prevents partial discovery state if the script is interrupted mid-write.
Ensures consumers always see either the old complete state or the new
complete state, never a mixed partial state.




### IMPL-0017: check is the designated repo contract guard command per AGENTS.md requirements.
Pre-push hook script: tools/install-hooks.sh.


**Rationale:**
AGENTS.md requires a repo-local contract guard for generated artifacts.
A companion install script (tools/install-hooks.sh) makes hook setup
explicit and reproducible for fork contributors.








---

*Generated from ADR-PC-0009 by ADR Architecture Kit*