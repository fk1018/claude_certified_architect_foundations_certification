# Building with the Claude API Flashcards

## Capture Status

Q: What is the capture limitation for this study pack?

A: Videos do not count for this course by user instruction; the pack uses the outline, non-video content, quiz metadata, and exam-guide alignment.

Domain: General

Example: The pack skips a walkthrough video demoing the API console but keeps the written outline notes and quiz text covering the same feature.

## API Keys

Q: What should you do after creating an Anthropic API key?

A: Copy it immediately, store it securely, and treat it as a secret.

Domain: General

Example: After generating a key like sk-ant-api03-..., paste it into a password manager entry named "prod-claude-key" right away, since the console will not show the full value again.

## API Keys

Q: What should you do if an API key is lost or accidentally exposed?

A: Delete or rotate it and create a new key.

Domain: General

Example: A key accidentally committed to a public GitHub repo should be revoked in the console immediately and replaced with a freshly generated one.

## API Keys

Q: Why name API keys clearly?

A: Names help identify what each key is used for when rotating, auditing, or cleaning up access.

Domain: General

Example: Naming a key "billing-service-prod" instead of "key1" makes it obvious which one to revoke during a security incident.

## Multi-Turn Conversations

Q: Who manages conversation history in an API integration?

A: The application manages and sends the relevant message history.

Domain: D5

Example: A chat app stores each user and assistant turn in its own database and resends the growing list as the `messages` array on every API call.

## Multi-Turn Conversations

Q: Why is missing conversation history risky?

A: Claude loses context needed to reason about prior facts, tool results, and decisions.

Domain: D5

Example: If a follow-up "what was the total again?" is sent without the earlier turn where the total was computed, Claude has no way to know the number.

## System Prompts

Q: What belongs in a system prompt?

A: Durable behavior, role, constraints, policy, and output expectations.

Domain: D4

Example: "You are a support agent for Acme Corp; always respond formally and never disclose internal pricing" belongs in the system prompt.

## System Prompts

Q: What should not be dumped into a system prompt?

A: Transient user facts or large changing task data.

Domain: D4

Example: A specific customer's order number or today's changing inventory count belongs in the user message, not baked into the system prompt.

## Temperature

Q: When should temperature usually be lower?

A: For extraction, grading, production workflows, and repeatable outputs.

Domain: D4

Example: An invoice line-item extraction pipeline sets temperature to 0 so the same invoice produces the same structured output every run.

## Temperature

Q: Does low temperature guarantee correctness?

A: No. It improves repeatability but still needs validation and review.

Domain: D4

Example: Temperature 0 on a flawed math word-problem prompt still yields the same consistently wrong answer every time.

## Streaming

Q: What problem does response streaming primarily solve?

A: It improves perceived latency and incremental user experience.

Domain: D5

Example: A chatbot UI shows tokens appearing word by word instead of a multi-second blank screen while Claude finishes the full reply.

## Streaming

Q: What problem does streaming not solve?

A: It does not enforce schemas, correctness, or semantic validation.

Domain: D4

Example: A streamed response can finish rendering token by token and still end up as invalid JSON that fails schema validation.

## Structured Data

Q: What is stronger than asking Claude to "return JSON"?

A: Tool use with JSON schemas plus validation.

Domain: D4

Example: Defining a tool with a schema requiring `name: string` and `amount: number`, then validating the returned tool arguments against it, is stronger than just asking Claude to "reply in JSON".

## Structured Data

Q: Why can schema-valid output still be wrong?

A: It may contain semantic errors, wrong fields, unsupported values, or arithmetic mistakes.

Domain: D4

Example: A schema-valid response might correctly format `{"total": 45.00}` while the actual sum of the line items is really 54.00.

## Prompt Evaluation

Q: What should a prompt eval start with?

A: Representative test cases and explicit grading criteria.

Domain: D4

Example: Before tuning a summarization prompt, assemble 20 sample articles with reference summaries and a rubric defining what counts as a passing summary.

## Prompt Evaluation

Q: When is code-based grading best?

A: When correctness can be checked deterministically, such as schema, format, arithmetic, or required fields.

Domain: D4

Example: Checking that an extracted date matches `YYYY-MM-DD` or that a returned total equals the sum of the line items.

## Prompt Evaluation

Q: When is model-based grading useful?

A: When evaluation requires semantic judgment, quality assessment, or nuanced reasoning.

Domain: D4

Example: Asking a grader model to rate whether a generated support reply is polite and on-topic.

## Prompt Engineering

Q: What beats vague instructions like "be conservative"?

A: Specific criteria, examples, and severity or inclusion rules.

Domain: D4

Example: Replacing "be conservative" with "flag any transaction over $10,000 or involving a new vendor as high risk" removes the guesswork.

## Prompt Engineering

Q: Why use examples in prompts?

A: Examples show desired format and ambiguous-case judgment better than abstract instructions alone.

Domain: D4

Example: Including two sample input/output pairs in the prompt shows Claude exactly how to format a phone number, resolving ambiguity a text instruction alone left open.

## XML Tags

Q: Why can XML tags help a prompt?

A: They separate instructions, context, examples, and expected output sections clearly.

Domain: D4

Example: Wrapping reference text in `<context>...</context>` and the question in `<question>...</question>` stops Claude from confusing source material with the instructions.

## Tool Use Loop

Q: What is the basic API tool-use loop?

A: Send request, inspect `tool_use`, execute the tool, return `tool_result`, and continue.

Domain: D2

Example: Claude returns a `tool_use` block calling `get_weather(city="Austin")`, the app runs the function, and sends the result back as a `tool_result` block so Claude can finish the reply.

## Tool Results

Q: Why must tool results be returned to Claude?

A: Claude needs them in context to decide the next step or produce the final answer.

Domain: D2

Example: After a `search_orders` tool returns order #4521's status, that result must be sent back to Claude before it can tell the user "your order shipped yesterday."

## Message Blocks

Q: Why inspect response content blocks instead of only final text?

A: Tool calls and other structured outputs appear as typed blocks.

Domain: D2

Example: A response might contain a `text` block plus a `tool_use` block, and code that only reads `response.content[0].text` would miss the tool call entirely.

## Tool Schemas

Q: What should a tool schema describe?

A: Inputs, required and optional fields, allowed values, and expected structure.

Domain: D2

Example: A `create_ticket` tool schema specifies `title` as a required string and `priority` as an optional enum of "low", "medium", or "high", rejecting any other value.

## Tool Descriptions

Q: Why are tool descriptions important?

A: They are a primary signal Claude uses for tool selection.

Domain: D2

Example: A `search_flights` tool described as "search available flights by origin, destination, and date" is far more likely to be picked correctly than one merely named `tool_2`.

## Tool Scope

Q: Why not give an agent every available tool?

A: Too many tools increase selection ambiguity and misuse.

Domain: D2

Example: Giving an agent both `delete_file` and `archive_file` with similar descriptions makes it likely to call the wrong one for a "clean up old logs" request.

## Multiple Tools

Q: What is a good way to handle overlapping tools?

A: Split, rename, or constrain them so each has a clear purpose and boundary.

Domain: D2

Example: Renaming two similar tools to `send_email_now` and `schedule_email_later` with distinct descriptions removes the ambiguity that generic names like `email_tool_1`/`email_tool_2` caused.

## RAG

Q: What are the core RAG steps?

A: Prepare content, chunk/index it, retrieve relevant context, answer with grounding, and cite sources.

Domain: D5

Example: A support-doc chatbot indexes help articles into chunks, embeds them, retrieves the top matches for "how do I reset my password," and answers while citing the specific article used.

## Chunking

Q: Why does chunking matter in RAG?

A: Chunks affect retrieval precision, context fit, and whether evidence remains understandable.

Domain: D5

Example: Splitting a 50-page manual into chunks by section heading keeps retrieved passages focused, versus one giant chunk that buries the relevant paragraph in irrelevant text.

## Embeddings

Q: What are embeddings useful for?

A: Finding semantically similar content even when wording differs.

Domain: D5

Example: A query for "cancel my subscription" retrieves a document titled "how to end your membership" even though the wording differs.

## BM25

Q: What is BM25 lexical search useful for?

A: Exact terms, IDs, names, filenames, and keywords.

Domain: D5

Example: Searching for the exact error code "ERR_4042" or a product SKU is better served by BM25 than by semantic embedding search.

## Multi-Index RAG

Q: Why combine lexical and semantic retrieval?

A: It improves recall across exact-match and meaning-based queries.

Domain: D5

Example: A hybrid search finds both the exact invoice number "INV-2024-0091" via BM25 and conceptually related billing questions via embeddings, something either method alone would miss.

## Citations

Q: What should a cited synthesis preserve?

A: Claim-source mappings, source dates, evidence, and conflicts.

Domain: D5

Example: An answer stating "revenue grew 12% (Q2 2024 report, page 3)" lets a reader trace the claim back to its exact source and date.

## Prompt Caching

Q: When is prompt caching useful?

A: When large stable prompt prefixes repeat across calls.

Domain: D5

Example: A coding assistant that sends the same 10,000-token system prompt and codebase context on every request caches that prefix so repeated calls skip re-processing it.

## Prompt Caching

Q: When is prompt caching weak?

A: When the prompt prefix changes often or stable context is placed after variable content.

Domain: D5

Example: Putting the user's constantly changing question before a large stable document breaks the cache, since the stable content is no longer a fixed prefix.

## MCP

Q: What does MCP connect?

A: MCP clients connect to MCP servers that expose tools, resources, and prompts.

Domain: D2

Example: Claude Code acts as an MCP client connecting to a GitHub MCP server that exposes tools like `create_issue` and resources like repository file listings.

## MCP Tools

Q: When should MCP expose a tool?

A: When Claude needs to perform an action or call an operation.

Domain: D2

Example: An MCP server exposes a `send_slack_message` tool so Claude can actually post a message, not just read one.

## MCP Resources

Q: When should MCP expose a resource?

A: When Claude needs discoverable contextual data or catalogs.

Domain: D2

Example: An MCP server exposes a `list_open_tickets` resource so Claude can browse the current ticket catalog without taking any action.

## MCP Inspector

Q: What is the MCP server inspector for?

A: Testing and debugging server capabilities before relying on them.

Domain: D2

Example: Running the MCP inspector against a new local server confirms the `create_issue` tool accepts the right parameters before wiring it into a live agent.

## Claude Code

Q: Why integrate MCP servers with Claude Code?

A: To expose team or project-specific external capabilities inside coding workflows.

Domain: D3

Example: A team connects an internal deployment-status MCP server so Claude Code can check build health directly while helping debug a failing pipeline.

## Workflows

Q: When should you choose a workflow over an agent?

A: When the path is known, controlled, and easy to test.

Domain: D1

Example: A fixed "upload file, validate format, then send confirmation email" sequence is better as a scripted workflow than an open-ended agent.

## Agents

Q: When should you choose an agent over a fixed workflow?

A: When Claude must inspect state, choose tools, and adapt next steps.

Domain: D1

Example: A research assistant that must decide which of several search tools to call next based on what it finds is better built as an agent than a fixed script.

## Parallelization

Q: When is parallelization appropriate?

A: When tasks are independent and can be completed at the same time.

Domain: D1

Example: Summarizing five unrelated news articles at once, since none of the summaries depends on another's output.

## Chaining

Q: When is chaining appropriate?

A: When each step depends on the prior step's output.

Domain: D1

Example: First extracting key facts from a contract, then using those facts as input to a second step that drafts a risk summary.

## Routing

Q: When is routing appropriate?

A: When task type determines the correct specialist, tool set, or workflow path.

Domain: D1

Example: An incoming support ticket gets classified as "billing," "technical," or "account" first, then routed to a prompt or tool set specialized for that category.

## Completion Tracking

Q: Why can this course be moved to done after this pass?

A: The user explicitly defined videos as out of scope, and the remaining visible outline/non-video materials were documented.

Domain: General

Example: The tracker marks the course complete once the outline, quiz metadata, and exam-guide topics are captured, without waiting on the excluded video lectures.
