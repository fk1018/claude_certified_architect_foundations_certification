# Claude with Google Cloud's Vertex AI Flashcards

## Vertex Setup

Q: What is the exam-relevant meaning of enabling Anthropic models in Vertex AI?

A: It is provider access setup; it does not replace prompt design, tool-loop logic, context management, or validation.

Domain: General

Example: Enabling Claude models in the Vertex Model Garden lets your app call them, but you still have to write the system prompt, structure the tool loop, and validate outputs yourself.

## Vertex Setup

Q: What local setup does the readable Vertex lesson emphasize?

A: Install/authenticate `gcloud`, set the project ID, and configure application-default credentials so the SDK can call Vertex.

Domain: General

Example: Run `gcloud auth application-default login`, then `gcloud config set project my-vertex-project`, so the Claude SDK's Vertex client can pick up credentials automatically.

## Provider Scope

Q: Why should you avoid memorizing detailed Vertex console steps for the exam?

A: The exam guide marks specific cloud-provider configuration out of scope; study transferable Claude architecture patterns instead.

Domain: General

Example: Skip memorizing exact IAM role names or console screen layouts in Vertex; focus instead on prompt structure and tool-loop design, which apply the same way on Bedrock or the Anthropic API.

## API State

Q: In a multi-turn Claude app on Vertex, where does conversation state live?

A: In the application; the app must preserve and resend relevant prior messages.

Domain: D5

Example: A chat app stores each turn in a database and, on every new request, resends the full prior message list to Claude, since the Vertex API itself does not remember earlier turns.

## Model Selection

Q: What model-selection rule should guide production design?

A: Use the smallest, fastest, cheapest model that meets the quality bar; escalate only when capability changes outcomes.

Domain: D1

Example: Use Haiku to classify support tickets by category, but reserve Sonnet or Opus for drafting the actual customer replies where reasoning quality matters more.

## System Prompts

Q: What belongs in a system prompt?

A: Durable behavior, role, boundaries, policy, style, and output expectations.

Domain: D4

Example: "You are a customer support agent for Acme; always respond in a friendly tone, never share internal pricing formulas, and format answers as short paragraphs."

## System Prompts

Q: What should not be hidden in a system prompt?

A: Transient user facts, case-specific state, or data that should come from tools/context.

Domain: D4

Example: Don't hardcode "the current user's name is Alex" into the system prompt; pass it in the user message or fetch it via a tool call instead.

## Temperature

Q: What does lower temperature improve?

A: Repeatability, not correctness.

Domain: D4

Example: Setting temperature to 0 for a classification prompt makes the same input return the same label every run, but it will not fix a prompt that misclassifies a category in the first place.

## Streaming

Q: When is response streaming useful?

A: When perceived latency matters in an interactive user experience.

Domain: D5

Example: In a chat UI, streaming tokens as they generate lets the user start reading the answer within a second instead of staring at a blank screen for the full 10-second generation.

## Streaming

Q: What does streaming not solve?

A: Schema validity, factual correctness, validation, or tool-loop control.

Domain: D5

Example: Streaming a JSON response token by token still requires parsing and validating the final assembled JSON against your schema before you trust it.

## Structured Output

Q: What is stronger than asking Claude to "return JSON"?

A: Tool/schema-based structured output plus deterministic parsing and semantic validation.

Domain: D4

Example: Define a `record_order` tool with a strict JSON schema for fields like `item_id` and `quantity`, then have your app validate the tool call's arguments before writing to the database.

## Output Control

Q: When are prefill and stop sequences reasonable?

A: For low-risk output shaping when schema/tool enforcement is unnecessary or unavailable.

Domain: D4

Example: Prefill the assistant turn with "{" to nudge Claude straight into JSON output for a quick internal script, where a malformed field is not a big deal.

## Prompt Evaluation

Q: What are the core pieces of a prompt evaluation loop?

A: Representative test data, grading criteria, graders, and iterative prompt changes.

Domain: D5

Example: Collect 50 real support tickets, define a rubric for "correctly identifies the issue," score each prompt version against that rubric, then tweak the prompt and re-run.

## Model Grading

Q: When should you use model-based grading?

A: For semantic, subjective, completeness, or judgment-heavy criteria.

Domain: D5

Example: Use a Claude grader to judge whether a generated email "sounds empathetic and addresses the customer's specific complaint," since no regex can check that.

## Code Grading

Q: When should you use code-based grading?

A: For deterministic checks like JSON validity, required fields, regexes, arithmetic, and exact format.

Domain: D5

Example: Write a Python assertion that checks the model's output parses as JSON and contains a non-empty `order_id` field before it's passed downstream.

## Prompting

Q: Why lead with a clear direct task?

A: It reduces inference burden and improves output consistency.

Domain: D4

Example: Opening with "Summarize this contract in 3 bullet points" gets more consistent results than burying the actual task after several paragraphs of background context.

## Prompting

Q: What do examples teach beyond output format?

A: Ambiguous-case judgment and boundary decisions.

Domain: D4

Example: Showing an example where a sarcastic review is labeled "negative" teaches Claude how to handle tone-based edge cases that a plain format spec wouldn't cover.

## XML Tags

Q: Why use XML tags in prompts?

A: They separate instructions, examples, context, and output requirements.

Domain: D4

Example: Wrapping reference material in `<document>...</document>` and the task in `<task>...</task>` helps Claude tell "background to read" apart from "the thing to actually do."

## Tool Loop

Q: What are the basic steps in a Claude tool-use loop?

A: Claude requests a tool, the app executes it, returns the tool result, then calls Claude again.

Domain: D1

Example: Claude asks to call `get_weather(city="Seattle")`, the app runs that function, sends back "62F and rainy" as a tool_result, and Claude uses it to answer the user.

## Tool Loop

Q: What should the app inspect to decide whether to continue a tool loop?

A: Structured response/message block types and stop reason, not only assistant prose.

Domain: D1

Example: Check whether `stop_reason` is `tool_use` and whether the response contains a `tool_use` content block, rather than scanning the assistant's text for phrases like "I'll call a tool now."

## Tool Schemas

Q: What makes a tool schema easier for Claude to use correctly?

A: Clear name, description, input fields, field descriptions, required fields, enums, and boundaries.

Domain: D2

Example: A `create_ticket` tool with a `priority` field constrained to the enum `["low","medium","high"]` and a description like "the urgency level, defaults to medium" leaves Claude no room to guess.

## Tool Selection

Q: What happens when many tools overlap?

A: Tool selection becomes less reliable and misrouting increases.

Domain: D2

Example: With both `search_orders` and `search_customers` tools described almost identically, Claude may call the wrong one for a query like "find recent activity for account 123."

## Tool Enforcement

Q: If a tool must run before a risky action, what should enforce it?

A: Programmatic control flow or hooks, not prompt instructions alone.

Domain: D2

Example: Before executing a `delete_account` tool call, the app code checks that a `confirm_deletion` tool was called first, rather than just telling Claude in the prompt "always confirm before deleting."

## Batch Tool

Q: When is a batch tool useful?

A: For independent operations that can run together without hidden dependencies.

Domain: D2

Example: Fetching the current weather for five different cities at once is a good batch candidate since none of those lookups depends on another's result.

## Text Edit Tool

Q: What exam principle applies to text editing tools?

A: Inspect context before editing, make targeted changes, and verify with tests/review.

Domain: D2

Example: Before changing a function signature, read the surrounding file to see its callers, make the minimal edit needed, then run the test suite to confirm nothing broke.

## Web Search Tool

Q: What should web/search workflows preserve?

A: Source provenance, dates when relevant, and claim-source mappings.

Domain: D2

Example: When Claude states "the API rate limit is 1000 requests/min," the workflow should retain which page and publish date that figure came from, in case the docs have since changed.

## RAG

Q: What problem does RAG solve?

A: It retrieves relevant source chunks instead of sending an entire corpus to the model.

Domain: D5

Example: Instead of pasting a 2,000-page policy manual into every prompt, RAG retrieves just the 3 paragraphs about "vacation carryover" that answer the user's question.

## Chunking

Q: What makes chunking good?

A: Chunks preserve semantic coherence and enough context to be useful when retrieved.

Domain: D5

Example: Splitting a manual by section headings keeps a full policy explanation together, instead of cutting it mid-sentence at a fixed 500-character boundary.

## Embeddings

Q: What are embeddings best at?

A: Semantic similarity.

Domain: D5

Example: A query for "how do I get my money back" retrieves a chunk titled "Refund Policy" via embeddings even though the words don't literally match.

## BM25

Q: What is BM25 best at?

A: Exact terms, identifiers, policy names, filenames, and codes.

Domain: D5

Example: A search for error code "ERR_4092" reliably surfaces the exact matching document with BM25, where an embedding search might rank it lower amid semantically similar but wrong results.

## Hybrid Retrieval

Q: When should you combine BM25 and embeddings?

A: When queries need both exact matching and semantic matching.

Domain: D5

Example: A support search combining BM25 and embeddings can correctly handle both "SKU-88213 return policy" (exact code) and "can I send this back" (semantic paraphrase) in the same system.

## Reranking

Q: When should you use reranking?

A: When first-pass retrieval finds plausible chunks but orders them poorly.

Domain: D5

Example: Initial retrieval returns 20 loosely relevant chunks; a reranker then reorders them so the one directly answering the user's question lands at the top before being sent to Claude.

## Contextual Retrieval

Q: What does contextual retrieval add?

A: Short document-level context to chunks before indexing so retrieved chunks remain meaningful.

Domain: D5

Example: Prepending "This chunk is from the Q3 2024 earnings call transcript" to an isolated paragraph keeps it interpretable even after it's been split away from the rest of the document.

## Citations

Q: Why are citations exam-relevant?

A: They support verification, provenance, uncertainty handling, and trustworthy synthesis.

Domain: D5

Example: A generated answer that says "returns are allowed within 30 days [Source: Return Policy, p.2]" lets a user or reviewer quickly check the claim against the original document.

## Prompt Caching

Q: What is prompt caching good for?

A: Reducing latency/cost when large stable prompt prefixes repeat.

Domain: D5

Example: Caching a 20-page product manual that's reused as context across hundreds of customer support queries avoids reprocessing it from scratch on every request.

## Prompt Caching

Q: What is prompt caching not?

A: A correctness or reliability mechanism.

Domain: D5

Example: Caching a flawed system prompt just makes the same wrong behavior repeat faster and cheaper; it does nothing to fix the underlying error.

## MCP

Q: What is the difference between MCP tools and resources?

A: Tools are model-controlled actions; resources are app-controlled context.

Domain: D2

Example: An MCP `send_email` tool is something Claude decides to invoke mid-conversation, while an MCP resource exposing a company's style guide is context the app chooses to attach up front.

## MCP

Q: What are MCP prompts?

A: Reusable user-invoked templates/workflows exposed by an MCP server.

Domain: D2

Example: A `/summarize-pr` prompt exposed by a GitHub MCP server lets a user trigger a preset "review this pull request and summarize the changes" workflow with one command.

## MCP Inspector

Q: Why use the MCP inspector?

A: To test tools, resources, and prompts before connecting them to production workflows.

Domain: D2

Example: Run the MCP inspector against a new `search_inventory` tool to confirm it returns correctly shaped results before wiring it into the live support agent.

## Claude Code

Q: What workflow pattern makes Claude Code safer?

A: Provide project context, plan before risky edits, test changes, and review diffs.

Domain: D3

Example: Before asking Claude Code to refactor the auth module, point it at the relevant files, have it propose a plan first, then run the test suite and review the diff before merging.

## Parallel Claude Code

Q: How should parallel Claude Code sessions be isolated?

A: Use separate git worktrees.

Domain: D3

Example: Running two Claude Code sessions on the same feature branch in one working directory would clash; separate worktrees let each session edit files without stepping on the other.

## Automated Debugging

Q: What guardrails should surround automated debugging?

A: Tests, review, limited permissions, observability, and deployment controls.

Domain: D3

Example: Let an automated debugging agent read logs and propose a fix, but require it to run in a sandboxed branch with no direct production deploy access, and require a human to approve the merge.

## Workflows

Q: When should you prefer a fixed workflow?

A: When the path is predictable and reliability/control matter.

Domain: D1

Example: A fixed workflow that always extracts fields, then validates, then writes to a database fits an invoice-processing pipeline where the steps never change.

## Agents

Q: When should you prefer an agent?

A: When the system must inspect state, choose tools, and adapt dynamically.

Domain: D1

Example: A research assistant that decides on the fly whether to search the web, query a database, or ask a clarifying question needs agent-style flexibility, not a fixed script.

## Workflow Patterns

Q: Match the workflow pattern to the situation: parallelization, chaining, routing.

A: Parallelize independent tasks, chain dependent steps, route by task type or complexity.

Domain: D1

Example: Summarize five unrelated documents in parallel, chain "extract data -> validate -> format report" as sequential steps, and route simple FAQs to Haiku while complex ones go to Opus.

## Computer Use

Q: How should computer use be treated for this exam?

A: Out of scope except as broad observe-act-tool-loop context.

Domain: D1

Example: Know that computer use lets Claude view a screenshot and click/type like a user in a general observe-decide-act loop, but don't expect exam questions on specific screen-coordinate APIs.
