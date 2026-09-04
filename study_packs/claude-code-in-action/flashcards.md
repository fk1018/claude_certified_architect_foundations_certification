# Claude Code in Action Flashcards

## Coding Assistant Tool Loop

Q: Why does a coding assistant need tools?

A: The model only produces text; Claude Code executes tool requests such as reading files, editing code, and running commands.

Domain: D1

Example: Asked to fix a bug, Claude can't run the failing test itself unless the host app invokes a Bash tool on its behalf and returns the output.

## Tool Use

Q: What transforms a text model into a coding assistant?

A: A tool-use loop where the app gives tools, Claude requests an action, the app executes it, and results return to Claude.

Domain: D1

Example: Claude requests `Read("app.py")`, the app returns the file text, then Claude requests `Edit(...)` based on what it read, repeating until the task is done.

## Built-In Tool Selection

Q: When should you choose Grep?

A: Use Grep to search file contents for symbols, imports, error messages, or text patterns.

Domain: D2

Example: Searching for every place `calculateTotal` is called before renaming the function.

## Built-In Tool Selection

Q: When should you choose Glob?

A: Use Glob to find files by path/name patterns, such as test files or files with a specific extension.

Domain: D2

Example: Running `**/*.test.ts` to list every TypeScript test file in the repo before deciding which suite to run.

## Built-In Tool Selection

Q: When should you choose Read?

A: Use Read when Claude needs full file context before reasoning or editing.

Domain: D2

Example: Reading `config.py` in full before deciding how a new setting should fit alongside the existing ones.

## Built-In Tool Selection

Q: When should you choose Edit?

A: Use Edit for targeted changes when the old text is unique enough to match safely.

Domain: D2

Example: Changing a single default timeout value on line 42 of `client.py` without touching the rest of the file.

## Built-In Tool Selection

Q: When should Write be preferred over Edit?

A: Use Write for new files or full-file replacement, especially when Edit cannot anchor a unique change safely.

Domain: D2

Example: Generating a brand-new `README.md` for a project, or rewriting a small config file where nearly every line changes.

## Built-In Tool Selection

Q: When should Bash be used?

A: Use Bash for commands, tests, setup, inspections, and verification steps that need a shell.

Domain: D2

Example: Running `npm test` after a change to confirm the suite still passes.

## `/init`

Q: What does `/init` do in a new Claude Code project?

A: It has Claude inspect the project and create starter project context, typically in `CLAUDE.md`.

Domain: D3

Example: Running `/init` in a fresh Next.js repo produces a `CLAUDE.md` noting the framework, package manager, and `npm run dev` command.

## `CLAUDE.md`

Q: What is `CLAUDE.md` for?

A: Persistent project guidance: architecture, commands, conventions, constraints, and recurring context.

Domain: D3

Example: A `CLAUDE.md` entry stating "run `pytest -x` before committing" so Claude runs it automatically on future sessions without being told again.

## Memory Scope

Q: What is the exam-relevant difference between project and user memory?

A: Project memory can be shared with the repo; user memory is personal and not shared with teammates.

Domain: D3

Example: A team's shared lint command lives in project `CLAUDE.md`, while one developer's personal preference for terse commit messages lives only in their user memory.

## `/memory`

Q: When should you use `/memory`?

A: When a correction or project rule should persist across future messages or sessions.

Domain: D3

Example: After telling Claude twice to use `pnpm` instead of `npm`, running `/memory` to save that rule so it isn't repeated in the next session.

## File Mentions

Q: When should you use `@path`?

A: When a specific known file should be included as context for the current request.

Domain: D5

Example: Typing "fix the bug in @src/utils/parser.ts" to pull that exact file into context instead of asking Claude to search for it.

## Persistent File References

Q: When should a file be referenced in `CLAUDE.md`?

A: When the file is frequently relevant, such as a schema, architecture doc, or existing agent instructions.

Domain: D3

Example: Adding "see `docs/schema.sql` for the database layout" to `CLAUDE.md` so every future data-related task automatically has that reference.

## Context Relevance

Q: Why is too much context an anti-pattern?

A: Irrelevant context consumes attention and tokens, making Claude less focused on the important files and facts.

Domain: D5

Example: Pasting an entire 5,000-line vendor library into the conversation when only one function from it is actually relevant to the bug being fixed.

## Screenshots

Q: What are screenshots best for in Claude Code?

A: Communicating UI targets, visual bugs, or design changes precisely.

Domain: D5

Example: Pasting a screenshot of a misaligned button on the checkout page instead of trying to describe the pixel offset in words.

## Plan Mode

Q: When should you use plan mode?

A: Use it for multi-file, risky, architectural, or exploratory tasks where the approach should be reviewed before editing.

Domain: D3

Example: Asking Claude to "migrate authentication from sessions to JWTs" and reviewing the proposed file-by-file plan before any code changes.

## Direct Execution

Q: When is direct execution appropriate?

A: For small, clear, low-risk changes with known scope and obvious verification.

Domain: D3

Example: "Rename the `userId` parameter to `accountId` in this one function" can be done directly since the change is small and easy to check.

## Effort

Q: What does `/effort` help with?

A: It adjusts reasoning depth for difficult logic/debugging problems, not broad codebase exploration.

Domain: D4

Example: Raising effort to work through a tricky race-condition bug in a concurrency module, rather than for a simple "find all TODO comments" search.

## `ultrathink`

Q: How is `ultrathink` different from `/effort`?

A: `ultrathink` signals extra reasoning for one prompt; `/effort` adjusts session-level reasoning behavior.

Domain: D4

Example: Adding "ultrathink" to one especially hard prompt about a deadlock, versus running `/effort high` at the start of a session that will involve many hard problems.

## Plan Review

Q: Why edit a plan before approving it?

A: To correct missing constraints or implementation direction before Claude modifies files.

Domain: D3

Example: Editing a plan step that says "add a new database table" to instead say "reuse the existing `users` table" before approving it.

## Escape

Q: When should you press Escape?

A: When Claude is heading in the wrong direction, doing too much, or needs immediate redirection.

Domain: D3

Example: Pressing Escape when Claude starts rewriting an entire module instead of the single function you asked it to fix.

## `/rewind`

Q: What problem does `/rewind` solve?

A: It returns to an earlier conversation point after distracting or unhelpful turns.

Domain: D3

Example: Using `/rewind` to jump back to before an unrelated tangent about logging so the conversation can refocus on the original bug fix.

## `/compact`

Q: When should you use `/compact`?

A: When a long session contains useful learning but needs a smaller context footprint for related work.

Domain: D5

Example: After a long debugging session that uncovered how the auth module works, running `/compact` before starting related follow-up work in the same area.

## `/clear`

Q: When should you use `/clear`?

A: When starting unrelated work where old context may confuse Claude.

Domain: D5

Example: Running `/clear` after finishing a frontend styling task and before starting a completely unrelated backend database migration.

## `/resume`

Q: What does `/resume` let you do?

A: Return to a prior session after clearing or leaving it.

Domain: D3

Example: Running `/resume` the next morning to pick back up a refactor session that was closed the night before.

## Custom Commands

Q: Where do project-scoped slash commands live?

A: In `.claude/commands/`, where each markdown file becomes a slash command.

Domain: D3

Example: Creating `.claude/commands/deploy.md` makes `/deploy` available as a custom command in that project.

## Command Arguments

Q: What does `$ARGUMENTS` do in a custom command?

A: It injects the user-provided command arguments into the command prompt.

Domain: D3

Example: Running `/fix-issue 123` fills `$ARGUMENTS` with `123` inside a command template like "Fix GitHub issue #$ARGUMENTS."

## Commands vs Memory

Q: When should you choose a slash command instead of `CLAUDE.md`?

A: For repeatable on-demand workflows rather than always-loaded project standards.

Domain: D3

Example: A `/release` command that runs the build, changelog, and tag steps on demand, versus a `CLAUDE.md` rule that always applies, like "use tabs not spaces."

## MCP Server Setup

Q: What does `claude mcp add playwright npx @playwright/mcp@latest` conceptually do?

A: Registers a local Playwright MCP server so Claude Code can use browser-control tools.

Domain: D2

Example: After running that command, Claude can open a browser tab and click through a signup form to verify a UI change actually works.

## MCP Permissions

Q: Why pre-approve MCP tools locally?

A: To reduce repeated permission prompts for trusted tools, while keeping the permission decision explicit.

Domain: D2

Example: Pre-approving the Playwright `browser_click` tool once so Claude doesn't ask for confirmation on every click during a long test session.

## MCP In CI

Q: How are MCP permissions different in GitHub Actions?

A: CI requires explicit `allowed_tools` entries for every permitted tool, including MCP tools.

Domain: D2

Example: A GitHub Actions workflow must list `mcp__playwright__browser_click` in `allowed_tools`, or that MCP tool call is rejected during the run.

## GitHub Integration

Q: What does `/install-github-app` set up?

A: GitHub Actions workflows for Claude mentions in issues/PRs and automated PR reviews.

Domain: D3

Example: After installing the app, commenting "@claude fix this" on an open issue triggers a workflow that has Claude push a fix as a PR.

## GitHub Custom Instructions

Q: Why add custom instructions to a Claude GitHub Action?

A: To provide CI-specific project context, such as setup state, server URL, logs, fixtures, and tool availability.

Domain: D3

Example: Adding "the test server runs at http://localhost:4000 and is already started" so Claude doesn't waste a CI run trying to start it again.

## Hook Basics

Q: What are Claude Code hooks?

A: Commands that run around Claude Code events, especially before or after tool use.

Domain: D3

Example: A hook that runs `prettier --write` automatically every time Claude edits a `.js` file.

## PreToolUse

Q: What is PreToolUse best for?

A: Blocking or validating a proposed tool call before it executes.

Domain: D3

Example: A PreToolUse hook that blocks any Bash command containing `rm -rf` before it ever runs.

## PostToolUse

Q: What is PostToolUse best for?

A: Formatting, testing, linting, reviewing, or feeding back results after a tool call.

Domain: D3

Example: A PostToolUse hook that runs `eslint --fix` right after Claude edits any `.ts` file and reports remaining errors back to Claude.

## Hook Exit Codes

Q: What does exit code 2 mean in a PreToolUse hook?

A: Block the tool call and send stderr feedback back to Claude.

Domain: D3

Example: A hook exits with code 2 and stderr "editing `.env` is not allowed" when Claude tries to edit that file, which blocks the edit and shows Claude the message.

## Hook Input

Q: Why should hook input be logged during development?

A: Event and tool input shapes differ; logging shows which fields the hook should inspect.

Domain: D3

Example: Logging a PreToolUse event to a file reveals that a Bash call's input arrives under `tool_input.command`, which the hook script then needs to parse correctly.

## Sensitive Files

Q: Why is a Read hook alone insufficient to protect `.env`?

A: Other tools like Grep and Bash have different inputs and may still access the file unless separately blocked.

Domain: D3

Example: Blocking only the Read tool on `.env` still lets Claude run `Bash("cat .env")` to see the same secrets.

## Permissions Deny

Q: When is a permission deny rule better than a single hook?

A: When a restriction should apply uniformly across multiple tools and access paths.

Domain: D3

Example: A single permissions deny rule for `.env` blocks Read, Grep, and Bash access to it at once, instead of writing a separate hook for each tool.

## Hook Path Security

Q: Why do hook docs recommend absolute paths?

A: They reduce path interception and binary planting risks.

Domain: D3

Example: A hook calling `/usr/bin/python3 check.py` instead of bare `python3` avoids running a malicious `python3` that a compromised `PATH` might resolve to first.

## Shared Hook Settings

Q: How can a team share hook settings while using local absolute paths?

A: Commit a template such as `settings.example.json` and generate local `settings.local.json` during setup.

Domain: D3

Example: `settings.example.json` has a placeholder path like `<REPO_ROOT>/scripts/lint.sh`, and a setup script fills in each developer's actual absolute path into their own `settings.local.json`.

## Type-Check Hook

Q: What problem does a type-check PostToolUse hook solve?

A: It catches missed call sites or type errors after edits and feeds diagnostics back to Claude.

Domain: D3

Example: After Claude changes a function's return type, a PostToolUse hook running `tsc --noEmit` flags three call sites that now fail to compile, and Claude fixes them.

## Independent Review Hook

Q: Why launch a second Claude instance from a hook?

A: To review changes independently, avoiding the original generator's context bias.

Domain: D1

Example: A Stop hook spawns a fresh Claude instance with no memory of the implementation discussion to review the diff purely on its own merits, catching an edge case the original session rationalized away.

## Expensive Hooks

Q: How should expensive hooks be targeted?

A: Limit them to high-value directories or operations to control latency and API usage.

Domain: D3

Example: Running an expensive AI-review hook only on edits under `src/payments/` instead of on every file edit in the whole repo.

## Agent SDK Package

Q: Which package does the course identify as importable for Claude Code automation?

A: `@anthropic-ai/claude-agent-sdk`.

Domain: D1

Example: `import { query } from "@anthropic-ai/claude-agent-sdk"` in a Node script that automates a code-review bot.

## SDK Query

Q: What does the SDK `query` function stream?

A: JSON conversation events, including tool calls, tool results, and Claude text/result messages.

Domain: D1

Example: Iterating over the async stream from `query()` and printing each event shows a `tool_use` event for a Bash call followed by a `tool_result` event with its output.

## `allowedTools`

Q: Why pass `allowedTools` to an SDK run?

A: To enforce least privilege and keep an automation focused on only the tools it needs.

Domain: D2

Example: An SDK script that only summarizes commits passes `allowedTools: ["Bash"]` so it can run `git log` but can't accidentally edit files.

## CI Gap

Q: What CI topic is not fully covered by this course but remains exam-relevant?

A: Non-interactive `claude -p`, `--output-format json`, and `--json-schema` structured CI output.

Domain: D4

Example: A CI script running `claude -p "summarize this diff" --output-format json` to get a machine-parseable summary instead of an interactive chat.

## Path Rules Gap

Q: What Claude Code configuration topic still needs follow-up?

A: `.claude/rules/` path-scoped rule files with YAML `paths` frontmatter.

Domain: D3

Example: A rule file with `paths: ["src/api/**"]` frontmatter that only applies its guidance when Claude is working inside the `src/api` directory.
