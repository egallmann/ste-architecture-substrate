<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: 388bf9287ff421913329e2d184442e8f374bbcecd6b5315244fc90e0b91747dc
rendered_hash: 548f6701e3cc42f26c88e67734e8ba1c45f517de87055f89d078edbfa84eed58
-->

# ADR-PC-0001: Substrate Tooling CLI

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** tooling  

**Implements Logical:** ADR-L-0001  
**Technologies:** 


---

## Context

The substrate CLI provides commands for discovering, retrieving, validating, and compiling
architecture substrate artifacts. It implements the tooling interface defined in ADR-PS-0001
for local artifact management and discovery bundle generation.

Primary use cases:
- Search for seeds, bundles, or primitives by technology
- Retrieve specific seed artifacts for project initialization
- Validate artifact structure and schemas
- Compile discovery bundles for consumption by other tools
- Initialize new substrate projects


## Technology Stack

### Python (language)

**Version:** 3.10+

**Rationale:**
Implementation language



## Component Specifications

### COMP-0001: substrate CLI (service)

**Responsibilities:**
- Manage substrate artifacts (search, get, validate)
- Generate discovery bundles
- Initialize substrate projects


**Interfaces:**
- **IFACE-0001** (CLI): Command structure and examples:

1. substrate search [options]
   Search for substrate artifacts
   ...

**Implementation Identifiers:**
- Module Path: `src/cli/substrate_cli.py`


## Deployment Model




## Implementation Decisions

### IMPL-0001: Use Click framework for CLI

**Rationale:**
Click provides robust argument parsing, automatic help generation, and nested command
groups that align with substrate's command structure (search, get-seed, validate, etc.)




### IMPL-0002: File-based artifact discovery

**Rationale:**
Artifacts are discovered by filesystem traversal and metadata.json parsing rather than
requiring a centralized database or API, enabling offline usage and git-based distribution








---

*Generated from ADR-PC-0001 by ADR Architecture Kit*