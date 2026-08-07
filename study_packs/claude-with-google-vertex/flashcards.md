# Claude with Google Cloud's Vertex AI Flashcards

## Vertex Setup

Q: What is the exam-relevant meaning of enabling Anthropic models in Vertex AI?

A: It is provider access setup; it does not replace prompt design, tool-loop logic, context management, or validation.

## Vertex Setup

Q: What local setup does the readable Vertex lesson emphasize?

A: Install/authenticate `gcloud`, set the project ID, and configure application-default credentials so the SDK can call Vertex.

## Provider Scope

Q: Why should you avoid memorizing detailed Vertex console steps for the exam?

A: The exam guide marks specific cloud-provider configuration out of scope; study transferable Claude architecture patterns instead.

## API State

Q: In a multi-turn Claude app on Vertex, where does conversation state live?

A: In the application; the app must preserve and resend relevant prior messages.

## Model Selection

Q: What model-selection rule should guide production design?

A: Use the smallest, fastest, cheapest model that meets the quality bar; escalate only when capability changes outcomes.

## System Prompts

Q: What belongs in a system prompt?

A: Durable behavior, role, boundaries, policy, style, and output expectations.

## System Prompts

Q: What should not be hidden in a system prompt?

A: Transient user facts, case-specific state, or data that should come from tools/context.

## Temperature

Q: What does lower temperature improve?

A: Repeatability, not correctness.

## Streaming

Q: When is response streaming useful?

A: When perceived latency matters in an interactive user experience.

## Streaming

Q: What does streaming not solve?

A: Schema validity, factual correctness, validation, or tool-loop control.

## Structured Output

Q: What is stronger than asking Claude to "return JSON"?

A: Tool/schema-based structured output plus deterministic parsing and semantic validation.

## Output Control

Q: When are prefill and stop sequences reasonable?

A: For low-risk output shaping when schema/tool enforcement is unnecessary or unavailable.

## Prompt Evaluation

Q: What are the core pieces of a prompt evaluation loop?

A: Representative test data, grading criteria, graders, and iterative prompt changes.

## Model Grading

Q: When should you use model-based grading?

A: For semantic, subjective, completeness, or judgment-heavy criteria.

## Code Grading

Q: When should you use code-based grading?

A: For deterministic checks like JSON validity, required fields, regexes, arithmetic, and exact format.

## Prompting

Q: Why lead with a clear direct task?

A: It reduces inference burden and improves output consistency.

## Prompting

Q: What do examples teach beyond output format?

A: Ambiguous-case judgment and boundary decisions.

## XML Tags

Q: Why use XML tags in prompts?

A: They separate instructions, examples, context, and output requirements.

## Tool Loop

Q: What are the basic steps in a Claude tool-use loop?

A: Claude requests a tool, the app executes it, returns the tool result, then calls Claude again.

## Tool Loop

Q: What should the app inspect to decide whether to continue a tool loop?

A: Structured response/message block types and stop reason, not only assistant prose.

## Tool Schemas

Q: What makes a tool schema easier for Claude to use correctly?

A: Clear name, description, input fields, field descriptions, required fields, enums, and boundaries.

## Tool Selection

Q: What happens when many tools overlap?

A: Tool selection becomes less reliable and misrouting increases.

## Tool Enforcement

Q: If a tool must run before a risky action, what should enforce it?

A: Programmatic control flow or hooks, not prompt instructions alone.

## Batch Tool

Q: When is a batch tool useful?

A: For independent operations that can run together without hidden dependencies.

## Text Edit Tool

Q: What exam principle applies to text editing tools?

A: Inspect context before editing, make targeted changes, and verify with tests/review.

## Web Search Tool

Q: What should web/search workflows preserve?

A: Source provenance, dates when relevant, and claim-source mappings.

## RAG

Q: What problem does RAG solve?

A: It retrieves relevant source chunks instead of sending an entire corpus to the model.

## Chunking

Q: What makes chunking good?

A: Chunks preserve semantic coherence and enough context to be useful when retrieved.

## Embeddings

Q: What are embeddings best at?

A: Semantic similarity.

## BM25

Q: What is BM25 best at?

A: Exact terms, identifiers, policy names, filenames, and codes.

## Hybrid Retrieval

Q: When should you combine BM25 and embeddings?

A: When queries need both exact matching and semantic matching.

## Reranking

Q: When should you use reranking?

A: When first-pass retrieval finds plausible chunks but orders them poorly.

## Contextual Retrieval

Q: What does contextual retrieval add?

A: Short document-level context to chunks before indexing so retrieved chunks remain meaningful.

## Citations

Q: Why are citations exam-relevant?

A: They support verification, provenance, uncertainty handling, and trustworthy synthesis.

## Prompt Caching

Q: What is prompt caching good for?

A: Reducing latency/cost when large stable prompt prefixes repeat.

## Prompt Caching

Q: What is prompt caching not?

A: A correctness or reliability mechanism.

## MCP

Q: What is the difference between MCP tools and resources?

A: Tools are model-controlled actions; resources are app-controlled context.

## MCP

Q: What are MCP prompts?

A: Reusable user-invoked templates/workflows exposed by an MCP server.

## MCP Inspector

Q: Why use the MCP inspector?

A: To test tools, resources, and prompts before connecting them to production workflows.

## Claude Code

Q: What workflow pattern makes Claude Code safer?

A: Provide project context, plan before risky edits, test changes, and review diffs.

## Parallel Claude Code

Q: How should parallel Claude Code sessions be isolated?

A: Use separate git worktrees.

## Automated Debugging

Q: What guardrails should surround automated debugging?

A: Tests, review, limited permissions, observability, and deployment controls.

## Workflows

Q: When should you prefer a fixed workflow?

A: When the path is predictable and reliability/control matter.

## Agents

Q: When should you prefer an agent?

A: When the system must inspect state, choose tools, and adapt dynamically.

## Workflow Patterns

Q: Match the workflow pattern to the situation: parallelization, chaining, routing.

A: Parallelize independent tasks, chain dependent steps, route by task type or complexity.

## Computer Use

Q: How should computer use be treated for this exam?

A: Out of scope except as broad observe-act-tool-loop context.
