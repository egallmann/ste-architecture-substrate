# ste-architecture-substrate

**Start architecture from something real.**

---

## Why this exists

Modern AI-assisted engineering is very good at generating code, but much weaker at consistently designing systems.

Most workflows still start from a blank page:

* What architecture should we use?
* What components do we need?
* What are the right defaults?
* What should never change?

That leads to:

* repeated discovery
* inconsistent designs
* lossy reasoning
* slow iteration

This repository exists to change that.

> Instead of designing systems from scratch, start from **prebuilt, structured, machine-readable architectures**.

---

## What this is

`ste-architecture-substrate` is a **machine-first repository of architecture substrates**:

* **Architecture Seeds**
  Complete, ADR-aligned reference architectures with IaC and encoded intent.

* **Building Block Bundles**
  Reusable components (IaC + mutation rules + context) that guide system composition.

* **Mutation Rules**
  Explicit, machine-readable constraints that encode how systems are expected to evolve.

These artifacts are designed for both:

* **humans** (as high-quality starting points)
* **AI systems** (as deterministic inputs for reasoning)

---

## What makes this different

This is not:

* a template library
* a collection of examples
* a policy engine
* a validation framework

This is:

> A **substrate** — the layer architectures are built from.

Key properties:

* **Pre-committed structure**
  Systems start from known-good patterns, not guesses.

* **Deterministic projection**
  Structural elements (IaC, components) are reused directly.

* **Interpretive intent**
  Decisions and tradeoffs are explicitly expressed (via ADR).

* **Normative constraints (Ulysses model)**
  Rules are encoded and followed by default, but can be overridden with explicit intent.

---

## How it fits (STE context)

This repository is part of the broader **System of Thought Engineering (STE)** model.

High-level flow:

```
Conversation / Problem
        ↓
Architecture Substrate (this repo)
        ↓
ADR (adr-architecture-kit)
        ↓
Implementation (IaC / Code)
```

* The **substrate** provides starting structures and constraints
* **ADR** captures and converges intent
* **AI systems** adapt and refine, rather than invent from scratch

---

## How it works

At design time:

1. **Select an Architecture Seed**
   Choose a starting system that fits the problem, or let the conversation engine surface alternative candidate seeds, including patterns you may not be aware of that could better match the discussion.

2. **Project Structure**
   Reuse IaC and components directly to eliminate redundant design work, compress design interrogation by not re-defining foundational elements from scratch, reduce token consumption, and accelerate convergence on a high-quality baseline.

3. **Compose with Building Blocks**
   Add or refine components using reusable bundles, enabling a clean path of customization for both bespoke architectures and extensions of architecture seeds. This approach reduces friction rather than introducing it, maintaining consistency across teams, projects, and changes.

4. **Generate ADR (PS / PC)**
   Capture:

   * why this structure is used
   * what constraints are accepted or overridden

5. **Converge to Executable Architecture**
   ADR-PC represents the final, implementation-ready design, while building blocks provide the structure and context needed to efficiently amend it without breaking executability.

---

## Core Principle

> **Use proven structures. Be explicit about decisions.**

* Start from established, reliable architecture patterns instead of designing everything from scratch
* Seeds and building block bundles include the structural definitions and mutation rules needed to preserve these patterns over time
* Clearly document why choices are made, so systems remain understandable, consistent, and adaptable

This enables:

* speed at implementation
* speed at design
* consistency
* compliant architectures
* maintainable, consumable organizational architectures

---

## Why this matters

This approach works because it changes the starting conditions of system design.

Instead of asking AI (or engineers) to generate structure from an open-ended prompt, it constrains the problem space with pre-existing, high-quality artifacts. This has several mechanical effects:

* **Reduces design iteration and token usage**
  When structure is already defined, the system does not need to repeatedly explore and discard alternatives. Fewer exploratory branches means fewer tokens spent on re-deriving known patterns.

* **Increases architectural consistency**
  Reusing the same seeds and building blocks ensures that similar problems converge toward similar solutions. This removes variance introduced by prompt phrasing, individual interpretation, or model randomness.

* **Encodes organizational knowledge in reusable form**
  Decisions that would normally live in people’s heads or scattered documentation are captured as substrates and mutation rules. This makes them directly usable by both humans and machines without reinterpretation.

* **Enables AI to operate within a bounded, high-quality context**
  By limiting the solution space to known-good structures and explicit constraints, the AI is guided toward valid designs instead of exploring the full, unconstrained space of possibilities.

Together, these effects shift architecture from an open-ended synthesis problem into a constrained adaptation problem.

It turns architecture from:

> “figure it out each time”

into:

> “start from something real, then adapt with intent”

---

## What this enables (forward-looking)

Because architectures are:

* structured
* comparable
* traceable

This opens the door to:

* agentic architectural evolution driven by falsifiable experimentation
* direct mapping of telemetry back to design decisions
* pattern discovery grounded in real system behavior
* architecture patterns can be A/B tested in controlled lab environments for high-confidence candidate selection and extended into self-healing systems where degradation or failure in production triggers mutation and evolution; experimentation driven by observability data feeds enables automated, agent-driven refinement of architectures by treating design as a structured data problem, where decisions, constraints, and outcomes are continuously captured, evaluated, and iterated on without manual guesswork

---

## Repository structure

```
adrs/                 Governance — architecture decisions, constraints, invariants
  logical/            ADR-L: capabilities, boundaries, contracts
  physical-system/    ADR-PS: system-scale physical design
  physical-component/ ADR-PC: implementation-ready component specs
  index/              Generated: entity registries, architecture index
  rendered/           Generated: markdown renders of each ADR

corpus/               The patterns this substrate owns
  seeds/              Complete architecture starting states
    reference-webapp/   CloudFront + S3 + WAF + API GW + Lambda + Cognito + DynamoDB
  building-blocks/    Reusable, composable components
    static-site-delivery/
    serverless-api/
    cognito-auth/
  primitives/         Minimal, low-level IaC constructs
    s3-secure-bucket/
    lambda-execution-role/
    lambda-function/

discovery/            Machine-readable catalog surface
  substrate-index.json      Entry point for tools and agents
  substrate-manifest.yaml   Human-readable summary
  registries/               Per-type artifact registries

schemas/              JSON Schema contracts for all artifact types
  cloudformation/     Technology-specific extension schemas

tools/                Corpus maintenance CLI (corpus sync / validate / check)

fixtures/             Local development fixtures (gitignored vendor templates)
```

---

## How consumers discover artifacts

**Do not browse `corpus/` directly.** Read `discovery/substrate-index.json` — the canonical, machine-readable entry point kept in sync with the corpus by the maintenance tooling.

```json
{
  "entries": [
    { "id": "reference-webapp", "type": "seed",
      "metadata_file": "corpus/seeds/reference-webapp/metadata.json", ... },
    { "id": "static-site-delivery", "type": "building_block", ... }
  ]
}
```

Each entry's `metadata_file` resolves to the authoritative artifact descriptor. From there, `cloudformation.templates[].path` (seeds/bundles) or `cloudformation.construct` (primitives) gives the IaC file.

---

## Branching

* **`main`** — stable, release line.
* **`develop`** — integration branch; created from `main` and kept in sync via PRs.
* **Feature branches** — branch from **`develop`**, open PRs into **`develop`**.

Promotion flow: work on a feature branch → PR to **`develop`** → when ready to ship, PR **`develop`** → **`main`**.

---

## Getting started

**Browse available patterns:**
```bash
python tools/corpus_cli.py list
```

**Validate all metadata against schemas:**
```bash
python tools/corpus_cli.py validate
```

**Install the pre-push contract guard:**
```bash
bash tools/install-hooks.sh
```

**Add a new building block:** see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Tooling requirements

- Python 3.10+
- `pip install adr-architecture-kit` (ADR authoring and validation)
- `pip install jsonschema pyyaml` (corpus tooling and schema validation)

---

## Related projects

* [`adr-architecture-kit`](https://github.com/egallmann/adr-architecture-kit)
  Structured ADR authoring and validation

* `ste-handbook` (in progress)
  Concepts, patterns, and methodology behind STE

---

## Final thought

This repository is an experiment in a simple idea:

> If we give AI better starting points, we get better systems.

Within the broader STE system, this repository serves as the structural foundation layer — providing the architectures that downstream components (like ADR generation and implementation workflows) build upon and refine.

---

If you’re exploring AI-assisted system design, architecture governance, or machine-readable architecture, feedback is welcome.
