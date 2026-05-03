<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: cd540c15ea3f281366edb78687faff7a976ee9092a48cbd7428babee80d60e1d
rendered_hash: 45a1b188d4a5bde8541b5deb642bb2359a8e30f12677f3be70b2e731ff85c311
-->

# ADR-PC-0008: Substrate Discovery Bundle Generation

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** discovery  

**Implements Logical:** ADR-L-0004  
**Technologies:** 


---

## Context

Discovery bundle generation produces machine-readable artifacts that enable substrate
artifact discovery, retrieval, and integration by downstream tooling. The bundle includes
indices, manifests, and registries derived from canonical seed/bundle/primitive artifacts.

Discovery artifacts are derived state, not canonical. They enable:
- Fast artifact search without filesystem traversal
- Technology-specific filtering (CloudFormation, Terraform, etc.)
- Dependency analysis and composition planning
- Integration with CI/CD pipelines and IaC tooling

Generation is idempotent and reproducible from canonical artifacts.


## Technology Stack

### Python (language)

**Version:** 3.10+

**Rationale:**
Generator implementation



## Component Specifications

### COMP-0008: Discovery Bundle Generator (service)

**Responsibilities:**
- Generate substrate-index.json from artifacts
- Generate substrate-manifest.yaml
- Generate artifact registries


**Interfaces:**
- **IFACE-0008** (CLI): substrate compile [options]

Options:
  --output <path>              Output directory (default: ./di...

**Implementation Identifiers:**
- Module Path: `src/cli/compile.py`


## Deployment Model




## Implementation Decisions

### IMPL-0011: Generate both machine-readable JSON and human-readable YAML

**Rationale:**
JSON index enables fast programmatic discovery; YAML manifest supports human review
and documentation generation. Dual format maximizes utility.




### IMPL-0012: Derive discovery artifacts from canonical sources only

**Rationale:**
Ensures discovery bundle can be regenerated from source artifacts without state.
Prevents drift between canonical artifacts and discovery metadata.




### IMPL-0013: Include ADR traceability in all discovery artifacts

**Rationale:**
Enables consumers to understand architecture decisions behind artifacts and navigate
from implementation (seed/bundle) back to logical decisions (ADR-L).








---

*Generated from ADR-PC-0008 by ADR Architecture Kit*