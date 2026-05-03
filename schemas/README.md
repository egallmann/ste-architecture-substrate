# Substrate Artifact Schemas

This directory contains JSON Schema definitions for substrate artifacts following the **core + extension model** defined in ADR-PS-0002 and ADR-PS-0003.

## Phase 5 status

All **10** planned schemas are present:

| Schema | Role |
|--------|------|
| `seed.schema.json` | Core seed interface |
| `building-block-bundle.schema.json` | Core bundle interface |
| `primitive-block.schema.json` | Core primitive interface |
| `mutation-rules.schema.json` | Core mutation rules (structured or logical-ID sidecar) |
| `cloudformation/seed-extension.schema.json` | CloudFormation seed namespace |
| `cloudformation/bundle-extension.schema.json` | CloudFormation bundle namespace |
| `cloudformation/primitive-extension.schema.json` | CloudFormation primitive namespace |
| `cloudformation/mutation-rules-extension.schema.json` | Optional CFN-specific tightening |
| `substrate-index.schema.json` | Discovery index JSON |
| `substrate-manifest.schema.json` | Discovery manifest (JSON-compatible subset) |

### Composed validation (recommended)

Validate a full CloudFormation seed document with JSON Schema `allOf`:

```json
{
  "allOf": [
    { "$ref": "seed.schema.json" },
    { "$ref": "cloudformation/seed-extension.schema.json" }
  ]
}
```

Reference fixture (stress-test): `fixtures/reference-architecture/aws-cloudformation-templates-webapp/` vendors upstream **Apache-2.0** `webapp.yaml` and includes `substrate-seed-metadata.example.json` validated against the composed seed schemas.

## Schema Architecture

### Core Schemas (Technology-Agnostic)

Core schemas define universal fields that ALL substrate artifacts must provide, regardless of IaC technology:

1. **`seed.schema.json`** - Core seed artifact interface
2. **`building-block-bundle.schema.json`** - Core bundle artifact interface  
3. **`primitive-block.schema.json`** - Core primitive artifact interface
4. **`mutation-rules.schema.json`** - Core mutation rules structure

### Extension Schemas (Technology-Specific)

Extension schemas define technology-specific namespaces that extend the core interface:

#### CloudFormation Extensions
Located in `cloudformation/` subdirectory:

1. **`cloudformation/seed-extension.schema.json`** - CloudFormation seed namespace
2. **`cloudformation/bundle-extension.schema.json`** - CloudFormation bundle namespace
3. **`cloudformation/primitive-extension.schema.json`** - CloudFormation primitive namespace
4. **`cloudformation/mutation-rules-extension.schema.json`** - CloudFormation mutation rule validation

#### Future Technology Extensions
Future IaC technologies will add their own extension directories:
- `terraform/` - Terraform extensions
- `sam/` - AWS SAM extensions
- `cdk/` - AWS CDK extensions

### Discovery Schemas (Technology-Agnostic)

Discovery schemas define derived artifacts for substrate consumption:

1. **`substrate-index.schema.json`** - Discovery index structure
2. **`substrate-manifest.schema.json`** - Discovery manifest structure

---

## Phase 4: Required Field Definitions

### Seed Artifact (Core + CloudFormation Extension)

#### Core Fields (Universal)
```yaml
# Required core fields for ALL seeds regardless of technology
id: string                        # Unique seed identifier
name: string                      # Human-readable name
version: string                   # Semantic version (e.g., "1.0.0")
technology: "cloudformation"      # Technology discriminator (enum)
domains: [string]                 # Architecture domains
tags: [string]                    # Discovery/classification tags
metadata:                         # Additional metadata
  description: string
  created_at: string              # ISO 8601 timestamp
  updated_at: string              # ISO 8601 timestamp
  deprecated_at: string           # Optional: ISO 8601 timestamp
  migration_guidance: string      # Optional: if deprecated
adr_bundle: [string]              # ADR references (ADR-L-XXXX, ADR-PS-YYYY)
mutation_rules: string            # Path to mutation-rules.yaml
composition: [object]             # Array of building block references
  - block_id: string
    version: string
    optional: boolean
```

#### CloudFormation Extension Namespace
```yaml
cloudformation:                   # Technology-specific namespace
  templates: [object]             # Array of CloudFormation templates
    - id: string                  # Template identifier
      path: string                # Relative path to template file
      description: string         # Template purpose
      stack_name_pattern: string  # Optional: e.g., "{env}-vpc-{region}"
  parameters: object              # Parameter definitions
    ParameterName:
      type: String|Number|CommaDelimitedList
      description: string
      default: any                # Optional
      allowed_values: [any]       # Optional
  capabilities: [string]          # Required CloudFormation capabilities
    # Examples: CAPABILITY_IAM, CAPABILITY_NAMED_IAM, CAPABILITY_AUTO_EXPAND
  stack_policy: string            # Optional: path to stack policy JSON
```

**Reference ADR**: ADR-PC-0002

---

### Building Block Bundle Artifact (Core + CloudFormation Extension)

#### Core Fields (Universal)
```yaml
# Required core fields for ALL bundles regardless of technology
id: string                        # Unique bundle identifier
name: string                      # Human-readable name
version: string                   # Semantic version
technology: "cloudformation"      # Technology discriminator
domains: [string]                 # Architecture domains
tags: [string]                    # Discovery tags
metadata:
  description: string
  created_at: string
  updated_at: string
adr_bundle: [string]              # Optional: ADR references
mutation_rules: string            # Path to mutation-rules.yaml (required for bundles)
dependencies: [string]            # Component dependencies (IDs or service names)
```

#### CloudFormation Extension Namespace
```yaml
cloudformation:
  template: string                # Path to single CloudFormation template
  fragment_type: enum             # Type of fragment
    # Values: resources, nested_stack, macro
  integration_points: object      # How bundle integrates into parent
    required_parameters: object   # Parameters bundle needs
      ParameterName:
        type: string
        description: string
    exports: object               # What bundle provides
      OutputName: string          # Description of export
```

#### Optional: ADR Context Prose
```yaml
adr_context_prose: string         # Optional: path to adr-context.md
```

**Reference ADRs**: ADR-PC-0003, ADR-PC-0008 (ADR context prose)

---

### Primitive Block Artifact (Core + CloudFormation Extension)

#### Core Fields (Universal)
```yaml
# Required core fields for ALL primitives regardless of technology
id: string                        # Unique primitive identifier
name: string                      # Human-readable name (optional for primitives)
version: string                   # Semantic version
technology: "cloudformation"      # Technology discriminator
metadata:                         # Minimal metadata
  description: string
```

#### CloudFormation Extension Namespace
```yaml
cloudformation:
  construct: string               # Path to CloudFormation construct file
  construct_type: enum            # Type of construct
    # Values: resource, parameter, output, condition
```

**Notes**:
- No `adr_bundle` field (primitives don't have ADR context)
- No `mutation_rules` field (primitives have no constraints)
- Minimal metadata (primitives are low-level fallbacks)

**Reference ADR**: ADR-PC-0004

---

### Mutation Rules (CloudFormation-Specific)

#### Core Structure (Technology-Agnostic)
```yaml
schema_version: string            # Schema version (e.g., "1.0.0")
iac_technology: "cloudformation"  # Technology discriminator
rules: [object]                   # Array of mutation rules
```

#### CloudFormation Rule Fields
```yaml
rules:
  - target: string                # CloudFormation path (e.g., "Resources.MyBucket.Properties.BucketName")
    classification: enum          # Mutability classification
      # Values: immutable, mutable, conditional
    condition: string             # Optional: when classification applies
    rationale: string             # Why this constraint exists
    severity: enum                # Severity level
      # Values: info, warning, error
    enforcement: enum             # Enforcement mechanism
      # Values: none, ci, cfn-hook, scp
```

#### Alternative YAML Structure (Simple)
```yaml
immutable: [string]               # List of logical IDs or patterns
append_only: [string]             # List of logical IDs or patterns
required: [string]                # List of logical IDs

metadata:                         # Optional documentation
  description: string
  rationale: string
  enforcement_level: enum         # advisory, required
```

**Reference ADR**: ADR-PC-0005

---

### Substrate Index (Technology-Agnostic)

```yaml
schema_version: string            # Schema version
type: "substrate-index"           # Type discriminator
namespace: string                 # Repository identifier
generated_at: string              # ISO 8601 timestamp
generator: string                 # Tool that generated this

# Registry paths (conventional)
seeds_registry_path: string       # e.g., "adrs/index/seed-registry.yaml"
building_blocks_registry_path: string
primitives_registry_path: string

# Technology support
technology_support: [string]      # e.g., ["cloudformation"]

# Statistics (optional)
statistics:
  total_seeds: number
  total_bundles: number
  total_primitives: number
  technologies: [string]
```

**Reference ADR**: ADR-PC-0008 (Discovery Bundle Generation)

---

### Substrate Manifest (Technology-Agnostic)

```yaml
schema_version: string            # Schema version
type: "substrate-manifest"        # Type discriminator
generated_from: string            # Source path
generated_at: string              # ISO 8601 timestamp

# Artifact summaries
seeds: [object]
  - id: string
    name: string
    description: string
    technology: string            # Technology discriminator
    version: string
    path: string
    adr_references: [string]
    templates_count: number       # Technology-specific summary

bundles: [object]
  - id: string
    name: string
    description: string
    technology: string
    version: string
    path: string
    mutation_rules: boolean
    adr_references: [string]

primitives: [object]
  - id: string
    technology: string
    path: string

# Statistics
statistics:
  by_type:
    seeds: number
    bundles: number
    primitives: number
  by_technology:
    cloudformation: number
```

**Reference ADR**: ADR-PC-0008

---

## Schema Validation Pattern

All core schemas will use JSON Schema `allOf` composition to combine core interface with extension validation:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "allOf": [
    { "$ref": "seed.schema.json#/definitions/core" },
    { "$ref": "cloudformation/seed-extension.schema.json" }
  ]
}
```

This pattern enables:
- **Stable core interface**: Core fields don't change when new technologies added
- **Flexible extensions**: Technologies can innovate in their namespaces
- **Independent validation**: Core and extension schemas validated separately
- **Clear separation**: Universal vs technology-specific is explicit

---

## Schema Evolution

Per ADR-L-0002 (Artifact Authority and Schema Ownership):

1. **Semantic versioning**: `schema_version` field in all artifacts
2. **Breaking changes**: Require explicit migration paths and documentation
3. **Non-breaking changes**: Backward compatible (add optional fields)
4. **Contract guards**: When mirroring external schemas (e.g., from ste-spec)

---

## Next Steps

**Phase 5** will create the actual JSON Schema files in this directory structure:

```
schemas/
  README.md                                   # This file
  seed.schema.json                            # Core seed
  building-block-bundle.schema.json           # Core bundle
  primitive-block.schema.json                 # Core primitive
  mutation-rules.schema.json                  # Core mutation rules
  substrate-index.schema.json                 # Discovery index
  substrate-manifest.schema.json              # Discovery manifest
  cloudformation/
    seed-extension.schema.json                # CFN seed namespace
    bundle-extension.schema.json              # CFN bundle namespace
    primitive-extension.schema.json           # CFN primitive namespace
    mutation-rules-extension.schema.json      # CFN mutation rule validation
```
