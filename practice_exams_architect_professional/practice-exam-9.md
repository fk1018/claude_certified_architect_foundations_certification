# CCARP Practice Exam 9

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent Underwriting Platform, Manufacturing Predictive-Maintenance RAG & Model Selection, Fraud-Detection Triage Evaluation & Optimization, Banking GDPR Governance & Stakeholder Communication) |
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

## Scenario A: Multi-Agent Underwriting Platform for a Commercial Insurer (Questions 1–15)

Meridian Commercial Insurance wants to modernize how it triages and prices incoming commercial property and casualty submissions. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with underwriting leadership.

---

**Question 1.** Discovery reveals Meridian's actual goal is cutting turnaround time for standard submissions from five days to one day with the same underwriter headcount — not expanding into new lines of business.

- A) Frame the architecture around transformation, arguing this initiative should be marketed as creating an entirely new underwriting capability rather than speeding up an existing one.
- B) Frame it around cost reduction exclusively, since headcount is unchanged and payroll is the only budget lever leadership will actually fund.
- C) Skip framing around any specific value pillar; a working system justifies itself regardless of what discovery uncovered.
- D) Frame it around efficiency, and build success metrics around cycle time and throughput per underwriter rather than novel capability.

**Question 2.** The right sequence of underwriting steps varies by submission type, industry class, prior loss history, and information discovered along the way.

- A) An agentic pattern, since the sequence of steps varies by case and depends on findings discovered along the way rather than one predetermined path.
- B) A fixed workflow, since commercial underwriting has an established process every submission should follow identically regardless of what's discovered.
- C) An augmented LLM pattern, since a single retrieval-enhanced call is enough to handle any underwriting workflow, however varied.
- D) Whichever pattern the team can implement fastest, since the four patterns are functionally interchangeable for this kind of task.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (submission intake, risk scoring, actuarial pricing lookup, underwriting-decision recommendation).

- A) Let each subagent pass results directly to whichever subagent needs them next, cutting out the coordinator hop to reduce turnaround time and simplify the message path.
- B) Merge all four responsibilities into a single subagent so there's no coordination overhead or handoffs to manage at all.
- C) Let subagents communicate directly, but log the peer-to-peer traffic in a structured audit trail so it can be reviewed later if needed.
- D) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition assigned only standard property submissions to the pipeline — excess and umbrella liability submissions are never routed to any subagent and silently fall through.

- A) Fix the coordinator's decomposition to explicitly cover every submission category, including excess and umbrella liability, instead of tuning subagents that already work.
- B) Add a prompt instruction telling each subagent to flag any submission type it doesn't recognize, so routing gaps surface downstream instead of failing silently.
- C) Give the existing subagents broader tool access so any one of them could, in principle, handle a submission type it wasn't originally scoped for.
- D) Add a fifth subagent dedicated to edge-case submissions, without changing how the coordinator's routing logic decides what counts as an edge case in the first place, leaving the same gap.

**Question 5.** The design must align technical architecture to a specific business value pillar Meridian's leadership actually cares about, distinct from a generic "we added AI" narrative.

- A) Any AI system inherently demonstrates transformation on its own merits, so no further framing around a specific pillar is ever needed.
- B) Efficiency, transformation, productivity, cost, and performance SLAs are examples of such pillars that should drive both architecture and metrics.
- C) Business value pillars are a sales and marketing concern, not something that belongs in an architectural conversation with leadership.
- D) The pillar should be picked only after the system ships, based on whichever benefit happens to be easiest to measure at that later point.

**Question 6.** Meridian's underwriting team is skeptical of automation and worried about job security; discovery interviews surface this repeatedly.

- A) Ignore the sentiment entirely, since job-security concerns aren't a technical requirement the architecture needs to satisfy.
- B) Proceed with the technical design as planned and let change management handle the sentiment separately, with no architectural input at all.
- C) Treat it as a real implicit constraint alongside the explicit technical requirements — it will shape rollout sequencing and where human-in-the-loop checkpoints matter most.
- D) Recommend against the project entirely on the strength of this sentiment alone, without weighing it at all against the turnaround-time and same-headcount case that originally motivated pursuing it.

**Question 7.** A stakeholder asks why the risk-scoring subagent uses a higher-capability, higher-cost model tier than the submission-intake subagent.

- A) "Higher tier because it's more important" is a sufficient answer for a stakeholder asking about cost.
- B) Explain the tradeoff explicitly: risk scoring needs deeper reasoning that justifies the added cost and latency, while intake is simpler and cheaper.
- C) Avoid explaining the tier difference at all, since stakeholders don't need architecture-level technical detail.
- D) Use the same tier everywhere for simplicity, regardless of how difficult each subagent's reasoning task actually is, since stakeholders would rather hear one consistent number than a tier-by-tier breakdown.

**Question 8.** The architecture's current design produces a final underwriting recommendation with no mechanism to learn from underwriter overrides or outcomes over time.

- A) Add a feedback loop capturing underwriter overrides and outcomes as a first-class architectural component, so the system can improve after deployment rather than staying static.
- B) This is acceptable as-is, since the initial design already reflects best practice and doesn't need a feedback mechanism.
- C) Feedback loops are a data science concern that has nothing to do with the architecture itself.
- D) Defer any feedback mechanism to a hypothetical future phase, with no hooks for it in the current design.

**Question 9.** Meridian wants a single enhanced LLM call — with retrieval of underwriting guidelines — to answer straightforward eligibility questions, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture with a coordinator delegating to specialized subagents, regardless of how simple the eligibility question actually turns out to be.
- B) An augmented LLM pattern (a single call enhanced with retrieval/tools) fits this simpler augmentation need without the overhead of agentic orchestration.
- C) This cannot be built with Claude at all, since anything without autonomous multi-step orchestration doesn't count as using an agent.
- D) This requires a fixed workflow with at least five sequential steps and a rigid output schema, even for a single straightforward lookup.

**Question 10.** The submission-intake subagent's toolset has grown to include tools for tasks like billing lookup and HR record access that are unrelated to submission intake.

- A) This has no architectural downside as long as the subagent's system prompt is written clearly enough to keep it focused.
- B) More tools always improve a subagent's flexibility, so billing and HR access should be encouraged rather than trimmed.
- C) The fix is to increase the subagent's context window and add a validation step, so it can hold the growing tool list without losing track of any of them.
- D) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or moved to a more appropriate subagent.

**Question 11.** The coordinator currently processes each submission sequentially through intake, risk scoring, pricing lookup, and decision recommendation, even though risk scoring and pricing lookup have no dependency on each other's output.

- A) Sequential processing is required for auditability, since parallel subagent calls can't be logged or traced the same way sequential ones can.
- B) Parallelization isn't possible with a coordinator/subagent architecture once more than two subagents are involved in a single submission.
- C) Run risk scoring and pricing lookup as independent, parallel subagent calls once intake completes, to increase throughput rather than forcing them through unnecessary sequential steps.
- D) Combine risk scoring and pricing lookup into a single subagent so the sequencing question never has to be answered.

**Question 12.** Meridian's steering committee asks how the end-to-end architecture should be described at a high level for members unfamiliar with the technical details.

- A) Present only the model names and per-token costs involved, since that's the information a steering committee actually needs.
- B) Present the complete technical architecture diagram with no simplification at all, trusting the committee to follow structured, subagent-level implementation detail unaided.
- C) Skip a high-level description entirely and go straight into a live implementation demo of the coordinator and subagents.
- D) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, without requiring implementation detail.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (intake, risk scoring, pricing, decisioning) rather than a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows, since one agent holding full context across every responsibility avoids handoff overhead between separate subagents entirely.
- B) Specialized subagents are strictly a cost-increasing choice with no reliability benefit over a single agent holding every tool.
- C) There's no meaningful architectural difference between the two approaches once both are given the same underlying model.
- D) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.

**Question 14.** The underwriting architecture must eventually support a new line (cyber liability) Meridian plans to launch next year, but detailed requirements aren't available yet.

- A) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements that may still change.
- B) Ignore future lines of business entirely until cyber liability's detailed requirements actually exist and are documented.
- C) Build full support for cyber liability now, making reasonable guesses about requirements that haven't been defined yet.
- D) Refuse to proceed with the current phase until the future cyber liability requirements are fully finalized by leadership.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, since a well-built implementation should be self-explanatory to any engineer who reads it.
- B) Document the architecture and the reasoning behind key decisions — pattern choices, decomposition boundaries, tier selections — not just final values.
- C) Rely on the original architect remaining available indefinitely to answer questions, instead of writing anything down.
- D) Documentation is unnecessary as long as the code is well-organized and consistently named, since a new team can always reconstruct the full decision-making reasoning just by reading the implementation carefully.

---

## Scenario B: RAG and Model Selection for a Manufacturing Predictive-Maintenance Platform (Questions 16–30)

Ironclad Manufacturing wants Claude to help maintenance technicians diagnose equipment issues using both general reasoning and retrieval over equipment manuals, sensor telemetry logs, and historical maintenance records. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most technician questions are moderately complex; a small fraction require deep multi-step diagnostic reasoning across sensor history and manuals, and a small fraction are simple lookups (e.g., part numbers).

- A) Use one fixed model tier for every question regardless of complexity, so the routing logic stays as simple as possible to build and maintain, even though the mix of questions ranges from simple lookups to deep diagnostic reasoning.
- B) Route based on task difficulty — fast tier for simple lookups, balanced tier for typical questions, higher-capability tier for deep diagnostic cases.
- C) Always use the highest-capability tier to guarantee quality on every question, including simple part-number lookups.
- D) Always use the fastest tier to minimize cost, accepting quality loss on the complex diagnostic questions.

**Question 17.** Every request sends the same long system prompt (technician persona, safety disclaimers, formatting rules) followed by retrieved manual and sensor excerpts that vary per query.

- A) Order doesn't affect cost or latency for this use case, since the total token count stays the same either way.
- B) Alternate system instructions and retrieved content throughout the prompt so related material stays near each other.
- C) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it, to reduce both latency and cost across the high query volume.
- D) Put the retrieved content first since it's the most relevant part of the prompt to the specific query.

**Question 18.** The corpus mixes long-form equipment manuals with short structured records (tables of sensor thresholds and part specifications).

- A) One chunking and indexing strategy tuned for long-form documents can serve both content types equally well without adjustment.
- B) Structured sensor-threshold and part-spec data should be excluded from retrieval entirely, since it doesn't fit a document-style, long-form chunking and indexing strategy built for manuals.
- C) Chunking and indexing strategy should match each data shape, or retrieval quality degrades for whichever content type doesn't match the chosen strategy.
- D) Use the largest possible chunk size for everything so a single strategy can be reused without building a second pipeline.

**Question 19.** Technician queries range from exact lookups ("torque spec for bearing X on Model 4000") to conceptual questions ("why do Model 4000 bearings fail more often in humid climates").

- A) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embeddings for conceptual questions, hybrid where both are needed.
- B) Use only embedding similarity search for every query type, whether it's an exact torque-spec lookup on a specific bearing or an open-ended question about humidity-related failure causes across models.
- C) Use only structured/metadata filtering for every query type, including open-ended conceptual questions about failure causes.
- D) Query pattern doesn't meaningfully affect which retrieval approach is appropriate, since the underlying corpus is the same either way.

**Question 20.** Technicians need citations that reliably map each claim to a specific manual and page/section, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without giving it any further structure to enforce the mapping.
- B) Append a general bibliography of every manual consulted at the end of each response, without tying any specific claim to it.
- C) Require structured output pairing each claim with its source (document, section, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.
- D) Add citations after the response is drafted, by searching for whichever source excerpt sounds like the closest plausible match to each individual claim.

**Question 21.** Two retrieved manual revisions disagree on the recommended maintenance interval for a component by a noticeable margin — likely because they reflect different manufacturer revision dates.

- A) Average the two figures and present the single averaged number as the recommended maintenance interval.
- B) Omit the maintenance interval entirely from the response, since the two sources disagree on the correct figure and neither one can be confirmed as the more current manufacturer revision.
- C) Always prefer whichever source was retrieved first, treating retrieval order as a proxy for reliability.
- D) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely explanation, rather than silently picking one.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the "always output valid structured JSON" instruction more emphatically, since stronger prose alone should make deterministic-looking output more reliable.
- B) Increase max_tokens so there's enough room in the output for both the conversational preamble and the JSON that follows it.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism itself rather than requested through prose alone.
- D) Post-process every response to strip any leading text that appears before the first `{` character.

**Question 23.** The platform needs to connect to a proprietary internal maintenance-ticketing system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this predictive-maintenance platform.

- A) Build an MCP server exposing the ticketing-system operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- B) Hard-code the ticketing-system integration directly into this platform's application code, and nowhere else.
- C) Paste the entire ticketing corpus into every prompt so no external lookup is ever needed.
- D) Require each consuming tool to reimplement its own ticketing-system integration independently, from scratch.

**Question 24.** The team is deciding between exposing the full equipment-manual catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Loading the full catalog up front is always preferable for completeness, even as the manual catalog keeps growing well beyond what fits comfortably in a single context window.
- B) The catalog should never be exposed to the agent in any structured form at all, to keep the prompt small regardless of catalog size.
- C) Progressive discovery — querying a catalog resource as needed — scales better than loading the entire catalog up front, especially as the corpus grows.
- D) There's no meaningful difference in context cost between loading everything up front and querying the catalog resource on demand.

**Question 25.** A technician asks a diagnostic question requiring the model to reason step by step across sensor logs, maintenance history, and manuals before concluding a likely root cause.

- A) Zero-shot prompting with no intermediate reasoning guidance is always just as effective as a guided step-by-step approach, regardless of how many sources the question spans.
- B) Chain-of-thought prompting is only useful for coding tasks, not for diagnostic reasoning that spans sensor logs, maintenance history, and manuals.
- C) The model cannot reason across multiple documents at all, regardless of what prompting approach or reasoning technique is used.
- D) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-source diagnostic synthesis question.

**Question 26.** The platform wants to standardize prompt fragments (safety disclaimers, citation format, units-of-measure formatting) across several different technician-facing features so changes propagate consistently.

- A) Duplicate the fragments into each feature's system prompt independently, updating every copy by hand whenever one changes.
- B) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).
- C) Modular prompt fragments and prompt caching are the same underlying mechanism, so choosing one covers the other.
- D) Standardization across features isn't achievable through prompt design and would require a separate configuration system.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific sensor threshold value from the correctly retrieved manual.

- A) Apply defensive validation — verify extracted figures against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- B) Trust the fluent, well-formatted output as sufficient evidence of correctness, since citations already look attached and correct.
- C) Increase the output length so the model has more room somewhere in the longer response to eventually state the correct figure.
- D) This isn't something the architecture can meaningfully address at all; it's purely an inherent model limitation with no available mitigation, regardless of how the pipeline is designed.

**Question 28.** The team debates whether shop-floor latency SLAs should factor into model tier selection for the predictive-maintenance platform.

- A) Latency should never factor into model or architecture decisions, regardless of what the shop-floor SLA requires or how the technicians actually use the tool day to day.
- B) Only cost should factor into tier selection for this platform; latency should never be part of that decision at all.
- C) Yes — model tier selection should weigh accuracy against the latency and cost the SLA can tolerate, not default to the most capable tier regardless of SLA.
- D) SLAs are purely a stakeholder-communication concern with no bearing whatsoever on technical architecture or model-tier decisions.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically in production, since a newer model version with better benchmark scores is always a safe improvement to ship immediately.
- B) Never upgrade the model once the initial version is chosen, regardless of what future releases or benchmark improvements might offer down the line.
- C) Pin the current version and test the new one against the platform's own evals before upgrading, since behavior can shift even with better benchmarks.
- D) Upgrade immediately without testing, since improved benchmark scores always guarantee an equivalent improvement in actual production behavior.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved manual/sensor excerpts must fit alongside room for a detailed diagnostic answer.

- A) Input and output share the same context-window budget, constraining how much retrieved content and answer detail can coexist.
- B) This tradeoff only matters for unusually long documents, and never comes up for a typical technician query about a straightforward torque spec or part number.
- C) Output length has no practical limit at all, regardless of how much input content is retrieved.
- D) Input and output token budgets are entirely independent line items with no shared constraint between them.

---

## Scenario C: Evaluation and Optimization of a Fraud-Detection Triage System (Questions 31–45)

A Claude-powered system at Vantage Payments flags suspicious transactions for human investigator review. It's been in production for eight months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only flag precision and hasn't defined targets for latency, cost, or safety.

- A) Precision alone is sufficient, since flagging suspicious transactions accurately is the fraud-triage system's stated primary purpose.
- B) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics — flagging fraud well isn't enough if the system is too slow, expensive, or unsafe.
- C) Latency and cost are purely operations concerns, unrelated to how the fraud-detection evaluation strategy itself should be designed.
- D) Safety and security metrics are only relevant for systems operating in explicitly regulated industries, and a payments fraud-triage system handling live transactions doesn't need them defined as first-class metrics at all.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past transactions.

- A) A single automated evaluation method is sufficient for any production system, regardless of how nuanced its failure modes are.
- B) Replace the automated checks entirely with only human review, since automation can't capture nuanced judgment calls.
- C) Expand the labeled set indefinitely, treating a bigger fixed dataset as the sole lever for improving evaluation coverage.
- D) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for safety-relevant paths — since no single method covers every failure mode.

**Question 33.** The team wants to test whether a new triage-scoring prompt improves flag quality before rolling it out to all traffic.

- A) Roll out the new prompt to all traffic immediately and monitor informally for problems after the fact.
- B) Change the prompt and the model tier at the same time, to maximize the potential improvement from both changes in a single rollout rather than testing them separately.
- C) Run an A/B test changing only the prompt version against a stable baseline, so any difference can be attributed to that one change.
- D) Skip testing entirely, since prompt changes are inherently low-risk and rarely affect flag quality.

**Question 34.** A flagged transaction was wrongly cleared as legitimate. Investigation shows the underlying transaction-history data was retrieved correctly, and the model's response paraphrased it inaccurately.

- A) This is best characterized as a prompt/generation issue (inaccurate paraphrasing of correctly retrieved data), which calls for prompt or output-validation fixes rather than retrieval changes.
- B) This is a retrieval problem, so the fix should focus on the indexing pipeline that surfaced the transaction history, even though the investigation found the retrieved data itself was accurate.
- C) This can't be diagnosed at all without retraining the underlying model from scratch on new data.
- D) This is a model mismatch requiring a switch to a different model tier, regardless of what the specific failure actually was.

**Question 35.** Immediately after a scheduled transaction-history database migration, the system starts flagging an elevated rate of clean transactions as fraud, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider, even though nothing in the validation logs points to a model-side change.
- B) Investigate the retrieval/indexing layer first, since the regression is tied specifically to the data migration event with model version and average latency unchanged.
- C) Suspect a temperature setting change, since the flagging behavior changed right after the migration.
- D) Suspect the context window shrank, even though window size has no bearing on how deterministic the model's flagging output is.

**Question 36.** The team wants to reduce cost and latency of fraud triage but is worried about hurting recall, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, one at a time and in isolation, since combining all three into a single joint tradeoff decision only overcomplicates an already difficult recall-versus-cost analysis.
- B) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest configuration that fails the recall bar isn't a win.
- C) Accuracy should always be maximized regardless of what that does to cost or latency, since fraud detection is the priority.
- D) This tradeoff can't be measured with the data available; it can only be guessed at until more data accumulates.

**Question 37.** Production monitoring currently reports only an overall weekly average precision score.

- A) A single aggregate weekly average is sufficient for production monitoring, regardless of what a specific merchant category or transaction type happening underneath it might actually be hiding.
- B) Monitoring should track only cost, since accuracy is already captured by the separate, structured eval suite.
- C) Monitoring should surface drift and outliers — a per-merchant or per-transaction-type breakdown — since an aggregate average can hide a failing segment.
- D) Weekly granularity is always sufficient regardless of how the system's behavior actually changes day to day.

**Question 38.** The team proposes cutting manual review of flagged transactions by 70%, citing a 98% aggregate accuracy score.

- A) Segment accuracy by merchant category and transaction type before cutting review, since an aggregate figure can mask a badly underperforming segment.
- B) Proceed with the 70% review cut based on the 98% aggregate figure alone, trusting that number to reflect real performance.
- C) Aggregate accuracy is, by definition, representative of how every individual merchant or transaction segment is performing underneath it.
- D) Human review should never be reduced under any circumstances, regardless of what a segmented accuracy analysis eventually shows about risk concentration.

**Question 39.** An A/B test shows a new triage model improves flag precision, but the team hasn't checked whether it also changed the false-negative rate on sophisticated fraud patterns that should be escalated.

- A) Precision improvement alone is a sufficient signal to ship the change, without checking any other failure mode.
- B) False-negative escalation behavior isn't something evaluation can measure at all, so it isn't worth specifically checking before a change ships to production traffic.
- C) Check the escalation-related failure mode specifically before shipping — an isolated precision gain could be masking missed sophisticated fraud.
- D) Ship the change and monitor informally after the fact, instead of testing the escalation behavior beforehand.

**Question 40.** The team wants to diagnose why a subset of flagged transactions are technically correctly classified but investigators rate the accompanying explanation as unhelpful.

- A) Assume the accuracy metric itself is broken and discard it, since it doesn't reflect what investigators are reporting.
- B) Increase the model's capability tier across the board, on the assumption that a higher-capability model will always produce more highly rated explanations regardless of what investigators actually found unhelpful.
- C) Ignore investigator ratings entirely and rely on the accuracy metric's validation results alone as the sole quality signal.
- D) Investigate a dimension beyond factual accuracy — e.g., clarity, completeness, or actionability of the explanation — since "correct but unhelpful" points at a quality dimension the current eval doesn't measure.

**Question 41.** The team is optimizing token usage and notices the system sends the full transaction history plus a large static fraud-policy document on every turn of multi-turn investigator conversations.

- A) Apply prompt caching to the static fraud-policy document and trim or summarize older conversation turns to reduce redundant token cost.
- B) Switch to a smaller model as the only lever for reducing token cost, without changing what's resent unchanged on every single turn.
- C) Remove the fraud-policy document from the prompt entirely to save tokens, even on turns where the policy is directly relevant.
- D) Full transaction history is always required on every turn, so there's no optimization opportunity here worth pursuing.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy, as long as the logs are retained somewhere and nobody deletes them during a routine cleanup.
- B) Reduce logging volume to save on storage cost, without making any other change to how it's structured.
- C) Observability requires no particular structure, as long as the underlying data is retained somewhere for later use.
- D) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, segment-level quality metrics — since raw logs at volume aren't reviewable on their own.

**Question 43.** The team wants to identify whether a quality regression was caused by a recent prompt change, a recent model version change, or a fraud-policy document update — all three happened in the same week.

- A) Assume the most recent of the three changes is always the one responsible for the regression, without testing that assumption against the prompt or fraud-policy changes shipped the same week.
- B) Attribution is impossible once multiple changes have shipped in the same week, so the question isn't worth pursuing.
- C) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating each independently.
- D) Revert all three changes without investigation, regardless of which one, if any, actually caused the regression.

**Question 44.** An automated eval asserts that a triage-explanation output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.
- B) The model is malfunctioning and needs to be retrained before the eval can be trusted again.
- C) The reference string needs to be made longer, and its exact-match validation left as-is, so more of the output matches it.
- D) The eval's threshold for what counts as a pass needs to be loosened until the intermittent failures stop appearing.

**Question 45.** Leadership wants a single number to represent "how good" the fraud-triage system is, to track over time.

- A) A single aggregate metric can be a useful top-line indicator, but should be paired with segment-level and multi-dimensional detail so a healthy top-line number doesn't mask a failing area.
- B) Use flag precision alone as the single number, since that's the system's stated primary purpose.
- C) Refuse to provide any single summary metric at all, regardless of how clearly leadership has asked for one.
- D) A single number is always fully achievable and sufficient for representing any system's evaluation needs, regardless of how many distinct dimensions like latency, cost, and safety actually feed into it.

---

## Scenario D: Governance and Stakeholder Communication for a Banking GDPR Deployment (Questions 46–60)

Nordbank, an EU retail bank, is deploying a Claude-powered system that assists customer-service representatives and supports internal credit-related workflows, alongside a small engineering team using Claude Code internally. You are responsible for governance, GDPR compliance, and stakeholder communication for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) This sequencing carries no real risk, since data-minimization, retention, and access-control requirements can always be layered on cleanly in the final week without touching anything already built.
- B) Compliance only affects legal documentation and contracts, not the system's underlying technical architecture.
- C) HIPAA, not GDPR, is the relevant regulatory regime for a retail bank operating inside the EU.
- D) GDPR-driven data-minimization, retention, and access-control requirements can force structural changes that are far more costly to retrofit than to design in from the start.

**Question 47.** A team proposes requiring human approval on every single output the customer-facing system produces, framing it as the safest governance posture.

- A) Maximal human review on every single output is always the correct default posture for a banking AI system, regardless of cost.
- B) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.
- C) Human reviewers are categorically less accurate than the model on every task, making review counterproductive across the board.
- D) This universal-review approach is required by GDPR regardless of the error cost or judgment involved in a given output.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from customer-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed reactively, once each one is actually observed happening in live production traffic, rather than designed against ahead of the initial customer-facing launch date.
- B) These three risks are considered exclusive to non-banking use cases and therefore don't meaningfully apply to a regulated financial system.
- C) A single generic guardrail, applied once across the board, addresses hallucination, prompt injection, and inconsistent output equally well without any task-specific tuning.
- D) Design mitigations for each known failure mode up front — grounding for hallucination, isolation for injection, validation for consistency — rather than as a reactive afterthought.

**Question 49.** The compliance team asks whether the system's credit-related outputs could produce disparate outcomes across different demographic groups.

- A) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population rather than assuming disparate impact is absent.
- B) This isn't an architectural concern at all; it belongs entirely to legal and compliance review conducted after the system has already launched.
- C) Disparate impact is impossible in an LLM-based system by construction, regardless of what data it was trained or evaluated on or how closely that data reflects the population actually served.
- D) This concern only applies to systems making final, legally binding credit decisions, not to an assistive system that merely supports representatives.

**Question 50.** The engineering team's Claude Code usage is inconsistent — some engineers have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Have each engineer individually troubleshoot their own local configuration, without any shared team-level standard to converge on.
- B) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team level so behavior doesn't depend on individual local machine setup at all.
- C) Restrict Claude Code usage to a single designated engineer, so configuration variance across the rest of the team simply stops mattering.
- D) Accept the inconsistency as an unavoidable, permanent cost of adopting AI-assisted tooling across a team of engineers.

**Question 51.** The team wants Claude Code-generated code changes in this banking context to go through the same review rigor as any other change to a regulated system.

- A) AI-assisted code should bypass standard review entirely, since Claude Code generated it directly and a human author would have needed the same review a hand-written change requires.
- B) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a regulated system.
- C) Only a quick spot-check validation of the AI-generated portion is necessary, rather than the full review process.
- D) Review requirements should be set lower for AI-generated code than for equivalent human-written code in the same system.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without first investigating whether the integration layer is actually at fault.
- B) Disable Claude Code for the team entirely, following any incident regardless of where the actual root cause turns out to be once the traces and logs are actually reviewed.
- C) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the model output — using traces and logs.
- D) Roll back all recent Claude Code-assisted changes regardless of whether they're actually relevant to this incident.

**Question 53.** The engineering team wants a documented, repeatable workflow for a recurring task (generating a weekly GDPR data-subject-access-request summary report) versus a one-off exploratory coding task.

- A) Build both the recurring report and the one-off exploratory task as ad hoc, undocumented prompts each time either is needed.
- B) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session, since it doesn't need standing infrastructure.
- C) Build both the recurring report and the one-off task as MCP servers, regardless of how often either one is actually reused.
- D) Recurring, well-defined workflows and one-off exploratory tasks should always be built with identical structure.

**Question 54.** The compliance team wants documented evidence of who accessed what customer data through the system and when.

- A) Access logging is optional as long as the system already enforces a role-based permission schema on who can reach which data.
- B) Audit logging can always be layered on afterward without any architectural impact, once role-based permissions and the rest of the customer-data-handling system are already fully built and shipped to production.
- C) Only failed access attempts need a structured log entry; successful, authorized access doesn't need one.
- D) Design access-control and audit-logging as explicit architectural components satisfying identity, authorization, and monitoring requirements — not an implicit byproduct.

**Question 55.** The steering committee for this deployment includes compliance, risk, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, trusting them to relay the relevant tradeoffs to compliance and risk.
- B) Skip stakeholder communication until the system is fully built and ready for a single end-of-project readout.
- C) Use identical technical documentation for all three audiences — compliance, risk, and engineering — to save preparation effort, trusting each group to extract what matters to them.
- D) Tailor architectural communication to each audience — tradeoffs framed in terms compliance and risk stakeholders can evaluate against their own priorities.

**Question 56.** Midway through the project, requirements shift meaningfully based on new EU regulatory guidance.

- A) Refuse to incorporate the new regulatory guidance, since requirements were already agreed upon and finalized earlier in the project timeline.
- B) Incorporate the change silently, without informing any stakeholders that the project's scope or timeline impact has meaningfully shifted.
- C) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope and communicate the tradeoff of the change to stakeholders.
- D) Restart the entire project from scratch, regardless of how narrow the new guidance's actual scope turns out to be in practice.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the operations team.

- A) This is the correct lifecycle model; once handoff to the operations team happens, ongoing monitoring and iteration based on production signal become entirely their responsibility going forward.
- B) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.
- C) Lifecycle responsibility ends once the contract with the operations team is signed, regardless of what happens in production afterward.
- D) Monitoring is only necessary if a major incident actually occurs sometime after handoff; otherwise it can reasonably be skipped entirely.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — not just the final configuration values.
- B) This level of documentation is already sufficient, since the final configuration values — model tier, retry settings, thresholds — are all a future team would ever realistically need to safely extend the system.
- C) Documenting the reasoning behind each decision is unnecessary overhead in an already heavily regulated environment.
- D) Only the original architect should ever be allowed to modify the system, which makes documentation effectively moot.

**Question 59.** The engineering team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves meaningful time on every task category, by default, without measuring documentation drafting or codebase exploration specifically.
- B) Evaluate specific task categories for genuine friction reduction versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.
- C) Mandate Claude Code usage for every task category regardless of any measured benefit or added review overhead.
- D) Ban Claude Code for all structured documentation tasks outright, without evaluating whether it actually reduces friction on repetitive drafting work.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no real architectural fix available for repeated, independent re-derivation.
- B) Restrict debugging of these integration failures to a single designated engineer, so the rest of the team stops encountering them.
- C) The issue can only be resolved by switching to an entirely different tool than Claude Code, since the underlying integration-layer-versus-model-output distinction can't be captured in any shared documentation.
- D) Document the triage process (how to distinguish integration-layer failures from model-output failures for this system) as shared operational knowledge, reducing redundant re-derivation across the team.

---
# Answer Key

**Quick key:** 1-D, 2-A, 3-D, 4-A, 5-B, 6-C, 7-B, 8-A, 9-B, 10-D, 11-C, 12-D, 13-D, 14-A, 15-B, 16-B, 17-C, 18-C, 19-A, 20-C, 21-D, 22-C, 23-A, 24-C, 25-D, 26-B, 27-A, 28-C, 29-C, 30-A, 31-B, 32-D, 33-C, 34-A, 35-B, 36-B, 37-C, 38-A, 39-C, 40-D, 41-A, 42-D, 43-C, 44-A, 45-A, 46-D, 47-B, 48-D, 49-A, 50-B, 51-B, 52-C, 53-B, 54-D, 55-D, 56-C, 57-B, 58-A, 59-B, 60-D

---

**1. D** — The stated goal (faster turnaround, same headcount) is a throughput/efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A, B, and C either misname the pillar or skip the framing that keeps the project aligned to what discovery actually found.

**2. A** — Steps that vary by case and depend on intermediate findings are the defining case for an agentic pattern. B assumes a predictability the scenario explicitly lacks; C undersells the orchestration actually needed; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. D** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. A and C sacrifice these properties for a shortcut; B discards the specialization that motivated separate subagents in the first place.

**4. A** — Every subagent succeeding while whole submission categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. B, C, and D all patch downstream instead of fixing the actual scope gap.

**5. B** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. A, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. C** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and B treat it as out of scope; D overreacts to sentiment alone without weighing it against the technical case.

**7. B** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. A and C withhold the reasoning stakeholders need; D removes a deliberate, justified difference for false simplicity.

**8. A** — Adding a feedback loop that captures underwriter overrides and outcomes as a first-class architectural component is what lets the system improve after deployment, per the input→processing→output→feedback loop framing. B, C, and D all treat a first-class architectural component as optional or someone else's problem.

**9. B** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and D over-engineer a simple augmentation need; C is factually wrong.

**10. D** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just writing around it. A and B ignore this real degradation; C doesn't address selection reliability at all.

**11. C** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (intake) completes, reducing latency without sacrificing correctness. A and B misstate real constraints; D avoids the sequencing question rather than answering it.

**12. D** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; B is too much of the wrong kind of detail; C skips the communication need entirely.

**13. D** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, B, and C understate or deny this real architectural tradeoff.

**14. A** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. B ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave the actual knowledge transfer gap unaddressed.

**16. B** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and C ignore fit-to-task; D sacrifices quality on the cases that need capability most.

**17. C** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, B, and D all misstate or break the caching opportunity.

**18. C** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and D ignore this mismatch; B discards useful structured data.

**19. A** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. B and C force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. C** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, B, and D all reintroduce the failure mode the fix is meant to prevent.

**21. D** — Presenting both figures with attribution and likely explanation preserves the actual information for the technician rather than resolving a real discrepancy arbitrarily. A, B, and C all discard or obscure a genuine data conflict.

**22. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and D are workarounds for a structurally solvable problem; B doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. B, C, and D all fail the reuse or maintainability requirement.

**24. C** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. A and D ignore the real context cost of the monolithic approach; B removes needed capability entirely.

**25. D** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-source diagnostic synthesis requiring step-by-step reasoning. A, B, and C all misstate the fit or capability of prompting techniques for this task.

**26. B** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. A** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. B is the failure mode itself; C doesn't address correctness; D incorrectly claims no architectural mitigation exists.

**28. C** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, B, and D each drop a relevant factor from the decision.

**29. C** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and D assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. A** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. B, C, and D all misstate this real, architecture-relevant constraint.

**31. B** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if it flags fraud well. A, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. D** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. A, B, and C each over-rely on or discard one method without addressing the actual coverage gap.

**33. C** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; D dismisses a real risk without evidence.

**34. A** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. B and D misdiagnose the layer at fault; C avoids diagnosis entirely.

**35. B** — A regression tied specifically to a data migration event, with model and latency unchanged, points first at retrieval/indexing. A, C, and D would not specifically correlate with a transaction-history migration.

**36. B** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "recall at all costs" outcome and a cheap configuration that fails the recall bar. A and C optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. C** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. A and D accept a monitoring blind spot; B drops accuracy monitoring from observability entirely.

**38. A** — Segmenting accuracy by merchant category and transaction type before cutting review protects against a failing segment hiding behind a healthy aggregate. B and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. C** — An isolated precision improvement could mask a worsened escalation failure mode; checking specifically for that before shipping is the correct diagnostic step. A and D ship without adequate testing; B incorrectly claims the failure mode is unmeasurable.

**40. D** — "Correct but unhelpful" points at an unmeasured quality dimension (clarity, completeness, actionability) rather than a broken accuracy metric. A and C discard a working, differently-scoped metric; B assumes a fix without diagnosis.

**41. A** — Caching the static fraud-policy document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. D denies an obvious lever; C removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. D** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and C accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. C** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and D guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. A** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. B and D misdiagnose model behavior as broken; C doesn't address the actual mismatch between eval design and output variability.

**45. A** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. B and D oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. D** — GDPR-driven requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate real architectural impact; C misidentifies the applicable regulatory regime.

**47. B** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and C overstate the universal safety case for maximal review; D misattributes this requirement to GDPR, which doesn't mandate it universally.

**48. D** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; C assumes one guardrail covers distinct risk types; B is factually wrong.

**49. A** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. B defers a design concern entirely to a later stage; C and D make unsupported blanket claims.

**50. B** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. A and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team.

**51. B** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a regulated system. A, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. C** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and D skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. B** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. D** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and C each understate what compliance-grade audit evidence actually requires.

**55. D** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by compliance, risk, and engineering audiences alike. A, B, and C each fail to serve at least one audience's real information need.

**56. C** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and B mishandle a real change; D disproportionately discards unaffected work.

**57. B** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. A** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. B, C, and D all leave that reasoning undocumented and effectively lost.

**59. B** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and C over-assume benefit; D forecloses potential benefit without evaluation.

**60. D** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; B and C propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 9.*
