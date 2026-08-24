# CCARP Practice Exam 4

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent Customer-Escalation Platform, Model Selection and Context Engineering for Retail Merchandising, Evaluation and Monitoring of Field-Service Dispatch, Governance and Team Enablement for Insurance Claims Modernization) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**. |

Domain distribution (approximate, matches the official blueprint weightings):

| Domain | Questions |
|---|---|
| D1: Solution Design & Architecture (17%) | 10 |
| D2: Claude Models, Prompting & Context Engineering (13%) | 8 |
| D3: Integration (19%) | 11 |
| D4: Evaluation, Testing & Optimization (16%) | 10 |
| D5: Governance, Safety & Risk Management (14%) | 8 |
| D6: Stakeholder Communication & Lifecycle Management (14%) | 8 |
| D7: Developer Productivity & Operational Enablement (7%) | 5 |

Answer key with explanations is at the end of this file. Answer every question before checking — the real exam does not allow skipping.

---

## Scenario A: Multi-Agent Customer-Escalation Platform for a Telecom Retailer (Questions 1–15)

NorthWave Mobile, a regional telecom retailer, wants to modernize how frontline store and call-center escalations are triaged and resolved. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with NorthWave's stakeholders.

---

**Question 1.** Discovery reveals NorthWave's actual goal is reducing average escalation resolution time for the existing complaint volume, not adding new self-service capabilities the current process lacks.

- A) Frame the architecture around transformation, arguing that even a resolution-time win should be marketed as a broader self-service capability rollout so the initiative reads as innovation to the steering committee.
- B) Frame the architecture around cost reduction exclusively, since headcount savings are easier to quantify than resolution-time improvements even though discovery pointed elsewhere.
- C) Skip framing around any specific value pillar, since a working system speaks for itself once escalations start resolving faster.
- D) Frame the architecture around efficiency, and build success metrics around resolution-time reduction for the existing complaint volume.

**Question 2.** Escalation handling follows one of three well-defined steps — verify identity, check account status, apply the resolution script — always in the same order regardless of case specifics.

- A) An agentic pattern, since even fixed-looking escalation steps secretly require the model to decide its own step order and tool calls at runtime.
- B) A fixed workflow, since the three steps — verify identity, check account status, apply the resolution script — are well-defined and always executed in that same order regardless of case specifics.
- C) An augmented LLM pattern, treating the three steps as one enhanced call with retrieval rather than a defined sequence.
- D) Whichever pattern the team can ship fastest this sprint, since all three patterns produce equivalent reliability for a process like this.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (sentiment analysis, account lookup, resolution drafting, compliance check).

- A) Let subagents communicate directly with whichever subagent needs their output next, skipping the coordinator entirely so hops are minimized and each subagent negotiates handoffs and retries with its peers.
- B) Merge all four responsibilities into one subagent to avoid the coordination overhead of separate roles.
- C) Let subagents communicate directly with each other, but log the traffic afterward for later review.
- D) Route all inter-subagent communication through the coordinator, preserving observability and consistent error handling.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition only routes billing-dispute complaints — network-outage complaints are never routed to any subagent and silently fall through.

- A) Add a fifth subagent dedicated to network-outage complaints, leaving the coordinator's existing routing logic for the other categories untouched.
- B) Give the existing four subagents broader tool access and instructions so any of them can attempt to handle a network-outage complaint that reaches it, without changing how the coordinator assigns work.
- C) Fix the coordinator's decomposition so it explicitly covers all complaint categories, including network-outage complaints.
- D) Add a prompt instruction telling subagents to flag any complaint type they don't recognize, without adding any validation of the coordinator's routing itself.

**Question 5.** The design must align technical architecture to a specific business value pillar NorthWave actually cares about, distinct from a generic "we added AI" narrative.

- A) Business value pillars are a sales and marketing concern that architects should leave entirely out of the technical design.
- B) Efficiency, transformation, productivity, cost, and performance SLAs are examples of such pillars; the one NorthWave actually cares about should drive both the architecture and its success metrics.
- C) Any AI system inherently demonstrates transformation on its own, so no additional pillar-specific framing is needed.
- D) The pillar should be picked after the system ships, based on whichever benefit turns out easiest to measure in hindsight.

**Question 6.** NorthWave's frontline store associates are worried automation will replace their role in handling escalations, and discovery interviews surface this repeatedly.

- A) Treat it as a real implicit constraint alongside the explicit technical requirements — it shapes adoption, rollout sequencing, and where human-in-the-loop checkpoints matter most.
- B) Ignore the sentiment in the architecture, since job-security worries aren't a technical requirement the system needs to satisfy.
- C) Proceed with the technical design as planned and let a separate change-management workstream handle the sentiment with no input from the architecture itself.
- D) Recommend against the project entirely, since repeated frontline concern about job displacement during discovery interviews is itself grounds to halt an automation initiative before design even starts.

**Question 7.** A stakeholder asks why the churn-risk assessment subagent uses a higher-capability, higher-cost model tier than the ticket-summarization subagent.

- A) Tell the stakeholder "higher tier because it's more important" and move on, since that framing is sufficient for a non-technical audience.
- B) Explain the tradeoff explicitly: churn-risk assessment needs deeper reasoning that justifies the added cost and latency, while ticket summarization is simpler and better served by a faster, cheaper tier.
- C) Standardize on the same model tier for every subagent in the pipeline for simplicity, regardless of how much structured reasoning depth each task requires.
- D) Avoid explaining the tier difference at all, since stakeholders outside engineering don't need technical detail about model selection.

**Question 8.** The architecture's current design produces a final resolution recommendation with no mechanism to learn from agent overrides or customer outcomes over time.

- A) This is acceptable as designed, since the initial architecture already reflects current best practice and doesn't need a feedback mechanism to remain sound.
- B) Add a feedback loop as a first-class architectural component, with explicit hooks for capturing agent overrides and customer outcomes so the system can improve post-deployment.
- C) Feedback loops are a data-science training concern unrelated to the architecture the architect is responsible for.
- D) Defer any feedback mechanism to a hypothetical future phase, with no hooks or data-capture points built into the current design.

**Question 9.** NorthWave wants a single enhanced LLM call — with retrieval of plan and billing FAQ documents — to answer straightforward plan-question escalations, without any multi-step autonomous orchestration.

- A) Build a full multi-agent architecture with a coordinator and specialized subagents regardless of how simple the underlying plan-question task actually is.
- B) This cannot be built with Claude at all, since anything without autonomous multi-step orchestration or built-in output validation doesn't count as a real AI system.
- C) This requires a fixed workflow with at least five sequential steps, since any use of retrieval alongside an LLM call implies a structured multi-step pipeline that must be modeled and ordered explicitly.
- D) An augmented LLM pattern — a single call enhanced with retrieval and tools — fits this simpler augmentation need without agentic orchestration overhead.

**Question 10.** The account-lookup subagent's toolset has grown to include tools for tasks like store-locator search and promotional-offer generation, unrelated to account lookup.

- A) This has no architectural downside as long as the subagent's instructions are written clearly enough, with no separate tool-selection validation needed, to explain when each tool applies.
- B) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or relocated to a more appropriate subagent.
- C) More tools always improve a subagent's flexibility and should be actively encouraged, since a broader toolset only ever expands what a single subagent is capable of handling on its own.
- D) The fix for this kind of tool sprawl is to increase the subagent's context window so it can reason about more candidate tools at once.

**Question 11.** The coordinator currently processes each escalation sequentially through identity verification, account lookup, sentiment analysis, and resolution drafting, even though account lookup and sentiment analysis have no dependency on each other's output.

- A) Sequential processing is required for auditability, since only a strict one-after-another order can produce a defensible trail.
- B) Combine account lookup and sentiment analysis into a single subagent so the sequencing question doesn't need to be answered at all.
- C) Run account lookup and sentiment analysis as independent, parallel subagent calls once identity verification completes, since neither has any dependency on the other's output and both feed into the later resolution-drafting step.
- D) Parallelization is not architecturally possible once a coordinator is delegating to specialized subagents, regardless of whether their inputs are independent.

**Question 12.** NorthWave asks how end-to-end architecture should be described at a high level for a retail-operations steering committee unfamiliar with the technical details.

- A) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, without requiring implementation detail.
- B) Present only the model names and per-token costs involved in the system, leaving process and outcome framing out of the discussion.
- C) Present the full technical architecture diagram, including subagent boundaries, tool schemas, and routing logic, with no simplification for a non-technical steering committee unfamiliar with any of those concepts.
- D) Skip a high-level description entirely and go straight into a live implementation demo for the committee.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (identity verification, account lookup, sentiment analysis, resolution drafting) rather than a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows, since one agent holding every tool avoids the coordination overhead of routing work between specialized subagents and keeps the whole toolset available for any request.
- B) Specialized subagents are strictly a cost-increasing choice with no offsetting reliability benefit over a single agent.
- C) There's no meaningful architectural difference between a single generalist agent and a coordinator with specialized subagents.
- D) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than subagents scoped to narrower roles.

**Question 14.** The architecture must eventually support a new escalation category (satellite-internet outage complaints) NorthWave plans to launch next year, but detailed requirements aren't available yet.

- A) Ignore future escalation categories entirely until detailed requirements for satellite-internet outages actually exist.
- B) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for the speculative, still-undefined satellite-outage requirements.
- C) Build full support for satellite-internet-outage complaints now, guessing at requirements that haven't been defined yet.
- D) Refuse to proceed with the current phase of work until the future satellite-outage requirements are fully finalized.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values — model tiers, timeout thresholds, routing rules — on the theory that a well-organized implementation is self-explanatory to any engineer who reads the code carefully enough.
- B) Document the architecture and the reasoning behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final configuration.
- C) Rely on the original architect remaining available indefinitely to answer questions instead of writing anything down.
- D) Documentation is unnecessary as long as the code itself is well-organized and readable.

---

## Scenario B: Model Selection and Context Engineering for a Retail Merchandising Copilot (Questions 16–30)

A national retail chain wants Claude to help category managers with pricing, assortment, and promotion questions, combining general reasoning with retrieval over product catalogs, sales data, and vendor contracts. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most merchandising questions are moderately complex; a small fraction require deep multi-step analysis across many SKUs, and a small fraction are simple lookups.

- A) Use one fixed model tier for every merchandising question, regardless of whether it's a simple SKU lookup or a deep multi-SKU analysis.
- B) Always use the highest-capability tier to guarantee top quality on every single question, accepting the added cost and latency across the entire volume of simple lookups, typical questions, and deep multi-step analyses alike.
- C) Route based on task difficulty — a fast tier for simple lookups, a balanced tier for typical questions, and a higher-capability tier for the deep multi-step cases, rather than temperature tuning as a shortcut.
- D) Always use the fastest, cheapest tier to minimize cost, accepting quality loss on the complex questions.

**Question 17.** Every request sends the same long system prompt (merchandiser persona, formatting rules, pricing-policy guardrails) followed by retrieved catalog and vendor excerpts that vary per query.

- A) Order doesn't affect cost or latency for this use case, since the API processes the entire prompt as a single unit regardless of how the system prompt and retrieved content are arranged.
- B) Alternate the system prompt and retrieved content in a structured, interleaved pattern throughout the request so each guardrail rule sits next to the catalog data it governs.
- C) Put the retrieved catalog and vendor content first, ahead of the system prompt, since it's most relevant to the specific query being answered.
- D) Place the stable system prompt first and enable prompt caching, with the varying retrieved catalog and vendor content after it, to reduce both latency and cost across the high query volume.

**Question 18.** The corpus mixes long-form vendor contracts with short structured data (a table of SKU-level price points).

- A) One chunking and indexing strategy tuned for long-form vendor contracts can serve the short structured SKU-price table equally well without any adjustment.
- B) Structured SKU-price data should be excluded from retrieval entirely, since only the long-form contract text is worth indexing for this copilot.
- C) Use the largest possible chunk size for both the long-form contracts and the short structured price table, so a single oversized chunking policy avoids the extra engineering work of maintaining two separate strategies for two different data shapes.
- D) Chunking and indexing strategy should match each data shape — long-form documents need different chunking than short structured records, or retrieval quality degrades for whichever type doesn't match.

**Question 19.** Category-manager queries range from exact lookups ("current price for SKU 48213") to conceptual questions ("how has the athleisure category's margin mix shifted over the last three seasons").

- A) Use only embedding similarity search for every query type, from exact SKU lookups to conceptual margin-mix questions.
- B) Use only structured/metadata filtering for every query type, including the open-ended conceptual questions about category trends.
- C) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where a query needs both.
- D) Query pattern doesn't affect which retrieval approach is appropriate for a merchandising copilot, since a single well-tuned embedding index can serve exact SKU lookups and open-ended conceptual questions with equal precision regardless of query shape.

**Question 20.** Category managers need pricing claims that reliably map to a specific source document and section, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite your sources" for every pricing claim, without any further structure around how that citation is captured.
- B) Append a general bibliography of every document consulted at the end of the response, without tying any individual claim to a specific document or section.
- C) Require structured output pairing each claim with its source (document, section, excerpt) so citation mapping survives synthesis instead of being reconstructed from memory afterward.
- D) Add citations after the fact by searching for a plausible-sounding source for each claim once the response has already been drafted.

**Question 21.** Two retrieved sources disagree on a SKU's current wholesale cost by a small margin — likely due to different contract effective dates.

- A) Present both figures explicitly, annotated as a discrepancy, with source attribution and the likely explanation (e.g., differing contract effective dates), rather than silently picking one.
- B) Average the two conflicting wholesale-cost figures together and present the single averaged number as the answer.
- C) Omit the wholesale cost figure from the response entirely, since the two sources disagree and neither can be confirmed as authoritative.
- D) Always prefer whichever source document happens to have been retrieved first in the ranked results, on the assumption that retrieval order reflects reliability and that presenting a single confident number keeps the category manager from having to weigh a discrepancy themselves.

**Question 22.** A prompt asking the model to "always output valid structured JSON with a source field" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the "always output valid structured JSON" instruction more emphatically, in bold, at both the start and end of the prompt.
- B) Increase max_tokens substantially so there's enough room in the response for both the conversational preamble the model tends to add and the full structured JSON payload that follows it, on the assumption that more room prevents the preamble from appearing at all.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism itself rather than requested through prose alone.
- D) Post-process every response to strip any leading text before the first opening brace, without validating the JSON structure itself.

**Question 23.** The platform needs to connect to a proprietary vendor-contract management system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this copilot.

- A) Build an MCP server exposing the vendor-contract search and retrieval operations as tools and resources, reusable across the multiple internal Claude-powered tools that need this same access.
- B) Hard-code the vendor-contract integration directly into this copilot's application code, with no path for other internal tools to reuse it.
- C) Paste the entire vendor-contract corpus into every prompt this copilot sends, regardless of query relevance.
- D) Require each consuming tool to reimplement its own vendor-contract integration independently, each defining its own request schema and auth handling from scratch.

**Question 24.** The team is deciding between exposing the full SKU catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Loading the full SKU catalog directly into every prompt up front is always preferable for completeness, since it guarantees the agent never has to make a separate query to find a SKU that happens to be relevant to the current question.
- B) There's no meaningful difference in context cost between loading the full catalog up front and querying a catalog resource only when needed.
- C) The SKU catalog should never be exposed to the agent in any form, structured or otherwise.
- D) Progressive discovery — querying a catalog resource as needed — scales better than loading the entire catalog into context up front, especially as the catalog grows.

**Question 25.** A category manager asks a chain-of-thought-friendly question requiring the model to reason step by step across several retrieved sales reports before concluding on a recommendation.

- A) A chain-of-thought prompting approach, allowing the model to lay out explicit intermediate reasoning steps, is well suited to this kind of multi-document synthesis question spanning several sales reports.
- B) Zero-shot prompting with no reasoning guidance is always equally effective for questions that require synthesizing conclusions across several retrieved documents.
- C) Chain-of-thought prompting is only useful for coding tasks, not for business-analysis questions like margin or assortment recommendations.
- D) The model cannot meaningfully reason across multiple retrieved sales reports at all, regardless of which prompting approach — chain-of-thought, zero-shot, or otherwise — is used to structure the request, since synthesis across separate source documents exceeds what any single-call architecture can achieve.

**Question 26.** The platform wants to standardize prompt fragments (pricing-guardrail language, formatting rules, disclaimer text) across several merchandiser-facing features so changes propagate consistently.

- A) Duplicate the pricing-guardrail, formatting, and disclaimer fragments independently into each feature's prompt, so each feature owns its own copy.
- B) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).
- C) Modular prompt fragments are the same mechanism as prompt caching, so enabling caching on the system prompt already solves the propagation problem.
- D) Standardizing shared language across features isn't achievable through prompt design at all.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific figure from the correctly retrieved source document.

- A) Apply defensive validation — verify each extracted figure against the actual source excerpt and its stated effective date — rather than accepting confident, well-formatted phrasing as proof of accuracy.
- B) Trust the fluent, well-cited-looking output as sufficient evidence of correctness on the theory that a response citing the correct source document and formatted with confident, specific figures has already done the verification work implicitly, so no separate check should be needed.
- C) This is not something the architecture can address; it is purely a model limitation with no available mitigation.
- D) Increase the output length so the model has more room to arrive at the correct figure before finalizing its answer.

**Question 28.** The team debates whether merchandiser-facing latency SLAs should factor into model tier selection for the copilot.

- A) Latency should never factor into model or architecture decisions at all, since accuracy is the only dimension that matters for a merchandising copilot regardless of how slow a response becomes or how much that slowness frustrates category managers trying to work through dozens of pricing questions in a day.
- B) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, rather than defaulting to the most capable tier regardless of SLA.
- C) Only cost should factor into tier selection; latency SLAs are a separate operational concern that model selection shouldn't need to account for.
- D) SLAs are purely a stakeholder-communication concern with no bearing on the technical architecture or model tier chosen.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to "latest" automatically in production, since a newer model version with improved benchmark scores is always a deterministic improvement for every downstream task.
- B) Never upgrade the model version once the initial one is chosen, regardless of how much better a newer release measures on relevant benchmarks.
- C) Upgrade to the new version immediately without testing against the platform's own evaluation suite, since a benchmark improvement guarantees a production improvement.
- D) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.

**Question 30.** The platform's context budget is a concern because both the system prompt/guardrail rules and the retrieved catalog/vendor excerpts must fit alongside room for a detailed answer.

- A) Input and output tokens share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.
- B) Input and output token budgets are entirely independent of each other, so retrieved-content volume never constrains how much room is left for the answer.
- C) This budget tradeoff only matters for unusually long vendor contracts, never for a typical category-manager query with a short answer.
- D) Output length has no practical limit regardless of how much input content — system prompt, guardrails, and retrieved catalog and vendor excerpts — is already loaded into the same request's context window.

---

## Scenario C: Evaluation and Monitoring of a Field-Service Dispatch Assistant (Questions 31–45)

A Claude-powered assistant helps a utility company dispatch field technicians, recommending technician assignment, scheduling windows, and triage of urgent versus routine tickets. It's been in production for six months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only the correct-technician-assignment rate and hasn't defined targets for latency, cost, or safety.

- A) Assignment-rate alone is a sufficient evaluation metric, since correctly matching a technician to a ticket is the system's entire stated purpose.
- B) Latency and cost are operations-team concerns that sit outside evaluation design, so the eval strategy should stay focused on the technician-assignment outcome and leave throughput and spend to a separate infrastructure review.
- C) Safety metrics are only relevant for evaluation strategies in explicitly regulated industries like healthcare or finance, not a utility dispatch assistant.
- D) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics — a system that assigns well but is too slow, too expensive, or unsafe still fails overall.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past dispatch tickets.

- A) A single automated evaluation method against a fixed labeled set is sufficient for any production system, regardless of how safety-relevant its failure modes are.
- B) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for safety-relevant paths — since no single method covers every failure mode.
- C) Replace the automated checks entirely with human review as the sole evaluation method going forward.
- D) Expand the labeled set of past dispatch tickets indefinitely as the sole lever for improving evaluation coverage.

**Question 33.** The team wants to test whether a new triage-prompt version improves urgent-versus-routine classification before rolling it out to all traffic.

- A) Roll out the new triage-prompt version to all production traffic immediately and monitor for problems as they surface.
- B) Change the triage prompt and the underlying model tier simultaneously in the same rollout, on the theory that combining two improvements at once maximizes the chance of a measurable gain in classification quality.
- C) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.
- D) Skip a formal test entirely, since prompt changes are inherently low-risk and don't need pre-rollout evaluation.

**Question 34.** A technician assignment is wrong. Investigation shows the underlying technician-skill database was correct and retrieved properly, and the model's reasoning misapplied the skill-match logic.

- A) This is a retrieval problem; fix the indexing pipeline for the technician-skill database even though it was confirmed correct and retrieved properly.
- B) This cannot be diagnosed at all without retraining the underlying model from scratch.
- C) This is a model-capability mismatch requiring a switch to a different, higher-capability model tier regardless of the specific reasoning error that was actually made, since any wrong output implies the current tier is inadequate for the task.
- D) This is best characterized as a prompt/generation issue — misapplied logic over correctly retrieved data — which calls for prompt or output-validation fixes rather than retrieval changes.

**Question 35.** Immediately after a scheduled technician-skills database refresh, the system starts recommending mismatched technicians, while model version and average latency are unchanged.

- A) Suspect the model provider silently pushed an update to the underlying model version, even though the platform's recorded model version is unchanged.
- B) Investigate the retrieval/indexing layer first, since the regression started immediately after the scheduled skills-database refresh while model version and average latency stayed unchanged.
- C) Suspect a temperature setting was changed somewhere in the pipeline, since the model's confidence in its recommendations appears to have shifted.
- D) Suspect the context window available to the model shrank, reducing how much of the technician-skill data it can consider per request.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting assignment accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another, since tuning them jointly against a shared SLA and budget makes the tradeoff too complicated to reason about and risks sacrificing gains available on any single dimension considered on its own.
- B) Accuracy should always be maximized regardless of cost or latency implications, since a dispatch assistant's only real job is to be right.
- C) Optimize cost, latency, and accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.
- D) This three-way tradeoff cannot be measured with any confidence, only guessed at qualitatively.

**Question 37.** Production monitoring currently reports only an overall weekly average accuracy score.

- A) Monitoring should surface drift and outliers — a per-region or per-ticket-type breakdown — since an aggregate weekly average can hide a specific failing segment even while looking healthy overall.
- B) A single aggregate weekly average accuracy score is sufficient for production monitoring, since any real regression large enough to matter will eventually show up in that top-line number regardless of which specific region or ticket type is driving it.
- C) Monitoring should track only cost going forward, since accuracy is already fully captured by the offline evaluation suite alone.
- D) Weekly granularity is always sufficient regardless of how quickly a regression in a specific segment could otherwise be caught and addressed.

**Question 38.** The team proposes cutting human review of flagged low-confidence assignments by 80%, citing a 97% aggregate accuracy score.

- A) Segment accuracy by region and ticket type before cutting review, since the 97% aggregate figure can mask a specific segment performing far worse than the average.
- B) Proceed with the 80% cut based on the 97% aggregate accuracy figure alone, without checking whether any individual region or ticket type performs worse than that average.
- C) Aggregate accuracy is definitionally representative of every underlying region and ticket-type segment, so no further breakdown is needed before acting on it.
- D) Human review of flagged low-confidence assignments should never be reduced, regardless of what the measured accuracy figures show.

**Question 39.** An A/B test shows a new prompt version improves assignment speed, but the team has not checked whether it also changed the rate of urgent tickets misclassified as routine.

- A) Assignment-speed improvement alone is a sufficient signal to ship the new prompt version to all traffic.
- B) The urgent-versus-routine misclassification failure mode isn't something an evaluation can actually measure before a change ships.
- C) Ship the speed-improving change now and monitor for any rise in urgent-tickets-misclassified-as-routine informally after the fact, through normal production dashboards, rather than running a dedicated pre-rollout check for that specific failure mode.
- D) Check the urgent-misclassification failure mode specifically before shipping — an isolated speed improvement could be masking an increase in urgent tickets wrongly treated as routine.

**Question 40.** The team wants to diagnose why a subset of dispatch recommendations are technically correct (right technician, right time window) but rated poorly by dispatchers in feedback surveys.

- A) Assume the accuracy metric itself is broken and discard it, since a recommendation rated poorly can't also be technically correct.
- B) Increase the model's capability tier across the board, on the assumption that higher raw capability always translates into higher dispatcher satisfaction even when the underlying assignment and time window were already correct and deterministic.
- C) Ignore the dispatcher satisfaction survey scores entirely and continue relying on accuracy validation alone as the only quality signal that matters.
- D) Investigate a dimension beyond correctness — e.g., clarity of reasoning, communication tone, or practicality of the suggested window — since "correct but poorly rated" points at a quality dimension the current eval doesn't measure.

**Question 41.** The team is optimizing token usage and notices the system sends full ticket history plus a large static service-policy document on every turn of multi-turn dispatch conversations.

- A) Apply prompt caching to the static service-policy document and trim or summarize older turns of ticket history, reducing redundant token cost across a multi-turn dispatch conversation.
- B) This has no optimization opportunity at all, since sending the full ticket history and the complete policy document on every turn is always required for correctness.
- C) Switch to a smaller model tier as the only lever for reducing token cost, leaving the redundant full-history and policy-document resending unchanged.
- D) Remove the static service-policy document from the conversation entirely to save tokens, even though the model needs that policy hook to apply it correctly.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume, captured without any tagging schema or sampling strategy, is itself a sufficient observability strategy as long as every prompt and response is retained somewhere the team can search later if a specific incident needs investigation.
- B) Reduce logging volume to save storage cost, with no other change to how the logs are structured or reviewed.
- C) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.
- D) Observability requires no structure at all as long as the raw data is retained somewhere indefinitely.

**Question 43.** The team wants to identify whether a quality regression was caused by a recent prompt change, a recent model version change, or a skills-database content change — all three happened in the same week.

- A) Assume the most recently shipped change is always the cause of a regression, regardless of what the other two simultaneous changes might have affected.
- B) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.
- C) Attribution is impossible once multiple changes have shipped in the same week, so the regression's cause has to remain unknown.
- D) Revert all three changes — the prompt update, the model version bump, and the skills-database content change — simultaneously and without investigation, restoring the prior state entirely before determining which change, if any, actually caused the regression.

**Question 44.** An automated eval asserts that a scheduling-summary output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining, since a correct output shouldn't ever fail an automated check.
- B) The fixed reference string used for the exact-match check simply needs to be made longer, more detailed, and better validated against sample outputs to capture the correct scheduling summary.
- C) Temperature should be increased to fix the intermittent eval failures, since more randomness in generation should make the output converge on the reference string more often over repeated runs.
- D) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output, where the same correct scheduling summary can legitimately be phrased several different ways; the eval should check for required content and structure rather than exact text.

**Question 45.** Leadership wants a single number to represent "how good" the dispatch assistant is, to track over time.

- A) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, safety) so a healthy top-line number doesn't mask a specific failing area.
- B) A single number is always achievable and fully sufficient for any system's evaluation needs, since leadership tracking a trend line over time is the entire point of an evaluation program regardless of how many underlying dimensions or segments that single number happens to compress together.
- C) Use assignment accuracy alone as the single number leadership tracks, since it's the system's stated purpose and every other dimension is secondary.
- D) Refuse to provide any single summary metric under any circumstances, since leadership's request is inherently unreasonable.

---

## Scenario D: Governance and Team Enablement for an Insurance Claims Modernization (Questions 46–60)

An insurance carrier is deploying a Claude-powered system that processes claims intake information and assists a 25-person claims-operations team using Claude Code internally. You are responsible for governance, regulatory compliance, and developer enablement for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) This sequencing carries no meaningful risk, since compliance requirements can always be layered on right before launch without touching the application logic already built.
- B) Regulatory data-residency, retention, and access-control requirements can force structural changes that are far more costly to retrofit than to design in from the start.
- C) Compliance only affects legal documentation and contract language, not the system's actual architecture or how data flows through it.
- D) HIPAA, not state insurance regulation, is the relevant compliance regime for an insurance claims client, so the architecture team's current data-flow and retention work should be scoped against HIPAA requirements rather than state insurance rules.

**Question 47.** A team proposes requiring human approval on every single output the claims-intake system produces, framing it as the safest governance posture.

- A) Blanket human-in-the-loop review on every single output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.
- B) Maximal human review of every output is always the correct default posture for an insurance AI system, regardless of the error cost or judgment required for a given output.
- C) Human reviewers are categorically less accurate than the model at this task, which makes universal review counterproductive rather than safe.
- D) This blanket-review approach is required by GDPR regardless of any other governance consideration specific to this system.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from claimant-submitted free text, and inconsistent output — as part of its design.

- A) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.
- B) These risks only need to be addressed once they're actually observed happening in production, not designed for in advance.
- C) A single generic guardrail layer, applied uniformly at the input stage, addresses hallucination, prompt injection, and inconsistent output equally well, since all three risks ultimately trace back to the same underlying model behavior and don't require separate, failure-mode-specific mitigations.
- D) These particular risks are exclusive to non-insurance use cases and don't meaningfully apply to a claims-intake system.

**Question 49.** The claims-operations team asks whether the system's decisions could produce disparate outcomes across different claimant demographics.

- A) This is not an architectural concern at all; disparate outcomes across claimant demographics belong entirely to a legal and compliance review that should happen only after the system has already launched and produced real claim outcomes to examine.
- B) Disparate impact across demographics is impossible in an LLM-based system by construction, since the model has no access to protected demographic fields.
- C) This concern only applies to systems making the final claim-payout decision, not to an assistive system that a human still reviews before any payout happens.
- D) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population and measure for disparate impact rather than assuming it's absent.

**Question 50.** The 25-person claims-operations team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Have each of the 25 staff members individually troubleshoot their own local Claude Code configuration whenever something behaves inconsistently.
- B) Restrict Claude Code usage to a single designated engineer on the team, so configuration variance across the other 24 staff members stops mattering.
- C) Standardize the CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on each person's individual local setup.
- D) Accept the inconsistency across the team as an unavoidable cost of adopting AI-assisted tooling at all.

**Question 51.** The team wants Claude Code-generated code changes in this insurance context to go through the same review rigor as any other change to a regulated system.

- A) AI-assisted code should bypass the standard review process entirely, since code that Claude Code generated has already been produced by a system trained on well-reviewed, structured patterns and doesn't need the same human scrutiny a regulated system's other changes require.
- B) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a regulated system.
- C) Only a spot-check of a small sample of the AI-generated code is necessary before merging it into the regulated system.
- D) Review requirements should be set lower for AI-generated code than for equivalent human-written code in this same regulated system.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the Claude Code-generated logic without validating whether the surrounding integration is actually where the failure originates.
- B) Disable Claude Code for the entire team following this incident, on the theory that any tool involved in a production data-handling bug should be removed from the workflow entirely until a full retrospective can determine whether the tool itself is fundamentally unsafe for this kind of regulated data-handling work.
- C) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces and logs to localize the actual failure point.
- D) Roll back all recent Claude Code-assisted changes regardless of whether they're related to this specific data-handling incident.

**Question 53.** The claims-operations team wants a documented, repeatable workflow for a recurring task (generating a weekly claims-aging summary report) versus a one-off exploratory coding task.

- A) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an informal, uninstrumented session, since it doesn't need standing infrastructure.
- B) Build both the recurring weekly report and the one-off exploratory task as ad hoc, undocumented prompts recreated from scratch each time either is needed.
- C) Build both the recurring report and the one-off exploratory task as MCP servers, regardless of how different their actual reuse profiles are.
- D) Recurring, well-defined workflows and one-off exploratory tasks should always be built using the identical amount of structure and tooling investment.

**Question 54.** The compliance team wants documented evidence of who accessed what claimant-related data through the system and when.

- A) Access logging is optional as long as the system already has role-based permissions in place, since a permission model that correctly restricts who can reach claimant data makes a separate record of who actually accessed it redundant for compliance purposes.
- B) Audit logging can be added later, after launch, without any architectural impact on how the system is currently designed.
- C) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- D) Only failed access attempts need a structured log entry; successful, authorized access doesn't need one.

**Question 55.** The steering committee for this deployment includes claims, legal, and engineering stakeholders with different priorities and vocabularies.

- A) Tailor architectural communication to each audience — tradeoffs framed in terms claims and legal stakeholders can evaluate against their own priorities, not just engineering metrics.
- B) Communicate only with the engineering stakeholders on the steering committee, trusting them to relay the relevant tradeoffs to claims and legal in their own words.
- C) Skip stakeholder communication with claims and legal entirely until the system is fully built and ready to demo.
- D) Use identical, engineering-oriented technical documentation for all three audiences — claims, legal, and engineering — to save the effort of producing separate materials tailored to each group's own priorities and vocabulary, on the assumption that any competent stakeholder can translate technical detail into their own terms.

**Question 56.** Midway through the project, the claims team's requirements shift meaningfully based on new state insurance regulatory guidance.

- A) Refuse to incorporate the new regulatory-driven requirement change, since the original requirements were already agreed upon with the claims team earlier in the project.
- B) Incorporate the new state regulatory guidance into the design silently, without informing any stakeholder of the resulting scope, cost, or timeline impact.
- C) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.
- D) Restart the entire project from scratch, discarding all work completed so far regardless of how much of it is actually affected by the new guidance.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the claims-operations team.

- A) This is the correct lifecycle model; once the system is handed off, monitoring production signal and iterating on the design becomes entirely the claims-operations team's responsibility, with no ongoing role for the architect who designed the original system.
- B) Lifecycle responsibility for the architecture ends once the deployment contract with the claims-operations team is signed.
- C) Production monitoring is only necessary if a major incident actually occurs after handoff.
- D) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient, since the final "what" — model tier, retry settings, thresholds — is all a future team actually needs to operate the system.
- B) Documenting the reasoning behind each configuration choice is unnecessary overhead in a regulated environment already burdened with compliance paperwork.
- C) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.
- D) Only the original architect should ever be allowed to modify the system's configuration going forward, which makes writing down the reasoning behind each value moot since no one else will need to consult it.

**Question 59.** The claims-operations team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves meaningful time on every task category by default, without checking any specific task against its own review overhead.
- B) Ban Claude Code for all documentation-drafting tasks outright, without evaluating whether it actually reduces friction on that category of work.
- C) Evaluate specific task categories for genuine friction reduction (e.g., repetitive documentation drafting, codebase exploration) versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.
- D) Mandate Claude Code usage across all task categories regardless of any measured benefit or added review overhead.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no realistic architectural fix, since every engineer's debugging process is inherently individual.
- B) Document the triage process — how to distinguish integration-layer failures from model-output failures for this system — as shared operational knowledge, reducing redundant re-derivation across the team.
- C) Restrict all Claude Code integration debugging to a single designated engineer, so the rest of the team stops encountering the same failures independently.
- D) The issue can only be resolved by switching the entire team away from Claude Code to a different tool entirely, since the redundant re-derivation is inherent to this specific tool's integration model rather than to the team's lack of a shared triage reference.

---
# Answer Key

**Quick key:** 1-D, 2-B, 3-D, 4-C, 5-B, 6-A, 7-B, 8-B, 9-D, 10-B, 11-C, 12-A, 13-D, 14-B, 15-B, 16-C, 17-D, 18-D, 19-C, 20-C, 21-A, 22-C, 23-A, 24-D, 25-A, 26-B, 27-A, 28-B, 29-D, 30-A, 31-D, 32-B, 33-C, 34-D, 35-B, 36-C, 37-A, 38-A, 39-D, 40-D, 41-A, 42-C, 43-B, 44-D, 45-A, 46-B, 47-A, 48-A, 49-D, 50-C, 51-B, 52-C, 53-A, 54-C, 55-A, 56-C, 57-D, 58-C, 59-C, 60-B

---

**1. D** — The stated goal (faster resolution for existing volume) is an efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A oversells the initiative as transformation despite what discovery found; B fixates on an easier-to-measure but wrong pillar; C skips the framing needed to keep the project aligned to what discovery actually found.

**2. B** — Steps that are well-defined and always applied in the same order are the defining case for a fixed workflow. A invents autonomy that isn't present in the scenario; C treats a genuine multi-step sequence as a single augmented call; D denies that the patterns have different, non-interchangeable tradeoffs.

**3. D** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. A discards the coordinator to shave hops at the cost of that control; C only adds logging after the fact rather than preventing the loss of control; B removes the specialization that motivated separate subagents in the first place.

**4. C** — Every subagent succeeding while entire complaint categories are never routed at all is a decomposition problem at the coordinator level, not a subagent capability problem. A, B, and D all patch subagent-side behavior instead of fixing the actual routing gap.

**5. B** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. A, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. A** — Adoption sentiment surfaced repeatedly in discovery is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. B and C treat it as out of scope for the architecture; D overreacts to sentiment alone without weighing it against the technical case for automation.

**7. B** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for communicating an architectural decision to a stakeholder. A and D withhold the reasoning stakeholders need; C erases a deliberate, justified difference for false simplicity.

**8. B** — Building a feedback loop with explicit capture hooks for agent overrides and outcomes as a first-class architectural component is what lets the system improve after deployment. A, C, and D all treat that component as optional or someone else's problem.

**9. D** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and C over-engineer a simple augmentation need into heavier patterns; B is factually wrong about what Claude can do.

**10. B** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows; removing or relocating them is the fix. A and C deny this degradation; D targets the wrong lever entirely.

**11. C** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (identity verification) completes, cutting latency without sacrificing correctness. A and D misstate real constraints of the pattern; B sidesteps the sequencing question instead of answering it.

**12. A** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. B under-informs; C over-informs with the wrong kind of detail; D skips the framing the committee needs before a demo means anything.

**13. D** — A single agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, B, and C each understate or deny that real architectural tradeoff.

**14. B** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave that actual knowledge-transfer gap unaddressed.

**16. C** — Routing by task difficulty matches fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and B ignore fit-to-task; D sacrifices quality on the cases that need capability most.

**17. D** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, B, and C all misstate or break that caching opportunity by reordering or denying it matters.

**18. D** — Chunking and indexing strategy must match each data shape; one strategy tuned for a single content type degrades retrieval for the mismatched type. A and C ignore that mismatch; B discards useful structured data outright.

**19. C** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and B force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. C** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation appending are exactly the patterns that lose or fabricate mappings. A, B, and D all reintroduce the failure mode the fix is meant to prevent.

**21. A** — Presenting both figures with attribution and a likely explanation preserves real information rather than resolving a genuine discrepancy arbitrarily. B, C, and D all discard or obscure a data conflict instead of surfacing it.

**22. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A, B, and D are workarounds for a structurally solvable problem rather than fixes to the actual cause.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained in one place instead of many. B, C, and D each fail the reuse or maintainability requirement.

**24. D** — Progressive discovery via a queryable catalog resource scales with catalog growth better than loading everything into every prompt. A and B ignore the real context cost of the monolithic approach; C removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. B** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared language across features. A reintroduces duplication; C conflates two distinct mechanisms; D denies a common, workable pattern.

**27. A** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. B is the failure mode itself; C wrongly claims no architectural mitigation exists; D doesn't address correctness at all.

**28. B** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, C, and D each drop a relevant factor from the decision.

**29. D** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and C assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. A** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. B, C, and D all misstate this real, architecture-relevant constraint.

**31. D** — Accuracy, latency, cost, and safety/security should all be first-class metrics, since failing on any one of them means the system isn't actually working well even if assignment is correct. A, B, and C each drop a dimension that materially affects whether the system succeeds.

**32. B** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. A, C, and D each over-rely on or discard one method without closing the actual coverage gap.

**33. C** — Changing only the prompt version against a stable baseline is what lets an observed difference be attributed correctly to that one change. A skips testing entirely; B confounds two variables so neither can be credited; D dismisses a real risk without evidence.

**34. D** — Correctly retrieved data plus misapplied reasoning logic is a generation-side issue, calling for prompt or output-validation fixes rather than retrieval or model-tier changes. A and C misdiagnose the layer at fault; B skips diagnosis entirely.

**35. B** — A regression tied specifically to a data-refresh event, with model version and latency unchanged, points first at the retrieval/indexing layer. A, C, and D each suspect a cause that wouldn't specifically correlate with a skills-database refresh.

**36. C** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and B optimize a single dimension in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment- and outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and D accept that blind spot; C drops accuracy monitoring from observability entirely.

**38. A** — Segmenting accuracy by region and ticket type before cutting review protects against a failing segment hiding behind a healthy aggregate. B and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. D** — An isolated speed improvement could mask a worsened urgent-misclassification failure mode; checking specifically for that before shipping is the correct diagnostic step. A and C ship without adequate pre-rollout testing; B incorrectly claims the failure mode is unmeasurable.

**40. D** — "Correct but poorly rated" points at an unmeasured quality dimension (clarity, tone, practicality) rather than a broken accuracy metric. A and C discard a working, differently-scoped metric; B assumes a fix without diagnosing the actual gap.

**41. A** — Caching the static policy document and trimming or summarizing older turns directly reduces redundant token cost in multi-turn conversations. B denies an obvious lever; C is a blunt, quality-risking lever when a more targeted fix is available; D removes content the model still needs.

**42. C** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable regardless of retention or logging schema. A and D accept that dysfunction; B addresses storage cost, not the actual observability gap.

**43. B** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and D guess without evidence; C gives up on a solvable, if effortful, diagnostic problem.

**44. D** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and C misdiagnose model behavior or temperature as the cause; B doesn't address the actual mismatch between eval design and output variability.

**45. A** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. B and C oversimplify to a single lossy number; D refuses a reasonable, common stakeholder request.

**46. B** — Regulatory data-residency, retention, and access-control requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and C understate the real architectural impact; D misidentifies the applicable regulatory regime for an insurance claims client.

**47. A** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. B and C overstate the case for universal review in either direction; D misattributes the requirement to GDPR, which isn't the relevant regime here.

**48. A** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. B defers to a reactive posture; C wrongly assumes one guardrail covers distinct risk types; D is factually wrong.

**49. D** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; B and C make unsupported blanket claims.

**50. C** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. A and D leave the systemic cause unaddressed; B sacrifices the tool's benefit for the rest of the team.

**51. B** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a regulated system. A, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. C** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces and logs — applies here just as it would to any other incident. A and D skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. A** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. B under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. C** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and D each understate what compliance-grade audit evidence actually requires.

**55. A** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by claims, legal, and engineering audiences alike. B, C, and D each fail to serve at least one audience's real information need.

**56. C** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and B mishandle a real change; D disproportionately discards unaffected work.

**57. D** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, B, and C all end architectural responsibility earlier than the lifecycle model calls for.

**58. C** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and D all leave that reasoning undocumented and effectively lost.

**59. C** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and D over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 4.*
