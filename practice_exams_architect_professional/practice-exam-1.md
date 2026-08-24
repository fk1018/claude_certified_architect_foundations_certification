# CCARP Practice Exam 1

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer and multiple-response practice set — most items have one correct answer and three distractors; a few state how many responses to select. |
| Scenarios | 4 (Multi-Agent Claims Architecture, Financial Research Model/RAG Integration, Support-Deflection Evaluation & Optimization, Healthcare Governance & Team Enablement) |
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

## Scenario A: Multi-Agent Claims-Processing Architecture (Questions 1–15)

An insurance client wants to modernize claims intake, triage, and initial adjudication. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with the client's stakeholders.

---

**Question 1.** Discovery reveals the client's actual goal is processing 3x current claim volume with the same staffing, at the same average cycle time — not new capabilities the current process lacks.

- A) Frame the architecture around transformation, since introducing an AI system into a business process is inherently transformative regardless of what discovery found.
- B) Frame the architecture around efficiency, and build success metrics around throughput per headcount rather than novel capability.
- C) Frame the architecture around cost reduction exclusively, since headcount-neutral volume growth is really a cost story regardless of what discovery surfaced.
- D) Skip framing around a specific value pillar, and let the steering committee infer the intended benefit once the system is in production.

**Question 2.** Claims intake, triage, and adjudication each require different steps depending on the claim type, prior findings, and missing information discovered along the way.

- A) An agentic pattern, since the right sequence of steps varies by case and depends on findings discovered along the way, not a route fixed in advance.
- B) A fixed workflow, since claims processing is a well-established business process with steps that don't need to vary case by case.
- C) An augmented LLM pattern with retrieval and tools, since a single enhanced call handles the reasoning this insurance workflow needs.
- D) Whichever pattern the team can implement fastest, since the three patterns are functionally interchangeable once tools are wired up.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (document intake, fraud-signal analysis, coverage lookup, adjudication recommendation).

- A) Let each subagent communicate results directly to whichever subagent needs them next, skipping the coordinator's structured routing entirely to minimize hops.
- B) Merge all four responsibilities into a single subagent so there's no inter-subagent communication to design at all.
- C) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow.
- D) Let subagents talk to each other directly, but add logging on the side so the traffic can be reviewed after the fact.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition assigned only auto-claims to the pipeline — claims involving injury or third-party liability are never routed to any subagent and silently fall through.

- A) Add a fifth subagent dedicated to edge cases, without changing how the coordinator currently assigns claim categories to the pipeline.
- B) Add a prompt instruction telling each subagent to flag any claim it doesn't recognize as its own, so the gap surfaces somewhere downstream in the pipeline.
- C) Give the existing four subagents broader tool access so any of them can pick up injury or liability claims if one happens to reach them.
- D) Fix the coordinator's decomposition so it explicitly covers all claim categories, including injury and liability claims, rather than tuning the existing subagents.

**Question 5.** The design must align technical architecture to a specific business value pillar the client actually cares about, distinct from a generic "we added AI" narrative.

- A) Any AI system inherently demonstrates transformation on its own, so no additional pillar-framing exercise is needed before architecture begins.
- B) Business value pillars are a sales and marketing concern, not something that should influence technical architecture decisions.
- C) Efficiency, transformation, productivity, cost, and performance SLAs are examples of pillars that should drive the architecture and its success metrics.
- D) The pillar should be chosen after the system ships, based on whichever benefit turns out to be easiest to measure in hindsight.

**Question 6.** The client's claims adjuster team is skeptical of automation and worried about job security; discovery interviews surface this repeatedly.

- A) Ignore the sentiment in the architecture discussion, since job-security concerns aren't a technical requirement the system needs to satisfy.
- B) Treat it as a real implicit constraint alongside the explicit requirements — it shapes adoption, rollout sequencing, and HITL checkpoints.
- C) Proceed with the technical design exactly as scoped, and hand the sentiment entirely to a separate change-management workstream with no influence on the architecture itself.
- D) Recommend against the project entirely, since adjuster sentiment this strong during discovery usually means the deployment can't succeed.

**Question 7.** A stakeholder asks why the fraud-signal subagent uses a higher-capability, higher-cost model tier than the document-intake subagent.

- A) "Higher tier because it's more important" is a sufficient answer, since stakeholders will accept a confidence-based justification without more detail.
- B) Avoid explaining tier differences at all, since stakeholders don't need or want technical detail about model selection.
- C) Explain the tradeoff: fraud-signal analysis needs deeper reasoning that justifies the added cost and latency, while document intake is simpler.
- D) Use the same tier everywhere for simplicity, regardless of how much reasoning depth each subagent's task actually requires.

**Question 8.** The architecture's current design produces a final adjudication recommendation with no mechanism to learn from adjuster overrides or outcomes over time.

- A) Add a feedback loop capturing adjuster overrides and outcomes as a first-class architectural component.
- B) This is acceptable as-is, since the initial design already reflects best practice and doesn't need a mechanism to learn from outcomes.
- C) Feedback loops are a data science concern unrelated to the architecture the coordinator and subagents were designed around.
- D) Defer any feedback mechanism to a hypothetical future phase, with no hooks or data capture built into the current design.

**Question 9.** The client wants a single enhanced LLM call — with retrieval of policy documents — to answer straightforward coverage questions, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture with a coordinator and specialized subagents, complete with a structured escalation path, regardless of how simple the underlying coverage question is.
- B) This cannot be built with Claude at all, since answering coverage questions with retrieval requires an autonomous agent loop.
- C) This requires a fixed workflow with at least five sequential steps to reliably answer a straightforward coverage question.
- D) An augmented LLM pattern — a single call enhanced with retrieval and tools — fits this simpler augmentation need without the overhead of multi-step agentic orchestration.

**Question 10.** The document-intake subagent's toolset has grown to include tools for tasks like customer notification and billing lookup that are unrelated to document intake.

- A) This has no architectural downside as long as the subagent's system prompt is written carefully enough to describe every tool's intended use.
- B) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or moved to a more appropriate subagent.
- C) More tools always improve a subagent's flexibility, so customer notification and billing lookup should be encouraged rather than trimmed.
- D) The fix is to increase the subagent's context window so it can hold instructions for all of its tools without losing track of any of them.

**Question 11.** The coordinator currently processes each claim sequentially through document intake, fraud analysis, coverage lookup, and adjudication, even though fraud analysis and coverage lookup have no dependency on each other's output.

- A) Run fraud analysis and coverage lookup as independent, parallel subagent calls once document intake completes, rather than processing them sequentially.
- B) Sequential processing end-to-end is required for auditability, since parallel subagent calls can't be logged in a single, deterministic causal order for a claims audit trail.
- C) Parallelization of subagent calls is not possible within a coordinator/subagent architecture, regardless of whether the calls are independent.
- D) Combine fraud analysis and coverage lookup into a single subagent so the sequencing question about their independent outputs never comes up.

**Question 12.** The client asks how end-to-end architecture should be described at a high level for a steering committee unfamiliar with the technical details.

- A) Present only the model names and token costs involved, since that's the information a steering committee cares most about evaluating.
- B) Present the full technical architecture diagram, including subagent boundaries, tool wiring, and the exact system prompt text, with no simplification for a non-technical audience.
- C) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes.
- D) Skip a high-level description entirely and go directly into a live implementation demo of the coordinator and subagents.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (document processing, fraud detection, coverage lookup, adjudication) rather than a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows, since it avoids the coordination overhead of routing between specialized subagents.
- B) Specialized subagents are strictly a cost-increasing choice with no reliability benefit over a single agent holding every tool.
- C) There's no meaningful architectural difference between a single generalist agent and a coordinator with specialized subagents.
- D) A single agent holding every tool is more likely to suffer degraded tool-selection reliability than specialized, narrowly-scoped subagents.

**Question 14.** The claims architecture must eventually support a new claim type (parametric weather claims) the client is planning to launch next year, but detailed requirements aren't available yet.

- A) Ignore future claim types entirely until detailed parametric weather claim requirements exist and are handed to the architecture team.
- B) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.
- C) Build full support for parametric weather claims now, guessing at adjudication rules, data sources, and payout logic the client hasn't specified yet.
- D) Refuse to proceed with the current phase of the project until the future parametric weather claim requirements are fully finalized and signed off.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values — model tiers, thresholds, retry settings — since a well-organized implementation is self-explanatory to a new team.
- B) Document the architecture and the reasoning behind key decisions — pattern choices, decomposition, tier selections — not just the final values.
- C) Rely on the original architect remaining available indefinitely to answer questions instead of writing anything down.
- D) Documentation is unnecessary if the code and configuration are well-organized enough for a new team to infer the reasoning themselves.

---

## Scenario B: Model, Prompting, and RAG Integration for a Financial Research Platform (Questions 16–30)

A financial research platform wants Claude to answer analyst questions using both general reasoning and retrieval over a large, constantly-updated corpus of filings, earnings transcripts, and internal research notes. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most analyst questions are moderately complex; a small fraction require deep multi-step reasoning across many documents, and a small fraction are simple lookups.

- A) Use one fixed model tier for every question, regardless of whether it's a simple lookup or a deep multi-step reasoning task.
- B) Always use the highest-capability tier for every question, to guarantee quality even on the simplest lookups.
- C) Route based on task difficulty — a fast tier for simple lookups, a balanced tier for typical questions, and a higher-capability tier for deep multi-step cases.
- D) Always use the fastest, cheapest tier for every question, accepting quality loss on the small fraction that need deep reasoning.

**Question 17.** Every request sends the same long system prompt (analyst persona, citation requirements, formatting rules) followed by retrieved document excerpts that vary per query.

- A) Order doesn't affect cost or latency for this use case, since the total token count is the same regardless of prompt structure.
- B) Alternate system instructions and retrieved content throughout the prompt so the model sees both together at each stage.
- C) Put retrieved content first since it's most relevant to the specific query, ahead of the stable system prompt.
- D) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it.

**Question 18.** The corpus mixes long-form filings (10-Ks, earnings call transcripts) with short structured data (a table of quarterly metrics).

- A) Define one rigid schema and chunking strategy tuned for long-form documents, and force the short structured quarterly-metrics table into the same shape.
- B) Chunking and indexing strategy should match each data shape — long-form documents need different chunking than short structured records.
- C) Structured data like the quarterly-metrics table should be excluded from retrieval entirely, since it doesn't fit a document-chunking pipeline.
- D) Use the largest possible chunk size for everything, long-form and structured alike, to avoid needing more than one strategy.

**Question 19.** Analyst queries range from exact lookups ("Q3 2026 revenue for Company X") to conceptual questions ("how has Company X's margin narrative evolved over the last four quarters").

- A) Use only embedding similarity search for every query type, from exact revenue lookups to open-ended narrative questions.
- B) Use only structured and metadata filtering for every query type, including open-ended conceptual questions about margin narrative.
- C) Match retrieval strategy to query pattern: structured/metadata filtering for lookups, embedding similarity for conceptual questions, hybrid where needed.
- D) Query pattern doesn't meaningfully affect which retrieval approach is appropriate, since embeddings can approximate any structured lookup given enough retrieved chunks.

**Question 20.** Analysts need citations that reliably map each claim to a specific source document and page/section, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without any structure enforcing where the citation actually comes from.
- B) Require structured output pairing each claim with its source (document, section, excerpt) rather than reconstructing citations from memory.
- C) Add citations after the fact by searching for a plausible source document for each claim once the response is already drafted.
- D) Append a general bibliography of consulted documents at the end of each response, without mapping specific claims to specific sources.

**Question 21.** Two retrieved sources disagree on a company's reported Q3 revenue by a small margin — likely different reporting bases (GAAP vs. non-GAAP).

- A) Average the two reported figures and present the blended number as the company's Q3 revenue, without flagging that the sources disagree.
- B) Omit the revenue figure from the response entirely, since the two retrieved sources disagree by a small margin.
- C) Always prefer whichever source was retrieved first in the search results, regardless of which reporting basis it uses.
- D) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely methodological explanation.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the JSON-only instruction more emphatically in the prompt, adding extra emphasis words like "strictly" and "only" each time.
- B) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.
- C) Post-process every response to strip any leading text before the first "{" character, which doesn't actually validate that what remains still matches the intended schema.
- D) Increase max_tokens so there's room for both the conversational preamble and the full JSON payload in the same response.

**Question 23.** The platform needs to connect to a proprietary internal research-notes system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this research platform.

- A) Hard-code the research-notes integration directly into this platform's application code, without exposing it to any other Claude-powered tool.
- B) Paste the entire research-notes corpus into every prompt across every internal Claude-powered tool that needs to reference it.
- C) Build an MCP server exposing the research-notes operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- D) Require each consuming tool to reimplement its own research-notes integration independently, rather than sharing a common interface.

**Question 24.** The team is deciding between exposing the full research-notes catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Progressive discovery — querying a catalog resource as needed — scales better than loading the entire catalog into context up front.
- B) Loading the full catalog into every prompt up front is always preferable for completeness, regardless of how large the catalog grows.
- C) There's no meaningful difference in context cost between querying a catalog on demand and loading the entire catalog up front.
- D) The catalog should never be exposed to the agent in any form, structured or otherwise, to avoid any context cost at all.

**Question 25.** An analyst asks a chain-of-thought-friendly question requiring the model to reason step by step across several retrieved documents before concluding.

- A) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-document synthesis question.
- B) Zero-shot prompting with no reasoning guidance is always equally effective as chain-of-thought for multi-document synthesis questions.
- C) Chain-of-thought prompting is only useful for coding tasks, not for financial-document reasoning across several sources.
- D) The model cannot reason across multiple retrieved documents regardless of prompting approach, since each document is processed independently.

**Question 26.** The platform wants to standardize prompt fragments (citation format, disclaimer language, formatting rules) across several different analyst-facing features so changes propagate consistently.

- A) Use modular, versioned prompt fragments shared across features — distinct from caching (cost/latency) or Skills (capability packaging).
- B) Duplicate the citation format, disclaimer language, and formatting rules directly inside each feature's system prompt independently, and update every copy by hand whenever a rule changes.
- C) Modular prompts are the same mechanism as prompt caching, so enabling caching already solves the standardization problem.
- D) Standardization of shared language across features isn't achievable through prompt design at all, only through post-processing.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific figure from the correctly retrieved source document.

- A) Trust the fluent, well-formatted, confidently-cited output as sufficient evidence that the figure it states is correct.
- B) This is not something an architecture can address; it's purely a model limitation with no available mitigation.
- C) Increase output length so the response has more room to state the figure correctly the next time.
- D) Apply defensive verification — check extracted figures against the actual source excerpt before trusting the phrasing.

**Question 28.** The team debates whether analyst-facing latency SLAs should factor into model tier selection for the research platform.

- A) Latency should never factor into model or architecture decisions, regardless of what the analyst-facing SLA actually requires.
- B) Yes — weigh accuracy needs against the latency and cost the use case's SLA can tolerate, rather than defaulting to the most capable tier.
- C) Only cost should factor into tier selection; latency has no bearing on which model tier is appropriate for the research platform.
- D) SLAs are purely a stakeholder-communication concern with no bearing on the technical architecture or model selection.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to "latest" automatically in production, since a newer, presumably more deterministic model with better benchmark scores is always an improvement in practice.
- B) Never upgrade the model once the initial version is chosen, regardless of how much better later versions test on the platform's own evaluation suite.
- C) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading.
- D) Upgrade to the new version immediately without testing, since improved benchmark scores guarantee an improvement in this platform's production behavior.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved document excerpts must fit alongside room for a detailed answer.

- A) Input and output token budgets are entirely independent of each other, regardless of how much structured retrieval content occupies the input side.
- B) This tradeoff only matters for unusually long documents like full 10-Ks, never for typical analyst queries with shorter excerpts.
- C) Output length has no practical limit regardless of how much retrieved content and system-prompt overhead the input side consumes.
- D) Input and output share the same context-window budget, so retrieved-content volume must be balanced against room for a detailed answer.
---

## Scenario C: Evaluation and Optimization of a Production Support-Deflection System (Questions 31–45)

A Claude-powered system answers customer questions directly to deflect support tickets. It's been in production for six months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only ticket-deflection rate and hasn't defined targets for latency, cost, or safety.

- A) Deflection rate alone is sufficient, since it's the system's stated primary purpose and the other dimensions are secondary concerns best left to operations once the number looks healthy.
- B) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics.
- C) Latency and cost are operations concerns unrelated to evaluation design, and shouldn't be part of the eval strategy itself.
- D) Safety metrics are only relevant for regulated industries, not for a general customer-support deflection system like this one.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past questions.

- A) Use mixed methodologies — automated eval for scale, human review for judgment calls, and adversarial testing for safety-relevant paths.
- B) A single automated method against a fixed labeled set is sufficient for any production system, regardless of how nuanced its failure modes are.
- C) Replace the automated checks entirely with only human review, since human judgment is strictly more reliable than any automated metric.
- D) Expand the labeled set of past questions indefinitely, using that as the sole lever for improving evaluation coverage over time.

**Question 33.** The team wants to test whether a new prompt version improves deflection quality before rolling it out to all traffic.

- A) Roll out the new prompt version to all traffic immediately and monitor deflection rate informally for problems afterward.
- B) Change the prompt version and the model tier at the same time, to maximize the chance of a measurable improvement showing up in one test.
- C) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.
- D) Skip testing entirely, since prompt changes are inherently low-risk and don't need to be validated before a full rollout.

**Question 34.** A support answer is factually wrong. Investigation shows the underlying knowledge-base article was correct and retrieved properly, and the model's response paraphrased it inaccurately.

- A) This is a retrieval problem; fix the indexing pipeline even though the correct article was already retrieved successfully.
- B) This cannot be diagnosed at all without retraining the underlying model on more paraphrase examples.
- C) This is a model mismatch requiring a different, higher-capability model tier regardless of what the specific failure actually was.
- D) This is best characterized as a prompt/generation issue, calling for prompt or output-validation fixes rather than retrieval changes.

**Question 35.** Immediately after a scheduled knowledge-base refresh, the system starts returning confident but incorrect answers, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider, even though the model version field hasn't changed since before the refresh.
- B) Investigate the retrieval/indexing layer first, since the regression tracks the data refresh event with model and latency unchanged.
- C) Suspect a temperature setting change, since the answers now sound more confident and less validated than before the refresh.
- D) Suspect the context window shrank, even though nothing in the deployment changed the model's configured context length.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another, without weighing them against each other.
- B) Accuracy should always be maximized regardless of cost or latency implications, since correctness matters more than efficiency.
- C) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget, rather than maximizing any one dimension alone.
- D) This tradeoff cannot be measured with any confidence and can only be guessed at without a full model retraining cycle.

**Question 37.** Production monitoring currently reports only an overall weekly average accuracy score.

- A) A single aggregate weekly average is sufficient for production monitoring, since it reflects overall system health well enough without a structured, per-topic breakdown every week.
- B) Monitoring should track only cost, since accuracy is already fully captured by the offline eval suite alone.
- C) Weekly granularity is always sufficient for production monitoring, regardless of how the underlying system actually behaves.
- D) Monitoring should surface drift and outliers — a per-topic or per-query-type breakdown — since an aggregate average can hide a failing segment.

**Question 38.** The team proposes cutting human review of flagged low-confidence answers by 80%, citing a 97% aggregate accuracy score.

- A) Proceed with the 80% cut based on the 97% aggregate accuracy figure alone, without checking whether it holds across every topic and query type.
- B) Segment accuracy by topic and query type before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.
- C) Aggregate accuracy is definitionally representative of every segment, so no further breakdown is needed before changing review coverage.
- D) Human review of flagged low-confidence answers should never be reduced, regardless of how strong the measured aggregate accuracy is.

**Question 39.** An A/B test shows a new prompt version improves deflection rate but the team has not checked whether it also changed the false-positive rate on genuinely complex questions that should escalate to a human.

- A) Deflection rate alone is a sufficient signal to ship the new prompt version, since it directly measures the system's core stated purpose.
- B) Check the escalation-related failure mode specifically before shipping, since an isolated deflection-rate gain could mask an increase in inappropriate deflections.
- C) False-positive escalation behavior on complex questions is not something the evaluation strategy can measure before a full production rollout.
- D) Ship the change and monitor deflection and escalation informally after the fact, instead of testing the escalation impact beforehand.

**Question 40.** The team wants to diagnose why a subset of answers are technically accurate but rated poorly by customers in satisfaction surveys.

- A) Assume the accuracy metric itself is broken and discard it, since it's reporting correctness on answers customers rate poorly.
- B) Increase the model's capability tier across the board, assuming higher capability always improves customer satisfaction scores.
- C) Investigate a dimension beyond factual accuracy — tone, completeness, or actionability — since accuracy alone doesn't explain the poor rating.
- D) Ignore the customer satisfaction survey scores entirely in favor of the accuracy metric the eval suite already reports.

**Question 41.** The team is optimizing token usage and notices the system sends full conversation history plus a large static policy document on every turn of multi-turn conversations.

- A) This has no optimization opportunity, since sending the full conversation history and the static policy document on every turn is always required.
- B) Switch to a smaller model as the only lever for reducing token cost, without changing what's sent on each turn of the conversation.
- C) Remove the static policy document entirely from every turn to save tokens, even though it's needed for the system's answers to stay compliant.
- D) Apply prompt caching to the static policy document and trim or summarize older conversation turns, rather than a blunt lever like raising temperature.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging of every prompt and response at full volume is itself a sufficient observability strategy for identifying emerging failure patterns.
- B) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment.
- C) Reduce logging volume to save storage cost, without changing anything else about how the logs are structured or reviewed.
- D) Observability requires no particular structure as long as the raw prompt/response data is retained somewhere for long enough.

**Question 43.** The team wants to identify whether a specific quality regression was caused by a recent prompt change, a recent model version change, or a knowledge-base content change — all three happened in the same week.

- A) Assume the most recent of the three changes is always the cause of the regression, without testing the other two changes.
- B) Attribution is impossible once multiple changes have shipped in the same week, so the regression should be accepted as unexplained.
- C) Test and roll out changes one variable at a time; with three simultaneous changes, isolate and re-test each independently rather than guessing.
- D) Revert all three changes without investigation, regardless of which one, if any, actually caused the regression.

**Question 44.** An automated eval asserts that a summarization output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning on this summarization task; the failure invalidates its current release and it needs retraining.
- B) Exact-string-match evals are the wrong tool for non-deterministic output; check for required content and structure instead of an exact match.
- C) The reference string needs to be longer so there's more surface area for an exact match to eventually succeed.
- D) Temperature should be increased to fix the intermittent failures, since more randomness should make the matches more consistent.

**Question 45.** Leadership wants a single number to represent "how good" the support-deflection system is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs, without any structured segment-level detail underneath it.
- B) Use deflection rate alone as the single number, since it's the system's stated primary purpose and the easiest figure to report.
- C) Refuse to provide any single summary metric under any circumstances, even when leadership needs one figure to track over time.
- D) A single aggregate metric is a useful top-line indicator, but should sit alongside segment-level and multi-dimensional detail.
---

## Scenario D: Governance, Compliance, and Team Enablement for a Healthcare Deployment (Questions 46–60)

A healthcare client is deploying a Claude-powered system that processes patient intake information and assists a 30-person clinical operations team using Claude Code internally. You are responsible for governance, regulatory compliance, and developer enablement for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) This sequencing carries no meaningful risk, since compliance requirements can always be layered on cleanly right before a healthcare system launch.
- B) HIPAA-driven residency, retention, and access-control requirements can force structural changes costlier to retrofit than to design in from the start.
- C) Compliance only affects legal documentation and contract language, not the system's actual technical architecture or data flows.
- D) FedRAMP, not HIPAA, is the relevant regulatory regime for a healthcare client processing patient intake information.

**Question 47.** A team proposes requiring human approval on every single output the patient-intake system produces, framing it as the safest governance posture.

- A) Maximal human review on every single output is always the correct default posture for healthcare AI systems, regardless of how low-stakes the specific decision is.
- B) Human reviewers are categorically less accurate than the model on every decision type, which makes universal review counterproductive by definition.
- C) Blanket human-in-the-loop on every output defeats much of the system's value; target HITL at high error-cost or judgment-requiring decisions.
- D) This blanket-review approach is required by GDPR regardless of what HIPAA or other applicable regulations actually specify for this deployment.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from patient-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed once they're actually observed happening in production, not as part of the initial system design.
- B) Hallucination, prompt injection, and inconsistent output are risks exclusive to non-healthcare use cases and don't meaningfully apply here.
- C) A single generic guardrail, applied uniformly across the system, addresses hallucination, prompt injection, and inconsistent output equally well.
- D) Design mitigations for each known failure mode up front — grounding for hallucination, isolation for injection, consistency checks for output.

**Question 49.** The clinical operations team asks whether the system's decisions could produce disparate outcomes across different patient demographics.

- A) This is not an architectural concern at all; it belongs entirely to legal and compliance review after the system has already launched.
- B) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population.
- C) Disparate impact across patient demographics is impossible in an LLM-based system by construction, regardless of the underlying training data.
- D) This concern only applies to systems making final clinical decisions outright, not to any assistive system that merely supports staff.

**Question 50.** The 30-person clinical operations team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.
- B) Have each of the 30 staff members individually troubleshoot and configure their own local Claude Code setup as issues come up, without any shared team-level configuration to fall back on.
- C) Restrict Claude Code usage to a single designated engineer on the team to reduce configuration variance across machines.
- D) Accept the inconsistency in conventions and MCP access as an unavoidable cost of rolling out AI tooling across a 30-person team.

**Question 51.** The team wants Claude Code-generated code changes in this healthcare context to go through the same review rigor as any other change to a regulated system.

- A) AI-assisted code should bypass standard review, since Claude Code output is already validated by the model that generated it.
- B) Only a spot-check of AI-generated code is necessary, since a full review adds redundant overhead on top of whatever checks the model already performed during generation.
- C) Standard SDLC practices — review, testing, version control — still apply; Claude Code assisting doesn't reduce required review rigor.
- D) Review requirements should be lower for AI-generated code than for human-written code, since the model's output is more consistent.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code itself without investigating the surrounding integration layer at all.
- B) Disable Claude Code for the team entirely following any incident, regardless of whether the tool was actually the root cause.
- C) Roll back all recent Claude Code-assisted changes regardless of relevance to the specific data-handling bug that caused the incident.
- D) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output.

**Question 53.** The clinical operations team wants a documented, repeatable workflow for a recurring task (generating a weekly compliance summary report) versus a one-off exploratory coding task.

- A) Build both the recurring compliance-report workflow and the one-off exploratory task as ad hoc, undocumented prompts each time either one is needed.
- B) Package the recurring report workflow as a Skill for consistent reuse; leave the one-off task as an unstructured session.
- C) Build both the recurring report and the one-off exploratory task as MCP servers, regardless of how often either one is actually reused.
- D) Recurring, well-defined workflows and one-off exploratory tasks should always be built with identical tooling and structure.

**Question 54.** The compliance team wants documented evidence of who accessed what patient-related data through the system and when.

- A) Access logging is optional if the system already has role-based permissions configured, since permissions alone already establish who is accountable for each action.
- B) Audit logging can be added later, after launch, without any architectural impact on how the system currently handles patient data access.
- C) Design access-control and audit-logging as explicit architectural components, not an implicit byproduct of normal operation.
- D) Only failed access attempts need to be logged, since successful, authorized access doesn't need to be part of the audit trail.

**Question 55.** The steering committee for this deployment includes clinical, legal, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders on the steering committee, since they'll relay the relevant information to clinical and legal.
- B) Skip stakeholder communication entirely until the system is fully built and ready for a single comprehensive demo.
- C) Use identical technical documentation for all three audiences — clinical, legal, and engineering — to save effort producing separate materials.
- D) Tailor architectural communication to each audience, framed in terms clinical and legal stakeholders can evaluate against their own priorities.
- 
**Question 56.** Midway through the project, the clinical team's requirements shift meaningfully based on a new regulatory guidance document.

- A) Re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline.
- B) Refuse to incorporate the new regulatory guidance since the requirements were already agreed upon earlier in the project.
- C) Incorporate the change silently, updating the design without informing stakeholders of the resulting tradeoff or timeline impact.
- D) Restart the entire project from scratch, regardless of how much of the existing design and delivered work the new guidance actually affects.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the operations team.

- A) This is the correct lifecycle model; monitoring and iteration after handoff are entirely the operations team's responsibility from that point on.
- B) Lifecycle management includes monitoring and iteration on production signal, not just discovery through handoff.
- C) Lifecycle responsibility ends once the contract is signed, regardless of what happens to the system after that point.
- D) Monitoring is only necessary if a major incident occurs, not as a routine ongoing part of the architect's responsibility.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient, since the final configuration values are all a future team needs to safely operate the system.
- B) Documenting the reasoning behind configuration choices is unnecessary overhead in a regulated environment already burdened with paperwork.
- C) Documentation should also capture the "why" behind key decisions, not just the final "what."
- D) Only the original architect should ever be allowed to modify the system, which makes writing down the reasoning behind decisions moot.

**Question 59.** The clinical operations team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume Claude Code-assisted tooling always saves meaningful time on every task category by default, without measuring any specific case or checking whether review overhead ever exceeds the time it claims to save.
- B) Ban Claude Code for all documentation tasks outright, without evaluating whether it actually reduces friction on any of them.
- C) Mandate Claude Code usage for every task category regardless of whether it measurably saves time versus adding review overhead.
- D) Evaluate specific task categories for genuine friction reduction versus cases where review overhead may exceed time saved.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no architectural fix, since every engineer eventually learns the triage process independently.
- B) Document the triage process as shared operational knowledge, reducing redundant re-derivation across the team.
- C) Restrict debugging of Claude Code integration failures to a single designated engineer so the triage knowledge stays with one person.
- D) The issue can only be resolved by switching to a different tool entirely, since the triage difficulty is inherent to Claude Code itself.

---
# Answer Key — Practice Exam 1

**Quick key:** 1-B, 2-A, 3-C, 4-D, 5-C, 6-B, 7-C, 8-A, 9-D, 10-B, 11-A, 12-C, 13-D, 14-B, 15-B, 16-C, 17-D, 18-B, 19-C, 20-B, 21-D, 22-B, 23-C, 24-A, 25-A, 26-A, 27-D, 28-B, 29-C, 30-D, 31-B, 32-A, 33-C, 34-D, 35-B, 36-C, 37-D, 38-B, 39-B, 40-C, 41-D, 42-B, 43-C, 44-B, 45-D, 46-B, 47-C, 48-D, 49-B, 50-A, 51-C, 52-D, 53-B, 54-C, 55-D, 56-A, 57-B, 58-C, 59-D, 60-B

---

**1. B** — The stated goal (more volume, same headcount, same cycle time) is an efficiency story; naming that pillar correctly shapes both the architecture and its success metrics. A overstates transformation as automatic; C narrows the framing to cost alone even though headcount-neutral throughput is the actual target; D skips the framing that keeps the project aligned to what discovery found.

**2. A** — Steps that vary by case and depend on intermediate findings are the defining case for an agentic pattern rather than a route decided up front. B assumes a predictability the scenario explicitly lacks; C undersells the orchestration actually needed beyond a single call; D treats real, non-interchangeable tradeoffs as cosmetic.

**3. C** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. A and D sacrifice these properties for a direct-communication shortcut (logging after the fact doesn't restore control); B discards the specialization that motivated separate subagents in the first place.

**4. D** — Every subagent succeeding while whole claim categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, B, and C all patch downstream instead of fixing the actual scope gap.

**5. C** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. A, B, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. B** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and C treat it as out of scope for the architecture; D overreacts to sentiment alone without weighing it against the technical case.

**7. C** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. A and B withhold the reasoning stakeholders need; D removes a deliberate, justified difference for false simplicity.

**8. A** — Adding a feedback loop that captures adjuster overrides and outcomes as a first-class architectural component is what lets the system improve after deployment, per the input→processing→output→feedback loop framing. B, C, and D all treat a first-class architectural component as optional or someone else's problem.

**9. D** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and C over-engineer a simple augmentation need; B is factually wrong.

**10. B** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not writing around it. A and C ignore this real degradation; D increases context budget without addressing selection reliability at all.

**11. A** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (document intake) completes, reducing latency without sacrificing correctness. B and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. C** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; B dumps the wrong kind of detail (including internals like the system prompt itself); D skips the communication need entirely.

**13. D** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, B, and C understate or deny this real architectural tradeoff.

**14. B** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave the actual knowledge transfer gap unaddressed.

**16. C** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and B ignore fit-to-task; D sacrifices quality on the cases that need capability most.

**17. D** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, B, and C all misstate or break the caching opportunity.

**18. B** — Chunking and indexing strategy must match each data shape; a single schema tuned for one content type degrades retrieval for the mismatched type. A and D force a mismatched shape onto the data; C discards useful structured data instead of indexing it appropriately.

**19. C** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and B force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. B** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, C, and D all reintroduce the failure mode the fix is meant to prevent.

**21. D** — Presenting both figures with attribution and likely methodological explanation preserves the actual information for the analyst rather than resolving a real discrepancy arbitrarily. A, B, and C all discard or obscure a genuine data conflict.

**22. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A, C, and D are all workarounds for a structurally solvable problem rather than fixes to the underlying mechanism.

**23. C** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. A, B, and D all fail the reuse or maintainability requirement.

**24. A** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. B and C ignore the real context cost of the monolithic approach; D removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. A** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. B reintroduces duplication (now scattered across each feature's system prompt); C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. D** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; C doesn't address correctness; B incorrectly claims no architectural mitigation exists.

**28. B** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, C, and D each drop a relevant factor from the decision.

**29. C** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and D assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. D** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and C all misstate this real, architecture-relevant constraint.

**31. B** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if it deflects tickets. A, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. A** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. B, C, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. C** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; D dismisses a real risk without evidence.

**34. D** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt or output-validation fixes rather than retrieval or model-tier changes. A and C misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. B** — A regression tied specifically to a data refresh event, with model and latency unchanged, points first at retrieval/indexing. A, C, and D would not specifically correlate with a knowledge-base refresh.

**36. C** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and B optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. D** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. A and C accept a monitoring blind spot; B drops accuracy monitoring from observability entirely.

**38. B** — Segmenting accuracy by topic/query type before cutting review protects against a failing segment hiding behind a healthy aggregate. A and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. B** — An isolated deflection-rate improvement could mask a worsened escalation failure mode; checking specifically for that before shipping is the correct diagnostic step. A and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. C** — "Accurate but poorly rated" points at an unmeasured quality dimension (tone, completeness, actionability) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; B assumes a fix without diagnosis.

**41. D** — Caching the static policy document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; C removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. B** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and D accept the described dysfunction; C addresses storage cost, not the actual observability gap.

**43. C** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and D guess without evidence; B gives up on a solvable, if effortful, diagnostic problem.

**44. B** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose the model itself as broken; C doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. B** — HIPAA-driven requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and C understate real architectural impact; D misidentifies the applicable regulatory regime.

**47. C** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal safety case for maximal review; D misattributes this to GDPR, which isn't the relevant regime described.

**48. D** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, consistency checks for output) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; C assumes one guardrail covers distinct risk types; B is factually wrong.

**49. B** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; C and D make unsupported blanket claims.

**50. A** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. B and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team.

**51. C** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a regulated system. A, B, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. D** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and C skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. B** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. C** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and D each understate what compliance-grade audit evidence actually requires.

**55. D** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by clinical, legal, and engineering audiences alike. A, B, and C each fail to serve at least one audience's real information need.

**56. A** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. B and C mishandle a real change; D disproportionately discards unaffected work.

**57. B** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. C** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and D all leave that reasoning undocumented and effectively lost.

**59. D** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and C over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 1.*
