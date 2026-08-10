# Exam Guide Gap Pack — Architect: Professional (CCAR-P)

- Source URL: `exam_guide_architect_professional.txt` (official exam guide v1.0, effective July 2026)
- Study pack: `study_packs_architect_professional/exam-guide-gap-pack/`
- Purpose: primary study pack for CCAR-P, built directly from the exam guide's content outline. This exam is architecture- and judgment-heavy — it tests tradeoff reasoning and stakeholder/governance judgment more than syntax, reflecting the Professional-tier target candidate (3+ years systems architecture, 6+ months hands-on Claude in production).

## Exam Domain Mapping

| Domain | Weight | Covered Ideas |
|---|---|---|
| D1: Solution Design & Architecture | 17% | Translating business problems into solutions, end-to-end architecture, workflow/agentic/augmented-LLM patterns, multi-agent orchestration, decomposition, business value alignment |
| D2: Claude Models, Prompting & Context Engineering | 13% | Model selection tradeoffs, system prompts/templates/guardrails, prompting techniques, context/token optimization, prompt reuse (caching, modular prompts, Skills) |
| D3: Integration | 19% | Tool/agent capability bloat, auth/authz gaps, accuracy-latency tradeoffs, observability at scale, RAG pipeline design, retrieval strategy, connection protocol selection (MCP/API/agent-to-agent), progressive discovery vs. monolithic context |
| D4: Evaluation, Testing & Optimization | 16% | Eval metrics, dataset/test-framework design, A/B testing, diagnosing failure modes, cost/latency optimization, observability tooling |
| D5: Governance, Safety & Risk Management | 14% | Guardrails, LLM risk/failure modes, human-in-the-loop, regulatory compliance (GDPR/HIPAA/FedRAMP), ethical AI (bias/fairness/transparency) |
| D6: Stakeholder Communication & Lifecycle Management | 14% | Discovery/requirements gathering, communicating tradeoffs, stakeholder feedback/SLA alignment, documentation, lifecycle phase support |
| D7: Developer Productivity & Operational Enablement | 7% | Configuring team tooling (Claude Code), AI-assisted workflow improvement, debugging/operational support |

## Key Concepts

### D1 — Solution Design & Architecture

- Translating a business problem into a Claude-based solution starts with the business value pillar it serves (efficiency, transformation, productivity, cost, or a performance SLA) — the architecture should be traceable back to that value, not just "we added AI."
- End-to-end architecture reasoning: input → processing → output → feedback loop. A design missing the feedback loop can't improve after deployment; treat it as a first-class architectural component, not an afterthought.
- Architectural pattern selection:
  - **Workflow**: fixed, predetermined sequence of LLM calls and tools — pick when the task is well-defined and repeatable.
  - **Agentic**: the model determines its own steps — pick when the path varies by case and depends on intermediate results.
  - **Augmented LLM**: a single LLM call enhanced with tools/retrieval but without multi-step autonomous orchestration — pick for simpler augmentation needs that don't warrant full agent overhead.
- Multi-agent systems and orchestration: a coordinator/supervisor delegates to specialized subagents. Route all inter-subagent communication through the coordinator (hub-and-spoke) for observability, consistent error handling, and controlled information flow — direct subagent-to-subagent channels sacrifice all three.
- Decomposition techniques: break a complex problem into subtasks whose combined coverage matches the full scope. A common failure mode is narrow decomposition — every subagent succeeds, but the decomposition itself omitted whole subdomains, and the fix is decomposition breadth, not subagent tuning.
- Business value alignment: the same technical solution can be justified on efficiency (do the same work with less cost) or transformation (do previously-impossible work) grounds — get explicit about which value pillar is the case for a given investment, since it changes what "success" measures should be.

### D2 — Claude Models, Prompting & Context Engineering

- Model selection tradeoffs: capability, cost, and latency move together — Opus-tier for the hardest reasoning, Haiku-tier for high-volume/low-latency simple tasks, Sonnet-tier as the balanced default. An architect's job is matching the tier to the task's actual difficulty, not defaulting to the most capable model everywhere.
- System prompts, templates, and guardrails: system prompts define role and constraints; templates standardize prompt structure across a product surface; guardrails layer programmatic checks on top of prompt-level guidance for anything that must hold reliably.
- Prompting techniques: zero-shot (no examples) for simple, well-understood tasks; few-shot for tasks needing consistent formatting or edge-case handling; chain-of-thought for tasks benefiting from explicit intermediate reasoning steps.
- Context window and token optimization: a long static system prompt and reference document repeated on every request is a caching opportunity, not just a cost line item — ordering stable content first and enabling prompt caching reduces both latency (time-to-first-token) and per-request cost.
- Prompt reuse strategies: caching (stable prefixes), modular prompts (composable, versioned prompt fragments), and Skills (on-demand reusable workflows) are three different reuse mechanisms solving different problems — caching is a cost/latency lever, modular prompts are a maintainability lever, Skills are a capability-packaging lever.

### D3 — Integration

- Tool/agent capability bloat: as an agent's toolset grows past what its role needs, tool-selection reliability degrades. Evaluate configurations for unnecessary capability and scope tools to role, or split into specialized agents.
- Authentication and authorization gap analysis: apply least privilege — remove capabilities a role doesn't need rather than only logging or confirming their use. A tool an agent doesn't need is an attack surface, not a convenience.
- Accuracy-latency tradeoffs: more retrieval, more verification steps, or a larger model generally buys accuracy at the cost of latency (and money). Justify the chosen point on that curve against the actual SLA, not a default assumption that "more accurate is always better."
- Observability at scale: logging every raw prompt/response for a high-volume production system is not itself an observability strategy — select monitoring approaches (sampling, structured event logging, aggregate quality metrics) that scale with volume without drowning the team in unreviewable data.
- RAG pipeline design: chunking strategy and indexing strategy must match the data's shape — long-form documents need different chunking than structured records or short FAQ entries. A retrieval strategy that ignores data shape produces irrelevant or fragmented context.
- Retrieval strategy matched to query pattern: exact-lookup queries favor structured/metadata filtering; conceptual/semantic queries favor embedding similarity search; hybrid queries often need both.
- Connection protocol selection: MCP for reusable, cross-application tool/resource access; direct API/CLI integration for tightly-coupled, single-application needs; agent-to-agent protocols when multiple autonomous systems (potentially from different vendors or teams) need to collaborate without a shared codebase.
- Progressive discovery vs. monolithic context: progressive discovery (expose a catalog/resource an agent queries as needed) scales better than dumping an entire dataset or tool schema set into context up front, especially as the underlying data or tool set grows.

### D4 — Evaluation, Testing & Optimization

- Evaluation metrics span more than accuracy: latency, cost, safety, and security must be defined and tracked as first-class metrics alongside correctness — a solution that's accurate but too slow, too expensive, or unsafe still fails.
- Evaluation dataset and test framework design: use mixed methodologies — automated metric-based evals for scale, human review for nuanced judgment, and adversarial/red-team test cases for safety-critical paths. No single method covers every failure mode.
- A/B testing and iterative improvement: change one variable at a time (a prompt, a model tier, a retrieval strategy) against a stable baseline so you can attribute observed differences correctly.
- Diagnosing system issues: distinguish prompt failure (the instructions were unclear or contradictory), hallucination (the model asserted something false confidently), and model mismatch (the wrong capability tier for the task) — each has a different fix, and treating all three the same way wastes iteration cycles.
- A confident-but-wrong answer appearing after a document refresh, with model and latency unchanged, points first at the retrieval/indexing layer (stale or broken embeddings/index), not the model.
- Cost-performance optimization: token usage, latency, and cost tradeoffs should be optimized against the actual SLA and budget, not minimized in isolation — the cheapest, fastest configuration that fails the accuracy bar isn't a win.
- Monitoring: production logging and observability tooling should surface drift (quality degrading over time) and outliers, not just aggregate averages that can hide a failing segment.

### D5 — Governance, Safety & Risk Management

- Guardrails and safety controls: layer multiple defenses (prompt-level guidance, programmatic gates/hooks, monitoring) rather than relying on any single layer to catch everything.
- Risk, limitation, and failure-mode identification: know the standard LLM failure modes (hallucination, prompt injection, inconsistent output, context loss/drift) and design mitigations for each as part of the architecture, not as an afterthought once something breaks in production.
- Human-in-the-loop (HITL) validation: apply HITL where the cost of an error is high or where judgment genuinely requires human context (e.g., approving refunds over a threshold, medical or legal determinations) — not as a blanket requirement on every model output, which defeats the purpose of automation.
- Regulatory compliance: GDPR (EU data protection/privacy), HIPAA (US healthcare data), FedRAMP (US federal cloud security authorization) are examples of regimes that constrain what data can be sent where, retained how long, and processed under what controls — compliance requirements shape architecture decisions (data residency, retention, access logging) before feature design, not after.
- Ethical AI considerations: bias, fairness, and transparency are architecture concerns — e.g., whether training/eval data reflects the population the system serves, whether decisions are explainable to affected users, and whether disparate impact is measured, not just assumed absent.

### D6 — Stakeholder Communication & Lifecycle Management

- Structured discovery and requirements gathering: elicit both explicit requirements (what stakeholders say they need) and implicit constraints (compliance, existing systems, org politics) before committing to an architecture.
- Communicating architectural decisions and tradeoffs: stakeholders need the tradeoff, not just the decision — e.g., "we chose Sonnet over Opus for this path, trading some capability for a 3x latency improvement that meets the SLA" is more useful than "we chose Sonnet."
- Managing stakeholder feedback loops and SLA alignment: set and revisit explicit SLAs (accuracy thresholds, latency targets, cost ceilings) with stakeholders rather than letting "good enough" be implicitly renegotiated after the fact.
- Documentation and implementation guidance: architecture documentation should let another engineer implement or extend the system without re-deriving the reasoning behind each decision — capture the "why," not just the "what."
- Lifecycle phase support: discovery → design → handoff → monitoring → iteration. An architect's responsibility doesn't end at handoff — monitoring and iteration based on production signal are part of the lifecycle, not a separate team's problem.

### D7 — Developer Productivity & Operational Enablement

- Configuring Claude tools and environments for teams: standardizing CLAUDE.md, settings.json, and shared MCP configuration across a team reduces inconsistent behavior and onboarding friction — this is an architectural responsibility, not just individual developer preference.
- Improving developer workflows with AI-assisted tooling: identify where Claude Code or similar tooling removes real friction (repetitive refactors, codebase exploration, test generation) versus where it adds review overhead that exceeds the time saved.
- Supporting debugging and operational issue resolution: architects should be able to read traces/logs from production Claude-powered systems to localize whether an incident is an integration-layer problem, a model-output problem, or a data/retrieval problem — the same triage skill developers use, applied at a systems level.

## Decision Rules

- If the task is well-defined and repeatable, use a workflow; if the right steps vary by case and depend on intermediate results, use an agent; if you just need to augment one LLM call with tools/retrieval, an augmented LLM pattern may be enough — don't reach for full multi-agent orchestration by default.
- If subagents all succeed but the final output still misses whole subdomains, fix the coordinator's decomposition breadth, not the subagents.
- If a hard rule (financial, safety, compliance) must hold every time, enforce it with a guardrail/hook, not a prompt instruction alone.
- If an agent's tools include capabilities its role doesn't need, remove them — don't just add logging or confirmation steps.
- If retrieval quality suddenly degrades after a document/data refresh with model and latency unchanged, investigate the indexing/retrieval layer first.
- If observability at scale means "log everything raw," redesign toward sampling and structured, aggregable signals instead.
- If a compliance regime applies (GDPR/HIPAA/FedRAMP), resolve data residency/retention/access-control requirements before finalizing the architecture, not after.
- If an error's cost is high or requires human judgment, apply human-in-the-loop specifically there — not everywhere, which defeats automation's value.
- If communicating a decision to stakeholders, state the tradeoff, not just the choice.
- If a document/data source shows aggregate accuracy but you're deciding whether to cut human review, check accuracy per segment (document type, field, use case) before trusting the aggregate.

## Anti-Patterns

- Defaulting to full multi-agent orchestration for tasks that a single augmented LLM call or a fixed workflow would handle more simply and reliably.
- Justifying an architecture as "we added AI" without tracing it to a specific business value pillar or measurable outcome.
- Direct subagent-to-subagent communication that bypasses the coordinator.
- Relying on prompt-level instructions alone for compliance- or safety-critical rules.
- Growing an agent's toolset indefinitely instead of scoping to role.
- Treating "more accurate" as free — ignoring the latency/cost tradeoff against the actual SLA.
- Logging raw prompts/responses at scale and calling it an observability strategy.
- Applying human-in-the-loop everywhere as a blanket safety measure, defeating automation's purpose.
- Treating compliance as a post-launch checklist item rather than an architecture input.
- Trusting an aggregate accuracy number without segment-level validation before reducing human review.
- Documenting only the final architecture without the reasoning ("why") behind key decisions.

## Scenario Traps

- "Add another subagent" when the real problem is coordinator decomposition breadth or capability bloat in an existing agent — more agents isn't automatically better architecture.
- "Switch to a bigger/more capable model" for problems actually caused by retrieval, context management, or prompt clarity — model tier is not a universal fix.
- "Full audit logging" presented as an observability solution at scale — raw logs alone don't scale into an actionable monitoring strategy.
- "Require human approval on every output" presented as the safe governance choice — the exam wants targeted HITL matched to error cost/judgment need, not blanket friction.
- A stakeholder-communication question where the "technically correct" answer omits the tradeoff explanation — the Professional exam rewards communicating tradeoffs, not just correct technical calls.

## Memorization Cues

- **Workflow = fixed. Agent = adaptive. Augmented LLM = single call + tools/retrieval, no orchestration.**
- **Hub-and-spoke: all subagent traffic through the coordinator.**
- **Decomposition breadth, not subagent tuning, fixes coverage gaps.**
- **Guardrails/hooks for guarantees; prompts for guidance.**
- **Retrieval/indexing is the first suspect after a data refresh breaks accuracy.**
- **Sample and structure observability data — don't just log everything raw.**
- **Compliance shapes architecture before feature design, not after.**
- **HITL where error cost or judgment is high — not everywhere.**
- **Communicate the tradeoff, not just the decision.**
- **Segment before you trust the aggregate.**

## Source References

- Exam guide Domain 1–7 content outline and detailed objectives (`exam_guide_architect_professional.txt`)
- Exam guide Section 8 sample questions (least privilege, prompt caching for latency/cost, retrieval regression diagnosis)

## Gaps / Follow-Up

- This pack is doctrine from the guide's task statements, not hands-on repetition. The guide's own preparation recommendation — build and operate at least one end-to-end Claude solution including RAG, evaluation, and observability — is the single highest-leverage follow-up activity.
- Deeper mechanics of prompt caching, hooks, and MCP protocol details overlap with the Developer: Foundations gap pack (`study_packs_developer_foundations/exam-guide-gap-pack/notes.md`) — worth a skim, since this exam tests judgment about *when* to use these mechanisms more than implementation syntax.
