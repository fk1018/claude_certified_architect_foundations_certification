# Claude Code, MCP & Integration Flashcards

## Permission Modes

Q: What does `default` permission mode auto-approve, and what does it always gate?

A: It auto-approves reads only; it prompts before nearly every file edit or shell command.

Domain: D3

Example: A developer opens an unfamiliar repo in default mode; Claude Code can read every file freely but must ask before saving any change or running any command.

Q: What does `acceptEdits` mode auto-approve that `default` mode does not, and what is the important limitation?

A: It auto-approves reads, file edits, and common filesystem commands (mkdir, touch, rm, rmdir, mv, cp, sed) inside the working directory; auto-approval is scoped to the working directory, protected paths still prompt, and it is not appropriate if the agent needs to run other scripts.

Domain: D3

Example: In acceptEdits mode, Claude Code can silently run `rm old_file.ts` inside the project folder, but a script invocation outside auto-approved commands still requires confirmation.

Q: What does `plan` mode do, and when is it the right default?

A: It auto-approves reads only, researches and proposes a plan, and blocks all file edits and shell commands until you approve the plan; it's the right default for exploration and planning on sensitive or unfamiliar codebases.

Domain: D3

Example: Before a risky database refactor, a team switches to plan mode so Claude Code explains its intended changes before touching a single file.

Q: How does `auto` mode differ from `bypassPermissions`?

A: `auto` auto-approves everything but runs a separate classifier that blocks actions escalating beyond the request, targeting unrecognized infrastructure, or driven by hostile content — and it still blocks production deploys, mass deletes, credential exfiltration, and force-push to main by default. `bypassPermissions` approves everything with no classifier and no safety checks except a last-resort prompt on catastrophic deletes.

Domain: D3

Example: In auto mode, an unexpected attempt to force-push to main is still blocked; in bypassPermissions, the same push would go through without a prompt.

Q: What does `dontAsk` mode do, and what is it built for?

A: It only auto-approves tools you've pre-approved in an allow rule plus read-only commands; everything else is auto-denied with no confirmation queue. It's built for locked-down CI and scripts, not for reducing friction on local interactive work.

Domain: D3

Example: A CI pipeline runs Claude Code in dontAsk mode with only `Bash(npm test:*)` allow-listed; any other command is denied outright rather than queued for approval.

Q: What does `bypassPermissions` mode uniquely remove compared to every other mode?

A: It removes the protected-path guard that all other modes keep, in addition to all confirmation prompts; only catastrophic commands like `rm -rf /` or `rm -rf ~` still trigger a last-resort prompt.

Domain: D3

Example: In bypassPermissions, a script that unexpectedly matches files in a repo's own `.claude/` configuration directory can overwrite them with no prompt, something that would still prompt under acceptEdits.

Q: In the bypassPermissions incident from this module, what specifically caused the production configuration files to be deleted?

A: A cleanup script matched a broader file pattern (`/v1/legacy/`) than the developer intended, hitting files in `/deploy/config/prod/` as well as `/src/`; with bypassPermissions active, the script invocation ran with no confirmation prompt to catch the mismatch.

Domain: D7

Example: A "safe" renaming task deletes production endpoint overrides because the developer assumed the pattern only matched their intended source directory.

## Human Gates and Governance

Q: What single question should decide where a human review gate sits, independent of which permission mode is active?

A: What is the worst outcome if this action runs without a person checking it first? Low-cost, reversible actions can pass without a gate; high-cost, hard-to-undo, or sensitive-path actions need one.

Domain: D7

Example: A formatting-only edit inside the working directory needs no gate; a write to a shared deployment configuration file that several production services read does need one.

Q: For code the team has marked as sensitive, what is the rule about the agent's own review?

A: The agent's work is an input to a human decision, never a replacement for one — a person must review the change before it merges no matter how confident the agent's review sounds.

Domain: D7

Example: Even if Claude Code reports high confidence that a payments-module change is correct, a human still reviews and approves it before merge.

Q: What always wins when an allow rule and a deny rule conflict, regardless of the active permission mode?

A: A deny rule always wins over an allow rule.

Domain: D3

Example: Even in `auto` mode with a broad allow rule for Bash commands, a project-level deny rule on `Bash(rm:*)` still blocks that command.

Q: Why is an enterprise-level deny rule considered the most durable governance control?

A: It cannot be overridden or removed by any individual developer or project file, and it applies even when a bypass mode is set.

Domain: D3

Example: An org sets an enterprise deny rule blocking reads of `.env.production`; no developer can override that rule locally, even by switching to bypassPermissions.

Q: Where do the four settings scopes live, and what is each one's intended use?

A: User (~/.claude/settings.json) — machine-wide personal preferences. Project (.claude/settings.json, committed) — team-wide conventions shared via the repo. Local (.claude/settings.local.json, gitignored) — personal overrides for one project. Enterprise (managed-settings.json, admin-controlled) — org-wide security controls that cannot be overridden.

Domain: D3

Example: A developer's preferred default mode goes in their user settings; a deny rule blocking edits to environment files across the whole org goes in enterprise managed settings.

## CLAUDE.md and Rules Files

Q: When does CLAUDE.md load, and what should it hold?

A: It's read at the start of every Claude Code session in a project directory and appended to the prompt before any user message; it should hold universal, session-critical constraints — testing commands, framework conventions, off-limits paths, and style decisions that differ from defaults.

Domain: D3

Example: A CLAUDE.md line saying "never modify the database schema" applies to every session because it's a universal constraint.

Q: What is the main failure mode of CLAUDE.md, and why does it happen?

A: Dilution — every line added reduces the effective weight of every other line, because a larger file consumes more of the context window, making any single instruction a smaller fraction of what loads.

Domain: D6

Example: In an 847-line CLAUDE.md containing a historical decisions log, a critical path restriction on line 347 gets violated because the surrounding 846 lines diluted its weight.

Q: In the diluted-CLAUDE.md incident, was the failure that the rule was missing from the file?

A: No — the rule was present and the agent had access to it; the failure was that hundreds of other lines (historical decisions, archived notes) reduced its effective weight until it stopped reliably landing.

Domain: D6

Example: The fix isn't adding the rule again — it's removing the historical log and archived notes from CLAUDE.md and keeping only session-critical rules.

Q: How does a rules instruction file differ from CLAUDE.md in scope and location?

A: Rules files live in .claude/rules/ and can be scoped to specific paths using a `paths` glob in YAML frontmatter, entering context only when Claude works with matching files — CLAUDE.md is always on for every session.

Domain: D3

Example: A rule that "all SQL in the database module must include an explicit transaction boundary" lives in .claude/rules/database.md scoped to `src/db/**/*.sql`, instead of cluttering every session via CLAUDE.md.

Q: If a rules file is placed inside a subdirectory like .claude/rules/database/ but has no `paths` field in its frontmatter, how does it behave?

A: It loads unconditionally at session start, with the same priority as CLAUDE.md — directory placement is organizational only; scoping comes exclusively from the `paths` field in frontmatter.

Domain: D3

Example: A rules file sitting in .claude/rules/database/ without a `paths` key still loads for every session touching any part of the project, not just database files.

## Hooks

Q: Why does a hook enforce a rule more reliably than a CLAUDE.md instruction telling the agent to do the same thing?

A: A CLAUDE.md instruction is followed most of the time but depends on the model's decision; a hook fires independently of what the model decides, at the configured lifecycle event, every single time.

Domain: D3

Example: Telling the agent in CLAUDE.md to "run Prettier after every edit" works most of the time; a PostToolUse hook running Prettier after every edit works every time.

Q: What makes PreToolUse the only hook event that can block a tool call, and how does it signal the block?

A: It runs before the tool call executes, so it can inspect the call and exit with code 2 to block it, writing the reason to stderr as feedback the agent sees.

Domain: D3

Example: A PreToolUse hook checks whether a Read call targets `.env.production` and exits with code 2 to block it, sending the reason back to the agent.

Q: Why can't a PostToolUse hook block the action it's attached to, and what is it good for instead?

A: It runs after the tool call has already completed, so blocking is impossible; it's the right place for automated side effects like running a formatter, triggering tests, or logging an operation for an audit trail.

Domain: D3

Example: A PostToolUse hook logs every MCP tool call and its parameters to an audit store for a compliance review, after each call completes.

Q: What do the UserPromptSubmit, Stop, SessionStart, and SessionEnd hook events each fire on?

A: UserPromptSubmit fires when a prompt is submitted, before the model processes it (inject context or validate the request). Stop fires when the model finishes responding (notifications, cleanup, committing an audit log). SessionStart fires when a session starts or resumes (initialize state, validate env vars, confirm services are reachable). SessionEnd fires when a session ends (teardown, final audit writes, closing notifications).

Domain: D3

Example: A SessionStart hook checks that a required API key environment variable is set before the agent begins work; a SessionEnd hook writes a final audit summary when the session closes.

Q: What two layers does the module recommend to stop an agent from writing credential values inline to .mcp.json?

A: A CLAUDE.md convention instruction stating credentials must never be written inline (signals intent each session), backed by a PreToolUse hook that inspects write/edit operations against .mcp.json for credential-shaped patterns and blocks with exit code 2 if found (enforces it deterministically).

Domain: D7

Example: Even if the model forgets the CLAUDE.md convention under context pressure, the PreToolUse hook still blocks an inline `Bearer sk-...` value from being written to .mcp.json.

## Subagents

Q: What context does a subagent inherit from the main session when it's dispatched a task?

A: None of the main conversation history, accumulated files, or session state — it starts from a clean slate, does the work, and returns only its output.

Domain: D1

Example: Delegating a large exploration task to a subagent keeps the main session's context window from filling up with the subagent's intermediate file reads.

Q: Why might a rule from CLAUDE.md fail to apply when a task is delegated to the built-in Explore or Plan subagent?

A: The Explore and Plan built-in subagents skip loading CLAUDE.md and git status to keep research fast and cheap, so project-level rules defined there are simply not in their context when they run.

Domain: D1

Example: A CLAUDE.md rule saying "never touch /legacy/" won't be honored by the Explore subagent because it never loaded CLAUDE.md in the first place; use general-purpose or a custom subagent instead when that constraint matters.

Q: Do custom subagents automatically have access to the skills defined in the project?

A: No — a custom subagent (.claude/agents) must explicitly list any skill it needs in its own frontmatter; built-in agents do not have preloaded skills either.

Domain: D1

Example: A custom code-review subagent that needs a "style-check" skill must list that skill explicitly in its agent definition, or it won't see it.

## Skills Across Runtimes

Q: What is the difference between how a skill loads in Claude Code versus the Messages API?

A: In Claude Code, a skill is discovered from .claude/skills on the filesystem and loads on description match or explicit invocation, running locally under the active permission mode. On the Messages API, the skill is sent with the request and runs inside Anthropic's code-execution container (requiring code-execution and skills beta headers), not on your machine or against your local files.

Domain: D2

Example: A skill that shells out to a local `git` command works fine in Claude Code but fails on the Messages API, because the container it runs in has no access to your local git installation.

Q: How does skill loading work under the Agent SDK, and what is the "common surprise" the module warns about?

A: Whether filesystem settings (CLAUDE.md, skills) load is controlled by the settingSources (TypeScript) / setting_sources (Python) configuration, which must be set explicitly rather than relied on as a default. The common surprise: a skill that worked fine in Claude Code does nothing under the SDK because settingSources was never set, so the skill never loaded.

Domain: D2

Example: A team ports a Claude Code skill to an Agent SDK-based automation and it silently never triggers, because settingSources was left unset.

Q: How do Claude Managed Agents load skills, and what compliance limitation currently applies to them?

A: Skills are attached when defining the agent as an API resource (requiring the managed-agents-2026-04-01 beta header) — there's no filesystem discovery step, and the skill runs in an Anthropic-provisioned sandbox. Sessions are stored server-side, so Managed Agents are not currently eligible for Zero Data Retention or HIPAA BAA coverage.

Domain: D2

Example: A healthcare team evaluating Claude Managed Agents for a HIPAA-covered workflow needs to know this limitation before committing to that runtime.

Q: What are the three portability rules for writing a skill that must run cleanly across multiple runtimes?

A: (1) Write the description as the matching criterion, since a vague description fails to load in every runtime. (2) Don't assume a local filesystem or local tools exist in the skill body — this breaks on the Messages API's container. (3) Remember subagents don't inherit skills automatically in any runtime — list them explicitly for the subagent.

Domain: D2

Example: A well-written skill description like "Validates a deployment configuration against the team's staging checklist before release" gives every runtime's matching logic something concrete to compare a request against.

Q: What is the difference between a skill and the older custom command format in current Claude Code?

A: Skills are the current recommended format for both explicit invocation (/skill-name) and automatic invocation (description match); the older .claude/commands/ directory format still works but is legacy. Use `disable-model-invocation: true` in a skill's frontmatter for a workflow that should only run when explicitly called.

Domain: D3

Example: A team migrating an old custom command to a skill sets `disable-model-invocation: true` so it only runs via explicit `/deploy-check` invocation, never automatically.

## Plugins and Packaging

Q: What does a plugin bundle, and how does it get distributed?

A: A plugin bundles skills, hooks, subagents, and MCP servers into a single installable unit, distributed through a marketplace — a catalog of plugins someone has created and shared, added via `/plugin marketplace add <owner/repo>`.

Domain: D3

Example: A team packages their deployment skill, its audit-logging hook, and a connected MCP server into one plugin so every new hire runs one install command instead of following a setup doc.

Q: How are plugin commands namespaced, and what does that imply for renaming a plugin?

A: The plugin's name becomes the command prefix — a `run-tests` command in a plugin named `payments` is invoked as `/payments:run-tests`. Renaming the plugin renames all of its commands, since the name is part of the interface.

Domain: D3

Example: Two different plugins can both ship a `run-tests` command without colliding, because one is `/payments:run-tests` and the other is `/billing:run-tests`.

Q: In the broken-plugin incident, what was the defect in the SKILL.md, and what is the correct fix?

A: The defect was an absolute path (`/Users/alexmorgan/projects/deploy-utils/validate.sh`) hardcoded in the skill's steps, which existed only on the author's machine. The correct fix is to reference the script from the project root using `$CLAUDE_PROJECT_DIR` (or `${CLAUDE_PLUGIN_ROOT}` if the script ships inside the plugin itself) so it resolves on any machine.

Domain: D3

Example: Replacing `/Users/alexmorgan/projects/deploy-utils/validate.sh` with `$CLAUDE_PROJECT_DIR/deploy-utils/validate.sh` lets every teammate's clone resolve the script correctly.

Q: Why did the deployment-workflow plugin fail for every teammate except its author, even though installation succeeded for everyone?

A: Installation only copies files into place and always succeeds if the package is assembled correctly; execution resolves paths and environment variables against the machine actually running it. The plugin's absolute path and an undocumented environment variable (DEPLOY_TOKEN) both existed only on the author's machine, so execution failed everywhere else.

Domain: D3

Example: Three teammates spent two hours debugging a skill failure before tracing it to a DEPLOY_TOKEN environment variable the README never mentioned.

Q: Does a distributed plugin automatically carry over a deny rule or hook the author relied on locally for safety?

A: No — a deny rule or hook the author relied on locally is not included in a plugin bundle unless it is explicitly listed as part of that bundle. If the local guardrail isn't packaged, the protection does not carry over to a teammate's install.

Domain: D7

Example: An author who protected a sensitive path with a personal local deny rule must explicitly add that deny rule to the plugin's settings component, or teammates who install the plugin get no such protection.

Q: What does a managed marketplace allowlist control, and what additional setting is needed to push a marketplace to all users automatically?

A: The allowlist gates which marketplace sources users are permitted to add, but it does not register marketplaces automatically. Pairing it with `extraKnownMarketplaces` in managed settings pushes a marketplace to all users without requiring them to run the add command themselves.

Domain: D3

Example: An org sets an allowlist restricting marketplace sources to internal repos, then uses extraKnownMarketplaces so every developer already has the internal marketplace registered on first launch.

## MCP Fundamentals

Q: What problem does an MCP server solve that wiring a tool directly into an application does not?

A: MCP separates tool definitions from individual applications into a standalone server process; instead of each of three applications maintaining its own integration to an external service, the capability is built once and every MCP client that connects gets access without re-implementing it.

Domain: D8

Example: A GitHub MCP server is built once and used by Claude Code, a CI bot, and an internal dashboard, instead of each maintaining its own GitHub API integration.

Q: What are the three things an MCP server can expose, and how does a resource differ from a tool?

A: Tools, resources, and prompts. A tool is an action the model calls; a resource is read-only data the client fetches and places directly into context, rather than the model calling a tool to retrieve it.

Domain: D8

Example: A list of available documents can be exposed as a direct resource with a fixed address, so it's in context from the start of a turn rather than requiring a tool call to fetch it.

Q: What is the difference between a direct resource and a templated resource?

A: A direct resource has a fixed address for data that takes no parameters (e.g. a document list); a templated resource puts a parameter in the address (e.g. a document address that takes a document identifier).

Domain: D8

Example: `documents://list` might be a direct resource, while `documents://{doc_id}` is a templated resource requiring a specific ID.

Q: What is an MCP prompt, and when is it worth exposing one?

A: A pre-written instruction template the server exposes so a client can invoke a vetted prompt by name instead of each user writing their own wording. It's worth it when carefully engineered wording produces materially better results than typical user phrasing, and you want every connected client to get the same quality.

Domain: D8

Example: A server exposes a "generate-incident-report" prompt with carefully tuned wording so every team using the server gets consistently well-structured incident reports.

## MCP Transport, Scope, and Context Cost

Q: When should you use stdio transport versus HTTP transport for an MCP server?

A: stdio runs the server as a local subprocess on the same machine as the client, communicating over stdin/stdout — correct for a local tool, personal script, or your own dev server, but it can't be shared across a team or hosted remotely. HTTP is the recommended transport for any server that doesn't run locally — you provide a URL and the client connects over the network, used for shared team servers and hosted integrations.

Domain: D8

Example: A personal SQLite query tool you use only on your own machine uses stdio; a company-hosted code search service the whole team accesses uses HTTP.

Q: Is SSE (Server-Sent Events) a currently recommended MCP transport?

A: No — SSE predates the current HTTP transport, has been superseded by it, and is no longer recommended for new servers; treat it as legacy if you encounter it in existing configuration.

Domain: D8

Example: An old MCP config referencing SSE transport should be migrated to HTTP transport rather than used as a template for a new server.

Q: What are the four MCP configuration scopes, and what does each control?

A: Local (~/.claude.json under the current project path — personal, applies only to that project, not shared). User (personal Claude settings — applies across all your projects, still not shared with teammates). Project (.mcp.json at repo root — committing it gives every clone the same server automatically). Enterprise (centrally managed by an administrator — pushed to all org users without individual configuration).

Domain: D8

Example: A personal database utility you use in every project goes in User scope; a server the whole engineering team needs goes in Project scope via a committed .mcp.json.

Q: For a project-scoped stdio MCP server committed to .mcp.json, what does each teammate's install actually require?

A: A project-scoped server still runs from each teammate's own machine — for a stdio server, the committed configuration stores the launch command, and every clone spawns its own local subprocess, so each teammate needs the runtime (e.g. Node for an npx-launched server) installed locally.

Domain: D8

Example: Committing a Node-based stdio MCP server to .mcp.json doesn't mean teammates skip installing Node — each of their machines still launches its own subprocess.

Q: By default, does Claude Code load every connected MCP server's tool definitions into context up front?

A: No — by default it defers these definitions and uses a search step to discover and load only the tools relevant to the current task; an opt-in mode loads definitions upfront only when they fit within roughly 10% of the context window, deferring past that limit.

Domain: D5

Example: Connecting five MCP servers doesn't mean all their tool definitions occupy context at session start — only the ones a given task actually calls for get loaded.

Q: What is the difference between a permission rule targeting `mcp__github__create_issue` and the API's `mcp_toolset` enabled flag for the same tool?

A: A permission rule is a governance control deciding whether an exposed tool may run (an allow rule lets it run without a prompt; a deny rule blocks it, and deny always overrides allow). The `enabled` flag on an `mcp_toolset` object is a context-cost/scope control deciding whether the model sees the tool at all.

Domain: D7

Example: You might disable a rarely-used GitHub tool via `enabled: false` to keep it out of context entirely, while separately using a deny rule to block a different tool the model can see but shouldn't run without approval.

## Prompt Caching and RAG

Q: How do you mark a prompt caching breakpoint, and what does it cache?

A: You add a `cache_control` field of type `ephemeral` to the last block you want cached; this caches everything up to and including that block. Up to four breakpoints are allowed, and requests process in a fixed order (tools, system prompt, messages), so a breakpoint after the tools caches the tool definitions while keeping messages dynamic.

Domain: D5

Example: Placing a cache breakpoint right after a large set of tool definitions lets follow-up requests reuse that cached prefix at a fraction of the cost while the conversation's messages stay fresh.

Q: What are the two cache lifetime options, and when does the 1-hour option make sense over the 5-minute default?

A: The default cache lifetime is 5 minutes from the last read (each read resets the clock); an opt-in 1-hour lifetime is set via a `ttl` of `1h` on the breakpoint. The 1-hour option suits workloads with longer gaps between requests, such as an agent that pauses between steps, where the 5-minute window would expire before the next request arrives.

Domain: D5

Example: An agent that only checks back in every 20 minutes between long-running steps should use the 1-hour TTL, or it pays the write cost again every time with no read benefit.

Q: What is the minimum token threshold for prompt caching to apply?

A: Roughly 1,024 tokens for most current models — short prompts below that threshold won't be cached even if a breakpoint is set.

Domain: D5

Example: A tiny 200-token system prompt with a cache breakpoint still gets reprocessed from scratch every time, because it's below the minimum caching threshold.

Q: What is the fundamental difference in timing between classical RAG and agentic search?

A: Classical RAG does the indexing work upfront — source material is chunked and embedded into a vector database before any question is asked, then a query is matched against that pre-built index. Agentic search has no pre-built index — the model figures out what it needs at the moment of the request and fetches it live.

Domain: D6

Example: Claude Code's on-demand discovery of MCP tool definitions, only loading the ones a task needs, is an example of agentic search rather than a pre-indexed retrieval system.

Q: What are the two properties of retrieval worth understanding regardless of which RAG approach is used?

A: It scales — cost per request stays roughly flat as source material grows, since the model only receives the relevant slice. It's only as good as what it finds — if retrieval misses the needed document, the model never sees it, so descriptive naming and good organization of source material materially improve results.

Domain: D6

Example: A file named "Q3 refund policy, updated August 2024" surfaces reliably in retrieval, while a file named "notes_final_v3.pdf" is much harder for the same retrieval step to find.

## Authentication and Secrets

Q: When should an MCP integration use OAuth versus an API key in an environment variable?

A: Use OAuth for remote services where the service's authorization model is tied to individual user identity (the server returns 401 Unauthorized, the client opens a browser sign-in flow, a token is issued and stored automatically). Use an API key passed through an environment variable for remote services with service identity, where the key identifies a service account rather than a person.

Domain: D8

Example: The Linear MCP server uses OAuth because access is tied to each user's own Linear account; the GitHub MCP server in this module's example authenticates with a personal access token as a service-style credential instead.

Q: What is the security boundary for a local MCP service reached over stdio with no network authentication?

A: The file-system permission model is the security boundary — a deny rule in the settings files is the governance layer, since there's no network credential involved at all.

Domain: D7

Example: A local SQLite MCP tool doesn't need an API key; instead, a deny rule prevents the agent from reading a sensitive local file the tool could otherwise touch.

Q: Why doesn't committing a "temporary" fix that moves a leaked API key to an environment variable actually resolve the exposure?

A: The key remains in the repository's commit history even after being removed from the current version of the file; overwriting a file in a later commit does not remove earlier commits' contents. The key must be treated as compromised and rotated.

Domain: D7

Example: After moving a leaked key to an environment variable and committing the corrected .mcp.json, the old key is still recoverable from git history until the service account credential is rotated.

Q: What are the three practices for managing a secret after choosing an authentication pattern, and what does each address?

A: Separation — the config file holds only a variable reference, never the value, because configs get committed/shared/cloned. Storage location — an environment variable suits a value local to one machine/pipeline run, while a secret store (a managed service returning credentials to authorized callers and recording who read what) suits values shared across services or people. Rotation — replacing a credential on a schedule and immediately after any suspected exposure, since a leaked key cannot be made secret again.

Domain: D7

Example: A CI pipeline injects a secret as an environment variable per run (storage location), while a service credential shared across five microservices lives in a central secret store so one rotation updates every consumer at once.

Q: Why is rotation "the only appropriate response" to a leaked credential, according to this module?

A: Because a key that has been exposed cannot be made secret again — you must issue a new one; simply moving the value's storage location afterward does nothing to invalidate the already-exposed value.

Domain: D7

Example: After discovering an inline API key was committed and cloned by three teammates and a CI runner, the only fix that actually closes the exposure is rotating the service account's key.

## Enterprise Integration

Q: What four questions does a production enterprise integration need to answer that a working prototype typically ignores?

A: Who is the model acting as, and is that identity auditable? What data can it access, and where does that data leave the organization? Can an administrator lock the configuration so no individual developer can change the authentication setup? Can access be logged in a way that satisfies a compliance audit?

Domain: D7

Example: A prototype MCP connection to a data warehouse "just works," but before a regulated customer accepts it, the team must also show who the connection authenticates as and how every access gets logged.

Q: Why did an OAuth-authenticated MCP connection that worked perfectly in staging fail entirely once moved to production?

A: OAuth redirect URIs are registered per host, and the OAuth app registration only listed the staging host — the production host was never added to the allowed redirect URI list, so every production sign-in attempt failed the URI match and looped back to the sign-in screen.

Domain: D8

Example: A team that tested an OAuth MCP integration thoroughly in staging still has to explicitly add the production hostname's redirect URI to the OAuth app registration before the production connection will work.

Q: Beyond adding the production redirect URI, what does the module say many regulated enterprise customers additionally require?

A: Separate OAuth app registrations for each environment (staging and production), rather than reusing one app registration with multiple redirect URIs, as part of their security policy.

Domain: D7

Example: A security reviewer flags that the same OAuth app was used across staging and production and asks the team to register a distinct app for each, per company policy.

Q: What hook and configuration mechanism together answer the compliance "logging" and "configuration lock" questions for a regulated deployment?

A: A PostToolUse hook that logs every tool call and its parameters to an audit store answers the logging question, firing deterministically regardless of what the model decides. An administrator-deployed enterprise managed configuration that individual users and project files cannot override answers the configuration-lock question.

Domain: D7

Example: A compliance reviewer asks whether a developer could quietly change the auth setup during an audit window; the answer is no, because it's locked at the enterprise managed-settings level.

Q: What three scoping questions should be answered before starting a high-risk code modernization session, and why does this task type surface them clearly?

A: What is the blast radius if something goes wrong (which systems depend on the code, what breaks downstream)? How are changes audited (is there a PostToolUse hook, and does its log satisfy the reviewer)? Who approves each phase before the next begins? Modernization surfaces these clearly because the scope is large, the codebase is unfamiliar, and the cost of a wrong edit is high — but the questions apply to any high-risk agentic task.

Domain: D7

Example: Before letting Claude Code modernize a legacy billing module, the team documents which downstream services depend on it, confirms a PostToolUse audit hook is active, and defines who signs off between the plan and code phases.

## Exam Traps and Trust Calibration

Q: What is the correct way to treat an AI code reviewer's finding about a missing null check versus its claim about a runtime race condition?

A: Trust findings the reviewer can prove directly from the diff in front of it (like a missing null check or unclosed resource) and verify them on the cited lines. Treat any claim about runtime behavior or another system as an unproven hypothesis to test, since the reviewer made that claim without evidence that would actually prove it.

Domain: D4

Example: A reviewer flagging "this resource is never closed" on a visible code path is easy to confirm by reading the diff; a reviewer claiming "this will deadlock under high concurrency" needs independent testing before you act on it.

Q: In the Cumulative Integration Task, the settings.json set `defaultMode: "bypassPermissions"` alongside a deny rule blocking `Read(.env.production)`. Why is this combination still broken?

A: bypassPermissions removes standard permission checks including the protected-path guard the other modes keep; relying on a deny rule to protect a sensitive read while running in a mode designed to bypass exactly that kind of check is an unreliable combination — the safer fix is a less permissive default mode (or ensuring deny rules are the enforcement layer administrators, not developers, control).

Domain: D3

Example: A reviewer catching this bug would flag that bypassPermissions is fundamentally the wrong mode for a refactor that has ANY file the agent must never read, regardless of what deny rules are also present.
