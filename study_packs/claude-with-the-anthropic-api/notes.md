# Building with the Claude API

- Source URL: https://anthropic-partners.skilljar.com/claude-with-the-anthropic-api/287818
- Documented: 2026-07-05
- Study pack: `study_packs/claude-with-the-anthropic-api/`
- Capture status: Complete under user-defined scope. Video lesson contents do not count for this course per explicit user instruction on 2026-07-05. Captured evidence is the visible course outline, the readable non-video "Getting an API key" lesson, quiz/final-assessment completion metadata, and exam-guide alignment.

## Captured Sections

| Section | Captured Evidence |
|---|---|
| Introduction | Outline captured. "Welcome to the course" displayed a video player; videos were out of scope. |
| Anthropic overview | Outline captured: "Overview of Claude models". Video content out of scope. |
| Accessing Claude with the API | Outline captured: API access, API keys, requests, multi-turn conversations, system prompts, temperature, streaming, structured data, quiz. "Getting an API key" readable lesson reviewed. |
| Prompt evaluation | Outline captured: eval workflow, test datasets, running evals, model-based grading, code-based grading, exercise, quiz. Video content out of scope. |
| Prompt engineering techniques | Outline captured: clear/direct prompting, specificity, XML tags, examples, exercise, quiz. Video content out of scope. |
| Tool use with Claude | Outline captured: tool functions, schemas, message blocks, tool results, multi-turn tool loops, multiple tools, fine-grained tool calling, text edit tool, web search tool, quiz. Video content out of scope. |
| RAG and Agentic Search | Outline captured: RAG, chunking, embeddings, full RAG flow, BM25 lexical search, multi-index RAG. Video content out of scope. |
| Features of Claude | Outline captured: extended thinking, image/PDF support, citations, prompt caching, code execution, Files API, quiz. Video content out of scope. |
| Model Context Protocol | Outline captured: MCP introduction, clients, project setup, tools, server inspector, client implementation, resources, prompts, review, quiz. Video content out of scope. |
| Anthropic apps - Claude Code and computer use | Outline captured: Anthropic apps, Claude Code setup/action, MCP server enhancements. Video content out of scope. |
| Agents and workflows | Outline captured: agents, parallelization, chaining, routing, agents and tools, environment inspection, workflows vs agents, quiz. Video content out of scope. |
| Final assessment | Completion metadata captured: passed, 23 of 23 correct. Quiz answers were not expanded or archived. |
| Wrapping up! | Outline captured: course wrap-up. Video content out of scope. |

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| Domain 1: Agentic Architecture & Orchestration | Medium | Course outline directly names agents, workflows, parallelization, chaining, routing, agents and tools, environment inspection, and workflows vs agents. Use this as outline-backed coverage, not full Agent SDK implementation detail. |
| Domain 2: Tool Design & MCP Integration | High | Outline covers Claude tool use, tool functions, tool schemas, message blocks, tool results, multiple tools, text edit/web search tools, MCP tools, resources, prompts, clients, and server inspector. Structured error-response content still needs another source. |
| Domain 3: Claude Code Configuration & Workflows | Medium | Outline includes Claude Code setup, Claude Code in action, and MCP server enhancements. It does not cover `CLAUDE.md`, slash command, path rule, or CI details. |
| Domain 4: Prompt Engineering & Structured Output | High | Outline covers system prompts, temperature, streaming, structured data, prompt evaluation, test datasets, model/code grading, clear/direct prompting, specificity, XML tags, examples, and structured-data exercises. Batch and multi-pass review need another source. |
| Domain 5: Context Management & Reliability | Medium | Outline covers multi-turn conversations, RAG, chunking, embeddings, citations, prompt caching, PDF/image support, code execution, Files API, and evals. Escalation and error propagation need another source. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| API key lifecycle | The readable lesson shows the practical path: use the Anthropic API Console, create a key, name it for identification, copy it when shown, and regenerate if lost. Treat keys as secrets, not as durable course notes or committed config. |
| Messages API request shape | The course outline implies a progression from API access to making requests, multi-turn conversations, system prompts, temperature, streaming, and structured data. For the exam, think in terms of request parameters, conversation history, stop reasons, and downstream validation. |
| Multi-turn state | Multi-turn API work is application-managed. The app must preserve relevant user/assistant/tool messages so Claude can reason over prior turns; missing or overstuffed context creates reliability problems. |
| System prompts | System prompts establish durable behavior, role, policy, and output expectations. They should not be used as a dumping ground for transient user facts. |
| Temperature | Lower temperature is favored for deterministic extraction, grading, and production workflows. Higher temperature can help brainstorming, but is weaker when repeatability and validation matter. |
| Streaming | Streaming improves perceived latency and user experience, but it is not a substitute for validation, schema enforcement, or error handling. |
| Structured data | For machine-consumed output, the exam favors JSON schemas and tool use over "please return JSON" prompting alone. Structured output still needs semantic validation. |
| Prompt evaluation | Eval work should start with representative examples, run repeatable tests, compare against criteria, and iterate prompts before scaling to production traffic. |
| Model-based grading | Use a model judge when quality is subjective, semantic, or hard to encode deterministically. Calibrate it with examples and human review. |
| Code-based grading | Use deterministic code checks for exact format, schema, arithmetic, field presence, and other rules that should not depend on model judgment. |
| Tool use loop | Claude can request a tool call, the application executes it, then returns a tool result for the next model turn. This maps directly to the exam's agentic loop lifecycle. |
| Tool schemas | Tool schemas define expected inputs. Clear descriptions, boundaries, enums, required/optional fields, and examples improve tool selection and reduce invalid calls. |
| Message blocks | Tool use returns mixed content blocks, not only conversational text. Applications must inspect block types and handle `tool_use` and `tool_result` correctly. |
| Multiple tools | Tool access should be scoped. Giving a model too many overlapping tools increases selection ambiguity; use specific tools and descriptions. |
| Text edit and web search tools | Built-in/specialized tools should be selected by task shape: edit tools for targeted changes, search tools for fresh or external information. |
| RAG flow | Retrieval augmented generation usually involves preparing content, chunking, embedding or indexing, retrieving relevant material, and grounding the answer in retrieved evidence. |
| BM25 and embeddings | Lexical search is strong for exact terms and identifiers; embedding search is strong for semantic similarity. Multi-index RAG can combine both. |
| Citations and provenance | Citations are not decoration. For exam scenarios, preserve claim-source mappings and conflicts rather than collapsing them into unsupported synthesis. |
| Prompt caching | Caching is useful when large stable prompt prefixes repeat across calls. It is not useful for highly variable prefixes or content placed in the wrong order. |
| MCP | MCP organizes external capabilities into clients, servers, tools, resources, and prompts. Resources expose context catalogs; tools perform actions. |
| MCP inspector | The server inspector is a development/debugging tool for validating server behavior before relying on it in Claude or agent workflows. |
| Claude Code and MCP servers | Claude Code can be extended with MCP servers, but server scope, secrets, tool descriptions, and team vs personal configuration matter. |
| Workflows vs agents | Workflows are more controlled and predictable when the path is known. Agents are more adaptive when the model must inspect state and choose the next step. |
| Parallelization, chaining, routing | Use parallelization for independent work, chaining for dependent sequential steps, and routing when task type determines the next specialist or path. |

## Decision Rules

- If output will feed a parser or downstream system, prefer tool use with a JSON schema plus validation over prose instructions.
- If the answer must be consistent across production cases, lower temperature and add deterministic checks.
- If the user is waiting in an interactive flow, use synchronous API calls or streaming; do not choose batch-style processing for blocking interactions.
- If a workflow needs exact pass/fail rules, use code-based grading. If quality is semantic or subjective, use model-based grading with calibration examples.
- If several tools overlap, split or rename them so each has a clear purpose, input boundary, and output contract.
- If a tool result is needed before the next decision, return the tool result to the conversation history and let Claude choose the next step.
- If a prompt keeps producing false positives, add concrete criteria and few-shot examples before relying on vague "be conservative" instructions.
- If RAG misses exact identifiers, add lexical search or hybrid retrieval rather than relying only on embeddings.
- If source attribution matters, require structured claim-source mappings before synthesis.
- If a task has a known sequence, use a workflow. If the task requires state-dependent decisions, use an agentic loop with guardrails.
- If MCP data is contextual and read-only, consider resources. If the model must take an action, define a tool.
- If a key is lost or exposed, delete/regenerate it rather than trying to recover or reuse it.

## Anti-Patterns

- Treating Skilljar completion checkmarks as evidence that the repo has documented the course.
- Committing API keys, screenshots of keys, copied secrets, or raw credential setup artifacts.
- Relying on "return valid JSON" without schema-enforced structure and validation.
- Letting every agent access every tool because it seems more flexible.
- Using generic tool names like `analyze_content` for unrelated actions that require different inputs and recovery behavior.
- Ignoring `tool_use` blocks and reading only final text.
- Using model-based grading for things a deterministic validator can check exactly.
- Using embeddings alone when exact terms, IDs, filenames, or policy codes matter.
- Summarizing sourced material without preserving citations or conflict metadata.
- Choosing an agent when a fixed workflow would be simpler, cheaper, and easier to test.
- Treating prompt caching as automatic optimization without checking stable-prefix placement.
- Omitting the scope note that video lessons were defined as out of scope for this course.

## Scenario Traps

- Trap: "The course is clicked through, so it is documented." Better: repo completion depends on captured and transformed study artifacts.
- Trap: "A low temperature guarantees correctness." Better: it improves repeatability but does not replace schemas, validators, retries, or review.
- Trap: "Streaming makes an API workflow more reliable." Better: streaming improves responsiveness; reliability comes from validation and error handling.
- Trap: "Structured output is solved by asking for JSON." Better: use tool use/JSON schema and validate semantics.
- Trap: "The synthesis agent can cite sources from memory." Better: subagents must preserve structured source metadata into synthesis.
- Trap: "The same search index handles every retrieval case." Better: combine lexical and semantic retrieval when exact and conceptual matching both matter.
- Trap: "MCP resources and MCP tools are interchangeable." Better: resources expose context; tools perform operations.
- Trap: "An agent is always more powerful than a workflow." Better: choose workflows for predictable paths and agents for adaptive decisions.
- Trap: "Tool choice improves when every capability is available." Better: scoped tool sets reduce ambiguity and misuse.
- Trap: "Video sections can be silently omitted with no note." Better: record that videos were explicitly out of scope for this course.

## Memorization Cues

- API key: create, name, copy once, protect, rotate.
- Tool loop: request, inspect `tool_use`, execute, return `tool_result`, repeat.
- Structured output: schema first, then semantic validation.
- Eval pair: model judge for meaning; code judge for exactness.
- Tool design: name, purpose, inputs, outputs, boundaries, examples.
- RAG: chunk, index, retrieve, ground, cite.
- Search pairing: BM25 = exact terms; embeddings = semantic similarity.
- MCP: clients call servers; servers expose tools, resources, prompts.
- Workflow trio: parallelize independent work, chain dependent work, route by task type.
- Scope rule: for this course, videos do not count by explicit user instruction.

## Source References

- Visible course title: "Building with the Claude API".
- Readable lesson reviewed: "Getting an API key" under "Accessing Claude with the API".
- Completion metadata reviewed: course survey, section quizzes, and final assessment showed completion/pass metadata only.
- Full outline captured for these sections: Introduction; Anthropic overview; Accessing Claude with the API; Prompt evaluation; Prompt engineering techniques; Tool use with Claude; RAG and Agentic Search; Features of Claude; Model Context Protocol; Anthropic apps - Claude Code and computer use; Agents and workflows; Final assessment; Wrapping up.
- Video lessons were explicitly defined as out of scope by user instruction. English caption tracks were visible in the player during inspection, but they were not needed for the scoped completion.

## Gaps / Follow-Up

- If deeper source fidelity is needed later, review the video lessons or captions as an optional enrichment pass.
- Expand coverage of exact API request examples, tool-call block handling, MCP implementation details, RAG implementation details, and Claude Code setup from another source if exam gaps remain.
- Validate quiz answers only if needed for final completion; current notes do not archive or reproduce quiz questions.
