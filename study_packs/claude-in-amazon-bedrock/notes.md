# Claude with Amazon Bedrock

- Source URL: https://anthropic-partners.skilljar.com/claude-in-amazon-bedrock/241929
- Capture date: 2026-07-05
- Completion date: 2026-07-05
- Completion status: Complete under repo video-scope rule. Video-only lessons without readable text/transcripts were recorded as out of scope.
- Study pack: `study_packs/claude-in-amazon-bedrock/`

## Capture Status

This course was reviewed through browser automation and authenticated HTTP fetches. Lesson pages with readable lesson-description text were transformed into the notes below.

Per the repo rule added on 2026-07-05, video-only lessons do not count toward course-capture completeness when no readable body text, transcript, captions text, or other text equivalent is available. Empty administrative/wrap-up pages with no exam-relevant content also do not block completion. The following visible pages were recorded as video-only or no-content/out of scope:

| Section | Lesson | Capture Note |
|---|---|---|
| Working with the API | Chat bot exercise | Video-only page; no readable lesson text or transcript available. |
| Working with the API | System prompt exercise | Video-processing/error page; no readable lesson text or transcript available. |
| Working with the API | Structured data exercise | Video-processing/error page; no readable lesson text or transcript available. |
| Prompt evaluations | Exercise on prompt evals | Video-processing/error page; no readable lesson text or transcript available. |
| Prompt engineering | Exercise on prompting | Video-processing/error page; no readable lesson text or transcript available. |
| Features of Claude | Prompt caching in action | Video-processing/error page; no readable lesson text or transcript available. |
| Agents | Agents overview | Video-processing/error page; no readable lesson text or transcript available. |
| Agents | Claude Code setup | Video-processing/error page; no readable lesson text or transcript available. |
| Wrap up | Course wrap up | Empty/near-empty page content; no exam-relevant readable content. |

Quiz and final-assessment pages were reviewed for placement/topic only. Raw quiz questions and answers were intentionally not archived.

## Captured Sections

| Section | Captured Evidence |
|---|---|
| Course introduction | Introduction and model-family overview captured, including model-selection tradeoffs and multi-model application design. |
| Working with the API | Bedrock request flow, model IDs and regional availability, inference profiles, message structure, multi-turn context, system prompts, temperature, streaming, output control, and structured data captured. Video-only exercises recorded as out of scope. |
| Prompt evaluations | Eval concepts, workflow, test dataset generation, running evals, model-based grading, and code-based grading captured. Video-only exercise recorded as out of scope. |
| Prompt engineering | Clear/direct prompting, specificity, XML structure, and examples captured. Video-only exercise recorded as out of scope. |
| Tool use | Tool-use workflow, tool functions, JSON schemas, response handling, tool execution, tool results, multi-turn tool loops, multiple tools, batch tool use, structured data with tools, flexible extraction, and text editor tool captured. |
| Retrieval Augmented Generation | RAG motivation, chunking, embeddings, full RAG flow, implementation, BM25, multi-search retrieval, reranking, and contextual retrieval captured. |
| Features of Claude | Extended thinking, image/PDF support, citations, and prompt caching concepts/rules captured. Video-only prompt-caching demo recorded as out of scope. |
| Model Context Protocol | MCP introduction, clients, project setup, tools, inspector, client implementation, resources, accessing resources, prompts, prompt access, and primitive review captured. |
| Agents | Claude Code in action, MCP server enhancements, parallelizing Claude Code, automated debugging, computer use, computer-use mechanics, and qualities of agents captured. Video-only overview/setup lessons recorded as out of scope. |
| Final assessment | Final-assessment page reviewed for placement only; raw questions/answers not captured. |
| Wrap up | Page was visible but had no meaningful readable body text; recorded as out of scope. |

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| Domain 1: Agentic Architecture & Orchestration | Medium | Tool loops, stop reasons, multi-step agent behavior, Claude Code as an agentic workflow, parallel Claude Code instances, observe-then-act patterns, focused tool sets, and continuous evaluation. Missing Agent SDK-specific hooks, Task subagents, and deeper coordinator/subagent mechanics. |
| Domain 2: Tool Design & MCP Integration | High | Tool descriptions, JSON schema, tool_choice, tool result handling, multiple tools, batch tool use, structured output through tools, text editor tool, MCP clients, servers, tools, resources, prompts, and inspector workflow. |
| Domain 3: Claude Code Configuration & Workflows | Medium | `/init`, `CLAUDE.md`, planning-first workflow, TDD workflow, MCP server integration, git worktrees for parallel Claude Code, and automated debugging. The course does not fully cover path-specific rules, slash commands, or CI flags. |
| Domain 4: Prompt Engineering & Structured Output | High | Clear/direct prompting, specificity, XML tags, examples, prompt evals, datasets, model/code/human graders, prefilled assistant messages, stop sequences, and tool-based structured output. |
| Domain 5: Context Management & Reliability | Medium | Application-managed conversation history, relevant-field context, RAG chunking/retrieval, citations, prompt caching, extended thinking tradeoffs, source grounding, and evaluation feedback loops. Missing deeper escalation, structured error propagation, confidence calibration, and human review workflows. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| Bedrock request flow | A user message travels from the UI to the application server, then to Bedrock Runtime, then to Claude, and the application renders Claude's response. For exam purposes, the important idea is application-owned orchestration, not AWS setup trivia. |
| Model selection | Choose the smallest/fastest/cheapest model that satisfies the task. Use faster models for latency-sensitive or high-volume interactions, balanced models for most application logic, and higher-capability models for complex reasoning where cost and latency are justified. |
| Multi-model architecture | A single application can route subtasks to different model tiers: fast handling for simple front-door interactions, balanced models for core logic, and stronger reasoning models for hard cases. |
| Model IDs and regions | Bedrock model IDs and regional availability matter operationally, but specific cloud-provider configuration is out of scope for the certification. Treat this as deployment context, not a memorization target. |
| Inference profiles | The course uses Bedrock inference profiles to reduce region/model friction. For the exam, the transferable lesson is to make model selection explicit and avoid brittle deployment assumptions. |
| App-managed conversation state | Claude and Bedrock do not preserve chat history for the application. The application must resend the relevant prior user/assistant/tool messages for multi-turn coherence. |
| Role alternation | Conversation histories need clean user/assistant role structure. Bad message ordering creates confusing context and can break request validity. |
| System prompts | Use system prompts for durable behavior, role, boundaries, style, and policy. Do not rely on repeated user-message instructions for core application behavior. |
| Temperature | Low temperature favors repeatability for extraction, grading, and production workflows. Higher temperature is more useful for ideation, but it does not replace validation. |
| Streaming | Streaming improves perceived latency by returning partial output as it is generated. It does not improve correctness, schema validity, or reliability by itself. |
| Prefill and stop sequences | Prefilled assistant messages can steer the start of output; stop sequences can halt generation at known boundaries. These are useful controls but weaker than schema/tool enforcement for machine-consumed output. |
| Structured data without tools | Prefill plus stop sequences can reduce extra prose around JSON or code. Use it for simple cases; validate outputs before downstream use. |
| Prompt evaluation | Prompt engineering improves the prompt; prompt evaluation measures whether the prompt works. Reliable systems need test cases, graders, and repeated iteration. |
| Evaluation datasets | Build representative test cases with inputs, expected properties, and scoring criteria. Avoid only testing happy paths. |
| Model-based grading | Use a model grader for semantic quality, reasoning, completeness, and judgment-heavy criteria. Calibrate it with examples and spot checks. |
| Code-based grading | Use deterministic code checks for syntax, parseability, JSON validity, regex validity, field presence, and exact format constraints. |
| Clear/direct prompting | Lead with the task. Vague or indirect first lines force Claude to infer the goal and reduce consistency. |
| Specific prompting | Add quality criteria, process steps, constraints, and examples when output quality depends on judgment or format. |
| XML tags | Tags create clear boundaries between instructions, examples, context, and output requirements. They are especially useful when prompts include large interpolated content. |
| Few-shot examples | Examples teach both output format and ambiguous-case judgment. Pull examples from evaluation failures when possible. |
| Tool use | Tools let Claude request external information or actions. The application defines tools, Claude decides when to call them, the application executes them, and the result is returned for the next model turn. |
| Tool functions | Tool implementations should be narrow, predictable, and clearly described. The course's reminder example decomposes current-time lookup, date arithmetic, and reminder creation into separate functions. |
| JSON schemas for tools | The schema tells Claude what arguments are valid. Names, descriptions, field descriptions, enums, required/optional fields, and examples all affect tool selection and correctness. |
| tool_choice | `auto` lets Claude decide whether to call a tool, `any` requires a tool call, and forced selection requires a specific tool. Use forced selection for required first steps or tests. |
| stop_reason | In a tool-enabled loop, inspect whether Claude stopped for tool use or final text. Continue the loop for tool use and terminate on a final answer. |
| Tool results | Add Claude's tool request and the application's tool result to conversation history so Claude can reason from the new evidence. |
| Multiple tools | Scoped, well-described tools reduce ambiguity. Too many overlapping tools make selection less reliable. |
| Batch tool use | A batch tool can encourage parallel work for independent operations, but it should not hide dependencies or replace normal tool-loop control. |
| Structured data with tools | Tool-based extraction is more reliable than asking for JSON in text because the requested structure is the tool input schema. Still validate semantic correctness. |
| Flexible extraction schema | A generic `to_json`-style tool reduces schema-writing overhead but is weaker than a purpose-built schema for strict production extraction. |
| Text editor tool | The built-in text editor tool maps to file inspection and edit operations. Exam-relevant transfer: choose specialized edit/read tools by task shape and preserve context before modifying files. |
| RAG | RAG retrieves only relevant source chunks instead of stuffing whole documents into the prompt. It trades simpler prompting for pipeline complexity and retrieval-quality risk. |
| Chunking | Chunk by size, overlap, or document structure. Good chunks preserve semantic coherence; bad chunks retrieve misleading context. |
| Embeddings | Embeddings support semantic search by comparing meaning, not exact words. They are useful but can miss identifiers, codes, and exact terms. |
| BM25 | BM25 lexical search is strong for exact words, IDs, incident numbers, filenames, and policy terms. Pair it with embeddings for hybrid retrieval. |
| Multi-search RAG | A retriever can merge vector and lexical results, then use reciprocal rank fusion or similar ranking logic to combine strengths. |
| Reranking | Claude can rerank retrieved chunks for relevance, but this adds latency/cost. Use it when first-pass retrieval returns plausible but poorly ordered results. |
| Contextual retrieval | Add short document-level context to chunks before indexing so isolated chunks carry enough meaning when retrieved later. |
| Citations | Citations support trust and source checking. For exam scenarios, preserve claim-source mappings rather than producing unsupported synthesis. |
| Prompt caching | Prompt caching helps when large, stable prompt prefixes repeat within the cache window. It is not a general reliability mechanism. |
| Extended thinking | Extended thinking can improve hard reasoning, but it costs more and adds latency. Use it selectively for complex tasks. |
| MCP | MCP separates integration responsibilities: clients connect, servers expose capabilities, tools let Claude act, resources expose context, and prompts provide reusable instructions. |
| MCP tools | Tools are model-controlled. Use them when Claude should decide to take an action or call a capability. |
| MCP resources | Resources are app-controlled context endpoints. Use them for read-only data catalogs or documents that the application chooses to include. |
| MCP prompts | Prompts are user-controlled reusable templates. Use them for tested workflows that users can invoke intentionally. |
| MCP inspector | The inspector is for testing server tools/resources/prompts before connecting them to a real client workflow. |
| Claude Code `/init` | `/init` scans a project and writes durable project context into `CLAUDE.md`. Project-level context can be shared; local context should stay personal. |
| Planning-first workflow | Ask Claude Code to inspect, plan, and test before risky edits. This maps to the exam's plan-mode judgment even though the course uses practical Claude Code language. |
| TDD workflow | Give Claude a failing test target, let it implement, run tests, and iterate on failures. This is stronger than vague "make it work" prompting. |
| Claude Code with MCP | MCP servers extend Claude Code with team-specific tools, resources, and prompts. Configure servers intentionally and test them before relying on them. |
| Parallel Claude Code | Use separate git worktrees for concurrent Claude Code instances so parallel work does not collide in the same files. Merge only after reviewing diffs and test results. |
| Automated debugging | Claude can inspect production errors and propose or apply fixes, but this needs guardrails, tests, review, and deployment controls. |
| Computer use | The course covers computer use, but the exam guide marks computer use and vision/image analysis as out of scope. Keep only the transferable tool-loop idea. |
| Agent qualities | Effective agents observe the environment before acting, use focused tool sets, loop through tool calls, operate with sufficient context, target high-value/low-error-cost work, and are continuously evaluated. |

## Decision Rules

- If a task is latency-sensitive and simple, prefer a faster/lower-cost model; if it requires deep reasoning, pay for more capability only where it changes outcomes.
- If a chat must remember prior turns, persist and resend the relevant conversation history; do not assume the provider stores state.
- If behavior should be durable across turns, use a system prompt or application guardrail rather than repeating hidden requirements in user messages.
- If output feeds a machine, prefer tool-based structured output or schemas plus validators over prose instructions.
- If output format is the only issue and risk is low, prefill plus stop sequences can be enough; for production extraction, use schema/tool enforcement.
- If correctness can be checked deterministically, use code-based grading; if correctness is semantic, use model-based grading with calibration.
- If retrieval misses exact identifiers, add lexical/BM25 search instead of relying on embeddings alone.
- If retrieved chunks are right but poorly ordered, consider reranking; if chunks lack enough context, consider contextual retrieval.
- If an MCP capability performs an action, model it as a tool; if it exposes context for the app to include, model it as a resource; if it is a reusable user-invoked instruction, model it as a prompt.
- If multiple Claude Code instances need to work in parallel, isolate them with git worktrees and merge deliberately.
- If an agent can affect production or user data, add deterministic guardrails, tests, review, and escalation paths.

## Anti-Patterns

- Treating Skilljar checkmarks or browser progress as evidence that the repo study pack is complete.
- Treating video-only pages as captured text; they should be recorded as out of scope unless a readable transcript/text equivalent is available.
- Over-studying AWS-specific setup, credentials, billing, or regional configuration for an exam that marks specific cloud-provider configuration out of scope.
- Assuming Claude/Bedrock stores messages between calls.
- Using low temperature as a substitute for validation.
- Relying on "return JSON" without schema, prefill/stop controls, tool use, or deterministic parsing.
- Giving Claude many overlapping tools with vague descriptions.
- Ignoring `stop_reason` and parsing assistant prose to decide whether a tool loop is complete.
- Running retrieval with embeddings only when questions involve exact IDs or policy terms.
- Collapsing cited source material into an unsupported summary.
- Connecting MCP servers to Claude Code before testing primitives in the inspector.
- Running multiple Claude Code agents in one working tree and hoping file edits do not conflict.
- Treating computer use details as exam focus; the exam guide explicitly excludes computer use.

## Scenario Traps

- Trap: "The course title says Bedrock, so memorize AWS configuration." Better: capture provider integration context, but prioritize API/tool/RAG/MCP/agent tradeoffs that overlap the exam guide.
- Trap: "The UI says the course was clicked through, so it is documented." Better: documentation requires transformed notes, flashcards, practice questions, and resolved blockers.
- Trap: "A structured-looking JSON answer is production-ready." Better: parse, validate, retry with feedback where appropriate, and route uncertain cases to review.
- Trap: "Long context is easier than RAG." Better: whole-document prompting can be simple, but retrieval is often better for targeted questions over large corpora.
- Trap: "Semantic search is enough because it understands meaning." Better: exact IDs and names often require lexical search.
- Trap: "MCP tools, resources, and prompts are interchangeable." Better: tools are model-controlled actions, resources are app-controlled context, prompts are user-controlled templates.
- Trap: "More tools make an agent more capable." Better: focused tool sets improve selection reliability.
- Trap: "Parallel Claude Code means multiple agents in one checkout." Better: isolate workspaces with git worktrees and merge after review.
- Trap: "Extended thinking always improves production UX." Better: it may help hard reasoning but adds latency and cost.
- Trap: "Computer use examples should become exam notes." Better: preserve only the general tool-loop lesson because computer use is out of scope.

## Memorization Cues

- Model choice: speed, cost, intelligence.
- Bedrock state: the app owns history.
- System prompt: durable behavior, not transient facts.
- Temperature: repeatability knob, not correctness guarantee.
- Streaming: UX latency, not validation.
- Structured output ladder: prompt controls, schema/tool use, semantic validation.
- Eval trio: dataset, grader, iteration.
- Grader split: model for meaning, code for exactness.
- Tool loop: request, `tool_use`, execute, `tool_result`, repeat.
- Tool descriptions: name, purpose, inputs, outputs, boundaries.
- RAG: chunk, embed/index, retrieve, rerank/ground, cite.
- Hybrid search: embeddings for meaning, BM25 for exact terms.
- MCP: tools act, resources inform, prompts guide.
- Claude Code: `/init`, plan, test, edit, verify.
- Parallel Claude Code: worktree first, merge later.
- Agent quality: observe, act, evaluate.

## Source References

- Course introduction: "Introduction to the course"; "Overview of Claude Models".
- Working with the API: "Accessing the API"; "Making a request"; "Multi-Turn conversations"; "System prompts"; "Temperature"; "Streaming"; "Controlling model output"; "Structured data".
- Prompt evaluations: "Prompt evaluation"; "A typical eval workflow"; "Generating test datasets"; "Running the eval"; "Model based grading"; "Code based grading".
- Prompt engineering: "Prompt engineering"; "Being clear and direct"; "Being specific"; "Structure with XML tags"; "Providing examples".
- Tool use: "Introducing tool use"; "Tool functions"; "JSON Schema for tools"; "Handling tool use responses"; "Running tool functions"; "Sending tool results"; "Multi-Turn conversations with tools"; "Adding multiple tools"; "Batch tool use"; "Structured data with tools"; "Flexible tool extraction"; "The text editor tool".
- Retrieval Augmented Generation: "Introducing Retrieval Augmented Generation"; "Text chunking strategies"; "Text embeddings"; "The full RAG flow"; "Implementing the RAG flow"; "BM25 lexical search"; "A multi-search RAG pipeline"; "Reranking results"; "Contextual retrieval".
- Features of Claude: "Extended thinking"; "Image support"; "PDF support"; "Citations"; "Prompt caching"; "Rules of prompt caching".
- Model Context Protocol: "Introducing MCP"; "MCP clients"; "Project setup"; "Defining tools with MCP"; "The server inspector"; "Implementing a client"; "Defining resources"; "Accessing resources"; "Defining prompts"; "Prompts in the client"; "MCP review".
- Agents: "Claude Code in action"; "Enhancements with MCP servers"; "Parallelizing Claude Code"; "Automated debugging"; "Computer Use"; "How Computer Use works"; "Qualities of agents".

## Gaps / Follow-Up

- Video-only lessons were not documented by repo rule; optional transcripts could enrich this pack later but are not required for completion.
- This course adds strong API/tool/RAG/MCP/prompt-eval coverage but still does not close Agent SDK hooks, Task-based subagent spawning, structured MCP error responses, Claude Code CI flags, Message Batches API, or confidence calibration gaps.
