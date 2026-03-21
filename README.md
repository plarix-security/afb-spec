# AFB Taxonomy Specification

The Agent Failure Boundary (AFB) taxonomy is an open security specification for agentic AI systems.

It defines four invariant failure boundaries in the agentic execution loop:

- **AFB01 - Context Poisoning**: the model ingests corrupted, forged, or manipulated context.
- **AFB02 - Model Boundary Compromise**: integrity/confidentiality failures at the model input/output boundary.
- **AFB03 - Instruction Hijack**: model output becomes unsafe instructions for the agent layer.
- **AFB04 - Unauthorized Action**: the agent attempts or performs an action outside authorized policy.

## Who this is for

- Security engineers designing controls for AI agents.
- Agent builders implementing policy and enforcement boundaries.
- Researchers analyzing structural failure modes in autonomous systems.

## How to use this spec

1. Start with `spec/afb-v1.md` and `spec/afb-v2.md` for the full taxonomy texts derived from the source papers.
2. Use boundary definitions to map architecture risks to loop transitions (`Context -> Model -> Agent -> Act`).
3. Use `owasp-mapping.md` to align AFB categories with OWASP LLM and OWASP Agentic categories (interpretive overlap only).
4. Use the examples in `examples/` to see concrete AFB01 and AFB04 exposure patterns.

## Project links

- https://plarix.dev
