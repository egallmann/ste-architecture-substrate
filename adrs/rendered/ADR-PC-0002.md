<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: 0fcfd3ee349bffe8c03cb0806c4aa0cd860013dee5cd00403a0092961f65e21e
rendered_hash: fad2f0488e73de49fe64477bb192bc8a4e7044af23e4f87ae0132933851c81fa
-->

# ADR-PC-0002: CloudFormation Seed Artifact Structure

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** cloudformation  

**Implements Logical:** ADR-L-0001  
**Technologies:** 


---

## Context

CloudFormation seed artifacts define complete architecture starting states as collections
of CloudFormation templates with metadata, parameters, capabilities, and optional stack
policies. Seeds represent "Architecture IR in CloudFormation form" and provide the baseline
from which building blocks compose.

Key characteristics:
- Contains one or more CloudFormation templates as an array
- Declares required parameters and their types
- Specifies CloudFormation capabilities needed for deployment
- Optionally references stack policy for operational governance
- Includes ADR traceability via metadata


## Technology Stack

### AWS CloudFormation (infrastructure)

**Version:** N/A

**Rationale:**
Primary IaC technology



## Component Specifications

### COMP-0002: CloudFormation Seed (library)

**Responsibilities:**
- Define complete CloudFormation architecture starting state
- Provide templates array with parameters and capabilities
- Reference optional stack policy


**Interfaces:**
- **IFACE-0002** (library_api): CloudFormation Seed Structure (JSON Schema):

```json
{
  "metadata": {
    "id": "string (unique se...

**Implementation Identifiers:**
- Module Path: `schemas/cloudformation-seed.schema.json`


## Deployment Model




## Implementation Decisions

### IMPL-0003: Templates as array rather than single file

**Rationale:**
Enables logical separation of concerns (e.g., VPC core vs VPC endpoints) while maintaining
a single seed identity. Supports staged deployment and independent stack lifecycle.




### IMPL-0004: Explicit capabilities declaration

**Rationale:**
Forces seed authors to acknowledge IAM/macro capabilities required by templates, improving
security review and deployment automation safety.








---

*Generated from ADR-PC-0002 by ADR Architecture Kit*