# CCARP Practice Exam 2

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent Supply-Chain and Logistics Orchestration, RAG Integration for a Legal Case-Law Research Platform, Evaluation and A/B Testing of a Sales-Forecasting Copilot, Lifecycle Management and Enablement for a Global Manufacturing Rollout) |
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

## Scenario A: Multi-Agent Supply-Chain and Logistics Orchestration Platform (Questions 1–15)

Meridian Freight Networks, a global logistics operator, wants to modernize freight booking, carrier selection, exception handling (delays, customs holds, damaged cargo), and shipment tracking. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with dispatch and operations stakeholders.

---

**Question 1.** Discovery with Meridian's operations leadership reveals the actual goal is booking 2.5x more freight volume through the existing carrier network with the same dispatch staff, at the same average booking cycle time — not new routing capabilities the current process lacks.

- A) Frame the architecture around transformation, arguing AI should always introduce new capability regardless of what discovery found.
- B) Frame the architecture around efficiency, with success metrics built around bookings processed per dispatcher rather than novel capability.
- C) Frame the architecture around cost reduction, since cutting spend is the pillar easiest to defend to a steering committee.
- D) Skip framing around a specific value pillar, and let the shipped system's throughput numbers speak for themselves.

**Question 2.** Generating the standard customs export declaration for an international shipment follows the same five-step sequence every time — regardless of shipment type, carrier, or destination country.

- A) An agentic pattern, since customs paperwork always benefits from autonomous step selection even when the steps never actually vary.
- B) An augmented LLM pattern, since a single retrieval-enhanced call handles any customs task regardless of how many steps it involves.
- C) Whichever pattern minimizes initial build time, treating the two patterns as interchangeable implementation choices.
- D) A fixed workflow, since the steps are predetermined and identical for every shipment regardless of case specifics.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (carrier-rate lookup, customs-compliance check, exception triage, shipment-status synthesis).

- A) Let each subagent pass its results directly to whichever subagent needs them next, skipping the coordinator to save a hop.
- B) Merge all four responsibilities into a single subagent, trading specialization for lower coordination overhead.
- C) Route all inter-subagent communication through the coordinator, preserving observability and consistent error handling.
- D) Let subagents communicate directly with each other, then reconstruct an audit trail afterward from logs.

**Question 4.** A stakeholder asks why the customs-compliance subagent runs on a higher-capability, higher-cost model tier than the shipment-status-synthesis subagent.

- A) "The higher tier is used because compliance work is more important" is a complete answer without needing to mention cost, latency, or the reasoning depth compliance actually requires.
- B) Avoid walking through the tradeoff in detail, since stakeholders don't need to understand which model tier serves which subagent.
- C) Explain the tradeoff explicitly: deeper reasoning justifies the added cost/latency for compliance, while synthesis is simpler and suits a cheaper tier.
- D) Standardize every subagent on the customs-compliance subagent's tier for consistency, regardless of how much reasoning each task actually needs.

**Question 5.** The design must align the technical architecture to a specific business value pillar Meridian's leadership actually cares about, distinct from a generic "we added AI" narrative.

- A) Efficiency, transformation, productivity, cost, and SLA performance are examples; the pillar chosen should drive the architecture and its success metrics.
- B) Any AI-powered logistics system inherently demonstrates transformation, so no further framing exercise is needed before design begins.
- C) Business value pillars are a sales and marketing concern that architects can leave entirely to the go-to-market team.
- D) The pillar should be selected after launch, once the team sees empirically which benefit turned out to be the easiest and cheapest one to report to the steering committee.

**Question 6.** Discovery interviews with dock and dispatch staff repeatedly surface fear that automated carrier selection and exception handling will eliminate their roles.

- A) Treat this sentiment as a real implicit constraint alongside the explicit requirements — it shapes sequencing and where human-in-the-loop checkpoints matter.
- B) Ignore the sentiment in the architecture entirely, since staffing anxiety wasn't written down anywhere as a stated technical requirement during discovery.
- C) Proceed with the technical design and hand the sentiment entirely to change management, with zero architectural input either way.
- D) Recommend against the project entirely, since staff fear of job loss should override whatever efficiency and throughput gains discovery already documented and confirmed.

**Question 7.** Every subagent performs its assigned work correctly, but the coordinator's decomposition routes only standard ocean-freight shipments into the pipeline — hazmat and oversized-cargo shipments are never routed to any subagent and silently fall through untouched.

- A) Add a fifth catch-all subagent specifically scoped to intercept hazmat and oversized-cargo shipments before they fall through untouched.
- B) Add a prompt instruction telling the existing subagents to flag shipment types they don't recognize.
- C) Give the existing subagents broader tool access so any of them can handle any shipment type end to end.
- D) Fix the coordinator's decomposition so it explicitly covers every shipment category, hazmat and oversized cargo included.

**Question 8.** The architecture currently produces a final exception-resolution recommendation with no mechanism to learn from dispatcher overrides or downstream outcomes over time.

- A) Add a feedback loop capturing dispatcher overrides and outcomes as a first-class architectural component.
- B) This is acceptable, since the initial design already reflects current best practice for exception handling.
- C) Feedback loops are a data-science concern that belongs to the analytics team, not the architecture.
- D) Defer any feedback mechanism to a hypothetical future phase, with no hooks built into the current design.

**Question 9.** Meridian wants a single enhanced LLM call — with tool access to the live shipment-tracking API — to answer straightforward "where is my shipment" questions, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture with a coordinator and specialized subagents, regardless of how simple the underlying task actually is.
- B) An augmented LLM pattern (a single call enhanced with tool access) fits this simpler augmentation need without the overhead of agentic orchestration.
- C) This requires a fixed workflow with at least five predetermined sequential steps before an answer can be returned.
- D) This cannot be built with Claude at all, since a tracking lookup doesn't involve autonomous agent behavior.

**Question 10.** The carrier-rate-lookup subagent's toolset has grown to include tools for tasks like invoice generation and driver scheduling that are unrelated to rate lookup.

- A) This capability bloat degrades tool-selection reliability; unrelated tools should move to a more appropriate subagent.
- B) This has no architectural downside as long as the subagent's prompt is written clearly enough to disambiguate.
- C) More tools always improve a subagent's flexibility, so growth here should be encouraged rather than pruned.
- D) The fix is to increase the subagent's context window so every added tool, however unrelated to rate lookup, still fits in a single prompt.

**Question 11.** The coordinator currently processes each shipment sequentially through carrier-rate lookup, customs-compliance check, exception triage, and status synthesis — even though customs-compliance check and exception triage have no dependency on each other's output.

- A) Sequential processing is required for auditability in a logistics context, even without a data dependency.
- B) Combine customs-compliance check and exception triage into a single subagent to avoid the sequencing question.
- C) Parallelization isn't possible within a coordinator/subagent architecture once the first lookup has run.
- D) Run customs-compliance check and exception triage as independent, parallel calls once rate lookup completes, to increase throughput.

**Question 12.** Meridian's steering committee, unfamiliar with the technical details, asks how the end-to-end architecture should be described at a high level.

- A) Present only the model names and per-call token costs involved in the pipeline, leaving business outcomes for the committee to infer on their own.
- B) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, not implementation internals.
- C) Present the full technical architecture diagram, including subagent prompts, with no simplification for the non-technical committee.
- D) Skip a high-level description entirely and move straight into a live implementation demo the committee has no context to evaluate.

**Question 13.** A competing vendor proposes a single generalist agent with every tool (rate lookup, compliance, exception handling, tracking) rather than a coordinator with specialized subagents.

- A) A single agent holding every tool is more likely to suffer degraded tool-selection reliability than subagents scoped to narrower roles.
- B) A single generalist agent scales better as the tool count grows, since it avoids coordinator overhead entirely.
- C) There is no meaningful architectural difference between a generalist agent and a coordinator with specialized subagents.
- D) Specialized subagents are strictly a cost-increasing choice, since a single generalist agent with every tool achieves the same reliability for less.

**Question 14.** The architecture must eventually support a new shipment category (cross-border rail freight) Meridian plans to launch next year, but detailed requirements aren't available yet.

- A) Build full support for cross-border rail freight now, guessing at requirements operations hasn't finalized and may still change before launch.
- B) Refuse to proceed with the current phase's delivery until next year's rail-freight requirements are finalized.
- C) Ignore the future shipment category entirely in the current design, addressing it only once requirements exist.
- D) Design the current decomposition and subagent boundaries with reasonable extensibility, without over-building for undefined requirements.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, since implementation details are self-explanatory to any competent engineer.
- B) Rely on the original architect remaining available indefinitely to answer questions in person, instead of writing any of the reasoning down.
- C) Documentation is unnecessary as long as the codebase itself is well organized and consistently named.
- D) Document the architecture and the reasoning behind key decisions — pattern choices, decomposition boundaries, tier selections.

---

## Scenario B: RAG Integration for a Legal Case-Law Research Platform (Questions 16–30)

CaseLantern, a legal research platform serving litigation attorneys, wants Claude to answer case-law research questions using both general reasoning and retrieval over a large, constantly-updated corpus of court opinions, statutes, and internal firm memoranda. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most attorney questions are moderately complex; a small fraction require deep multi-step reasoning across many opinions, and a small fraction are simple citation lookups.

- A) Always use the fastest tier to minimize cost across the board, accepting quality loss on the complex multi-step questions that need reasoning most.
- B) Always use the highest-capability tier to guarantee quality on every question, even the simple citation lookups that plainly don't need it.
- C) Route based on task difficulty — fast tier for lookups, balanced tier for typical questions, higher-capability tier for deep research.
- D) Use one fixed model tier for every question that comes in, regardless of whether it's a one-line lookup or a multi-opinion synthesis task.

**Question 17.** Every request sends the same long system prompt (attorney persona, citation-format rules, jurisdiction-handling instructions) followed by retrieved opinion excerpts that vary per query.

- A) Order doesn't affect cost or latency for this use case, so any arrangement of the system prompt and retrieved content works.
- B) Place the stable system prompt first and enable caching, with the varying retrieved content after it, to cut latency and cost.
- C) Put the retrieved content first since it's most specific to the query, ahead of the stable system prompt.
- D) Alternate the system prompt and retrieved content throughout the request so neither one sits first consistently.

**Question 18.** The corpus mixes long-form court opinions with short structured data (a table of statute citations and effective dates).

- A) Chunking and indexing strategy should match each data shape, or retrieval quality degrades for whichever type doesn't match the tuning.
- B) One chunking and indexing strategy tuned for long-form opinions can serve short tabular statute records equally well without adjustment.
- C) Structured statute data should be excluded from retrieval entirely, since it doesn't resemble the long-form opinions the system is built around.
- D) Use the largest possible chunk size for everything so a single strategy never needs to change across content types.

**Question 19.** Attorney queries range from exact lookups ("cite for Smith v. Jones, 2019") to conceptual questions ("how has the standard for qualified immunity evolved across circuits").

- A) Use only embedding similarity search for every query type, including exact citation lookups that have a known, unambiguous target.
- B) Query pattern doesn't affect which retrieval approach is appropriate, so one mechanism can serve every kind of question equally.
- C) Match retrieval strategy to query pattern: metadata filtering for exact lookups, embeddings for conceptual questions, hybrid where needed.
- D) Use only structured/metadata filtering for every query type, including open-ended conceptual synthesis questions.

**Question 20.** Attorneys need citations that reliably map each claim to a specific opinion and pincite, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without further structure, trusting the instruction alone to hold under load.
- B) Add pincites after the fact by searching for a plausible source for each claim, without validating that the source actually supports the specific wording used.
- C) Append a general bibliography of consulted opinions at the end of each response instead of tying individual claims to individual sources.
- D) Require structured output pairing each claim with its source (case, pincite, excerpt) so mapping survives synthesis.

**Question 21.** Two retrieved opinions from different circuits state the applicable standard differently — likely reflecting a genuine circuit split rather than an error.

- A) Average the two standards together and present a single blended formulation as the applicable rule.
- B) Omit the applicable standard entirely from the answer, since the two retrieved sources disagree with each other.
- C) Always prefer whichever opinion happened to be retrieved first, treating retrieval order as a tiebreaker.
- D) Present both standards explicitly, annotated as a circuit split, with source attribution for each rather than picking one.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the structured-output instruction more emphatically in the prompt text, without changing the mechanism by which the request is actually sent to the model.
- B) Increase max_tokens to leave room for both the conversational preamble and the schema-shaped JSON that's supposed to follow it.
- C) Post-process every response to strip any text appearing before the first `{` of the structured JSON payload, treating drift as a string-cleanup problem.
- D) Use tool-use/schema-constrained output so structure is enforced by the API mechanism, not requested through prose.

**Question 23.** CaseLantern needs to connect to a proprietary internal memoranda system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this research platform.

- A) Hard-code the memoranda integration into this platform's application code only, without publishing a reusable schema or interface any other tool could call.
- B) Build an MCP server exposing the memoranda operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- C) Paste the entire memoranda corpus into every prompt so no separate integration layer is needed.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team is deciding between exposing the full case-law catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Loading the full catalog up front is always preferable for completeness, even as the corpus grows past what any single prompt can hold.
- B) There is no meaningful difference in context cost between loading everything up front and querying a catalog resource only when needed.
- C) The catalog should never be exposed to the agent in any form, forcing every lookup through a human intermediary instead.
- D) Progressive discovery scales better than loading the entire catalog up front, especially as the corpus grows.

**Question 25.** An attorney asks a chain-of-thought-friendly question requiring the model to reason step by step across several retrieved opinions before concluding.

- A) A chain-of-thought approach, allowing explicit intermediate reasoning steps, suits this multi-opinion synthesis question.
- B) Zero-shot prompting with no reasoning guidance is always equally effective, even across several opinions requiring multi-step synthesis.
- C) Chain-of-thought prompting is only useful for coding tasks, not for legal reasoning across multiple retrieved opinions.
- D) The model cannot reason across multiple opinions regardless of prompting approach, so any technique here is equivalent.

**Question 26.** CaseLantern wants to standardize prompt fragments (citation format, jurisdiction disclaimers, formatting rules) across several different attorney-facing features so changes propagate consistently.

- A) Duplicate the fragments into each feature's prompt independently, updating every copy by hand whenever a rule changes.
- B) Modular prompts are the same thing as prompt caching, so introducing versioned fragments adds no real capability.
- C) Use modular, composable, versioned prompt fragments shared across features, distinct from caching or Skills packaging.
- D) Standardization across features isn't achievable through prompt design, only through a shared code library.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific holding from the correctly retrieved opinion.

- A) Trust the fluent, well-formatted output as evidence of correctness, since confident phrasing is itself a reliable quality signal.
- B) Apply defensive validation — verify extracted holdings against the source excerpt rather than trusting confident phrasing.
- C) Increase output length so there's more room for the response to be correct, on the theory that longer answers are more thorough.
- D) This is not something an architecture can address; it's purely a model limitation with no available mitigation at all.

**Question 28.** The team debates whether attorney-facing latency SLAs should factor into model-tier selection for the research platform.

- A) Yes — tier selection should weigh accuracy needs against latency/cost the SLA can tolerate, not default to maximum capability.
- B) Only cost should factor into tier selection, never latency, since attorneys never notice response time in a research tool.
- C) SLAs are a stakeholder-communication concern with no bearing on technical architecture or model-tier decisions at all.
- D) Latency should never factor into model or architecture decisions, regardless of what the attorney-facing SLA actually requires.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically in production, since a newer model version is always a fully deterministic, safe drop-in replacement.
- B) Pin the current version in production and evaluate the new one against the platform's own tests before deliberately upgrading.
- C) Upgrade immediately without testing, trusting that improved benchmark scores guarantee the same gains in production.
- D) Never upgrade models once the initial version is chosen, regardless of what future benchmark improvements show.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved opinion excerpts must fit alongside room for a detailed answer.

- A) Input and output token budgets are entirely independent of each other, so retrieved-content volume never affects room for the answer.
- B) This tradeoff only matters for very long opinions, never for typical queries with modest retrieved-content volume.
- C) Output length has no practical limit regardless of input size, so architects don't need to budget for it at all.
- D) Input and output share the same context-window budget, constraining retrieved content against room for an answer.

---

## Scenario C: Evaluation and A/B Testing of a Sales-Forecasting Copilot (Questions 31–45)

Quotient Analytics, a B2B software company, has had a Claude-powered sales-forecasting copilot in production for revenue teams for eight months. You are responsible for the evaluation strategy, A/B testing prompt and model changes, and diagnosing quality regressions.

---

**Question 31.** The team currently measures only forecast-adoption rate (how often reps accept the copilot's forecast) and hasn't defined targets for latency, cost, or safety.

- A) Latency and cost are operations concerns unrelated to evaluation design, so they don't need explicit targets from the eval strategy at all.
- B) Adoption rate alone is sufficient since it directly reflects the system's stated purpose better than any other single number could.
- C) Safety metrics are only relevant for regulated industries, not for an internal sales-forecasting copilot used by revenue teams.
- D) Define metrics spanning accuracy, latency, cost, and safety as first-class — adoption alone can look healthy while the system still fails.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past forecasting scenarios.

- A) A single automated method against a fixed labeled set is sufficient for any production evaluation need.
- B) Replace the automated checks entirely with only human review, dropping automation from the evaluation mix.
- C) Use mixed methodologies — automated eval for scale, human review for judgment, adversarial testing for safety paths.
- D) Expand the labeled set indefinitely, treating a bigger fixed set as the sole lever for improving evaluation.

**Question 33.** The team wants to test whether a new prompt version improves forecast quality before rolling it out to all revenue teams.

- A) Roll out the new prompt version to all revenue teams immediately, monitoring for problems only after the change is already live everywhere.
- B) Run an A/B test changing only the prompt version against a stable baseline, so the observed difference is attributable.
- C) Change the prompt and the underlying model tier at the same time, on the theory that stacking changes maximizes potential improvement.
- D) Skip testing entirely since prompt changes are inherently low-risk and never worth the delay of a controlled comparison.

**Question 34.** A forecast is materially wrong. Investigation shows the underlying pipeline data (historical deal velocity, quota attainment) was correctly retrieved, and the model's narrative summary misinterpreted the trend direction.

- A) This is a retrieval problem, so the fix belongs entirely in the data pipeline rather than anywhere in the generation step.
- B) This cannot be diagnosed at all without retraining the underlying model from scratch on new forecasting data.
- C) This is a generation-side issue — misinterpreting correctly retrieved data — calling for prompt or output-review fixes.
- D) This is a model mismatch requiring a different capability tier, regardless of what the specific failure actually was.

**Question 35.** Immediately after a scheduled CRM data-sync refresh, the copilot starts producing confident but incorrect quarterly forecasts, while model version and average latency are unchanged.

- A) Investigate the CRM-sync layer first, since the regression tracks the data-refresh event with model and latency unchanged.
- B) Suspect the model was silently updated by the provider, even though nothing about the release schedule points that way.
- C) Suspect a temperature setting change, since the forecasts read as more confident than before the refresh happened.
- D) Suspect the context window shrank somewhere in the pipeline, even though nothing else about the request size changed.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting forecast accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Accuracy should always be maximized regardless of what that does to cost or latency for the team's budget.
- B) Optimize cost, latency, and accuracy jointly against the SLA and budget — maximizing accuracy alone is also a loss.
- C) Cost, latency, and accuracy should each be optimized independently, without ever weighing one against another.
- D) This tradeoff cannot be measured at all, only guessed at, so there's no point trying to quantify it.

**Question 37.** Production monitoring currently reports only an overall weekly average forecast-accuracy score.

- A) Monitoring should surface a per-segment breakdown, since an aggregate average can hide a specific failing segment.
- B) A single aggregate weekly average is sufficient for production monitoring of a forecasting copilot at this scale.
- C) Weekly granularity is always sufficient regardless of how quickly a given segment's forecast quality is drifting.
- D) Monitoring should track only cost, since accuracy is already fully captured by the offline eval suite alone.

**Question 38.** The team proposes cutting human review of flagged low-confidence forecasts by 75%, citing a 96% aggregate accuracy score.

- A) Segment accuracy by product line and deal size before cutting review, since the aggregate figure can mask a weak segment.
- B) Proceed with the review cut based on the 96% aggregate figure alone, without checking any segment-level breakdown first.
- C) Aggregate accuracy is definitionally representative of every segment, so no further validation across segments is needed.
- D) Human review should never be reduced at all, regardless of what the measured accuracy figures eventually show.

**Question 39.** An A/B test shows a new prompt version improves forecast-adoption rate, but the team has not checked whether it also changed the rate at which the copilot overconfidently forecasts deals that later slip.

- A) Check the deal-slippage failure mode specifically before shipping, since an adoption-rate gain could mask it.
- B) Adoption rate alone is a sufficient signal to ship the change, without checking any other failure mode.
- C) Ship the change now and monitor informally afterward instead of testing for slippage beforehand.
- D) Deal-slippage failure behavior isn't something evaluation can measure, so it isn't worth testing for.

**Question 40.** The team wants to diagnose why a subset of forecasts are numerically accurate but rated poorly by reps in feedback surveys.

- A) Assume the accuracy metric itself is broken and discard it, without checking any other quality dimension first.
- B) Increase the model's capability tier, assuming higher capability always improves rep satisfaction regardless of what the surveys measure.
- C) Investigate a dimension beyond accuracy — explanation clarity, actionability, or tone — since the current eval misses it.
- D) Ignore rep satisfaction scores entirely in favor of the accuracy metric, since accuracy is the harder number to argue with.

**Question 41.** The team is optimizing token usage and notices the system sends full quarter-to-date deal history plus a large static forecasting-methodology document on every turn of a multi-turn coaching conversation.

- A) This has no optimization opportunity since the full deal history is always required on every turn regardless of length.
- B) Remove the static methodology document entirely from every turn to save tokens, dropping it from the conversation.
- C) Cache the static methodology document and trim or summarize older conversation turns to cut redundant token cost across the exchange.
- D) Switch to a smaller model as the only lever available for reducing token cost in this conversation.

**Question 42.** Logging captures every raw prompt and response for the production copilot, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy, since every event is technically captured somewhere.
- B) Redesign observability toward aggregable, sampled signals — tagged failure categories, quality metrics by segment.
- C) Reduce logging volume to save storage cost, without changing anything else about how the logs get reviewed.
- D) Observability requires no particular structure as long as the raw data is retained somewhere for later reference.

**Question 43.** The team wants to identify whether a recent forecast-quality regression was caused by a prompt change, a model-version change, or a CRM schema change — all three happened in the same release week.

- A) Assume the most recent change is always the cause, without isolating or re-testing any of the three changes.
- B) Test and roll out changes one variable at a time — with three simultaneous changes, isolate and re-test each independently.
- C) Revert all three changes without investigation, regardless of which one (if any) actually caused the regression.
- D) Attribution is impossible once multiple changes have shipped in the same release week, so don't bother trying to investigate further.

**Question 44.** An automated eval asserts that a forecast-narrative summary must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining, since correct behavior should be perfectly deterministic call to call.
- B) Exact-string-match evals are wrong for non-deterministic output — temperature introduces legitimate variation — check content instead.
- C) The reference string needs to be longer and cross-validated against a broader sample of acceptable outputs first.
- D) Temperature should be increased to fix the intermittent failures, since more randomness will smooth out the mismatch.

**Question 45.** Leadership wants a single number to represent "how good" the sales-forecasting copilot is, to track over time.

- A) Use adoption rate alone as the single number, since it's closest to the system's originally stated purpose.
- B) Refuse to provide any single summary metric under any circumstances, even as a rough top-line indicator leadership can track over time.
- C) A single aggregate metric is a useful top-line indicator, but should sit alongside segment-level detail.
- D) A single number is always achievable and sufficient for any system's evaluation needs, regardless of complexity.

---

## Scenario D: Lifecycle Management and Enablement for a Global Manufacturing Rollout (Questions 46–60)

Ferrum Industrial Group, a multinational manufacturer, is rolling out a Claude-powered production-quality assistant across plants in twelve countries and enabling a 200-person global engineering organization to use Claude Code. You are responsible for governance, regulatory alignment across jurisdictions, and lifecycle management for the rollout.

---

**Question 46.** The architecture team is finalizing data-residency, retention, and access-logging design in the final weeks before the first plant's go-live, after core application logic is already built.

- A) Cross-border data-residency and retention requirements can force costly structural retrofits late in a build.
- B) This sequencing carries no real risk, since compliance requirements can always be bolted on right before go-live.
- C) Compliance only affects legal documentation and contract language, never the system architecture itself.
- D) A single global data-residency standard applies uniformly, regardless of which country's plant is actually involved.

**Question 47.** A regional team proposes requiring human approval on every single output the production-quality assistant produces, framing it as the safest governance posture ahead of the multi-country rollout.

- A) Maximal human review on every output is always the correct default posture for a rollout at this scale and geography.
- B) Human reviewers are categorically less accurate than the model, which makes any review step counterproductive here.
- C) This blanket-review approach is required by ISO quality standards, regardless of what the actual error-cost analysis shows.
- D) Blanket review defeats much of the system's value; HITL should target high error-cost or judgment-heavy decisions.

**Question 48.** The production-quality assistant must identify and mitigate standard LLM risks — hallucination, prompt injection from freeform operator notes, and inconsistent output — as part of its design.

- A) These risks only need addressing once they've actually been observed happening in production somewhere.
- B) A single generic guardrail addresses hallucination, injection, and inconsistency equally well on its own.
- C) Design mitigations for each known failure mode up front — grounding, input isolation, and output validation.
- D) These risks apply only to consumer-facing products, never to an internal manufacturing quality assistant.

**Question 49.** Plant managers ask whether the assistant's quality-flagging decisions could produce disparate outcomes across different plants due to uneven historical sensor-data quality.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review after the system is already live.
- B) Disparate impact across plants is impossible in an LLM-based system, simply by virtue of how the model was built.
- C) This concern only applies to systems making a final shutdown decision, never to a system that only flags for review.
- D) Bias and fairness are architecture concerns — check whether eval data reflects each plant's actual sensor conditions.

**Question 50.** Across Ferrum's 200-person engineering organization, Claude Code usage is inconsistent — some teams have conventions applied automatically, others don't, and internal MCP server access varies by site.

- A) Have each engineer individually troubleshoot their own local configuration whenever something behaves inconsistently.
- B) Standardize CLAUDE.md hierarchy and shared MCP configuration at the team level so behavior doesn't depend on local setup.
- C) Restrict Claude Code usage to a single designated global team to reduce variance across the other 199 engineers.
- D) Accept the inconsistency as an unavoidable cost of AI tooling adoption across a 200-person distributed organization.

**Question 51.** Ferrum wants Claude Code-generated code changes to production-quality-assistant components to go through the same review rigor as any other change to a manufacturing safety-adjacent system.

- A) AI-assisted code should bypass standard review entirely, purely on the basis of having been written by a model.
- B) Only a spot-check of AI-generated code is necessary, given how much faster it was to produce than by hand.
- C) Standard SDLC practices still apply; Claude Code assisting doesn't reduce review rigor for a safety-adjacent system.
- D) Review requirements should be set lower for AI-generated code than for code an engineer wrote unassisted.

**Question 52.** A production incident at one plant traces back to a Claude Code-generated sensor-threshold change. The team can't immediately tell whether the bug is in the generated logic or in how the plant's control system integrated it.

- A) Assume the bug is in the generated code without any independent investigation or validation of how the integration layer handled it.
- B) Triage like any other incident — isolate whether the fault sits in the integration layer or the model output.
- C) Disable Claude Code across the entire engineering organization the moment any single incident is traced back to it.
- D) Roll back every recent Claude Code-assisted change across all twelve plants regardless of whether it's relevant.

**Question 53.** A regional engineering team wants a documented, repeatable workflow for a recurring task (generating a weekly cross-plant quality-variance report) versus a one-off exploratory investigation of an unfamiliar legacy module.

- A) Build both the recurring report and the one-off investigation as ad hoc, undocumented prompts each time.
- B) Recurring workflows and genuinely one-off exploratory tasks should always be built using the identical approach.
- C) Package the recurring report as a Skill for consistent reuse; leave the one-off task as a freeform session.
- D) Build both the recurring report and the one-off investigation as standing MCP servers regardless of reuse.

**Question 54.** Ferrum's compliance team wants documented evidence of who accessed which plant's production data through the assistant, and when, across all twelve countries.

- A) Access logging becomes optional once the system already has role-based permissions configured correctly.
- B) Only failed access attempts actually need to be logged, since a successful access was already authorized by definition.
- C) Design access control and audit logging as explicit architectural components satisfying identity and monitoring needs.
- D) Audit logging can be added later across all twelve countries without any impact on the architecture.

**Question 55.** The steering committee for the rollout includes plant-operations, legal/compliance, and engineering stakeholders across different countries, with different priorities and vocabularies.

- A) Tailor architectural communication to each audience so tradeoffs are framed in terms plant-operations and legal can each evaluate.
- B) Communicate only with the engineering stakeholders, trusting them to relay everything to operations and legal.
- C) Use identical technical documentation for all three audiences, regardless of their differing priorities.
- D) Skip stakeholder communication entirely until the rollout is fully complete across every one of the twelve plants.

**Question 56.** Midway through the rollout, requirements shift meaningfully after a new cross-border data-transfer regulation is issued affecting several plants.

- A) Refuse to incorporate the new regulation since the original requirements were already agreed upon by the committee.
- B) Incorporate the regulatory change silently into the design without informing any stakeholder of its actual impact.
- C) Treat this as normal lifecycle management — re-engage discovery, communicate the tradeoff, adjust design and timeline.
- D) Restart the entire multi-country rollout from scratch, regardless of how many plants the new regulation actually affects.

**Question 57.** After the first plant's go-live, the architect's involvement is discussed as ending at handoff to each plant's local operations team.

- A) Lifecycle management includes monitoring and iteration on production signal, not just discovery through handoff.
- B) This is the correct model; monitoring and iteration become entirely each plant's local operations team's job.
- C) Lifecycle responsibility ends the moment the rollout contract for the first plant's go-live is formally signed.
- D) Monitoring is only necessary if a major incident actually occurs at a given plant sometime after go-live.

**Question 58.** Documentation for the rollout currently lists final configuration values (model tier, retry settings, per-plant thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient, since the final "what" is all a future team would ever need.
- B) Documenting the reasoning is unnecessary overhead in a multi-country regulated environment like this one.
- C) Only the original architect should ever be allowed to modify the system, which makes documentation moot anyway.
- D) Documentation should also capture the "why" behind key decisions — regulatory drivers and tradeoff reasoning per jurisdiction.

**Question 59.** Engineering leads across several plants want Claude Code to help with routine tasks (drafting maintenance documentation, exploring an unfamiliar legacy module) but are unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves meaningful time on every task category without checking any of them.
- B) Ban Claude Code for all documentation tasks across every plant without first evaluating where it might actually help.
- C) Mandate Claude Code usage for every task category regardless of whether it measurably saves any time at all.
- D) Evaluate specific task categories for genuine friction reduction versus cases where review overhead exceeds it.

**Question 60.** A recurring operational issue is that engineers at different plants debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency across plants, with no architectural fix worth pursuing.
- B) Document the shared triage process as reusable operational knowledge, reducing redundant re-derivation across plants.
- C) Restrict all debugging of Claude Code integration failures to a single designated engineer company-wide.
- D) The issue can only be resolved by switching the entire engineering organization to a different tool.

---
# Answer Key — Practice Exam 2

**Quick key:** 1-B, 2-D, 3-C, 4-C, 5-A, 6-A, 7-D, 8-A, 9-B, 10-A, 11-D, 12-B, 13-A, 14-D, 15-D, 16-C, 17-B, 18-A, 19-C, 20-D, 21-D, 22-D, 23-B, 24-D, 25-A, 26-C, 27-B, 28-A, 29-B, 30-D, 31-D, 32-C, 33-B, 34-C, 35-A, 36-B, 37-A, 38-A, 39-A, 40-C, 41-C, 42-B, 43-B, 44-B, 45-C, 46-A, 47-D, 48-C, 49-D, 50-B, 51-C, 52-B, 53-C, 54-C, 55-A, 56-C, 57-A, 58-D, 59-D, 60-B

---

**1. B** — The stated goal (more volume, same headcount, same cycle time) is a throughput/efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A wrongly insists transformation applies regardless of what discovery found; C locks onto cost despite that not being the surfaced goal; D defers the framing question entirely.

**2. D** — A predetermined sequence identical for every case, regardless of shipment specifics, is the defining case for a fixed workflow. A wrongly claims autonomy is warranted for a sequence that never varies; B undersells the multi-step nature of the task; C treats two non-interchangeable patterns as equivalent.

**3. C** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. A and D sacrifice these properties for a shortcut; B discards the specialization that motivated separate subagents in the first place.

**4. C** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. A and B withhold the reasoning stakeholders need; D removes a deliberate, justified difference for false consistency.

**5. A** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. B, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. A** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. B and C treat it as out of scope; D overreacts to sentiment alone without weighing it against the documented technical case.

**7. D** — Every subagent succeeding while whole shipment categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, B, and C all patch downstream instead of fixing the actual scope gap.

**8. A** — Adding a feedback loop that captures dispatcher overrides and outcomes as a first-class architectural component is what lets the system improve after deployment. B, C, and D all treat a first-class architectural component as optional or someone else's problem.

**9. B** — A single call enhanced with tool access, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and C over-engineer a simple augmentation need; D is factually wrong.

**10. A** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just writing around it. B and C ignore this real degradation; D doesn't address selection reliability at all.

**11. D** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (carrier-rate lookup) completes, reducing latency without sacrificing correctness. A and C misstate real constraints; B avoids the sequencing question rather than answering it.

**12. B** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; C is too much of the wrong kind of detail; D skips the communication need entirely.

**13. A** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. B, C, and D understate or deny this real architectural tradeoff.

**14. D** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A wastes effort guessing at undefined requirements; B blocks current delivery unnecessarily; C ignores a known future need entirely.

**15. D** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, B, and C all leave the actual knowledge transfer gap unaddressed.

**16. C** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and B ignore fit-to-task; D sacrifices quality on the cases that need capability most.

**17. B** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, C, and D all misstate or break the caching opportunity.

**18. A** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. B and D ignore this mismatch; C discards useful structured data.

**19. C** — Matching retrieval mechanism to query pattern — metadata/field filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and D force one mechanism onto queries it doesn't fit; B denies a real, consequential distinction.

**20. D** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, B, and C all reintroduce the failure mode the fix is meant to prevent.

**21. D** — Presenting both figures with attribution and the likely explanation (a circuit split) preserves the actual information for the attorney rather than resolving a real disagreement arbitrarily. A, B, and C all discard or obscure a genuine conflict in the sources.

**22. D** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and C are workarounds for a structurally solvable problem; B doesn't address the preamble at all.

**23. B** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. A, C, and D all fail the reuse or maintainability requirement.

**24. D** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. A and B ignore the real context cost of the monolithic approach; C removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-opinion synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. C** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; B conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. B** — Verifying extracted holdings against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; C doesn't address correctness; D incorrectly claims no architectural mitigation exists.

**28. A** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. B, C, and D each drop a relevant factor from the decision.

**29. B** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and C assume benchmark gains transfer automatically and that new releases behave identically to old ones; D over-corrects into permanent stagnation.

**30. D** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and C all misstate this real, architecture-relevant constraint.

**31. D** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if adoption looks healthy. A, B, and C each drop a dimension that materially affects whether the system is actually working well.

**32. C** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. A, B, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. B** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; C confounds two variables; D dismisses a real risk without evidence.

**34. C** — Correct pipeline retrieval plus a misinterpreted trend direction is a generation-side issue, calling for prompt or output-review fixes rather than pipeline or model-tier changes. A and D misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. A** — A regression tied specifically to a data-refresh event, with model and latency unchanged, points first at the data pipeline/CRM-sync layer. B, C, and D would not specifically correlate with a scheduled data refresh.

**36. B** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and C optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and C accept a monitoring blind spot; D drops accuracy monitoring from observability entirely.

**38. A** — Segmenting accuracy by product line and deal size before cutting review protects against a failing segment hiding behind a healthy aggregate. B and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. A** — An isolated adoption-rate improvement could mask a worsened deal-slippage failure mode; checking specifically for that before shipping is the correct diagnostic step. B and C ship without adequate testing; D incorrectly claims the failure mode is unmeasurable.

**40. C** — "Accurate but poorly rated" points at an unmeasured quality dimension (explanation clarity, actionability, tone) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; B assumes a capability-tier fix without diagnosing what the surveys are actually measuring.

**41. C** — Caching the static methodology document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; B removes needed content; D is a blunt, quality-risking lever when a more targeted fix is available.

**42. B** — Aggregable, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and D accept the described dysfunction; C addresses cost, not the actual observability gap.

**43. B** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and C guess without evidence; D gives up on a solvable (if effortful) diagnostic problem.

**44. B** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose ordinary sampling variation as broken model behavior; C doesn't address the actual mismatch between eval design and output variability.

**45. C** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and D oversimplify to a single lossy number; B refuses a reasonable, common stakeholder request.

**46. A** — Cross-border data-residency and retention requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. B and C understate real architectural impact; D wrongly assumes a single uniform standard applies across every jurisdiction.

**47. D** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal safety case for maximal review; C misattributes this requirement to a standard that doesn't actually mandate it.

**48. C** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; B assumes one guardrail covers distinct risk types; D is factually wrong.

**49. D** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness across plants, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; B and C make unsupported blanket claims.

**50. B** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. A and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the organization.

**51. C** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a safety-adjacent system. A, B, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for this context.

**52. B** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and D skip diagnosis; C is a disproportionate reaction that doesn't investigate the actual cause.

**53. C** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; B ignores that reuse profile should drive the choice; D over-engineers the one-off task.

**54. C** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and D each understate what compliance-grade audit evidence actually requires across jurisdictions.

**55. A** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by plant-operations, legal, and engineering audiences alike. B, C, and D each fail to serve at least one audience's real information need.

**56. C** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and B mishandle a real change; D disproportionately discards unaffected work.

**57. A** — Lifecycle management extends through monitoring and iteration based on production signal, not just through discovery and handoff. B, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. D** — Capturing the "why" (regulatory drivers, tradeoff reasoning per jurisdiction) alongside the "what" is what lets a future team safely extend the system across a multi-country deployment. A, B, and C all leave that reasoning undocumented and effectively lost.

**59. D** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and C over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 2.*
