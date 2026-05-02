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
   Choose a starting system that fits the problem, or let the conversation engine surface alternative candidate seeds, including patterns you may not be aware of, that could better match the discussion.

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
* architecture patterns can be A/B tested in controlled lab environments for high-confidence candidate selection, and extended into self-healing systems where degradation or failure in production triggers mutation and evolution, with experimentation driven by observability data feeds, enabling automated, agent-driven refinement of architectures by treating design as a structured data problem, where decisions, constraints, and outcomes are continuously captured, evaluated, and iterated on without manual guesswork

---

## Getting started

Explore:

* `/seeds/` — complete architecture starting points
* `/building-blocks/` — reusable components
* `/schemas/` — artifact definitions

Start with a seed, then adapt.

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
