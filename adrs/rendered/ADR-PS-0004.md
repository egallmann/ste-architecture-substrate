<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: bd6b030945c02156507efb3491a3fa9f0f8520b45fdd2948378f5f6f123e61d7
rendered_hash: f207b0045549479ea43d3dc8ad25dc688482de39d4b1e4a24934dac1a00f10d2
-->

# ADR-PS-0004: Artifact Composition Model

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** architecture, composition  

**Implements Logical:** ADR-L-0001  
**Technologies:** 


---

## Context

Architecture seeds are complete starting architectures, building block bundles
are reusable components, and primitive blocks are low-level constructs. This
ADR defines how these artifacts compose: seeds compose building blocks, blocks
may reference primitives, dependency resolution, versioning, and metadata for
discovery.


## Technology Stack

### Semantic Versioning (tooling)

**Version:** 2.0.0

**Rationale:**
Artifact versioning and compatibility model

### YAML (tooling)

**Version:** N/A

**Rationale:**
Composition manifest serialization



## Component Specifications








---

*Generated from ADR-PS-0004 by ADR Architecture Kit*