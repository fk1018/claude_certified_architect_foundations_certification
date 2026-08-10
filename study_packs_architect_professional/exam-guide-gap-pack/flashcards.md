# Exam Guide Gap Pack Flashcards — Architect: Professional

## Workflow vs. Agentic vs. Augmented LLM

Q: What are the three architectural patterns an architect chooses among, and what distinguishes them?

A: Workflow (fixed, predetermined sequence), agentic (model decides its own steps), and augmented LLM (a single call enhanced with tools/retrieval but no multi-step orchestration). Choose based on whether the task path is fixed, variable, or just needs light augmentation.

## Business Value Pillars

Q: Name the business value pillars an AI architecture should trace back to.

A: Efficiency, transformation, productivity, cost, and performance SLAs. An architecture without a clear pillar is hard to justify or measure.

## Feedback Loops in Architecture

Q: Why treat the feedback loop as a first-class part of an end-to-end architecture rather than an afterthought?

A: Without it, the system can't improve after deployment — input/processing/output alone is a one-shot design with no mechanism to learn from production signal.

## Hub-and-Spoke Orchestration

Q: Why should all subagent communication route through the coordinator rather than directly between subagents?

A: It preserves observability, consistent error handling, and controlled information flow. Direct subagent-to-subagent channels sacrifice all three.

## Narrow Decomposition Failure

Q: Every subagent in a multi-agent system succeeds, yet the final output misses whole subdomains of the task. What's the root cause and fix?

A: The coordinator's decomposition was too narrow — it never assigned those subdomains to any subagent. Fix decomposition breadth, not subagent performance.

## Model Tier Tradeoff

Q: What's the architect-level framing for choosing among Opus/Sonnet/Haiku tiers?

A: Match capability tier to actual task difficulty — capability, cost, and latency move together, so defaulting to the most capable tier everywhere overspends on tasks that don't need it.

## Prompt Caching for Latency and Cost

Q: An application resends the same 8,000-token system prompt and policy document on every request. What single change most directly reduces both latency and cost?

A: Order the static content first and enable prompt caching — this reduces time-to-first-token and per-request cost without discarding needed content.

## Prompt Reuse Mechanisms

Q: Caching, modular prompts, and Skills are all "prompt reuse strategies" — what problem does each solve?

A: Caching is a cost/latency lever (reusing a stable prefix); modular prompts are a maintainability lever (composable, versioned fragments); Skills are a capability-packaging lever (on-demand reusable workflows).

## Least Privilege in Integration

Q: A customer-support agent has refund and account-deletion tools it never needs for its actual role. What's the least-privilege fix, and what's the weaker alternative?

A: Remove the unneeded tools entirely. Adding logging or a confirmation step only monitors or slows misuse — it doesn't eliminate the unnecessary attack surface.

## Accuracy-Latency Tradeoff

Q: How should an architect justify a chosen point on the accuracy-latency-cost curve?

A: Against the actual SLA and budget for that use case — "more accurate" is not free, and the right tradeoff point depends on what the task actually requires, not a default assumption that more is always better.

## Observability at Scale

Q: Why isn't "log every raw prompt and response" an adequate observability strategy for a high-volume production system?

A: Raw logs at volume aren't reviewable or actionable. Effective observability needs sampling, structured event logging, and aggregate quality metrics that surface drift and outliers.

## RAG Chunking and Data Shape

Q: Why can't one chunking/indexing strategy serve both long-form documents and short structured FAQ entries equally well?

A: Chunking and indexing strategy must match the data's shape — a strategy tuned for long-form prose fragments or dilutes short structured records, and vice versa.

## Retrieval Strategy by Query Pattern

Q: When does an architect favor structured/metadata filtering over embedding similarity search for retrieval?

A: For exact-lookup queries (specific IDs, dates, categories). Embedding similarity search fits conceptual/semantic queries better; many real systems need both (hybrid retrieval).

## Connection Protocol Selection

Q: When is MCP the right integration mechanism versus a direct API/CLI integration?

A: MCP fits reusable, cross-application tool/resource access maintained independently of any one app. Direct API/CLI integration fits tightly-coupled, single-application needs where reuse isn't a goal.

## Progressive Discovery vs. Monolithic Context

Q: Why does exposing a queryable catalog/resource scale better than loading an entire dataset or full tool schema set into context up front?

A: Progressive discovery lets an agent pull only what it needs per task; monolithic context grows unboundedly with the underlying data or tool set and wastes context budget on unused material.

## Retrieval Regression Diagnosis

Q: A RAG system starts returning confident but incorrect answers right after a document refresh; model version and latency are unchanged. Where do you look first?

A: The retrieval/indexing layer — a broken re-index or mismatched embeddings is the most likely cause of a regression tied specifically to a data refresh event.

## Diagnosing Prompt Failure vs. Hallucination vs. Model Mismatch

Q: Why does it matter whether a bad output is a prompt failure, a hallucination, or a model mismatch?

A: Each has a different fix — clarify instructions, add grounding/verification, or change capability tier respectively. Treating all three the same way wastes iteration cycles on the wrong lever.

## Segment-Level Validation

Q: A system shows 97% aggregate accuracy. Why shouldn't that number alone justify cutting human review?

A: Aggregate accuracy can hide a failing segment — one document type or field can perform far worse than the average while the overall number still looks healthy. Segment before you trust the aggregate.

## Human-in-the-Loop Placement

Q: Why is "require human approval on every model output" not the correct governance default?

A: It defeats the purpose of automation. HITL should be targeted at high error-cost or genuinely judgment-requiring decisions (e.g., large refunds, medical/legal determinations), not applied blanket.

## Compliance as Architecture Input

Q: Why should GDPR/HIPAA/FedRAMP-type requirements be resolved before finalizing an architecture rather than after?

A: They constrain data residency, retention, and access-control design at a structural level — retrofitting compliance after the architecture is set is far more costly and sometimes impossible without a redesign.

## Communicating Tradeoffs

Q: What makes "we chose Sonnet over Opus for this path" a weaker stakeholder communication than the fuller version?

A: It states the decision without the tradeoff. "We traded some capability for a 3x latency improvement that meets the SLA" gives stakeholders the reasoning they need to evaluate and revisit the decision later.

## Lifecycle Ownership Beyond Handoff

Q: Does an architect's responsibility end at solution handoff?

A: No — the lifecycle includes discovery, design, handoff, monitoring, and iteration. Monitoring production signal and iterating based on it are part of the architect's ongoing responsibility.

## Developer Productivity Enablement

Q: Why is standardizing CLAUDE.md and shared MCP configuration across a team an architectural concern, not just individual preference?

A: Inconsistent per-developer configuration produces inconsistent Claude Code behavior across a team and onboarding friction — standardizing it is a deliberate architectural decision with team-wide impact.
