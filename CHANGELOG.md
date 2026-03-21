# Changelog

## v2.0 — 2026-03-20

Introduced and formalized:

- **Canonical Execution Event (CEE)** as a four-field normalization schema (Operation, Principal, State Delta, Policy Basis) for policy evaluation and audit at every agent action.
- **Temporal context entropy** as a failure mode where dangerous information state accumulates across sequences of individually authorized operations.
- **Multi-agent trust propagation** showing agent-to-agent communication channels as a super-linear attack surface (O(N²) in fully connected systems) with trust laundering risk.
- **Policy language position**: v1 APG uses declarative rules as primary, with a bounded natural-language escape hatch; complete policy language remains an open problem.
- **SDL semantic compression position**: v1 SDL scope is structured sensitive fields; free-text sensitive data where semantics and sensitivity are inseparable is explicitly out of scope and remains open research.

## v1.0 — 2026-03-15

Introduced:

- The first-principles AFB taxonomy grounded in the minimal ontology of **context, model, agent, act**.
- The four Agent Failure Boundaries: **AFB01 Context Poisoning**, **AFB02 Model Boundary Compromise**, **AFB03 Instruction Hijack**, **AFB04 Unauthorized Action**.
- The perception/agency split and the two product wedges: **Agent Policy Gateway (APG)** at AFB04 and **Selective Disclosure Layer (SDL)** on the perception side.
