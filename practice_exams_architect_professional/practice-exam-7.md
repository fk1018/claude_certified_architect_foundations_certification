# CCARP Practice Exam 7

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent E-Discovery Platform for a Legal Services Firm, RAG and Model Tiering for a Pharmaceutical Literature-Review Platform, Evaluation and Optimization of an HR Recruiting Assistant, Governance and Enablement for a Public-Sector FedRAMP Deployment) |
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

Meridian Discovery Partners, a litigation-support firm serving Am Law 100 clients, is building a Claude-powered e-discovery platform to review, tag, and produce documents for active litigation matters. The platform must classify documents for relevance, screen for attorney-client privilege, and route borderline calls to reviewing attorneys. You are the architect responsible for the multi-agent design and for running discovery with the firm's litigation-support leadership.

---

**Question 1.** Discovery with Meridian's litigation-support leadership reveals the actual goal: processing 5x the current document-review volume during peak discovery windows, using the same review team size and without increasing average per-document review time.

- A) Frame the architecture around transformation, since leadership will want a novel-capability story even though discovery pointed at headcount and cycle time instead.
- B) Frame the architecture around efficiency and build success metrics around review throughput per reviewer.
- C) Frame the architecture around risk reduction, since litigation work is inherently risk-sensitive regardless of the stated volume goal.
- D) Skip framing around any value pillar; a working system will justify itself to the partners without a named story.

**Question 2.** Document-review steps vary by document type, by findings from earlier documents in the same custodian's collection, and by whether a privilege flag was already raised — the right next step isn't knowable in advance.

- A) A fixed workflow, since document review is a well-established process with predictable steps.
- B) An augmented LLM pattern, since one enhanced call with retrieval can resolve any document-review question in a single pass without further steps.
- C) An agentic pattern, since the right next step depends on document type and on findings discovered earlier in the same collection.
- D) Whichever pattern the review team already knows, since the four patterns are functionally interchangeable in practice.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents: document classification, privilege screening, relevance tagging, and production formatting.

- A) Let each subagent pass its output directly to whichever subagent needs it next, skipping the coordinator entirely to save a hop.
- B) Merge all four responsibilities into a single subagent, since combining them removes coordination overhead entirely.
- C) Route all inter-subagent communication through the coordinator, preserving observability and consistent error handling.
- D) Allow direct subagent-to-subagent communication, but require each subagent to log its own traffic separately.

**Question 4.** Every subagent performs its assigned task correctly, but the coordinator's decomposition routes only email and standard office documents through the pipeline — text messages and voicemail transcripts are never assigned to any subagent and silently skip review entirely.

- A) Add a fifth subagent purely to catch document formats the other four don't recognize.
- B) Instruct the existing subagents, via prompt, to flag any document type they don't recognize as their own.
- C) Fix the coordinator's decomposition so it explicitly covers every document format in the collection.
- D) Expand every subagent's tool access so each one can process any document type it happens to receive.

**Question 5.** The design must align the technical architecture to a specific business value pillar the firm's leadership actually cares about, rather than a generic "we added AI to document review" narrative.

- A) Name a pillar such as efficiency, risk reduction, cost, or defensibility, and let that choice drive both the architecture and its metrics.
- B) Any AI-assisted review process inherently demonstrates transformation, so no separate framing conversation with leadership is required.
- C) Business value pillars are a business-development concern the architecture team can leave to the partners entirely.
- D) Select the pillar after launch, based on whichever production metric happens to look best at the time.

**Question 6.** Discovery interviews with the firm's contract reviewers and paralegals repeatedly surface anxiety that the platform will eliminate their roles.

- A) Disregard the sentiment in the architecture conversation, since it isn't a stated technical requirement from leadership.
- B) Proceed with the technical design as planned and let a separate change-management effort handle morale, with zero architectural input.
- C) Recommend cancelling the project on the basis of the sentiment alone, without weighing it against the stated volume goal.
- D) Treat the sentiment as a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints go.

**Question 7.** A partner asks why the privilege-screening subagent runs on a higher-capability, higher-cost model tier than the document-classification subagent.

- A) Explain that privilege calls carry high error cost and need deeper reasoning, which justifies the added cost and latency over the simpler classification task.
- B) Respond that the higher tier is used "because privilege is important," and move on without further detail.
- C) Avoid answering directly, since partners aren't expected to understand technical tier decisions.
- D) Standardize both subagents on one tier for simplicity, since tier matching mostly matters at far higher volume than this.

**Question 8.** The current design produces a final privilege/relevance recommendation with no mechanism to capture attorney overrides or downstream case outcomes for future improvement.

- A) This is acceptable for now, since the initial classification logic already reflects current review-team best practice.
- B) Add a feedback loop, as a first-class architectural component, that captures attorney overrides and case outcomes for improving the system after launch.
- C) Feedback loops are a data-science concern that has no bearing on the architecture itself.
- D) Defer any feedback mechanism to a hypothetical future phase, with no hooks designed into the current build.

**Question 9.** For a narrower need, the firm wants a single enhanced call — with retrieval over the firm's internal case-law and precedent database — to answer straightforward "has this privilege argument been raised before in this matter" questions, without multi-step autonomous orchestration.

- A) This requires a full multi-agent architecture regardless of how narrow the underlying task actually is.
- B) This can't be built with Claude, since retrieval-augmented lookups always need autonomous agent behavior in order to function.
- C) This requires a fixed, structured workflow of at least four sequential steps, matching the platform's other pipelines.
- D) An augmented LLM pattern — a single call enhanced with retrieval — fits this narrower need without agentic overhead.

**Question 10.** The document-classification subagent's toolset has grown to include tools for tasks like billing-code lookup and client-invoice generation, unrelated to classification.

- A) This carries no architectural downside as long as the subagent's system prompt stays well-structured.
- B) More tools always increase a subagent's flexibility, so the growing toolset should be encouraged as the platform expands.
- C) This capability bloat degrades tool-selection reliability; remove or relocate the unrelated tools.
- D) The correct fix is to increase the subagent's context window rather than reconsider its toolset.

**Question 11.** The coordinator currently runs document classification, then privilege screening, then relevance tagging, then production formatting strictly in sequence, even though privilege screening and relevance tagging have no dependency on each other's output.

- A) Run privilege screening and relevance tagging as independent, parallel calls once classification finishes.
- B) Sequential processing across all four stages is required to preserve an admissible, defensible audit trail for the matter.
- C) Parallelization of independent subagent calls isn't achievable within a coordinator/subagent architecture.
- D) Combine privilege screening and relevance tagging into a single subagent to sidestep the sequencing question.

**Question 12.** Firm leadership asks how the end-to-end architecture should be described to a steering committee of partners unfamiliar with the technical implementation.

- A) Present only the model names and per-document token costs, since those are the numbers leadership asks about first.
- B) Present the complete technical architecture diagram, including subagent prompts and tool schemas, with no simplification for the audience.
- C) Describe input → processing → output → feedback loop at a level the committee can evaluate against defensibility and throughput goals.
- D) Skip a high-level description and move directly into a live system demo, letting the interface speak for itself.

**Question 13.** A competing vendor proposes a single generalist agent holding every tool (classification, privilege logic, relevance tagging, production formatting) instead of a coordinator with specialized subagents.

- A) A single generalist agent scales better as the number of tools grows, since it avoids inter-agent coordination overhead.
- B) Specialized subagents are strictly a cost-increasing choice, since running several narrow agents costs more than one broad one.
- C) There is no meaningful architectural difference between the two approaches once both use the same underlying model.
- D) A single agent holding every tool is more likely to suffer degraded tool-selection reliability than narrower subagents.

**Question 14.** The platform must eventually support a new matter type (regulatory investigations with different privilege rules) the firm expects to take on next year, but detailed requirements aren't defined yet.

- A) Ignore future matter types entirely in the current design until firm requirements for regulatory investigations exist.
- B) Build full support for regulatory-investigation privilege rules now, filling gaps in the undefined requirements with guesses.
- C) Design current subagent boundaries with reasonable extensibility in mind, without over-building for speculative requirements.
- D) Refuse to proceed with the current phase until next year's requirements are formally finalized by the firm.

**Question 15.** Firm leadership wants documentation they can hand to a new engineering vendor in a year, who will extend the platform without the original architect present.

- A) Document only the final configuration values, since a well-organized implementation is otherwise self-explanatory.
- B) Document the reasoning behind key decisions — pattern choices, subagent boundaries, tier selections — not just the final values, so a future vendor isn't left re-deriving that context from scratch.
- C) Rely on the original architect remaining reachable indefinitely instead of writing anything down.
- D) Documentation is unnecessary as long as the code and prompts themselves stay well-organized.

---

## Scenario B: RAG and Model Tiering for a Pharmaceutical Literature-Review Platform (Questions 16–30)

Verdant Biosciences operates a literature-review platform that helps pharmacovigilance and regulatory-affairs teams synthesize findings across journal articles, clinical-trial registries, and internal safety reports. You are architecting model tiering, prompting, and the retrieval layer that connects the platform to a constantly growing corpus of publications and structured trial data.

---

**Question 16.** Most literature-review questions on Verdant's platform are moderately complex; a small fraction require deep multi-step reasoning across many trial reports, and a small fraction are simple lookups (e.g., a single drug's approval date).

- A) Use one fixed model tier for every question, since consistent tiering is simpler to operate than routing logic.
- B) Route by task difficulty: a fast tier for lookups, a balanced tier for typical questions, a high-capability tier for deep cases.
- C) Always use the fastest, cheapest tier to control cost, accepting quality loss on the complex minority of trial-report synthesis questions.
- D) Always use the highest-capability tier on every question, regardless of how simple the lookup actually is.

**Question 17.** Every request sends the same long system prompt (regulatory-affairs persona, citation format, formatting rules) followed by retrieved excerpts that vary per query.

- A) Order has no meaningful effect on cost or latency for a workload of this size.
- B) Interleave system instructions and retrieved content throughout the prompt so related rules sit right beside the excerpts they individually govern.
- C) Put the retrieved content first, since it's the part most specific to the current query.
- D) Place the stable system prompt first and enable caching, with the varying excerpts after it, to cut cost across high query volume.

**Question 18.** The corpus mixes long-form journal articles and trial reports with short structured records (a table of adverse-event counts by dose).

- A) Match chunking and indexing strategy to each data shape, since one strategy tuned for long-form text degrades retrieval on the short structured records and vice versa.
- B) One chunking strategy tuned for long-form documents can serve the short structured records equally well.
- C) Structured adverse-event data should be excluded from retrieval entirely, since only prose benefits from a RAG layer.
- D) Use the largest possible chunk size everywhere so only one indexing strategy needs maintaining.

**Question 19.** Queries range from exact lookups ("what was the enrollment size of Trial NCT-1147") to conceptual questions ("how has the safety narrative for Drug X evolved across recent publications").

- A) Match retrieval to query pattern: structured filtering for exact lookups, embedding search for conceptual questions.
- B) Use only embedding similarity search for every query type, since semantic search is normally the stronger default across use cases.
- C) Use only structured, schema-based metadata filtering for every query type, since exact figures are what reviewers check most.
- D) Query pattern has no real bearing on which retrieval approach is appropriate here.

**Question 20.** Regulatory-affairs reviewers need citations that reliably map each claim to a specific source document and section, and prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite your sources" without any further structural requirement.
- B) Pair each claim with its source (document, section, excerpt) in the output so mapping survives synthesis.
- C) Add citations after the fact by searching the corpus for a plausible source matching each claim already written.
- D) Append a general bibliography of consulted documents at the end, without tying individual claims to it.

**Question 21.** Two retrieved sources report different adverse-event rates for the same trial arm — likely because one reports crude incidence and the other reports incidence adjusted for exposure time.

- A) Average the two figures together and present the blended average as the single answer.
- B) Omit the adverse-event rate entirely from the response, since the two sources disagree on the exact number reported.
- C) Always prefer whichever source the retrieval layer happened to rank first.
- D) Present both figures explicitly, annotated as a discrepancy with source attribution and the likely explanation.

**Question 22.** A prompt instructing the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Enforce structure through tool-use/schema-constrained output rather than through prose instructions alone.
- B) Repeat the instruction more emphatically in the system prompt, on the assumption that emphatic prose makes output deterministic.
- C) Post-process every response to strip any text appearing before the first `{` character.
- D) Increase max_tokens so there's room for both the preamble and the JSON to fit in one response.

**Question 23.** The platform needs to connect to Verdant's proprietary internal safety-report system, exposing search and retrieval to several other internal Claude-powered tools beyond the literature-review platform.

- A) Build an MCP server exposing the safety-report operations as reusable tools/resources.
- B) Hard-code the safety-report integration directly into this one platform's application code and nowhere else.
- C) Paste the entire safety-report corpus into every prompt so no separate integration layer is needed.
- D) Have each consuming tool reimplement its own integration independently, since a shared server adds a coordination dependency between teams.

**Question 24.** The team is deciding between exposing the full trial-registry catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Progressive discovery — querying the catalog only as needed — scales better as the registry keeps growing.
- B) Loading the full catalog up front is always preferable, since it guarantees complete registry coverage on every call.
- C) There's no meaningful difference in context cost between the two approaches once caching is enabled.
- D) The catalog should never be exposed to the agent in any form, whether up front or on demand.

**Question 25.** A researcher asks a question requiring the model to reason step by step across several trial reports and journal articles before concluding whether a safety signal is emerging.

- A) Zero-shot prompting with no reasoning guidance is equally effective for this kind of multi-document safety-signal question.
- B) Chain-of-thought prompting, allowing explicit intermediate reasoning steps, fits this multi-document synthesis task well.
- C) Chain-of-thought prompting is only useful for coding tasks and doesn't transfer to literature synthesis.
- D) The model cannot reason across multiple documents regardless of prompting approach.

**Question 26.** The platform wants to standardize prompt fragments (citation format, disclaimer language, formatting rules) across several different researcher-facing features so changes propagate consistently.

- A) Duplicate the fragments into each feature's prompt independently, since each system prompt should stay self-contained.
- B) Rely on prompt caching alone, since a cached system prompt already behaves like a shared fragment across features.
- C) Standardization across features isn't achievable through prompt design at all, and instead needs a separate, structured configuration service.
- D) Use modular, versioned prompt fragments shared across features — distinct from caching (cost/latency) or Skills (capability packaging).

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific figure from the correctly retrieved source document.

- A) Trust the fluent, well-formatted output as sufficient evidence that the extracted figure is correct.
- B) Verify extracted figures against the actual source excerpt rather than trusting confident, well-formatted phrasing.
- C) Increase output length across the board, on the theory that a longer answer leaves more room to get the figure right.
- D) Treat this as a pure model limitation with no architectural mitigation available on the platform side.

**Question 28.** The team debates whether researcher-facing latency SLAs should factor into model tier selection for the platform.

- A) Yes — weigh accuracy needs against the latency and cost the SLA can tolerate, rather than defaulting to the top tier.
- B) Latency should never factor into model or architecture decisions, since accuracy is the only dimension that matters here.
- C) Only raw cost should factor into tier selection, since latency is mainly a frontend concern rather than a model one.
- D) SLAs are purely a stakeholder-communication artifact with no real bearing on technical architecture.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, since a benchmark improvement is a deterministic predictor of better production behavior.
- B) Never upgrade the model once an initial version has been chosen, to keep production behavior permanently fixed.
- C) Upgrade immediately without testing, since a benchmark improvement alone is sufficient proof of a production gain.
- D) Pin the current version and test the new one against the platform's own evaluation suite before deliberately upgrading, since behavior can shift across releases even when benchmarks improve.

**Question 30.** The platform's context budget is a concern because the system prompt/citation rules and the retrieved excerpts must fit alongside room for a detailed, well-cited answer.

- A) Input and output token budgets are entirely independent line items that never compete with each other.
- B) This tradeoff only matters for unusually long source documents, not for the platform's typical queries.
- C) Input and output share one context-window budget, so retrieved-content volume must be balanced against room for a detailed answer.
- D) Output length has no practical limit regardless of how much retrieved content the input side consumes.

---

## Scenario C: Evaluation and Optimization of an HR Recruiting Assistant (Questions 31–45)

A Claude-powered recruiting assistant screens resumes, drafts outreach messages, and answers candidate questions for TalentBridge, a mid-market staffing firm. It has been in production for four months, and you are responsible for the evaluation strategy, diagnosing quality regressions, and optimizing the cost/latency/accuracy tradeoff as volume grows.

---

**Question 31.** TalentBridge's team currently measures only resume-screening throughput and hasn't defined targets for latency, cost, or fairness.

- A) Throughput alone is sufficient, since it directly reflects the assistant's primary purpose.
- B) Define accuracy, latency, cost, and safety/fairness as first-class metrics, since failing on any one of them still means the assistant fails overall.
- C) Latency and cost are operations-team concerns that shouldn't be part of the evaluation design itself.
- D) Fairness metrics only need to be defined once a complaint has actually been filed against the system.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past candidate resumes.

- A) A single automated method against a fixed labeled set is sufficient for any production system at this scale.
- B) Replace the automated checks entirely with human review, dropping the automated layer altogether.
- C) Expand the labeled set indefinitely, treating dataset size as the sole lever for improving evaluation quality.
- D) Mix methodologies — automated checks for scale, human review for judgment calls, adversarial tests for bias-relevant edge cases — since no one method covers every failure mode.

**Question 33.** The team wants to test whether a new outreach-message prompt improves candidate response rate before rolling it out to all traffic.

- A) Roll out the new prompt to all traffic immediately, then monitor production metrics afterward for problems.
- B) A/B test the prompt change alone against a stable baseline so any difference can be attributed to it.
- C) Change the prompt and the model tier at the same time, to maximize the chance of seeing an improvement.
- D) Skip a formal test, since outreach-message wording changes are inherently low-risk to candidates.

**Question 34.** A candidate's screening summary misstates their years of relevant experience. Investigation shows the resume was parsed and retrieved correctly, and the model's response paraphrased the experience section inaccurately.

- A) This is a retrieval problem, so the fix should focus on the resume-parsing pipeline rather than on the summary text itself.
- B) This is a generation-side issue — inaccurate paraphrasing of correctly retrieved content — calling for prompt or output-validation fixes.
- C) This is a model mismatch requiring a different, more capable model tier, regardless of what the specific underlying failure turns out to be.
- D) This cannot be diagnosed without retraining the model from scratch on the affected resume category.

**Question 35.** Immediately after a scheduled refresh of the job-requisition database, the assistant starts recommending mismatched candidates, while model version and average latency are unchanged.

- A) Suspect the model provider silently updated the underlying model version behind the scenes.
- B) Suspect a change to a generation-side setting, since the mismatches look somewhat erratic in nature.
- C) Investigate the retrieval/indexing layer first, since the regression tracks the data-refresh event specifically.
- D) Suspect the context window available to the model shrank during the same maintenance window.

**Question 36.** The team wants to reduce cost and latency in the screening pipeline but is worried about hurting candidate-match accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, without weighing how a change in one affects the others.
- B) Optimize the three jointly against the system's actual SLA and budget, since the cheapest configuration that fails the accuracy bar is no better than an unaffordable one that maximizes accuracy.
- C) Accuracy should always be maximized first, with cost and latency addressed only afterward if budget allows.
- D) This tradeoff can't be measured with data currently available, so any change here is effectively a guess.

**Question 37.** Production monitoring currently reports only an overall weekly average match-quality score.

- A) Add per-role or per-source breakdowns to surface drift and outliers hidden inside the aggregate.
- B) A single aggregate average is sufficient for production monitoring at TalentBridge's current volume.
- C) Monitoring should track only cost going forward, since match quality is already fully captured by the offline eval suite alone.
- D) Weekly granularity is always sufficient, regardless of how quickly a given failure mode develops.

**Question 38.** The team proposes cutting human review of flagged low-confidence screening decisions by 80%, citing a 96% aggregate accuracy score.

- A) Proceed with the cut based on the 96% aggregate figure alone, since it clears a normal accuracy bar.
- B) Aggregate accuracy is by definition representative of every individual role and candidate segment the assistant screens.
- C) Human review should never be reduced, regardless of what the measured accuracy figures show over time.
- D) Segment accuracy by role and source first, since the aggregate can mask a segment performing far worse than average.

**Question 39.** An A/B test shows a new screening prompt improves throughput, but the team hasn't checked whether it also changed the false-negative rate for genuinely qualified candidates who should have advanced.

- A) Throughput alone is a sufficient signal to ship the change to all traffic.
- B) Ship the change now and monitor informally after the fact, rather than testing the false-negative rate beforehand.
- C) Check the qualified-candidate false-negative rate specifically, since a throughput gain could mask an increase in inappropriately filtered strong candidates.
- D) False-negative behavior on qualified candidates isn't something the current evaluation setup is designed to measure at all.

**Question 40.** The team wants to diagnose why a subset of screening summaries are factually accurate but rated poorly by hiring managers.

- A) Assume the accuracy metric itself is broken and discard it in favor of hiring-manager ratings alone.
- B) Investigate a dimension beyond accuracy, like tone, completeness, or actionability, since the current eval doesn't measure them.
- C) Increase the model's capability tier, on the assumption that higher capability will automatically improve hiring-manager satisfaction scores.
- D) Ignore the hiring-manager ratings going forward and report only the accuracy metric.

**Question 41.** The team is optimizing token usage and notices the system sends the full conversation history plus a large static compliance-policy document on every turn of multi-turn candidate conversations.

- A) Cache the static compliance-policy document and trim or summarize older conversation turns to cut redundant token cost.
- B) Switch to a smaller model as the only lever considered for reducing token cost in these conversations.
- C) Remove the compliance-policy document from the prompt entirely to save tokens on every turn.
- D) This workflow has no real optimization opportunity, since sending the full history and policy text every turn is unavoidable.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself already a sufficient observability strategy for a system at this scale.
- B) Reduce logging volume to save storage cost, without changing anything else about how the logs are used.
- C) Move to structured, aggregable signals — sampling, tagged failure categories, per-segment quality metrics — since raw logs at volume aren't reviewable on their own.
- D) Observability requires no particular structure, as long as the raw data is retained somewhere for later reference.

**Question 43.** The team wants to identify whether a recent quality regression was caused by a prompt change, a model version change, or a job-requisition data change — all three happened in the same week.

- A) Assume the most recently shipped of the three changes is always the actual cause of the regression.
- B) Attribution becomes impossible once multiple changes have shipped in the same week, so the investigation should be dropped.
- C) Revert all three changes immediately, without investigating which one, if any, actually caused the regression.
- D) Isolate and re-test each change independently, which is exactly why changes should normally ship one variable at a time.

**Question 44.** An automated eval asserts that an outreach-message draft must exactly match a fixed reference string, and the eval fails intermittently even on drafts a human reviewer would call correct.

- A) Exact-string-match evals don't fit non-deterministic LLM output; check for required content/structure instead of exact text.
- B) The model is malfunctioning and needs to be retrained before the eval can be trusted again.
- C) The reference string used by the eval needs to be made longer and more detailed.
- D) A generation setting like temperature should be adjusted downward to fix these intermittent, hard-to-reproduce eval failures.

**Question 45.** Leadership wants a single number to represent "how good" the recruiting assistant is, to track over time.

- A) A single number is always achievable and sufficient on its own for tracking any system's evaluation needs.
- B) Use throughput alone as the single number, since it maps most directly to the assistant's stated purpose.
- C) Refuse to provide any single summary metric at all, regardless of how leadership plans to use it.
- D) Offer a top-line aggregate but pair it with segment- and dimension-level detail (accuracy, latency, cost, fairness) so it can't mask a failing area.

---

## Scenario D: Governance and Enablement for a Public-Sector FedRAMP Deployment (Questions 46–60)

The Department of Civic Records Modernization (DCRM), a state-level public-sector agency pursuing a FedRAMP Moderate authorization, is deploying a Claude-powered system that helps citizens navigate benefits applications, alongside a 25-person internal engineering team using Claude Code to build and maintain it. You are responsible for governance, ATO-relevant compliance, and developer enablement for the launch.

---

**Question 46.** DCRM's architecture team is finalizing data-boundary, retention, and access-logging design in the final weeks before the ATO assessment, after core application logic is already built.

- A) This sequencing carries no real risk, since compliance controls can generally be added right before an ATO review.
- B) Compliance only affects the documentation submitted for the ATO package, not the system's actual architecture.
- C) HIPAA, not FedRAMP, is the relevant regulatory regime for a state benefits agency of this kind.
- D) FedRAMP-driven data-boundary and access-control requirements can force structural changes far costlier to retrofit late than to design in from the start, which is the risk this sequencing runs.

**Question 47.** A team proposes requiring human approval on every single response the citizen-facing benefits assistant produces, framing it as the safest governance posture.

- A) Maximal human review on every output is always the correct default posture for public-sector AI systems.
- B) Human reviewers are categorically less accurate than the model on this task, making universal review counterproductive.
- C) Blanket human-in-the-loop on every output defeats much of the system's value; target HITL at high error-cost or judgment-requiring decisions instead.
- D) This universal-review approach is a specific, named requirement of FedRAMP itself, independent of the system's actual risk profile or decision stakes.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from citizen-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need architectural attention once at least one has actually been observed in production.
- B) These three risk categories are specific to non-government deployments and don't meaningfully apply here.
- C) A single generic guardrail, applied once, addresses hallucination, injection, and inconsistent output equally well.
- D) Design a mitigation for each failure mode up front, matching mechanism to risk rather than reacting after the fact.

**Question 49.** Program staff ask whether the assistant's eligibility-guidance responses could produce disparate outcomes across different applicant demographics.

- A) This isn't an architectural concern at all; it belongs entirely to legal/compliance review after launch.
- B) Disparate impact is structurally impossible in an LLM-based system, by the nature of how the model was trained.
- C) This kind of concern only applies to systems making final, binding eligibility determinations, not an assistive one.
- D) Treat bias and fairness as architecture concerns: check whether training/eval data reflects the served population, and measure for disparate impact rather than assuming it's absent.

**Question 50.** The 25-person engineering team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Have each staff member individually troubleshoot and reconfigure their own local development environment.
- B) Standardize the CLAUDE.md hierarchy and shared MCP server configuration at the team/project level.
- C) Restrict Claude Code usage across the team to a single designated engineer, to reduce configuration variance.
- D) Accept the inconsistency as an unavoidable cost of adopting AI-assisted development tooling at this team size.

**Question 51.** The team wants Claude Code-generated code changes in this FedRAMP context to go through the same review rigor as any other change to an authorized system.

- A) AI-assisted code should bypass the standard review process entirely, on the reasoning that it was "written by AI" rather than a person on the team.
- B) Only a light spot-check of AI-generated code is necessary before it merges into the authorized system.
- C) Standard SDLC practices still apply; Claude Code assisting with generation doesn't reduce the review rigor an authorized system requires.
- D) Review requirements should be set lower for AI-generated code than for equivalent human-written code.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Triage it like any incident: use traces/logs to isolate whether the integration layer or the code/model output is at fault.
- B) Disable Claude Code for the entire team as a standing response to this one incident.
- C) Roll back every recent Claude Code-assisted change across the team, without validating which one actually caused the incident.
- D) Assume the bug lives in the generated code and skip investigating the integration layer.

**Question 53.** The engineering team wants a documented, repeatable workflow for a recurring task (generating a weekly ATO-evidence summary) versus a one-off exploratory coding task.

- A) Package the recurring report as a Skill for consistent reuse; leave the one-off task unstructured, since it doesn't need standing infrastructure.
- B) Build both the recurring report and the one-off task as ad hoc, undocumented prompts recreated each time they're needed.
- C) Build both the recurring report and the one-off task as dedicated MCP servers, regardless of reuse frequency.
- D) Recurring workflows and one-off exploratory tasks should always be built with identical amounts of structure.

**Question 54.** The compliance office wants documented evidence of who accessed what citizen data through the system and when, as part of the ATO evidence package.

- A) Access logging is optional as long as the system already validates users through role-based permissions elsewhere.
- B) Audit logging can be added to the system later, once the ATO package is submitted, without any architectural impact.
- C) Only failed access attempts need to be captured in the audit trail; successful, authorized access doesn't.
- D) Design access-control and audit-logging as explicit architectural components meeting identity, authorization, and monitoring requirements, not an implicit byproduct of normal operation.

**Question 55.** The steering group for this deployment includes program office, ATO assessors, and engineering stakeholders with different priorities and vocabularies.

- A) Tailor architectural communication to each audience, framing tradeoffs in terms each group can evaluate against its own priorities.
- B) Communicate primarily with the engineering stakeholders, and let them relay the relevant details to program office and the assessors.
- C) Skip stakeholder communication until the system is fully built and ready for its ATO assessment.
- D) Use identical, engineering-oriented technical documentation for all three audiences to save preparation effort.

**Question 56.** Midway through the project, eligibility requirements shift meaningfully based on new state regulatory guidance.

- A) Refuse to incorporate the change, since the original requirements were already agreed upon with stakeholders.
- B) Incorporate the change into the build silently, without informing stakeholders of its downstream impact.
- C) Re-engage discovery for the affected scope, communicate the tradeoff to stakeholders, and adjust design and timeline accordingly.
- D) Restart the entire project from scratch, regardless of how much of the existing, already-approved design the new guidance actually affects.

**Question 57.** After launch, the architect's involvement is discussed as ending once the system passes its ATO assessment.

- A) This is the correct lifecycle model; monitoring and iteration afterward are entirely the operations team's responsibility from then on.
- B) Lifecycle responsibility ends the moment the ATO is formally granted.
- C) Lifecycle management continues through monitoring and iteration on production signal, not just discovery through authorization.
- D) Monitoring only becomes necessary if and when a major incident actually occurs.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation, a structured list of final values, is sufficient for a future engineering team.
- B) Documenting the reasoning behind configuration choices is unnecessary overhead in an already heavily regulated environment.
- C) Capture the "why" too — compliance drivers, tradeoff reasoning — so a future team can extend the system without re-deriving that context from scratch on their own.
- D) Only the original architect should ever be allowed to modify the system, which makes further documentation moot.

**Question 59.** The engineering team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves meaningful time on every task category without needing to check.
- B) Evaluate specific task categories for genuine friction reduction versus cases where review overhead may exceed the time saved.
- C) Mandate Claude Code usage across all task categories, regardless of whether a measured benefit shows up.
- D) Ban Claude Code for all documentation and exploration tasks outright, without first evaluating where it actually helps the team.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) Treat this as an acceptable ongoing inefficiency, since no architectural fix is available for this kind of duplicated effort.
- B) Document the triage process as shared operational knowledge, so engineers stop independently re-deriving the same integration-versus-model-output distinction from scratch each time.
- C) Restrict integration debugging across the team to a single designated engineer going forward.
- D) Conclude that the issue can only be resolved by switching the team to a different tool entirely.

---
# Answer Key

**Quick key:** 1-B, 2-C, 3-C, 4-C, 5-A, 6-D, 7-A, 8-B, 9-D, 10-C, 11-A, 12-C, 13-D, 14-C, 15-B, 16-B, 17-D, 18-A, 19-A, 20-B, 21-D, 22-A, 23-A, 24-A, 25-B, 26-D, 27-B, 28-A, 29-D, 30-C, 31-B, 32-D, 33-B, 34-B, 35-C, 36-B, 37-A, 38-D, 39-C, 40-B, 41-A, 42-C, 43-D, 44-A, 45-D, 46-D, 47-C, 48-D, 49-D, 50-B, 51-C, 52-A, 53-A, 54-D, 55-A, 56-C, 57-C, 58-C, 59-B, 60-B

---

**1. B** — The stated goal (more volume, same headcount, unchanged review time) is an efficiency problem, so naming that pillar shapes both the architecture and its metrics. A assumes a transformation narrative that discovery didn't actually support; C substitutes a different pillar than the one leadership named; D skips framing instead of using what discovery surfaced.

**2. C** — Steps that vary by document type and depend on findings discovered along the way are the defining case for an agentic pattern. A assumes a predictability the scenario lacks; B undersells the orchestration a single enhanced call can't provide here; D treats genuinely different patterns as interchangeable.

**3. C** — Hub-and-spoke routing through the coordinator preserves observability and consistent error handling. A and D sacrifice these properties for a shortcut; B discards the specialization that motivated separate subagents in the first place.

**4. C** — Every subagent succeeding while whole document formats are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, B, and D all patch downstream instead of fixing the actual scope gap in the coordinator's routing.

**5. A** — Business value pillars (efficiency, risk reduction, cost, defensibility) give both the architecture and its metrics a clear anchor. B, C, and D all skip, misassign, or defer this framing in ways that risk building toward the wrong measure of success.

**6. D** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and B treat it as out of scope for the architecture; C overreacts to sentiment alone without weighing it against the stated volume goal.

**7. A** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. B and C withhold the reasoning stakeholders actually need; D removes a deliberate, justified difference for a simplicity that doesn't hold up at the described error stakes.

**8. B** — Adding a feedback loop that captures attorney overrides and outcomes as a first-class architectural component is what lets the system improve after deployment. A, C, and D all treat that component as optional, someone else's concern, or something to defer indefinitely.

**9. D** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and C over-engineer a simple augmentation need by importing structure from the platform's other workflows; B is factually wrong about what the pattern requires.

**10. C** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not writing around it. A and B ignore this real degradation; D reaches for the wrong lever, since the problem is toolset scope, not context capacity.

**11. A** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (classification) completes, reducing latency without sacrificing correctness. B and C misstate real constraints on the architecture; D avoids the sequencing question rather than answering it.

**12. C** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A gives too little of the relevant detail; B gives too much of the wrong kind of detail; D skips the communication need entirely in favor of a demo.

**13. D** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, B, and C understate or misstate this real architectural tradeoff.

**14. C** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A ignores a known future need entirely; B wastes effort guessing at requirements that don't exist yet; D blocks current delivery over information that isn't available yet.

**15. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave the actual knowledge-transfer gap unaddressed.

**16. B** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and C ignore fit-to-task; D sacrifices cost and latency on the majority of questions that never needed the top tier.

**17. D** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, B, and C all misstate or break the caching opportunity described.

**18. A** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. B and D ignore this mismatch; C discards useful structured data instead of indexing it appropriately.

**19. A** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions — is the correct architecture. B and C force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction between query types.

**20. B** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, C, and D all reintroduce the failure mode the fix is meant to prevent.

**21. D** — Presenting both figures with attribution and likely methodological explanation preserves the actual information for the reviewer rather than resolving a real discrepancy arbitrarily. A, B, and C all discard or obscure a genuine data conflict instead of surfacing it.

**22. A** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift regardless of emphasis. B and C are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently of any one of them. B, C, and D all fail the reuse or maintainability requirement the scenario describes.

**24. A** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. B and C ignore the real context cost of the monolithic approach; D removes a needed capability entirely rather than scoping how it's exposed.

**25. B** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. A, C, and D all misstate the fit or capability of prompting techniques for this kind of task.

**26. D** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; B conflates two distinct mechanisms; C denies a real, common architecture pattern.

**27. B** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; C doesn't address correctness at all; D incorrectly claims no architectural mitigation exists for a fixable problem.

**28. A** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. B, C, and D each drop a relevant factor from the decision.

**29. D** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and C assume benchmark gains transfer automatically to this workload; B over-corrects into permanent stagnation instead of a deliberate upgrade process.

**30. C** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and D all misstate this real, architecture-relevant constraint.

**31. B** — Accuracy, latency, cost, and safety/fairness should all be defined as first-class metrics, since a system failing on any of them fails overall even if it screens quickly. A, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. D** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially bias-relevant edge cases. A, B, and C each over-rely on or discard one method without addressing the actual coverage gap.

**33. B** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; C confounds two variables at once; D dismisses a real risk without evidence to support doing so.

**34. B** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt or output-validation fixes rather than retrieval or model-tier changes. A and C misdiagnose which layer is at fault; D avoids diagnosis entirely in favor of an expensive default.

**35. C** — A regression tied specifically to a data-refresh event, with model and latency unchanged, points first at retrieval/indexing. A, B, and D would not specifically correlate with a requisition-database refresh the way the retrieval layer does.

**36. B** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and C optimize dimensions in isolation; D claims the tradeoff is unmeasurable when the data needed to measure it can actually be collected.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and D accept a monitoring blind spot at the current volume; C drops accuracy monitoring from observability entirely in favor of cost alone.

**38. D** — Segmenting accuracy by role and candidate source before cutting review protects against a failing segment hiding behind a healthy aggregate. A and B trust the aggregate figure uncritically; C over-corrects by refusing any reduction regardless of what segmented evidence would show.

**39. C** — An isolated throughput improvement could mask a worsened false-negative rate on qualified candidates; checking specifically for that before shipping is the correct diagnostic step. A and B ship without adequate testing beforehand; D incorrectly claims the failure mode is unmeasurable with the tools already in place.

**40. B** — "Accurate but poorly rated" points at an unmeasured quality dimension (tone, completeness, actionability) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; C assumes a fix without first diagnosing the actual gap.

**41. A** — Caching the static compliance-policy document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. B reaches for a blunter, quality-risking lever before a more targeted fix; C removes content the conversation still needs; D denies an optimization opportunity that clearly exists.

**42. C** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and D accept the described dysfunction as sufficient; B addresses storage cost, not the actual observability gap.

**43. D** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and C guess without evidence; B gives up on a solvable, if effortful, diagnostic problem.

**44. A** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. B and D misdiagnose ordinary generation variability as a malfunction; C doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request outright.

**46. D** — FedRAMP-driven requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate the real architectural impact; C misidentifies the applicable regulatory regime for this deployment.

**47. C** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal case for maximal review; D misattributes this requirement to FedRAMP, which isn't what the regime actually mandates.

**48. D** — Designing a matched mitigation for each known failure mode up front — grounding for hallucination, isolation/guardrails for injection, output checks for consistency — is the architecture-first approach the domain calls for. A defers to a reactive posture; C assumes one guardrail covers distinct risk types; B is factually wrong about where these risks apply.

**49. D** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; B and C make unsupported blanket claims about where disparate impact can occur.

**50. B** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. A and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team instead of fixing the root cause.

**51. C** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in an authorized system. A, B, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. A** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. C and D skip diagnosis in favor of a broad reaction; B is disproportionate and doesn't investigate the actual cause of this one incident.

**53. A** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. B under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice at all.

**54. D** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and C each understate what ATO-grade audit evidence actually requires.

**55. A** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by program-office, assessor, and engineering audiences alike. B, C, and D each fail to serve at least one audience's real information need.

**56. C** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally driven requirements shift. A and B mishandle a real, unavoidable change; D disproportionately discards unaffected work along with the affected scope.

**57. C** — Lifecycle management extends through monitoring and iteration based on production signal, not just through discovery and authorization. A, B, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. C** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and D all leave that reasoning undocumented and effectively lost to future maintainers.

**59. B** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and C over-assume benefit without checking; D forecloses a potential benefit without evaluating it first.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 7.*
