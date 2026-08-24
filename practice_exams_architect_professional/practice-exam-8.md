# CCARP Practice Exam 8

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent Customer-Escalation Platform for a Telecom Retailer, Model Selection and Context Engineering for a Retail Merchandising Copilot, Evaluation and Monitoring of a Field-Service Dispatch Assistant, Governance and Team Enablement for an Insurance Claims Modernization) |
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

Northfield Mobile, a regional telecom retailer, is building a Claude-powered platform to handle escalated customer contacts — billing disputes, service outages, and retention saves — that its front-line chat system can't resolve. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with Northfield's operations stakeholders.

---

**Question 1.** Discovery reveals Northfield's actual goal is reducing average escalation handle time by 30% with the same headcount, not adding capabilities the current process lacks.

- A) Frame the architecture around transformation, arguing that even a handle-time reduction ultimately expands what the escalation team can capably do without adding staff.
- B) Frame the architecture around cost reduction exclusively, treating headcount neutrality as the only pillar worth naming even though discovery centered on handle time.
- C) Skip framing around any specific value pillar, since a working system speaks for itself regardless of what discovery uncovered.
- D) Frame the architecture around efficiency, and build success metrics around handle time per agent rather than novel capability.

**Question 2.** Escalation intake, categorization, and routing to the correct back-office queue follow a fixed, well-established sequence of steps that doesn't vary case to case, regardless of dispute type.

- A) An agentic pattern, since routing benefits from autonomous judgment even when the categorization rules never actually change from case to case.
- B) A fixed workflow, since the steps are well-defined and don't depend on intermediate findings.
- C) An augmented LLM pattern, since a single enhanced call plus retrieval is sufficient for any escalation workflow regardless of how many downstream queues exist.
- D) Whichever pattern the team can implement fastest this sprint, since all three patterns produce equivalent reliability once deployed.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (billing-dispute analysis, outage diagnostics, retention-offer calculation, resolution drafting).

- A) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow.
- B) Let each subagent pass results directly to whichever subagent needs them next, cutting the coordinator out of the loop to minimize hops between billing, outage, retention, and drafting.
- C) Merge all four responsibilities into a single subagent so there's no coordination overhead or handoff logic left to maintain.
- D) Let subagents communicate directly with each other but log the traffic afterward so the coordinator can review what happened.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition assigned only billing and outage cases to the pipeline — retention escalations and legal-threat complaints are never routed to any subagent and silently fall through.

- A) Add a fifth subagent dedicated to edge cases like retention and legal-threat complaints, without changing how the coordinator decides what gets routed anywhere.
- B) Add a prompt instruction telling each subagent to flag cases it doesn't recognize as its own, relying on subagents to catch a routing gap they were never sent.
- C) Give the billing and outage subagents broader tool access so they can absorb retention and legal-threat cases alongside their existing work, stretching them well beyond their original scope.
- D) Fix the coordinator's decomposition so it explicitly covers all escalation categories, including retention and legal-threat cases, rather than tuning the existing subagents.

**Question 5.** The design must align technical architecture to a specific business value pillar Northfield actually cares about, distinct from a generic "we added AI" narrative.

- A) Efficiency, transformation, productivity, cost, and performance SLAs are examples of such pillars; the chosen one should drive both the architecture and its success metrics.
- B) Any AI system inherently demonstrates transformation the moment it's deployed, so no further framing exercise is needed before or after launch.
- C) Business value pillars are a sales and marketing concern that belongs in the pitch deck, not something the architecture itself needs to reflect.
- D) The pillar should be chosen after the system ships, based on whichever benefit turns out easiest to measure in hindsight.

**Question 6.** Northfield's frontline escalation agents fear the new system will be used to justify layoffs, and raise this repeatedly during discovery interviews.

- A) Treat it as a real implicit constraint alongside the explicit technical requirements — it will shape adoption, rollout sequencing, and where human-in-the-loop checkpoints matter most.
- B) Ignore the sentiment in the architecture since headcount concerns aren't a technical requirement, and let HR address it separately if it persists.
- C) Proceed with the technical design as scoped and let change management handle morale separately, treating rollout sequencing and human-in-the-loop checkpoints as questions with no architectural input at all.
- D) Recommend against the project entirely, since staff sentiment alone is reason enough to halt a technically sound design.

**Question 7.** A stakeholder asks why the retention-offer subagent uses a higher-capability, higher-cost model tier than the categorization subagent.

- A) "Higher tier because it's more important" is a sufficient answer for a stakeholder asking about cost and latency tradeoffs in a retention workflow.
- B) Avoid explaining the tier difference in detail, since stakeholders outside engineering don't need to understand model selection reasoning.
- C) Explain the tradeoff explicitly: retention offers require deeper reasoning about financial exposure that justifies the increase in cost and latency, while categorization is simpler and better served by a faster, cheaper tier.
- D) Use the same tier everywhere for simplicity, since matching tier to task difficulty adds architectural complexity without a clear payoff.

**Question 8.** The architecture's current design produces a final retention-offer recommendation with no mechanism to learn whether the customer accepted the offer or churned anyway.

- A) This is acceptable since the initial design already reflects best practice, and outcome data can be bolted on later if leadership eventually asks for it.
- B) Feedback loops are a data science concern that lives downstream of the architecture, not something the system design itself needs to account for.
- C) Defer any feedback mechanism to a hypothetical future phase, keeping the current architecture free of hooks for capturing acceptance or churn outcomes.
- D) Add a feedback loop capturing offer acceptance and churn outcomes as a first-class architectural component, so the system can improve post-deployment.

**Question 9.** Northfield wants a single enhanced LLM call — with retrieval of current plan details — to answer straightforward "what's my current plan" questions, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture with a coordinator and specialized subagents, without first validating that a single retrieval-augmented call couldn't handle a plan-lookup this simple.
- B) This cannot be built with Claude at all, since answering "what's my current plan" requires an agentic loop rather than a single retrieval-augmented call.
- C) An augmented LLM pattern (a single call enhanced with retrieval/tools) fits this simpler augmentation need without the overhead of agentic orchestration.
- D) This requires a fixed workflow with at least five sequential steps producing structured intermediate outputs, even though the task is a single lookup with no branching logic.

**Question 10.** The billing-dispute subagent's toolset has grown to include tools for scheduling technician truck rolls and adjusting loyalty-tier status, unrelated to billing disputes.

- A) This has no architectural downside as long as the subagent's system prompt clearly explains when to use each tool, regardless of how many unrelated tools it holds.
- B) More tools always improve a subagent's flexibility and should be encouraged, since a larger toolset only ever expands what a subagent can resolve on its own.
- C) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or moved to a more appropriate subagent.
- D) The fix is to increase the subagent's context window so it has more room to reason about which of its many tools to select for a given case.

**Question 11.** The coordinator currently processes each escalation sequentially through categorization, outage diagnostics, retention-offer calculation, and resolution drafting, even though outage diagnostics and retention-offer calculation have no dependency on each other's output.

- A) Sequential processing is required for auditability, since running outage diagnostics and retention-offer calculation in parallel would make the audit trail harder to reconstruct.
- B) Run outage diagnostics and retention-offer calculation as independent, parallel subagent calls once categorization completes, rather than sequentially.
- C) Parallelization is not possible within a coordinator/subagent architecture once a fixed processing order has already been established.
- D) Combine outage diagnostics and retention-offer calculation into a single subagent so the sequencing question never has to be answered.

**Question 12.** Northfield's steering committee, unfamiliar with technical details, asks how the end-to-end architecture should be described at a high level.

- A) Present only the model names and token costs involved, trusting the committee to infer the business impact from the technical stack alone.
- B) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, without requiring them to understand implementation internals.
- C) Present the full technical architecture diagram with no simplification, since a steering committee should see exactly what engineering sees.
- D) Skip a high-level description and go directly into an implementation demo, letting the running system speak for the architecture instead of walking the committee through input, processing, and output first.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (billing, outage diagnostics, retention, drafting) rather than a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows, since one agent holding every tool avoids the coordination overhead a coordinator/subagent split introduces.
- B) Specialized subagents are strictly a cost-increasing choice with no reliability benefit over a single agent holding the same total toolset.
- C) There's no meaningful architectural difference between the two approaches once both are given access to the same underlying tools.
- D) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.

**Question 14.** The escalation platform must eventually support a new category (5G home-internet escalations) Northfield plans to launch next year, but detailed requirements aren't available yet.

- A) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.
- B) Ignore future categories until requirements exist, treating extensibility as something to retrofit entirely once 5G home-internet requirements are finalized.
- C) Build full support for 5G home-internet escalations now, guessing at the required subagents and tools ahead of any confirmed requirements.
- D) Refuse to proceed with the current phase until Northfield finalizes the 5G home-internet requirements, blocking delivery on the escalation platform entirely over an undefined future scope.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, since a well-organized implementation is self-explanatory to any engineer who reads the code closely enough.
- B) Rely on the original architect remaining available indefinitely to answer questions, instead of writing down the reasoning behind key decisions.
- C) Document the architecture and the reasoning ("why") behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final "what."
- D) Documentation is unnecessary if the code is well-organized, since a new engineering team can reconstruct intent from the structure alone.

---

## Scenario B: Model Selection and Context Engineering for a Retail Merchandising Copilot (Questions 16–30)

Meridian Home Goods wants Claude to help merchandising planners answer questions ranging from simple SKU price lookups to complex, multi-region assortment tradeoff analysis, using retrieval over vendor contracts, sales reports, and inventory data. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Planner questions range from simple SKU lookups to complex multi-region assortment tradeoff analysis requiring deep reasoning.

- A) Always use the highest-capability tier for every query regardless of complexity, since consistency across tiers matters more than matching cost to task difficulty for a simple SKU lookup versus a multi-region tradeoff question.
- B) Route based on task difficulty — a fast tier for simple SKU lookups, a balanced tier for typical planning questions, and a higher-capability tier reserved for complex multi-region tradeoff analysis.
- C) Use one fixed mid-tier model for all queries regardless of complexity, treating tier selection as a one-time decision rather than a per-query one.
- D) Always use the fastest/cheapest tier to minimize cost, accepting quality loss on complex multi-region tradeoff analysis as an acceptable tradeoff.

**Question 17.** Every request sends the same long system prompt (merchandising rules, tone, formatting) followed by retrieved sales-data excerpts that vary per query.

- A) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it, to reduce both latency and cost across the high query volume.
- B) Alternate system instructions and retrieved content throughout the prompt, interleaving stable rules with per-query sales-data excerpts as they become relevant.
- C) Put the retrieved sales-data excerpts first since they're most relevant to the specific query, placing the stable merchandising rules and tone instructions afterward.
- D) Order doesn't affect cost or latency for this use case, since the total token count sent to the model is what determines both, not the sequence of content.

**Question 18.** The corpus mixes long-form vendor contracts with short structured SKU/price tables.

- A) One chunking and indexing strategy tuned for long-form vendor contracts can serve short structured SKU/price tables equally well, since chunk size mainly affects retrieval speed rather than which records get returned.
- B) Structured SKU/price data should be excluded from retrieval entirely, leaving planners to look up exact prices outside the merchandising copilot.
- C) Use the largest possible chunk size for everything, including short structured tables, to avoid needing more than one indexing strategy.
- D) Chunking and indexing strategy should match each data shape — long-form documents need different chunking than short structured records, or retrieval quality degrades for whichever type doesn't match.

**Question 19.** Planner queries range from exact lookups ("current price for SKU 48213") to conceptual questions ("how has our outdoor-furniture assortment mix shifted over two years").

- A) Use only embedding similarity search for every query type, including exact SKU lookups where a metadata filter would return the precise record directly.
- B) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.
- C) Use only structured/metadata filtering for every query type, including conceptual questions like assortment-mix shifts that have no exact field to filter on.
- D) Query pattern doesn't affect which retrieval approach is appropriate, since both exact lookups and conceptual questions can be answered adequately by either mechanism once enough documents are indexed.

**Question 20.** Planners need each pricing recommendation reliably mapped to its specific source (vendor contract clause, sales report section), and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without further structure, trusting the instruction alone to keep each claim paired with its source through synthesis.
- B) Add citations after the fact by searching for a plausible source for each claim once the response has already been drafted and the mapping has been lost.
- C) Append a general bibliography of consulted documents at the end of each response, without pairing any individual claim to a specific source.
- D) Require structured output pairing each claim with its source (document, section, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.

**Question 21.** Two systems disagree on the current on-hand inventory count for a SKU by a meaningful margin — likely due to a stale nightly sync in one of them.

- A) Average the two on-hand inventory figures and present the average as the current count, treating a midpoint as a reasonable resolution even though a stale nightly sync likely explains the gap.
- B) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely explanation (e.g., a stale sync), rather than silently picking one.
- C) Always prefer whichever source was retrieved first, treating retrieval order as a reasonable tiebreaker between two disagreeing inventory systems.
- D) Omit the inventory figure entirely since the sources disagree, leaving the planner with no number rather than an annotated discrepancy.

**Question 22.** A prompt asking the model to "always output valid structured JSON with source fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the "always output valid structured JSON" instruction more emphatically in the prompt, hoping stronger prose wording eliminates the occasional preamble.
- B) Increase max_tokens to leave room for both the conversational preamble and the JSON, treating leftover token budget as the fix instead of validating output against a schema.
- C) Post-process every response to strip leading text before the first `{`, patching the symptom each time rather than constraining the output format itself.
- D) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.

**Question 23.** The platform needs to connect to a proprietary vendor-catalog system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just the merchandising copilot.

- A) Build an MCP server exposing the vendor-catalog operations as tools/resources, reusable across the multiple internal tools that need it.
- B) Hard-code the vendor-catalog integration into this copilot's application code only, leaving other internal Claude-powered tools to build their own path to it.
- C) Paste the entire vendor catalog into every prompt across every consuming tool, regardless of how large the catalog grows over time.
- D) Require each consuming tool to reimplement its own vendor-catalog integration independently, duplicating the same connection logic across teams.

**Question 24.** The team is deciding between exposing the full vendor catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Progressive discovery (querying a catalog resource as needed) scales better than loading the entire catalog into context up front, especially as the catalog grows.
- B) Loading the full vendor catalog into context up front is always preferable for completeness, even as the catalog grows well beyond what a single query needs and crowds out room for the answer itself.
- C) There's no meaningful difference in context cost between querying a catalog resource on demand and loading the entire catalog into every prompt.
- D) The catalog should never be exposed to the agent in any form, leaving catalog lookups to a separate, non-agentic system entirely.

**Question 25.** A planner asks a question requiring the model to reason step by step across several sales reports before concluding on an assortment recommendation.

- A) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-document synthesis question.
- B) Zero-shot prompting with no reasoning guidance is always equally effective as chain-of-thought for questions that require synthesizing several sales reports.
- C) Chain-of-thought prompting is only useful for coding tasks, not for reasoning across multiple sales reports toward an assortment recommendation.
- D) The model cannot reason across multiple documents regardless of prompting approach, making this class of assortment question out of scope entirely.

**Question 26.** The platform wants to standardize prompt fragments (formatting rules, disclaimer language, tone) across several different planner-facing features so changes propagate consistently.

- A) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).
- B) Duplicate the formatting, disclaimer, and tone fragments into each feature's system prompt independently, updating every copy by hand whenever the wording changes.
- C) Modular prompts are the same thing as prompt caching, so enabling caching on the existing prompts already achieves the standardization the team wants for structured formatting rules and disclaimer language alike.
- D) Standardization of formatting and tone across features isn't achievable through prompt design and instead requires a separate governance policy.

**Question 27.** The system occasionally returns confident, well-formatted answers that, on manual review, misstate a specific figure from the correctly retrieved source document.

- A) Trust the fluent, well-formatted output as evidence of correctness, since a response that reads confidently and cites the right document is unlikely to misstate a retrieved figure.
- B) Apply defensive validation — verify extracted figures against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- C) Increase output length so there's more room for the model to restate the figure correctly somewhere within a longer response.
- D) This is not something an architecture can address; it's purely a model limitation with no mitigation available at the system level.

**Question 28.** The team debates whether planner-facing latency SLAs should factor into model tier selection for the copilot.

- A) Latency should never factor into model or architecture decisions, since accuracy is the only dimension a planner-facing copilot needs to optimize for.
- B) Only cost should factor into tier selection, never latency, since planners are assumed to tolerate any response time as long as the answer is cheap to produce.
- C) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, independent of temperature settings, rather than defaulting to the most capable tier regardless of SLA.
- D) SLAs are a stakeholder-communication concern with no bearing on technical architecture, so tier selection should proceed independent of what was promised.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to "latest" automatically in production, assuming model behavior is deterministic across releases and a newer version with improved benchmark scores needs no retesting on this platform's own tasks.
- B) Never upgrade models once the initial version is chosen, treating the first deployed version as permanent regardless of what later benchmark improvements show.
- C) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.
- D) Upgrade immediately without testing, since benchmark improvements on standard evaluation sets guarantee a corresponding improvement on this platform's specific workload.

**Question 30.** The copilot's context budget is a concern because both the system prompt/formatting rules and the retrieved excerpts must fit alongside room for a detailed answer.

- A) Input and output token budgets are entirely independent of each other, so the retrieved-content volume the copilot pulls in can grow indefinitely without affecting how much room remains for the answer.
- B) This tradeoff only matters for very long vendor contracts, never for typical SKU-lookup or planning queries with modest retrieved content.
- C) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.
- D) Output length has no practical limit regardless of how much retrieved content and system-prompt text precedes it in the context window.

---

## Scenario C: Evaluation and Monitoring of a Field-Service Dispatch Assistant (Questions 31–45)

Cascade Utilities uses a Claude-powered assistant to triage and assign field technicians to service jobs based on urgency, required skills, and location. It's been in production for six months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only technician-assignment accuracy and hasn't defined targets for latency, cost, or safety.

- A) Accuracy alone is sufficient since it's the system's primary purpose, and a technician-assignment engine that's slow, costly, or occasionally unsafe is still doing its core job well enough to matter.
- B) Latency and cost are operations concerns that live outside evaluation design, tracked by infrastructure dashboards rather than the eval suite itself.
- C) Safety metrics are only relevant for regulated industries, not a utility dispatch assistant that's merely routing technicians to jobs.
- D) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics — a system that assigns technicians well but is too slow, too expensive, or unsafe still fails overall.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past dispatch decisions.

- A) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for safety-relevant paths — since no single method covers every failure mode.
- B) A single automated method against a fixed labeled set is sufficient for any production system, regardless of how nuanced or safety-relevant its edge cases are.
- C) Replace the automated accuracy checks entirely with only human review, dropping the scale automated evaluation provides across the full dispatch volume.
- D) Expand the labeled set of past dispatch decisions indefinitely as the sole improvement lever, without introducing human review or adversarial testing.

**Question 33.** The team wants to test whether a new prioritization-scoring prompt improves dispatch quality before rolling it out to all technicians.

- A) Roll out the new prioritization-scoring prompt to all traffic immediately and monitor for problems afterward, rather than testing against a stable baseline first.
- B) Change the prompt and the model tier simultaneously, assuming deterministic output would make it easy to tell which change actually helped.
- C) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.
- D) Skip testing since prompt changes to a prioritization-scoring workflow are low-risk by nature and unlikely to affect dispatch outcomes.

**Question 34.** A dispatch recommendation assigns the wrong-skilled technician. Investigation shows the skill-matrix lookup was correct and retrieved properly, and the model's job-summary paraphrase mischaracterized the required skill.

- A) This is a retrieval problem; fix the indexing pipeline even though the skill-matrix lookup was confirmed to be correct and retrieved properly.
- B) This cannot be diagnosed without retraining the model, since a mischaracterized required skill in a job-summary paraphrase reflects a deeper capability gap.
- C) This is a model mismatch requiring a different, higher-capability model tier, regardless of the specific failure being a straightforward paraphrase error rather than a genuine reasoning gap in the underlying task.
- D) This is best characterized as a prompt/generation issue (inaccurate paraphrasing of correctly retrieved content), which calls for prompt or output-validation fixes rather than retrieval changes.

**Question 35.** Immediately after a scheduled technician-roster and skill-matrix refresh, the assistant starts making poor assignments, while model version and average latency are unchanged.

- A) Investigate the retrieval/indexing layer first, since the regression is tied specifically to the data refresh event with model version and average latency unchanged.
- B) Suspect the model was silently updated by the provider, even though the regression coincides precisely with the scheduled roster and skill-matrix refresh rather than any provider-side release window.
- C) Suspect a temperature setting change, since the assistant's confidence in its assignments appears to have shifted right after the refresh.
- D) Suspect the context window shrank, unrelated to any schema change in the refreshed roster and skill-matrix data.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another, since improving one dimension shouldn't be constrained by the others.
- B) Accuracy should always be maximized regardless of cost or latency implications, since a dispatch assistant's core value is getting assignments right.
- C) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.
- D) This tradeoff cannot be measured, only guessed at, since cost, latency, and accuracy interact in ways too complex to quantify against an SLA.

**Question 37.** Production monitoring currently reports only an overall weekly average assignment-accuracy score.

- A) Monitoring should surface drift and outliers — a per-region or per-job-type breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.
- B) A single aggregate weekly average is sufficient for production monitoring, since per-region and per-job-type breakdowns mainly add dashboard complexity without surfacing any signal an aggregate doesn't already carry.
- C) Monitoring should track only cost, since assignment accuracy is already fully captured by the offline eval suite rather than needing production monitoring.
- D) Weekly granularity is always sufficient regardless of system behavior, since dispatch quality issues don't tend to emerge and resolve faster than a week.

**Question 38.** The team proposes cutting human review of flagged low-confidence dispatch decisions by 75%, citing a 96% aggregate accuracy score.

- A) Proceed with the cut based on the 96% aggregate accuracy figure alone, treating it as representative of every region and job type without further breakdown.
- B) Aggregate accuracy is definitionally representative of every segment, so a 96% overall score rules out any single region or job type performing meaningfully worse.
- C) Human review of flagged low-confidence decisions should never be reduced regardless of measured accuracy, even once segment-level performance has been confirmed.
- D) Segment accuracy by region and job type before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.

**Question 39.** An A/B test shows a new prioritization prompt improves on-time-arrival rate, but the team hasn't checked whether it increased mis-escalations of complex, safety-critical jobs that should route to senior technicians.

- A) On-time-arrival rate alone is a sufficient signal to ship the change, since it's the metric the prioritization-scoring prompt was specifically designed to improve.
- B) Check the escalation-related failure mode specifically before shipping — an isolated on-time improvement could be masking an increase in inappropriate routing of complex, safety-critical jobs.
- C) False-positive escalation behavior is not something evaluation can measure ahead of rollout even with a structured eval harness in place, so shipping decisions should rest on on-time-arrival rate and other quantifiable signals already in the A/B report.
- D) Ship the change and monitor mis-escalation informally after the fact, rather than testing for it as part of the A/B comparison before rollout.

**Question 40.** A subset of dispatch assignments are technically correct (right skill match) but rated poorly by technicians in satisfaction surveys, often citing unreasonable travel distance.

- A) Assume the accuracy metric is broken and discard it, even though it relies on a structured skill-match comparison that hasn't actually failed here.
- B) Increase the model's capability tier on the assumption — never validated against survey data — that higher capability always improves technician satisfaction.
- C) Investigate a dimension beyond skill-match correctness — e.g., travel burden or workload balance — since "accurate but poorly rated" points at a quality dimension the current eval doesn't measure.
- D) Ignore technician satisfaction scores in favor of the accuracy metric alone, treating skill-match correctness as the complete definition of assignment quality.

**Question 41.** The team is optimizing token usage and notices the system sends full technician-roster history plus a large static skill-matrix reference document on every dispatch decision.

- A) Apply prompt caching to the static skill-matrix document and consider trimming or summarizing older roster history to reduce redundant token cost.
- B) Switch to a smaller, cheaper model as the only lever for reducing token cost, leaving the full roster history and skill-matrix document unchanged on every call.
- C) Remove the skill-matrix reference document entirely to save tokens, even though dispatch decisions depend on it for matching technician skills to jobs.
- D) This has no optimization opportunity since full roster history and the static skill-matrix document are always required in full on every dispatch decision, without validating whether older history could be trimmed instead.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy, since every prompt and response is captured and available for review, without ever validating whether failure patterns are actually visible in it.
- B) Reduce logging volume to save storage cost, with no other change to how failure patterns are surfaced from whatever logs remain.
- C) Observability requires no structure as long as the data is retained somewhere, since retention alone satisfies the goal of being able to review production behavior when a pattern eventually surfaces.
- D) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.

**Question 43.** The team wants to identify whether a quality regression was caused by a recent prompt change, a recent model version change, or a roster-data schema change — all three shipped in the same week.

- A) Assume the most recent of the three shipped changes is always the cause, without isolating the prompt, model, and roster-schema changes individually.
- B) Attribution is impossible once multiple changes have shipped in the same week, so the regression's cause should be treated as permanently unknown.
- C) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.
- D) Revert all three changes without investigation, regardless of which (if any) of the prompt, model, or schema change actually caused the regression.

**Question 44.** An automated eval asserts that a dispatch-summary output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining, since it should be able to reproduce the exact reference string for the dispatch summary every time.
- B) The reference string needs to be longer, so there's a larger surface for the model's output to match against, rather than validating for required content instead of exact text.
- C) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.
- D) Temperature should be increased to fix the intermittent exact-match failures, giving the model more room to vary its phrasing around the fixed reference string.

**Question 45.** Leadership wants a single number to represent "how good" the dispatch assistant is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs, including one spanning accuracy, latency, cost, and safety dimensions.
- B) Use on-time-arrival rate alone as the single number, since it's the system's stated purpose and the metric leadership is most familiar with.
- C) Refuse to provide any single summary metric under any circumstances, even when leadership specifically wants one top-line indicator to track over time.
- D) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, safety) so a healthy top-line number doesn't mask a specific failing area.

---

## Scenario D: Governance and Team Enablement for an Insurance Claims Modernization (Questions 46–60)

Harborline Insurance is deploying a Claude-powered system that assists claims adjusters with intake, coverage lookup, and payout recommendations, alongside a 25-person claims-engineering team using Claude Code internally to build and maintain it. You are responsible for governance, regulatory compliance, and developer enablement for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) State insurance-regulation requirements around data residency, retention, and access control can force structural changes that are far more costly to retrofit than to design in from the start.
- B) This sequencing carries no risk since compliance requirements can always be added right before launch without touching core application logic.
- C) Compliance only affects legal documentation, not system architecture, so finalizing data flow and access-logging design in the final week is fine.
- D) HIPAA, not state insurance regulation, is the relevant regime for this claims system, so finalizing data residency, retention, and access-logging design in the final week carries no compliance risk.

**Question 47.** A team proposes requiring human approval on every single claims-adjudication output, framing it as the safest governance posture.

- A) Maximal human review on every claims-adjudication output is always the correct default for regulated AI systems, regardless of the decision's actual error cost or how much judgment it genuinely requires.
- B) Human reviewers are categorically less accurate than the model, making universal review of every claims-adjudication output counterproductive.
- C) Requiring human approval on every single output is required by GDPR regardless of other considerations specific to this claims workflow.
- D) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from claimant-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed once hallucination, prompt injection, or inconsistent output are actually observed in production, not designed for up front.
- B) Hallucination, prompt injection, and inconsistent output are risks exclusive to non-insurance use cases and don't meaningfully apply to a claims-adjudication system.
- C) A single generic guardrail addresses hallucination, prompt injection, and inconsistent output equally well, without needing failure-mode-specific mitigations.
- D) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.

**Question 49.** The claims team asks whether the system's payout recommendations could produce disparate outcomes across different policyholder demographics.

- A) This is not an architectural concern; disparate outcomes across policyholder demographics belong entirely to legal/compliance review after the payout-recommendation system has already launched.
- B) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population and measure for disparate impact rather than assuming it's absent.
- C) Disparate impact across policyholder demographics is impossible in an LLM-based payout-recommendation system by construction, regardless of the underlying data.
- D) This concern only applies to systems making final payout decisions, not to an assistive system whose recommendations still influence adjuster outcomes.

**Question 50.** The 25-person claims-engineering team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Have each of the 25 engineers individually troubleshoot their own local Claude Code configuration and MCP server access as issues come up.
- B) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.
- C) Restrict Claude Code usage to a single designated engineer to reduce the variance caused by inconsistent local configuration across the 25-person team.
- D) Accept the configuration inconsistency as an unavoidable cost of adopting Claude Code across a 25-person claims-engineering team.

**Question 51.** The team wants Claude Code-generated code changes in this regulated claims system to go through the same review rigor as any other change.

- A) AI-assisted code should bypass standard code review since Claude Code, not a human, wrote the initial version of the claims-data-handling change.
- B) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a regulated system.
- C) Only a spot-check of AI-generated code is necessary in a regulated claims system, since Claude Code output is generally more consistent than human-written code.
- D) Review requirements should be set lower for AI-generated code than for human-written code, given how much of the claims system Claude Code now touches.

**Question 52.** A production incident traces back to a Claude Code-generated claims-data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the Claude Code-generated code itself without investigating whether the surrounding integration layer mishandled the change instead.
- B) Disable Claude Code for the claims-engineering team entirely following this incident, rather than isolating whether the failure was in the generated code or the surrounding integration layer.
- C) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.
- D) Roll back all recent Claude Code-assisted changes regardless of relevance, rather than tracing the specific claims-data-handling change involved.

**Question 53.** The claims-ops team wants a documented, repeatable workflow for a recurring task (generating a weekly reserve-adequacy summary report) versus a one-off exploratory investigation task.

- A) Build both the weekly reserve-adequacy report and the one-off exploratory task as ad hoc, undocumented prompts recreated from scratch each time they're needed.
- B) Build both the recurring report and the one-off investigation as MCP servers, regardless of whether either actually gets reused often enough to justify it.
- C) Recurring workflows and one-off tasks should be built identically, since a repeatable weekly reserve-adequacy report and a single exploratory investigation ultimately have the same reuse profile.
- D) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session, since it doesn't need standing infrastructure.

**Question 54.** The compliance team wants documented evidence of who accessed what claimant data through the system and when.

- A) Access logging is optional if the system already has role-based permissions, since permission checks alone satisfy compliance's request for documented access evidence.
- B) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- C) Audit logging of claimant-data access can be added later without architectural impact, once the core claims-adjudication system is already in production.
- D) Only failed access attempts need to be logged, since successful, authorized access to claimant data doesn't require documentation for compliance purposes.

**Question 55.** The steering committee for this deployment includes claims-ops, legal/compliance, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders on this steering committee, trusting them to relay the relevant tradeoffs to claims-ops and legal/compliance in whatever terms make sense to each.
- B) Tailor architectural communication to each audience — tradeoffs framed in terms claims-ops and legal stakeholders can evaluate against their own priorities, not just engineering metrics.
- C) Use identical technical documentation for claims-ops, legal/compliance, and engineering stakeholders alike, to save the effort of producing separate materials.
- D) Skip stakeholder communication with claims-ops and legal until the system is fully built and ready for a single end-to-end demonstration.

**Question 56.** Midway through the project, claims-handling requirements shift meaningfully based on new state insurance-regulation guidance.

- A) Refuse to incorporate the new state insurance-regulation guidance since claims-handling requirements were already agreed upon earlier in the project.
- B) Incorporate the regulation-driven change silently without informing claims-ops, legal, or engineering stakeholders of the resulting timeline or design impact, since the guidance itself is non-negotiable.
- C) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.
- D) Restart the entire claims-modernization project from scratch, regardless of how much of the existing design the new guidance actually affects.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the claims-operations team.

- A) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.
- B) This is the correct lifecycle model; monitoring and iteration on the deployed claims system are entirely the operations team's responsibility after handoff.
- C) Lifecycle responsibility ends once the contract with Harborline is signed, without validating whether the deployed system still meets its original design goals after handoff.
- D) Monitoring is only necessary if a major incident occurs, so no ongoing architectural involvement is needed absent a specific triggering event.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) Listing final configuration values (model tier, retry settings, thresholds) is sufficient documentation, since the "what" is all a future team needs to extend the system.
- B) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.
- C) Documenting the reasoning behind configuration choices is unnecessary overhead in a regulated environment already covered by compliance sign-off.
- D) Only the original architect should ever be allowed to modify the system, making documentation of configuration reasoning largely moot.

**Question 59.** The claims-ops team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume Claude Code always saves meaningful time on every routine task category by default — documentation drafting, codebase exploration, and everything in between — without checking where review overhead might exceed the time saved.
- B) Ban Claude Code for all documentation tasks without evaluation, on the assumption that drafting documentation never benefits from AI assistance.
- C) Evaluate specific task categories for genuine friction reduction (e.g., repetitive documentation drafting, codebase exploration) versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.
- D) Mandate Claude Code usage for all routine claims-ops tasks regardless of whether the time saved outweighs the added review overhead in each category.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no architectural fix, since each engineer re-deriving the triage process independently doesn't affect delivery speed.
- B) Document the triage process (how to distinguish integration-layer failures from model-output failures for this system) as shared operational knowledge, reducing redundant re-derivation across the team.
- C) Restrict debugging of Claude Code integration failures to a single designated engineer, rather than documenting the triage process for the wider team.
- D) The issue can only be resolved by switching away from Claude Code to a different tool entirely, rather than documenting the existing triage process.

---
# Answer Key

**Quick key:** 1-D, 2-B, 3-A, 4-D, 5-A, 6-A, 7-C, 8-D, 9-C, 10-C, 11-B, 12-B, 13-D, 14-A, 15-C, 16-B, 17-A, 18-D, 19-B, 20-D, 21-B, 22-D, 23-A, 24-A, 25-A, 26-A, 27-B, 28-C, 29-C, 30-C, 31-D, 32-A, 33-C, 34-D, 35-A, 36-C, 37-A, 38-D, 39-B, 40-C, 41-A, 42-D, 43-C, 44-C, 45-D, 46-A, 47-D, 48-D, 49-B, 50-B, 51-B, 52-C, 53-D, 54-B, 55-B, 56-C, 57-A, 58-B, 59-C, 60-B

---

**1. D** — The stated goal (less handle time, same headcount) is an efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A, B, and C either misname the pillar or skip the framing that keeps the project aligned to what discovery actually found.

**2. B** — Steps that are well-defined and don't vary case to case are the defining case for a fixed workflow, not autonomous orchestration. A overstates the need for agentic autonomy; C undersells what a genuinely multi-step, standardized process needs; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. A** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. B and D sacrifice these properties for a shortcut; C discards the specialization that motivated separate subagents in the first place.

**4. D** — Every subagent succeeding while whole escalation categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, B, and C all patch downstream instead of fixing the actual scope gap.

**5. A** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. B, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. A** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. B and C treat it as out of scope; D overreacts to sentiment alone without weighing it against the technical case.

**7. C** — Explaining the specific tradeoff (deeper reasoning need vs. increased cost/latency) is the standard for stakeholder communication about architectural decisions. A and B withhold the reasoning stakeholders need; D removes a deliberate, justified difference for false simplicity.

**8. D** — Adding a feedback loop that captures offer acceptance and churn outcomes as a first-class architectural component is what lets the system improve after deployment. A, B, and C all treat a first-class architectural component as optional or someone else's problem.

**9. C** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and D over-engineer a simple augmentation need; B is factually wrong.

**10. C** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just writing around it. A and B ignore this real degradation; D doesn't address selection reliability at all.

**11. B** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (categorization) completes, reducing latency without sacrificing correctness. A and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. B** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; C is too much of the wrong kind of detail; D skips the communication need entirely.

**13. D** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, B, and C understate or deny this real architectural tradeoff.

**14. A** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. B ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. C** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, B, and D all leave the actual knowledge transfer gap unaddressed.

**16. B** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and D ignore or sacrifice fit-to-task; C forces one tier onto queries with very different needs.

**17. A** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. B, C, and D all misstate or break the caching opportunity.

**18. D** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and C ignore this mismatch; B discards useful structured data.

**19. B** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and C force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. D** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, B, and C all reintroduce the failure mode the fix is meant to prevent.

**21. B** — Presenting both figures with attribution and a likely explanation preserves the actual information for the planner rather than resolving a real discrepancy arbitrarily. A, C, and D all discard or obscure a genuine data conflict.

**22. D** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and C are workarounds for a structurally solvable problem; B doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. B, C, and D all fail the reuse or maintainability requirement.

**24. A** — Progressive discovery via a queryable catalog resource scales with catalog growth better than loading the entire catalog into every prompt. B and C ignore the real context cost of the monolithic approach; D removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. A** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. B reintroduces duplication; C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. B** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; C doesn't address correctness; D incorrectly claims no architectural mitigation exists.

**28. C** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, B, and D each drop a relevant factor from the decision.

**29. C** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and D assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. C** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and D all misstate this real, architecture-relevant constraint.

**31. D** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if it assigns technicians well. A, B, and C each drop a dimension that materially affects whether the system is actually working well.

**32. A** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. B, C, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. C** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; D dismisses a real risk without evidence.

**34. D** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. A and C misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. A** — A regression tied specifically to a data refresh event, with model and latency unchanged, points first at retrieval/indexing. B, C, and D would not specifically correlate with a roster/skill-matrix refresh.

**36. C** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and B optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and D accept a monitoring blind spot; C drops accuracy monitoring from observability entirely.

**38. D** — Segmenting accuracy by region and job type before cutting review protects against a failing segment hiding behind a healthy aggregate. A and B trust the aggregate uncritically; C over-corrects by refusing any reduction regardless of evidence.

**39. B** — An isolated on-time-arrival improvement could mask a worsened escalation failure mode; checking specifically for that before shipping is the correct diagnostic step. A and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. C** — "Accurate but poorly rated" points at an unmeasured quality dimension (travel burden, workload balance) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; B assumes a fix without diagnosis.

**41. A** — Caching the static skill-matrix document and trimming/summarizing older roster history directly reduces redundant token cost. D denies an obvious lever; C removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. D** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and C accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. C** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and D guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. C** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. A** — State insurance-regulation requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. B and C understate real architectural impact; D misidentifies the applicable regulatory regime.

**47. D** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal safety case for maximal review; C misattributes this to GDPR, which isn't the relevant regime described.

**48. D** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; C assumes one guardrail covers distinct risk types; B is factually wrong.

**49. B** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; C and D make unsupported blanket claims.

**50. B** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. A and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team.

**51. B** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a regulated system. A, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. C** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and D skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. D** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; B over-engineers the one-off task; C ignores that reuse profile should drive the choice.

**54. B** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, C, and D each understate what compliance-grade audit evidence actually requires.

**55. B** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by claims-ops, legal, and engineering audiences alike. A, C, and D each fail to serve at least one audience's real information need.

**56. C** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and B mishandle a real change; D disproportionately discards unaffected work.

**57. A** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. B, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. B** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, C, and D all leave that reasoning undocumented and effectively lost.

**59. C** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and D over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 8.*
