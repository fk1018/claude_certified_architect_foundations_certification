# Introduction to Model Context Protocol Flashcards

## MCP Purpose

Q: What problem does MCP solve in Claude integrations?

A: It standardizes how apps connect Claude to external tools, resources, and prompts without hand-writing every integration schema and execution path.

## MCP vs Tool Use

Q: Is MCP the same thing as Claude tool use?

A: No. MCP supplies and executes capabilities; Claude tool use is the model deciding when to call those capabilities.

## MCP Client

Q: What is the role of an MCP client?

A: It bridges the application to MCP servers, handles protocol communication, initializes sessions, and lists/calls/reads server capabilities.

## MCP Server

Q: What does an MCP server provide?

A: A standardized interface to external data or functionality through tools, resources, and prompts.

## Tools

Q: In MCP, when should something be modeled as a tool?

A: When it performs an action, calls a service, computes a result, or mutates external state.

## Resources

Q: In MCP, when should something be modeled as a resource?

A: When it exposes context, catalogs, documents, schemas, or other read-oriented data.

## Prompts

Q: In MCP, when should something be modeled as a prompt?

A: When it is a reusable instruction template or user-triggered workflow.

## Tool Discovery

Q: What should an MCP client do before sending server tools to Claude?

A: Ask the MCP server for its available tools, then pass the resulting definitions to Claude.

## Tool Execution

Q: What happens after Claude emits a `tool_use` for an MCP-backed tool?

A: The app calls the MCP client/server, receives the result, appends it as a `tool_result`, and calls Claude again.

## List Tools

Q: What MCP exchange lets the client learn available tools?

A: A list-tools request/result exchange.

## Call Tool

Q: What MCP exchange runs a selected tool?

A: A call-tool request/result exchange.

## Transport

Q: What does it mean that MCP is transport agnostic?

A: The same client/server concepts can communicate over different transports such as stdio, HTTP, or WebSockets.

## Stdio Setup

Q: What does the course sample use to connect to its local MCP server?

A: `StdioServerParameters`, `stdio_client`, and `ClientSession` initialized over stdio.

## FastMCP

Q: What Python SDK pattern does the completed project use to define MCP server capabilities?

A: `FastMCP` decorators such as `@mcp.tool`, `@mcp.resource`, and `@mcp.prompt`.

## Argument Descriptions

Q: Why should MCP tool arguments include descriptions?

A: Claude uses names and descriptions to choose tools and provide valid arguments.

## Static Resource

Q: What is a static resource in the course sample?

A: A fixed URI such as `docs://documents` that returns the document catalog.

## Templated Resource

Q: What is a templated MCP resource?

A: A resource URI with a variable segment, such as `docs://documents/{doc_id}`, used to fetch item-specific content.

## Resource Mentions

Q: How does the sample CLI use `@document` mentions?

A: It maps the mentioned document ID to an MCP resource read and adds the document content to the prompt context.

## Slash Commands

Q: How does the sample CLI use slash commands?

A: It maps a slash command to an MCP prompt, retrieves prompt messages, and appends them to the Claude conversation.

## Server Inspector

Q: When should you use the MCP server inspector?

A: When testing server tools and behavior before connecting the server to a full application workflow.

## Agentic Loop

Q: How does MCP fit the exam's agentic loop lifecycle?

A: Claude requests a tool, the app executes it through MCP, returns the result, and loops until Claude ends the turn.

## Error Flag

Q: What does MCP `isError` communicate?

A: That a tool call failed, so the app should return an error tool result instead of treating the output as success.

## Structured Errors

Q: Why is `isError` alone not enough for production exam scenarios?

A: The exam expects structured category, retryability, attempted action, partial-result, and recovery metadata.

## Existing MCP Servers

Q: In an exam scenario, when should you prefer an existing MCP server over a custom integration?

A: When a maintained server already covers the standard service workflow; reserve custom servers for team-specific needs.

## Catalog Visibility

Q: Why expose catalogs as MCP resources?

A: They let the app/agent see available context without making exploratory action-oriented tool calls.

## Prompt Primitive Trap

Q: A user should click a button to start a reusable "summarize this document" workflow. Which MCP primitive is most likely?

A: A prompt, unless the primitive itself is performing the document operation.

## Resource Trap

Q: A team models a document catalog as an MCP tool. What is the better choice?

A: Use an MCP resource for the catalog and tools only for actions like editing or updating.

## Tool Selection Trap

Q: Why is a vague MCP tool description risky?

A: Claude may misroute calls among similar tools or provide invalid arguments.

## Completion Trap

Q: Why are Skilljar completion checkmarks not enough for this repo?

A: The repo requires transformed notes, flashcards, practice questions, tracker updates, and progress-file updates.
