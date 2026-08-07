# Introduction to Model Context Protocol

- Source URL: https://anthropic-partners.skilljar.com/introduction-to-model-context-protocol/303756
- Documented: 2026-07-06
- Study pack: `study_packs/introduction-to-model-context-protocol/`
- Capture status: Complete. Captured the visible lesson outline, readable non-video lesson text for the introductory MCP/client lessons, project download evidence from the course page, completed project code from the visible download, final-assessment concept prompts, and video-only/player-error pages as out of scope.

## Captured Sections

| Section | Captured Evidence |
|---|---|
| Welcome to the course | Video/player page with reference links to the uv install guide and MCP introduction. No readable instructional body beyond links. |
| Introducing MCP | Readable lesson body captured. Covers MCP purpose, client/server architecture, MCP servers exposing tools/resources/prompts, and why MCP differs from direct API integration or raw tool use. |
| MCP clients | Readable lesson body captured. Covers MCP client role, transport-agnostic communication, `ListToolsRequest` / `ListToolsResult`, `CallToolRequest` / `CallToolResult`, and the end-to-end Claude tool-use flow. |
| Project setup | Video/player page plus starter and completed project downloads. Completed project inspected in `/tmp` only for transformed study notes. |
| Defining tools with MCP | Video/player-error page. Completed project shows `FastMCP`, `@mcp.tool`, Pydantic `Field` descriptions, read/edit document tools, and exact-match edit behavior. |
| The server inspector | Video/player-error page. Final assessment concept metadata confirms the inspector is used to test MCP server tools before full application integration. |
| Course satisfaction survey | Administrative survey only; no exam-relevant instructional content. |
| Implementing a client | Video/player-error page. Completed project shows `ClientSession`, `StdioServerParameters`, `stdio_client`, `initialize`, `list_tools`, `call_tool`, `list_prompts`, `get_prompt`, and `read_resource`. |
| Defining resources | Video/player-error page. Completed project shows static and templated resources: `docs://documents` and `docs://documents/{doc_id}` with MIME types. |
| Accessing resources | Video/player-error page. Completed project shows resource access through `read_resource`, JSON parsing for resource lists, and `@doc_id` query expansion. |
| Defining prompts | Video/player-error page. Completed project shows `@mcp.prompt` returning prompt messages for a document-formatting workflow. |
| Prompts in the client | Video/player-error page. Completed project shows slash-command handling that retrieves prompt messages and appends them into Claude conversation history. |
| Final assessment on MCP | Assessment prompts reviewed only as concept metadata, not archived as raw quiz answers. Concepts included MCP client components, tool discovery, inspector use, MCP vs direct API integration, prompt primitive choice, Python SDK decorators, and dynamic resources. |
| MCP review | Video/player-error page; no readable instructional body. |

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| Domain 1: Agentic Architecture & Orchestration | Medium | MCP client flow reinforces the agentic loop: discover tools, send tools to Claude, inspect `tool_use`, execute via MCP, append `tool_result`, and continue until final response. |
| Domain 2: Tool Design & MCP Integration | High | Direct coverage of MCP clients, servers, tools, resources, prompts, transport, tool discovery, tool execution, inspector use, and sample server/client implementation. |
| Domain 3: Claude Code Configuration & Workflows | Low | Course is not primarily about Claude Code configuration. It helps with MCP mental models that later apply to Claude Code MCP integrations, but does not cover `.mcp.json`, user-level config, or slash commands in Claude Code. |
| Domain 4: Prompt Engineering & Structured Output | Low | MCP prompts are covered as reusable prompt templates/workflows, but the course does not focus on JSON schemas, few-shot prompting, extraction validation, or batch processing. |
| Domain 5: Context Management & Reliability | Medium | Resources provide a way to expose context catalogs and fetch specific context on demand. The sample also shows basic error propagation with MCP `isError`, but not full structured retry metadata. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| MCP purpose | MCP moves integration work into specialized servers that expose external tools, resources, and prompts through a standard protocol. This reduces app-side schema/function maintenance for services like GitHub or document stores. |
| MCP client | The client is the bridge between the application and MCP servers. It handles protocol messages, server startup/connection, initialization, and calls such as list tools, call tool, list prompts, get prompt, and read resource. |
| MCP server | The server wraps an external service or local capability and exposes standardized MCP primitives. In the course sample, a document server exposes read/edit tools, document resources, and a formatting prompt. |
| MCP is not tool use | Tool use is Claude deciding to invoke a tool. MCP is a standard way to provide and execute those tools. They work together, but they solve different parts of the integration problem. |
| Tool discovery | The client asks an MCP server what tools it provides, then the app can pass those tool definitions to Claude. This maps to `ListToolsRequest` / `ListToolsResult` in the course lesson. |
| Tool execution | When Claude chooses a tool, the app asks the MCP client/server to execute it, then sends the returned result back to Claude as tool-result context. This maps to `CallToolRequest` / `CallToolResult`. |
| Transport choices | The course emphasizes MCP as transport agnostic. The sample uses stdio, while the lesson notes that other transports such as HTTP or WebSockets can fit different deployment shapes. |
| Python SDK server definitions | The completed project uses `FastMCP` decorators for primitives: `@mcp.tool`, `@mcp.resource`, and `@mcp.prompt`. Pydantic `Field` descriptions document tool/prompt arguments. |
| Tools | Tools perform actions. In the sample, `read_doc_contents` reads a document and `edit_document` mutates a document by exact string replacement. Tool descriptions and argument descriptions are part of the model-facing contract. |
| Resources | Resources expose context. The sample has a resource listing available document IDs and a templated resource for fetching document contents by ID. Use resources when Claude or the app needs visibility into available data before deciding what action to take. |
| Static vs dynamic resources | A static resource like `docs://documents` returns a fixed catalog. A templated resource like `docs://documents/{doc_id}` fetches content based on a variable URI segment. |
| Prompts | Prompts define reusable workflows or prompt templates. In the sample, a prompt builds instructions for reformatting a document and tells Claude which document/tool to use. |
| User interaction model | The sample CLI maps `@document` mentions to resource reads and slash commands such as `/format <doc>` to MCP prompts. This is a useful mental model: resources supply context, prompts supply reusable instructions, and tools perform actions. |
| Server inspector | The assessment metadata reinforces the inspector as the easy way to test an MCP server and its tools before wiring it into a larger app. |
| Tool results and errors | The sample app converts MCP tool output into Anthropic `tool_result` blocks and maps MCP `isError` into `is_error`. This is useful but incomplete for the exam's structured error-response requirements because it does not include categories or retryability metadata. |

## Decision Rules

- If the capability performs an operation or changes external state, model it as an MCP tool.
- If the capability exposes available context, catalogs, schemas, documents, or other read-oriented data, model it as an MCP resource.
- If the capability is a reusable user-triggered workflow or prompt template, model it as an MCP prompt.
- If the app needs to know available server capabilities before calling Claude, first list tools/prompts/resources through the MCP client rather than hardcoding stale definitions.
- If a resource accepts an identifier in the URI, use a templated resource such as `scheme://collection/{id}` rather than creating one static resource per item.
- If using Python `FastMCP`, use decorators to define server primitives and include useful argument descriptions so Claude can choose and call tools correctly.
- If integrating through stdio, configure command/args/env explicitly and initialize the `ClientSession` before listing or calling capabilities.
- If a tool result comes back from MCP, convert it into a Claude-compatible `tool_result` and preserve the error flag so the model can react appropriately.
- If an MCP server is new or changed, test it with the server inspector before embedding it in the full app workflow.

## Anti-Patterns

- Treating MCP as a replacement for Claude tool use. MCP supplies capabilities; Claude still decides when to call tools in the model/tool loop.
- Calling external APIs directly from the app for every integration when a maintained MCP server already exposes the needed capability.
- Modeling read-only catalogs as tools when resources would let the app/agent inspect available context with less ambiguity.
- Modeling action workflows as resources. Resources expose context; tools and prompts drive work.
- Omitting descriptions for tools or arguments and expecting reliable tool selection anyway.
- Returning only generic tool failures. The sample preserves an error flag, but exam scenarios require richer metadata such as category and retryability.
- Treating a video/player-error page as captured instructional content. It should be recorded as video-only/out of scope unless readable text, transcript, or equivalent content is available.

## Scenario Traps

- Trap: "The user clicked through the course, so documentation is complete." Better: completion requires captured sections and transformed study artifacts in the repo.
- Trap: "MCP means Claude can call any API automatically." Better: MCP servers must expose specific tools/resources/prompts, and the client/app must discover and route them.
- Trap: "A document list should be a tool because Claude can ask for it." Better: use a resource for catalogs and a tool only when an action is performed.
- Trap: "A slash-command workflow should be a tool by default." Better: if it is a reusable instruction template, use an MCP prompt; if it performs an operation, pair that prompt with tools.
- Trap: "The app can stop after a `tool_use` response." Better: execute the requested tool, return the result, and call Claude again.
- Trap: "MCP `isError` alone satisfies production error handling." Better: the exam expects structured categories, retryability, attempted action, and recovery context.
- Trap: "Transport choice changes the protocol concept." Better: stdio, HTTP, and WebSocket transports can carry the same MCP client/server responsibilities.
- Trap: "Resources are only static files." Better: resources can be templated, such as fetching a document by ID.

## Memorization Cues

- MCP primitives: tools do, resources show, prompts guide.
- Client flow: connect, initialize, discover, call/read/get, clean up.
- Tool loop: Claude `tool_use`, MCP `call_tool`, Claude `tool_result`, repeat.
- Discovery message pair: list tools, then call tools.
- Python SDK cue: `FastMCP` plus decorators.
- Resource URI cue: static catalog first, templated item fetch second.
- Error cue: `isError` is a start, not a full recovery contract.
- Inspector cue: test the MCP server before the full app.

## Source References

- `Welcome to the course`: uv install guide and MCP introduction links visible; no readable lesson body beyond references.
- `Introducing MCP`: readable lesson text on MCP purpose, client/server architecture, MCP servers, and MCP vs direct API/tool-use integration.
- `MCP clients`: readable lesson text on client role, transport options, list/call message flow, and end-to-end user-query/tool-result path.
- `Project setup`: visible downloads `cli_project.zip` and `cli_project_COMPLETE.zip`; completed project inspected temporarily outside the repo.
- Completed project files used as transformed source evidence: `README.md`, `mcp_server.py`, `mcp_client.py`, `main.py`, `core/chat.py`, `core/cli_chat.py`, `core/tools.py`, `core/cli.py`.
- `Course satisfaction survey`: administrative survey only.
- `Final assessment on MCP`: concept prompts reviewed; quiz content and answers were not archived.
- Several hands-on/review lesson pages displayed video/player-error text without readable instructional body and were treated as video-only/out of scope.

## Gaps / Follow-Up

- This course does not fully cover exam task 2.2 structured MCP error responses with `errorCategory`, retryability, business/permission/transient distinctions, and partial-result propagation.
- This course does not cover Claude Code MCP configuration mechanics such as project `.mcp.json`, user `~/.claude.json`, environment variable expansion, or team vs personal server scope.
- The visible completed sample demonstrates concepts but is not production hardened: it uses in-memory documents, basic `ValueError` failures, and minimal structured error metadata.
