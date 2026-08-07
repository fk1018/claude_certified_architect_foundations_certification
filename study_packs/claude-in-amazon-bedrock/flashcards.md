# Claude with Amazon Bedrock Flashcards

## Capture Status

Q: What is the capture limitation for this course?

A: Several visible exercise/setup/wrap-up pages were video-only or empty; by repo rule they are recorded as out of scope, not blockers.

## Capture Status

Q: Should this course be moved from todo to done now?

A: Yes. Under the video-scope rule, readable non-video sections were captured and video-only sections were recorded as out of scope.

## Exam Scope

Q: How should AWS-specific Bedrock setup details be treated for the certification?

A: As context only; the exam guide marks specific cloud provider configurations out of scope.

## Model Selection

Q: What three tradeoffs drive Claude model selection in the course?

A: Intelligence, speed/latency, and cost.

## Model Selection

Q: When should a stronger, slower, more expensive model be selected?

A: When the task requires deeper reasoning and the outcome justifies the added latency and cost.

## Model Selection

Q: Why might one application use multiple model tiers?

A: Different subtasks can optimize for speed, cost, or reasoning depth independently.

## Bedrock API

Q: Who manages conversation history in a Bedrock/Claude chat app?

A: The application manages and resends the relevant message history.

## Bedrock API

Q: What happens if a follow-up request omits prior conversation context?

A: Claude treats it as an independent call and may miss prior facts or intent.

## Bedrock API

Q: What operational issue can model IDs and regions create?

A: A model may not be available in the selected region, causing brittle deployment behavior.

## System Prompts

Q: What belongs in a system prompt?

A: Durable role, behavior, boundaries, policy, style, and output expectations.

## System Prompts

Q: Why not put core behavior only in repeated user instructions?

A: It is repetitive, user-visible, and weaker than durable system-level configuration.

## Temperature

Q: When should temperature generally be low?

A: For extraction, grading, production workflows, and repeatable behavior.

## Temperature

Q: Does low temperature guarantee correctness?

A: No. It improves repeatability but still needs validation and review.

## Streaming

Q: What problem does streaming solve?

A: It improves perceived latency by returning output incrementally.

## Streaming

Q: What problem does streaming not solve?

A: It does not enforce schema, correctness, or semantic validation.

## Output Control

Q: What can prefilled assistant messages do?

A: Steer the beginning and shape of Claude's response.

## Output Control

Q: What do stop sequences do?

A: Stop generation at predefined boundaries.

## Structured Data

Q: When are prefill and stop sequences useful for structured output?

A: For lower-risk cases where raw JSON/code needs less surrounding prose.

## Structured Data

Q: What is stronger than asking Claude to return JSON?

A: Tool-based structured output with a schema plus validation.

## Structured Data

Q: Why can schema-valid output still need validation?

A: It can contain semantic errors, unsupported values, or wrong field assignments.

## Prompt Evaluation

Q: What is the difference between prompt engineering and prompt evaluation?

A: Engineering improves prompts; evaluation measures whether they work.

## Prompt Evaluation

Q: What are the core pieces of an eval workflow?

A: Prompt, evaluation dataset, model output, grader, and iteration.

## Prompt Evaluation

Q: When is a code-based grader best?

A: When correctness can be checked deterministically, such as syntax, JSON validity, or required fields.

## Prompt Evaluation

Q: When is a model-based grader useful?

A: When evaluation requires semantic or qualitative judgment.

## Prompt Evaluation

Q: Why should eval datasets include edge cases?

A: Happy-path tests hide failures that appear in production.

## Prompt Engineering

Q: What is the first prompt-engineering improvement for vague output?

A: Lead with a clear, direct statement of the task.

## Prompt Engineering

Q: What should specificity add to a prompt?

A: Criteria, constraints, process steps, and desired output properties.

## Prompt Engineering

Q: Why use XML tags in prompts?

A: They separate instructions, examples, context, and output sections clearly.

## Prompt Engineering

Q: What do few-shot examples teach?

A: Output format and judgment for ambiguous cases.

## Prompt Engineering

Q: Where can good few-shot examples come from?

A: Evaluation failures and representative edge cases.

## Tool Use

Q: What is the basic tool-use loop?

A: Send tools, inspect `tool_use`, execute the tool, return `tool_result`, and continue.

## Tool Use

Q: Why should applications inspect `stop_reason`?

A: It tells whether Claude is requesting tools or producing a final answer.

## Tool Use

Q: Why must tool results be added to conversation history?

A: Claude needs the results in context to reason about the next step.

## Tool Design

Q: What makes a tool description effective?

A: Clear purpose, inputs, outputs, boundaries, and when to use it versus similar tools.

## Tool Design

Q: Why should tools be narrow and scoped?

A: Focused tools reduce selection ambiguity and misuse.

## Tool Schema

Q: What does a JSON schema tell Claude?

A: The tool arguments, required fields, allowed structure, and field meanings.

## Tool Choice

Q: What does `tool_choice: auto` mean?

A: Claude may call a tool or answer directly.

## Tool Choice

Q: What does `tool_choice: any` mean?

A: Claude must call a tool but can choose which one.

## Tool Choice

Q: When should forced tool choice be used?

A: When a specific tool must run first or when testing a required tool path.

## Batch Tools

Q: When is batch tool use appropriate?

A: When multiple independent operations can be executed in parallel.

## Batch Tools

Q: What is the risk of batching dependent operations?

A: It hides ordering requirements and can produce incorrect workflow behavior.

## Structured Data With Tools

Q: Why is tool-based extraction more reliable than text JSON?

A: Claude fills structured tool inputs instead of free-form prose.

## Flexible Extraction

Q: What is the tradeoff of a generic `to_json` extraction tool?

A: Less schema work, but weaker guarantees than a purpose-built schema.

## Text Editor Tool

Q: What is the transferable exam lesson from the Bedrock text editor tool?

A: Pick specialized read/edit tools by task shape and inspect context before modifying files.

## RAG

Q: What is the purpose of RAG?

A: Retrieve relevant source chunks instead of sending entire large documents.

## RAG

Q: Why does chunking strategy matter?

A: Chunks determine whether retrieved context is relevant and coherent.

## RAG

Q: What is size-based chunking best for?

A: Simple implementation when document structure is weak or unavailable.

## RAG

Q: What is structure-based chunking best for?

A: Preserving meaningful sections like headings, records, or document units.

## Embeddings

Q: What are embeddings useful for?

A: Semantic search based on meaning rather than exact word matching.

## BM25

Q: When is BM25 stronger than embeddings?

A: Exact identifiers, names, codes, policy terms, filenames, and incident numbers.

## Hybrid Retrieval

Q: Why combine embeddings and BM25?

A: To capture both semantic similarity and exact-term matches.

## Reranking

Q: What does reranking do in RAG?

A: Reorders retrieved chunks by relevance to the specific question.

## Contextual Retrieval

Q: Why add context to chunks before indexing?

A: It helps isolated chunks retain enough source meaning when retrieved later.

## Citations

Q: Why do citations matter in Claude document workflows?

A: They preserve evidence so users can verify where claims came from.

## Prompt Caching

Q: When is prompt caching useful?

A: When large stable prompt prefixes repeat within the cache window.

## Prompt Caching

Q: Is prompt caching a reliability feature?

A: No. It helps cost/latency, not correctness.

## Extended Thinking

Q: When should extended thinking be used?

A: For complex reasoning where quality justifies extra latency and cost.

## MCP

Q: What are the three core MCP server primitives?

A: Tools, resources, and prompts.

## MCP Tools

Q: Who controls MCP tools?

A: The model controls tool use.

## MCP Resources

Q: Who controls MCP resources?

A: The application controls when resources are read and included.

## MCP Prompts

Q: Who controls MCP prompts?

A: Users or client workflows intentionally invoke them.

## MCP Design

Q: When should an MCP capability be a tool?

A: When Claude should take an action or call an external capability.

## MCP Design

Q: When should an MCP capability be a resource?

A: When it exposes read-only context or catalogs for the app to include.

## MCP Inspector

Q: What is the MCP inspector for?

A: Testing and debugging MCP server primitives before production use.

## Claude Code

Q: What does `/init` do in Claude Code?

A: It inspects the project and creates project context in `CLAUDE.md`.

## Claude Code

Q: When is a planning-first Claude Code workflow best?

A: Before risky or multi-file changes with design tradeoffs.

## Claude Code

Q: Why is test-driven iteration effective with Claude Code?

A: Failing tests provide concrete feedback for implementation refinement.

## Claude Code And MCP

Q: Why connect MCP servers to Claude Code?

A: To add team-specific tools, resources, and prompts to development workflows.

## Parallel Claude Code

Q: Why use git worktrees for parallel Claude Code?

A: They isolate file edits so concurrent agents do not collide.

## Parallel Claude Code

Q: What must happen before merging parallel Claude Code work?

A: Review diffs, run tests, and resolve conflicts deliberately.

## Agents

Q: What pattern did the course emphasize for effective agents?

A: Observe the environment first, then act with focused tools and evaluate results.

## Agents

Q: Why should agents have focused tool sets?

A: Fewer relevant tools improve selection reliability.

## Agents

Q: What tasks are best suited to agents?

A: High-value tasks where the cost of occasional errors can be controlled.

## Out Of Scope

Q: How should computer use lessons be studied for this exam?

A: Keep only the general tool-loop idea; computer use itself is out of scope.
