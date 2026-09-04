# Claude Platform & Solution Design Flashcards

## Four Design Decisions

Q: What four decisions does an architect make before building a Claude solution?

A: (1) What part of the work Claude owns, (2) what shape the work takes (augmented call, workflow, agent), (3) which reference architecture fits, (4) where the work interacts with Claude (entry point, model, context strategy).

Domain: D1

Example: Before scoping a claims-triage assistant, an architect first decides Claude drafts summaries (not decisions), it runs as a workflow (not an open agent), it follows the routing reference architecture, and it's delivered via the API behind the partner's own app.

## Four Properties Overview

Q: What are the four properties of generative AI that architects design around?

A: Next-token prediction, Knowledge, Working memory, Steerability — each a capability/limitation pair, not a flaw to fix.

Domain: D2

Example: A team names a failure as "a knowledge-boundary problem" instead of debating whether the model is "good enough," which keeps the design conversation precise.

## Next-Token Prediction

Q: What is Claude reliable at, and what does next-token prediction fail on?

A: Reliable on pattern-rich tasks (summarizing, reformatting, explaining established concepts); fails on precision specifics like names, dates, citations, and statistics, where it can be fluently wrong.

Domain: D2

Example: Claude confidently cites a plausible-sounding but incorrect case citation in a legal memo draft; the fix is citations, uncertainty signaling, and routing factual lookups to tools.

## Knowledge Boundary

Q: When is Claude's parametric knowledge unreliable, and what's the mitigation?

A: Unreliable for rare, niche, contested, or fast-changing topics, presented with the same confident tone as established facts. Mitigation: make an external system (web search, RAG, tool use, MCP) the source of truth instead.

Domain: D2

Example: Asking Claude the current interest rate on a specific savings product should route to a live tool call, not the model's training-time knowledge.

## Working Memory

Q: What are the two distinct errors that occur at the context-window edge?

A: An oversized request (rejected before generation, 400 invalid_request_error or 413 request_too_large) versus a mid-generation ceiling hit (returns with a model_context_window_exceeded stop reason and truncated output).

Domain: D2

Example: A 250,000-token prompt is rejected immediately with a 400 error, while a 190,000-token prompt that fits but generates a long response gets truncated mid-answer.

## Steerability

Q: What does steerability fail on, and why is that dangerous?

A: Abstract or ambiguous instructions, long reasoning chains, and precise numerical/logical computation — the model may follow the letter of an instruction while drifting from its intent.

Domain: D2

Example: Told to "route claims over five thousand pounds to senior review," Claude treats "damages estimated around five thousand pounds" as a loose estimate rather than a trigger, misrouting the claim.

## Design Consequences

Q: Match each property to its main design consequence: non-determinism, knowledge boundary, context as a finite resource, confidence-is-not-validity.

A: Non-determinism → why evaluation frameworks exist. Knowledge boundary → why retrieval/tools/MCP exist. Context as finite resource → why context strategy is a design decision. Confidence is not validity → why human-in-the-loop placement is an architectural choice.

Domain: D1

Example: A team builds an eval set specifically because a demo running clean five times is not proof the pipeline will behave the same way in production.

## Demo Is Not Determinism

Q: Why did a team's financial reconciliation pipeline drift in week two of production?

A: They concluded from five clean demo runs that behavior was deterministic and shipped without checks; re-processing the same statement later produced a different categorization because the model is non-deterministic regardless of whether the architecture acknowledges it.

Domain: D4

Example: An architect who has only ever seen a pipeline pass in staging insists it's "basically deterministic" — the correct response is to build an eval set, not trust the streak.

## Three Architecture Layers

Q: What are the three distinct architecture layers, and who is each chosen for?

A: Entry Points (chosen for the user and the work), Build-Time Interfaces (chosen for the engineering team and integration), Delivery Routes (chosen for the partner's cloud commitments and compliance posture).

Domain: D1

Example: A design review gets stuck arguing in circles until someone separates "which UI do users see" from "which API layer do engineers code to" from "whose cloud does the traffic run on."

## Entry Points Defined

Q: What is an entry point, and what are three examples?

A: What a person or system directly interacts with — the wrapper deciding who can talk to Claude and how. Examples: Claude.ai, Claude Code, a custom app built on the API.

Domain: D1

Example: A bank's branch staff use a custom SSO-authenticated web app (an entry point) rather than Claude Code, because Claude Code is built for developers running a terminal.

## Build-Time Interfaces Defined

Q: What is a build-time interface, and what are four examples?

A: How an engineer programs against Claude — the layer the partner's code is written to. Examples: the direct API, SDKs, MCP, the Agent SDK.

Domain: D3

Example: A partner's engineering team writes their integration against the TypeScript SDK rather than raw HTTP, because the SDK handles streaming and tool-use boilerplate.

## Delivery Routes Defined

Q: What is a delivery route, and what determines the right choice?

A: Where API traffic terminates — whose infrastructure the request runs on (Anthropic directly, AWS Bedrock, GCP Vertex AI, Microsoft Foundry). The right choice depends on the partner's existing cloud contract and compliance posture, not technical capability, since the model behaves identically on every route.

Domain: D3

Example: A partner with a long-standing AWS enterprise agreement routes through Bedrock so AI spend falls under the existing contract and their IAM identity system works as-is.

## Collapsed-Layers Failure

Q: What went wrong when a retail banking proposal put Claude Code in front of bank branch staff?

A: The three layers (entry point, build-time interface, delivery route) were collapsed into one undifferentiated concept ("it's all Claude"), so an engineering entry point built for developers running a terminal was proposed for a non-engineering audience.

Domain: D1

Example: The same mistake shows up when a proposal says "let's just use MCP for the front end" — MCP is a build-time interface, not something end users interact with directly.

## Seven AI Primitives

Q: Name the seven AI primitives and their one-word jobs.

A: Tools=Act, MCP=Connect, Subagents=Isolate/Parallelize, Hooks=Guarantee, Skills=Package a procedure, Agent Teams=Coordinate peers, Dynamic Workflows=Compose at runtime.

Domain: D3

Example: A code-review agent uses Tools to run a linter, Hooks to block a commit that fails a security check no matter what the model decides, and Skills to package the review checklist as one versioned unit.

## Hooks Defined

Q: What is a Hook, and why does it matter for governance?

A: Deterministic code that fires on a defined event to enforce a rule the model cannot skip — unlike a prompted instruction, a Hook is a guarantee, not a request.

Domain: D5

Example: A Hook blocks any file write outside an approved directory regardless of what the agent's reasoning concluded, closing the gap a prompt-only guardrail would leave open.

## Shared Vocabulary Failure

Q: Why did "we'll use an agent" stall a design review for twenty minutes?

A: Five people heard five different architectures (a single tool-using model, a multi-step workflow, a subagent team, Claude Code, a chatbot) because the team lacked shared primitive vocabulary.

Domain: D1

Example: Before scoping a project, a lead architect insists the team first agree whether "agent" means a single Claude call with tools or a full autonomous multi-turn loop.

## Three Solution Owners

Q: What are the three owners in solution decomposition, and what belongs to each?

A: What Claude does (language understanding, summarization, planning, drafting, tool-mediated action); what existing systems do (anything the partner already paid to make reliable, like a rules engine or database of record); what humans do (judgment calls, exception paths, approvals).

Domain: D1

Example: In a claims assistant, Claude reads and summarizes the claim, the rules engine decides priority, and a human approves any payout above a threshold.

## Delegation Justification Tests

Q: What three tests justify whether Claude should own a piece of work?

A: Reversibility (can a wrong call be undone?), Stakes (what does a wrong call cost?), Accountability (who must answer for it?).

Domain: D5

Example: Drafting a customer email is low-stakes and reversible before sending, so Claude can own the draft; approving a refund above £2,000 has real stakes and clear accountability, so a human owns the decision.

## Decomposition Framing Question

Q: What question should drive decomposition, instead of "where can Claude help?"

A: "Where do the four properties argue for Claude over the system that already does this right?"

Domain: D1

Example: Instead of asking whether Claude *could* check a coverage table, the architect asks whether Claude's knowledge boundary makes it worse than the partner's existing policy-lookup system — and routes the lookup to that system instead.

## Claims Triage Decomposition

Q: In the claims-triage worked example, why does "decide priority" belong to an existing system, not Claude?

A: Priority is a deterministic rule the partner's rule engine already maintains — what counts as priority lives in a rule engine, not in Claude's training data, so routing it to Claude introduces an unnecessary knowledge limitation.

Domain: D1

Example: Claude calls the rule engine as a tool to get the priority determination rather than inferring it from the claim text itself.

## Deterministic-Drift Failure

Q: What broke when a £5,000 claims-routing SQL check was replaced with a Claude prompt?

A: Of 14,000 claims, 41 misrouted — all cases where the amount was embedded in prose ("around five thousand pounds") rather than a clean number; a rule that needed to be right every time was handed to a system that's right most of the time, and the gap was invisible until an audit three months later.

Domain: D5

Example: An architect proposing to fold a KYC threshold check into a prompt "to keep it simple" should recall this case and keep the check in the deterministic system instead.

## Why Deterministic Drift Was Invisible

Q: Why didn't monitoring catch the deterministic-drift misroutes?

A: The kind of logging that catches a broken SQL check does not record the choices a model makes inside a single request, and the team never built test cases because they'd treated routing as something the model would "just handle" rather than a rule the business was counting on.

Domain: D4

Example: A team assumes a model-based routing step is "self-monitoring" and skips building a labeled test set for it — exactly the gap that let the misroutes go undetected for three months.

## Three Architecture Patterns

Q: What are the three architecture patterns, and how are they positioned?

A: Augmented LLM (high predictability, low autonomy — one bounded call), Workflow (predictable shape, bounded judgment per step), Agent (high autonomy, low predictability — the model owns the trajectory).

Domain: D1

Example: A single-call sentiment classifier is an augmented LLM; a multi-step contract-review pipeline coded as extract-then-classify-then-summarize is a workflow; Claude Code exploring an unfamiliar codebase is an agent.

## Augmented LLM Defined

Q: When should you use the augmented LLM pattern?

A: When the task is well-defined, the output is verifiable, and there's no reason to split the work across multiple steps — control flow never branches based on what the model decides.

Domain: D1

Example: A single Claude call that classifies a support ticket into one of five categories, optionally using a tool to look up account status, is an augmented LLM.

## Workflow Defined

Q: When should you use the workflow pattern, and why is it easier to govern than an agent?

A: When error cost is real, observability matters, and steps can be determined in advance — because control flow lives in your code, you can log, test, and reason about it like any other software.

Domain: D1

Example: A contract-review pipeline coded as extract → classify → draft-memo is loggable and testable at each step, unlike a single open-ended agent loop.

## Agent Defined

Q: When should you use the agent pattern, and what must bound it in production?

A: Only when the path through the work cannot be enumerated in advance and the cost of an unexpected/inconsistent output is acceptable and recoverable. Production agents need constrained tool entry points, per-turn budgets, explicit permissions, and stopping criteria — not optional.

Domain: D1

Example: Claude Code deciding which files to read in an unfamiliar codebase is a valid agent use case, but it still runs inside permission boundaries and stopping criteria.

## Workflow Sub-Pattern: Chaining

Q: What is the chaining sub-pattern, and when does it earn its place?

A: Step 2 takes step 1's output as input, sequential and linear. Use when the task decomposes into stages with clear handoffs, each with a defined output the next stage consumes.

Domain: D1

Example: A contract review pipeline extracts obligations first, classifies each by risk level second, then drafts a summary memo third.

## Workflow Sub-Pattern: Routing

Q: What is the routing sub-pattern, and when does it earn its place?

A: A classifier (often Claude itself) decides which downstream path to take. Use when inputs vary in kind and need different handling.

Domain: D1

Example: A support ticket classifier routes billing questions to an account-data retrieval index, technical issues to product documentation, and escalations directly to a human queue.

## Workflow Sub-Pattern: Parallelization

Q: What is the parallelization sub-pattern, and when does it earn its place?

A: Multiple model calls run concurrently and results are aggregated or voted on. Use when sub-tasks are independent and can run at the same time.

Domain: D1

Example: Twelve supplier contracts are each sent to a separate concurrent model call for a due-diligence review, then all twelve results are aggregated into one risk report.

## Workflow Sub-Pattern: Evaluator-Optimizer

Q: What is the evaluator-optimizer sub-pattern, and when does it earn its place?

A: One call drafts, a second call grades against criteria and requests revision; the loop repeats until a quality criterion is met or a retry limit is reached. Use when quality is verifiable but a single attempt isn't reliable enough.

Domain: D1

Example: A model drafts a customer-complaint response; a second call grades it against a rubric (names the issue, takes ownership, matches brand tone) and the generator rewrites until every rubric item passes or the retry limit hits.

## Five-Factor Pattern Selection

Q: What are the five factors in the pattern-selection framework, and how do you apply them?

A: Predictability, Error cost, Observability, Latency budget, Cost — walk them in sequence and stop at the first factor that rules out a pattern.

Domain: D1

Example: If error cost is high (a wrong output triggers a lawsuit), that alone rules out an agent even if latency and cost would otherwise favor it.

## Fine-Tuning Progression

Q: What is the recommended order of operations before considering fine-tuning?

A: (1) Optimize the prompt, (2) add tool use or retrieval, (3) move to a stronger pattern like evaluator-optimizer, (4) only then consider fine-tuning.

Domain: D2

Example: A team whose extraction accuracy is low first tightens the prompt and adds a retrieval step before ever proposing a fine-tuned model.

## When Fine-Tuning Has a Place

Q: In what three situations does fine-tuning make sense on Claude?

A: Very high volume where inference cost is the real constraint; latency-critical work where a smaller specialized model beats a prompted general one; output needing a consistent format that prompting hasn't reliably solved.

Domain: D2

Example: A high-volume, latency-sensitive classification endpoint processing millions of calls a day is a case where fine-tuning a smaller model might be justified after prompting alone falls short.

## Skills-Based Packaging Spectrum

Q: What are the three packaging options for a Claude capability, and when do you reach for a Skill?

A: Prompt-only (instructions alone), direct tool use (model calls functions in your code), Skills-based (a versioned, reusable, governed unit). Reach for a Skill when the same procedure runs repeatedly, must be distributed across teams/products, or must be versioned and governed.

Domain: D2

Example: A "weekly compliance report" procedure used by five different regional teams is packaged as a Skill so every team runs the exact same governed version.

## Flexibility-vs-Non-Determinism Failure

Q: What did a team discover when they mined the traces of an agent they'd built for "flexibility"?

A: The actual paths through the system fell into only four shapes, all enumerable from week one — they could have built a router with four chains and saved six months instead of rebuilding that structure inside an agent loop.

Domain: D1

Example: Before defaulting to an agent because a task "feels open-ended," an architect proposes mining a few weeks of real traces first to see if the paths are actually enumerable.

## Agent Autonomy As Compliance Risk

Q: Why did an agent-based disbursement-approval system become a compliance problem?

A: When an auditor asked which step approved a disbursement, the team could only point to a model turn with no discrete auditable step — and the model version had rolled forward two weeks earlier with no re-validation checkpoint.

Domain: D5

Example: A regulated workflow that needs to answer "which exact step approved this and on what model version" is a strong signal to prefer a workflow over an agent.

## Cost Myth About Agents

Q: Is it true that agents always cost more than workflows?

A: No — cost is driven by how much context accumulates and how many model calls are made, not the pattern label; a poorly designed workflow can cost more than a well-designed agent.

Domain: D4

Example: A workflow that re-sends the full conversation history on every step can cost more per run than a tightly bounded agent with a small per-turn budget.

## Multi-Agent Roles

Q: What are the two roles in a multi-agent system, and what does each own?

A: The Orchestrator owns the goal — decomposes work, decides delegation, synthesizes results, never does sub-task work itself. Subagents own scoped sub-tasks, each in its own context, returning a result.

Domain: D1

Example: An orchestrator splits a 400-file codebase audit into per-directory units and dispatches one subagent per unit, then synthesizes their findings into one report.

## Three Things To Design In Multi-Agent Systems

Q: What three things must be explicitly designed (not assumed) in a multi-agent system?

A: How work is decomposed into sub-tasks; how each subagent's result is structured for the orchestrator to combine; how the orchestrator resolves conflicts or gaps in returned results.

Domain: D1

Example: Two subagents reviewing overlapping sections of a document return conflicting risk ratings — the orchestrator needs an explicit conflict-resolution rule or escalation path for this case.

## Fan-Out Pattern

Q: What is the fan-out pattern, and what two wins does it produce?

A: The orchestrator splits a large work item into independent units and dispatches one subagent per unit (parallel where independent), then synthesizes results into one deliverable. Wins: clean per-unit context sizing and concurrent execution.

Domain: D1

Example: A 200-document corpus summarization job dispatches one subagent per document batch running concurrently, each with a clean, appropriately-sized context.

## Multi-Agent Failure Recoverability Asymmetry

Q: Why is a subagent failure usually recoverable while an orchestrator failure usually is not?

A: A subagent failure can be retried, re-routed, or dropped-and-flagged while the rest of the work proceeds; an orchestrator failure loses the goal or synthesis thread, so the whole run fails and partial subagent work may be stranded.

Domain: D1

Example: A design protects orchestrator state with checkpoints so a failed run can resume rather than restart, while treating individual subagent timeouts as simply retryable.

## Fan-Out Drop Failure

Q: What went wrong in the 50-section vendor-contract review that reported "48 sections reviewed, 3 flagged"?

A: Two subagents had actually failed (one timeout, one unparseable scan) and returned nothing; the orchestrator only counted results it received with no rule requiring the result count to equal the dispatched-unit count, so a confident, fluent, well-formed summary masked the gap.

Domain: D5

Example: A synthesis step is redesigned to assert "results returned == units dispatched" and flag any discrepancy before the summary is shown to anyone.

## Human-in-the-Loop Checkpoint Placement

Q: How should a human-in-the-loop checkpoint be positioned in an agent or multi-agent workflow?

A: By the risk and reversibility of the action about to be taken — place a gate before any irreversible or high-stakes autonomous action; sample lower-stakes actions rather than gating every one.

Domain: D5

Example: An agent that can both draft a customer email (low stakes, sampled review) and issue a refund (high stakes, always gated) has different checkpoint density on each action type.

## Reference Architectures Defined

Q: What is a reference architecture, and how should it be used?

A: A documented, industry-proven way to wire an LLM application together for a recurring class of problem — a reference, not a rigid blueprint; adapt the shape that fits rather than implementing it as drawn.

Domain: D1

Example: An architect adapts the RAG reference architecture for a corpus with unusual document structure rather than copying a generic implementation verbatim.

## Five Named Reference Architectures

Q: Name the five reference architectures covered in this module.

A: Agent; Retrieval-augmented generation (RAG); Document processing pipeline (evaluator-optimizer); Customer-service/ticket triage (routing); Coding agent (agentic exploration with deterministic edit/test/review steps).

Domain: D1

Example: A support-ticket system that classifies then dispatches to different handling paths is an instance of the routing reference architecture.

## Composing Reference Architectures

Q: When is it right to compose two reference architectures instead of picking one?

A: Only when the two parts of the problem break in genuinely different ways worth managing separately — not because you haven't decided what problem you're solving, which is a deferred design decision, not a composition.

Domain: D1

Example: A routing workflow that hands certain intents off to an agentic investigation loop is a legitimate composition because ticket classification and open-ended investigation fail differently.

## Retrieval-vs-Tool-Call Mistake

Q: What is the most common reference-architecture mistake, and what are its symptoms?

A: Using retrieval where a tool call belongs. Symptoms: stale chunks, results shifting with each index refresh, answers contradicting the live database — a better embedding model or shorter refresh interval will NOT fix it.

Domain: D3

Example: A customer-service assistant answers "where's my order?" from two conflicting retrieved chunks (one saying shipped, one saying still processing) instead of calling the live order-status API.

## Retrieval Principle

Q: What is the core principle distinguishing when to use retrieval versus a tool call?

A: Retrieval is for stable knowledge: things true yesterday and true tomorrow. Tool use is for live state: things whose current value is owned by a system and changes independently of your index.

Domain: D3

Example: Product manual content is stable enough for retrieval; a customer's current account balance is live state and must be fetched via a tool call.

## RAG Chunking Approaches

Q: Name the three chunking approaches and when each earns its place.

A: Fixed-size (uniform spans + overlap; homogeneous unstructured text, simplest to operate); Semantic (split on meaning/topic boundaries; prose needing self-contained chunks); Hierarchical (preserve document structure; structured docs like contracts/manuals where section context carries meaning).

Domain: D3

Example: A 4,000-document corpus with section-numbered client contracts uses hierarchical chunking so a retrieved chunk keeps its section context.

## RAG Indexing Strategies

Q: Name the three indexing strategies and when each earns its place.

A: Dense/embeddings (semantic similarity; paraphrase/intent/concept matching); Sparse/keyword like BM25 (exact terms, identifiers, codes, names); Hybrid (both, merged; the common production case, recovers exact-match hits dense retrieval misses).

Domain: D3

Example: A corpus mixing "what does our methodology say about X" (concept) queries and "find the termination clause in the Acme contract" (exact-target) queries needs hybrid indexing to serve both patterns well.

## Reciprocal Rank Fusion

Q: What is reciprocal rank fusion, and why does it matter?

A: The standard, low-tuning way to merge two ranked lists (dense + sparse) into one score: each result is scored by its rank in each list, and the combined score favors items ranking well in both — combining dense and sparse is a design decision with a known, defensible default.

Domain: D3

Example: A hybrid retrieval system uses reciprocal rank fusion rather than an ad-hoc weighted average to merge its semantic and keyword search results.

## RAG Three-Way Trade-off

Q: What three things does every retrieval design trade off against each other?

A: Retrieval quality (does the right chunk come back?), Latency (how long retrieval adds per request), Maintenance (pipeline cost to keep correct as the corpus grows and changes).

Domain: D3

Example: An architect picks larger chunks and dense-only indexing to keep latency and maintenance low, explicitly accepting that some exact-match queries will be missed.

## Four Context-Related Terms

Q: Distinguish context window, retrieval, persistent application state, and summaries/memory layers.

A: Context window = the model's active attention space, resets between calls. Retrieval = fetched external knowledge, augments but doesn't replace the window. Persistent application state = owned by your system (order status, balances), requires a tool call. Summaries/memory = application-managed continuity; the model has no native memory between calls.

Domain: D2

Example: A support assistant's "remembered" preference from last week's chat only persists because the application explicitly stored and re-passed it — Claude itself has no native memory of that prior session.

## Model Selection Rule

Q: What is the default model tier, and when should you move up or down?

A: Start with Sonnet. Move up to Opus only when an eval set shows Sonnet isn't meeting the quality bar. Move down to Haiku only when an eval set confirms the quality tradeoff is acceptable.

Domain: D2

Example: A document-intelligence team tests Haiku against a 250-document eval set before switching from Sonnet, rather than switching first and checking quality later.

## Working-Memory Cliff

Q: Why is the context window called a "hard edge" or "cliff," and what's the practical implication?

A: Attention works fully inside the window and not at all outside it, an abrupt rather than gradual transition. Practical implication: don't budget the full window — budget for the largest realistic conversation plus retrieved context plus system prompt plus scratch plus growth margin.

Domain: D2

Example: A long-running coding agent that never budgets margin hits the ceiling mid-session at turn 30 with no warning, because the window filled silently.

## Context Strategy Spectrum

Q: What are the four context strategies on the monolithic-progressive spectrum?

A: Monolithic (load everything into one prompt; bounded/predictable tasks, but hits the cliff as context accumulates), Progressive (stage context, retrieve just-in-time, load only what's next needed), Retrieval/RAG (fetch relevant chunks at query time), Compaction (periodically summarize/compress accumulated context).

Domain: D2

Example: A long-running coding agent uses monolithic loading at session start, progressive state for recent tool calls, just-in-time retrieval when it needs an unloaded file, and compaction once early exploration has piled up.

## Extended Thinking Decision Rule

Q: When should you enable extended thinking, and why?

A: It's a cost/latency tradeoff, not a free quality boost — run evals without it first, and enable it only when accuracy still misses the bar after prompt work, justified by a measured accuracy gap.

Domain: D2

Example: A team runs their eval suite both with and without extended thinking and only ships it enabled because the measured accuracy gap justified the added latency and token cost.

## Gating a Model Swap

Q: What three things does an architect need at minimum before shipping a model swap?

A: A curated test set with known-good outputs covering the real work distribution; a grading function (model-graded or programmatic); a delta/rollback threshold set in advance, before running the eval.

Domain: D4

Example: A team sets "reject the migration if any single document type drops below 0.85" before running the Sonnet-vs-Haiku comparison, so the decision doesn't get renegotiated once the numbers come in.

## Sonnet-to-Haiku Downgrade Case

Q: What was the outcome of the Sonnet-to-Haiku migration case study, and why?

A: Full migration was rejected because two document types scored below the pre-set 0.85 rollback threshold; the salvage move routed those two types to Sonnet and the rest to Haiku, cutting cost materially with no regression on the hard types.

Domain: D4

Example: A partial-migration strategy like this is only possible because the eval set was stratified by document type rather than reported as one overall average score.

## Opus-Everywhere Failure

Q: What caused a 7x cost overrun and 2.3s median latency ninety days after launch?

A: Every call in the stack defaulted to Opus because no per-step model-tier decision was written into the architecture, and extended thinking was left on for a routing classifier that never needed reasoning.

Domain: D4

Example: A retroactive eval set let the team route the classifier to Haiku and mid-pipeline summarization to Sonnet, keeping Opus only where the eval justified it — cutting cost 71% with unchanged customer satisfaction.

## Opus-Everywhere Lesson

Q: Why is "not choosing a model" equivalent to "choosing the most expensive one"?

A: The absence of a deliberate model-tier decision is not neutral — the system defaults to the most capable (and most expensive) option, and an eval set is the only thing that makes the tier decision defensible during design, not just a post-hoc release gate.

Domain: D4

Example: An architecture document that never lists a model tier per step is implicitly an Opus-everywhere architecture document.

## Enterprise System-Prompt Structure

Q: What does an enterprise-grade system prompt need that a one-off chat prompt doesn't?

A: A clear role/scope statement, explicit constraints (what it must not do, what it must always do), and an output contract naming the response shape — because ambiguity in a reused prompt is a defect multiplied across every request.

Domain: D2

Example: A support-reply system prompt states explicitly it must never promise a refund or timeline the agent hasn't approved, as a structural output-contract constraint, not just a hoped-for instruction.

## Templates

Q: What is a template, and what's its design goal?

A: A system prompt with parameterized slots (per-request variable content) and fixed scaffolding around them. Design goal: the fixed scaffolding carries the consistency and safety guarantees, so filling a slot cannot accidentally remove a constraint.

Domain: D2

Example: A support-reply template lets an agent fill in the customer's name and issue while the never-promise-a-refund guardrail stays baked into the fixed scaffolding regardless of what's filled in.

## Underspecification

Q: What is underspecification, and why is it dangerous in a reused prompt?

A: A gap where the prompt is silent and the model improvises differently each time — exactly the non-determinism you don't want in a reused asset; an underspecified guardrail is worse than a missing one because it creates the appearance of control without the substance.

Domain: D2

Example: A prompt that says "keep responses professional" without naming a length limit or forbidden claims lets the model drift on both dimensions across requests.

## Prompt Technique Ladder

Q: What is the deliberate progression for choosing a prompting technique?

A: Start zero-shot (instruction only), add few-shot examples only if the task needs them, add chain-of-thought only if the task's structure demands it — each step adds tokens and latency.

Domain: D2

Example: A ticket classifier into five fixed categories stays zero-shot; a receipt-field extractor with wildly varying layouts gets few-shot examples; a multi-condition liability determination gets chain-of-thought.

## Avoiding Prompt Bias

Q: What three things can introduce invisible bias into a prompt?

A: Leading phrasing, unbalanced few-shot examples (showing only one kind of case), and assumptions baked into the instruction — bias is invisible in any single output and only shows up in aggregate.

Domain: D5

Example: A few-shot set for résumé screening that only shows examples of one demographic being flagged as "strong" quietly steers the model's judgment across many requests.

## Caching Mechanics

Q: What is the key ordering rule for prompt caching, and why?

A: Fixed content first, dynamic content last — the cache matches on a stable prefix, so putting per-request content ahead of the large fixed instruction block means the prefix changes every request and the cache never hits.

Domain: D2

Example: A team that put the document being analyzed at the top of the prompt (ahead of instructions) saw zero cache savings until they reordered fixed content first.

## Prompt Library vs Skill

Q: When should you use a modular prompt library instead of a Skill, and vice versa?

A: Prompt library: lightweight, engineer-owned, an assembled and often-tweaked prompt within one codebase/team. Skill: a stable procedure run the same way every time, distributed across teams/products, needing versioning, approval, and rollback.

Domain: D2

Example: A one-off internal analysis prompt tweaked per project stays a library fragment; a company-wide "weekly status report" procedure ships as a governed, versioned Skill.

## Three Sequential Consumption Decisions

Q: What are the three sequential decisions in choosing how a partner consumes Claude?

A: Which entry point fits the work → which build-time interface suits the team → which delivery route fits the partner's cloud commitments — made in that order.

Domain: D1

Example: A team first confirms branch staff need a web app (entry point), then that the API/SDK (not MCP) suits a single-product integration, then that Bedrock fits the bank's existing AWS agreement.

## API vs SDK

Q: What's the difference between the API and the SDK, and when do you drop to raw HTTP?

A: The same entry point from Claude's perspective — the SDK is an opinionated wrapper adding language-native types and handling streaming/tool-use boilerplate. Drop to raw HTTP only when a freshly shipped API feature hasn't reached the SDK yet.

Domain: D3

Example: A Python engineering team defaults to the Python SDK for a new integration rather than hand-rolling raw HTTP calls.

## MCP vs API Tool Use

Q: When do you choose MCP over direct API tool use?

A: Pick MCP when one tool entry point needs to be reachable from multiple Claude clients; pick raw API tool use when the tools live inside one product only — they're different layers, not alternatives.

Domain: D3

Example: A customer database exposed only to one internal support app doesn't need MCP; the same database reused by three different Claude-powered products would justify an MCP server.

## Claude Agent SDK

Q: What is the Claude Agent SDK, and how is it different from the "Anthropic SDK"?

A: The Agent SDK is the managed runtime that runs the agent loop (the same one powering Claude Code) — the model picks a tool, runs it, sees the result, and keeps going until done or a stop condition fires. The "Anthropic SDK" is a convenience wrapper over the API with no agent loop.

Domain: D3

Example: A partner embedding multi-turn autonomous tool use inside their own product reaches for the Agent SDK, not just the general-purpose Anthropic SDK.

## Claude Code Shaping vs Governing Layers

Q: What are the two groups of Claude Code customization layers?

A: Shaping layers (what the agent knows and does): CLAUDE.md, Skills, subagents, MCP. Governing layers (what the agent is allowed to touch): Hooks, permission boundaries, approval flows, sandboxing, restricted execution.

Domain: D7

Example: A team adds a CLAUDE.md describing project conventions (shaping) and a Hook that blocks writes outside the repo (governing) as two independent, composable layers.

## CSP Delivery Route Decision Rule

Q: What determines the right CSP delivery route, and what's the trade-off?

A: The partner's existing cloud contract, identity system, and procurement — not technical capability, since the model behaves identically on every route. Trade-off: CSP-mediated routes (Bedrock/Vertex/Foundry) tend to lag the first-party API on new features by weeks or longer.

Domain: D3

Example: A GCP-committed partner routes through Vertex AI even knowing a brand-new feature shipped on the direct API weeks earlier and hasn't reached Vertex yet.

## Regulated-Industry Constraints Eliminate First

Q: How should governance constraints (HIPAA, GDPR, FedRAMP, privilege, residency) factor into entry-point selection?

A: They rule entry points in or out BEFORE cost, ergonomics, or build effort enter the conversation — Claude.ai (consumer-grade) is hit most often since it wasn't built to satisfy every enterprise data-handling requirement out of the box.

Domain: D5

Example: A law firm bound by attorney-client privilege rules out Claude.ai immediately and routes through the direct API/SDK behind its own approved gateway instead.

## Claude Code Misused Failure

Q: What were the three failure mechanisms in the regional bank's Claude-Code-on-branch-laptops proposal?

A: (1) The entry point was chosen before the user was named (branch staff don't run terminals). (2) MCP was carried forward as a default with no reusability need (no other Claude clients existed in the bank). (3) Compliance, the highest-consequence path, was assigned to subagents, the weakest deterministic guarantee — inverting the pattern.

Domain: D5

Example: The corrected architecture used a custom SSO-authenticated web app calling the API directly, with compliance enforced in deterministic server-side code instead of subagents.

## Entry-Point Tradeoff Naming

Q: What makes an entry-point recommendation defensible in a review?

A: Being able to name the tradeoff out loud at the time you make it (audience, integration depth, governance/control, latency, etc.) — that same named tradeoff is what tells you later when to switch.

Domain: D6

Example: "We chose Bedrock because the deciding tradeoff is integration depth: the bank already runs on AWS and needs core-banking data access" is a defensible, checkable recommendation.

## Recap Takeaway: Decomposition First

Q: Per the module recap, why must decomposition happen before pattern selection?

A: Designs that skip decomposition end up forcing Claude into work another system would do at lower cost, or ask it to operate without context a human would have given a colleague.

Domain: D1

Example: A team that jumps straight to "let's build an agent" without first deciding what Claude, systems, and humans each own risks over-assigning work to Claude by default.

## Recap Takeaway: Pattern = Autonomy Choice

Q: Per the module recap, what is choosing a pattern really a choice about?

A: How much autonomy to grant Claude — when error cost is the binding constraint among the five factors, error cost picks the pattern; the tightest constraint decides.

Domain: D1

Example: Even if latency and cost budgets would allow an agent, a high error-cost scenario (audit exposure, legal risk) rules it out first.

## Recap Takeaway: Reference Architectures Before Invention

Q: Per the module recap, what should an architect do before inventing a novel architecture?

A: Reach for the tested reference architectures (Agent, RAG, Document processing/evaluator-optimizer, Routing, Coding agent) first, since other teams have already learned what breaks in each — and the most common mistake to avoid is using retrieval as a substitute for live state.

Domain: D1

Example: A ticket-triage system is built on the routing reference architecture rather than a bespoke design, because routing's failure modes are already well documented.

## Recap Takeaway: Model Swap = Release

Q: Per the module recap, how should a model tier change be treated?

A: As a release, gated by an eval set that defines "better" and a rollback criterion set before the swap, not after — the same principle applies to context strategy, where progressive context holds up better over a long-lived deployment than monolithic context.

Domain: D4

Example: A team refuses to ship a Sonnet-to-Haiku swap until the pre-set eval thresholds are met, exactly as they would gate a code deployment.

## Recap Takeaway: Entry Point By Work, Not Shelf

Q: Per the module recap, how should you choose an entry point?

A: By the work it has to do, not by what's already on the shelf — Claude.ai, the direct API, the SDK, Claude Code, and MCP each carry a different core tradeoff, and naming that tradeoff out loud is what tells you later when to switch.

Domain: D6

Example: A team resists reusing Claude Code on a new non-engineering project just because the last project used it, and instead re-derives the entry-point choice from the new audience and work.
