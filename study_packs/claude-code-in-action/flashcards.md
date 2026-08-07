# Claude Code in Action Flashcards

## Coding Assistant Tool Loop

Q: Why does a coding assistant need tools?

A: The model only produces text; Claude Code executes tool requests such as reading files, editing code, and running commands.

## Tool Use

Q: What transforms a text model into a coding assistant?

A: A tool-use loop where the app gives tools, Claude requests an action, the app executes it, and results return to Claude.

## Built-In Tool Selection

Q: When should you choose Grep?

A: Use Grep to search file contents for symbols, imports, error messages, or text patterns.

## Built-In Tool Selection

Q: When should you choose Glob?

A: Use Glob to find files by path/name patterns, such as test files or files with a specific extension.

## Built-In Tool Selection

Q: When should you choose Read?

A: Use Read when Claude needs full file context before reasoning or editing.

## Built-In Tool Selection

Q: When should you choose Edit?

A: Use Edit for targeted changes when the old text is unique enough to match safely.

## Built-In Tool Selection

Q: When should Write be preferred over Edit?

A: Use Write for new files or full-file replacement, especially when Edit cannot anchor a unique change safely.

## Built-In Tool Selection

Q: When should Bash be used?

A: Use Bash for commands, tests, setup, inspections, and verification steps that need a shell.

## `/init`

Q: What does `/init` do in a new Claude Code project?

A: It has Claude inspect the project and create starter project context, typically in `CLAUDE.md`.

## `CLAUDE.md`

Q: What is `CLAUDE.md` for?

A: Persistent project guidance: architecture, commands, conventions, constraints, and recurring context.

## Memory Scope

Q: What is the exam-relevant difference between project and user memory?

A: Project memory can be shared with the repo; user memory is personal and not shared with teammates.

## `/memory`

Q: When should you use `/memory`?

A: When a correction or project rule should persist across future messages or sessions.

## File Mentions

Q: When should you use `@path`?

A: When a specific known file should be included as context for the current request.

## Persistent File References

Q: When should a file be referenced in `CLAUDE.md`?

A: When the file is frequently relevant, such as a schema, architecture doc, or existing agent instructions.

## Context Relevance

Q: Why is too much context an anti-pattern?

A: Irrelevant context consumes attention and tokens, making Claude less focused on the important files and facts.

## Screenshots

Q: What are screenshots best for in Claude Code?

A: Communicating UI targets, visual bugs, or design changes precisely.

## Plan Mode

Q: When should you use plan mode?

A: Use it for multi-file, risky, architectural, or exploratory tasks where the approach should be reviewed before editing.

## Direct Execution

Q: When is direct execution appropriate?

A: For small, clear, low-risk changes with known scope and obvious verification.

## Effort

Q: What does `/effort` help with?

A: It adjusts reasoning depth for difficult logic/debugging problems, not broad codebase exploration.

## `ultrathink`

Q: How is `ultrathink` different from `/effort`?

A: `ultrathink` signals extra reasoning for one prompt; `/effort` adjusts session-level reasoning behavior.

## Plan Review

Q: Why edit a plan before approving it?

A: To correct missing constraints or implementation direction before Claude modifies files.

## Escape

Q: When should you press Escape?

A: When Claude is heading in the wrong direction, doing too much, or needs immediate redirection.

## `/rewind`

Q: What problem does `/rewind` solve?

A: It returns to an earlier conversation point after distracting or unhelpful turns.

## `/compact`

Q: When should you use `/compact`?

A: When a long session contains useful learning but needs a smaller context footprint for related work.

## `/clear`

Q: When should you use `/clear`?

A: When starting unrelated work where old context may confuse Claude.

## `/resume`

Q: What does `/resume` let you do?

A: Return to a prior session after clearing or leaving it.

## Custom Commands

Q: Where do project-scoped slash commands live?

A: In `.claude/commands/`, where each markdown file becomes a slash command.

## Command Arguments

Q: What does `$ARGUMENTS` do in a custom command?

A: It injects the user-provided command arguments into the command prompt.

## Commands vs Memory

Q: When should you choose a slash command instead of `CLAUDE.md`?

A: For repeatable on-demand workflows rather than always-loaded project standards.

## MCP Server Setup

Q: What does `claude mcp add playwright npx @playwright/mcp@latest` conceptually do?

A: Registers a local Playwright MCP server so Claude Code can use browser-control tools.

## MCP Permissions

Q: Why pre-approve MCP tools locally?

A: To reduce repeated permission prompts for trusted tools, while keeping the permission decision explicit.

## MCP In CI

Q: How are MCP permissions different in GitHub Actions?

A: CI requires explicit `allowed_tools` entries for every permitted tool, including MCP tools.

## GitHub Integration

Q: What does `/install-github-app` set up?

A: GitHub Actions workflows for Claude mentions in issues/PRs and automated PR reviews.

## GitHub Custom Instructions

Q: Why add custom instructions to a Claude GitHub Action?

A: To provide CI-specific project context, such as setup state, server URL, logs, fixtures, and tool availability.

## Hook Basics

Q: What are Claude Code hooks?

A: Commands that run around Claude Code events, especially before or after tool use.

## PreToolUse

Q: What is PreToolUse best for?

A: Blocking or validating a proposed tool call before it executes.

## PostToolUse

Q: What is PostToolUse best for?

A: Formatting, testing, linting, reviewing, or feeding back results after a tool call.

## Hook Exit Codes

Q: What does exit code 2 mean in a PreToolUse hook?

A: Block the tool call and send stderr feedback back to Claude.

## Hook Input

Q: Why should hook input be logged during development?

A: Event and tool input shapes differ; logging shows which fields the hook should inspect.

## Sensitive Files

Q: Why is a Read hook alone insufficient to protect `.env`?

A: Other tools like Grep and Bash have different inputs and may still access the file unless separately blocked.

## Permissions Deny

Q: When is a permission deny rule better than a single hook?

A: When a restriction should apply uniformly across multiple tools and access paths.

## Hook Path Security

Q: Why do hook docs recommend absolute paths?

A: They reduce path interception and binary planting risks.

## Shared Hook Settings

Q: How can a team share hook settings while using local absolute paths?

A: Commit a template such as `settings.example.json` and generate local `settings.local.json` during setup.

## Type-Check Hook

Q: What problem does a type-check PostToolUse hook solve?

A: It catches missed call sites or type errors after edits and feeds diagnostics back to Claude.

## Independent Review Hook

Q: Why launch a second Claude instance from a hook?

A: To review changes independently, avoiding the original generator's context bias.

## Expensive Hooks

Q: How should expensive hooks be targeted?

A: Limit them to high-value directories or operations to control latency and API usage.

## Agent SDK Package

Q: Which package does the course identify as importable for Claude Code automation?

A: `@anthropic-ai/claude-agent-sdk`.

## SDK Query

Q: What does the SDK `query` function stream?

A: JSON conversation events, including tool calls, tool results, and Claude text/result messages.

## `allowedTools`

Q: Why pass `allowedTools` to an SDK run?

A: To enforce least privilege and keep an automation focused on only the tools it needs.

## CI Gap

Q: What CI topic is not fully covered by this course but remains exam-relevant?

A: Non-interactive `claude -p`, `--output-format json`, and `--json-schema` structured CI output.

## Path Rules Gap

Q: What Claude Code configuration topic still needs follow-up?

A: `.claude/rules/` path-scoped rule files with YAML `paths` frontmatter.
