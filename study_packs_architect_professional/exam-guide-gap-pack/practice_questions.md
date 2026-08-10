# Exam Guide Gap Pack Practice Questions — Architect: Professional

Supplemental drills covering all seven CCAR-P domains, weighted toward Domain 3 (Integration, 19%), Domain 1 (Solution Design & Architecture, 17%), and Domain 4 (Evaluation, Testing & Optimization, 16%). The real exam includes some multi-response items (each states how many responses to select) — most drills here are single-select, with two multi-select items included for realism. Pair these with `practice_exams_architect_professional/` for full-length simulation.

## Question 1

Scenario: A client wants to "add AI" to their claims-processing workflow. Initial discovery reveals the actual goal is handling 3x current claim volume without adding headcount, within the same average processing time.

Question: Which business value pillar should anchor this architecture, and why does that matter?

A. Transformation, because AI is inherently transformative technology.

B. Efficiency, because the stated goal is doing more of the same work with the same resources — the architecture and success metrics should be built around throughput per headcount, not novel capability.

C. Cost, because AI projects are usually justified on cost alone.

D. It doesn't matter which pillar is named as long as the system works technically.

Correct answer: B

Explanation: The stated goal — more volume, same headcount, same processing time — is a throughput/efficiency problem. Naming the correct pillar changes what you architect for and measure; a transformation-framed project would chase new capabilities the client didn't ask for.

Distractors:

- A: Transformation implies doing previously-impossible work, which isn't what was requested here.
- C: Cost framing is a guess not grounded in what discovery actually surfaced.
- D: Skipping this framing risks building toward the wrong success metric even if the system technically functions.

## Question 2

Scenario: A three-agent research pipeline (search, analysis, synthesis) is coordinated by a supervisor agent. An engineer proposes letting the search agent hand results directly to the analysis agent to "save a hop" through the coordinator.

Question: What is the strongest architectural objection?

A. Direct agent-to-agent communication is blocked by the Claude Agent SDK at the protocol level.

B. It doubles token usage because results would be serialized twice.

C. Routing through the coordinator preserves observability, consistent error handling, and controlled information flow — a direct channel sacrifices all three.

D. The analysis agent would require the search agent's exact tool permissions.

Correct answer: C

Explanation: Hub-and-spoke orchestration through the coordinator is what provides observability, consistent error handling, and controlled information flow across a multi-agent system. Bypassing it for one hop sacrifices those properties for that path.

Distractors:

- A: This isn't a hard protocol restriction — it's an architectural choice with real tradeoffs, which is the actual point being tested.
- B: A token-doubling claim isn't the core architectural issue here.
- D: Tool permissions aren't inherently shared just because two agents exchange data directly.

## Question 3

Scenario: A multi-agent system decomposes "summarize the competitive landscape for creative-industry AI tools" into subagents covering only visual-arts tools. Every subagent completes its assigned work correctly, but the final report never mentions music, writing, or film tools.

Question: What is the correct architectural fix?

A. Give the synthesis agent a stronger prompt asking it to check for completeness.

B. Add a fourth QA subagent to review the final report for gaps.

C. Fix the coordinator's decomposition to cover all relevant creative-industry subdomains before delegating.

D. Increase each subagent's context window so it can research more broadly.

Correct answer: C

Explanation: Every subagent succeeded at the (too-narrow) scope it was assigned — the decomposition itself, done by the coordinator, never included the missing subdomains. The fix belongs at the decomposition step, not downstream.

Distractors:

- A: The synthesis agent can only synthesize what it received; it never received the missing subdomains.
- B: A QA pass might catch the gap after the fact but doesn't fix the architectural cause.
- D: Context window size doesn't cause or fix a scoping/decomposition problem.

## Question 4

Scenario: An architecture team is deciding between MCP, a direct API/CLI integration, and an agent-to-agent protocol for connecting a Claude-based system to an internal inventory service used by exactly one application team, with no plans for reuse.

Question: Which integration mechanism best fits, and why?

A. MCP, because it's the newest and most capable option.

B. A direct API/CLI integration, since the need is tightly coupled to a single application with no reuse requirement.

C. An agent-to-agent protocol, since any two systems communicating should use agent-to-agent patterns.

D. All three are functionally interchangeable, so the choice doesn't matter architecturally.

Correct answer: B

Explanation: Connection protocol should match the actual reuse and coupling profile. A single-application, non-reused integration doesn't need MCP's cross-application reuse machinery or an agent-to-agent protocol meant for autonomous multi-system collaboration.

Distractors:

- A: MCP being commonly used for other cases doesn't make it the right fit here; "newest" is not the deciding criterion.
- C: Agent-to-agent protocols solve a different problem (autonomous cross-system collaboration), not simple single-app integration.
- D: The choice materially affects reusability and maintenance burden — it isn't interchangeable.

## Question 5

Scenario: A RAG system indexes both long-form legal contracts and a short structured FAQ table using the same chunking and indexing configuration tuned for the contracts. FAQ retrieval quality is poor.

Question: What is the most likely architectural cause?

A. The embedding model is too small for legal language.

B. Chunking and indexing strategy tuned for long-form documents doesn't match the FAQ table's structured, short-entry shape.

C. The FAQ table needs a larger context window to retrieve correctly.

D. FAQ content should be excluded from RAG entirely.

Correct answer: B

Explanation: Chunking and indexing strategy must match the data's shape. A configuration tuned for long-form prose will fragment or dilute short structured entries like FAQ rows, degrading retrieval quality for that content type specifically.

Distractors:

- A: Embedding model capacity isn't the described symptom — it's a shape mismatch between content type and chunking strategy.
- C: Context window size at generation time doesn't address a retrieval-stage indexing mismatch.
- D: Excluding the FAQ content removes value rather than fixing the retrieval configuration.

## Question 6

Scenario: A production RAG-based support system suddenly starts returning confident, plausible-sounding wrong answers immediately after a scheduled document refresh. Model version, prompt, and average latency are all unchanged.

Question: Where should the architect investigate first?

A. Whether the model was silently updated by the provider.

B. Whether the retrieval/indexing step is returning irrelevant or stale chunks after the refresh.

C. Whether the temperature setting drifted.

D. Whether the context window shrank.

Correct answer: B

Explanation: A regression tied specifically to a document refresh event, with model and latency unchanged, points first at the retrieval/indexing layer — a broken re-index or mismatched embeddings is the most likely cause.

Distractors:

- A: A silent model change wouldn't correlate specifically with the document refresh event.
- C: Temperature drift wouldn't explain a regression timed exactly to a data refresh.
- D: Context window size doesn't change from a document refresh event.

## Question 7

Scenario: A team is designing the evaluation strategy for a safety-critical Claude-based system that screens loan applications. They currently rely solely on an automated accuracy metric measured against a labeled test set.

Question: Which two additions would most strengthen the evaluation strategy? (Select TWO responses.)

A. Human expert review of edge cases and disputed decisions.

B. Adversarial/red-team test cases targeting bias and safety failure modes.

C. Increasing the size of the labeled test set with more of the same kind of examples.

D. Switching to a larger model to improve the automated accuracy score.

Correct answer: A, B

Explanation: A single automated accuracy metric doesn't cover nuanced judgment calls or adversarial/safety failure modes. Human review and red-team testing are the mixed-methodology additions the guide calls for in safety-critical evaluation design — no single method covers every failure mode.

Distractors:

- C: More examples of the same kind don't add a new failure-mode lens; they just add volume to the existing method.
- D: A larger model may or may not improve the metric, but doesn't address the evaluation strategy's actual gap (coverage of judgment and adversarial cases).

## Question 8

Scenario: A support agent's toolset has grown over six months from 4 tools to 18, including several rarely-used tools (loyalty program, gift cards, subscriptions) unrelated to its core refund/return responsibilities.

Question: What is the primary architectural risk, and what is the correct least-privilege fix?

A. Risk: MCP protocol tool-count limits will be exceeded. Fix: split tools across two MCP servers.

B. Risk: tool-selection reliability degrades as available tools grow. Fix: remove or scope out tools unrelated to the agent's core role, or split into specialized agents.

C. Risk: the agent will run out of context. Fix: shorten each tool's description.

D. Risk: none — more tools only add capability, not risk.

Correct answer: B

Explanation: Decision complexity and misrouting risk increase as an agent's toolset grows past what its role needs. Least privilege means removing the unnecessary capability (or splitting responsibilities across specialized agents), not just working around a perceived technical limit.

Distractors:

- A: There's no such hard MCP tool-count limit driving this scenario.
- C: Shortening descriptions trades clarity for a marginal context savings and doesn't address selection reliability.
- D: Growing toolsets do measurably degrade selection reliability — this is a real architectural risk.

## Question 9

Scenario: A healthcare client's Claude-based system will process patient records. The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after the core application logic is already built.

Question: What is the architectural risk in this sequencing?

A. None — compliance can always be layered on right before launch.

B. HIPAA-driven data residency, retention, and access-control requirements can force structural changes that are far more costly to retrofit than to design in from the start.

C. Compliance only affects legal documentation, not system architecture.

D. FedRAMP, not HIPAA, would apply to a healthcare client.

Correct answer: B

Explanation: Regulatory requirements like HIPAA constrain data residency, retention, and access-control design at a structural level. Resolving them after core application logic is built risks costly rework or an architecture that can't actually be brought into compliance without a redesign.

Distractors:

- A: Compliance requirements often require structural decisions (e.g., where data is stored, how it's logged) that are difficult to bolt on afterward.
- C: Compliance directly shapes technical architecture, not just legal paperwork.
- D: HIPAA (healthcare data) is the relevant regime here; FedRAMP applies to US federal government cloud authorization, a different context.

## Question 10

Scenario: A stakeholder asks why the team chose Sonnet-tier instead of Opus-tier for a customer-facing summarization feature. The architect responds: "We chose Sonnet because it's cheaper."

Question: What is missing from this communication, and why does it matter?

A. Nothing — cost is a valid and sufficient justification.

B. The specific tradeoff: what capability, if any, was given up, and what benefit (latency, cost, or both) was gained relative to the SLA — stakeholders need the tradeoff to evaluate and revisit the decision later.

C. The exact per-token price difference between the tiers.

D. A promise that the decision will never be revisited.

Correct answer: B

Explanation: Effective architectural communication states the tradeoff, not just the decision — e.g., "we traded some capability for a 3x latency improvement that meets the SLA." A bare cost justification doesn't let stakeholders evaluate whether the tradeoff is still right as requirements evolve.

Distractors:

- A: "Cheaper" alone doesn't communicate what was given up or whether the tradeoff still holds under changing requirements.
- C: Exact pricing detail isn't the missing architectural reasoning stakeholders need.
- D: Architectural decisions should remain revisitable as requirements or model capabilities change.

## Question 11

Scenario: A production system reports 97% aggregate extraction accuracy across all document types. A team proposes cutting human review by 80% based on this number.

Question: What should happen before that decision is made?

A. Nothing further — 97% aggregate accuracy is a strong enough signal on its own.

B. Segment accuracy by document type and field to check whether the aggregate is hiding a failing segment before reducing review.

C. Re-run the same evaluation on the same test set to confirm the number.

D. Switch to a different accuracy metric that produces a more conservative number.

Correct answer: B

Explanation: Aggregate accuracy can mask a failing segment (one document type or field performing far worse than the average). Segmenting accuracy by type/field before cutting review protects against silently degrading quality on the segments that need it most.

Distractors:

- A: A single aggregate number, without segmentation, is exactly the risk described.
- C: Re-running the same evaluation on the same data doesn't surface segment-level variance.
- D: Changing metrics doesn't address whether specific segments are underperforming.

## Question 12

Scenario: A team building an autonomous claims-approval agent proposes requiring human approval on every single decision the agent makes, framing it as the safest governance posture.

Question: What is the architectural problem with this approach?

A. There is no problem — maximal human review is always the correct default for AI systems.

B. Blanket human-in-the-loop on every decision defeats the purpose of automation; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions.

C. Human reviewers are less accurate than the model, so this would reduce quality.

D. This approach violates GDPR.

Correct answer: B

Explanation: Human-in-the-loop is most valuable where the cost of an error is high or where judgment genuinely requires human context. Applying it to every decision erases the efficiency gains the system was built to provide, without a proportional safety benefit for low-stakes decisions.

Distractors:

- A: Blanket review isn't automatically "safest" — it has a real cost in defeating the system's purpose, which is part of the tradeoff an architect must weigh.
- C: Relative accuracy of humans vs. the model isn't the stated architectural objection here.
- D: This scenario doesn't describe a GDPR-specific issue.

## Question 13

Scenario: An architecture team is choosing between a workflow pattern and an agentic pattern for a new invoice-processing feature. Invoices arrive in a small number of known formats and always require the same four processing steps in the same order.

Question: Which two considerations most strongly favor a workflow pattern over an agentic pattern here? (Select TWO responses.)

A. The task is well-defined and repeatable with a predictable sequence of steps.

B. A fixed pipeline is easier to test, monitor, and reason about than a model-driven decision path when the sequence never actually varies.

C. Agentic patterns are always more expensive regardless of the task.

D. Workflows can call more tools than agents can.

Correct answer: A, B

Explanation: A predictable, repeatable sequence is the textbook case for a workflow: it's simpler to test, monitor, and operate than an agentic pattern, and a fixed pipeline doesn't sacrifice anything when the steps genuinely never vary.

Distractors:

- C: Cost depends on the specific configuration (models, tool calls, retries), not the pattern category alone.
- D: Tool-calling capacity isn't a structural difference between workflows and agents.

## Question 14

Scenario: A client's Claude Code usage across a 40-engineer team is inconsistent — some engineers get project conventions applied automatically, others don't, and MCP server access varies by machine.

Question: As the architect responsible for developer productivity enablement, what is the most effective fix?

A. Tell each engineer individually to check their local configuration.

B. Standardize CLAUDE.md hierarchy and shared MCP server configuration at the project/team level so behavior doesn't depend on individual local setup.

C. Restrict Claude Code to a single designated "AI engineer" role to reduce variance.

D. Accept the inconsistency as an unavoidable cost of AI tooling adoption.

Correct answer: B

Explanation: Standardizing CLAUDE.md and shared MCP configuration at the team/project level is an architectural responsibility that directly reduces onboarding friction and behavioral inconsistency across a team — treating it as individual preference is what caused the drift in the first place.

Distractors:

- A: Individual troubleshooting doesn't fix the systemic lack of shared configuration causing the drift.
- C: Restricting usage to one role abandons the productivity benefit for the rest of the team rather than fixing the consistency problem.
- D: The inconsistency is fixable through standard configuration management, not an inherent limitation.
