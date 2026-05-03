<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: b11a6ea465d98977f825093eedc4c4f5e6f28a9b8410dd03490f93b44b2813b4
rendered_hash: dd27910ff050b47686a48852b6849dc25b67fc2b99d883919a9d65edd0e5f6ad
-->

# ADR-PS-0003: Technology Extension Model

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** architecture, schema-design  

**Implements Logical:** ADR-L-0001, ADR-L-0004  
**Technologies:** 


---

## Context

ADR-PS-0002 defines the core artifact interface with technology-agnostic fields.
Different IaC technologies need technology-specific fields (CloudFormation templates,
Terraform modules, CDK constructs). This ADR defines the extension model: how
technologies add namespaced fields without breaking the core interface.


## Technology Stack

### JSON Schema (tooling)

**Version:** Draft 2020-12

**Rationale:**
Extension namespace schema definition with composition (allOf)

### YAML (tooling)

**Version:** N/A

**Rationale:**
Technology-specific extension serialization



## Component Specifications








---

*Generated from ADR-PS-0003 by ADR Architecture Kit*