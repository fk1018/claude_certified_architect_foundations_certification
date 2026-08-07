# Claude with Google Cloud's Vertex AI

- Source URL: https://anthropic-partners.skilljar.com/claude-with-google-vertex/289145
- Capture date: 2026-07-05
- Completion date: 2026-07-05
- Completion status: Complete under repo video-scope rule. Video-only lessons without readable lesson body, transcript, captions text, or other text equivalent were recorded as out of scope.
- Study pack: `study_packs/claude-with-google-vertex/`

## Capture Status

This course was reviewed through browser automation in the authenticated Skilljar session. The sidebar showed 93 visible pages across course sections. The only substantive readable instructional body found during the sweep was the modular `Vertex AI Setup` lesson. The rest of the instructional pages were video-player pages with no readable body text, transcript, or captions text exposed in the page during inspection.

Per the repo rule, video-only pages do not block course completion when no readable text equivalent is available. Quiz, survey, final-assessment, and wrap-up pages were reviewed for placement/topic only; raw quiz questions and answers were intentionally not archived.

## Captured Sections

| Section | Captured Evidence |
|---|---|
| Introduction | `Welcome to the course` was visible as a video-only page; recorded as out of scope for text capture. |
| Anthropic overview | `Overview of Claude models` was visible as video-only course structure; use as outline-backed model-selection context. |
| Accessing Claude with the API | `Vertex AI Setup` readable text captured. Video-only pages covered API access, requests, multi-turn conversations, chat exercise, system prompts, temperature, streaming, output control, structured data, and exercises. Survey and API quiz placement reviewed only. |
| Prompt evaluation | Visible video-only outline covered prompt evaluation, eval workflow, test datasets, running evals, model-based grading, code-based grading, exercise, and quiz placement. |
| Prompt engineering techniques | Visible video-only outline covered prompt engineering, clear/direct prompting, specificity, XML tags, examples, exercise, and quiz placement. |
| Tool use with Claude | Visible video-only outline covered tool use, project overview, tool functions, tool schemas, message blocks, tool results, multi-turn tool loops, multiple tools, batch tool, structured data tools, text edit tool, web search tool, and quiz placement. |
| Retrieval Augmented Generation | Visible video-only outline covered RAG, chunking, embeddings, full flow, implementation, BM25, multi-index RAG, reranking, contextual retrieval, and quiz placement. |
| Features of Claude | Visible video-only outline covered extended thinking, image/PDF support, citations, prompt caching, prompt caching rules, prompt caching in action, and quiz placement. |
| Model Context Protocol | Visible video-only outline covered MCP introduction, clients, project setup, tools, server inspector, client implementation, resources, resource access, prompts, client prompts, review, and quiz placement. |
| Anthropic apps - Claude Code and computer use | Visible video-only outline covered Anthropic apps, Claude Code setup/action, MCP server enhancements, parallel Claude Code, automated debugging, computer use, and computer-use mechanics. Computer use is out of exam scope except as general tool-loop context. |
| Agents and workflows | Visible video-only outline covered agents/workflows, parallelization, chaining, routing, agents and tools, environment inspection, workflows vs agents, and quiz placement. |
| Final assessment | Final assessment page reviewed for placement only; raw questions/answers were not captured. |
| Wrapping up! | `Course Wrap Up` was visible as video-only content; recorded as out of scope for text capture. |

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| Domain 1: Agentic Architecture & Orchestration | Medium | Outline-backed coverage of tool loops, multi-turn tool conversations, agents and workflows, parallelization, chaining, routing, agents and tools, environment inspection, and workflows-vs-agents tradeoffs. Does not close Agent SDK hooks, Task subagents, or session forking gaps. |
| Domain 2: Tool Design & MCP Integration | High | Outline-backed coverage of tool functions, schemas, message blocks, tool results, multiple tools, batch tool, text edit/web search tools, MCP clients/tools/resources/prompts, and server inspector. Does not add structured MCP error-response details. |
| Domain 3: Claude Code Configuration & Workflows | Medium | Outline-backed coverage of Claude Code setup/action, MCP server enhancements, parallel Claude Code, automated debugging, and environment inspection. Does not add slash commands, path rules, or CI flags. |
| Domain 4: Prompt Engineering & Structured Output | High | Outline-backed coverage of system prompts, temperature, streaming, output control, structured data, prompt evals, model/code grading, clear/direct prompting, specificity, XML tags, examples, and tool-backed structured data. |
| Domain 5: Context Management & Reliability | Medium | Outline-backed coverage of multi-turn conversations, RAG, chunking, embeddings, BM25, reranking, contextual retrieval, citations, prompt caching, environment inspection, and evaluation loops. Does not close escalation, error propagation, or confidence-calibration gaps. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| Vertex as provider context | The course is framed around calling Claude through Google Cloud Vertex AI. For the certification, keep provider setup as deployment context and focus on transferable Claude architecture, tools, prompts, context, and reliability patterns. |
| Enabling Anthropic models in Vertex | The readable setup lesson directs learners to Vertex AI Model Garden, search for Anthropic, choose the intended model, and enable it if needed. Exam relevance: ensure the deployment environment exposes the model before debugging application logic. |
| `gcloud` authentication | The setup lesson uses `gcloud init`, `gcloud auth login`, project selection, and application-default login so the SDK can use local credentials. Exam relevance: credentials and provider setup are prerequisites, not reliability guarantees. |
| Application-owned API orchestration | A Vertex-hosted Claude call still relies on the application to send messages, manage history, inspect tool-use responses, execute tools, return results, validate outputs, and handle errors. |
| Model selection | Choose the smallest, fastest, lowest-cost model that meets the task's quality bar. Escalate capability for complex reasoning, high ambiguity, or high-value decisions. |
| Multi-turn state | Claude does not magically know prior turns unless the application supplies relevant conversation history. Preserve critical user/assistant/tool messages and trim irrelevant context. |
| System prompts | Use system prompts for durable behavior, role, policy, boundaries, and response requirements. Do not bury transient case facts or business state in the system prompt. |
| Temperature | Lower temperature improves repeatability but does not prove correctness. Use validation, tests, schemas, and review for production reliability. |
| Streaming | Streaming improves perceived latency. It does not solve correctness, schema validity, or tool-loop control. |
| Output control | Prefill and stop sequences can shape low-risk text output, but schema/tool enforcement and validators are stronger for machine-consumed data. |
| Structured data | For extraction or downstream automation, prefer JSON-schema-backed tool use or structured APIs plus semantic validation over plain "return JSON" prompting. |
| Prompt evaluation | Evaluate prompts against representative examples, criteria, and graders. Iterate before scaling to production workloads. |
| Model-based grading | Use a model grader for semantic quality, completeness, and judgment-heavy criteria. Calibrate with examples and human spot checks. |
| Code-based grading | Use deterministic code checks for syntax, parseability, schema validity, exact fields, regexes, arithmetic, and other objective rules. |
| Clear/direct prompting | Put the task and success criteria up front. Ambiguous prompts force Claude to infer intent and reduce consistency. |
| Specific prompting | Add constraints, acceptance criteria, examples, and edge cases when quality depends on judgment. |
| XML tags | Use tags to separate instructions, examples, context, and output requirements when prompts contain multiple information types. |
| Few-shot examples | Examples teach format and ambiguous-case judgment. Prefer examples taken from eval failures. |
| Tool use loop | Claude requests a tool call, the application executes it, returns a tool result, and calls Claude again until the model produces the final answer. |
| Message blocks | Tool-enabled APIs return structured content blocks. Applications must inspect block types instead of assuming every assistant response is final text. |
| Tool schemas | Tool names, descriptions, input schemas, field descriptions, required fields, enums, and examples all influence whether Claude selects and fills tools correctly. |
| Multiple tools | Focused tools with clear boundaries beat many overlapping tools. More tools can reduce reliability if descriptions and responsibilities blur. |
| Batch tool | Batch tools can help independent work happen together, but they should not hide dependencies or remove normal loop/error handling. |
| Text edit and web search tools | Specialized tools should be chosen by task shape. Editing tools need context and review; search tools need source evaluation and provenance. |
| RAG | Retrieval augmented generation retrieves relevant chunks instead of stuffing entire corpora into prompts. It improves grounding only when retrieval quality is good. |
| Chunking | Chunks should preserve semantic coherence and enough context to answer questions. Bad chunking creates misleading partial evidence. |
| Embeddings | Embeddings support semantic similarity, but they can miss exact identifiers, filenames, policy codes, and unusual terms. |
| BM25 and hybrid search | BM25 is strong for exact words and identifiers. Combine lexical and vector retrieval when both exact and semantic matching matter. |
| Reranking | Reranking can improve result order at additional latency/cost. Use it when first-pass retrieval finds plausible but poorly ordered chunks. |
| Contextual retrieval | Add short document-level context to chunks before indexing so retrieved chunks carry meaning outside their original location. |
| Citations | Citations and claim-source mappings support verification and uncertainty handling. Do not collapse sourced material into unsupported synthesis. |
| Prompt caching | Caching helps when large stable prompt prefixes repeat. It is a cost/latency optimization, not a correctness mechanism. |
| MCP | MCP separates clients, servers, tools, resources, and prompts. Tools are model-controlled actions; resources are app-controlled context; prompts are reusable user-invoked workflows. |
| MCP inspector | Test MCP primitives in the inspector before relying on them in Claude Code or agent workflows. |
| Claude Code setup/action | Claude Code workflows benefit from durable project context, planning before risky edits, tests, and review. Exact setup mechanics still need deeper study from Claude Code-focused material. |
| Parallel Claude Code | Use separate worktrees for parallel Claude Code sessions so independent work does not collide in one checkout. |
| Automated debugging | Claude can inspect logs and propose fixes, but production debugging needs tests, guardrails, review, and deployment controls. |
| Workflows vs agents | Use fixed workflows when the path is predictable. Use agents when the model must inspect state, choose tools, and adapt across turns. |
| Parallelization, chaining, routing | Parallelize independent subtasks, chain dependent steps, and route by task type or complexity. |
| Computer use | The course includes computer use, but the exam guide marks computer use and vision/image analysis as out of scope. Preserve only the general observe-act-tool-loop lesson. |

## Decision Rules

- If a failure occurs before the first model call on Vertex, check model access, project selection, and credentials before changing prompts.
- If a scenario asks for exam-relevant architecture, do not answer with cloud-provider setup unless the problem is explicitly access/authentication.
- If the system must remember prior turns, store and resend relevant history; do not assume Vertex or Claude stores application state.
- If output feeds software, choose tool/schema-based structured output and validation over prose formatting instructions.
- If a prompt fails on subjective quality, build representative evals and use model-based grading with calibration.
- If a format or field rule is deterministic, use code-based grading or validators rather than a model judge.
- If a tool must always run before a risky action, enforce the sequence programmatically; prompt instructions alone are weaker.
- If similar tools are confused, improve names/descriptions and clarify input/output boundaries before adding a routing layer.
- If retrieval misses exact values, add lexical/BM25 or hybrid search rather than increasing prompt length.
- If retrieved chunks lack context, improve chunking/contextual retrieval before blaming Claude.
- If users need trust in generated claims, preserve citations and claim-source mappings through synthesis.
- If work is predictable, use a workflow; if it requires environment inspection and dynamic tool choice, use an agent with guardrails.
- If Claude Code sessions run in parallel, isolate them with worktrees and merge after reviewing diffs and tests.

## Anti-Patterns

- Treating Skilljar progress state as documentation evidence. Repo completion depends on transformed study artifacts.
- Over-studying Vertex console clicks, billing, or exact provider mechanics for an exam that excludes specific cloud-provider configuration.
- Assuming `gcloud` authentication or model enablement improves prompt reliability.
- Relying on "return JSON" without schemas, validators, retries, or review.
- Using low temperature as a substitute for correctness checks.
- Treating streaming as a reliability feature instead of a UX latency feature.
- Giving Claude many overlapping tools with vague descriptions.
- Ignoring structured message blocks and parsing only assistant text.
- Using embeddings alone for exact IDs, filenames, or policy terms.
- Summarizing retrieved evidence without preserving provenance.
- Connecting MCP servers before testing tools/resources/prompts.
- Running multiple Claude Code agents in one working tree.
- Treating computer use details as exam content.

## Scenario Traps

- Trap: "The course title says Vertex, so memorize Google Cloud setup." Better: know setup as context, but study transferable Claude API, tool, RAG, MCP, prompt, and agent tradeoffs.
- Trap: "The user clicked through Skilljar, so the course is documented." Better: documentation requires notes, flashcards, practice questions, tracker updates, and progress-file updates.
- Trap: "Authentication succeeded, so the app is reliable." Better: credentials only unlock access; reliability comes from context management, validation, evals, guardrails, and error handling.
- Trap: "Streaming is the right fix for slow or wrong structured output." Better: streaming helps users see tokens sooner; schemas and validation handle structure.
- Trap: "More tools improve an agent." Better: scoped, clearly described tools reduce selection errors.
- Trap: "A model judge can grade everything." Better: deterministic checks should be code-based.
- Trap: "RAG means embeddings." Better: exact lookup often needs BM25 or hybrid retrieval.
- Trap: "MCP resources and tools are interchangeable." Better: resources expose context; tools perform model-selected actions.
- Trap: "Agents are always better than workflows." Better: workflows are simpler and more reliable when the path is known.

## Memorization Cues

- Vertex setup: model enabled, project selected, credentials available.
- Provider setup is access, not architecture.
- State lives in the app.
- Temperature repeats; validation verifies.
- Streaming is UX, not correctness.
- Structured output ladder: prompt controls, schema/tool use, validators/retries.
- Eval loop: dataset, grader, iteration.
- Grader split: model for meaning, code for exactness.
- Tool loop: request, `tool_use`, execute, `tool_result`, repeat.
- Tool design: name, purpose, inputs, outputs, boundaries.
- RAG: chunk, index, retrieve, rerank, cite.
- Hybrid search: BM25 exact, embeddings semantic.
- MCP: tools act, resources inform, prompts guide.
- Claude Code: context, plan, test, edit, verify.
- Workflow trio: parallelize, chain, route.
- Agent choice: dynamic inspection and tool choice.

## Source References

- Readable lesson reviewed: `Vertex AI Setup`.
- Visible course title: `Claude with Google Cloud's Vertex AI`.
- Visible section outline: Introduction; Anthropic overview; Accessing Claude with the API; Prompt evaluation; Prompt engineering techniques; Tool use with Claude; Retrieval Augmented Generation; Features of Claude; Model Context Protocol; Anthropic apps - Claude Code and computer use; Agents and workflows; Final assessment; Wrapping up.
- `Vertex AI Setup`: provider access path, Anthropic model enablement in Vertex, `gcloud` installation/authentication, project selection, and application-default credentials.
- Video-only lesson titles captured for topic provenance only; no raw transcript or captions text was available during inspection.
- Quiz, survey, and final-assessment pages were reviewed only for placement/topic; raw questions and answers were not archived.

## Gaps / Follow-Up

- Video lessons were not documented by transcript because no readable transcript/captions text was available; optional transcripts could enrich this pack later.
- This course reinforces API/tool/RAG/MCP/prompt-eval/Claude Code/workflow coverage but still does not close Agent SDK hooks, Task-based subagent spawning, structured MCP errors, Claude Code CI flags, Message Batches API, or confidence calibration.
