# CCARP Practice Exam 12

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
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

Meridian Mobile, a regional telecom retailer, wants to modernize how it handles customer escalations that arrive through three previously disconnected queues — billing disputes, device warranty claims, and network outage complaints — plus a fourth workflow for retention offers to at-risk subscribers. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with Meridian's stakeholders.

---

**Question 1.** Discovery reveals the client's actual goal is reducing average escalation resolution time by unifying the three disconnected queues, at the same staffing level — not adding new self-service capabilities customers currently lack.

- A) Frame the architecture around efficiency, building resolution-time and handle-volume metrics rather than novel-capability claims.
- B) Frame it around transformation instead, since collapsing three queues into one is inherently a transformational change no matter what discovery found.
- C) Frame it around cost reduction only, on the assumption that staffing cost is always the real driver behind a queue-consolidation project like this.
- D) Skip picking a specific value pillar entirely — a system that measurably works speaks for itself regardless of how the business frames its goals.

**Question 2.** Escalation handling requires different steps depending on the issue category, customer tier, and information uncovered mid-conversation (for example, discovering a device is under an active recall).

- A) A fixed workflow, since escalations of this kind always follow the same script no matter what the customer says mid-call.
- B) An agentic pattern, since the right sequence of steps varies by case and depends on findings uncovered mid-conversation.
- C) An augmented LLM pattern, since one retrieval-enhanced call is always treated as sufficient regardless of how the case actually unfolds.
- D) Whichever pattern prototypes fastest, since fixed workflows, agentic patterns, and augmented calls are functionally interchangeable here.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (billing-dispute, device-warranty, network-outage-diagnostics, retention-offer).

- A) Let each subagent message whichever subagent needs its output next directly, skipping the coordinator entirely to minimize hops.
- B) Merge all four responsibilities and their entire toolsets into a single subagent, trading specialization for less coordination overhead and simpler routing logic.
- C) Let subagents talk to each other directly, but log the traffic afterward so the coordinator can review it during a later audit.
- D) Route inter-subagent traffic through the coordinator to preserve observability, error handling, and controlled information flow.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition routes billing, device, and network escalations correctly while retention-eligible cases (customers actively threatening to cancel) are never routed to any subagent and silently fall through.

- A) Add a fifth, generic catch-all subagent whose only job is to absorb whatever escalation type the other four don't recognize as their own.
- B) Give the existing subagents broader tool access, on the reasoning that any one of them could, in principle, be stretched to handle any escalation type.
- C) Fix the coordinator's decomposition so it explicitly covers retention-eligible cases, instead of tuning the subagents that already work.
- D) Add a prompt instruction telling every subagent to flag any escalation it personally doesn't recognize as its own to handle.

**Question 5.** The design must align technical architecture to a specific business value pillar Meridian actually cares about, distinct from a generic "we added AI" narrative.

- A) Any AI system inherently demonstrates transformation on its own, so no additional framing work is needed from the architect.
- B) Efficiency, transformation, cost, and performance SLAs are example pillars; the chosen one should drive both architecture and metrics.
- C) Treat business value pillars as a sales-team concern that the architecture itself doesn't need to reference at all, regardless of what discovery surfaced.
- D) Choose the pillar after the system ships, based on whichever benefit turns out easiest to measure in hindsight, rather than up front.

**Question 6.** Frontline escalation agents are skeptical of the new system and worried it will be used to justify headcount reductions; discovery interviews surface this repeatedly.

- A) Ignore the sentiment entirely in the discussion, treating adoption concerns as something only change management should handle.
- B) Treat it as a real implicit constraint shaping adoption and rollout sequencing, alongside the explicit technical requirements raised in discovery.
- C) Proceed with the technical design and hand the sentiment entirely to change management, with no architectural input either way at all.
- D) Recommend against the project outright, based on the sentiment alone and independent of the technical case for it entirely.

**Question 7.** A stakeholder asks why the network-outage-diagnostics subagent uses a higher-capability, higher-cost model tier than the billing-dispute subagent.

- A) Use the same tier everywhere for simplicity, regardless of how much reasoning depth each task actually needs.
- B) Answer that a higher tier is used because outage work is simply "more important," without giving any further technical detail.
- C) Avoid explaining the tier difference at all, on the assumption that stakeholders don't need or want technical detail.
- D) Explain the tradeoff: outage diagnostics needs deeper telemetry reasoning, while billing disputes are simpler and cheaper to serve.

**Question 8.** The architecture's current design produces a final retention-offer recommendation with no mechanism to learn from which offers customers actually accepted or rejected over time.

- A) Treat this as acceptable, since the initial design was validated at launch and already reflects best practice.
- B) Treat feedback loops as a data-science concern that sits entirely outside the architecture, with no hooks needed in the system design.
- C) Add a feedback loop capturing offer acceptance and rejection outcomes as a first-class architectural hook.
- D) Defer any feedback mechanism to a hypothetical future phase, with no hooks for it in the current design.

**Question 9.** The client wants a single enhanced LLM call — with retrieval of the customer's plan and billing history — to answer straightforward "why is my bill higher this month" questions, without any multi-step autonomous orchestration.

- A) Build a full multi-agent architecture regardless of the task's simplicity, rewriting the system prompt for orchestration it doesn't need.
- B) Conclude this cannot be built with Claude at all, on the reasoning that it isn't structured as a multi-step autonomous agent.
- C) Require a structured fixed workflow with at least five sequential steps, regardless of how simple the underlying billing question actually is.
- D) Use an augmented LLM pattern — a single call enhanced with retrieval — fitting this simpler need without agentic orchestration overhead.

**Question 10.** The billing-dispute subagent's toolset has grown to include tools for tasks like device-shipping tracking and network-status lookups that are unrelated to billing disputes.

- A) Remove or relocate the unrelated tools, since capability bloat degrades tool-selection reliability.
- B) Treat this as having no architectural downside, as long as the subagent's prompt is well-written enough to compensate.
- C) Treat more tools as always improving a subagent's flexibility, and encourage adding still more over time.
- D) Increase the subagent's context window instead, on the theory that a bigger window will fully offset the added tool count and keep selection reliable.

**Question 11.** The coordinator currently processes each escalation sequentially through billing-dispute lookup, device-warranty lookup, and retention-offer scoring, even though device-warranty lookup and retention-offer scoring have no dependency on each other's output.

- A) Combine device-warranty lookup and retention-offer scoring into one subagent, so the sequencing question never has to be answered.
- B) Run device-warranty lookup and retention-offer scoring as independent, parallel calls once billing-dispute lookup completes.
- C) Treat sequential processing as required for auditability, regardless of whether the steps actually depend on each other.
- D) Treat parallelization as impossible within a coordinator/subagent architecture in general, regardless of whether steps share any real dependency.

**Question 12.** A regional VP unfamiliar with the technical details asks how the end-to-end escalation architecture should be described for a steering review.

- A) Present only the model names and per-call token costs involved, leaving the actual escalation flow undescribed for the committee.
- B) Describe input, processing, output, and the feedback loop at a level the committee can evaluate against business outcomes.
- C) Present the full technical architecture diagram, including every subagent's internal prompt and tool schema, without any simplification for a non-technical audience.
- D) Skip a high-level description entirely and go straight into a live implementation demo of the coordinator and subagents.

**Question 13.** A competing vendor proposes a single, generalist agent holding every tool (billing, device, network, retention) rather than a coordinator with specialized subagents.

- A) A single agent holding every tool is more likely to suffer degraded tool-selection reliability than specialized subagents.
- B) A single generalist agent scales better as tool count grows, since it avoids maintaining separate subagent boundaries.
- C) Treat specialized subagents as strictly a cost-increasing choice, with no reliability benefit to offset the added complexity.
- D) Treat the two approaches as architecturally equivalent, with no meaningful reliability or cost difference between a generalist agent and specialized subagents.

**Question 14.** The escalation architecture must eventually support a new escalation category (streaming-bundle disputes) planned for next year, but detailed requirements aren't available yet.

- A) Build full support for streaming-bundle disputes now, filling in the missing requirements with reasonable-sounding guesses.
- B) Ignore future escalation categories entirely until concrete requirements exist for them, even ones already announced as coming next year.
- C) Refuse to proceed with the current phase of work until every future requirement is fully finalized and signed off by stakeholders.
- D) Design the current decomposition with reasonable extensibility in mind, without over-building for speculative, undefined requirements down the line.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, on the assumption that a well-organized implementation is self-explanatory.
- B) Plan around the original architect remaining available indefinitely on call, instead of investing in documentation now.
- C) Document the reasoning behind key decisions — pattern choices, decomposition, tier selections — not just the final configuration values.
- D) Treat documentation as unnecessary, on the assumption that clean, well-organized code already makes the reasoning self-evident.

---

## Scenario B: Model Selection and Context Engineering for a Retail Merchandising Copilot (Questions 16–30)

Harborview Retail Group, a multi-category apparel retailer, wants Claude to help category buyers answer questions using both general reasoning and retrieval over a large, constantly-updated corpus of vendor contracts, sell-through reports, and category strategy memos. You're architecting the model selection, prompting approach, and integration layer for the merchandising copilot.

---

**Question 16.** Most buyer questions to the copilot are moderately complex; a small fraction require deep multi-step reasoning across many SKUs and vendors, and a small fraction are simple lookups (for example, "current on-hand units for SKU 4471").

- A) Route by task difficulty: a fast tier for lookups, a balanced tier for typical questions, and a higher tier for deep multi-step cases.
- B) Use the highest-capability tier on every question, to guarantee quality regardless of how simple the underlying lookup is.
- C) Use one fixed model tier for every question, treating complexity as irrelevant to tier selection, since routing logic adds engineering overhead the team would rather avoid.
- D) Use the fastest tier on every question to minimize cost, accepting the resulting quality loss on the harder cases.

**Question 17.** Every request to the copilot sends the same long system prompt (merchandiser persona, formatting rules, category taxonomy) followed by retrieved SKU and vendor data that varies per query.

- A) Put the retrieved content first, on the reasoning that it's the part most relevant to the specific query being asked.
- B) Place the stable system prompt first and enable caching, with retrieved content after it, to reduce latency and cost.
- C) Alternate system instructions and retrieved content throughout the prompt so both stay close to whatever they relate to.
- D) Treat prompt ordering as having no effect on cost or latency for a use case like this one, even at high query volume with heavy caching potential.

**Question 18.** The merchandising corpus mixes long-form vendor contracts and category strategy memos with short structured data (a table of weekly sell-through by SKU).

- A) Use the largest possible chunk size for everything, skipping schema- or shape-specific tuning, on the theory that one large-chunk strategy is simplest to build and maintain long-term.
- B) Assume one chunking and indexing strategy tuned for long-form documents can serve both content types equally well.
- C) Match chunking and indexing strategy to each data shape — long-form documents need different chunking than short structured records.
- D) Exclude the structured sell-through data from retrieval entirely, relying only on the long-form documents.

**Question 19.** Buyer queries range from exact lookups ("current inventory for SKU 4471") to conceptual questions ("how has the athleisure category's margin story evolved this year").

- A) Use only embedding similarity search for every query type, regardless of whether the query is an exact lookup.
- B) Match retrieval strategy to query pattern — metadata filtering for exact lookups, embeddings for conceptual questions, hybrid where both are needed.
- C) Use only structured metadata filtering for every query type, including the open-ended conceptual ones.
- D) Treat query pattern as entirely irrelevant to which retrieval approach is appropriate, since a single, well-tuned embedding index should already generalize across every kind of query without further tailoring.

**Question 20.** Buyers need each margin or forecast claim reliably mapped to a specific source document and section, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without any further structure or output validation behind it.
- B) Add citations after generation by searching for a plausible-looking source for each claim already produced, matching phrasing rather than verifying the underlying figure.
- C) Require structured output pairing each claim with its source (document, section, excerpt) so citation mapping survives synthesis.
- D) Append a general bibliography of consulted documents at the end of each response, without linking individual claims to it.

**Question 21.** Two retrieved sources disagree on a vendor's quoted unit cost by a small margin — likely because one reflects a pre-rebate price and the other a post-rebate net price.

- A) Average the two figures together and present the average as the unit cost, treating the discrepancy as noise rather than a real methodological difference.
- B) Prefer whichever source was retrieved first, regardless of which figure it happens to contain or how the two prices were actually calculated.
- C) Present both figures explicitly, annotated as a discrepancy, with source attribution and the likely methodological explanation.
- D) Omit the unit cost figure from the response entirely, since the two sources disagree and no single number can be confidently reported.

**Question 22.** A prompt asking the model to "always output valid structured JSON with source fields" still occasionally produces a conversational preamble before the JSON.

- A) Use tool-use or schema-constrained output so structure is enforced by the API mechanism, not by adjusting temperature.
- B) Repeat the same instruction more emphatically, in stronger language, elsewhere in the prompt.
- C) Post-process every response to strip any leading text that appears before the first `{`.
- D) Increase `max_tokens` so there's room for both the preamble and the JSON to fit, plus extra buffer in case the model adds trailing commentary after the closing brace too.

**Question 23.** The copilot needs to connect to a proprietary internal vendor-catalog system, exposing search and lookup capabilities to multiple other internal Claude-powered tools beyond just the merchandising copilot.

- A) Hard-code the vendor-catalog integration directly into this one copilot's application code, with no reuse path for other tools.
- B) Paste the entire vendor catalog into every prompt sent to every consuming tool, refreshing the pasted copy manually whenever the catalog changes upstream.
- C) Build an MCP server exposing the vendor-catalog operations as tools and resources, reusable across the internal tools that need it.
- D) Require each consuming tool to reimplement its own vendor-catalog integration independently, from scratch.

**Question 24.** The team is deciding between exposing the full vendor catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Treat loading the full catalog up front as always preferable, since completeness matters more than context cost, latency, or how much the catalog is expected to grow.
- B) Treat the two approaches as having no meaningful difference in context cost between them.
- C) Refuse to expose the catalog to the agent in any form, forcing all lookups through a human intermediary.
- D) Use progressive discovery — querying a catalog resource as needed — scaling better than loading the entire catalog up front.

**Question 25.** A buyer asks a chain-of-thought-friendly question requiring the model to reason step by step across several vendor contracts and sell-through reports before recommending a reorder quantity.

- A) Use zero-shot prompting with no reasoning guidance, treating it as always equally effective regardless of task structure.
- B) Treat multi-document reasoning as something the model cannot do at all, regardless of prompting approach or how the reasoning steps are structured.
- C) Use a chain-of-thought approach, allowing explicit intermediate reasoning, suited to this multi-document synthesis question.
- D) Restrict chain-of-thought prompting to coding tasks only, on the assumption it doesn't transfer to document synthesis.

**Question 26.** The copilot wants to standardize prompt fragments (citation format, category taxonomy, formatting rules) across several different buyer-facing features so changes propagate consistently.

- A) Duplicate the fragments into each feature's own structured prompt independently, updating each copy by hand.
- B) Treat modular prompt fragments as the same mechanism as prompt caching, and rely on caching alone to keep them consistent.
- C) Treat standardization across features as unachievable through prompt design, since only a single shared system prompt could keep them consistent, and even that doesn't scale well across many features.
- D) Use modular, composable, versioned prompt fragments shared across features — distinct from caching (a cost/latency lever) or Skills (a capability lever).

**Question 27.** The copilot occasionally returns confident, well-cited-looking margin figures that, on manual review, misstate a specific number from the correctly retrieved source report.

- A) Trust the fluent, well-formatted output as evidence that the cited figure is correct, since citation formatting alone signals accuracy.
- B) Increase output length, on the reasoning that more room in the response leaves more space for the model to work out and double-check the correct figure.
- C) Apply defensive validation, verifying extracted figures against the source excerpt rather than trusting confident phrasing.
- D) Treat this as purely a model limitation with no architectural mitigation available, regardless of what verification steps might catch it.

**Question 28.** The team debates whether buyer-facing latency SLAs should factor into model tier selection for the merchandising copilot.

- A) Let only cost factor into tier selection, treating latency as irrelevant to the decision.
- B) Treat SLAs as a stakeholder-communication concern only, with no bearing on technical architecture or model tier selection decisions at all.
- C) Treat latency as something that should never factor into model or architecture decisions.
- D) Weigh accuracy against the SLA's latency and cost tolerance, rather than defaulting to peak capability.

**Question 29.** A new model version is released with improved benchmark scores. The merchandising copilot currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, on the reasoning that newer benchmark scores are validation enough on their own, regardless of behavioral drift risk.
- B) Never upgrade models once the initial version is chosen, treating current behavior as permanently fixed and deterministic.
- C) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading.
- D) Upgrade immediately without testing, on the assumption that benchmark improvements guarantee production improvements.

**Question 30.** The copilot's context budget is a concern because both the system prompt/citation rules and the retrieved vendor/SKU data must fit alongside room for a detailed recommendation.

- A) Treat input and output token budgets as entirely independent, so schema design or content volume on one side never affects headroom on the other.
- B) Treat this tradeoff as only mattering for unusually long documents, never for typical queries.
- C) Treat output length as having no practical limit, regardless of how much input content is already in context.
- D) Input and output share one context-window budget, so retrieved content must be balanced against room for a detailed answer.

---

## Scenario C: Evaluation and Monitoring of a Field-Service Dispatch Assistant (Questions 31–45)

Atlas Utilities operates a fleet of field-service technicians who service gas and electric meters. A Claude-powered dispatch assistant recommends likely fault causes, required parts, and whether an issue can be resolved remotely versus requiring an on-site visit. It's been in production for several months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only technician first-time-fix rate and hasn't defined targets for latency, cost, or safety.

- A) Treat latency and cost as operations concerns that sit outside evaluation design entirely.
- B) Define metrics spanning accuracy, latency, cost, and safety as first-class alongside first-time-fix rate.
- C) Treat first-time-fix rate alone as sufficient, since it's the system's primary stated purpose and the only metric leadership originally asked to track.
- D) Treat safety metrics as relevant only for explicitly regulated industries.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past dispatch tickets.

- A) Treat a single automated method as sufficient for any production system, regardless of what edge cases or safety-relevant paths it fails to cover.
- B) Replace the automated checks entirely with human review as the sole evaluation method going forward.
- C) Expand the labeled set indefinitely, treating dataset size as the only improvement lever available.
- D) Use mixed methodologies — automated eval, human review, and adversarial testing — since no single method covers every failure mode.

**Question 33.** The team wants to test whether a new prompt version improves technician-recommendation quality before rolling it out to all dispatch traffic.

- A) Roll the new prompt out to all traffic immediately, watching for problems only after the fact instead of testing beforehand at all.
- B) Change the prompt and the model tier at the same time, assuming deterministic output will make attribution easy afterward, even with two variables changing together.
- C) Skip testing altogether, treating prompt changes as inherently low-risk regardless of how technician-facing recommendations might change.
- D) Run an A/B test changing only the prompt version against a stable baseline, so any difference can be attributed to that change.

**Question 34.** A dispatch recommendation cites the wrong required part number. Investigation shows the underlying parts-catalog lookup returned correct, current data, and the model's response paraphrased it inaccurately.

- A) Treat this as a prompt/generation issue, calling for prompt or output-validation fixes rather than retrieval changes.
- B) Treat this as a retrieval problem and fix the indexing pipeline instead, even though the pipeline already returned correct, current data.
- C) Treat this as impossible to diagnose without a full model retraining cycle, regardless of what the paraphrasing error actually indicates.
- D) Treat this as a model-tier mismatch requiring a different, higher tier, regardless of what the investigation actually found about where the error occurred.

**Question 35.** Immediately after a scheduled parts-catalog refresh, the dispatch assistant starts recommending obsolete part numbers, while model version and average latency are unchanged.

- A) Suspect a temperature setting change, since the assistant's apparent confidence changed, even though no temperature parameter was actually touched in the refresh.
- B) Suspect the model was silently updated by the provider, despite the version string staying the same.
- C) Investigate the retrieval and indexing layer first, since the regression tracks the data refresh event with model and latency unchanged.
- D) Suspect the context window shrank, rather than the structured retrieval layer that was just refreshed.

**Question 36.** The team wants to reduce cost and latency for dispatch recommendations but is worried about hurting first-time-fix accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Optimize cost, latency, and accuracy jointly against the system's actual SLA and budget, not any single dimension in isolation.
- B) Maximize accuracy without regard to cost or latency, treating a slower, pricier configuration as always the safer choice.
- C) Optimize cost, latency, and accuracy independently of each other, treating each as a fixed, deterministic target on its own.
- D) Treat this tradeoff as unmeasurable, something that can only be guessed at rather than tested.

**Question 37.** Production monitoring for the dispatch assistant currently reports only an overall weekly average accuracy score.

- A) Treat a single aggregate average, once validated, as sufficient for production monitoring regardless of segment performance.
- B) Have monitoring surface drift and outliers — a per-specialty breakdown — since an aggregate average can hide a failing segment.
- C) Treat weekly granularity as always sufficient, regardless of how the system is actually behaving across specialties.
- D) Have monitoring track only cost, on the assumption that accuracy is already fully captured by the eval suite alone.

**Question 38.** The team proposes cutting human review of flagged low-confidence dispatch recommendations by 80%, citing a 96% aggregate accuracy score.

- A) Segment accuracy by issue type and specialty before cutting review, since an aggregate figure can mask a failing segment.
- B) Proceed with the review cut based on the 96% aggregate figure alone, without further segmentation.
- C) Treat aggregate accuracy as definitionally representative of every individual segment.
- D) Treat human review as something that should never be reduced, regardless of measured accuracy, segment performance, or the actual cost of maintaining it.

**Question 39.** An A/B test shows a new prompt version improves first-time-fix rate, but the team has not checked whether it also changed the rate of recommending an on-site visit for issues that should have been resolved remotely.

- A) Treat first-time-fix rate alone as a sufficient signal to ship the change without checking any other dispatch-outcome metric.
- B) Check the remote-resolution-eligible failure mode before shipping, since a fix-rate gain could increase unnecessary dispatches unnoticed.
- C) Treat this failure mode as something evaluation is structurally unable to measure, no matter how the test data or dispatch logs are instrumented.
- D) Ship the change and monitor informally afterward, in place of testing for this specific failure mode beforehand.

**Question 40.** The team wants to diagnose why a subset of technically accurate dispatch recommendations are rated poorly by technicians in post-job surveys.

- A) Investigate a dimension beyond accuracy, like clarity or field practicality, since "accurate but poorly rated" points at an unmeasured gap.
- B) Assume the accuracy metric itself is broken and discard it outright, without checking any other explanation for the low ratings first.
- C) Increase the model's capability tier, assuming higher capability always improves structured output ratings regardless of what technicians are actually reacting to.
- D) Ignore technician satisfaction scores entirely, in favor of the accuracy metric alone, since surveys are harder to standardize than an automated check.

**Question 41.** The team is optimizing token usage and notices the system sends the full ticket history plus a large static equipment-manual excerpt on every turn of multi-turn dispatch conversations.

- A) Treat this as having no optimization opportunity, on the assumption that full history is always required on every turn.
- B) Remove the equipment-manual excerpt entirely, without an alternative source for the content it provided to technicians.
- C) Switch to a smaller model as the only lever for reducing token cost, even though redundant static content is the larger driver.
- D) Apply prompt caching to the static equipment-manual excerpt, and trim or summarize older ticket-history turns to cut token cost.

**Question 42.** Logging captures every raw prompt and response for the dispatch assistant, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Treat raw logging at full volume, by itself, as a sufficient and complete observability strategy for any production system regardless of scale.
- B) Reduce logging volume to save storage cost, treating that as a full fix even though the signals stay unstructured and unreviewable.
- C) Treat observability as requiring no structure at all, as long as every prompt and response is retained somewhere on disk indefinitely.
- D) Redesign observability toward structured, aggregable signals — sampling, tagged categories, segment metrics — since raw logs aren't reviewable at volume.

**Question 43.** The team wants to identify whether a recent quality regression was caused by a prompt change, a model version change, or an equipment-manual content update — all three happened in the same week.

- A) Assume whichever change shipped most recently is automatically the cause, without checking the other two changes at all.
- B) Revert all three changes without investigation, regardless of which one, if any, actually caused the regression, and regardless of the cost of reverting each.
- C) Treat attribution as impossible once multiple changes ship in the same week, even though each one could still be tested in isolation afterward.
- D) This is why changes should ship one variable at a time — with three at once, attribution requires isolating and re-testing each independently.

**Question 44.** An automated eval asserts that a dispatch-summary output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) Make the reference string longer, on the assumption that added length will resolve the intermittent failures.
- B) Conclude the model is malfunctioning and needs retraining, since its outputs can no longer be validated against the fixed string.
- C) Increase the temperature setting to fix the intermittent failures, on the reasoning that more randomness will somehow stabilize matching.
- D) Exact-string-match evals are the wrong tool for non-deterministic LLM output; the eval should check content and structure, not exact text.

**Question 45.** Leadership wants a single number to represent "how good" the dispatch assistant is, to track over time.

- A) Treat a single number as always achievable and sufficient on its own, regardless of how many dimensions quality actually spans.
- B) Use first-time-fix rate alone as that single number, since it's the system's stated purpose and the metric leadership already recognizes.
- C) Offer a single aggregate metric as a top-line indicator, but pair it with segment- and dimension-level detail so it doesn't mask a failing area.
- D) Refuse to provide any single summary metric, under any circumstances leadership might reasonably ask for one to track.

---

## Scenario D: Governance and Team Enablement for an Insurance Claims Modernization (Questions 46–60)

Cascade Mutual Insurance is modernizing its claims-intake and reserve-estimation systems with a Claude-powered assistant, and its 25-person claims engineering team uses Claude Code internally for day-to-day development. You are responsible for governance, regulatory alignment, and developer enablement for the program.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic for the claims system is already built.

- A) Treat this sequencing as carrying no real risk, on the assumption that compliance requirements can always be bolted on right before launch without touching core logic.
- B) Treat compliance as affecting only legal documentation, with no bearing on the system's architecture.
- C) State insurance data-privacy and retention rules can force structural changes far costlier to retrofit than to design in early.
- D) Treat FedRAMP, rather than state insurance regulation, as the relevant regime for this client.

**Question 47.** A team proposes requiring human approval on every single output the claims-intake system produces, framing it as the safest governance posture.

- A) Treat maximal human review on every single output as always the correct default posture for any insurance AI system, regardless of error cost.
- B) Treat human reviewers as categorically less accurate than the model, making any review step counterproductive regardless of stakes.
- C) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should target high-stakes, judgment-requiring decisions specifically.
- D) Treat this level of review as required by GDPR, regardless of the actual regulatory regime or error-cost profile of this specific program.

**Question 48.** The claims system must identify and mitigate standard LLM risks — hallucination, prompt injection from claimant-submitted free text, and inconsistent output — as part of its design.

- A) Address these risks only if and when they're observed in production first, rather than addressing them during design.
- B) Design mitigations for each known failure mode up front — grounding, isolation, and output validation — rather than reacting after the fact.
- C) Treat these risks as exclusive to non-insurance use cases, and entirely out of scope for a regulated claims system like this one.
- D) Rely on a single generic guardrail to address all three distinct risk types equally well, without tuning specific to each mode.

**Question 49.** The claims operations team asks whether the system's payout recommendations could produce disparate outcomes across different policyholder demographics.

- A) Treat this as entirely a legal/compliance concern that belongs to review after launch, with no bearing on the architecture chosen beforehand.
- B) Recognize bias and fairness as architecture concerns — check whether training/eval data reflects the served population and measure disparate impact.
- C) Treat disparate impact as impossible in an LLM-based system by construction, since the model has no explicit demographic fields in its prompt.
- D) Treat this concern as applying only to systems making final payout decisions, not to any assistive system.

**Question 50.** The claims engineering team's Claude Code usage is inconsistent — some engineers have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Standardize CLAUDE.md hierarchy and shared MCP configuration at the team level so behavior doesn't depend on local setup.
- B) Have each engineer individually troubleshoot their own local configuration on an ad hoc basis.
- C) Restrict Claude Code usage to a single designated engineer to reduce variance across the team.
- D) Accept the inconsistency as an unavoidable cost of adopting AI tooling at all, since every engineer's local machine will always differ somewhat.

**Question 51.** The team wants Claude Code-generated code changes in this regulated claims context to go through the same review rigor as any other change.

- A) Let AI-assisted code bypass standard review, on the reasoning that it was "written by AI" rather than a person.
- B) Keep standard SDLC practices — code review, testing, version control — in place regardless of whether Claude Code assisted with the generation.
- C) Apply only a spot-check to AI-generated code, on the assumption that its output is already pre-validated.
- D) Set a lower review bar for AI-generated code than for human-written code in this same regulated codebase, on the reasoning that Claude Code output needs less scrutiny.

**Question 52.** A production incident traces back to a Claude Code-generated claims-calculation change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code itself, without further investigation into the integration layer.
- B) Triage the same way any incident is triaged — isolate integration-layer versus code/model-output failure using traces and logs.
- C) Disable Claude Code for the team entirely, as a blanket response to any incident involving it, regardless of what caused it.
- D) Roll back all recent Claude Code-assisted changes, regardless of whether they're actually relevant to this specific incident.

**Question 53.** The claims operations team wants a documented, repeatable workflow for a recurring task (generating a weekly reserve-adequacy summary) versus a one-off exploratory coding task.

- A) Package the recurring report workflow as a Skill for on-demand, consistent reuse; leave the one-off task as unstructured.
- B) Build both the recurring report and the one-off task as ad hoc, undocumented prompts each time either is needed.
- C) Build both as dedicated MCP servers, regardless of how often either one is actually reused later on.
- D) Treat recurring workflows and one-off tasks as needing to be built identically, with no real distinction between them.

**Question 54.** The compliance team wants documented evidence of who accessed what claimant-related data through the system and when.

- A) Design access-control and audit-logging as explicit components satisfying identity, authorization, and monitoring requirements.
- B) Treat access logging as optional, as long as the system already has role-based permissions in place.
- C) Treat audit logging as something that can be added later, with no real architectural impact from doing so.
- D) Log only failed access attempts, on the assumption that successful, authorized access to claimant data never needs its own audit trail at all, since it was permitted.

**Question 55.** The steering committee for this claims modernization includes claims-operations, legal, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, on the assumption they'll fully relay the relevant tradeoffs to operations and legal on their own.
- B) Skip stakeholder communication of any kind until the system is fully built and ready to demo.
- C) Tailor architectural communication to each audience, framing tradeoffs in terms claims-operations and legal can evaluate.
- D) Use identical technical documentation for all three audiences, to save the effort of tailoring it.

**Question 56.** Midway through the project, the claims team's requirements shift meaningfully based on a new state regulatory bulletin.

- A) Treat this as normal lifecycle management — re-engage discovery for the affected scope and communicate the change's tradeoff to stakeholders.
- B) Refuse to incorporate the change, on the reasoning that requirements were already agreed upon earlier and shouldn't shift mid-project.
- C) Incorporate the change silently, without informing stakeholders of its impact on scope, timeline, or downstream dependencies.
- D) Restart the entire project from scratch, regardless of the change's actual scope or how much unaffected work already exists.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the claims operations team.

- A) Treat this as the correct lifecycle model, with monitoring and iteration becoming entirely the operations team's responsibility.
- B) Treat lifecycle responsibility as ending once the contract is signed, regardless of what happens to the system after launch.
- C) Treat monitoring as necessary only if a major incident actually occurs, since routine operation needs no architect-level attention.
- D) Lifecycle management includes monitoring and iteration on production signal as part of the architect's ongoing responsibility, not just handoff.

**Question 58.** Documentation for this claims system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) Treat this level of documentation as sufficient, since the structured "what" is all a future team needs.
- B) Have documentation also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — not just the final values.
- C) Treat documenting the reasoning behind decisions as unnecessary overhead in a regulated environment.
- D) Restrict system modification to the original architect only, treating any future documentation effort as effectively moot once that restriction is in place.

**Question 59.** The claims operations team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Evaluate specific task categories for genuine friction reduction versus cases where review overhead may exceed time saved.
- B) Assume AI-assisted tooling always saves time on every task category, as a default without measurement.
- C) Ban Claude Code for all documentation tasks outright, without evaluation, since output can't be validated well enough to trust unsupervised.
- D) Mandate Claude Code usage for every task category, regardless of any measured benefit, since broad adoption is treated as valuable on its own.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) Treat this as an acceptable ongoing inefficiency, with no architectural fix considered even though the same triage steps repeat weekly.
- B) Document the triage process (distinguishing integration-layer from model-output failures) as shared operational knowledge, reducing redundant re-derivation.
- C) Restrict debugging responsibilities to a single designated engineer going forward, rather than sharing the triage knowledge across the team.
- D) Treat this as resolvable only by switching to an entirely different tool, rather than addressing how failures are currently triaged.

---
# Answer Key — Practice Exam 12

**Quick key:** 1-A, 2-B, 3-D, 4-C, 5-B, 6-B, 7-D, 8-C, 9-D, 10-A, 11-B, 12-B, 13-A, 14-D, 15-C, 16-A, 17-B, 18-C, 19-B, 20-C, 21-C, 22-A, 23-C, 24-D, 25-C, 26-D, 27-C, 28-D, 29-C, 30-D, 31-B, 32-D, 33-D, 34-A, 35-C, 36-A, 37-B, 38-A, 39-B, 40-A, 41-D, 42-D, 43-D, 44-D, 45-C, 46-C, 47-C, 48-B, 49-B, 50-A, 51-B, 52-B, 53-A, 54-A, 55-C, 56-A, 57-D, 58-B, 59-A, 60-B

---

**1. A** — A goal of more volume/consistency within the same staffing and cycle time is a throughput/efficiency problem; naming that pillar correctly shapes both architecture and success metrics. B, C, and D either misname the pillar or skip the framing discovery actually surfaced.

**2. B** — Steps that vary by case and depend on intermediate findings are the defining case for an agentic pattern. A assumes a predictability the scenario lacks; C undersells the orchestration needed; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. D** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. A and C sacrifice these properties for a shortcut; B discards the specialization that motivated separate subagents.

**4. C** — Every subagent succeeding while an entire escalation category is never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, B, and D all patch downstream instead of fixing the actual scope gap.

**5. B** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. A, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. B** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and C treat it as out of scope; D overreacts to sentiment alone without weighing it against the technical case.

**7. D** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. A and B withhold the reasoning stakeholders need; C removes a deliberate, justified difference for false simplicity.

**8. C** — Adding a feedback loop that captures offer outcomes as a first-class architectural component is what lets the system improve after deployment. A, B, and D all treat a first-class architectural component as optional or someone else's problem.

**9. D** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and C over-engineer a simple augmentation need; B is factually wrong.

**10. A** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not writing around it. B and C ignore this real degradation; D doesn't address selection reliability at all.

**11. B** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite completes, reducing latency without sacrificing correctness. A and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. B** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; C is too much of the wrong kind of detail; D skips the communication need entirely.

**13. A** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. B, C, and D all understate or deny this real architectural tradeoff.

**14. D** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A wastes effort guessing at undefined requirements; B ignores a known future need entirely; C blocks current delivery unnecessarily.

**15. C** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, B, and D all leave the actual knowledge transfer gap unaddressed.

**16. A** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. B and D sacrifice fit-to-task or quality; C ignores complexity variation entirely.

**17. B** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, C, and D all misstate or break the caching opportunity.

**18. C** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and B ignore this mismatch; D discards useful structured data.

**19. B** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and C force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. C** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, B, and D all reintroduce the failure mode the fix is meant to prevent.

**21. C** — Presenting both figures with attribution and a likely methodological explanation preserves the actual information for the buyer rather than resolving a real discrepancy arbitrarily. A, B, and D all discard or obscure a genuine data conflict.

**22. A** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests or sampling-parameter tweaks that can still drift. B and C are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. C** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. A, B, and D all fail the reuse or maintainability requirement.

**24. D** — Progressive discovery via a queryable catalog resource scales with catalog growth better than loading the entire catalog into every prompt. A and B ignore the real context cost of the monolithic approach; C removes needed capability entirely.

**25. C** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. A, B, and D all misstate the fit or capability of prompting techniques for this task.

**26. D** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; B conflates two distinct mechanisms; C denies a real, common architecture pattern.

**27. C** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; B doesn't address correctness; D incorrectly claims no architectural mitigation exists.

**28. D** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, B, and C each drop a relevant factor from the decision.

**29. C** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and D assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. D** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and C all misstate this real, architecture-relevant constraint.

**31. B** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if first-time-fix rate improves. A, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. D** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. A, B, and C each over-rely on or discard one method without addressing the actual coverage gap.

**33. D** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; C dismisses a real risk without evidence.

**34. A** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. B and D misdiagnose the layer at fault; C avoids diagnosis entirely.

**35. C** — A regression tied specifically to a data refresh event, with model and latency unchanged, points first at retrieval/indexing. A, B, and D would not specifically correlate with a parts-catalog refresh.

**36. A** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. B and C optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. B** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. A and C accept a monitoring blind spot; D drops accuracy monitoring from observability entirely.

**38. A** — Segmenting accuracy by issue type and technician specialty before cutting review protects against a failing segment hiding behind a healthy aggregate. B and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. B** — An isolated first-time-fix improvement could mask a worsened dispatch-necessity failure mode; checking specifically for that before shipping is the correct diagnostic step. A and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. A** — "Accurate but poorly rated" points at an unmeasured quality dimension (clarity, completeness, practicality) rather than a broken accuracy metric. B and D discard a working, differently-scoped metric; C assumes a fix without diagnosis.

**41. D** — Caching the static equipment-manual excerpt and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; B removes needed content; C is a blunt, quality-risking lever when a more targeted fix is available.

**42. D** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and C accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. D** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and B guess without evidence; C gives up on a solvable (if effortful) diagnostic problem.

**44. D** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. B and C misdiagnose model behavior as broken; A doesn't address the actual mismatch between eval design and output variability.

**45. C** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; D refuses a reasonable, common stakeholder request.

**46. C** — State insurance data-privacy and retention requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate real architectural impact; D misidentifies the applicable regulatory regime.

**47. C** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal safety case for maximal review; D misattributes this to GDPR, which isn't the relevant regime described.

**48. B** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; D assumes one guardrail covers distinct risk types; C is factually wrong.

**49. B** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; C and D make unsupported blanket claims.

**50. A** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. B and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team.

**51. B** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a regulated system. A, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. B** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and D skip diagnosis; C is a disproportionate reaction that doesn't investigate the actual cause.

**53. A** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. B under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. A** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. B, C, and D each understate what compliance-grade audit evidence actually requires.

**55. C** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by claims-operations, legal, and engineering audiences alike. A, B, and D each fail to serve at least one audience's real information need.

**56. A** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. B and C mishandle a real change; D disproportionately discards unaffected work.

**57. D** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, B, and C all end architectural responsibility earlier than the lifecycle model calls for.

**58. B** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, C, and D all leave that reasoning undocumented and effectively lost.

**59. A** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. B and D over-assume benefit; C forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 12.*
