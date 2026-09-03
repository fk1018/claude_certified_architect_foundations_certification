# MSO Foundations

- Source URL: https://anthropic-partners.skilljar.com/path/claude-certified-developer-foundations
- Completed: 2026-09-03
- Study pack: `study_packs_developer_foundations/mso-foundations/`

## Captured Sections

- Orientation: module goals and educational-content disclaimer
- How LLMs Behave: Tokens, Context Window, Sampling, Non-determinism
- Models & Reasoning: The Model Family, Reasoning Modes, How They Work Together
- Prompting Modes: The Three Modes, Cost & Quality Trade-off, Mode & Model Choice
- Technical Substrate: SDK vs. REST, Sync/Streaming/Real-time, Async for High-Volume Work
- Module Quiz (4 questions on sampling, model vs. reasoning mode, shot-prompting cost, batch fit)
- Exercise: Predict the Behavior (4 scenarios on temperature, shot-prompting, batch pipelines, context-window failure)
- Recap: Five Takeaways
- Module Complete (path overview: M1 this module, M2 Production-Grade Prompting/Agents/Tool-use, M3 Claude Code/MCP/Integration, M4 Production Engineering/Evals/Security, M5 Accelerators and IP Contribution)

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| D1: Agents and Workflows | None | Module does not touch agent loops, harnesses, hooks, subagents, or memory. The "agentic work" phrase appears only when describing Fable's capability tier, not agent construction. |
| D2: Applications and Integration | Medium | Covers REST mechanics (endpoint, API key, JSON body/response), SDK as a convenience layer over REST (Python/TypeScript), synchronous vs. streaming (SSE) vs. async (AsyncAnthropic, Promise-based TS client) vs. Message Batches API. Does not cover tools, vision, thinking-block handling, prompt caching mechanics, or CLAUDE.md/settings.json configuration. |
| D3: Claude Code | None | Not mentioned in this module; Claude Code / MCP is flagged as Module 3 content. |
| D4: Eval, Testing, and Debugging | Low | Introduces why non-determinism breaks exact-text assertions and gestures at evals/model-graded judges as the fix, but does not teach trace analysis, error-type identification, or recovery strategies. Full eval-building is deferred to Module 3. |
| D5: Model Selection and Optimization | High | This is the module's core: tokens as the unit of cost/budget, context window as a fixed budget with two failure modes, sampling and temperature, non-determinism, the four-tier model family (Fable/Opus/Sonnet/Haiku) and tier-selection heuristic, reasoning mode (adaptive thinking, effort setting, deprecated budget_tokens) as separate from model choice, zero/one/multi-shot prompting and its cost-quality trade-off, SDK vs. REST, sync/streaming/async/batch request shapes. |
| D6: Prompt and Context Engineering | Medium | Covers context-window budget mechanics and the discipline of trimming/summarizing history, plus shot-prompting as a lever for output structure. Does not cover drift/bloat prevention techniques, input sanitization, or structured-output validation in depth (deferred to Module 2). |
| D7: Security and Safety | None | Not addressed in this module. |
| D8: Tools and MCPs | None | Not addressed in this module; tool schemas are explicitly deferred to Module 2. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| Tokens | The unit Claude reads, prices, and budgets in — not characters or words. Chars-per-token ratio is model-dependent and varies by tokenizer/generation; do not memorize a fixed ratio. Everything counted: prompt, conversation history, tool definitions, tool results, and the response itself. |
| Context window | A fixed total-token budget per request holding system prompt + full conversation + injected documents + tool results + output. Two distinct failure modes: (1) input already exceeds the window → rejected with a validation error before generation starts; (2) input fits but generation reaches the ceiling mid-stream → model stops and returns partial output with stop_reason `model_context_window_exceeded` (no error raised). Managing a long session (trimming/summarizing history) is the application's responsibility, not automatic. |
| Sampling | The model produces a probability distribution over next tokens at each step and samples from it rather than always picking one fixed token. Temperature reshapes that distribution: lower = concentrated on most-likely tokens (more repeatable), higher = spread out (more varied). |
| Sampling parameter support is model-dependent | The newest Claude models reject non-default temperature/top_p/top_k with a 400 error; behavior on those models is steered through prompting instead. Even where temperature is accepted, temperature 0 increases repeatability but does not guarantee identical output across calls. Confirm current support in the API reference at build time. |
| Non-determinism | Direct consequence of sampling: identical inputs do not guarantee identical outputs. Breaks exact-text test assertions. Correct testing strategy: assert on properties that must hold (field present, value in range, structure parses) rather than exact wording; use a model-graded judge (an eval) when meaning must be judged. |
| The Claude model family (four tiers) | Fable (most capable tier — hardest reasoning/coding/agentic work), Opus (demanding work above Sonnet's envelope), Sonnet (balanced default for most production workloads), Haiku (speed/cost efficiency within its capability envelope). Practical default: start with Sonnet; move up a tier only when an eval shows the current tier missing the quality bar; move down to Haiku only when an eval shows the quality drop is acceptable. Confirm current lineup/identifiers at platform.claude.com/docs since the family evolves. |
| Reasoning mode vs. model choice | Two separate, composable decisions. Model choice picks the family member; reasoning mode (adaptive thinking) is configured per call. On current models, the model decides when/how much to think, tuned via an effort setting (the older fixed `budget_tokens` control is deprecated and returns a 400 error on the newest generations). Thinking content is omitted from responses by default on the newest models — request a summarized display to see it. Reasoning is worth its cost on hard multi-step problems; wasted on lookups/classification. Per-model thinking defaults differ (some newest models think adaptively by default or always) — confirm at build time. |
| Zero-shot / one-shot / multi-shot | Distinct from prompt wording — this is about how many worked examples you give inside the prompt. Zero-shot: instruction only, no examples. One-shot: one input/output example. Multi-shot (a.k.a. few-shot): several examples. Examples are not training data; they live in the prompt and show the exact output shape a description alone often fails to pin down. |
| Shot-prompting cost/quality trade-off | Each example costs tokens on every call and consumes context budget. Use zero-shot when the task is simple and output shape is obvious. Move to one/multi-shot when output needs a specific structure, casing, or edge-case handling that description text keeps missing. General discipline: add the smallest amount of prompt that produces a reliable result. |
| Mode choice interacts with model choice | A more capable model often succeeds zero-shot where a smaller model needs examples to match structure — so adding examples can let a cheaper model do the job. Try the simplest model + fewest examples that meet your eval; add capability or examples only where the eval shows you need them. |
| SDK vs. raw REST | Claude is reached over an HTTP REST API at its core: request to an endpoint with an API key and JSON body, JSON response back — callable with any HTTP client. The official SDK (Python, TypeScript, others) is a thin convenience layer over the same REST API, handling auth, request construction, retries, and response parsing. SDK and raw REST reach the identical API and model; the SDK just reduces boilerplate. |
| Synchronous requests | Send the request, wait for the complete response as one piece, then act. Fine for short responses and backend jobs with no one watching. |
| Streaming | Sends the response in pieces as the model generates it, over the same HTTP connection using server-sent events (SSE). Used when a response is long or a user is watching; output appears immediately instead of after a blank-screen wait. The application must reassemble pieces into the final message. |
| Async patterns for concurrency | Two Python/TypeScript SDK patterns for not blocking the application thread while a request is in flight: Python's `AsyncAnthropic` client (non-blocking async/await); TypeScript's standard client is already Promise-based (no separate async client class needed). The request still returns in real time — this is about concurrency, not bulk throughput. |
| Message Batches API | Separate pattern for bulk offline workloads: submit a large set of requests in one call, receive an identifier, poll for completion. Can take up to 24 hours, at a lower per-token cost in exchange for latency. Fits offline pipelines, evaluation runs, and bulk jobs where no user waits per-result and cost matters more than turnaround time. |

## Decision Rules

- If a test needs to assert correctness of a Claude response, assert on structural/value properties (field present, value in range, structure parses), not exact text — use a model-graded eval when meaning must be judged.
- If output quality is below the bar, first ask whether an eval shows it, then move up a model tier — do not upgrade the model on intuition alone. Same logic in reverse for downgrading to Haiku.
- If a task is a hard multi-step reasoning/coding/agentic problem, consider enabling reasoning (adaptive thinking) with a higher effort setting; if it's a lookup or classification task, leave reasoning off — its cost is wasted there.
- If a prompt keeps missing a specific output structure, casing, or edge case despite clear instructions, add one or two worked examples (one-shot/multi-shot) before writing more instruction text.
- If the task is simple with an obvious output shape, stay zero-shot to avoid the added token cost of examples on every call.
- If processing thousands of inputs offline with no user waiting and cost matters more than latency, use the Message Batches API rather than a synchronous loop.
- If a user is actively watching a long-running response, use streaming (SSE) rather than synchronous so output appears incrementally.
- If the application needs to issue many concurrent requests without blocking the app thread (not bulk offline), use the async/await pattern (`AsyncAnthropic` in Python, the Promise-based client in TypeScript) rather than the Batches API.
- If a long multi-turn session keeps growing, proactively trim or summarize conversation history before each call — the context window does not manage this automatically, and letting it run unmanaged risks a `model_context_window_exceeded` stop reason or an outright rejected request.
- If deciding whether to call raw REST or use the SDK, default to the SDK for less boilerplate (auth, retries, parsing) — reach for raw REST only when you need something the SDK does not expose, since both hit the same API and model.

## Anti-Patterns

- Asserting exact response text in an automated test — sampling makes wording non-deterministic even when the answer is correct.
- Assuming temperature 0 guarantees identical output across calls — it increases repeatability but is not a determinism guarantee.
- Treating model choice and reasoning mode as one setting — they are independent, composable levers (model picks the family member; thinking is a per-call toggle/effort setting).
- Setting a fixed `budget_tokens` for reasoning depth on the newest model generations — that control is deprecated and returns a 400 error; effort settings replace it.
- Adding examples (multi-shot) reflexively for every task regardless of need — each example costs tokens on every call; use the minimum needed to hit the quality bar.
- Assuming a chars-per-token ratio is fixed across models — it's tokenizer- and generation-dependent.
- Using a synchronous loop to process a large offline batch of documents — this hits rate limits and ties up the application; use the Batches API instead.
- Assuming the context window silently drops old turns to make room — instead, an oversized input is rejected before generation, or a mid-generation ceiling hit returns truncated output with a specific stop reason. Nothing auto-manages history for you.
- Assuming streaming speeds up bulk offline processing — streaming exists for perceived responsiveness to a waiting user, not throughput or cost.
- Confusing SDK capability with API capability — the SDK is a convenience wrapper; it does not expose anything the REST API doesn't already have.

## Scenario Traps

- Trap: "Two identical prompts must return identical text." Better: the model samples each next token from a probability distribution, so wording can vary even when both answers are correct — this is expected non-determinism, not a bug.
- Trap: "Extended thinking is a different model." Better: model choice (which family member runs) and reasoning mode (adaptive thinking, on/off, effort level) are separate settings that compose.
- Trap: "A short, well-specified classification task returns the right zero-shot answer, so add three examples to be safe." Better: for a task already succeeding zero-shot, added examples mostly add token cost on every call for little or no gain — add examples only where an eval shows a real gap.
- Trap: "Process thousands of offline inputs with a bigger context window or a synchronous loop." Better: this is the Batches API's exact use case — submit once, poll, accept added latency for lower per-token cost.
- Trap: "A long-running agent session's context window auto-expands to fit growing history." Better: the window is a fixed budget; an oversized input errors before generation, and a mid-generation ceiling hit returns truncated output with `model_context_window_exceeded` — the app must trim/summarize history itself.
- Trap: "Temperature only affects response length." Better: temperature reshapes the probability distribution over next tokens, affecting wording variety (and, at extremes, even which label a classifier returns), not length.
- Trap: "A high-temperature run is more accurate because it considers more of the correct answers." Better: higher temperature spreads probability mass and increases variability; it does not improve correctness, and for a classifier you generally want the low-temperature, repeatable behavior.
- Trap: "Streaming helps a pipeline process documents faster." Better: streaming exists to reduce perceived latency for a watching user over one connection; it does not help an unattended bulk pipeline, where Batches is the right shape.

## Memorization Cues

- Four tiers, one sentence: Fable = most capable (hardest work), Opus = above Sonnet's envelope, Sonnet = balanced default, Haiku = speed/cost within its envelope.
- Two levers, always separate: model choice (which tier) + reasoning mode (thinking on/off, effort level) — never conflate them.
- Two context-window failure modes: too big up front → rejected before generation; hits ceiling mid-generation → truncated output + `model_context_window_exceeded` stop reason.
- Shot-prompting ladder: zero-shot (no examples) → one-shot (one example) → multi-shot/few-shot (several examples); each rung costs more tokens per call.
- Four request shapes: synchronous (wait, one piece), streaming (SSE, pieces as generated), async/await (concurrency, still real-time), batch (bulk offline, poll, up to 24h, cheaper per token).
- Non-determinism testing rule: assert properties (present/in-range/parses), not exact text; use a model-graded eval for meaning.
- SDK = REST + convenience (auth, retries, parsing) — same API, same model, less boilerplate.

## Source References

- Orientation: module learning objectives and the educational-content disclaimer (adapt to your situation; verify against Anthropic docs; illustrative/fictitious examples).
- How LLMs Behave (Teaching, 12 min): Tokens, Context Window, Sampling, Non-determinism tabs.
- Models & Reasoning (Teaching, 10 min): The Model Family, Reasoning Modes, How They Work Together tabs.
- Prompting Modes (Teaching, 8 min): The Three Modes, Cost & Quality Trade-off, Mode & Model Choice tabs.
- Technical Substrate (Teaching, 12 min): SDK vs. REST, Sync/Streaming/Real-time, Async for High-Volume Work tabs.
- Module Quiz (5 min): 4 multiple-choice questions covering non-determinism, model-vs-reasoning-mode, shot-prompting cost, and batch fit for offline bulk work.
- Exercise: Predict the Behavior (6 min): 4 scenarios covering temperature effects on classification, multi-shot fixing structure problems, batch fit for a 50,000-document overnight pipeline, and context-window symptoms/failure modes in a long agent session.
- Recap: Five Takeaways — tokens as budget/pricing unit; context window as fixed budget with two failure modes; sampling causes non-determinism (evals as the fix); model choice and reasoning mode as separate composable levers; REST+SDK as the transport with sync/streaming/async/batch chosen by wait-state and workload shape.
- Sources cited by the module: Claude 101 (Skilljar), Building with the Claude API (Skilljar), AI Fluency: Framework & Foundations (Skilljar), platform.claude.com/docs.
- Module Complete: path map — M1 (this module) → M2 Production-Grade Prompting, Agents & Tool-use → M3 Claude Code, MCP & Integration → M4 Production Engineering, Evals, and Security → M5 Accelerators and IP Contribution.

## Gaps / Follow-Up

- Study extended thinking mechanics in depth: enabling it via the API, handling returned thinking blocks, and summarized-display behavior (deferred explicitly to Module 2).
- Study tool schemas, tool use/function calling, and structured output enforcement (deferred to Module 2; not touched in this module at all).
- Study context engineering techniques beyond "trim or summarize" (drift/bloat prevention, structured context management) — deferred to Module 2.
- Study full eval-building methodology beyond the property-assertion heuristic introduced here (deferred to Module 3).
- Study Claude Code, permission modes, and MCP integration — entirely out of scope for this module (Module 3 territory).
- Study production security boundaries, credential/key management, and safety guardrails — entirely out of scope for this module (Module 4 territory).
- Study prompt caching mechanics and vision/multimodal input handling — not mentioned in this module; confirm coverage in Module 2 or later.
- Confirm current model identifiers, sampling-parameter support per model, and thinking defaults at platform.claude.com/docs before exam day, since the module repeatedly flags these as evolving and build-time-verifiable rather than fixed facts.
