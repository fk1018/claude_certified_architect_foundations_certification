# Introduction to Model Context Protocol Flashcards

## MCP Purpose

Q: What problem does MCP solve in Claude integrations?

A: It standardizes how apps connect Claude to external tools, resources, and prompts without hand-writing every integration schema and execution path.

Domain: D2

Example: A team wiring Claude to Jira and GitHub can point at existing MCP servers for each instead of writing custom API glue and schema definitions for both.

## MCP vs Tool Use

Q: Is MCP the same thing as Claude tool use?

A: No. MCP supplies and executes capabilities; Claude tool use is the model deciding when to call those capabilities.

Domain: D2

Example: Claude decides ("tool use") that it needs to look up a customer record, then the app dispatches that call through an MCP server that actually queries the CRM.

## MCP Client

Q: What is the role of an MCP client?

A: It bridges the application to MCP servers, handles protocol communication, initializes sessions, and lists/calls/reads server capabilities.

Domain: D2

Example: A CLI app creates a `ClientSession`, calls `list_tools()` to discover what a filesystem MCP server offers, then calls `call_tool("read_file", {...})` on the user's behalf.

## MCP Server

Q: What does an MCP server provide?

A: A standardized interface to external data or functionality through tools, resources, and prompts.

Domain: D2

Example: A "docs" MCP server exposes a `search_documents` tool, a `docs://documents` resource, and a `/summarize` prompt, all reachable the same way regardless of which client connects.

## Tools

Q: In MCP, when should something be modeled as a tool?

A: When it performs an action, calls a service, computes a result, or mutates external state.

Domain: D2

Example: `send_email(to, subject, body)` is a tool because it actually dispatches a message and changes something outside the conversation.

## Resources

Q: In MCP, when should something be modeled as a resource?

A: When it exposes context, catalogs, documents, schemas, or other read-oriented data.

Domain: D2

Example: `docs://documents` returning the full list of available document titles and IDs is a resource, since it only surfaces information rather than doing something.

## Prompts

Q: In MCP, when should something be modeled as a prompt?

A: When it is a reusable instruction template or user-triggered workflow.

Domain: D2

Example: A `/summarize` slash command that always sends "Summarize the following document in three bullet points: {content}" is modeled as a prompt.

## Tool Discovery

Q: What should an MCP client do before sending server tools to Claude?

A: Ask the MCP server for its available tools, then pass the resulting definitions to Claude.

Domain: D2

Example: On startup, the app calls `session.list_tools()` and forwards the returned tool schemas into the `tools` parameter of the Messages API request.

## Tool Execution

Q: What happens after Claude emits a `tool_use` for an MCP-backed tool?

A: The app calls the MCP client/server, receives the result, appends it as a `tool_result`, and calls Claude again.

Domain: D1

Example: Claude emits `tool_use` for `get_weather(city="Boise")`; the app calls the MCP server, gets back "72F and sunny," sends that as a `tool_result`, and Claude continues the reply using it.

## List Tools

Q: What MCP exchange lets the client learn available tools?

A: A list-tools request/result exchange.

Domain: D2

Example: The client sends a `list_tools` request and the server responds with a JSON array describing `read_file`, `write_file`, and their input schemas.

## Call Tool

Q: What MCP exchange runs a selected tool?

A: A call-tool request/result exchange.

Domain: D2

Example: The client sends `call_tool("read_file", {"path": "notes.txt"})` and the server responds with the file's contents.

## Transport

Q: What does it mean that MCP is transport agnostic?

A: The same client/server concepts can communicate over different transports such as stdio, HTTP, or WebSockets.

Domain: D2

Example: A server started as a local subprocess talks over stdio during development, but the same server logic can later be exposed over HTTP for a hosted deployment without changing its tool definitions.

## Stdio Setup

Q: What does the course sample use to connect to its local MCP server?

A: `StdioServerParameters`, `stdio_client`, and `ClientSession` initialized over stdio.

Domain: D2

Example: The client builds `StdioServerParameters(command="python", args=["server.py"])`, opens it with `stdio_client(...)`, then wraps the resulting streams in a `ClientSession` before calling `initialize()`.

## FastMCP

Q: What Python SDK pattern does the completed project use to define MCP server capabilities?

A: `FastMCP` decorators such as `@mcp.tool`, `@mcp.resource`, and `@mcp.prompt`.

Domain: D2

Example: Writing `@mcp.tool` above a Python function `def add_note(title: str, body: str):` automatically registers it as a callable MCP tool with a generated schema.

## Argument Descriptions

Q: Why should MCP tool arguments include descriptions?

A: Claude uses names and descriptions to choose tools and provide valid arguments.

Domain: D2

Example: Describing a `doc_id` argument as "the document's unique ID from the catalog, e.g. 'report-2024'" helps Claude pass a valid ID instead of guessing a document's title.

## Static Resource

Q: What is a static resource in the course sample?

A: A fixed URI such as `docs://documents` that returns the document catalog.

Domain: D2

Example: Reading `docs://documents` always returns the same kind of response, a JSON list of all documents, regardless of any input.

## Templated Resource

Q: What is a templated MCP resource?

A: A resource URI with a variable segment, such as `docs://documents/{doc_id}`, used to fetch item-specific content.

Domain: D2

Example: Reading `docs://documents/report-2024` substitutes `report-2024` for `{doc_id}` and returns just that one document's content.

## Resource Mentions

Q: How does the sample CLI use `@document` mentions?

A: It maps the mentioned document ID to an MCP resource read and adds the document content to the prompt context.

Domain: D2

Example: Typing `@report-2024` in the CLI triggers a read of `docs://documents/report-2024`, and its text is inserted into the message sent to Claude.

## Slash Commands

Q: How does the sample CLI use slash commands?

A: It maps a slash command to an MCP prompt, retrieves prompt messages, and appends them to the Claude conversation.

Domain: D2

Example: Typing `/summarize report-2024` fetches the `summarize` prompt's messages from the server and appends them to the conversation sent to Claude.

## Server Inspector

Q: When should you use the MCP server inspector?

A: When testing server tools and behavior before connecting the server to a full application workflow.

Domain: D2

Example: Before wiring a new `create_ticket` tool into the app, a developer runs the MCP inspector to call it directly and confirm it returns the expected result.

## Agentic Loop

Q: How does MCP fit the exam's agentic loop lifecycle?

A: Claude requests a tool, the app executes it through MCP, returns the result, and loops until Claude ends the turn.

Domain: D1

Example: Claude calls `search_documents`, then `read_document`, then finally answers the user in plain text with no further `tool_use`, ending the loop.

## Error Flag

Q: What does MCP `isError` communicate?

A: That a tool call failed, so the app should return an error tool result instead of treating the output as success.

Domain: D5

Example: A `read_file` call for a missing file returns `isError: true` with a message like "file not found," so the app reports failure back to Claude instead of pretending the empty result was the file's content.

## Structured Errors

Q: Why is `isError` alone not enough for production exam scenarios?

A: The exam expects structured category, retryability, attempted action, partial-result, and recovery metadata.

Domain: D5

Example: Instead of just `isError: true`, a robust response includes `{category: "rate_limit", retryable: true, action_attempted: "create_ticket", partial_result: null}` so the app can decide whether to retry automatically.

## Existing MCP Servers

Q: In an exam scenario, when should you prefer an existing MCP server over a custom integration?

A: When a maintained server already covers the standard service workflow; reserve custom servers for team-specific needs.

Domain: D2

Example: A team needing Slack integration adopts the existing Slack MCP server rather than building a bespoke one, saving custom development for their internal ticketing tool that has no public server.

## Catalog Visibility

Q: Why expose catalogs as MCP resources?

A: They let the app/agent see available context without making exploratory action-oriented tool calls.

Domain: D2

Example: Reading a `catalog://products` resource shows every product ID up front, instead of Claude having to call a `search_products` tool repeatedly just to discover what exists.

## Prompt Primitive Trap

Q: A user should click a button to start a reusable "summarize this document" workflow. Which MCP primitive is most likely?

A: A prompt, unless the primitive itself is performing the document operation.

Domain: D2

Example: The button triggers a `/summarize` MCP prompt that sends a fixed instruction template to Claude, rather than a tool that would need to itself generate the summary text.

## Resource Trap

Q: A team models a document catalog as an MCP tool. What is the better choice?

A: Use an MCP resource for the catalog and tools only for actions like editing or updating.

Domain: D2

Example: Expose `docs://documents` as a resource for browsing the catalog, and keep a separate `update_document` tool only for the action of editing a document's content.

## Tool Selection Trap

Q: Why is a vague MCP tool description risky?

A: Claude may misroute calls among similar tools or provide invalid arguments.

Domain: D2

Example: Two tools both named vaguely as "update" (one for user profiles, one for orders) with no distinguishing description can cause Claude to call the wrong one when asked to "update the order."

## Completion Trap

Q: Why are Skilljar completion checkmarks not enough for this repo?

A: The repo requires transformed notes, flashcards, practice questions, tracker updates, and progress-file updates.

Domain: General

Example: Finishing a Skilljar module's video checkmark still leaves work undone until its notes are rewritten, flashcards like this one are added, practice questions are drafted, and the tracker file is updated.
