# CCARP Practice Exam 11

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent E-Discovery Platform, RAG and Model Tiering for a Pharmaceutical Literature-Review Platform, Evaluation and Optimization of an HR Recruiting Assistant, Governance and Enablement for a Public-Sector FedRAMP Deployment) |
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

## Scenario A: Multi-Agent E-Discovery Platform for a Legal Services Firm (Questions 1–15)

Harrow & Vance LLP, a mid-size litigation firm, is building an internal e-discovery platform to handle document classification, privilege review, custodian communication analysis, and production packaging for large litigation matters. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with the firm's stakeholders.

---

**Question 1.** Discovery reveals the firm's actual goal is processing 3x the current document volume per matter with the same review-team headcount, while preserving the same defensibility standard — not new capabilities the current process lacks.

- A) Frame the architecture around transformation, since stakeholders generally expect new capability from any AI investment regardless of what discovery found.
- B) Frame the architecture around cost reduction exclusively, treating the headcount-neutral volume target as a budget line item to report upward each quarter.
- C) Skip framing around a specific value pillar, since a system that technically works should speak for itself once it ships to the review team.
- D) Frame the architecture around efficiency, building success metrics around review throughput per attorney-hour while holding the existing defensibility standard fixed and auditable.

**Question 2.** Document classification, privilege review, and production each require different steps depending on document type, privilege signals surfaced along the way, and custodian context discovered mid-review.

- A) A fixed workflow, since e-discovery follows a well-established legal process whose steps don't need to adapt to what review turns up midstream.
- B) An augmented LLM pattern, since one enhanced call with retrieval of privilege rules is sufficient to handle any document regardless of custodian context.
- C) An agentic pattern, since the right next step varies by document type and depends on findings surfaced partway through the review.
- D) Whichever pattern implements fastest this quarter, since the four orchestration patterns produce functionally interchangeable outcomes for a workflow this thoroughly validated.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (document classification, privilege detection, redaction, production formatting).

- A) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow across the pipeline.
- B) Let subagents communicate directly with each other, but log the traffic centrally afterward so the coordinator can review what was exchanged.
- C) Merge all four responsibilities into a single subagent, since coordination overhead outweighs keeping classification, privilege, redaction, and formatting separate.
- D) Let each subagent hand its output directly to whichever subagent needs it next, minimizing hops through the coordinator layer.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition routes only email-format documents into the pipeline — scanned PDFs and chat-export logs are never routed to any subagent and silently fall through, missing production.

- A) Fix the coordinator's decomposition so it explicitly covers every document source type, including scanned PDFs and chat exports.
- B) Add a prompt instruction telling each subagent to flag any document type it doesn't recognize as unrouted, then queue it for a nightly reconciliation review.
- C) Give the existing subagents broader tool access so they can pull in document types the coordinator never actually sends them.
- D) Add a fifth subagent dedicated to handling edge-case document types the coordinator currently drops on the floor.

**Question 5.** The design must align technical architecture to a specific business value pillar the firm actually cares about, distinct from a generic "we added AI" narrative.

- A) Any AI system inherently demonstrates transformation to stakeholders, so no additional value-pillar framing is required before this launch, regardless of what discovery found.
- B) Business value pillars are a business-development concern for the client relationship team, not something the technical architecture itself needs to reflect.
- C) Efficiency, risk-reduction/defensibility, cost-per-gigabyte, and cycle-time-to-production are pillar examples; the chosen one should drive the architecture and its metrics.
- D) The pillar should be picked after the matter closes, based on whichever benefit turns out easiest to measure in hindsight.

**Question 6.** The firm's associates and paralegals are skeptical of automation and worried about reduced review hours; discovery interviews surface this repeatedly.

- A) Ignore the sentiment since staff comfort with automation isn't a technical requirement the architecture needs to accommodate before launch.
- B) Treat it as a real implicit constraint alongside the explicit technical requirements — it shapes adoption, rollout sequencing, and where checkpoints matter most.
- C) Proceed with the technical design as planned and let change management handle staff sentiment separately, with no architectural input into rollout sequencing at all, even later.
- D) Recommend against the project entirely, since staff skepticism surfacing repeatedly this early is a strong enough signal on its own that the initiative will fail.

**Question 7.** A partner asks why the privilege-detection subagent uses a higher-capability, higher-cost model tier than the document-classification subagent.

- A) Use the same model tier everywhere for simplicity, since tier differences are usually more about habit than actual task difficulty.
- B) Explain the tradeoff explicitly: privilege determinations carry high legal risk and need deeper reasoning that justifies the added cost and latency involved.
- C) Tell the partner "higher tier because it's more important" and move on, since that captures the gist without needing further technical detail.
- D) Avoid explaining tier differences to partners at all, since the reasoning behind model selection is an implementation detail non-technical stakeholders won't find useful.

**Question 8.** The architecture's current design produces a final production recommendation with no mechanism to learn from attorney overrides of privilege or relevance calls over time.

- A) Add a feedback loop that captures attorney overrides and outcomes as a first-class architectural component, so the system keeps improving after deployment.
- B) Accept the current design as-is, since a system that already reflects best practice at launch doesn't need a mechanism for learning from later corrections.
- C) Treat feedback loops as a data science concern to raise with the analytics team after launch, unrelated to the architecture itself.
- D) Defer any feedback mechanism to a hypothetical future phase, since nothing about the current design needs to account for it right now.

**Question 9.** A litigation support team wants a single enhanced LLM call — with retrieval of privilege-rule guidance — to answer straightforward attorney questions about privilege categories, without any multi-step autonomous orchestration.

- A) This requires a fixed workflow with a structured five-step sequence, since privilege-category questions always follow the same predictable steps.
- B) This cannot be built with Claude at all, since anything involving retrieval implies an agentic architecture Claude doesn't support for simple lookups.
- C) An augmented LLM pattern — a single call enhanced with retrieval — fits this simpler augmentation need without the overhead of agentic orchestration.
- D) This calls for a full multi-agent architecture regardless of task simplicity, since privilege questions always warrant the most capable pattern available.

**Question 10.** The document-classification subagent's toolset has grown to include tools for billing entry and calendar scheduling that are unrelated to document classification.

- A) This has no architectural downside as long as the subagent's prompt is well-written and its inputs are validated before each tool call.
- B) More tools always improve a subagent's flexibility and should be encouraged, since a broader toolset only expands what a well-prompted subagent handles.
- C) The fix is to increase the subagent's context window, so it has more room to reason about which tool actually applies here.
- D) This capability bloat degrades tool-selection reliability; the unrelated billing and calendar tools should be removed or relocated to a more appropriate subagent.

**Question 11.** The coordinator currently processes each document sequentially through classification, privilege detection, relevance scoring, and redaction, even though privilege detection and relevance scoring have no dependency on each other's output.

- A) Run privilege detection and relevance scoring as independent, parallel subagent calls once classification completes, instead of processing every stage sequentially.
- B) Sequential processing of every stage is required to preserve chain-of-custody defensibility for the eventual production package handed to opposing counsel and the court.
- C) Parallelization isn't possible within a coordinator/subagent architecture, since subagents can only run one at a time by design.
- D) Combine privilege detection and relevance scoring into a single subagent so the sequencing question doesn't need to be answered.

**Question 12.** General counsel asks how the end-to-end architecture should be described at a high level for a steering committee unfamiliar with the technical details.

- A) Present only the model names and per-document token costs involved, since that's the financial detail a steering committee actually needs to sign off.
- B) Present the full technical architecture diagram in complete implementation detail, so the committee understands exactly how each subagent operates and validates its output internally.
- C) Skip a high-level description and move straight into an implementation demo, since watching the system work explains it better than words would.
- D) Describe input → processing → output → feedback loop at a level the committee can evaluate against case-outcome and cost goals, without implementation detail.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (document processing, privilege detection, redaction, production formatting) rather than a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows, since one unified schema can register unlimited tools without added complexity.
- B) Specialized subagents are strictly a cost-increasing choice, since splitting work across multiple calls only adds overhead with no reliability upside at all.
- C) There's no meaningful architectural difference between a single generalist agent and a coordinator with specialized subagents at this particular tool count.
- D) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped narrowly.

**Question 14.** The e-discovery architecture must eventually support a new matter type (regulatory investigations) the firm is planning to take on next year, but detailed requirements aren't available yet.

- A) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for requirements that aren't defined yet.
- B) Ignore future matter types entirely until next year's regulatory-investigation requirements actually exist and are formally handed to the architecture team for review.
- C) Build full support for regulatory investigations right now, making reasonable guesses at requirements that haven't actually been gathered from anyone yet.
- D) Refuse to proceed with any part of the current phase of work until next year's requirements are fully finalized.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document the architecture and the reasoning behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final values.
- B) Document only the final configuration values, since a well-built implementation with clean naming and inline comments should already be self-explanatory to whoever inherits it next year.
- C) Rely on the original architect remaining reachable indefinitely for questions, rather than writing anything down beyond the code itself.
- D) Skip formal documentation entirely if the codebase is organized well enough for a new team to read through it directly.

---

## Scenario B: RAG and Model Tiering for a Pharmaceutical Literature-Review Platform (Questions 16–30)

Veritas Biopharma's medical affairs team needs Claude to answer scientific-literature questions using both general reasoning and retrieval over a large, constantly-updated corpus of clinical trial publications, regulatory filings, and internal study reports. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most medical-affairs questions are moderately complex; a small fraction require deep multi-step reasoning across many trial publications, and a small fraction are simple lookups.

- A) Always use the highest-capability tier for every question, to guarantee top quality even on the simple lookups that don't need it.
- B) Route based on task difficulty — a fast tier for simple lookups, a balanced tier for typical questions, a higher tier for deep multi-step cases.
- C) Always use the fastest, cheapest tier for every question, accepting whatever quality loss shows up on the harder multi-step cases each week.
- D) Use one fixed model tier for every question regardless of complexity, since tier selection adds operational complexity without enough measurable benefit.

**Question 17.** Every request sends the same long system prompt (medical-affairs persona, citation requirements, regulatory disclaimer language) followed by retrieved document excerpts that vary per query.

- A) Alternate system instructions and retrieved content throughout the prompt so related material stays physically close together for the model to use.
- B) Put the retrieved content first in the prompt, since it's the part most specifically relevant to answering the particular query being asked right now.
- C) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it, cutting both latency and cost at high volume.
- D) Ordering of the system prompt and retrieved content doesn't meaningfully affect cost or latency for a retrieval-heavy workload running at this query volume.

**Question 18.** The corpus mixes long-form publications (full-text articles) with short structured data (dosing and adverse-event tables).

- A) One chunking and indexing strategy tuned for long-form articles can serve short structured dosing tables equally well without any adjustment at all.
- B) Chunking and indexing strategy should match each data shape — long-form articles need different chunking than structured tables, or retrieval degrades.
- C) Structured dosing and adverse-event data should be excluded from retrieval entirely, since it doesn't fit a document-oriented pipeline well.
- D) Use the largest possible chunk size across the board, so one strategy avoids needing to maintain two separate pipelines.

**Question 19.** Reviewer queries range from exact lookups ("what was the primary endpoint p-value in Trial 4471") to conceptual questions ("how has the safety narrative for Compound K evolved across recent publications").

- A) Use only embedding similarity search for every query type, since it generally captures meaning well enough regardless of how literal the query is.
- B) Query pattern doesn't meaningfully affect which retrieval approach fits best, since a well-tuned single approach handles both lookup and conceptual questions equally.
- C) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding search for conceptual questions, hybrid where both are needed.
- D) Use only structured/metadata filtering for every query type, since exact fields are always retrievable that way regardless of how the question is phrased.

**Question 20.** Reviewers need citations that reliably map each claim to a specific source publication and page/section, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources," and trust that instruction alone to keep every claim correctly mapped to its source.
- B) Add citations after the fact by searching for a plausible source matching each claim once the response has already been generated in full.
- C) Append a general bibliography of every publication consulted at the end of each response, without tying claims to specific sections.
- D) Require structured output pairing each claim with its source so citation mapping survives synthesis.

**Question 21.** Two retrieved trial reports disagree on a reported adverse-event rate by a small margin — likely different reporting populations (intent-to-treat vs. per-protocol).

- A) Average the two reported figures together and present the single averaged number as the definitive adverse-event rate for the trial.
- B) Always prefer whichever source was retrieved first, treating retrieval order as a reasonable tiebreaker between two disagreeing publications rather than surfacing the conflict.
- C) Omit the adverse-event figure from the response entirely, since the two sources disagree and neither can be confirmed as authoritative.
- D) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely methodological explanation, rather than silently picking one.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the "always output valid JSON" instruction more emphatically in the prompt, trusting stronger prose alone to close the gap.
- B) Post-process every response to strip any leading text before the first `{`, treating the preamble as a formatting artifact to clean up.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.
- D) Increase max_tokens so there's room for both the conversational preamble and the JSON structure that follows it each time.

**Question 23.** The platform needs to connect to a proprietary internal clinical-study-reports repository, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this literature-review platform.

- A) Build an MCP server exposing the study-reports repository's search operations as tools, reusable across internal Claude-powered tools.
- B) Hard-code the study-reports repository integration directly into this literature-review platform's own application code, since only one team currently needs it.
- C) Paste the entire study-reports corpus into every prompt, so no external retrieval integration or schema mapping is required at all.
- D) Require each consuming tool across the organization to reimplement its own separate integration with the repository independently.

**Question 24.** The team is deciding between exposing the full study-report catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Progressive discovery — querying a catalog resource as needed — scales better than loading the entire catalog into context up front.
- B) Loading the full study-report catalog into every prompt up front is always preferable to progressive querying, since completeness beats efficiency for a literature-review platform like this one.
- C) There's no meaningful difference in context cost between loading the full catalog and querying it progressively as needed here.
- D) The catalog should never be exposed to the agent in any form, structured or otherwise, regardless of how it's queried.

**Question 25.** A reviewer asks a chain-of-thought-friendly question requiring the model to reason step by step across several trial publications before concluding on a possible safety signal.

- A) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, fits this kind of multi-document synthesis question well.
- B) Zero-shot prompting with no reasoning guidance is always exactly as effective as prompting that asks for step-by-step intermediate reasoning.
- C) Chain-of-thought prompting is useful only for coding tasks and offers no real benefit for reasoning across scientific-literature publications toward a conclusion.
- D) The model can't reason across multiple retrieved documents at all, regardless of which prompting approach is used to guide it.

**Question 26.** The platform wants to standardize prompt fragments (citation format, regulatory disclaimer language, formatting rules) across several different literature-review features so changes propagate consistently.

- A) Duplicate the structured fragments into each feature's system prompt independently, keeping every feature free to diverge over time as needs change.
- B) Modular prompts and prompt caching are the same underlying mechanism, so adopting one automatically gives every feature the other's latency and cost benefits too.
- C) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching or Skills.
- D) Standardization of citation format and disclaimer language across features isn't something prompt design can actually achieve on its own.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific statistic from the correctly retrieved source publication.

- A) Trust the fluent, well-formatted, confidently-cited output as sufficient evidence on its own that the underlying statistic is correct.
- B) Apply defensive validation — verify extracted figures against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof.
- C) Treat this as purely a model limitation with no architectural mitigation available, since fluent wrong answers can't be caught systematically by any process at all.
- D) Increase output length so there's more room within the response for the correct statistic to eventually show up somewhere.

**Question 28.** The team debates whether reviewer-facing latency SLAs should factor into model tier selection for the literature-review platform.

- A) Latency should never factor into model or architecture decisions, since validated accuracy is the only dimension that ultimately matters to reviewers.
- B) Only cost should factor into tier selection; latency is a user-experience concern that belongs entirely outside the architecture decision.
- C) Yes — tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, not default to the top tier.
- D) SLAs are purely a stakeholder-communication topic with no bearing on which model tier the technical architecture actually selects for this platform.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to "latest" automatically in production, since a newer model release is always an improvement over whatever came before it.
- B) Upgrade immediately without running any of the platform's own tests, since improved benchmark scores already guarantee a deterministic, matching production-quality improvement across every reviewer workflow.
- C) Pin the current version and evaluate the new release against the platform's own tests before deliberately upgrading, since behavior can shift.
- D) Never upgrade models once the initial version is chosen, regardless of how the field or the platform's own needs evolve.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved document excerpts must fit alongside room for a detailed answer.

- A) Input and output share the same context-window budget, so retrieved-content volume must be balanced against room for a detailed answer.
- B) Input and output token budgets are entirely independent pools that never compete with each other for space within a single request to the model.
- C) This tradeoff only matters for unusually long documents, and never comes up for the platform's typical, shorter reviewer queries.
- D) Output length has no practical limit regardless of how much retrieved content is packed into the input alongside it.

---

## Scenario C: Evaluation and Optimization of an HR Recruiting Assistant (Questions 31–45)

TalentBridge Staffing built a Claude-powered assistant that screens resumes, drafts candidate outreach, and answers recruiter questions about pipeline status. It's been in production for four months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only resume-screening throughput and hasn't defined targets for latency, cost, or safety/fairness.

- A) Throughput alone is sufficient, since resume-screening volume is the system's stated primary purpose and everything else is secondary.
- B) Define evaluation metrics spanning accuracy, latency, cost, and safety/fairness as first-class metrics, so a fast but biased or unsafe system doesn't still count as a success story.
- C) Latency and cost are operations concerns to hand off to the infrastructure team, unrelated to how the evaluation strategy is designed.
- D) Fairness metrics only need to be defined once an actual complaint is filed against a specific screening decision.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past resumes.

- A) A single automated method checked against a fixed labeled set is sufficient for any production system, regardless of how nuanced its decisions are.
- B) Use mixed methodologies — automated eval for scale, human review, adversarial testing for fairness paths — since no single method covers every mode.
- C) Replace the automated checks entirely with human review, since only a person can judge whether a specific screening decision was fair, accurate, and appropriately worded for the candidate involved.
- D) Keep expanding the labeled set of past resumes indefinitely, treating dataset size as the only lever for improving coverage.

**Question 33.** The team wants to test whether a new candidate-outreach prompt improves response rates before rolling it out to all traffic.

- A) Roll out the new outreach prompt to all traffic immediately and monitor response rates informally after the fact each week.
- B) Change the prompt wording and the underlying model tier at the same time, to maximize the chance of seeing an improvement.
- C) Skip testing altogether, since a prompt change is inherently low-risk and doesn't need the rigor a model change would.
- D) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change alone.

**Question 34.** A candidate outreach message states the wrong compensation band for a role. Investigation shows the underlying job-requisition data was correct and retrieved properly, and the model's message paraphrased it inaccurately.

- A) This is a retrieval problem; fix the indexing pipeline, even though the investigation already shows the job-requisition data was retrieved correctly.
- B) This can't be diagnosed at all without retraining the underlying model on compensation-related examples first, regardless of what the investigation found.
- C) This is best characterized as a prompt/generation issue — inaccurate paraphrasing of correctly retrieved content — calling for prompt or output-validation fixes.
- D) This is a model-tier mismatch requiring a switch to a different tier, regardless of what the specific failure actually turned out to be.

**Question 35.** Immediately after a scheduled job-requisition data refresh, the system starts returning confident but incorrect compensation figures, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider, even though the investigation found the model version unchanged throughout.
- B) Suspect a temperature setting change, since the system's apparent confidence in its incorrect compensation figures seems to have gone up right around the refresh.
- C) Suspect the context window shrank, even though nothing about the regression points at truncated input at all.
- D) Investigate the retrieval/indexing layer first, since the regression is tied to the data refresh event with model, temperature, and latency all unchanged.

**Question 36.** The team wants to reduce cost and latency of resume screening but is worried about hurting accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Optimize cost, latency, and accuracy independently of one another, tuning each in isolation without regard for how the changes interact.
- B) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest configuration that fails the accuracy bar isn't a win either.
- C) Accuracy should always be maximized regardless of what that does to cost or latency, since screening quality is what matters most.
- D) This tradeoff can't actually be measured with real data, only estimated by guessing at where the configuration probably sits.

**Question 37.** Production monitoring currently reports only an overall weekly average screening-accuracy score.

- A) Monitoring should surface drift and outliers — a per-segment breakdown — since an aggregate average can hide a failing segment.
- B) A single aggregate weekly average is sufficient for production monitoring, since it already reflects performance across every role and candidate segment being screened.
- C) Monitoring should track only cost going forward, since the separate eval suite already covers accuracy entirely on its own.
- D) Weekly granularity is always sufficient for this kind of monitoring, regardless of how quickly a segment's performance might shift.

**Question 38.** The team proposes cutting human review of flagged low-confidence screening decisions by 80%, citing a 96% aggregate accuracy score.

- A) Proceed with the cut based on the 96% aggregate figure alone, since that number already reflects overall system quality closely enough.
- B) Aggregate accuracy is definitionally representative of every role and candidate segment underneath it, by simple construction of the metric.
- C) Segment accuracy by role and candidate type before cutting review, since the aggregate figure can mask a specific segment performing far worse than average.
- D) Human review should never be reduced at all, regardless of what the measured accuracy numbers eventually show over time.

**Question 39.** An A/B test shows a new screening prompt improves throughput, but the team hasn't checked whether it also changed the false-negative rate on qualified candidates from underrepresented backgrounds.

- A) Throughput alone is a sufficient signal to ship the new screening prompt, since improving speed was the change's stated goal.
- B) False-negative behavior on underrepresented candidates isn't something a structured evaluation process can actually measure before a change ships to production.
- C) Ship the change now and monitor informally after the fact, rather than testing the fairness dimension beforehand at all.
- D) Check the fairness-related failure mode specifically before shipping — a throughput gain could be masking a rise in false negatives.

**Question 40.** The team wants to diagnose why a subset of screening summaries are technically accurate but rated poorly by recruiters in usability feedback.

- A) Assume the accuracy metric itself is broken and discard it, since recruiters are rating technically accurate summaries poorly in feedback surveys.
- B) Investigate a dimension beyond factual accuracy — clarity, completeness, actionability — since "accurate but poorly rated" points at an unmeasured gap.
- C) Increase the model's capability tier, assuming a more capable model will automatically satisfy recruiters regardless of the complaint.
- D) Ignore the recruiter feedback scores entirely and keep relying on the existing accuracy metric as the sole quality signal.

**Question 41.** The team is optimizing token usage and notices the system sends full candidate-conversation history plus a large static company hiring-policy document on every turn of multi-turn recruiter chats.

- A) This has no optimization opportunity, since sending full conversation history and the policy document on every turn is always required.
- B) Apply prompt caching to the static hiring-policy document and trim or summarize older conversation turns, to increase headroom for the live turn.
- C) Remove the hiring-policy document from the prompt entirely, since it's static and therefore assumed less important than the live conversation.
- D) Switch to a smaller model as the only lever considered for reducing token cost, accepting whatever accuracy loss that brings.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Redesign observability toward structured, aggregable signals — sampling, tagged categories — since raw logs at volume aren't reviewable.
- B) Raw logging of every prompt and response at full volume is itself already a sufficient observability strategy for a production system running at this scale and traffic level.
- C) Reduce the volume of logging to save on storage cost, without changing anything else about how the logs get used.
- D) Observability doesn't require any particular structure, as long as the underlying raw data is retained somewhere for later use.

**Question 43.** The team wants to identify whether a recent screening-quality regression was caused by a recent prompt change, a recent model version change, or a job-requisition data change — all three happened in the same week.

- A) Assume the most recently shipped change is always the cause of the regression, without checking either of the other two changes.
- B) Attribution becomes impossible once multiple changes have shipped in the same week, so the actual cause simply can't ever be determined after the fact with any confidence.
- C) Revert all three changes at once without investigating which one — if any — actually caused the regression this week.
- D) Test and roll out one variable at a time — with three simultaneous changes, attribution requires isolating each independently.

**Question 44.** An automated eval asserts that a candidate-summary output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining, since it can't reliably reproduce the exact same summary text on every single run.
- B) The reference string just needs to be longer, so there's more surface area for the model's generated output to match against each time.
- C) Temperature should be increased to fix the intermittent failures, since more randomness across runs should even out the mismatches over several evaluation cycles.
- D) Exact-string-match evals are the wrong tool for non-deterministic output; the eval should check content or structure instead.

**Question 45.** Leadership wants a single number to represent "how good" the recruiting assistant is, to track over time.

- A) A single aggregate metric can be useful, but should sit alongside segment-level and multi-dimensional detail so it doesn't mask a failing area.
- B) A single number is always achievable and sufficient for any system's evaluation needs, since aggregate metrics are inherently deterministic and therefore always comparable across every reporting period.
- C) Use screening throughput alone as the single number, since it's the system's stated primary purpose and easiest figure to track weekly.
- D) Refuse to provide leadership any single summary metric at all, under any circumstances, regardless of what they're asking for.

---

## Scenario D: Governance and Enablement for a Public-Sector FedRAMP Deployment (Questions 46–60)

The Department of Civic Services, a state benefits agency, is deploying a Claude-powered system that processes constituent benefits applications and assists a 25-person case-management team using Claude Code internally, operating within a FedRAMP Moderate authorization boundary. You are responsible for governance, compliance, and developer enablement for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) This sequencing carries no real risk, since compliance controls can always be bolted on cleanly in the final week before a public-sector launch.
- B) Compliance only affects legal documentation and sign-off paperwork, not anything about how the underlying system itself gets validated, architected, or built.
- C) HIPAA, not FedRAMP, is the relevant regulatory regime for a state benefits system like this one, since it involves individual applicant data.
- D) FedRAMP-driven data-boundary, retention, and access-control requirements can force structural changes far costlier to retrofit than to design in from the start.

**Question 47.** A team proposes requiring human approval on every single output the benefits-eligibility system produces, framing it as the safest governance posture.

- A) Maximal human review on every output is always the correct default posture for a public-sector AI system, regardless of the decision's actual error cost.
- B) Human reviewers are categorically less accurate than the model on eligibility questions, which makes universal review actively counterproductive here.
- C) Requiring human approval on every output is mandated by FedRAMP itself, independent of any other governance consideration in play.
- D) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions instead.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from applicant-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed once they're actually observed in production, rather than planned for up front.
- B) A single generic guardrail addresses hallucination, prompt injection, and inconsistent output equally well, since all three are just variations of the same general "LLM risk" that one broad control can cover.
- C) Design mitigations for each known failure mode up front — grounding for hallucination, isolation for injection, validation for consistency — rather than reactively.
- D) These risks are exclusive to non-government use cases and don't meaningfully apply to a public-sector benefits system.

**Question 49.** The case-management team asks whether the system's eligibility recommendations could produce disparate outcomes across different applicant demographics.

- A) This is not an architectural concern; it belongs entirely to a legal/compliance review conducted after the system has already launched.
- B) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population rather than assuming disparate impact is absent.
- C) Disparate impact is impossible in an LLM-based system by construction, since the model has no awareness of demographic categories or applicant backgrounds whatsoever.
- D) This concern only applies to systems that make final eligibility decisions outright, not to an assistive system a caseworker still reviews.

**Question 50.** The 25-person case-management team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team level so behavior doesn't depend on local setup.
- B) Have each of the 25 staff members individually troubleshoot and configure their own local Claude Code setup as issues come up week to week.
- C) Restrict Claude Code usage to a single designated engineer, so configuration variance across the rest of the team stops mattering.
- D) Accept the inconsistency as an unavoidable cost of rolling out AI tooling across a 25-person team this year.

**Question 51.** The team wants Claude Code-generated code changes in this FedRAMP context to go through the same review rigor as any other change to an authorized system.

- A) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the required review rigor.
- B) AI-assisted code should bypass the standard review process entirely, since it was generated rather than hand-written by an engineer directly.
- C) Only a brief spot-check of AI-generated code is necessary, since the generation process itself already catches most of the mistakes.
- D) Review requirements should be set lower for AI-generated code than for human-written code, given how the code was actually produced.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug lives in the generated code itself, without first checking how the surrounding system actually integrated that change.
- B) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the model output — using traces to localize it.
- C) Disable Claude Code for the entire case-management team going forward, following any incident that traces back to AI-assisted code.
- D) Roll back every recent Claude Code-assisted change across the system, skipping any structured triage, regardless of whether it's actually related to this incident.

**Question 53.** The case-management team wants a documented, repeatable workflow for a recurring task (generating a weekly caseload-compliance report) versus a one-off exploratory coding task.

- A) Build both the recurring report and the one-off exploratory task as ad hoc, undocumented prompts recreated from scratch every time they're needed.
- B) Build both the recurring report and the one-off task as standing MCP servers, regardless of how often either one is actually going to be reused.
- C) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session.
- D) Recurring workflows and one-off exploratory tasks should be built identically, since the underlying tool doing the work is the same.

**Question 54.** The compliance team wants documented evidence of who accessed what applicant-related data through the system and when.

- A) Access logging is optional if the system already has role-based permissions configured, since permissions alone already constrain who can view any given applicant's record.
- B) Audit logging can be added to the system later, without any real architectural impact from having deferred it this long.
- C) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements.
- D) Only failed access attempts actually need to be logged; successful access doesn't need to be recorded at all.

**Question 55.** The steering committee for this deployment includes program-office, legal, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with engineering stakeholders directly, and let them relay whatever they judge relevant to program-office and legal on their own, without a dedicated communication plan for either group.
- B) Tailor architectural communication to each audience — tradeoffs framed in terms program-office and legal can evaluate against their own priorities.
- C) Skip stakeholder communication with the steering committee entirely until the system is fully built and ready to demo.
- D) Use one set of identical technical documentation for all three audiences, to save the effort of producing separate materials.

**Question 56.** Midway through the project, the case-management team's requirements shift meaningfully based on a new state regulatory guidance document.

- A) Refuse to incorporate the new regulatory guidance at all, since the original requirements were already formally agreed upon with the team.
- B) Incorporate the regulatory-driven change silently, without informing the steering committee of its impact on scope, cost, or timeline going forward.
- C) Restart the entire project from scratch, regardless of how narrow or broad the actual scope of the new regulatory change turns out to be.
- D) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff, and adjust the design and timeline accordingly.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the operations team.

- A) This is the correct lifecycle model; monitoring and iteration after handoff become entirely the operations team's responsibility from that point forward.
- B) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility.
- C) Lifecycle responsibility for the architecture ends once the deployment contract with the agency is signed and delivered.
- D) Ongoing monitoring is only necessary if and when a major production incident actually occurs down the road.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient, since the final configuration values were already validated once and are really all a future team needs to keep the system running safely.
- B) Documenting the reasoning behind configuration choices is unnecessary overhead in an already heavily regulated compliance environment like this one.
- C) Only the original architect should ever be allowed to modify the system going forward, which makes further documentation effectively moot.
- D) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system.

**Question 59.** The case-management team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves meaningful time on every task category by default, without checking any specific case first.
- B) Evaluate task categories for genuine friction reduction versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit either way across the whole team's workload.
- C) Ban Claude Code for all documentation tasks outright, without evaluating whether it actually helps or hurts in that category.
- D) Mandate Claude Code usage across all task categories regardless of whether the measured benefit actually supports doing so.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) Treat the redundant re-derivation as an acceptable ongoing inefficiency, since no architectural fix could really address how engineers debug this.
- B) Restrict debugging of Claude Code integration failures to a single designated engineer, so the rest of the team stops needing the shared triage process at all going forward.
- C) Document the triage process — distinguishing integration-layer failures from model-output failures — as shared operational knowledge.
- D) Conclude the issue can only be resolved by switching away from Claude Code to a different tool entirely.

---
# Answer Key — Practice Exam 11

**Quick key:** 1-D, 2-C, 3-A, 4-A, 5-C, 6-B, 7-B, 8-A, 9-C, 10-D, 11-A, 12-D, 13-D, 14-A, 15-A, 16-B, 17-C, 18-B, 19-C, 20-D, 21-D, 22-C, 23-A, 24-A, 25-A, 26-C, 27-B, 28-C, 29-C, 30-A, 31-B, 32-B, 33-D, 34-C, 35-D, 36-B, 37-A, 38-C, 39-D, 40-B, 41-B, 42-A, 43-D, 44-D, 45-A, 46-D, 47-D, 48-C, 49-B, 50-A, 51-A, 52-B, 53-C, 54-C, 55-B, 56-D, 57-B, 58-D, 59-B, 60-C

---

**1. D** — The stated goal (3x volume, same headcount, same defensibility standard) is a throughput/efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A, B, and C either misname the pillar or skip the framing that keeps the project aligned to what discovery actually found.

**2. C** — Steps that vary by document and depend on intermediate findings are the defining case for an agentic pattern. A assumes a predictability the scenario explicitly lacks; B undersells the orchestration actually needed; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. A** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. B and D sacrifice these properties for a shortcut; C discards the specialization that motivated separate subagents in the first place.

**4. A** — Every subagent succeeding while whole document-source categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. B, C, and D all patch downstream instead of fixing the actual scope gap.

**5. C** — Business value pillars (efficiency, defensibility, cost-per-gigabyte, cycle time) give both the architecture and its metrics a clear anchor. A, B, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. B** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and C treat it as out of scope; D overreacts to sentiment alone without weighing it against the technical case.

**7. B** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. A and C withhold the reasoning stakeholders need; D removes a deliberate, justified difference for false simplicity.

**8. A** — Adding a feedback loop that captures attorney overrides and outcomes as a first-class architectural component is what lets the system improve after deployment, per the input→processing→output→feedback loop framing. B, C, and D all treat a first-class architectural component as optional or someone else's problem.

**9. C** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and D over-engineer a simple augmentation need; B is factually wrong.

**10. D** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just adding input checks around the existing sprawl. A and B ignore this real degradation; C doesn't address selection reliability at all.

**11. A** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (classification) completes, reducing latency without sacrificing correctness. B and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. D** — A steering committee needs the architecture communicated at the level of case-outcome and cost evaluation, not implementation internals. A is insufficient detail; B is too much of the wrong kind of detail; C skips the communication need entirely.

**13. D** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, B, and C understate or deny this real architectural tradeoff.

**14. A** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. B ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. A** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. B, C, and D all leave the actual knowledge transfer gap unaddressed.

**16. B** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and D ignore fit-to-task; C sacrifices quality on the cases that need capability most.

**17. C** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, B, and D all misstate or break the caching opportunity.

**18. B** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and D ignore this mismatch; C discards useful structured data.

**19. C** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and D force one mechanism onto queries it doesn't fit; B denies a real, consequential distinction.

**20. D** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, B, and C all reintroduce the failure mode the fix is meant to prevent.

**21. D** — Presenting both figures with attribution and likely methodological explanation preserves the actual information for the reviewer rather than resolving a real discrepancy arbitrarily. A, B, and C all discard or obscure a genuine data conflict.

**22. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and B are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. B, C, and D all fail the reuse or maintainability requirement.

**24. A** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. B and C ignore the real context cost of the monolithic approach; D removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. C** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; B conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. B** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; D doesn't address correctness; C incorrectly claims no architectural mitigation exists.

**28. C** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, B, and D each drop a relevant factor from the decision.

**29. C** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and B assume benchmark gains transfer automatically; D over-corrects into permanent stagnation.

**30. A** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. B, C, and D all misstate this real, architecture-relevant constraint.

**31. B** — Accuracy, latency, cost, and safety/fairness should all be defined as first-class metrics, since a system failing on any of them fails overall even if it screens quickly. A, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. B** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially fairness-relevant edge cases. A, C, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. D** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; C dismisses a real risk without evidence.

**34. C** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. A and D misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. D** — A regression tied specifically to a data refresh event, with model version, temperature, and latency all unchanged, points first at retrieval/indexing. A, B, and C would not specifically correlate with a job-requisition data refresh.

**36. B** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and C optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and D accept a monitoring blind spot; C drops accuracy monitoring from observability entirely.

**38. C** — Segmenting accuracy by role/candidate type before cutting review protects against a failing segment hiding behind a healthy aggregate. A and B trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. D** — An isolated throughput improvement could mask a worsened fairness-related failure mode; checking specifically for that before shipping is the correct diagnostic step. A and C ship without adequate testing; B incorrectly claims the failure mode is unmeasurable.

**40. B** — "Accurate but poorly rated" points at an unmeasured quality dimension (clarity, completeness, actionability) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; C assumes a fix without diagnosis.

**41. B** — Caching the static hiring-policy document and trimming/summarizing older turns directly increases the headroom available for the live turn in multi-turn conversations. A denies an obvious lever; C removes needed content; D is a blunt, quality-risking lever when a more targeted fix is available.

**42. A** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. B and D accept the described dysfunction; C addresses cost, not the actual observability gap.

**43. D** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and C guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. D** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and C misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. A** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. B and C oversimplify to a single lossy number — B by wrongly assuming determinism makes any one aggregate automatically comparable over time; D refuses a reasonable, common stakeholder request.

**46. D** — FedRAMP-driven requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate real architectural impact; C misidentifies the applicable regulatory regime.

**47. D** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal safety case for maximal review; C misattributes this to FedRAMP, which doesn't mandate universal review.

**48. C** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; B assumes one guardrail covers distinct risk types; D is factually wrong.

**49. B** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; C makes an unsupported blanket claim; D wrongly assumes the concern disappears just because a caseworker is nominally in the loop.

**50. A** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. B and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team.

**51. A** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a FedRAMP-authorized system. B, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. B** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and C skip diagnosis; D is a disproportionate reaction that doesn't investigate the actual cause.

**53. C** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; B over-engineers the one-off task by defaulting to standing infrastructure regardless of reuse; D ignores that reuse profile should drive the choice.

**54. C** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and D each understate what compliance-grade audit evidence actually requires.

**55. B** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by program-office, legal, and engineering audiences alike. A, C, and D each fail to serve at least one audience's real information need.

**56. D** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and B mishandle a real change; C disproportionately discards unaffected work.

**57. B** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. D** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and C all leave that reasoning undocumented and effectively lost.

**59. B** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and D over-assume benefit; C forecloses potential benefit without evaluation.

**60. C** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; B and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 11.*
