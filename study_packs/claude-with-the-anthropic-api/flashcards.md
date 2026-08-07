# Building with the Claude API Flashcards

## Capture Status

Q: What is the capture limitation for this study pack?

A: Videos do not count for this course by user instruction; the pack uses the outline, non-video content, quiz metadata, and exam-guide alignment.

## API Keys

Q: What should you do after creating an Anthropic API key?

A: Copy it immediately, store it securely, and treat it as a secret.

## API Keys

Q: What should you do if an API key is lost or accidentally exposed?

A: Delete or rotate it and create a new key.

## API Keys

Q: Why name API keys clearly?

A: Names help identify what each key is used for when rotating, auditing, or cleaning up access.

## Multi-Turn Conversations

Q: Who manages conversation history in an API integration?

A: The application manages and sends the relevant message history.

## Multi-Turn Conversations

Q: Why is missing conversation history risky?

A: Claude loses context needed to reason about prior facts, tool results, and decisions.

## System Prompts

Q: What belongs in a system prompt?

A: Durable behavior, role, constraints, policy, and output expectations.

## System Prompts

Q: What should not be dumped into a system prompt?

A: Transient user facts or large changing task data.

## Temperature

Q: When should temperature usually be lower?

A: For extraction, grading, production workflows, and repeatable outputs.

## Temperature

Q: Does low temperature guarantee correctness?

A: No. It improves repeatability but still needs validation and review.

## Streaming

Q: What problem does response streaming primarily solve?

A: It improves perceived latency and incremental user experience.

## Streaming

Q: What problem does streaming not solve?

A: It does not enforce schemas, correctness, or semantic validation.

## Structured Data

Q: What is stronger than asking Claude to "return JSON"?

A: Tool use with JSON schemas plus validation.

## Structured Data

Q: Why can schema-valid output still be wrong?

A: It may contain semantic errors, wrong fields, unsupported values, or arithmetic mistakes.

## Prompt Evaluation

Q: What should a prompt eval start with?

A: Representative test cases and explicit grading criteria.

## Prompt Evaluation

Q: When is code-based grading best?

A: When correctness can be checked deterministically, such as schema, format, arithmetic, or required fields.

## Prompt Evaluation

Q: When is model-based grading useful?

A: When evaluation requires semantic judgment, quality assessment, or nuanced reasoning.

## Prompt Engineering

Q: What beats vague instructions like "be conservative"?

A: Specific criteria, examples, and severity or inclusion rules.

## Prompt Engineering

Q: Why use examples in prompts?

A: Examples show desired format and ambiguous-case judgment better than abstract instructions alone.

## XML Tags

Q: Why can XML tags help a prompt?

A: They separate instructions, context, examples, and expected output sections clearly.

## Tool Use Loop

Q: What is the basic API tool-use loop?

A: Send request, inspect `tool_use`, execute the tool, return `tool_result`, and continue.

## Tool Results

Q: Why must tool results be returned to Claude?

A: Claude needs them in context to decide the next step or produce the final answer.

## Message Blocks

Q: Why inspect response content blocks instead of only final text?

A: Tool calls and other structured outputs appear as typed blocks.

## Tool Schemas

Q: What should a tool schema describe?

A: Inputs, required and optional fields, allowed values, and expected structure.

## Tool Descriptions

Q: Why are tool descriptions important?

A: They are a primary signal Claude uses for tool selection.

## Tool Scope

Q: Why not give an agent every available tool?

A: Too many tools increase selection ambiguity and misuse.

## Multiple Tools

Q: What is a good way to handle overlapping tools?

A: Split, rename, or constrain them so each has a clear purpose and boundary.

## RAG

Q: What are the core RAG steps?

A: Prepare content, chunk/index it, retrieve relevant context, answer with grounding, and cite sources.

## Chunking

Q: Why does chunking matter in RAG?

A: Chunks affect retrieval precision, context fit, and whether evidence remains understandable.

## Embeddings

Q: What are embeddings useful for?

A: Finding semantically similar content even when wording differs.

## BM25

Q: What is BM25 lexical search useful for?

A: Exact terms, IDs, names, filenames, and keywords.

## Multi-Index RAG

Q: Why combine lexical and semantic retrieval?

A: It improves recall across exact-match and meaning-based queries.

## Citations

Q: What should a cited synthesis preserve?

A: Claim-source mappings, source dates, evidence, and conflicts.

## Prompt Caching

Q: When is prompt caching useful?

A: When large stable prompt prefixes repeat across calls.

## Prompt Caching

Q: When is prompt caching weak?

A: When the prompt prefix changes often or stable context is placed after variable content.

## MCP

Q: What does MCP connect?

A: MCP clients connect to MCP servers that expose tools, resources, and prompts.

## MCP Tools

Q: When should MCP expose a tool?

A: When Claude needs to perform an action or call an operation.

## MCP Resources

Q: When should MCP expose a resource?

A: When Claude needs discoverable contextual data or catalogs.

## MCP Inspector

Q: What is the MCP server inspector for?

A: Testing and debugging server capabilities before relying on them.

## Claude Code

Q: Why integrate MCP servers with Claude Code?

A: To expose team or project-specific external capabilities inside coding workflows.

## Workflows

Q: When should you choose a workflow over an agent?

A: When the path is known, controlled, and easy to test.

## Agents

Q: When should you choose an agent over a fixed workflow?

A: When Claude must inspect state, choose tools, and adapt next steps.

## Parallelization

Q: When is parallelization appropriate?

A: When tasks are independent and can be completed at the same time.

## Chaining

Q: When is chaining appropriate?

A: When each step depends on the prior step's output.

## Routing

Q: When is routing appropriate?

A: When task type determines the correct specialist, tool set, or workflow path.

## Completion Tracking

Q: Why can this course be moved to done after this pass?

A: The user explicitly defined videos as out of scope, and the remaining visible outline/non-video materials were documented.
