<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: 9fb3caf80229a9317019b1933341ca6025051993d88bc884ef3d6211106be0cd
rendered_hash: 68fcfd31968d2c773e9aa82d5929ec957b38754239bf39f0dfaeee5644d23a7d
-->

# ADR-PC-0005: CloudFormation Mutation Rules Schema

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** cloudformation, governance  

**Implements Logical:** ADR-L-0003  
**Technologies:** 


---

## Context

CloudFormation mutation rules define composition constraints for building block bundles
using CloudFormation logical IDs as the addressing model. Rules specify which resources
and properties are immutable, append-only, or required during composition and updates.

The logical ID addressing model leverages CloudFormation's native resource identification:
- Logical IDs uniquely identify resources within a template
- Dot notation accesses nested properties (LogicalId.Property.Nested)
- Wildcard patterns support resource families (MyResource.Tags.*)

Mutation rules bridge architecture governance (ADR-L-0003) with CloudFormation's
declarative model, enabling safe composition without custom tooling.


## Technology Stack

### AWS CloudFormation (infrastructure)

**Version:** N/A

**Rationale:**
Target IaC technology



## Component Specifications

### COMP-0005: CloudFormation Mutation Rules (library)

**Responsibilities:**
- Define mutation rules using CloudFormation logical ID addressing
- Specify immutable and append-only patterns
- Document logical ID addressing model


**Interfaces:**
- **IFACE-0005** (library_api): mutation-rules.yaml Structure:

```yaml
# Resources/properties that cannot be modified after initial...

**Implementation Identifiers:**
- Module Path: `schemas/mutation-rules.schema.json`


## Deployment Model




## Implementation Decisions

### IMPL-0007: Use CloudFormation logical IDs as addressing model

**Rationale:**
Leverages CloudFormation's native resource identification rather than introducing
custom addressing scheme. Enables validation against template structure and aligns
with CloudFormation tooling (drift detection, change sets).




### IMPL-0008: Support wildcard patterns for property families

**Rationale:**
Enables concise rules for repeated patterns (e.g., all tag keys immutable) without
enumerating every instance. Balances specificity with maintainability.








---

*Generated from ADR-PC-0005 by ADR Architecture Kit*