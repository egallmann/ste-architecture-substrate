<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: 46f3dcb5b0cf39a77dbba734158995f3e834fb9c3c5f37203ff3f1ac78a1ea0b
rendered_hash: 9b2efc07a34018a4128c75983a9737b092717e8a6ce90f7d1ea6b80c0852f3b6
-->

# ADR-PC-0004: CloudFormation Primitive Block Structure

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** cloudformation  

**Implements Logical:** ADR-L-0001  
**Technologies:** 


---

## Context

Defines minimal CloudFormation primitives without ADR context.


## Technology Stack

### AWS CloudFormation (infrastructure)

**Version:** N/A

**Rationale:**
Primary IaC technology



## Component Specifications

### COMP-0004: CloudFormation Primitive (library)

**Responsibilities:**
- Define minimal CloudFormation primitive structure
- Exclude ADR context and mutation rules
- Single template only


**Interfaces:**
- **IFACE-0004** (library_api): Single file: template.yaml (CloudFormation template only)
...

**Implementation Identifiers:**
- Module Path: `schemas/cloudformation-primitive.schema.json`


## Deployment Model








---

*Generated from ADR-PC-0004 by ADR Architecture Kit*