<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: bd36798ac49cd124f3ae8125328f716bfc903d314e092ad45f52e236cf74a23c
rendered_hash: e914857cd2f454b5b74f72e39b62514964403ecaedb0c812ed732772b16bd061
-->

# ADR-PC-0007: CloudFormation Stack Policy Integration

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** cloudformation, governance  

**Implements Logical:** ADR-L-0003  
**Technologies:** 


---

## Context

Defines how seeds reference CloudFormation stack policies for operational enforcement.


## Technology Stack

### AWS CloudFormation (infrastructure)

**Version:** N/A

**Rationale:**
Target platform



## Component Specifications

### COMP-0007: Stack Policy Integration (library)

**Responsibilities:**
- Define stack policy integration for seeds
- Reference stack policy files
- Document enforcement semantics


**Interfaces:**
- **IFACE-0007** (library_api): Seed cloudformation.stack_policy field:
- Optional string path to stack policy JSON
- Applied during...

**Implementation Identifiers:**
- Module Path: `schemas/cloudformation-seed.schema.json`


## Deployment Model








---

*Generated from ADR-PC-0007 by ADR Architecture Kit*