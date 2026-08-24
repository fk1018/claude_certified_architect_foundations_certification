# CCARP Practice Exam 3

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent E-Discovery Platform, Pharmaceutical RAG and Model Tiering, HR Recruiting Assistant Evaluation & Optimization, Public-Sector FedRAMP Governance & Enablement) |
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

Harlow & Voss LLP, a 400-attorney litigation firm, is building a multi-agent e-discovery platform to review, classify, and produce documents for active matters. The platform must handle document intake/OCR, responsiveness classification, privilege review, redaction, and production formatting across matters governed by different protective orders. You are the architect responsible for the end-to-end design and for running discovery with litigation-support staff and partner stakeholders.

---

**Question 1.** Discovery reveals the firm's actual goal is reducing the per-matter cost of first-pass document review by using fewer contract attorneys, while maintaining the same review turnaround time — not adding entirely new review capabilities.

- A) Frame the architecture around transformation, treating AI-assisted review as inherently transformative regardless of the stated cost objective.
- B) Frame the architecture around performance SLAs exclusively, since turnaround time is historically the only metric litigation partners track.
- C) Frame the architecture around new capability, since first-pass review didn't previously use AI and the shift itself justifies novel-capability framing.
- D) Frame the architecture around cost/efficiency, with success metrics tied to cost-per-document and reviewer headcount.

**Question 2.** Document intake, responsiveness classification, privilege review, and redaction each require different steps depending on document type, matter-specific protective order terms, and findings from prior steps (e.g., a privilege hit changes downstream handling).

- A) Use an agentic pattern, since needed steps vary by document type and depend on prior findings.
- B) Use a fixed, linear workflow, since intake, classification, privilege review, and redaction always occur as one standardized sequence in litigation practice.
- C) Use a single augmented LLM call, since one enhanced prompt with retrieval can substitute for coordinated multi-step handling in this case.
- D) Use whichever pattern the vendor ships fastest, since the patterns produce interchangeable outcomes for this kind of review.

**Question 3.** In the proposed coordinator/subagent design, the privilege-review subagent identifies a document as privileged and needs the redaction subagent to apply redactions before production.

- A) Route the privilege determination through the coordinator, which dispatches to the redaction subagent.
- B) Let the privilege-review subagent call the redaction subagent directly, since a direct hand-off saves a coordination hop and reduces latency.
- C) Merge privilege review and redaction into a single subagent, since combining reduces the number of hand-offs the architecture must coordinate.
- D) Have every subagent broadcast its findings to all other subagents, so no coordinator bottleneck can ever form in the pipeline.

**Question 4.** Every subagent completes its assigned work correctly, but the responsiveness-classification and privilege-review subagents each independently re-run OCR on the same intake documents, since neither receives the intake subagent's OCR output.

- A) Add a fifth subagent dedicated to OCR deduplication, layering a new component on top of the existing hand-off gap instead of closing it.
- B) Give the intake subagent tool access to write directly into each downstream subagent's private context, bypassing the coordinator's data flow.
- C) Fix the coordinator's data flow so intake's OCR output passes downstream to each subagent that needs it.
- D) Increase the context window of the responsiveness-classification subagent so it can regenerate OCR output faster.

**Question 5.** Discovery with partners surfaces that what actually worries them is defensibility of privilege calls in front of a judge, not raw review speed or cost.

- A) Ignore this and keep the cost-per-document framing, since cost was the pillar named in the original engagement letter and discovery came later.
- B) Treat defensibility as identical to cost efficiency, since both ultimately reduce the firm's exposure to downstream litigation risk.
- C) Reframe the pillar toward auditability/defensibility, with metrics for accuracy, explainability, and privilege-call audit trails.
- D) Add defensibility as a documentation footnote, keeping the original cost-based metrics and design unchanged.

**Question 6.** Discovery interviews reveal review attorneys are worried the AI will be used as the sole justification for withholding documents without attorney sign-off, exposing the firm to sanctions risk.

- A) Ignore the sentiment since it's a change-management issue that has no bearing on subagent design or the escalation path.
- B) Proceed with full automation of withholding decisions and address attorney sentiment only through a communications campaign afterward.
- C) Treat this as a real constraint and add a human-in-the-loop checkpoint before any document is withheld from production.
- D) Recommend the firm abandon the AI review project entirely based on this sentiment alone, without weighing the technical case.

**Question 7.** A partner asks why the privilege-review subagent uses a higher-capability model tier than the intake/OCR subagent.

- A) Explain the tradeoff: privilege determination needs nuanced legal reasoning that justifies the added cost, while OCR is comparatively mechanical.
- B) Say the higher tier is used everywhere to be safe, regardless of what each subagent's task actually requires.
- C) Avoid explaining the difference, since partners don't need technical detail about model tier selection.
- D) Say the tier choice was arbitrary and any subagent's model tier could be swapped for a cheaper one without measurably changing privilege-call accuracy.

**Question 8.** The current design produces final privilege/responsiveness calls with no mechanism to capture reviewing-attorney overrides for future improvement.

- A) This is acceptable; the initial classifier already reflects current best practice and won't need revision.
- B) Feedback loops are purely a data-science concern that sits outside the architecture, so no hook or capture mechanism belongs in this design.
- C) Defer any feedback mechanism to an undefined future phase, with no design hooks captured in the current architecture.
- D) Add a feedback loop with explicit hooks capturing attorney overrides and their reasons as a first-class architectural component.

**Question 9.** A partner wants a single enhanced call — with retrieval over a matter's document set — to answer a quick question like "do we have any emails between X and Y," without multi-step autonomous orchestration.

- A) Use an augmented LLM pattern, since a single retrieval-enhanced call fits this quick-lookup need without multi-step orchestration.
- B) This requires the full multi-agent e-discovery pipeline, since any retrieval-backed question should route through the same coordinator regardless of scope.
- C) This cannot be done with Claude at all, since answering with retrieval requires a dedicated agent framework outside the model.
- D) This requires a fixed workflow with at least five sequential steps, since retrieval-backed answers always need a structured pipeline.

**Question 10.** The intake/OCR subagent's toolset has grown to include billing-code lookup and calendar-scheduling tools unrelated to document intake.

- A) This has no downside as long as the prompt is well-written enough to describe every tool's intended use case.
- B) This capability bloat degrades tool-selection reliability; unrelated tools should be removed or relocated.
- C) More tools always increase flexibility and should be encouraged across every subagent regardless of role.
- D) The fix is to enlarge the subagent's context window so it can reason through the larger tool list.

**Question 11.** The coordinator currently runs responsiveness classification and privilege review sequentially for each document, though neither depends on the other's output once intake/OCR completes.

- A) Run responsiveness classification and privilege review as independent, parallel subagent calls once intake completes.
- B) Sequential processing is required for defensibility in litigation, since a judge could question any concurrently produced call.
- C) Parallelization isn't possible in a coordinator/subagent architecture once more than one subagent needs the same upstream output.
- D) Combine both into a single subagent so the sequencing question never has to be answered at all.

**Question 12.** The firm's managing partners, unfamiliar with technical detail, ask how the e-discovery architecture should be described to the executive committee.

- A) Present only model names and token costs, treating that as the full extent of what the committee needs from a system prompt configuration.
- B) Present the full technical architecture diagram with no simplification, so the committee sees every subagent and tool boundary in full detail.
- C) Skip a high-level description and go straight to a live demo of the intake-to-production pipeline.
- D) Describe the pipeline end-to-end at a level the committee can evaluate against cost, risk, and turnaround, without implementation detail.

**Question 13.** A competing vendor proposes one generalist agent holding every tool (OCR, classification, privilege review, redaction, production formatting) instead of a coordinator with specialized subagents.

- A) A single generalist agent holding every tool is more likely to suffer degraded tool-selection reliability than specialized subagents.
- B) A single generalist agent scales better as tool count grows, since one context window can index every tool without coordination overhead.
- C) Specialized subagents are strictly a cost-increasing choice with no reliability benefit over one agent holding every tool.
- D) There's no meaningful architectural difference between the two approaches once both are given the same underlying model tier.

**Question 14.** The platform must eventually support foreign-language document review, a matter type planned for next year, but detailed requirements aren't finalized.

- A) Build full foreign-language support now, guessing at requirements that legal, compliance, and litigation support haven't finalized for next year's matter type.
- B) Ignore future foreign-language needs entirely until requirements are formally scoped by the litigation team.
- C) Refuse to proceed with the current phase of the platform until every future requirement is finalized in writing.
- D) Design the current decomposition and subagent/tool boundaries with reasonable extensibility, without over-building for undefined requirements.

**Question 15.** The steering committee wants documentation a new engineering team can use to extend the system next year without the original architect present.

- A) Document only final configuration values, since a well-organized implementation is self-explanatory to a new team.
- B) Rely on the original architect remaining available indefinitely for every future question, instead of documenting the reasoning behind pattern and tier choices.
- C) Documentation is unnecessary if the code and subagent boundaries are already cleanly organized.
- D) Document the architecture and the reasoning behind key decisions — pattern choices, decomposition boundaries, tier selections.

---

## Scenario B: RAG and Model Tiering for a Pharmaceutical Literature-Review Platform (Questions 16–30)

Aventra Biosciences' medical affairs team needs Claude to answer scientist questions using both general reasoning and retrieval over a large, constantly-updated corpus of clinical trial protocols, published literature, and internal study reports. You are architecting model selection, prompting, and the integration layer.

---

**Question 16.** Most scientist questions are moderately complex; a small fraction require deep multi-step reasoning across many studies, and a small fraction are simple lookups (e.g., "what was the primary endpoint in Study 204").

- A) Always use the highest-capability tier, guaranteeing quality on every question regardless of its actual complexity.
- B) Always use the fastest tier to minimize cost, accepting some quality loss even on the multi-step reasoning cases.
- C) Route by task difficulty — fast tier for lookups, balanced tier for typical questions, higher-capability tier reserved for deep multi-step cases.
- D) Use one fixed model tier for all questions, since switching tiers mid-session adds engineering complexity the platform doesn't actually need to take on.

**Question 17.** Every request sends the same long system prompt (scientific-writing persona, citation format, disclaimer language) followed by retrieved excerpts that vary per query.

- A) Order doesn't affect cost or latency here, since API output is already deterministic and caching wouldn't change token costs.
- B) Put retrieved content first, since it's the most relevant part of the prompt for the specific query being answered.
- C) Place the stable system prompt first and enable prompt caching, with varying retrieved content after it.
- D) Alternate system prompt instructions and retrieved content throughout the prompt so each excerpt stays near its relevant instruction.

**Question 18.** The corpus mixes long-form clinical study reports with short structured data (a table of adverse-event rates by treatment arm).

- A) One chunking/indexing strategy tuned for long-form documents can serve short structured records equally well without adjustment.
- B) Use the largest possible chunk size for everything, avoiding the need to maintain multiple chunking strategies.
- C) Match chunking and indexing to each data shape — long-form reports need different treatment than short tabular records.
- D) Structured adverse-event data should be excluded from retrieval entirely, since only long-form narrative content benefits from indexing.

**Question 19.** Scientist queries range from exact lookups ("primary endpoint for Study 204") to conceptual questions ("how has the safety narrative for Compound X evolved across trials").

- A) Use only embedding similarity search for every query type, from exact lookups to broad conceptual questions.
- B) Use only structured/metadata filtering for every query type, including open-ended conceptual questions about how a compound's safety narrative evolved across trials.
- C) Match retrieval strategy to query pattern — metadata filtering for exact lookups, embedding search for conceptual questions, hybrid where both are needed.
- D) Query pattern doesn't affect which retrieval approach is appropriate, since embeddings alone can resolve exact-match lookups just as reliably.

**Question 20.** Scientists need citations that reliably map each claim to a specific study and section, and generic prose responses often lose this mapping.

- A) Require structured output pairing each claim with its source study and section, so citation mapping survives synthesis.
- B) Ask the model, in prose, to always cite sources without any further mechanism enforcing the mapping.
- C) Add a structured-looking citation after the fact by searching for a plausible source matching each claim already written.
- D) Append a general bibliography of consulted documents at the end of the response instead of a per-claim schema mapping.

**Question 21.** Two retrieved sources disagree on a trial's reported adverse-event rate by a small margin — likely different analysis populations (intent-to-treat vs. per-protocol).

- A) Present both figures, annotated as a discrepancy with source attribution and the likely explanation (e.g., ITT vs. per-protocol).
- B) Average the two figures and present the blended number as the trial's adverse-event rate, since both sources are nominally about the same trial.
- C) Omit the adverse-event rate entirely from the response, since the two sources disagree.
- D) Always prefer whichever source was retrieved first, treating retrieval order as a stand-in for methodological reliability.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the JSON-only instruction more emphatically in the prompt, adding stronger language each time the preamble reappears.
- B) Use tool-use/schema-constrained output so structure is enforced by the API mechanism, rather than relying on prose instructions or a lower temperature setting alone.
- C) Post-process every response to strip any leading text before the first curly brace of the JSON schema.
- D) Increase max_tokens to leave room for both the conversational preamble and the JSON payload.

**Question 23.** The platform needs to connect to a proprietary internal study-repository system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond this literature-review platform.

- A) Build an MCP server exposing study-repository operations as tools/resources, reusable across the internal Claude-powered tools that need it.
- B) Hard-code the integration into this literature-review platform's application code only.
- C) Paste the entire study repository into every prompt sent to any of the internal tools, refreshing the pasted content whenever the repository changes.
- D) Require each consuming tool to reimplement its own study-repository integration independently.

**Question 24.** The team is deciding between exposing the full study catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Loading the full catalog up front is always preferable for completeness, regardless of how large the corpus grows.
- B) Progressive discovery, querying a catalog resource as needed, scales better than loading the entire catalog up front as the corpus grows.
- C) There's no meaningful difference in context cost between the two approaches at any corpus size.
- D) The catalog should never be exposed to the agent in any form, only to the application layer.

**Question 25.** A scientist asks a chain-of-thought-friendly question requiring the model to reason step by step across several retrieved studies before concluding.

- A) Zero-shot prompting with no reasoning guidance is equally effective for multi-study synthesis questions.
- B) Chain-of-thought prompting is only useful for coding and structured data-transformation tasks, not for literature synthesis across studies.
- C) The model cannot reason across multiple retrieved documents regardless of prompting approach used.
- D) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, suits this multi-study synthesis question.

**Question 26.** The platform wants to standardize prompt fragments (citation format, disclaimer language, formatting rules) across several different scientist-facing features so changes propagate consistently.

- A) Use modular, versioned prompt fragments shared across features — distinct from caching (cost/latency) or Skills (capability packaging).
- B) Duplicate the fragments into each feature's prompt independently, keeping a structured copy inside each feature's own codebase.
- C) Modular prompts are the same thing as prompt caching, so enabling caching accomplishes the standardization goal.
- D) Standardization across features isn't achievable through prompt design at all, only through a shared code library outside the prompt layer.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific figure from the correctly retrieved source document.

- A) Trust the fluent, well-formatted output as sufficient evidence that the cited figure is correct, since confident phrasing rarely appears alongside factual errors.
- B) This is purely a model limitation with no architectural mitigation available.
- C) Apply defensive validation — verify extracted figures against the actual source excerpt rather than trusting confident phrasing.
- D) Increase output length so there's more room for the model to state the correct figure.

**Question 28.** The team debates whether scientist-facing latency SLAs should factor into model tier selection.

- A) Latency should never factor into model or architecture decisions, regardless of the use case's SLA.
- B) Only cost should factor into tier selection, never latency, since cost is the sole business driver medical-affairs leadership tracks.
- C) Model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate.
- D) SLAs are purely a stakeholder-communication concern with no bearing on the technical tier-selection decision.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, since improved benchmark validation is always sufficient proof for production readiness.
- B) Pin the current version and evaluate the new release against the platform's own tests before deliberately upgrading.
- C) Never upgrade models once the initial version is chosen, regardless of what later benchmarks show.
- D) Upgrade immediately without testing, since benchmark improvements guarantee production improvements for this platform.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved study excerpts must fit alongside room for a detailed answer.

- A) Input and output share the same context-window budget, so retrieved-content volume must be balanced against room for a detailed answer.
- B) Output length has no practical limit regardless of how much retrieved content is placed in the input.
- C) This tradeoff only matters for very long documents, never for typical scientist queries.
- D) Input and output token budgets are entirely independent of each other within a single request, since each is billed and windowed separately.

---

## Scenario C: Evaluation and Optimization of an HR Recruiting Assistant (Questions 31–45)

A Claude-powered recruiting assistant screens resumes, drafts candidate outreach messages, and answers candidate FAQs for a mid-size tech company's talent acquisition team. It has been in production for six months, and you are responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only resume-screening throughput and hasn't defined targets for accuracy, latency, cost, or fairness.

- A) Define metrics spanning accuracy, latency, cost, and safety/fairness as first-class evaluation targets.
- B) Throughput alone is sufficient, since it's the system's stated primary purpose for the talent-acquisition team.
- C) Latency and cost are operations concerns unrelated to the evaluation design the team should own.
- D) Fairness metrics are only relevant once a complaint has actually been filed against a specific requisition, not before any incident occurs.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past resumes.

- A) A single automated method against a fixed labeled set is sufficient for any production system at this scale.
- B) Use mixed methodologies — automated eval for scale, human review for nuanced calls, adversarial testing for fairness-relevant paths.
- C) Replace the automated checks entirely with only human review of every screened resume, discarding the existing labeled-set infrastructure.
- D) Expand the labeled set indefinitely as the sole lever for improving evaluation coverage.

**Question 33.** The team wants to test whether a new screening-prompt version improves accuracy before rolling it out to all requisitions.

- A) Roll out the new prompt to all requisitions immediately and monitor for problems after the fact, treating production traffic itself as the test.
- B) Change the prompt and the model tier simultaneously to maximize the potential accuracy improvement.
- C) Skip testing entirely, since prompt changes produce deterministic output and are inherently low-risk compared to model changes.
- D) Run an A/B test changing only the prompt version against a stable baseline, isolating that one variable.

**Question 34.** A candidate is incorrectly screened out. Investigation shows the underlying resume was parsed and retrieved correctly, and the model's screening rationale misread a clearly-stated qualification.

- A) This is a retrieval/parsing problem, so the fix belongs in the ingestion pipeline regardless of what investigation showed.
- B) This cannot be diagnosed without retraining the underlying model from scratch.
- C) This is a model mismatch requiring a different model tier regardless of what the specific failure turned out to be.
- D) This is best characterized as a generation/reasoning issue, calling for prompt fixes or extra output checks rather than ingestion changes.

**Question 35.** Immediately after a scheduled update to the job-requisition template library, the assistant starts screening out qualified candidates at a higher rate, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider, even though no version-pin change was reported.
- B) Investigate the requisition-template/retrieval layer first, since the regression tracks the template update with model and latency unchanged.
- C) Suspect a temperature setting change, since screening behavior shifted around the same time as the update.
- D) Suspect the context window shrank, even though no configuration change to window size was made.

**Question 36.** The team wants to reduce cost and latency in outreach-message drafting but is worried about hurting quality, with no current data on where the configuration sits on that tradeoff curve.

- A) Optimize cost, latency, and quality independently, in isolation from one another and from the SLA.
- B) Optimize cost/latency/quality jointly against the system's actual SLA and budget, without letting a cost cut increase quality risk beyond what the SLA tolerates.
- C) Quality should always be maximized regardless of cost or latency implications, since candidate experience outweighs any budget constraint.
- D) This tradeoff cannot be measured at all, only guessed at without data.

**Question 37.** Production monitoring currently reports only an overall weekly average screening-accuracy score.

- A) Monitoring should surface drift and outliers via a per-role or per-requisition-type breakdown, not just an aggregate.
- B) A single aggregate weekly average is sufficient for production monitoring at this scale.
- C) Monitoring should track only cost, since accuracy is already fully captured by the offline eval suite.
- D) Weekly granularity is always sufficient regardless of how quickly a specific segment's accuracy degrades between reporting cycles, since averages smooth out short-term noise.

**Question 38.** The team proposes cutting human review of flagged low-confidence screens by 80%, citing a 96% aggregate accuracy score.

- A) Proceed with the review cut based on the 96% aggregate figure alone, without segmenting further or checking any specific requisition type.
- B) Segment accuracy by role and requisition type before cutting review, since the aggregate can mask a weak segment.
- C) Aggregate accuracy is definitionally representative of every role and requisition type it was averaged from.
- D) Human review should never be reduced regardless of what segmented accuracy figures eventually show.

**Question 39.** An A/B test shows a new screening-prompt version improves throughput, but the team hasn't checked whether it also changed the false-negative rate on genuinely qualified candidates from underrepresented backgrounds.

- A) Throughput alone is a sufficient signal to ship the change without checking any other metric.
- B) Check the fairness-related failure mode specifically before shipping, since a throughput increase could be masking a worse screen-out rate for one specific group.
- C) Fairness-related false-negative behavior is not something the evaluation suite can measure in this system.
- D) Ship the change and monitor informally after the fact instead of testing the fairness dimension beforehand.

**Question 40.** The team wants to diagnose why a subset of outreach messages are factually accurate but rated poorly by candidates in post-interaction surveys.

- A) Assume the accuracy metric itself is broken and discard it from the evaluation suite.
- B) Increase the model's capability tier, assuming higher capability always improves candidate perception scores.
- C) Ignore candidate satisfaction scores entirely in favor of the accuracy metric alone, since factual validation is the only dimension that matters.
- D) Investigate a dimension beyond factual accuracy, such as tone, personalization, or warmth, that the current eval doesn't measure.

**Question 41.** The team is optimizing token usage and notices the system sends the full candidate conversation history plus a large static company-policy/EEO-compliance document on every turn of multi-turn candidate chats.

- A) This has no optimization opportunity, since sending the full history and the full compliance document on every single turn is simply required.
- B) Switch to a smaller model as the only lever for reducing token cost on these conversations.
- C) Remove the compliance document entirely from the prompt to save tokens on every turn.
- D) Apply prompt caching to the static compliance document and trim or summarize older conversation turns to cut redundant cost.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy at this scale.
- B) Reduce logging volume to save storage cost, with no other change to how failures are surfaced.
- C) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment.
- D) Observability requires no structure as long as the raw data is retained somewhere for later review, since storage is cheap enough not to matter.

**Question 43.** The team wants to identify whether a recent quality regression was caused by a prompt change, a model version change, or an update to the resume-parsing library — all three shipped in the same week.

- A) Assume the most recent of the three changes is always the cause of the regression.
- B) Attribution is impossible once multiple changes have shipped in the same week, so no further investigation is worthwhile.
- C) Revert all three changes without investigation, regardless of which one, if any, actually caused the regression.
- D) Test one variable at a time — isolate and re-test each of the three changes independently rather than guessing.

**Question 44.** An automated eval asserts that an outreach-message draft must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining, since no further prompt validation could fix a nondeterministic reference-string mismatch.
- B) The reference string needs to be longer so more of the output has a chance to match.
- C) Exact-string-match evals are the wrong tool for non-deterministic LLM output; check for required content/structure instead.
- D) Temperature should be increased to fix the intermittent exact-match failures against the fixed reference string.

**Question 45.** Leadership wants a single number to represent "how good" the recruiting assistant is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs.
- B) Use screening throughput alone as the single number, since it's the system's stated purpose.
- C) Refuse to provide any single summary metric under any circumstances, even for executive reporting.
- D) A single aggregate metric can be a useful top-line indicator, paired with segment-level and multi-dimensional detail so it doesn't mask a failing area.

---

## Scenario D: Governance and Enablement for a Public-Sector FedRAMP Deployment (Questions 46–60)

A state health-and-human-services agency is deploying a Claude-powered system that processes benefits-eligibility case files under a FedRAMP Moderate authorization, and assists a 25-person caseworker operations team using Claude Code internally. You are responsible for governance, compliance, and developer enablement for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) This sequencing carries no risk, since compliance requirements like data residency and access logging can always be bolted on right before launch.
- B) Compliance only affects legal documentation, not the system's data-flow validation or logging architecture.
- C) HIPAA, not FedRAMP, is the relevant regime governing a public-sector benefits-eligibility system.
- D) FedRAMP-driven data residency, boundary, and access-logging requirements can force structural changes that are costlier to retrofit than to design in early.

**Question 47.** A team proposes requiring caseworker approval on every single output the eligibility system produces, framing it as the safest governance posture.

- A) Maximal human review on every output is always the correct default posture for a public-sector AI system.
- B) Blanket human-in-the-loop on every output defeats much of the system's value; target HITL at high error-cost or judgment-requiring decisions.
- C) Human reviewers are categorically less accurate than the model on eligibility determinations, making review of any output counterproductive.
- D) This blanket-review approach is required by the Privacy Act regardless of what the actual decisions involve.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from applicant-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed once they're actually observed in production, not during design.
- B) These risks are exclusive to private-sector deployments and don't apply to a public-sector benefits system.
- C) Design mitigations for each known failure mode up front — grounding for hallucination, input isolation for injection, and output checks for consistency.
- D) A single generic guardrail addresses hallucination, injection, and inconsistent output equally well.

**Question 49.** The agency's civil-rights office asks whether the system's eligibility recommendations could produce disparate outcomes across different applicant demographics.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review conducted after launch.
- B) Disparate impact is impossible in an LLM-based system by construction, regardless of the training data used.
- C) Bias, fairness, and transparency are architecture concerns — check whether training/eval data reflects the served population and measure for disparate impact.
- D) This concern only applies to systems making final, unreviewed determinations, not to any system with a human reviewer in the loop.

**Question 50.** The 25-person caseworker operations team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Restrict Claude Code usage to a single designated engineer to reduce configuration variance across the team.
- B) Have each staff member individually troubleshoot their own local configuration and MCP server setup.
- C) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level.
- D) Accept the inconsistency as an unavoidable cost of rolling out AI tooling across a 25-person team with varied local machine setups.

**Question 51.** The team wants Claude Code-generated code changes in this FedRAMP context to go through the same review rigor as any other change to an authorized system.

- A) AI-assisted code should bypass standard review, since a human didn't originally author every line of it.
- B) Only a spot-check of AI-generated code is necessary before it merges into the authorized system.
- C) Review requirements should be lower for AI-generated code than for human-written code in this environment.
- D) Standard SDLC practices — code review, testing, version control, change control — still apply regardless of how the change was generated.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without investigating the surrounding integration layer.
- B) Triage the same way any incident is triaged — isolate integration-layer versus code/model-output failure using traces and logs.
- C) Disable Claude Code for the entire team following this one incident, regardless of whether the root cause turns out to be integration or model output.
- D) Roll back all recent Claude Code-assisted changes, regardless of whether they're related to this incident.

**Question 53.** The caseworker operations team wants a documented, repeatable workflow for a recurring task (generating a weekly eligibility-determination audit report) versus a one-off exploratory data-migration script.

- A) Build both as standing MCP servers regardless of how often each one will actually be reused by the operations team.
- B) Build both as ad hoc, undocumented prompts each time either task needs to run.
- C) Recurring workflows and one-off exploratory tasks should be built with identical structure and tooling.
- D) Package the recurring report as a Skill for consistent, on-demand reuse; leave the one-off script as a plain, disposable session.

**Question 54.** The compliance office wants documented evidence of who accessed what applicant-related data through the system and when.

- A) Access logging is optional as long as the system already enforces role-based permissions on who can open a case file.
- B) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements.
- C) Only failed access attempts need to be logged, not successful reads of applicant data by authorized caseworkers.
- D) Audit logging can be added later without any impact on the system's architecture.

**Question 55.** The steering committee for this deployment includes caseworker operations, legal/compliance, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, since they'll relay the relevant information to the others.
- B) Tailor architectural communication to each audience — tradeoffs framed in terms caseworker and compliance stakeholders can evaluate.
- C) Use identical technical documentation for all three audiences to save preparation effort.
- D) Skip stakeholder communication entirely until the system is fully built and ready to demo.

**Question 56.** Midway through the project, eligibility-determination requirements shift meaningfully based on new state legislation.

- A) Treat this as normal lifecycle management — re-engage discovery for the affected scope and communicate the tradeoff to stakeholders.
- B) Refuse to incorporate the change, since requirements were already agreed upon earlier in the project.
- C) Incorporate the change silently without informing stakeholders of the resulting impact on scope or timeline.
- D) Restart the entire project from scratch, regardless of how much of the existing design and already-built subagent boundaries the new legislation actually affects.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the operations team.

- A) This is the correct lifecycle model; monitoring and iteration become entirely the operations team's responsibility at handoff.
- B) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility.
- C) Lifecycle responsibility ends once the authorization to operate is granted, regardless of what happens after.
- D) Monitoring is only necessary if a major incident occurs after the operations team takes over.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient, since the final configuration values are all a future team needs.
- B) Documenting reasoning is unnecessary overhead in a regulated environment that already has its own compliance paperwork.
- C) Documentation should also capture the why — compliance drivers and tradeoff reasoning — so a future team can safely extend the system.
- D) Only the original architect should ever be allowed to modify the system going forward, which makes further documentation of tradeoff reasoning moot.

**Question 59.** The caseworker operations team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Evaluate specific task categories for genuine friction reduction versus cases where review overhead may exceed time saved.
- B) Ban Claude Code for all documentation tasks without running any evaluation of where it actually helps.
- C) Mandate Claude Code usage for all tasks regardless of measured benefit in any specific category.
- D) Assume AI-assisted tooling always saves time on every task category by default, without ever checking the review overhead it might quietly add.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency, since re-deriving the triage process each time carries no real cost.
- B) Document the triage process for distinguishing integration-layer failures from model-output failures as shared operational knowledge.
- C) Restrict debugging of Claude Code integration failures to a single designated engineer on the team.
- D) The issue can only be resolved by switching to a different AI-assisted tool entirely.

---
# Answer Key — Practice Exam 3

**Quick key:** 1-D, 2-A, 3-A, 4-C, 5-C, 6-C, 7-A, 8-D, 9-A, 10-B, 11-A, 12-D, 13-A, 14-D, 15-D, 16-C, 17-C, 18-C, 19-C, 20-A, 21-A, 22-B, 23-A, 24-B, 25-D, 26-A, 27-C, 28-C, 29-B, 30-A, 31-A, 32-B, 33-D, 34-D, 35-B, 36-B, 37-A, 38-B, 39-B, 40-D, 41-D, 42-C, 43-D, 44-C, 45-D, 46-D, 47-B, 48-C, 49-C, 50-C, 51-D, 52-B, 53-D, 54-B, 55-B, 56-A, 57-B, 58-C, 59-A, 60-B

---

**1. D** — The stated goal (fewer contract attorneys, same turnaround) is a cost/efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A and C misname the pillar as transformation/new capability, and B drops the cost objective discovery actually surfaced.

**2. A** — Steps that vary by document type, protective-order terms, and intermediate findings (a privilege hit changing downstream handling) are the defining case for an agentic pattern. B wrongly assumes review is a single standardized sequence; C undersells the orchestration needed; D ignores real, non-interchangeable tradeoffs.

**3. A** — Routing the privilege determination through the coordinator preserves observability and consistent handling of privilege calls across the matter. B trades that away for a latency shortcut, and D for indiscriminate noise; C discards the specialization that motivated separate subagents in the first place.

**4. C** — Every subagent succeeding while redundantly re-deriving the same OCR output is a coordinator data-flow problem, not a subagent capability gap. A, B, and D all patch around the issue instead of fixing the missing hand-off.

**5. C** — Discovery surfacing defensibility as the actual driving concern means the pillar and its metrics should shift toward auditability/explainability, not stay anchored to the originally named pillar. A and D ignore what discovery revealed; B conflates two distinct concerns.

**6. C** — Adoption/liability sentiment about unsupervised withholding decisions is a real implicit constraint that should shape a specific HITL checkpoint in the architecture. A treats it as out of scope and B proceeds around it; D overreacts to sentiment alone without weighing the technical case.

**7. A** — Explaining the specific tradeoff (deeper legal reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. B and D deny or hide a deliberate, justified difference; C withholds reasoning partners need.

**8. D** — Adding a feedback loop that captures attorney overrides and reasoning as a first-class architectural component is what lets the system improve post-deployment. A, B, and C all treat this component as optional, out of scope, or someone else's problem.

**9. A** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. B and D over-engineer a simple augmentation need by forcing it through heavier patterns; C is factually wrong.

**10. B** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows; the fix is removing or relocating them. A and C assume no such degradation exists; D doesn't address selection reliability at all.

**11. A** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (intake) completes, reducing latency without sacrificing correctness. B and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. D** — A steering-level audience needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A and B are the wrong level of detail; C skips the communication need entirely.

**13. A** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. B, C, and D understate or deny this real architectural tradeoff.

**14. D** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A wastes effort guessing at unscoped requirements; B ignores a known future need entirely; C blocks current delivery unnecessarily.

**15. D** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, B, and C all leave that actual knowledge-transfer gap unaddressed.

**16. C** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and B ignore fit-to-task; D avoids a manageable engineering cost at the expense of quality.

**17. C** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A misdescribes what caching does; B and D both break the cacheable prefix.

**18. C** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and B ignore this mismatch; D discards useful structured data instead of indexing it appropriately.

**19. C** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and B force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. A** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. B, C, and D all reintroduce the failure mode the fix is meant to prevent.

**21. A** — Presenting both figures with attribution and the likely methodological explanation preserves the actual information for the scientist rather than resolving a real discrepancy arbitrarily. B, C, and D all discard or obscure a genuine data conflict.

**22. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests or temperature tweaks that can still drift. A and C are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. B, C, and D all fail the reuse or maintainability requirement.

**24. B** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. A and C ignore the real context cost of the monolithic approach; D removes needed capability entirely.

**25. D** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-study synthesis requiring step-by-step reasoning. A, B, and C all misstate the fit or capability of prompting techniques for this task.

**26. A** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. B reintroduces duplication; C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. C** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; D doesn't address correctness; B incorrectly claims no architectural mitigation exists.

**28. C** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to one factor regardless of SLA ignores a real, decidable tradeoff. A, B, and D each drop a relevant factor from the decision.

**29. B** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and D assume benchmark gains transfer automatically; C over-corrects into permanent stagnation.

**30. A** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. B, C, and D all misstate this real, architecture-relevant constraint.

**31. A** — Accuracy, latency, cost, and safety/fairness should all be defined as first-class metrics, since a system failing on any of them fails overall even if it screens quickly. B, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. B** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially fairness-relevant edge cases. A, C, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. D** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips a controlled test; B confounds two variables; C wrongly assumes prompt-driven LLM output is deterministic and therefore low-risk.

**34. D** — Correct parsing plus a misread qualification is a generation-side issue, calling for prompt or output-checking fixes rather than ingestion or model-tier changes. A and C misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. B** — A regression tied specifically to a template-update event, with model and latency unchanged, points first at the requisition-template/retrieval layer. A, C, and D would not specifically correlate with that update.

**36. B** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "quality at all costs" outcome and a cheap configuration that fails the quality bar. A optimizes dimensions in isolation; C assumes quality trumps all constraints; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and D accept that same blind spot; C drops accuracy monitoring from observability entirely.

**38. B** — Segmenting accuracy by role/requisition type before cutting review protects against a failing segment hiding behind a healthy aggregate. A and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. B** — An isolated throughput improvement could mask a worsened fairness-related failure mode; checking specifically for that before shipping is the correct diagnostic step. A and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. D** — "Accurate but poorly rated" points at an unmeasured quality dimension (tone, personalization, warmth) rather than a broken accuracy metric. A and C discard a working, differently-scoped metric; B assumes a fix without diagnosis.

**41. D** — Caching the static compliance document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; C removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. C** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and D accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. D** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and C guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. C** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose the situation as a model or sampling defect; B doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. D** — FedRAMP-driven boundary, residency, and logging requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate real architectural impact; C misidentifies the applicable regulatory regime.

**47. B** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and C overstate the universal safety or accuracy case in one direction; D misattributes the requirement to a statute that isn't the relevant driver described.

**48. C** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, checks for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; D assumes one guardrail covers distinct risk types; B is factually wrong.

**49. C** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; B and D make unsupported blanket claims.

**50. C** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. B and D leave the systemic cause unaddressed; A sacrifices the tool's benefit for the rest of the team.

**51. D** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially for an authorized system. A, B, and C all propose reducing rigor specifically because AI was involved, which is the wrong direction in this context.

**52. B** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and D skip or overreach on diagnosis; C is a disproportionate reaction that doesn't investigate the actual cause.

**53. D** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory script as a plain session avoids unnecessary standing infrastructure. A over-engineers the one-off task; B under-serves the recurring task; C ignores that reuse profile should drive the choice.

**54. B** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, C, and D each understate what compliance-grade audit evidence actually requires.

**55. B** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by caseworker, compliance, and engineering audiences alike. A, C, and D each fail to serve at least one audience's real information need.

**56. A** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. B and C mishandle a real change; D disproportionately discards unaffected work.

**57. B** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. C** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and D all leave that reasoning undocumented and effectively lost.

**59. A** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. C and D over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 3.*
