id: STE_ARCHITECTURE_SUBSTRATE_ORIENTATION
version: 2.1
type: decision_compiled
audience: ai_builder

purpose: >
  Define the architecture substrate subsystem as a repository of
  pre-committed, machine-readable architecture artifacts used to
  accelerate and standardize architecture design.

---

system_identity:

  definition: >
    The architecture substrate is the foundational layer from which
    architectures are formed. It provides prebuilt architecture seeds
    and building block bundles that encode structure, intent, and
    mutation rules.

  primary_function:
    - provide_starting_architecture_states
    - provide_reusable_component_bundles
    - encode_organizational_patterns

---

core_artifacts:

  architecture_seed:
    definition: >
      A complete architecture starting state including IaC and full
      ADR bundle (ADR-L, ADR-PS, ADR-PC).

    properties:
      - fully_defined_structure
      - executable_intent
      - system_level_commitments

  building_block_bundle:
    definition: >
      A reusable architecture component including IaC fragment,
      mutation rules, and ADR-compatible context prose.

    properties:
      - component_level_structure
      - normative_constraints
      - non_authoritative_context

  primitive_block:
    definition: >
      A low-level IaC construct without ADR context, used for fallback
      composition when higher-level abstractions are unavailable.

---

ulysses_contract_model:

  definition: >
    Substrate artifacts encode pre-committed architectural intent and
    mutation rules that bias future design decisions.

  properties:
    - constraints_are_explicit
    - constraints_are_machine_readable
    - constraints_are_normative
    - compliance_is_default
    - deviation_is_allowed
    - enforcement_is_external

---

adr_relationship:

  authority_model:
    adr_is_authoritative: true
    substrate_is_non_authoritative: true

  convergence:
    adr_pc_definition: >
      ADR-PC represents the converged, authoritative, executable
      architecture derived from substrate artifacts.

---

projection_interpretation_invariant:

  structure:
    rule: deterministic_projection
    definition: >
      Structural elements (IaC, resource definitions, defaults)
      must be mapped directly from substrate artifacts without reinterpretation.

  intent:
    rule: interpretive_generation
    definition: >
      Architectural reasoning must be generated based on system context
      and must explain selection, fit, and deviations.

---

building_block_behavior:

  constraints:
    type: normative
    behavior:
      - applied_by_default
      - may_be_overridden
      - override_requires_explicit_intent

  contents:
    - iac_fragment
    - mutation_rules
    - adr_context_prose

---

mutation_rules:

  definition: >
    Mutation rules define expected modification boundaries and
    organizationally aligned behavior for substrate artifacts.

  types:
    - immutable
    - mutable
    - conditional

  behavior:
    - guide_ai_decision_making
    - maximize_compliance_by_default
    - do_not_enforce_locally

---

usage_model:

  description: >
    The architecture substrate is consumed by external systems through
    deterministic retrieval and projection of artifacts into target
    representations such as ADR-PC.

  interaction_pattern:
    - select_seed_or_block
    - retrieve_artifact
    - project_structure_into_target_representation
    - interpret_intent_and_constraints

  projection_rule:
    - structure_must_be_projected_1_to_1
    - intent_must_be_generated_post_projection

  note: >
    The substrate does not perform projection itself. It provides artifacts
    that are designed to be projected deterministically by consuming systems.

---

system_boundaries:

  included:
    - artifact_storage
    - artifact_structuring
    - mutation_rule_definition

  excluded:
    - validation
    - enforcement
    - runtime_execution
    - policy_decision

---

design_objectives:

  - reduce_reasoning_surface
  - reduce_token_consumption
  - increase_architecture_consistency
  - accelerate_adr_generation
  - encode_organizational_knowledge

---

invariants:

  - structure_must_be_deterministic
  - intent_must_be_interpretive
  - substrate_must_not_enforce_constraints
  - artifacts_must_be_machine_readable
  - seeds_must_include_adr_bundle
  - building_blocks_must_include_mutation_rules

---

artifact_relationships:

  - seeds_are_composed_of_building_blocks
  - building_blocks_can_be_used_independently
  - primitive_blocks_support_low_level_construction

---

future_direction:

  pattern_evolution:
    description: >
      Substrate artifacts may evolve based on observed system behavior,
      telemetry, and architectural evaluation.

    constraint:
      - no_unreviewed_updates