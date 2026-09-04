# Claude Code, MCP & Integration Practice Questions

## Question 1

Scenario: A developer is three days into a codebase cleanup that has gone smoothly. Tired of confirming every prompt, they switch Claude Code to `bypassPermissions` and ask it to rename all references matching the pattern `/v1/legacy/`. The pattern unexpectedly also matches files in `/deploy/config/prod/`, and those files get deleted with no confirmation.

Question: What is the most accurate explanation of why nothing caught this before the deletion happened?

A. `acceptEdits` mode was active, and it does not gate `rm` commands inside the working directory.

B. `bypassPermissions` removes all confirmation prompts and also removes the protected-path guard that every other mode keeps.

C. The classifier in `auto` mode failed to recognize the production directory as sensitive infrastructure.

D. The deny rule on `/deploy/config/prod/` was overridden by an allow rule in project settings.

Correct answer: B

Explanation: The scenario explicitly describes `bypassPermissions` mode. Unlike every other mode, it skips both confirmation prompts and the protected-path guard that the other modes retain, so a broader-than-intended file match had nothing to stop it before deletion.

Distractors:
- A: The scenario states `bypassPermissions` was active, not `acceptEdits` — this describes a different (though also risky) mode.
- C: `auto` mode was not in use here; the scenario never mentions a classifier.
- D: No deny/allow rule conflict is described — the failure is the complete absence of any gate under bypass mode, not a rule-precedence issue.

## Question 2

Scenario: A team's CLAUDE.md has grown to 847 lines over two months, including a historical decisions log and archived notes. A path restriction on line 347 ("Do not modify files in /legacy/tokens/") is present in the file, but Claude Code edits a file in that directory anyway during a refactor.

Question: What is the best diagnosis and fix?

A. The rule was missing from CLAUDE.md; add it back and the problem is resolved.

B. CLAUDE.md dilutes with size — the fix is to move historical and archived content out, keeping only session-critical rules, and consider a hook for the one rule that must never be violated.

C. CLAUDE.md doesn't support path restrictions; move the rule to a rules file instead, since rules files are the only mechanism that can express "do not modify."

D. The agent ignored CLAUDE.md entirely because the file exceeded a hard size limit and failed to load.

Correct answer: B

Explanation: The rule was present and loaded; the failure was dilution, where hundreds of unrelated lines reduced the effective weight of the one instruction that mattered. The fix is to prune CLAUDE.md to session-critical content and consider backing a must-never-violate rule with a deterministic hook.

Distractors:
- A: The scenario states the rule was present in the file at line 347 — it wasn't missing.
- C: CLAUDE.md and rules files can both express path-based instructions; the issue here is dilution, not an inherent limitation of CLAUDE.md's syntax.
- D: The module describes dilution as a gradual weighting problem, not a hard file-size cutoff that fails to load; there's no evidence in the scenario that the file failed to load at all.

## Question 3

Scenario: A team wants a hook that reliably blocks reads of `.env.production` every single time, regardless of what the model decides mid-session.

Question: Which hook event and command behavior correctly implements this?

A. A PostToolUse hook that logs the read attempt and exits with code 0.

B. A PreToolUse hook that inspects the tool call, and exits with code 2 (writing the reason to stderr) when the path is `.env.production`.

C. A UserPromptSubmit hook that warns the user in the prompt but allows the read to proceed.

D. A Stop hook that reports the violation after the model finishes responding.

Correct answer: B

Explanation: PreToolUse is the only event that runs before the tool call executes, making it the only one capable of blocking it. Exiting with code 2 blocks the call and surfaces the reason to the agent via stderr.

Distractors:
- A: PostToolUse fires after the call has already completed, so it cannot block the read — it can only log or react afterward.
- C: UserPromptSubmit fires on prompt submission, before any tool call is even proposed, and does not gate a specific tool call from occurring.
- D: Stop fires after the model finishes its turn, long after any read would have already happened — it cannot prevent the read.

## Question 4

Scenario: A team packages a deployment-validation skill and a related hook into a plugin, tests it thoroughly on the author's machine, and distributes it through the internal marketplace. Every teammate's install succeeds, but the skill fails for everyone except the author when actually run.

Question: What is the most likely root cause, and what does it reveal about plugin distribution?

A. The marketplace corrupted the plugin package during distribution, so the install silently failed for teammates.

B. The SKILL.md likely references an absolute path or an undocumented environment variable specific to the author's machine — installation succeeding says nothing about whether execution will succeed elsewhere.

C. Teammates need to grant `bypassPermissions` mode before a newly installed plugin's skill can execute correctly.

D. Plugins cannot bundle hooks, so the accompanying hook was silently dropped during install, breaking the skill's validation step.

Correct answer: B

Explanation: This is the module's canonical failure pattern: an absolute path or an undocumented environment variable baked into a skill body installs cleanly everywhere (a copy operation) but only resolves correctly on the machine where that path or variable actually exists. Installation and execution are different guarantees.

Distractors:
- A: The scenario states install succeeded for everyone; there's no indication of package corruption.
- C: Permission mode is unrelated to whether a hardcoded path or missing environment variable resolves correctly.
- D: Plugins can bundle hooks, subagents, and MCP servers alongside skills; nothing in the scenario suggests the hook was dropped, and this isn't the module's actual explanation for such failures.

## Question 5

Scenario: An architect is deciding where to register a new internal code-search MCP server that the entire engineering team should be able to use, hosted on company infrastructure.

Question: Which transport and scope combination is correct?

A. stdio transport, Local scope.

B. HTTP transport, Project scope (.mcp.json committed to the repo).

C. stdio transport, Project scope, since committing the launch command lets every teammate share one running instance.

D. HTTP transport, Local scope, so each developer configures it individually for security.

Correct answer: B

Explanation: HTTP is the recommended transport for any server that doesn't run locally, and Project scope (a committed .mcp.json) is the right choice when the whole team needs the same server configuration shared via the repository.

Distractors:
- A: stdio only works for a server that runs as a local subprocess on the same machine as the client — it cannot be shared across a team.
- C: This misunderstands stdio: even if committed to .mcp.json, a stdio server spawns a separate local subprocess on each teammate's own machine rather than sharing one running instance, and the server here is remote/company-hosted, not local at all.
- D: Local scope is explicitly for a server tied to one person's context, not shared team access; this also misapplies "security" reasoning that isn't part of the scope decision.

## Question 6

Scenario: A developer needs the server working quickly, so they place a data warehouse MCP server's API key directly in `.mcp.json`, planning to move it to an environment variable "later." The file gets committed so teammates can connect by cloning the repo. Three teammates clone it and a CI runner also picks it up within 48 hours. The developer later updates `.mcp.json` to reference an environment variable and commits the fix.

Question: Is the exposure resolved at that point, and what is the correct remaining action?

A. Yes — once the corrected .mcp.json no longer contains the inline key, the exposure is closed.

B. No — the key remains in the repository's commit history even after the fix; the service account key must be rotated.

C. No — the fix must also delete the repository's entire git history, since there is no other way to remove a leaked key from a file.

D. Yes, as long as the three teammates and the CI runner each individually delete their local clones.

Correct answer: B

Explanation: Overwriting a file in a later commit does not remove the earlier value from repository history. The only way to close a credential exposure like this is rotation — issuing a new key so the leaked one is worthless — as the module states directly.

Distractors:
- A: This is the exact mistake the scenario is testing against; the committed history still contains the original key regardless of what the current file shows.
- C: Deleting git history is not the practice the module recommends, and is a disproportionate, often infeasible response compared to simply rotating the credential.
- D: Deleting local clones does nothing about the value already recorded in the shared repository's commit history, which any future clone would still expose.

## Question 7

Scenario: An OAuth-authenticated MCP integration to a SaaS service passed every test in staging. After deployment to production, every sign-in attempt fails with a redirect URI mismatch error.

Question: What is the most likely cause and the correct fix?

A. The OAuth provider is down; wait and retry the connection later.

B. OAuth redirect URIs are registered per host; the production host was never added to the OAuth app's allowed redirect URI list, so it must be registered before production sign-ins can succeed.

C. The MCP client has a code defect that only manifests under production load; the client library needs to be patched.

D. Production requires API-key authentication instead of OAuth; switch the integration's auth method.

Correct answer: B

Explanation: This matches the module's staging-to-production OAuth failure exactly: redirect URIs are registered per host, and a working staging connection says nothing about whether the production host has been authorized. The fix is registering the production redirect URI (and, per many enterprise policies, potentially a separate app registration for production).

Distractors:
- A: A redirect URI mismatch is a configuration error, not a provider outage — retrying will not change the outcome.
- C: The module frames this explicitly as a configuration/registration gap, not a code defect — staging passing "end to end" already rules out a code-level cause.
- D: Nothing about moving to production requires switching authentication mechanisms; the issue is the OAuth app's registered redirect URI, not the auth pattern choice itself.

## Question 8

Scenario: A regulated financial services customer is evaluating an MCP integration before accepting it into production. They ask about audit logging, configuration lock-down, and data residency, in addition to whether the connection works.

Question: Which combination of mechanisms from this module most directly answers those three additional questions (in order)?

A. A PreToolUse hook for logging, a `.gitignore` entry for lock-down, and an OAuth scope restriction for data residency.

B. A PostToolUse hook that logs every tool call, an enterprise managed configuration that individual developers cannot override, and an HTTP endpoint pinned to a specific region combined with region-pinned platform deployment.

C. A CLAUDE.md instruction requiring logging, a local `.claude/settings.local.json` override, and a stdio transport for locality.

D. A `dontAsk` permission mode for logging discipline, a project-scoped `.mcp.json` for lock-down, and a classical RAG index for data residency.

Correct answer: B

Explanation: PostToolUse hooks answer the audit-logging question because they fire deterministically regardless of model behavior. Enterprise managed configuration (which individual users and project files cannot override) answers the configuration-lock question. An HTTP endpoint pinned to a region plus platform deployment pinned to that region gives a checkable answer to the data-residency question — this is the module's explicit mapping.

Distractors:
- A: PreToolUse can only inspect calls before they run and is not framed as the audit-logging mechanism (that's PostToolUse); a `.gitignore` entry does nothing to lock configuration against override by developers; an OAuth scope restricts access, not where data is processed.
- C: A CLAUDE.md instruction is a convention, not a deterministic audit mechanism; a local, git-ignored settings file is the opposite of an enterprise-locked configuration; transport choice doesn't determine data residency.
- D: `dontAsk` mode governs which tools auto-run, not audit logging; project scope for .mcp.json is about sharing a server config with a team, not enterprise-level lock-down; a RAG index has nothing to do with where data is physically processed.

## Question 9

Scenario: A developer delegates an exploration task to Claude Code's built-in Explore subagent on a project whose CLAUDE.md contains the constraint "never modify files in /legacy/tokens/." During the delegated task, the subagent's output ends up recommending an edit inside that directory.

Question: What is the most accurate explanation?

A. The Explore subagent inherited the main session's full context, so the recommendation is a bug that should be reported.

B. The built-in Explore subagent skips loading CLAUDE.md and git status by design to stay fast and cheap, so the constraint was never in its context in the first place.

C. Subagents always automatically load every skill and rules file in the project, so CLAUDE.md must have been corrupted for this to happen.

D. The constraint should have been placed in a rules file instead, since CLAUDE.md constraints never apply to any Claude Code workflow involving subagents.

Correct answer: B

Explanation: The built-in Explore and Plan subagents intentionally skip CLAUDE.md and git status to keep research fast and cheap. Project-level rules and repository state defined there simply are not loaded into their context. For tasks where such constraints must be respected, use the general-purpose subagent or a custom subagent that explicitly loads what it needs.

Distractors:
- A: This is backwards — subagents explicitly do NOT inherit the main session's history or state; that's the whole point of running in an isolated context, and Explore specifically also skips CLAUDE.md.
- C: The opposite is true — subagents do not automatically load skills, and Explore/Plan specifically skip CLAUDE.md; nothing indicates corruption.
- D: CLAUDE.md constraints do apply to subagents that load it (e.g. general-purpose or a properly configured custom subagent) — the issue is specifically that Explore/Plan skip it, not that CLAUDE.md is universally inapplicable to subagent workflows.

## Question 10

Scenario: An architect is scoping the authentication approach for three MCP integrations: (1) a SaaS project-management tool where each employee signs in with their own account, (2) an internal warehouse API accessed under a shared service account, and (3) a local SQLite database tool used only for personal development.

Question: Which authentication pattern correctly matches each of the three, respectively?

A. OAuth for (1), OAuth for (2), OAuth for (3) — OAuth is the universal recommended pattern for all MCP servers.

B. OAuth for (1), an API key in an environment variable for (2), stdio transport governed by filesystem permissions (deny rules) for (3).

C. An API key in an environment variable for (1), OAuth for (2), an OAuth token for (3).

D. A committed API key in the shared `.mcp.json` for all three, since committing ensures every teammate has consistent access.

Correct answer: B

Explanation: This maps exactly to the module's three authentication patterns by service type: remote services with user identity use OAuth (the SaaS tool tied to individual sign-in), remote services with service identity use an API key via environment variable (the internal API under a shared service account), and local services use stdio with no network authentication, where the file-system permission model and deny rules are the governance layer.

Distractors:
- A: OAuth is specifically for services where the authorization model is tied to individual user identity; it is not the recommended pattern for a service-identity API or a purely local filesystem tool.
- C: This swaps the patterns — OAuth belongs with the user-identity SaaS tool (1), not the service-identity API (2); and a local filesystem tool doesn't use an OAuth token at all.
- D: This is the module's explicit anti-pattern — committing any API key inline into a shared, version-controlled `.mcp.json` is the credential-leakage failure the module warns against, regardless of convenience.
