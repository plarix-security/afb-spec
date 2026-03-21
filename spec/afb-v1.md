# AFB Taxonomy v1.0 (Derived from v1.0-plarix-thesis-15-03-26.pdf)

Toward a First-Principles Security Architecture for
Agentic Systems
A thesis for Plarix on perception, agency, and the four Agent
Failure Boundaries
Prepared from a ground-up reasoning exercise on the structure of AI agents, their failure surfaces, and the
product wedges that follow from them.
Abstract
This document reconstructs, formalizes, and extends a first-principles analysis of agentic security into a
coherent thesis for product design. It begins from a minimal ontology of an AI agent - context, model,
agent, and act - and derives a compact security taxonomy around four invariant transition zones:  AFB01
Context  Poisoning,  AFB02  Model  Boundary  Compromise,  AFB03  Instruction  Hijack,  and  AFB04
Unauthorized  Action.  The  paper  argues  that  these  are  not  arbitrary  categories  but  stable  failure
boundaries  that  recur  across  simple  agents,  real-time  daemons,  tool-using  assistants,  and  multi-agent
hierarchies.
The analysis then shows that the agent problem naturally decomposes into two sides:  perception and
agency. Perception concerns what the agent sees. Agency concerns what the agent can do. From this split,
two product wedges emerge. The first is the Agent Policy Gateway (APG), which targets the decisive last-
mile enforcement problem at AFB04. The second is the Selective Disclosure Layer (SDL), which minimizes
exposure on the perception side by controlling which attributes, identifiers, and secrets are ever revealed to
models.
The purpose of this thesis is not to imitate an existing checklist. It is to produce a compact theory sturdy
enough to guide architecture, threat modeling, and product scope.
1. Introduction
Security around AI agents is often discussed in a language that is too close to symptoms and too far from
mechanism.  Lists  of  threats  are  useful,  but  they  become  crowded  quickly:  prompt  injection,  excessive
agency,  output  handling,  memory  poisoning,  privilege  abuse,  tool  exploitation,  supply  chain,  context
poisoning, and more. The danger is not that these categories are wrong. The danger is that they live at
different levels of abstraction. As a result, they do not immediately tell a builder where a product should
stand.
This thesis takes a different route. Instead of starting from a crowded catalog of named attacks, it starts
from a simpler question:

What is the minimal loop of an AI agent, and where can that loop fail?
Once that loop is written clearly enough, a small number of transition boundaries appear . Those boundaries
turn out to be surprisingly stable across implementations. A chatbot, a LangGraph workflow, a daemon with
tools, a browser-using operator , and a hierarchical multi-agent system all differ in scale and wiring, but they
still move information and control across the same kinds of boundaries.
The practical consequence is important. If a company can define those boundaries clearly, it can stop
building around fashionable labels and start building around invariant choke points. This is where the thesis
places the first Plarix wedge. The core claim is not that every upstream problem disappears. The core claim
is that last-mile action control is the strongest first choke point, provided the surrounding ontology is
explicit enough to support a wider architecture later .
2. Minimal Ontology of an AI Agent
The first step is terminological discipline. Four base elements are enough to describe the agentic loop at the
level relevant for security design:
Context
Model
Agent
Act
The surrounding details - frameworks, number of models, number of subagents, tool protocols, memory
systems, and deployment topology - change the scale of the system but do not remove the need for these
four elements.
2.1 Context
Context is any information available to the system before the next step is chosen. It includes system
prompts, user prompts, retrieved documents, database records, prior messages, tool outputs, environment
observations,  metadata,  memory,  state  variables,  and  any  additional  information  that  can  condition
behavior .
The important property is not where the information came from. The important property is that the system
can see it and be shaped by it.
Two subforms of context are analytically useful.
Initial context
The starting seed.
This includes: - role - task - system prompt - initial user prompt - initial data - constraints - policies already
present before the first meaningful step
1.
2.
3.
4.

Ongoing context
The evolving state visible during execution.
This includes: - intermediate outputs - errors - prior acts - tool responses - environment changes - new
observations - consequences of previous steps
This distinction matters because many attacks are not only about corrupting the first prompt. They are
about corrupting the rolling informational state the agent relies on while it continues to act.
2.2 Model
The model is the token-processing reasoning engine. In the narrow abstraction used here, it receives input
tokens  and  produces  output  tokens.  Internal  chain-of-thought,  provider-side  orchestration,  decoding
strategies, and hidden reasoning mechanisms are treated as inside the model box.
This abstraction is deliberate. The point is not to decompose transformer internals. The point is to mark the
model as the place where visible context is transformed into outputs that will later shape action.
At this abstraction level:
Model = context in, model output out
2.3 Agent
The agent is the action-enabling system around the model. It includes: - code - orchestration logic -
planners - workflows - wrappers - memory management - tool interfaces - APIs - MCP clients and servers -
retrieval components - state machines - computer-use modules - execution scaffolding
If the model is the reasoning core, the agent is the machinery that turns reasoning into operations.
One analogy captured this cleanly:
Model = driver
Agent = car + controls + connections to the world
The analogy is not perfect, but it captures the main distinction. The model emits intent-like output. The
agent layer makes that output operable.
2.4 AI Agent
For the purposes of this thesis, an AI agent can be boxed as:
AI Agent = Model + Agent

The tools themselves may physically reside outside the runtime, but the operative question is whether the
agent can call them. At this level of abstraction, the box is therefore defined by control rather than by
process boundaries.
2.5 Act
Act is any operation the AI agent chooses or attempts.
The term is intentionally broad. It includes: - reading - writing - selecting a tool - changing a plan - calling an
API - generating text - generating code - deleting a file - sending an email - retrying after an error - updating
memory - choosing to inspect rather than modify
Act is not restricted to visibly destructive execution. It is any chosen operation that moves the loop forward.
2.6 Consequence
Consequence is what comes back from the act.
A consequence may be: - a visible world change - a returned error - a tool response - a successful update - a
partial failure - a subtle shift in state
Consequence feeds ongoing context, which means the agent sees not only the world as it was, but the
world as its previous acts have reshaped it.
3. The Minimal Agentic Loop
With the terms fixed, the loop becomes simple:
Context -> AI Agent -> Act -> Consequence -> Context
If unpacked:
Initial context + ongoing context -> model -> agent -> act -> consequence -> new ongoing context
The value of this loop is not its novelty. The value is its compactness. Once written this way, one can ask
where corruption, misdirection, or unauthorized behavior can be introduced.
The answer is not an infinite list.
It is a small number of transition boundaries.

4. The Four Agent Failure Boundaries
The original reasoning exercise identified four failure points in the path from context to action. These were
eventually  named  Agent  Failure  Boundaries,  or  AFBs,  because  each  one  marks  an  interface  where
information or control crosses from one stage to another and can be corrupted, redirected, or abused.
AFB01 - Context Poisoning
Transition: Context -> Model
AFB01 describes the failure condition in which the model ingests bad context.
This includes: - prompt injection - hidden instructions in documents - poisoned retrieved content - malicious
tool outputs - forged observations - compromised memory - false feedback about what just happened
At first principles level, AFB01 is not about whether the bad content came from a prompt, a webpage, a
vector store, a memory record, or a tool. Those are delivery mechanisms. The deeper issue is that the model
sees content it should not trust, yet treats it as part of the informational basis for its next step.
This category also absorbs what might otherwise be described as  feedback spoofing or  consequence
spoofing. If an agent is shown a fake result after an act - for example, a false message saying that a
payment succeeded or that a file was deleted - that false result simply becomes bad ongoing context. The
system is being lied to about what just happened. That still belongs to AFB01.
AFB02 - Model Boundary Compromise
Transition: Model I/O boundary
AFB02 marks the model-provider boundary. The initial shorthand for this category was API safety, but that
phrase was too narrow. The broader concern is integrity, confidentiality, and trust at the model boundary.
This  includes:  -  prompt  leakage  -  output  leakage  -  tampering  in  transit  -  unauthorized  middleware  -
provider-side mishandling - boundary failures that alter or expose information before it is reasoned over or
after it is produced
In a simple hosted model setup this looks like transport and provider risk. In a layered or routed model
architecture it can include internal model brokers, policy services, and model-serving layers.
AFB02  matters  because  a  secure  ontology  should  not  assume  the  model  boundary  is  automatically
trustworthy.
AFB03 - Instruction Hijack
Transition: Model -> Agent

AFB03 sits between model output and agent. Here the key problem is that the output of the model becomes
unsafe instructions, intents, or operational guidance for the agent layer .
Two broad pathways lead here.
1. Adversarial influence
A malicious input changes the model's output such that the agent is redirected toward unsafe behavior .
2. Endogenous error
The  model,  without  direct  adversarial  steering,  produces  unsafe  instructions  because  of  hallucination,
misgeneralization, or poor reasoning.
The result is the same in both cases: the agent is handed instructions that exceed or distort what should
have been produced.
The phrase  instruction hijack works because it captures both routes. The issue is not merely that the
model said something wrong. The issue is that the instruction channel from model to agent is no longer
trustworthy.
AFB04 - Unauthorized Action
Transition: Agent -> Act
AFB04 is the decisive boundary for the first product wedge.
The failure occurs when the agent attempts or performs an act that it is not authorized to perform, should
not perform in the present context, or performs in an unsafe way despite lacking sufficient policy basis.
This may involve: - the wrong tool - the wrong command - the wrong target - the wrong data movement -
the wrong privilege level - the wrong sequence of operations
AFB04 is where excessive agency becomes concrete. The earlier boundaries shape what the system thinks.
AFB04 is where the system touches state.
In this thesis, permission and execution both live here.
Permission asks what the agent is allowed to do.
Execution asks what the agent actually does.
The agent can be misled upstream and still fail harmlessly if AFB04 is properly constrained. Without AFB04
control, upstream corruption gains a route into the world.
•
•

5. Why There Are Four and Not Five
A useful taxonomy should not be forced into existence by naming enthusiasm.
The natural question arose: is there an AFB05?
At this abstraction level, the answer is no.
The reason is structural. Context, model, agent, and act define the minimal loop. The boundary taxonomy
follows the critical transitions that matter inside that loop:
context to model
model I/O boundary
model to agent
agent to act
What appear to be additional categories usually collapse into one of the existing four .
Examples: - feedback spoofing becomes AFB01 because it poisons ongoing context - multi-agent message
manipulation becomes repeated instances of AFB01 or AFB03 - tool execution abuse collapses into AFB04
because it concerns unauthorized action
A fifth boundary would only become necessary if a new invariant transition type were discovered that
cannot be represented as a subtype, repetition, or merging of the existing four .
The stress tests in this document do not produce such a case.
6. Perception and Agency
Once the boundary model was stable, a second abstraction emerged that is more product-legible.
An AI agent has two major sides:
What it sees
What it can do
The thesis names these:
Perception
Agency
6.1 Perception
Perception includes the informational side of the loop: the data, instructions, context, and operational cues
the agent sees before acting.
•
•
•
•
1.
2.
•
•

At the level adopted here, perception includes: - AFB01 - AFB02 - AFB03
Why?
Because after layers 1 to 3, the system is still in the realm of what the AI agent sees and operationalizes
before action.
AFB01 corrupts what enters the model as context.
AFB02 can alter , expose, or distort what reaches the model or returns from it.
AFB03 corrupts the instruction stream the agent receives before acting.
This framing is intentionally broader than a narrow sensory metaphor . The point is not only what the model
literally reads. The point is what the AI agent as a whole sees and operationalizes before action.
6.2 Agency
Agency concerns what the system can do.
It has two subparts:
Permission
What authority, access, and allowable operations the system possesses.
Execution
What operation is actually attempted or performed in the present moment.
AFB04 belongs squarely to agency because it is the place where permission and execution become real. The
earlier boundaries may alter the system's understanding or intent. AFB04 is where authority is exercised
against the environment.
7. Mapping the AFB Model to OWASP
The AFB taxonomy was not derived from OWASP , but it can be mapped onto OWASP categories to show that
it is not detached from the broader security landscape. The mapping is interpretive, not official.
AFB01 - Context Poisoning
OWASP LLM overlap: - LLM01 Prompt Injection - LLM04 Data and Model Poisoning - LLM08 Vector and
Embedding Weaknesses
OWASP Agentic overlap: - ASI06 Memory & Context Poisoning - ASI01 Agent Goal Hijack when poisoned
context redirects goals
•
•
•

AFB02 - Model Boundary Compromise
OWASP LLM overlap: - LLM02 Sensitive Information Disclosure - LLM03 Supply Chain
OWASP Agentic overlap: - ASI04 Agentic Supply Chain Vulnerabilities as nearest fit
AFB03 - Instruction Hijack
OWASP LLM overlap: - LLM01 Prompt Injection - LLM05 Improper Output Handling
OWASP Agentic overlap: - ASI01 Agent Goal Hijack - ASI02 Tool Misuse & Exploitation
AFB04 - Unauthorized Action
OWASP LLM overlap: - LLM05 Improper Output Handling - LLM06 Excessive Agency
OWASP Agentic overlap: - ASI02 Tool Misuse & Exploitation - ASI03 Identity & Privilege Abuse - ASI05
Unexpected Code Execution
This  should  be  read  carefully.  It  does  not  claim  equivalence.  It  claims  overlap.  The  purpose  is  not  to
subordinate the AFB model to OWASP nomenclature, but to show that the AFB model compresses several
established risk categories into a smaller set of transition boundaries that are easier to design against.
8. Why the First Product Wedge Lives at AFB04
A core insight of the reasoning process was that fixing AFB04 does not solve everything, but it does blunt
the damage potential of a large portion of the system.
If perception is poisoned upstream yet the agent cannot perform unsafe acts, the blast radius is sharply
reduced.
The poisoned water stays in the pipe rather than reaching the patient.
This metaphor is useful but should not be overextended. AFB04 enforcement does not make all upstream
failures harmless. A model can still produce harmful recommendations, subtle manipulation, unsafe but
superficially allowed advice, or confidential leakage through text. A poorly scoped action policy can also
allow catastrophic but policy-conformant behavior .
The point is not that AFB04 is total security.
The point is that AFB04 is the decisive last-mile enforcement point.
In practice, this means the first Plarix wedge should be defined as a policy enforcement architecture for
agent acts. The product should mediate whether a planned act is allowed, under what identity, against
which resources, with what constraints, under which conditions, and with what observability.

This is where excessive agency becomes enforceable rather than merely discussed.
9. Agent Policy Gateway
The natural product name for the first wedge is Agent Policy Gateway (APG).
The APG is the mechanism that sits at AFB04 and decides whether an intended act may become an actual
operation.
At minimum, it must evaluate policy against: - context - requested tool - requested operation - target
resource - identity - current state
In stronger forms it may also: - inject justification requirements - require human approval - downgrade
operations - strip dangerous parameters - substitute a safer operation
The essential thesis behind APG is simple:
If an AI agent is going to touch state, it should not do so through unbounded trust in model output.
It should cross a policy gate.
10. The Second Wedge on the Perception Side
The dialogue did not stop at AFB04. Once the action side was clear , attention returned to the perception
side.
If APG governs what the agent can do, what governs what the agent can see?
An early idea framed this as a zero-trust model that sees only encrypted data. That wording was too literal.
An LLM that sees only ciphertext is usually not useful.
The stronger formulation is not LLM on gibberish.
It is controlled data exposure.
Sensitive  fields  should  be  withheld,  transformed,  tokenized,  pseudonymized,  or  represented  through
derived attributes unless there is a policy-grounded reason to reveal them.
11. Selective Disclosure Layer
The resulting wedge is best named Selective Disclosure Layer (SDL).

The term is stronger than an invented label because it already lives inside serious privacy and identity
language. The core idea is simple:
The  model  should  not  receive  raw  sensitive  context  by  default.  It  should  receive  the  minimum
necessary representation for the task.
In the Plarix context, SDL means: - names may become tokens - high-risk identifiers may be withheld behind
separate secure mappings - some decisions may rely on derived attributes rather than raw values - a low-
trust front-end model may interact with masked state - a more privileged internal reasoning layer may
receive constrained disclosure through policy
This is compatible with layered model architectures. A public-facing chat layer does not need the same
visibility as a tightly controlled internal reasoning layer . What matters is not how many models exist, but
whether disclosure is minimal, purposeful, and policy mediated.
11.1 Relation of SDL to the AFB Model
SDL primarily addresses the perception side, especially AFB01.
It also improves resilience against AFB02 and AFB03 because less exposed context means: - less valuable
leakage  -  fewer  high-value  instruction  surfaces  -  less  dangerous  downstream  operationalization  if  an
upstream compromise occurs
SDL is not a replacement for APG.
It is the complementary wedge.
SDL controls what the agent sees. APG controls what the agent can do.
12. Combined Product Thesis for Plarix
The two wedges together form a much stronger architecture than an agent firewall alone.
SDL
Govern what the agent sees.
APG
Govern what the agent can do.
This yields a compact product thesis:
Plarix secures both sides of an AI agent. It constrains perception through selective disclosure and
constrains agency through policy-gated action enforcement.

That framing is stronger than generic "agent security" language because it is tied to a real ontology.
It also avoids trying to solve all risks at once.
The first product can live at AFB04.
The second wedge can extend the architecture upstream into perception.
Both sit naturally inside the same theory.
13. Stress Tests
A taxonomy that works only for a toy chatbot is not a taxonomy. It is a diagram.
The AFB model was therefore stress tested conceptually against several architectural variations.
13.1 Different models
Changing the model does not change the boundary types. Whether the reasoning engine is a hosted
frontier model, a local model, or a small specialist model, the system still has: - context entering reasoning -
a model boundary - output crossing into an agent layer - acts crossing into the world
13.2 Different agent frameworks
Using  LangGraph,  a  custom  orchestrator ,  no-code  workflows,  MCP ,  or  agent-to-tool  wrappers  changes
implementation detail rather than ontology. The same boundaries remain.
13.3 Real-time and daemon systems
Long-running autonomous systems produce more ongoing context and more repeated acts, but not new
boundary types. The same four recur in loops.
13.4 Multi-agent and hierarchical systems
This was the hardest stress test and the most important one.
In agent-to-agent systems, meta-agents, coordinator-worker setups, or hierarchical swarms, the same four
boundaries still apply. They do not disappear . They multiply.
Examples: - one agent's output can become another agent's context -> another AFB01 instance - one agent
can pass unsafe instructions to another -> another AFB03 instance - each agent still has its own model-
provider  boundary  ->  another  AFB02  instance  -  each  agent,  coordinator ,  or  worker  may  still  perform
unauthorized acts -> another AFB04 instance
The conclusion is strict:
•
•
•

Large systems do not introduce a fifth invariant boundary type. They produce many copies of the
same four.
13.5 Boundary merging
Some  implementations  collapse  boundaries  in  concrete  code.  A  tightly  fused  local  runtime  may  make
model and agent look almost indistinguishable. A direct function-calling stack may compress the visible gap
between model output and agent behavior .
These  cases  do  not  invalidate  the  taxonomy.  They  merely  show  that  conceptual  boundaries  can  be
implemented in merged ways. The type remains even when the physical separation narrows.
14. Dialectical Clarifications and Rejected Alternatives
Several clarifications emerged only because weaker formulations were rejected.
14.1 Action versus execution
Action  was  kept  broader  than  execution.  The  term  act was  chosen  to  include  not  only  destructive
operations but any chosen operation that moves the loop forward.
14.2 Rogue AI versus instruction hijack
Instruction Hijack replaced the looser phrase rogue AI because rogue AI confuses endogenous error with
adversarial redirection and loses the boundary logic.
14.3 API safety versus model boundary compromise
Model Boundary Compromise replaced API safety because transport, provider , and serving-layer integrity
are broader than raw API abuse.
14.4 Encrypted data everywhere versus controlled disclosure
Selective Disclosure Layer replaced the naive image of a model that works directly on ciphertext, which
would often be impractical or useless.
These rejections matter because naming controls architecture. A sloppy label quietly produces a sloppy
product boundary.
15. Limitations and Open Problems
No compact ontology eliminates the need for domain-specific controls.

A medical workflow still needs medical policy. A financial workflow still needs financial policy. An APG can
stop many dangerous acts, but it cannot guarantee the correctness of allowed recommendations if the
recommendation itself is harmful and the policy language is too weak to recognize it.
Similarly, SDL reduces exposure but raises practical design questions: - which fields should be tokenized? -
which should be pseudonymized? - which may be exposed as derived attributes? - when should disclosure
be granted to a more trusted internal model? - how are join risks, re-identification risks, and output leakage
handled?
These are not reasons to reject the wedge.
They are the research agenda implied by it.
16. Conclusion
The path taken in this document began with a desire for clarity and ended with a compact ontology strong
enough to support a company wedge.
An AI agent can be understood through four primitives: - context - model - agent - act
The critical failures in that loop can be organized into four Agent Failure Boundaries: -  AFB01 Context
Poisoning -  AFB02 Model Boundary Compromise -  AFB03 Instruction Hijack -  AFB04 Unauthorized
Action
These boundaries hold across simple and large-scale agentic systems because they describe transition
types rather than implementation quirks.
From there the architecture becomes legible.
Perception covers what the agent sees and is primarily threatened by AFB01-03.
Agency covers what the agent can do and is threatened at AFB04.
The first Plarix wedge, the Agent Policy Gateway, naturally targets AFB04 because it is the
strongest last-mile control point.
The second wedge, the Selective Disclosure Layer, extends protection upstream by minimizing
what models see in the first place.
The deeper value of the thesis is not the naming itself. It is the reduction. Once the agent problem is
reduced to stable boundaries, product scope stops drifting. That is the real gain.
A company can now ask not "which scary AI risk should we talk about" but:
Which boundary do we own, and how do we enforce it well enough that the rest of the architecture
can be built on top of it?
For Plarix, that answer begins at AFB04 and expands, carefully, toward perception.
•
•
•
•

Appendix A. Working Glossary
Context
Any information visible to the system before the next step is chosen.
Initial context
The starting seed: role, task, initial data, constraints.
Ongoing context
The evolving state visible during execution, including consequences of prior acts.
Model
The token-in, token-out reasoning engine.
Agent
The action-enabling machinery around the model.
AI agent
The boxed combination of model and agent.
Act
Any chosen operation that moves the loop forward.
Consequence
What comes back from an act and feeds future context.
Perception
The informational side of the system: what the agent sees and operationalizes before action.
Agency
The operative side of the system: what the agent can do.
Permission
The authority and access available to the agent.

Execution
The operation the agent actually attempts or performs.
Appendix B. Reference Notes
The AFB taxonomy itself is original to the reasoning process summarized in this document. External sources
are  relevant  here  for  alignment,  terminology,  and  comparison  rather  than  as  the  origin  of  the  four-
boundary model.
Relevant source families include: - OWASP Top 10 for LLM Applications 2025 - OWASP Top 10 for Agentic
Applications 2026 - NIST SP 800-63C on selective disclosure and derived attribute values - ICO guidance on
pseudonymisation and data minimisation
