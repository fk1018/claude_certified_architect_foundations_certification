# Claude Code in Action

- Source URL: https://anthropic-partners.skilljar.com/claude-code-in-action/303233
- Completed: 2026-07-06
- Study pack: `study_packs/claude-code-in-action/`
- Capture status: Complete. Captured the visible course outline, readable lesson bodies, accessible project-download evidence inspected temporarily in `/tmp`, and video/admin/loading pages as no-readable-content or administrative where appropriate.

## Captured Sections

| Section | Captured Evidence |
|---|---|
| Introduction | Video player only, 38 seconds. No readable instructional body or transcript visible. |
| What is a coding assistant? | Readable lesson body. Covers tool use as the bridge between language-model text and real-world coding actions. |
| Claude Code in action | Brief readable lesson body. Covers Claude Code built-in tools and multi-step tool combination. |
| Claude Code setup | Readable setup page. Covers installation entry points, `claude` CLI launch, provider setup references, and official docs links. |
| Project setup | Readable project setup page plus `uigen.zip` download inspected in `/tmp`. Covers sample app setup, Node, `npm run setup`, optional Anthropic API key, and `npm run dev`. |
| Adding context | Readable lesson body. Covers `/init`, generated `CLAUDE.md`, memory file locations, custom instructions, `@` file mentions, and referencing files such as schemas or `AGENTS.md`. |
| Making changes | Readable lesson body. Covers screenshots, `/plan`, `Shift+Tab`, plan approval, `Ctrl+G` plan editing, `/effort`, `ultrathink`, and when to use planning versus higher effort. |
| Course satisfaction survey | Survey/loading shell only. Administrative/no exam-relevant content captured. |
| Controlling context | Readable lesson body. Covers Escape interruption, `/memory`, `/rewind`, `/compact`, `/clear`, and `/resume`. |
| Custom commands | Readable lesson body. Covers `.claude/commands/`, markdown command files, command naming, `$ARGUMENTS`, automation, consistency, and project-specific workflows. |
| MCP servers with Claude Code | Readable lesson body. Covers `claude mcp add`, Playwright MCP, `.claude/settings.local.json` permissions, MCP tool naming, browser-based workflows, and MCP server selection. |
| Github integration | Readable lesson body. Covers `/install-github-app`, GitHub Actions workflows, `@claude` mentions, PR review action, custom setup, `mcp_config`, and explicit `allowed_tools`. |
| Introducing hooks | Readable lesson body. Covers PreToolUse/PostToolUse, settings scopes, `/hooks`, matchers, formatting/test/access-control hooks, and hook use cases. |
| Defining hooks | Readable lesson body plus `queries.zip` and `queries_COMPLETED.zip` inspected in `/tmp`. Covers hook design steps, JSON stdin shape, tool-specific input fields, exit codes, `.env` blocking, and downloadable sample settings. |
| Implementing a hook | Readable lesson body. Covers a PreToolUse Read hook that blocks `.env`, stderr feedback, exit code 2, and why permissions or separate matchers are needed for Grep/Bash. |
| Gotchas around hooks | Readable lesson body. Covers absolute script paths, path interception/binary planting risk, `$PWD` placeholders, `settings.example.json`, and generated `settings.local.json`. |
| Useful hooks! | Readable lesson body. Covers TypeScript type-check feedback hooks, duplicate-query prevention, second Claude Code instance review through the Agent SDK, and cost/latency tradeoffs. |
| Another useful hook | Readable lesson body. Covers additional hook events: `Notification`, `Stop`, `SubagentStop`, `PreCompact`, `UserPromptSubmit`, `SessionStart`, and `SessionEnd`; also covers logging hook inputs for schema discovery. |
| The Claude Code SDK | Readable lesson body. Covers `@anthropic-ai/claude-agent-sdk`, `query`, streamed JSON messages, tool calls/results, and `allowedTools`. |
| Quiz on Claude Code | Loading shell only. No readable quiz content or answer archive captured. |
| Summary and next steps | Page shell only. No readable instructional body captured. |

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| Domain 1: Agentic Architecture & Orchestration | Medium | Claude Code and the Agent SDK share an agentic tool loop. Hooks provide deterministic interception, second Claude instances support independent review, and SDK `allowedTools` scopes agent behavior. |
| Domain 2: Tool Design & MCP Integration | High | Covers built-in tools, MCP server installation, MCP permissions, MCP tool names, GitHub Actions MCP config, explicit allowed tools, and tool-specific hook input shapes. |
| Domain 3: Claude Code Configuration & Workflows | High | Direct coverage of setup, `CLAUDE.md`, `/init`, `/memory`, custom slash commands, plan mode, context controls, hooks, GitHub integration, and SDK use. |
| Domain 4: Prompt Engineering & Structured Output | Medium | Covers custom instructions, custom commands as reusable prompts, screenshot context, CI review customization, and independent review. Does not teach JSON schema CLI output flags. |
| Domain 5: Context Management & Reliability | High | Covers keeping context relevant, `@` file references, `/compact`, `/clear`, `/rewind`, Escape redirection, hook feedback loops, independent review, and large-project duplicate prevention. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| Coding assistant tool loop | A coding assistant turns model-generated tool requests into real file reads, edits, command execution, and tool results. The model does not read files by itself; Claude Code mediates the interaction. |
| Tool-use strength | Claude Code depends on Claude choosing and chaining tools effectively across code search, file reading, edits, tests, browser actions, and MCP-provided capabilities. |
| Built-in development tools | The exam names Read, Write, Edit, Bash, Grep, and Glob. Use Grep for content search, Glob for path patterns, Read for full context, Edit for targeted unique replacements, Write for full-file creation/replacement, and Bash for commands/tests. |
| Setup baseline | Start Claude Code in a project with `claude`. Use official install and troubleshooting docs for platform details; avoid memorizing course-specific installer text over exam task statements. |
| `/init` | Run `/init` in a new project so Claude can inspect structure and create a project-level `CLAUDE.md` with architecture, commands, and conventions. Treat it as a starting point, not a perfect source of truth. |
| `CLAUDE.md` | `CLAUDE.md` is persistent project context included in requests. It should capture project purpose, important commands, architecture, coding style, constraints, and high-value references. |
| Memory locations | The course covers shared `CLAUDE.md`, local `CLAUDE.local.md`, and user-level `~/.claude/CLAUDE.md`. The exam guide also expects knowledge of project, user, and directory-level hierarchy plus modular rule files. |
| `/memory` | Use `/memory` to inspect or edit memory/context files when behavior needs durable correction. It is useful after repeated mistakes or inconsistent project behavior. |
| `@` file references | Use `@path` in prompts to inject known-relevant files. Use durable references in `CLAUDE.md` only for high-value files that should be loaded often, such as schemas or existing agent instructions. |
| Context relevance | More context is not always better. Irrelevant files reduce attention quality. Prefer targeted references, summaries, and commands that preserve important facts while clearing clutter. |
| Screenshot context | Screenshots help communicate UI targets and visual bugs precisely. They should supplement, not replace, code/test verification. |
| Plan mode | `/plan` or `Shift+Tab` planning makes Claude explore before editing, produce a plan, and wait for approval. Use it for broad codebase exploration, multi-file work, architecture choices, and risky changes. |
| Direct execution | Direct execution fits clear, small, low-risk changes where the desired modification and affected file are known. Plan mode adds overhead when the work is simple. |
| Effort controls | `/effort` adjusts reasoning depth for a session; `ultrathink` requests extra reasoning for a single prompt. Use these for difficult logic/debugging, not as a substitute for planning broad codebase changes. |
| Plan editing | `Ctrl+G` can open a plan in an editor so the user can correct or tighten it before Claude executes. This is a control point for missed constraints. |
| Escape interruption | Press Escape when Claude goes in the wrong direction or takes on too much. Redirect to a narrower task rather than letting a low-value path consume context. |
| `/rewind` | Use `/rewind` or double Escape to jump back before distracting turns while preserving earlier useful context. Good after a bad debugging branch. |
| `/compact` | Use `/compact` when a long session contains useful project learning but needs a smaller context footprint. It preserves a summary for related follow-up work. |
| `/clear` and `/resume` | Use `/clear` for unrelated new work when old context could confuse the model. The prior session can still be reopened with `/resume`. |
| Custom slash commands | Project commands live in `.claude/commands/`; each markdown file becomes a slash command. Use them for repeatable team workflows like audits, test generation, deploy checks, or boilerplate. |
| `$ARGUMENTS` | Custom commands can accept flexible user-supplied context. This keeps one command reusable across files, features, and tasks. |
| Commands vs `CLAUDE.md` | Put always-on project standards in `CLAUDE.md`. Put repeatable, on-demand workflows in slash commands or skills. |
| MCP server integration | `claude mcp add <name> <command>` registers a local MCP server. The server exposes additional tools, such as Playwright browser control, to Claude Code. |
| MCP permissions | Local `.claude/settings.local.json` can allow MCP tools, such as `mcp__playwright`, to avoid repeated prompts. In GitHub Actions, each allowed tool must be explicitly listed. |
| MCP workflow fit | Add MCP servers when Claude needs external systems or modalities, such as browser interaction, APIs, databases, or cloud services. Prefer existing servers for standard integrations. |
| GitHub integration | `/install-github-app` sets up GitHub Actions workflows for `@claude` mention support and automated PR review. Customize environment setup, instructions, MCP config, and allowed tools. |
| CI customization | GitHub Actions examples include project setup steps, custom instructions, MCP server config, and explicit tool permissions. The course does not cover `claude -p`, `--output-format json`, or `--json-schema`. |
| Hooks | Hooks run commands around Claude Code events. PreToolUse can block or provide feedback before a tool executes; PostToolUse can format, test, analyze, or provide feedback after execution. |
| Hook settings scopes | Hooks can be configured globally, project-shared, or project-local. Use shared settings for team policy and local settings for personal machine-specific paths. |
| Hook input shape | Hook commands receive JSON on stdin. Shape differs by event and by tool. Inspect inputs before assuming field names. |
| Hook exit codes | Exit code 0 allows success. For PreToolUse, exit code 2 blocks the tool call and sends stderr feedback to Claude. PostToolUse cannot undo a completed tool call but can report problems. |
| Sensitive-file protection | A PreToolUse Read hook can block `.env`, but comprehensive protection requires separate checks for Grep/Bash or uniform permission denies because tool input fields differ. |
| Absolute path gotcha | Hook docs recommend absolute script paths for security, but absolute paths are machine-specific. A template settings file plus setup script can generate local paths safely. |
| Feedback hooks | Post-edit hooks can run formatters, type checkers, linters, or tests and feed failures back to Claude immediately. This supports test-driven and compiler-driven iteration. |
| Independent review hooks | A hook can launch a second Claude Code/SDK instance to review a proposed change for duplication or policy violations. This improves review independence but costs time and tokens. |
| Hook targeting | Monitor high-value directories and events rather than every action when expensive hooks are involved. Broad hooks can slow workflows and increase API usage. |
| Claude Agent SDK | The package `@anthropic-ai/claude-agent-sdk` exposes programmatic Claude Code behavior through `query`, streamed JSON messages, tool calls/results, MCP servers, hooks, subagents, sessions, and tool restrictions. |
| SDK tool restrictions | `allowedTools` narrows tool access for an SDK run. Use it for least privilege, predictable automation, and exam scenarios where a specialized agent should not have unrelated tools. |

## Decision Rules

- If the task is a small, known single-file change, use direct execution and verify with focused tests.
- If the task has multiple plausible approaches, touches several files, or needs codebase exploration, use plan mode before modifying files.
- If the task is logically hard but scope is known, increase `/effort` or use `ultrathink`; if scope is broad, use plan mode first.
- If Claude repeatedly makes the same project-specific mistake, add durable guidance through `/memory` or a memory file rather than repeating the correction manually.
- If a prompt needs a known file, reference it with `@path`; if that file is needed in almost every interaction, put the reference in `CLAUDE.md`.
- If context has useful project learning but is getting long, use `/compact`; if switching to unrelated work, use `/clear`.
- If a session took a bad branch, use Escape or `/rewind` to return before the distracting context.
- If a workflow is repeated by the team, create a project slash command in `.claude/commands/`; if it is personal, keep it under user scope.
- If a command must work with different inputs, use `$ARGUMENTS` and document expected argument shape in the command file.
- If Claude needs browser, API, database, or external-tool capability, add an MCP server instead of asking it to infer unavailable capabilities.
- If MCP tools run in CI, explicitly list each allowed tool; do not rely on local permission shortcuts.
- If a rule must block unsafe behavior deterministically, use hooks or permissions rather than a prompt reminder.
- If a hook is meant to prevent a tool action, use PreToolUse; if it is meant to format, test, lint, or review after an edit, use PostToolUse.
- If protecting sensitive files, account for each tool's input shape or use permission denies; a Read hook alone does not stop Bash or Grep access.
- If a hook command needs to inspect input, first add a logging helper hook to capture the event JSON shape.
- If a hook script is shared with a team, avoid committing machine-specific absolute paths; generate local settings from a template.
- If a hook launches another Claude instance, limit it to high-value paths or decisions because it adds latency and token/API cost.
- If building an SDK automation, restrict `allowedTools` to the minimum needed for the task.

## Anti-Patterns

- Treating Skilljar completed checkmarks as documentation completion.
- Reading entire large codebases up front instead of using Grep/Glob, targeted Read, and `@` references.
- Using plan mode for every tiny change, creating unnecessary overhead.
- Using higher effort to solve missing-context or broad-scope problems that should start with exploration.
- Keeping stale or distracting context alive across unrelated tasks.
- Putting every possible project detail in `CLAUDE.md`, reducing attention quality.
- Encoding a frequently repeated workflow only as a one-off prompt instead of a slash command or skill.
- Giving Claude broad MCP permissions in CI without explicitly listing allowed tools.
- Relying on prompt instructions to prevent sensitive file access when hooks/permissions are available.
- Assuming all hook events or tools send the same JSON fields.
- Using relative hook script paths without considering path interception and machine-specific execution.
- Running expensive independent-review hooks on every edit in a large repo.
- Treating PostToolUse hooks as if they can block an already executed tool call.
- Confusing the Claude Code CLI package with the importable Agent SDK package.

## Scenario Traps

- Trap: "A completed course page means the study pack can be marked done." Better: every visible required section must be reviewed and transformed into notes, flashcards, practice questions, and tracker updates.
- Trap: "The model can read files directly." Better: Claude Code exposes tools, executes requested actions, and returns results to the model.
- Trap: "More context always improves answers." Better: irrelevant context can degrade focus; target context with `@`, `CLAUDE.md`, Grep/Glob, and compacting.
- Trap: "Plan mode is only for asking permission." Better: it is for exploration, design, and approval before risky or broad changes.
- Trap: "Effort and plan mode solve the same problem." Better: effort increases reasoning depth; plan mode handles scope, exploration, and implementation design.
- Trap: "A custom command belongs in `CLAUDE.md`." Better: project slash commands belong in `.claude/commands/`; `CLAUDE.md` is persistent project guidance.
- Trap: "A local MCP permission shortcut is enough for GitHub Actions." Better: CI must explicitly list allowed tools, including MCP tools.
- Trap: "A PreToolUse hook for Read protects secrets everywhere." Better: Grep and Bash use different inputs and need separate rules or permission denies.
- Trap: "PostToolUse can block bad edits." Better: it runs after the edit; it can provide feedback or trigger follow-up fixes, not prevent the completed action.
- Trap: "The same Claude session that wrote code is the best reviewer." Better: an independent Claude instance avoids generator context bias.
- Trap: "Hook scripts can assume stable JSON schemas." Better: event and tool input shapes differ; log and inspect before implementing assumptions.
- Trap: "CI review is covered because GitHub Actions integration was shown." Better: the course covers Actions workflow customization, but not all exam CLI flags for structured CI output.

## Memorization Cues

- Tool cue: Grep finds text; Glob finds paths; Read gets context; Edit changes unique text; Write replaces/creates; Bash verifies.
- Context cue: `@` for known file now; `CLAUDE.md` for recurring project context.
- Session cue: Escape redirects, `/rewind` backs up, `/compact` compresses, `/clear` starts fresh, `/resume` returns.
- Planning cue: plan for breadth, effort for depth.
- Command cue: `.claude/commands/<name>.md` becomes `/<name>`.
- Argument cue: `$ARGUMENTS` makes one slash command reusable.
- MCP cue: add capability with `claude mcp add`; allow local tools carefully; enumerate CI tools explicitly.
- Hook cue: Pre blocks; Post reacts.
- Hook JSON cue: event shape plus tool shape; inspect before coding.
- Security cue: prompt asks, hook enforces, permissions deny.
- SDK cue: `query` streams events; `allowedTools` limits reach.

## Source References

- `Introduction`: video player only, no readable body.
- `What is a coding assistant?`: tool-use flow, context gathering, planning, action, and why Claude Code tool use matters.
- `Claude Code in action`: built-in tools and multi-step task execution.
- `Claude Code setup`: install/launch references and provider setup context.
- `Project setup`: sample UI generation app setup; `uigen.zip` inspected in `/tmp` only.
- `Adding context`: `/init`, `CLAUDE.md`, memory locations, custom instructions, `@` file references, schema/`AGENTS.md` references.
- `Making changes`: screenshots, `/plan`, plan review/editing, `/effort`, `ultrathink`, breadth-vs-depth decision.
- `Course satisfaction survey`: administrative/loading page only.
- `Controlling context`: Escape, `/memory`, `/rewind`, `/compact`, `/clear`, `/resume`.
- `Custom commands`: `.claude/commands/`, markdown command files, `$ARGUMENTS`, audit/test command examples.
- `MCP servers with Claude Code`: Playwright MCP install, local permissions, browser-based prompt improvement workflow, MCP server ecosystem.
- `Github integration`: `/install-github-app`, issue/PR mention action, PR review action, workflow customization, `mcp_config`, `allowed_tools`.
- `Introducing hooks`: hook event timing, settings scopes, `/hooks`, PreToolUse/PostToolUse examples.
- `Defining hooks`: hook build steps, stdin JSON, exit codes, Read/Grep/Bash input differences, downloads.
- `Implementing a hook`: `.env` Read-blocking hook and permission-deny caveat.
- `Gotchas around hooks`: absolute path security, `$PWD` placeholders, generated `settings.local.json`.
- `Useful hooks!`: type-check feedback, duplicate query review, independent Claude instance review, targeting/cost tradeoffs.
- `Another useful hook`: additional hook events and logging helper pattern.
- `The Claude Code SDK`: importable Agent SDK, streamed messages, tool calls/results, `allowedTools`.
- `Quiz on Claude Code`: loading shell only; no raw quiz content captured.
- `Summary and next steps`: no readable instructional body captured.
- Downloaded assets inspected temporarily: `uigen.zip`, `queries.zip`, `queries_COMPLETED.zip`; no raw archives stored in repo.

## Gaps / Follow-Up

- This course substantially improves Claude Code workflow coverage but does not fully cover path-specific rules in `.claude/rules/` with YAML `paths` frontmatter.
- This course covers GitHub Actions integration but not the exam guide's `claude -p`, `--output-format json`, or `--json-schema` CLI flags for structured CI output.
- This course covers Claude Code hooks, but not full Agent SDK coordinator/subagent orchestration, `Task` spawning, session forking, or production handoff patterns.
- This course introduces MCP server setup in Claude Code, but not full project `.mcp.json` versus user `~/.claude.json` credential mechanics from the exam guide.
- This course does not cover Message Batches API, extraction-specific retry loops, or structured data extraction beyond code-review workflow relevance.
