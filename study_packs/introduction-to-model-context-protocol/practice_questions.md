# Introduction to Model Context Protocol Practice Questions

These questions are exam-aligned study material based on the captured Skilljar course structure, readable introductory lessons, visible completed project download, final-assessment concept metadata, and `exam_guide_pdf.txt`.

## Question 1

Scenario: A team is building a chat app where users ask Claude about GitHub repositories, pull requests, and issues. The team is considering writing all GitHub tool schemas and API wrappers inside its app.

Question: What is the best reason to consider an MCP server instead?

A. MCP eliminates the need for Claude tool use.

B. MCP can shift tool definitions and execution into a dedicated server that wraps GitHub functionality.

C. MCP forces every GitHub operation to run in a browser.

D. MCP replaces the need to return tool results to Claude.

Correct answer: B

Explanation: MCP standardizes external capability exposure through servers. A GitHub MCP server can provide tools/resources/prompts without the app hand-maintaining every schema and API wrapper.

Distractors:

- A: Claude still uses tool use to decide when to call capabilities.
- C: MCP is not browser-specific.
- D: Tool results still need to be returned to Claude in the agentic loop.

## Question 2

Scenario: Your MCP-backed app receives a Claude response with a `tool_use` block for `read_doc_contents`.

Question: What should the app do next?

A. Return the tool name to the user and stop.

B. Execute the tool through the MCP client/server, append a `tool_result`, and call Claude again.

C. Ask the MCP server to list prompts instead.

D. Convert the tool call into a static resource URI and skip execution.

Correct answer: B

Explanation: MCP-backed tools still follow the agentic tool loop: execute the requested tool, return the result, and let Claude continue reasoning.

Distractors:

- A: Stopping at `tool_use` leaves the user without an answer.
- C: Prompt listing is unrelated to executing the requested tool.
- D: Resources expose context; they do not replace action execution.

## Question 3

Scenario: A document MCP server needs to expose the list of available document IDs so a client can offer autocomplete and decide which document to fetch.

Question: Which MCP primitive is the best fit?

A. A resource such as a document catalog URI.

B. A prompt that asks Claude to guess available documents.

C. A mutating edit tool.

D. A system prompt hardcoded with every document forever.

Correct answer: A

Explanation: A document catalog is read-oriented context. Resources are designed to expose this kind of data without treating it as an action.

Distractors:

- B: Guessing documents is unreliable.
- C: Edit tools mutate data and do not fit a catalog.
- D: Hardcoding dynamic catalogs creates stale context.

## Question 4

Scenario: Users can type `@report.pdf` in a CLI, and the app should include that document's contents in Claude's context before answering.

Question: What is the best MCP design?

A. Read a templated resource such as `docs://documents/{doc_id}` and insert the returned content into context.

B. Force Claude to call every document-related tool.

C. Treat `@report.pdf` as a human escalation request.

D. Store the document list in a hidden completion checkmark.

Correct answer: A

Explanation: Templated resources let the client fetch item-specific context by URI, matching the course sample's document access pattern.

Distractors:

- B: Calling every tool adds noise and risk.
- C: A document mention is a context reference, not an escalation.
- D: Completion state is not runtime context.

## Question 5

Scenario: A team wants users to trigger a reusable "format this document as Markdown" workflow from the client UI.

Question: Which MCP primitive should represent the reusable workflow instructions?

A. An MCP prompt.

B. An MCP resource catalog.

C. A transport setting.

D. A final answer from Claude with no tool access.

Correct answer: A

Explanation: MCP prompts package reusable instructions/workflows. They can be combined with tools, such as an edit tool, when action is required.

Distractors:

- B: A resource exposes data, not a workflow template.
- C: Transport does not define user-facing workflow logic.
- D: The workflow may need tools and structured instructions.

## Question 6

Scenario: You are implementing a Python MCP document server. You need to expose a function that reads a document and accepts a `doc_id` argument with a useful description.

Question: Which implementation style best matches the course sample?

A. Define a `FastMCP` server and decorate the function with `@mcp.tool`, using argument descriptions.

B. Put the function name in a README only.

C. Add the document text to every system prompt.

D. Wait for Claude to infer the function signature from natural language.

Correct answer: A

Explanation: The sample uses `FastMCP` decorators and described arguments so the capability becomes a model-facing MCP tool.

Distractors:

- B: Documentation alone does not expose a callable tool.
- C: System prompts are not a tool execution interface.
- D: Inference is unreliable and not a protocol contract.

## Question 7

Scenario: You built an MCP server and want to check whether its tools are callable before integrating it with your production chat app.

Question: What should you use first?

A. The MCP server inspector.

B. A production customer request.

C. A vague prompt asking Claude to test everything.

D. A resource URI with no server running.

Correct answer: A

Explanation: The course assessment metadata reinforces the inspector as the simplest way to validate server tools before full application integration.

Distractors:

- B: Production traffic is a poor first test.
- C: A vague prompt is not a deterministic server validation tool.
- D: A URI alone cannot validate server behavior.

## Question 8

Scenario: An MCP server returns a failed tool result. The app maps the result to Claude with `is_error: true`, but the model cannot tell whether to retry, ask for different input, or escalate.

Question: What should the team add for exam-aligned production reliability?

A. Structured error metadata such as category, retryability, attempted action, and human-readable recovery context.

B. A lower model temperature only.

C. More static resources with no error information.

D. A hidden survey page.

Correct answer: A

Explanation: `isError` communicates failure, but the exam expects richer error responses so agents and coordinators can recover intelligently.

Distractors:

- B: Temperature does not classify failures.
- C: More resources do not explain a failed action.
- D: Survey content is administrative, not error handling.

## Question 9

Scenario: A local MCP sample starts a document server process and communicates with it through stdin/stdout. Another deployment may use HTTP.

Question: What concept does this illustrate?

A. MCP is transport agnostic.

B. MCP requires browser automation.

C. MCP resources cannot be used locally.

D. MCP prompts can only run in CI.

Correct answer: A

Explanation: MCP client/server responsibilities are separate from the transport. Stdio is common for local servers, while other transports can fit different setups.

Distractors:

- B: Browsers are not required.
- C: Local resource access is valid.
- D: Prompts are not CI-specific.

## Question 10

Scenario: A Claude Code team wants to add a shared MCP integration for Jira. The exam asks what should be reviewed before writing a custom server.

Question: What is the best first step?

A. Check whether an existing maintained MCP server covers the standard Jira workflow.

B. Build a custom server immediately so every tool name is unique.

C. Store the Jira token directly in committed source files.

D. Ask Claude to use Grep instead of Jira data.

Correct answer: A

Explanation: The exam guide favors existing community servers for standard integrations and custom servers for team-specific workflows.

Distractors:

- B: Custom work may be unnecessary maintenance.
- C: Secrets should not be committed.
- D: Grep cannot replace external Jira integration.
