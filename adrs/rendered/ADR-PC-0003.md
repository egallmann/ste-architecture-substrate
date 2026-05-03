<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: f4b708ecb4520e031df8210efbe94caa4b578514dc977f11df6d619cab94d2f2
rendered_hash: 597d21d6f15a55a6ff10187cdb6ec60652497458d4952f23d9f1ae30bacf770c
-->

# ADR-PC-0003: CloudFormation Building Block Bundle Structure

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** cloudformation  

**Implements Logical:** ADR-L-0001  
**Technologies:** 


---

## Context

CloudFormation building block bundles are reusable, composable components that extend
seed architectures with additional capabilities. Unlike seeds, bundles include mutation
rules that define composition constraints and integration requirements.

Key characteristics:
- Single CloudFormation template per bundle (focused scope)
- Mutation rules define composition constraints (immutable, append-only, required resources)
- Metadata includes ADR traceability
- Designed for composition into existing architectures
- Self-describing integration requirements


## Technology Stack

### AWS CloudFormation (infrastructure)

**Version:** N/A

**Rationale:**
Primary IaC technology



## Component Specifications

### COMP-0003: CloudFormation Bundle (library)

**Responsibilities:**
- Define reusable CloudFormation building block structure
- Include mutation rules for composition
- Maintain ADR traceability


**Interfaces:**
- **IFACE-0003** (library_api): CloudFormation Bundle Structure:

Directory structure:
```
building-blocks/<bundle-name>/
  metadata...

**Implementation Identifiers:**
- Module Path: `schemas/cloudformation-bundle.schema.json`


## Deployment Model




## Implementation Decisions

### IMPL-0005: Single template per bundle for focused scope

**Rationale:**
Enforces single-responsibility principle for building blocks. Complex capabilities
spanning multiple templates should be modeled as seeds instead.




### IMPL-0006: Mandatory mutation rules

**Rationale:**
Bundles are explicitly designed for composition. Mutation rules communicate integration
constraints and prevent unsafe modifications by downstream consumers.








---

*Generated from ADR-PC-0003 by ADR Architecture Kit*