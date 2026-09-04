# Claude with Amazon Bedrock Flashcards

## Capture Status

Q: What is the capture limitation for this course?

A: Several visible exercise/setup/wrap-up pages were video-only or empty; by repo rule they are recorded as out of scope, not blockers.

Domain: General

Example: A "Set up your AWS account" video lesson with no accompanying transcript text is logged as out of scope rather than left as an unresolved gap.

## Capture Status

Q: Should this course be moved from todo to done now?

A: Yes. Under the video-scope rule, readable non-video sections were captured and video-only sections were recorded as out of scope.

Domain: General

Example: All readable lesson pages for the Bedrock course are captured while two video-only demo segments stay marked out of scope, so the course moves to done.

## Exam Scope

Q: How should AWS-specific Bedrock setup details be treated for the certification?

A: As context only; the exam guide marks specific cloud provider configurations out of scope.

Domain: General

Example: Knowing that Bedrock requires enabling model access in the AWS console is useful background, but the exam will not test the exact console click path.

## Model Selection

Q: What three tradeoffs drive Claude model selection in the course?

A: Intelligence, speed/latency, and cost.

Domain: D1

Example: A team picks a smaller, faster model for real-time chat autocomplete but a larger model for overnight batch summarization where latency matters less.

## Model Selection

Q: When should a stronger, slower, more expensive model be selected?

A: When the task requires deeper reasoning and the outcome justifies the added latency and cost.

Domain: D1

Example: A legal-contract risk analysis tool uses the strongest model because a missed clause is costlier than the extra few seconds and cents per call.

## Model Selection

Q: Why might one application use multiple model tiers?

A: Different subtasks can optimize for speed, cost, or reasoning depth independently.

Domain: D1

Example: A support app uses a fast, cheap model to classify ticket urgency and a stronger model only for drafting the final customer reply.

## Bedrock API

Q: Who manages conversation history in a Bedrock/Claude chat app?

A: The application manages and resends the relevant message history.

Domain: D5

Example: A chatbot backend stores each turn in a database and reassembles the last N messages into the `messages` array on every new Bedrock InvokeModel call.

## Bedrock API

Q: What happens if a follow-up request omits prior conversation context?

A: Claude treats it as an independent call and may miss prior facts or intent.

Domain: D5

Example: A user says "make it shorter" in a new request with no history attached, and Claude has no idea what "it" refers to.

## Bedrock API

Q: What operational issue can model IDs and regions create?

A: A model may not be available in the selected region, causing brittle deployment behavior.

Domain: D5

Example: An app hardcodes a Claude model ID for us-east-1 and starts throwing errors when traffic is routed through an eu-west-1 Bedrock endpoint where that model isn't enabled.

## System Prompts

Q: What belongs in a system prompt?

A: Durable role, behavior, boundaries, policy, style, and output expectations.

Domain: D4

Example: "You are a customer support agent for Acme; never share internal pricing, always respond in a friendly tone, and cite the relevant help-article ID" belongs in the system prompt.

## System Prompts

Q: Why not put core behavior only in repeated user instructions?

A: It is repetitive, user-visible, and weaker than durable system-level configuration.

Domain: D4

Example: Retyping "always answer in bullet points" at the top of every user message is redundant compared to setting it once in the system prompt.

## Temperature

Q: When should temperature generally be low?

A: For extraction, grading, production workflows, and repeatable behavior.

Domain: D4

Example: A pipeline that pulls invoice totals into a database field sets temperature near 0 so the same invoice yields the same extracted number every run.

## Temperature

Q: Does low temperature guarantee correctness?

A: No. It improves repeatability but still needs validation and review.

Domain: D4

Example: A low-temperature extraction run consistently returns the same wrong field mapping, so a validation step is still needed to catch it.

## Streaming

Q: What problem does streaming solve?

A: It improves perceived latency by returning output incrementally.

Domain: D4

Example: A chat UI shows Claude's response appearing word by word instead of the user staring at a blank screen for ten seconds before the full answer appears.

## Streaming

Q: What problem does streaming not solve?

A: It does not enforce schema, correctness, or semantic validation.

Domain: D4

Example: Streaming a JSON response token by token still lets the final output be malformed or missing a required field.

## Output Control

Q: What can prefilled assistant messages do?

A: Steer the beginning and shape of Claude's response.

Domain: D4

Example: Prefilling the assistant turn with "{" pushes Claude straight into producing a JSON object instead of a prose lead-in.

## Output Control

Q: What do stop sequences do?

A: Stop generation at predefined boundaries.

Domain: D4

Example: Setting a stop sequence of "\`\`\`" halts generation right after a code block closes, trimming trailing commentary.

## Structured Data

Q: When are prefill and stop sequences useful for structured output?

A: For lower-risk cases where raw JSON/code needs less surrounding prose.

Domain: D4

Example: A quick internal script prefills "{" and stops at "}" to grab a small config object without building a full tool schema.

## Structured Data

Q: What is stronger than asking Claude to return JSON?

A: Tool-based structured output with a schema plus validation.

Domain: D4

Example: Defining a `record_order` tool with a JSON schema for `order_id`, `total`, and `items` guarantees Claude's output matches that shape, unlike asking it to "return JSON" in prose.

## Structured Data

Q: Why can schema-valid output still need validation?

A: It can contain semantic errors, unsupported values, or wrong field assignments.

Domain: D4

Example: A tool call correctly fills the `status` field with a valid enum value, but picks "shipped" for an order that hasn't actually shipped yet.

## Prompt Evaluation

Q: What is the difference between prompt engineering and prompt evaluation?

A: Engineering improves prompts; evaluation measures whether they work.

Domain: D4

Example: Rewriting a summarization prompt to add constraints is prompt engineering; running it against 50 labeled test articles and scoring accuracy is prompt evaluation.

## Prompt Evaluation

Q: What are the core pieces of an eval workflow?

A: Prompt, evaluation dataset, model output, grader, and iteration.

Domain: D4

Example: A team tests a classification prompt against 100 labeled emails, scores each output with a grader, then tweaks the prompt and reruns the same dataset.

## Prompt Evaluation

Q: When is a code-based grader best?

A: When correctness can be checked deterministically, such as syntax, JSON validity, or required fields.

Domain: D4

Example: A script runs `json.loads()` on every model output and flags a failure whenever parsing throws or a required "id" field is missing.

## Prompt Evaluation

Q: When is a model-based grader useful?

A: When evaluation requires semantic or qualitative judgment.

Domain: D4

Example: A second Claude call is prompted to rate whether a generated customer-support reply is "polite and on-topic" on a 1-5 scale.

## Prompt Evaluation

Q: Why should eval datasets include edge cases?

A: Happy-path tests hide failures that appear in production.

Domain: D4

Example: A dataset that only includes well-formatted invoices misses how the prompt handles a scanned invoice with a smudged total, which shows up once deployed.

## Prompt Engineering

Q: What is the first prompt-engineering improvement for vague output?

A: Lead with a clear, direct statement of the task.

Domain: D4

Example: Replacing "Can you maybe help with this document?" with "Summarize this document in 3 bullet points" removes the vagueness up front.

## Prompt Engineering

Q: What should specificity add to a prompt?

A: Criteria, constraints, process steps, and desired output properties.

Domain: D4

Example: "Summarize in exactly 3 bullets, under 15 words each, focusing only on financial figures" gives Claude concrete criteria instead of a vague "summarize this."

## Prompt Engineering

Q: Why use XML tags in prompts?

A: They separate instructions, examples, context, and output sections clearly.

Domain: D4

Example: Wrapping the source document in `<document>...</document>` and the task instructions in `<instructions>...</instructions>` keeps Claude from confusing the two.

## Prompt Engineering

Q: What do few-shot examples teach?

A: Output format and judgment for ambiguous cases.

Domain: D4

Example: Showing two example support tickets labeled "urgent" and "not urgent" teaches Claude how to classify a borderline third ticket the same way.

## Prompt Engineering

Q: Where can good few-shot examples come from?

A: Evaluation failures and representative edge cases.

Domain: D4

Example: A ticket that the model previously misclassified during eval testing gets added as a labeled few-shot example so the same mistake doesn't repeat.

## Tool Use

Q: What is the basic tool-use loop?

A: Send tools, inspect `tool_use`, execute the tool, return `tool_result`, and continue.

Domain: D2

Example: Claude emits a `tool_use` block calling `get_weather(city="Austin")`, the app runs that function, sends back a `tool_result` with the temperature, and Claude uses it to answer the user.

## Tool Use

Q: Why should applications inspect `stop_reason`?

A: It tells whether Claude is requesting tools or producing a final answer.

Domain: D2

Example: An app checks `stop_reason == "tool_use"` to decide whether to run a function versus `stop_reason == "end_turn"` to display the reply straight to the user.

## Tool Use

Q: Why must tool results be added to conversation history?

A: Claude needs the results in context to reason about the next step.

Domain: D2

Example: After a `search_orders` tool returns a list of order IDs, that `tool_result` is appended to the conversation so Claude can pick the right one for the next step.

## Tool Design

Q: What makes a tool description effective?

A: Clear purpose, inputs, outputs, boundaries, and when to use it versus similar tools.

Domain: D2

Example: "Use `search_orders` to find orders by customer email; use `get_order` only when you already have a specific order ID" tells Claude exactly when each tool applies.

## Tool Design

Q: Why should tools be narrow and scoped?

A: Focused tools reduce selection ambiguity and misuse.

Domain: D2

Example: Splitting a bloated `manage_orders` tool into separate `get_order`, `cancel_order`, and `refund_order` tools makes it clearer which one Claude should call for a refund request.

## Tool Schema

Q: What does a JSON schema tell Claude?

A: The tool arguments, required fields, allowed structure, and field meanings.

Domain: D2

Example: A schema marking `email` as a required string and `priority` as an enum of "low"/"medium"/"high" tells Claude exactly what shape to fill in for a `create_ticket` call.

## Tool Choice

Q: What does `tool_choice: auto` mean?

A: Claude may call a tool or answer directly.

Domain: D2

Example: Asked "what's 2+2?" with a calculator tool available under `tool_choice: auto`, Claude just answers "4" directly instead of invoking the tool.

## Tool Choice

Q: What does `tool_choice: any` mean?

A: Claude must call a tool but can choose which one.

Domain: D2

Example: With `tool_choice: any` and both `search_orders` and `get_order` available, Claude picks whichever tool fits the request but cannot just reply in plain text.

## Tool Choice

Q: When should forced tool choice be used?

A: When a specific tool must run first or when testing a required tool path.

Domain: D2

Example: A test harness forces `tool_choice: {"type": "tool", "name": "lookup_customer"}` to verify the tool integration works before letting Claude choose freely.

## Batch Tools

Q: When is batch tool use appropriate?

A: When multiple independent operations can be executed in parallel.

Domain: D2

Example: Claude issues three separate `get_weather` calls for New York, London, and Tokyo in one turn since none of the calls depend on another's result.

## Batch Tools

Q: What is the risk of batching dependent operations?

A: It hides ordering requirements and can produce incorrect workflow behavior.

Domain: D2

Example: Batching a `create_account` call together with a `create_order` call for that same account can fail if the order call runs before the account exists.

## Structured Data With Tools

Q: Why is tool-based extraction more reliable than text JSON?

A: Claude fills structured tool inputs instead of free-form prose.

Domain: D2

Example: A `record_contact` tool with typed `name` and `phone` fields reliably produces a clean structured record instead of Claude writing "Name: John, Phone: 555-1234" as text to be re-parsed.

## Flexible Extraction

Q: What is the tradeoff of a generic `to_json` extraction tool?

A: Less schema work, but weaker guarantees than a purpose-built schema.

Domain: D2

Example: A generic `to_json` tool can quickly extract "any relevant fields" from a messy email, but won't guarantee a `phone_number` field is always present the way a dedicated schema would.

## Text Editor Tool

Q: What is the transferable exam lesson from the Bedrock text editor tool?

A: Pick specialized read/edit tools by task shape and inspect context before modifying files.

Domain: D2

Example: Before replacing a line in a config file, the text editor tool first reads the surrounding lines so the edit targets the correct occurrence rather than guessing blindly.

## RAG

Q: What is the purpose of RAG?

A: Retrieve relevant source chunks instead of sending entire large documents.

Domain: D5

Example: Instead of pasting an entire 500-page policy manual into the prompt, a RAG system retrieves only the 3 paragraphs about vacation accrual to answer a specific employee question.

## RAG

Q: Why does chunking strategy matter?

A: Chunks determine whether retrieved context is relevant and coherent.

Domain: D5

Example: Splitting a contract mid-sentence at a fixed character count can cut off the clause that answers the question, while splitting by section keeps it intact.

## RAG

Q: What is size-based chunking best for?

A: Simple implementation when document structure is weak or unavailable.

Domain: D5

Example: A folder of unformatted plain-text chat logs is split into fixed 500-character chunks since there are no headings or sections to key off of.

## RAG

Q: What is structure-based chunking best for?

A: Preserving meaningful sections like headings, records, or document units.

Domain: D5

Example: A markdown handbook is chunked by `##` heading so each retrieved chunk is a complete, self-contained policy section rather than a fragment.

## Embeddings

Q: What are embeddings useful for?

A: Semantic search based on meaning rather than exact word matching.

Domain: D5

Example: A search for "how do I get my money back" retrieves a chunk titled "Refund Policy" even though none of those exact words appear together in the query.

## BM25

Q: When is BM25 stronger than embeddings?

A: Exact identifiers, names, codes, policy terms, filenames, and incident numbers.

Domain: D5

Example: A search for the exact ticket ID "INC-004521" is matched reliably by BM25's keyword overlap, whereas an embedding search might return semantically similar but wrong incident tickets.

## Hybrid Retrieval

Q: Why combine embeddings and BM25?

A: To capture both semantic similarity and exact-term matches.

Domain: D5

Example: A hybrid search for "billing error on invoice INV-9981" uses embeddings to find billing-related content and BM25 to make sure the exact invoice number surfaces.

## Reranking

Q: What does reranking do in RAG?

A: Reorders retrieved chunks by relevance to the specific question.

Domain: D5

Example: An initial retrieval pulls 20 loosely related chunks, and a reranker moves the 3 chunks that most directly answer "what is the cancellation deadline" to the top.

## Contextual Retrieval

Q: Why add context to chunks before indexing?

A: It helps isolated chunks retain enough source meaning when retrieved later.

Domain: D5

Example: A chunk that just says "the deadline is 30 days" gets prefixed with "This is from the Refund Policy section on returns:" so it still makes sense retrieved on its own.

## Citations

Q: Why do citations matter in Claude document workflows?

A: They preserve evidence so users can verify where claims came from.

Domain: D5

Example: A generated answer states "your warranty expires in 2027" with a citation pointing to page 4 of the uploaded warranty PDF, letting the user check the source directly.

## Prompt Caching

Q: When is prompt caching useful?

A: When large stable prompt prefixes repeat within the cache window.

Domain: D5

Example: A 10,000-token system prompt with tool definitions is cached so each new user turn only pays for the small delta instead of re-processing the whole prefix.

## Prompt Caching

Q: Is prompt caching a reliability feature?

A: No. It helps cost/latency, not correctness.

Domain: D5

Example: Caching a flawed system prompt makes every subsequent call cheaper and faster, but it still reproduces the same flawed behavior each time.

## Extended Thinking

Q: When should extended thinking be used?

A: For complex reasoning where quality justifies extra latency and cost.

Domain: D4

Example: A multi-step math word problem or a tricky debugging task benefits from extended thinking, while a simple "translate this sentence" request does not need it.

## MCP

Q: What are the three core MCP server primitives?

A: Tools, resources, and prompts.

Domain: D2

Example: A GitHub MCP server might expose a `create_issue` tool, a `repo://readme` resource, and a "summarize pull request" prompt template.

## MCP Tools

Q: Who controls MCP tools?

A: The model controls tool use.

Domain: D2

Example: Claude decides on its own, mid-conversation, to call an MCP `search_files` tool when it determines it needs to look something up.

## MCP Resources

Q: Who controls MCP resources?

A: The application controls when resources are read and included.

Domain: D2

Example: A code-editor plugin decides to attach the `file://current_file.py` resource to the context only when the user has that file open.

## MCP Prompts

Q: Who controls MCP prompts?

A: Users or client workflows intentionally invoke them.

Domain: D2

Example: A user explicitly selects a "/summarize-pr" MCP prompt template from a menu rather than Claude deciding on its own to run it.

## MCP Design

Q: When should an MCP capability be a tool?

A: When Claude should take an action or call an external capability.

Domain: D2

Example: "Send a Slack message" or "create a Jira ticket" are actions, so they belong as MCP tools rather than resources.

## MCP Design

Q: When should an MCP capability be a resource?

A: When it exposes read-only context or catalogs for the app to include.

Domain: D2

Example: A catalog of available product SKUs is exposed as an MCP resource the app attaches to context, rather than a tool Claude has to call and wait on.

## MCP Inspector

Q: What is the MCP inspector for?

A: Testing and debugging MCP server primitives before production use.

Domain: D2

Example: A developer uses the MCP inspector to manually invoke a new `get_invoice` tool and check its response shape before wiring it into a live agent.

## Claude Code

Q: What does `/init` do in Claude Code?

A: It inspects the project and creates project context in `CLAUDE.md`.

Domain: D3

Example: Running `/init` in a new Next.js repo scans the folder structure and package.json, then writes a `CLAUDE.md` noting it's a Next.js app with a `components/` and `api/` layout.

## Claude Code

Q: When is a planning-first Claude Code workflow best?

A: Before risky or multi-file changes with design tradeoffs.

Domain: D3

Example: Before migrating an app's auth system to a new provider, a plan is written and reviewed first rather than jumping straight into editing a dozen files.

## Claude Code

Q: Why is test-driven iteration effective with Claude Code?

A: Failing tests provide concrete feedback for implementation refinement.

Domain: D3

Example: Claude writes a test asserting `parse_date("2026-09-03")` returns the right object, watches it fail, then iterates on the implementation until it passes.

## Claude Code And MCP

Q: Why connect MCP servers to Claude Code?

A: To add team-specific tools, resources, and prompts to development workflows.

Domain: D3

Example: A team connects an internal Jira MCP server so Claude Code can create and update tickets directly as part of a coding session.

## Parallel Claude Code

Q: Why use git worktrees for parallel Claude Code?

A: They isolate file edits so concurrent agents do not collide.

Domain: D3

Example: Two agents work on separate git worktrees, one fixing a bug in `auth.py` and another adding a feature in `billing.py`, without either touching the other's working copy.

## Parallel Claude Code

Q: What must happen before merging parallel Claude Code work?

A: Review diffs, run tests, and resolve conflicts deliberately.

Domain: D3

Example: Before merging two worktree branches, the developer reads each diff, runs the full test suite, and manually resolves a conflict where both branches edited the same config file.

## Agents

Q: What pattern did the course emphasize for effective agents?

A: Observe the environment first, then act with focused tools and evaluate results.

Domain: D1

Example: Before renaming a function, an agent first searches the codebase for all its call sites, then makes the edits, then runs tests to confirm nothing broke.

## Agents

Q: Why should agents have focused tool sets?

A: Fewer relevant tools improve selection reliability.

Domain: D1

Example: A coding agent given only `read_file`, `edit_file`, and `run_tests` picks the right tool more reliably than one also cluttered with unrelated marketing or billing tools.

## Agents

Q: What tasks are best suited to agents?

A: High-value tasks where the cost of occasional errors can be controlled.

Domain: D1

Example: An agent triages and drafts replies to routine support tickets with human review before sending, since a wrong draft is cheap to catch and fix.

## Out Of Scope

Q: How should computer use lessons be studied for this exam?

A: Keep only the general tool-loop idea; computer use itself is out of scope.

Domain: General

Example: Remember that computer use follows the same observe-act-evaluate loop as other tool use, but skip memorizing the specific screenshot/click coordinate mechanics for the exam.
