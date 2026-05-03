<!--
integrity_schema_version: 1
generated: deterministic_projection_v1
artifact_kind: rendered_adr_markdown
generator_id: adr-rendered-markdown
generator_version: 1
hash_algorithm: sha256
source_hash: 3f50dcff24c2f42984977132c95b6cf33d1d26084a3f0e5b9ea7556a35224c14
rendered_hash: 84d9308fc27bab5f9737602a6d1949742297e52586996b33bb101a6fba20841e
-->

# ADR-PC-0006: CloudFormation Template Structure Requirements

**Status:** proposed  
**Created:** 2026-05-02  
**Authors:** Erik Gallmann  
**Domains:** cloudformation  

**Implements Logical:** ADR-L-0001  
**Technologies:** 


---

## Context

CloudFormation template structural validity defines requirements for template syntax,
resource types, property schemas, and AWS service limits. While substrate artifacts
(seeds, bundles) do not perform runtime validation, they document structural requirements
that external tools (cfn-lint, AWS CloudFormation validation API) enforce.

Key validation dimensions:
- Syntax: Valid YAML/JSON CloudFormation template
- Schema: Resource types and properties match AWS schemas
- Limits: AWS service limits (200 resources, 60 outputs, etc.)
- References: Intrinsic functions reference valid resources/parameters
- Naming: Logical IDs follow CloudFormation conventions


## Technology Stack

### AWS CloudFormation (infrastructure)

**Version:** N/A

**Rationale:**
Target platform

### cfn-lint (tooling)

**Version:** 0.70+

**Rationale:**
Validation tool



## Component Specifications

### COMP-0006: CloudFormation Template Structure (library)

**Responsibilities:**
- Define structural validity requirements for CloudFormation templates
- Reference cfn-lint validation
- Document required sections


**Interfaces:**
- **IFACE-0006** (library_api): CloudFormation Template Structure Requirements:

1. Required Sections:
```yaml
AWSTemplateFormatVers...

**Implementation Identifiers:**
- Module Path: `docs/cloudformation-template-requirements.md`


## Deployment Model




## Implementation Decisions

### IMPL-0009: Document validation requirements without implementing validators

**Rationale:**
Leverages existing tooling (cfn-lint, AWS validation API) rather than duplicating
validation logic. Substrate focuses on artifact structure and discovery, not runtime
validation.




### IMPL-0010: Reference cfn-lint as recommended validation tool

**Rationale:**
cfn-lint is open-source, actively maintained, supports custom rules, and provides
detailed error messages aligned with AWS best practices.








---

*Generated from ADR-PC-0006 by ADR Architecture Kit*