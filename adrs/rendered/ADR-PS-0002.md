<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: 6ffe5ba3fc755a921c61681e9f0ac26badb875dbbe7b6b69f824e466c5e11bee
rendered_hash: 6eae4310eae1e469bbe8be217924334524b82b6550a3e6dc5ef792fd8093f88e
-->

# ADR-PS-0002: Core Artifact Interface Contract

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** architecture, schema-design  

**Implements Logical:** ADR-L-0001, ADR-L-0004  
**Technologies:** 


---

## Context

ste-architecture-substrate must support multiple IaC technologies (CloudFormation,
Terraform, SAM, CDK) while providing a stable consumption interface. This ADR
defines the core artifact interface contract: universal fields ALL technologies
must provide, enabling technology-agnostic discovery and consumption.

The core interface ensures consuming systems can discover and retrieve artifacts
without technology-specific code, while technology extensions (ADR-PS-0003) provide
IaC-specific fields.


## Technology Stack

### JSON Schema (tooling)

**Version:** Draft 2020-12

**Rationale:**
Core interface contract definition

### YAML (tooling)

**Version:** N/A

**Rationale:**
Artifact serialization format



## Component Specifications








---

*Generated from ADR-PS-0002 by ADR Architecture Kit*