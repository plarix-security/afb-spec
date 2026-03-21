# AFB to OWASP Mapping

**Note:** This mapping is interpretive overlap, not official equivalence. It is derived from Section 12 of the v2.0 paper.

| AFB | Description | OWASP LLM | OWASP Agentic |
|---|---|---|---|
| AFB01 | Context Poisoning (model ingests corrupted context) | LLM01 Prompt Injection; LLM04 Data Poisoning; LLM08 Embedding Weaknesses | ASI06 Memory & Context Poisoning; ASI01 Agent Goal Hijack |
| AFB02 | Model Boundary Compromise (I/O boundary tampered or exposed) | LLM02 Info Disclosure; LLM03 Supply Chain | ASI04 Supply Chain |
| AFB03 | Instruction Hijack (model output becomes unsafe instructions) | LLM01 Prompt Injection; LLM05 Output Handling | ASI01 Agent Goal Hijack; ASI02 Tool Misuse |
| AFB04 | Unauthorized Action (agent executes unpermitted acts) | LLM05 Output Handling; LLM06 Excessive Agency | ASI02 Tool Misuse; ASI03 Privilege Abuse; ASI05 Code Execution |
