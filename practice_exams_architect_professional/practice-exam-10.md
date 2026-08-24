# CCARP Practice Exam 10

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent Supply-Chain and Logistics Orchestration Platform, RAG Integration for a Legal Case-Law Research Platform, Evaluation and A/B Testing of a Sales-Forecasting Copilot, Lifecycle Management and Enablement for a Global Manufacturing Rollout) |
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

Meridian Freight Systems, a mid-market logistics provider, wants to modernize its order-to-delivery pipeline — carrier-capacity procurement, route/mode selection, in-transit exception handling, and customs/compliance checks — using a Claude-powered multi-agent architecture. You are the architect leading discovery and design.

---

**Question 1.** Discovery reveals the real business driver is reducing carrier detention and demurrage fees by 30%, not adding capabilities the current process lacks.

- A) Frame the rollout around transformation, arguing new automated capability justifies the investment even though discovery pointed at a cost driver.
- B) Frame the rollout around throughput and efficiency gains exclusively, since faster cycle times are easier to demonstrate than fee reduction.
- C) Skip formal pillar framing and let the detention-fee savings show up in the executive dashboard after go-live.
- D) Frame around cost reduction, anchoring both the architecture and success metrics on detention/demurrage fee reduction.

**Question 2.** Procurement, mode selection, and exception handling each require different steps depending on carrier responses, inventory position, and disruptions discovered mid-shipment.

- A) Use an agentic pattern, since the right sequence of procurement, mode-selection, and exception steps varies by shipment and depends on intermediate findings.
- B) Use a fixed workflow with a predetermined step order, since freight logistics across carriers is standardized enough that branching adds needless complexity.
- C) Use a single augmented LLM call with retrieval and tools, since one well-prompted call can absorb procurement, routing, and exception handling together.
- D) Pick whichever pattern prototypes fastest this sprint, since procurement, routing, and exception handling are functionally interchangeable workloads.

**Question 3.** The design has a coordinator delegating to subagents (procurement, routing, exception-handling, customs-compliance). Every subagent works correctly, but shipments requiring both a customs hold and a carrier substitution are never routed to any subagent — they fall through silently.

- A) Add a fifth "edge case" subagent whose whole job is catching any shipment that none of the four existing specialists recognize as belonging to their own domain.
- B) Instruct each subagent to flag any shipment whose details look unfamiliar, so the coordinator can retry routing.
- C) Broaden every subagent's tool access so any of the four can pick up a compound customs-plus-substitution case if it slips through.
- D) Fix the coordinator's decomposition to explicitly cover compound cases like simultaneous holds and substitutions.

**Question 4.** Meridian's ops leadership wants the architecture aligned to a specific, named business value pillar rather than a generic "we added AI" narrative.

- A) Name a specific pillar — efficiency, cost, transformation, or performance-SLA — and let that choice drive both the architecture and its success metrics.
- B) Treat any automated system as inherently demonstrating transformation, since replacing manual steps with AI is transformation by definition.
- C) Treat business value pillars as a sales and marketing concern that architecture doesn't need to reference.
- D) Defer picking a pillar until after launch, then choose whichever benefit turned out easiest to report to leadership.

**Question 5.** Dispatch coordinators are skeptical of the system and worried it will replace their jobs; this comes up repeatedly in discovery interviews.

- A) Treat the sentiment as noise, since job-security worries aren't a technical requirement for the system design.
- B) Proceed with the design as planned and hand the sentiment entirely to a separate change-management workstream later.
- C) Recommend shelving the project based on dispatcher pushback alone, without weighing the cost case discovery already established for the rollout.
- D) Treat the sentiment as a real implicit constraint that shapes rollout sequencing and where human-in-the-loop checkpoints matter most.

**Question 6.** A stakeholder asks why the exception-handling subagent uses a higher-capability, higher-cost model tier than the procurement subagent.

- A) Answer that exception handling is "the more important subagent," treating that framing alone as sufficient justification for the stakeholder.
- B) Avoid the tier question altogether, on the assumption that stakeholders don't need or want any technical detail.
- C) Explain the tradeoff explicitly — exception handling needs deeper reasoning over disruptive events, justifying its cost, while procurement is routine.
- D) Use the same tier everywhere for simplicity, arguing that per-task tier tuning isn't worth the ongoing configuration and monitoring overhead it adds.

**Question 7.** The current design produces a route/mode recommendation with no mechanism to learn from dispatcher overrides or actual delivery outcomes.

- A) Treat the lack of a feedback loop as acceptable, since the initial design reflects current best practice for a first release.
- B) Add a feedback loop capturing dispatcher overrides and delivery outcomes as a first-class architectural component.
- C) Treat feedback loops as a data-science team's concern, outside the scope of the architecture being reviewed here.
- D) Defer any feedback mechanism to a hypothetical future phase, with no hooks or schema reserved for it in the current design.

**Question 8.** Meridian's customer-service team wants a single enhanced LLM call — with retrieval over the carrier-rate/contract database — to answer straightforward "what's my current rate to lane X" questions, without any multi-step autonomous orchestration.

- A) Build a full multi-agent architecture with a coordinator and specialists, regardless of how simple the rate-lookup task actually is.
- B) Use an augmented LLM pattern — a single call enhanced with retrieval and tools — which fits this simpler augmentation need.
- C) Require a fixed workflow with at least five sequential steps, even though the request is a single lookup.
- D) Say this can't be built with Claude at all, since it involves no autonomous multi-step agent behavior.

**Question 9.** The procurement subagent's toolset has grown to include tools for tasks like driver payroll lookup and warehouse-staffing scheduling, unrelated to procurement.

- A) Treat the added tools as having no architectural downside as long as the subagent's prompt is validated once at launch.
- B) Treat more tools as always improving flexibility, and actively encourage adding further unrelated capabilities.
- C) Increase the subagent's context window, on the theory that a bigger window offsets a larger, less-structured tool list.
- D) Remove or relocate the unrelated tools, since this capability bloat degrades tool-selection reliability.

**Question 10.** The coordinator currently processes each shipment sequentially through procurement, routing, exception-check, and customs-check, even though routing and customs-check have no dependency on each other's output.

- A) Keep processing sequential, arguing that only strict step-by-step execution is auditable for a shipment record.
- B) Run routing and customs-check as independent, parallel subagent calls once procurement completes.
- C) Say true parallelization isn't possible once a coordinator delegates to specialized subagents.
- D) Merge routing and customs-check into one subagent so the sequencing question never has to be answered.

**Question 11.** Meridian's executive steering committee, unfamiliar with technical detail, asks for a high-level description of the architecture.

- A) Present only model names and per-call token costs, since that's the detail executives ultimately approve.
- B) Describe input, processing, output, and the feedback loop at a level the committee can evaluate against business outcomes.
- C) Present the full technical architecture diagram exactly as built, including the raw system prompt text, with no simplification.
- D) Skip the high-level description entirely and move straight into a live implementation demo.

**Question 12.** A competing vendor proposes a single generalist agent holding every tool (procurement, routing, exception handling, customs) instead of a coordinator with specialized subagents.

- A) Say a single generalist agent scales better as the tool count grows, since it avoids coordination overhead between subagents.
- B) Say there's no meaningful architectural difference between a generalist agent and specialized subagents.
- C) Say a single agent holding every tool is more likely to suffer degraded tool-selection reliability than scoped subagents.
- D) Say specialized subagents are strictly a cost-increasing choice with no reliability benefit over one agent.

**Question 13.** The architecture must eventually support a new mode of transport (intermodal rail) Meridian plans to add next year, but detailed requirements aren't yet available.

- A) Ignore intermodal rail entirely until Meridian delivers detailed requirements next year.
- B) Design current decomposition with reasonable extensibility, without over-building for requirements that aren't defined yet.
- C) Build full intermodal-rail support now, inventing requirements Meridian hasn't specified yet.
- D) Refuse to proceed with the current phase at all until next year's full intermodal-rail requirements are finalized and signed off.

**Question 14.** The steering committee wants documentation a new engineering team can use to extend the system in a year, without the original architect present.

- A) Document only final configuration values, since a well-built implementation should be self-explanatory.
- B) Document the architecture and the reasoning behind key decisions — pattern choices, decomposition, tier selections — not just the final values.
- C) Plan for the original architect to remain reachable indefinitely, instead of writing anything down.
- D) Treat documentation as unnecessary as long as the codebase itself stays well-organized.

**Question 15.** Discovery also surfaces that Meridian's warehouse-staffing team assumed this project would also automate staffing schedules, which was never in scope.

- A) Clarify and document scope explicitly with the staffing team now, rather than let the assumption persist into delivery.
- B) Quietly build staffing-schedule automation too, so no stakeholder ends up disappointed at launch.
- C) Ignore the misunderstanding, since staffing automation was never written into the original requirements document.
- D) Cancel the current project until every stakeholder's expectations are fully unified.

---

## Scenario B: RAG Integration for a Legal Case-Law Research Platform (Questions 16–30)

Caselight is a legal research platform that wants Claude to answer attorney questions using retrieval over case law, statutes, and secondary treatises, combined with general reasoning. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most attorney queries are moderately complex research questions; a small fraction require deep multi-step reasoning across many cases, and a small fraction are simple citation lookups.

- A) Route by difficulty — a fast tier for citation lookups, a balanced tier for typical research, and a higher-capability tier with extended thinking for deep multi-case reasoning.
- B) Always use the highest-capability tier, to guarantee quality on every single question regardless of its actual difficulty.
- C) Use one fixed model tier for every question, regardless of whether it's a lookup or a multi-case synthesis.
- D) Always use the fastest, cheapest tier, accepting the quality loss on the deep multi-case questions.

**Question 17.** Every request sends the same long system prompt (jurisdiction rules, citation style, formatting requirements) followed by retrieved case excerpts that vary per query.

- A) Say prompt ordering doesn't affect cost or latency for a retrieval-heavy legal research workload.
- B) Place the stable system prompt first with caching enabled, and the varying retrieved excerpts after it.
- C) Put the retrieved excerpts before the system prompt, since they're the content most relevant to the specific attorney query.
- D) Alternate system instructions and retrieved content throughout the prompt on each turn.

**Question 18.** The corpus mixes long-form judicial opinions with short structured data (a table of statute citations and effective dates).

- A) Use one chunking strategy tuned for long-form opinions and apply it to the short structured statute table too.
- B) Match chunking and indexing strategy to each data shape, since one strategy tuned for opinions degrades retrieval for structured records.
- C) Exclude the structured statute-citation table from retrieval entirely, keeping only long-form opinions indexed.
- D) Use the largest possible chunk size everywhere, to avoid maintaining two separate chunking strategies.

**Question 19.** Attorney queries range from exact lookups ("cite for Smith v. Jones") to conceptual questions ("how has the reasonable-reliance standard evolved across circuits").

- A) Use only embedding similarity search, ignoring the structured citation metadata, for both exact lookups and conceptual questions.
- B) Use only structured or metadata filtering, for both exact citation lookups and open-ended conceptual questions.
- C) Match retrieval to query pattern: metadata filtering for exact lookups, embeddings for conceptual questions, hybrid where both matter.
- D) Treat query pattern as irrelevant to which retrieval approach is the right fit for a given attorney question.

**Question 20.** Attorneys need citations that reliably map each legal claim to a specific case and pincite, and generic prose responses often lose this mapping.

- A) Require structured output pairing each claim with its case, reporter citation, and pincite, so mapping survives synthesis.
- B) Ask the model, in prose only, to "always cite sources," with no schema or field structure behind the instruction.
- C) Add citations after drafting, by searching afterward for a plausible case to attach to each already-written claim.
- D) Append a general bibliography of consulted cases at the end, without tying any specific claim to a specific source.

**Question 21.** Two retrieved cases disagree on how a particular statute of limitations is tolled — likely because they're from different circuits with different precedent.

- A) Average the two circuits' tolling positions together and present a single blended rule to the attorney.
- B) Omit the tolling analysis from the answer entirely, since the two retrieved cases disagree with each other.
- C) Always prefer whichever of the two conflicting cases the retrieval system happened to return first.
- D) Present both positions explicitly, attributed to their respective circuits, rather than blending or silently picking one.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the "always output valid JSON" instruction more emphatically, assuming the model's structured output is deterministic once phrased right.
- B) Increase max_tokens, on the theory that more room fixes a preamble the model keeps generating before the JSON.
- C) Use tool-use or schema-constrained output so structure is enforced by the API mechanism, not requested through prose.
- D) Post-process every response to strip any leading text that appears before the first curly brace.

**Question 23.** The platform needs to connect to a proprietary internal brief bank, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this research platform.

- A) Hard-code the brief-bank integration into this one research platform's application code only.
- B) Paste the entire proprietary brief bank into every prompt that might need to reference it.
- C) Build an MCP server exposing brief-bank operations as tools/resources, reusable across the internal tools.
- D) Require each internal tool that needs the brief bank to reimplement its own separate integration and authentication layer independently.

**Question 24.** The team debates between exposing the full case-law catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Load the full case-law catalog into every prompt up front, on the theory that completeness always wins.
- B) Treat context cost as roughly the same either way, since loading the full catalog and querying it on demand end up costing about the same per query.
- C) Never expose the catalog to the agent in any form, forcing attorneys to search it manually outside Claude.
- D) Use progressive discovery, querying a catalog resource as needed, which scales better as the corpus grows.

**Question 25.** An attorney asks a chain-of-thought-friendly question requiring the model to reason step by step across several retrieved opinions before concluding on a multi-factor test.

- A) Use chain-of-thought prompting, letting the model reason step by step across the retrieved opinions before concluding.
- B) Use zero-shot prompting with no reasoning guidance, since it performs equally well on any multi-document synthesis task.
- C) Treat chain-of-thought prompting as useful only for coding tasks, not for legal multi-factor analysis.
- D) Say the model can't reason across multiple documents no matter which prompting approach is used.

**Question 26.** The platform wants to standardize prompt fragments (citation format, jurisdiction disclaimers, formatting rules) across several different attorney-facing features so changes propagate consistently.

- A) Duplicate the citation-format and disclaimer fragments into each attorney-facing feature's prompt independently.
- B) Use modular, versioned prompt fragments shared across features — distinct from caching's cost/latency role or Skills' capability packaging.
- C) Treat modular prompt fragments as just another name for prompt caching, since both involve reusing prompt content.
- D) Say standardization across features isn't something prompt design can achieve at all.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific holding from the correctly retrieved opinion.

- A) Apply defensive validation — check extracted holdings against the actual source excerpt rather than trusting confident phrasing.
- B) Trust the fluent, well-cited-looking output as sufficient evidence that the holding was already validated.
- C) Say this is purely a model limitation with no architectural mitigation available at all.
- D) Increase the output's length, on the theory that more room to elaborate reduces misstatement risk.

**Question 28.** The team debates whether attorney-facing latency SLAs should factor into model tier selection for the research platform.

- A) Say latency should never factor into model or architecture decisions, regardless of the platform's SLA.
- B) Say only cost should factor into tier selection, and latency should never be part of that decision.
- C) Weigh accuracy needs against the latency and cost the SLA can tolerate, instead of defaulting to the most capable tier regardless of SLA.
- D) Treat SLAs as a stakeholder-communication topic with no bearing on the technical tier-selection decision.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Pin the current production version and evaluate the new release against the platform's own tests before deliberately upgrading.
- B) Keep floating to "latest" automatically in production, since a newer model is always better than an older one.
- C) Never upgrade the model again once an initial version has been chosen for production.
- D) Upgrade immediately without testing, since an improved benchmark score guarantees a production improvement.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved case excerpts must fit alongside room for a detailed analytical answer.

- A) Treat input and output token budgets as entirely independent of one another within a single context window.
- B) Say this tradeoff only matters for unusually long documents that approach the model's maximum context window, never for a typical query.
- C) Say output length has no practical limit, regardless of how much retrieved content the input already uses.
- D) Balance retrieved-content volume against room for a detailed answer, since input and output share one context budget.

---

## Scenario C: Evaluation and A/B Testing of a Sales-Forecasting Copilot (Questions 31–45)

A Claude-powered copilot at Northwind Analytics helps sales reps and managers forecast pipeline and deal close probability. It's been in production for six months, and you're responsible for the evaluation strategy, diagnosing quality issues, and running A/B tests on prompt/model changes.

---

**Question 31.** The team currently measures only forecast accuracy against actuals and hasn't defined targets for latency, cost, or safety/guardrail behavior.

- A) Treat forecast accuracy alone as sufficient, since it's the copilot's stated primary purpose.
- B) Treat latency and cost as pure operations concerns, unrelated to how evaluation itself is designed.
- C) Treat safety and guardrail metrics as relevant only for heavily regulated industries like finance or healthcare, not an internal sales copilot.
- D) Define accuracy, latency, cost, and safety as first-class metrics, since forecasting well isn't enough on its own.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed set of past quarters' actual outcomes.

- A) Say one automated accuracy check against past quarters is sufficient for any production system's eval needs.
- B) Replace the automated checks entirely with human review, dropping automation from the eval suite altogether.
- C) Use mixed methods — automated eval for scale, manager judgment for nuanced calls, adversarial testing for safety paths.
- D) Expand the labeled historical dataset indefinitely, treating that as the sole lever for improving evaluation.

**Question 33.** The team wants to test whether a new prompt version improves forecast-narrative quality before rolling it out to all sales reps.

- A) Roll the new prompt out to every rep immediately and monitor informally afterward for problems.
- B) Change the prompt version and the underlying model tier at the same time, to try to maximize the potential improvement in one pass.
- C) Skip testing altogether, on the assumption that prompt changes are inherently low-risk.
- D) Run an A/B test changing only the prompt version against a stable baseline, isolating that one variable.

**Question 34.** A forecast narrative is factually wrong about a deal's stage. Investigation shows the CRM data was correct and retrieved properly, and the model's response paraphrased it inaccurately.

- A) Treat this as a retrieval problem and start by reworking the CRM indexing pipeline.
- B) Say this can't be diagnosed at all without retraining the underlying model.
- C) Treat this as a model-tier mismatch requiring a switch to a different, presumably more capable tier, regardless of what the investigation actually found.
- D) Treat it as a prompt or generation issue — inaccurate paraphrasing of correctly retrieved data — needing prompt or output-validation fixes.

**Question 35.** Immediately after a scheduled CRM data-sync refresh, the copilot starts producing confident but incorrect deal-stage references, while model version and average latency are unchanged.

- A) Suspect the model provider silently pushed an unannounced update to the underlying model version, changing behavior with no notice to the team.
- B) Suspect a temperature setting change, since the narratives suddenly sound more confident.
- C) Investigate retrieval/indexing first, since the regression tracks the sync event while model and latency stayed unchanged.
- D) Suspect the context window shrank, cutting off part of the retrieved deal record.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting forecast accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Optimize cost, latency, and accuracy each independently, in isolation from the other two.
- B) Always maximize accuracy first, regardless of what it costs or how much latency it adds.
- C) Optimize cost, latency, and accuracy jointly against the SLA and budget, instead of maximizing any one alone.
- D) Say this tradeoff can't be measured at all with the data currently available, only guessed at from prior experience.

**Question 37.** Production monitoring currently reports only an overall monthly average forecast-accuracy score across all sales regions, hiding drift specific to one region.

- A) Add per-region breakdowns to increase visibility into region-specific drift that a single monthly average can hide.
- B) Say a single aggregate monthly average is sufficient for production monitoring on its own.
- C) Track only cost in monitoring, since the eval suite alone already covers accuracy.
- D) Say monthly granularity is always sufficient, regardless of how quickly a given region's underlying drift actually develops week to week.

**Question 38.** The team proposes cutting manager review of flagged low-confidence forecasts by 80%, citing a 96% aggregate accuracy score.

- A) Segment accuracy by region and deal size before cutting review, since the aggregate could mask a weak segment.
- B) Proceed with the 80% review cut based on the 96% aggregate accuracy figure alone.
- C) Treat aggregate accuracy as automatically representative of performance in every single region and every deal-size bucket without exception.
- D) Refuse to reduce manager review at all, regardless of what a segment-level analysis might show.

**Question 39.** An A/B test shows a new prompt version improves narrative-quality ratings, but the team has not checked whether it also changed the rate of overconfident forecasts on genuinely volatile deals that should be flagged as uncertain.

- A) Check the uncertainty-flagging rate on volatile deals, since a narrative-quality gain could hide more overconfidence there.
- B) Treat the narrative-quality rating alone as a sufficient signal that the new prompt is safe to ship.
- C) Say overconfidence behavior on volatile deals isn't something an evaluation can actually measure.
- D) Ship the new prompt version to all reps and monitor informally afterward instead of testing for this specific failure mode beforehand.

**Question 40.** The team wants to diagnose why a subset of forecasts are numerically accurate but rated as unhelpful by sales managers in feedback surveys.

- A) Investigate a dimension beyond accuracy, like actionability or relevance to the manager's own pipeline.
- B) Assume the accuracy metric itself must be broken, and discard it from the eval suite entirely.
- C) Increase the model's capability tier across the board, on the assumption that higher capability always raises perceived helpfulness too.
- D) Ignore the manager feedback survey scores, since the accuracy metric alone is already validated by past quarters.

**Question 41.** The team is optimizing token usage and notices the system sends the full deal history plus a large static sales-methodology reference on every turn of multi-turn conversations with reps.

- A) Say there's no optimization opportunity here at all, since sending the full deal history on every single turn is always strictly required.
- B) Switch to a smaller model as the only lever considered for reducing per-turn token cost.
- C) Remove the sales-methodology reference entirely, dropping it from every turn to save tokens.
- D) Cache the static methodology reference and trim older turns to cut redundant token cost.

**Question 42.** Logging captures every raw prompt and response for the production copilot, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Treat raw logging at full volume, with every prompt and response captured verbatim, as itself a sufficient observability strategy.
- B) Reduce logging volume to save on storage cost, without validating whether the reduced set still captures failure patterns.
- C) Say observability needs no structure at all, as long as the raw data is retained somewhere.
- D) Redesign observability toward structured, sampled signals with tagged failure categories.

**Question 43.** The team wants to identify whether a specific forecast-quality regression was caused by a recent prompt change, a recent model version change, or a CRM schema change — all three happened in the same week.

- A) Assume the most recently shipped change is always the one responsible for the regression.
- B) Isolate and re-test each of the three changes independently, since attribution requires exactly that discipline.
- C) Say attribution becomes impossible once more than one change has shipped in the same week.
- D) Revert all three changes at once immediately without investigating which one, if any of them, actually caused the regression.

**Question 44.** An automated eval asserts that a forecast-narrative output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) Say the model itself is malfunctioning and should be scheduled for a full retraining cycle based on these intermittent evaluation failures.
- B) Make the fixed reference string longer, so the exact-match check has more text to compare against.
- C) Replace the exact-match eval with a content/structure check, since output varies run to run even at a fixed temperature and won't suit exact matching.
- D) Increase the temperature setting, on the theory that it will fix the eval's intermittent failures.

**Question 45.** Leadership wants a single number to represent "how good" the sales-forecasting copilot is, to track over time.

- A) Say a single number is always achievable and sufficient for evaluating any production system.
- B) Use forecast accuracy alone as the single number, since it matches the copilot's stated purpose.
- C) Refuse to provide any single summary metric to leadership under any circumstances, insisting only on a full multi-page breakdown.
- D) Offer a single aggregate metric as a top-line indicator, paired with segment-level detail so it can't mask a failing area.

---

## Scenario D: Lifecycle Management and Enablement for a Global Manufacturing Rollout (Questions 46–60)

Ferrotech Industries, a global manufacturer, is rolling out a Claude-powered production-line quality-inspection assistant across plants in multiple countries, alongside internal Claude Code enablement for its distributed engineering teams. You are responsible for governance, phased global rollout, lifecycle management, and developer enablement.

---

**Question 46.** The architecture team is finalizing data residency, retention, and access-logging design for plant-floor quality data in the final weeks before the first regional rollout, after core application logic is already built.

- A) Say this sequencing carries no risk, since compliance details can always be bolted on right before launch.
- B) Say compliance only affects legal paperwork, with no bearing on the system's actual architecture.
- C) Say cross-border residency and access-control requirements can force structural changes costlier to retrofit than to design in up front.
- D) Assume a single global data-handling policy is guaranteed to satisfy every plant's local regulatory regime across every country of operation.

**Question 47.** A team proposes requiring human approval on every single output the quality-inspection system produces across all plants, framing it as the safest governance posture for a global rollout.

- A) Say maximal human review on every output is always the correct default posture for manufacturing AI.
- B) Say human reviewers are categorically less accurate than the model, making review counterproductive everywhere.
- C) Target human-in-the-loop at high error-cost or judgment-requiring calls, since blanket review on every output defeats the system's value.
- D) Say this blanket-review approach is required by every relevant regulatory regime that could plausibly apply to this global rollout, regardless of other considerations.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from free-text inspector notes, and inconsistent output — as part of its design across every plant.

- A) Design mitigations for each known failure mode up front — grounding for hallucination, isolation for injection, validation for consistency.
- B) Address these risks only if and when they're actually observed happening in production first.
- C) Say a single generic guardrail addresses hallucination, injection, and inconsistency equally well.
- D) Say these risks are exclusive to consumer-facing products built for the public, not to an internal manufacturing tool used by trained staff.

**Question 49.** The plant-safety team asks whether the system's defect-flagging decisions could produce inconsistent outcomes across different plants with different equipment vintages and lighting conditions.

- A) Say this isn't an architectural concern at all, and belongs entirely to legal review after launch.
- B) Say disparate outcomes across plants are impossible in an LLM-based system by construction.
- C) Evaluate whether eval data reflects the range of plant conditions and measure for disparate performance rather than assume it's absent.
- D) Say this concern only applies to a system making final automated shutdown decisions on its own, not one that merely assists a human inspector.

**Question 50.** Engineering teams across Ferrotech's plants have inconsistent Claude Code usage — some plants have team conventions applied automatically, others don't, and internal MCP server access to plant systems varies by machine.

- A) Restrict Claude Code usage globally to a single designated engineer, to reduce configuration variance.
- B) Standardize the CLAUDE.md hierarchy and shared MCP configuration at the organization level, so behavior doesn't depend on local setup.
- C) Have each plant's engineers individually troubleshoot their own local configuration as issues come up.
- D) Accept the inconsistency as an unavoidable, permanent cost of running a coordinated rollout across so many plants and countries.

**Question 51.** The team wants Claude Code-generated code changes to plant-control-adjacent software to go through the same review rigor as any other change to a safety-relevant system.

- A) Let AI-assisted code bypass the standard review process, since it was "written by AI" rather than a person.
- B) Keep standard SDLC practices in place — review, testing, version control — since AI assistance doesn't reduce required rigor.
- C) Apply only a light spot-check to AI-generated code, skipping the review a human-written change would get.
- D) Lower review requirements specifically for AI-generated code relative to equivalent human-written changes to the same system.

**Question 52.** A production incident at one plant traces back to a Claude Code-generated change to the inspection-data pipeline. The team can't immediately tell whether the bug is in the generated code logic or in how the plant's surrounding system integrated it.

- A) Assume the bug lives in the generated code without validating that assumption against the surrounding integration.
- B) Disable Claude Code across every plant globally following this one incident.
- C) Roll back every recent Claude Code-assisted change at every plant worldwide, regardless of whether it's even related to this incident.
- D) Triage it the way any incident is triaged — isolate integration versus code/model failure using traces and logs.

**Question 53.** A plant's engineering team wants a documented, repeatable workflow for a recurring task (generating a weekly quality-defect summary report) versus a one-off exploratory investigation into a new sensor integration.

- A) Build both the recurring report and the one-off investigation as ad hoc, undocumented prompts each time.
- B) Package the recurring report as a Skill for consistent reuse; leave the one-off investigation unstructured.
- C) Build both the recurring report and the one-off sensor investigation as dedicated MCP servers, regardless of their actual reuse profile.
- D) Say recurring workflows and one-off explorations should always be built the same way.

**Question 54.** Ferrotech's compliance team wants documented evidence of who accessed what plant-floor quality data through the system and when, across every regional deployment.

- A) Design access-control and audit-logging as explicit architectural components satisfying identity and monitoring requirements.
- B) Treat access logging as optional, as long as the system already has a structured, role-based permission scheme configured.
- C) Say audit logging can be added later, with no real impact on the architecture built up to that point.
- D) Log only failed access attempts, leaving every successful access to plant-floor data completely unrecorded and unreviewable.

**Question 55.** The global rollout's steering committee includes plant operations, legal/compliance, and engineering stakeholders across regions, each with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, on the assumption they'll relay everything to the rest.
- B) Skip stakeholder communication entirely until the system is fully rolled out to every plant.
- C) Tailor architectural communication to each audience, framing tradeoffs in terms plant operations and legal/compliance can evaluate.
- D) Send identical technical documentation to every audience across every region, to save time preparing separate materials for each group.

**Question 56.** Midway through the global rollout, requirements shift meaningfully after a new regional safety regulation is issued in one of the countries where Ferrotech operates.

- A) Refuse to incorporate the new regional safety regulation, since requirements were already agreed upon.
- B) Re-engage discovery for the affected region's scope, communicate the tradeoff, and adjust design and timeline.
- C) Incorporate the regulatory change silently, without telling stakeholders what it changes.
- D) Restart the entire global rollout from scratch across every plant and region, regardless of how narrow the regulation's actual scope is.

**Question 57.** After the final plant's rollout, the architect's involvement is discussed as ending at handoff to each plant's local operations team.

- A) Keep monitoring and iteration on production signal as part of the architect's ongoing responsibility, not just handoff.
- B) Treat this as correct — monitoring and iteration become entirely the local operations team's responsibility once handoff is complete.
- C) Treat lifecycle responsibility as ending once the rollout contract is signed.
- D) Say monitoring is only necessary if a major incident actually occurs at a given plant.

**Question 58.** Documentation for the global rollout currently lists final configuration values (model tier, retry settings, thresholds per region) with no explanation of why each was chosen.

- A) Say listing final configuration values alone is sufficient documentation, since the "what" is really all a future team needs to know.
- B) Say documenting the reasoning behind each value is unnecessary overhead in a multi-region rollout.
- C) Capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend the system.
- D) Say only the original architect should ever be allowed to modify the system, making documentation moot.

**Question 59.** Plant engineering teams want Claude Code to help with routine tasks (drafting maintenance documentation, exploring an unfamiliar legacy control module) but are unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves meaningful time on every task category by default.
- B) Ban Claude Code for all documentation tasks outright, without evaluating where it actually helps.
- C) Mandate Claude Code usage for every single task across every plant, regardless of any measured benefit or engineer feedback about actual time saved.
- D) Evaluate task categories for genuine friction reduction versus overhead that may exceed the time saved.

**Question 60.** A recurring operational issue is that different plant engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) Treat the redundant re-derivation across plants as an acceptable ongoing inefficiency with no architectural fix.
- B) Document the triage process — how to tell integration-layer failures from model-output failures — as shared operational knowledge.
- C) Restrict all debugging of Claude Code integration failures to one designated global engineer.
- D) Say the issue can only be resolved by switching to an entirely different tool.

---
# Answer Key

**Quick key:** 1-D, 2-A, 3-D, 4-A, 5-D, 6-C, 7-B, 8-B, 9-D, 10-B, 11-B, 12-C, 13-B, 14-B, 15-A, 16-A, 17-B, 18-B, 19-C, 20-A, 21-D, 22-C, 23-C, 24-D, 25-A, 26-B, 27-A, 28-C, 29-A, 30-D, 31-D, 32-C, 33-D, 34-D, 35-C, 36-C, 37-A, 38-A, 39-A, 40-A, 41-D, 42-D, 43-B, 44-C, 45-D, 46-C, 47-C, 48-A, 49-C, 50-B, 51-B, 52-D, 53-B, 54-A, 55-C, 56-B, 57-A, 58-C, 59-D, 60-B

---

**1. D** — Discovery pointed to a cost driver (detention/demurrage fees), so the architecture and metrics should be anchored on cost reduction. A and B reach for a different pillar than what discovery found; C skips framing that keeps the project aligned to real value.

**2. A** — Steps that vary by shipment and depend on intermediate findings (carrier responses, disruptions) are the defining case for an agentic pattern. B assumes a predictability the scenario lacks; C undersells the orchestration needed; D treats genuinely different patterns as interchangeable.

**3. D** — Whole compound case categories never being routed at all is a coordinator decomposition gap, not a subagent performance issue. A, B, and C all patch downstream instead of fixing the actual scope gap in the coordinator's routing logic.

**4. A** — Naming a specific pillar (efficiency, cost, transformation, SLA) gives both architecture and metrics a clear anchor. B, C, and D each skip or defer that framing in ways that risk building toward the wrong measure of success.

**5. D** — Adoption sentiment from dispatchers is a real implicit constraint shaping rollout sequencing and HITL placement, not noise to dismiss. A and B treat it as out of scope; C overreacts to sentiment alone without weighing the cost case already established.

**6. C** — Explaining the specific tradeoff (deeper reasoning need vs. cost/latency) is the standard for communicating tier decisions to stakeholders. A and B withhold reasoning stakeholders need; D removes a deliberate, justified difference for false simplicity.

**7. B** — A first-class feedback loop capturing dispatcher overrides and outcomes is what lets the system improve post-deployment. A, C, and D each treat this component as optional, someone else's job, or a someday concern.

**8. B** — A single call enhanced with retrieval, without multi-step orchestration, is exactly what an augmented LLM pattern serves. A and C over-engineer a simple augmentation need; D is factually wrong.

**9. D** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows. A and B ignore this real degradation; C treats a bigger context window as a substitute for fixing the actual selection problem.

**10. B** — Independent subagent calls with no shared dependency can run in parallel once their prerequisite (procurement) completes, cutting latency without sacrificing correctness. A and C misstate real constraints; D avoids the sequencing question rather than answering it.

**11. B** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail, C is too much of the wrong kind, and D skips the communication need entirely.

**12. C** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles. A, B, and D understate or deny this real architectural tradeoff.

**13. B** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A ignores a known future need; C wastes effort guessing; D blocks current delivery unnecessarily.

**14. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave the actual knowledge-transfer gap unaddressed.

**15. A** — Clarifying and documenting scope now prevents an unspoken assumption from becoming a delivery conflict later. B expands scope without agreement; C ignores a real stakeholder misunderstanding; D is a disproportionate reaction to a clarifiable gap.

**16. A** — Routing by task difficulty matches fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex research questions. B and D ignore fit-to-task; C sacrifices quality on the cases that need capability most.

**17. B** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, C, and D all misstate or break the caching opportunity.

**18. B** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and D ignore this mismatch; C discards useful structured data.

**19. C** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and B force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. A** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. B, C, and D all reintroduce the failure mode the fix is meant to prevent.

**21. D** — Presenting both positions with attribution preserves the actual information for the attorney rather than resolving a genuine jurisdictional conflict arbitrarily. A, B, and C all discard or obscure a real disagreement.

**22. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and D are workarounds for a structurally solvable problem; B doesn't address the preamble at all.

**23. C** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. A, B, and D all fail the reuse or maintainability requirement.

**24. D** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. A and B ignore the real context cost of the monolithic approach; C removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning across a multi-factor test. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. B** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. A** — Verifying extracted holdings against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. B is the failure mode itself; D doesn't address correctness; C incorrectly claims no architectural mitigation exists.

**28. C** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, B, and D each drop a relevant factor from the decision.

**29. A** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. B and D assume benchmark gains transfer automatically; C over-corrects into permanent stagnation.

**30. D** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and C all misstate this real, architecture-relevant constraint.

**31. D** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if it forecasts well. A, B, and C each drop a dimension that materially affects whether the system is actually working.

**32. C** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. A, B, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. D** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; C dismisses a real risk without evidence.

**34. D** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. A and C misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. C** — A regression tied specifically to a data-sync event, with model and latency unchanged, points first at retrieval/indexing. A, B, and D would not specifically correlate with a CRM data-sync refresh.

**36. C** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and B optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate monthly average can hide, such as region-specific drift. B and D accept a monitoring blind spot; C drops accuracy monitoring from observability entirely.

**38. A** — Segmenting accuracy by region and deal size before cutting review protects against a failing segment hiding behind a healthy aggregate. B and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. A** — An isolated narrative-quality improvement could mask a worsened overconfidence failure mode; checking specifically for that before shipping is the correct diagnostic step. B and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. A** — "Accurate but unhelpful" points at an unmeasured quality dimension (actionability, explanation quality) rather than a broken accuracy metric. B and D discard a working, differently-scoped metric; C assumes a fix without diagnosis.

**41. D** — Caching the static methodology reference and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; C removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. D** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and C accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. B** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and D guess without evidence; C gives up on a solvable (if effortful) diagnostic problem.

**44. C** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. C** — Cross-border data residency, retention, and access-control requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate real architectural impact; D wrongly assumes one policy fits every regime.

**47. C** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically, like borderline defect calls. A and B overstate the universal safety case for maximal review; D makes an unsupported blanket regulatory claim.

**48. A** — Designing mitigations for each known failure mode (grounding for hallucination, isolation for injection, validation for consistency) up front is the architecture-first approach the domain calls for. B defers to a reactive posture; C assumes one guardrail covers distinct risk types; D is factually wrong.

**49. C** — Consistency and fairness across deployment contexts are architecture concerns requiring active measurement (data representativeness across plant conditions, disparate-performance checks), not an assumption of absence. A defers a design concern entirely to a later stage; B and D make unsupported blanket claims.

**50. B** — Standardizing CLAUDE.md and shared MCP configuration at the organization level directly fixes the described inconsistency, which stems from relying on individual local setup. C and D leave the systemic cause unaddressed; A sacrifices the tool's benefit for the rest of the organization.

**51. B** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially for safety-relevant systems. A, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for this context.

**52. D** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and C skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. B** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory investigation unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. A** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. B, C, and D each understate what compliance-grade audit evidence actually requires.

**55. C** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by plant operations, legal/compliance, and engineering alike. A, B, and D each fail to serve at least one audience's real information need.

**56. B** — Re-engaging discovery for the affected region's scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and C mishandle a real change; D disproportionately discards unaffected work.

**57. A** — Lifecycle management extends through monitoring and iteration based on production signal, not just through discovery and handoff. B, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. C** — Capturing the "why" (regional compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend or modify the system at any plant. A, B, and D all leave that reasoning undocumented and effectively lost.

**59. D** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and C over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 10.*
