# Claude Code in Action Practice Questions

These questions are exam-aligned study material based on the captured Skilljar course structure, readable lesson bodies, temporary inspection of course downloads, and `exam_guide_pdf.txt`.

## Question 1

Scenario: A developer asks Claude Code to "fix the login bug," but the stack trace points to one function in one file and the expected change is a single conditional check.

Question: What is the best Claude Code workflow?

A. Use direct execution, make the focused change, and run the relevant test.

B. Start plan mode, ask Claude to inspect the entire repository, and wait for a full architecture plan.

C. Add a permanent `CLAUDE.md` instruction saying login bugs are always simple.

D. Increase `/effort` to max and avoid reading the file.

Correct answer: A

Explanation: The change is narrow, low-risk, and already localized. Direct execution with targeted verification is sufficient.

Distractors:

- B: Plan mode is valuable for broad or risky changes, but excessive here.
- C: A one-off bug should not become a blanket memory rule.
- D: More reasoning does not replace reading the relevant code.

## Question 2

Scenario: A team asks Claude Code to migrate a shared authentication library used by dozens of packages. There are multiple possible migration strategies.

Question: What should the developer do first?

A. Tell Claude to edit all imports immediately and run tests later.

B. Use plan mode so Claude explores dependencies and proposes an implementation plan before editing.

C. Use `/clear` to remove all project context before starting.

D. Create a custom slash command for this one-time migration before understanding the codebase.

Correct answer: B

Explanation: Large, multi-file, architectural work benefits from plan mode because it separates exploration and design from execution.

Distractors:

- A: Immediate edits risk broad breakage before dependencies are understood.
- C: Clearing useful project context is counterproductive.
- D: A slash command is for repeatable workflows, not the first step in a one-time unknown migration.

## Question 3

Scenario: Claude repeatedly adds verbose comments to simple code despite repeated conversational reminders.

Question: What is the best durable fix?

A. Press Escape after every generated comment.

B. Raise `/effort` to max.

C. Add a concise project memory instruction through `/memory` or edit `CLAUDE.md`.

D. Remove all test files from context.

Correct answer: C

Explanation: Repeated project-specific behavior should be corrected in durable project guidance so future turns inherit the rule.

Distractors:

- A: Escape is useful for immediate redirection, not durable behavior.
- B: More reasoning does not encode a stable style preference.
- D: Test files are unrelated to comment verbosity.

## Question 4

Scenario: A developer knows that `prisma/schema.prisma` defines the database structure needed for many future Claude Code sessions.

Question: What is the best context strategy?

A. Paste the entire schema into every prompt manually.

B. Ask Claude to search the whole repository every time database structure matters.

C. Put the schema path in `.claude/commands/` without a command body.

D. Reference it in `CLAUDE.md` so Claude includes it when needed across recurring work.

Correct answer: D

Explanation: Durable references in `CLAUDE.md` are appropriate for high-value files that are often relevant.

Distractors:

- A: Manual repetition is noisy and error-prone.
- B: Repeated broad search wastes context and time.
- C: Slash commands encode workflows, not passive project context by themselves.

## Question 5

Scenario: A team wants a repeatable `/write_tests` workflow that accepts a file or feature name and applies team testing conventions.

Question: Where should they put it?

A. The root `README.md`, because Claude always treats it as a slash command.

B. `.claude/commands/write_tests.md` using `$ARGUMENTS` for the target.

C. `~/.claude/CLAUDE.md`, so every teammate gets it through version control.

D. A PostToolUse hook, because test writing must happen after every edit.

Correct answer: B

Explanation: Project slash commands live in `.claude/commands/`, and `$ARGUMENTS` makes the command reusable for different targets.

Distractors:

- A: README content does not define slash commands.
- C: User-level memory is personal, not team-shared through the repo.
- D: Hooks are event automation; this is an on-demand workflow.

## Question 6

Scenario: Claude Code needs to inspect a locally running web app, click through UI states, and revise a component-generation prompt based on the visual result.

Question: What capability should be added?

A. Increase `/effort` and ask Claude to imagine the browser output.

B. Put screenshots in `CLAUDE.md` forever.

C. Add a Playwright MCP server and grant appropriate browser-tool permissions.

D. Use Glob to find screenshots by filename instead of opening the app.

Correct answer: C

Explanation: Browser interaction is an external capability. An MCP server such as Playwright gives Claude Code tools to inspect and act in the browser.

Distractors:

- A: Reasoning cannot replace missing browser-control capability.
- B: Persistent screenshots would become stale and noisy.
- D: Static files do not provide live browser state.

## Question 7

Scenario: A GitHub Action running Claude Code with a Playwright MCP server fails because the workflow did not grant MCP tool access.

Question: What should be changed?

A. Add `mcp__playwright` to local `.claude/settings.local.json` only.

B. Ask Claude to approve browser permissions interactively during CI.

C. Remove all tool restrictions from the repository permanently.

D. Explicitly list the needed MCP tools in the workflow `allowed_tools`.

Correct answer: D

Explanation: GitHub Actions must explicitly enumerate allowed tools, including MCP tools. Local permission shortcuts do not apply to CI.

Distractors:

- A: Local settings do not grant CI permissions.
- B: CI cannot depend on interactive approval.
- C: Broad unrestricted access is not least privilege.

## Question 8

Scenario: Claude Code sometimes attempts to read `.env`. A team needs deterministic protection before the file is opened.

Question: What is the best first mechanism?

A. A PreToolUse hook or permission deny that blocks sensitive file access before execution.

B. A PostToolUse hook that apologizes after reading the file.

C. A prompt reminder saying secrets should be avoided.

D. A custom slash command named `/dont_read_env`.

Correct answer: A

Explanation: Deterministic protection must run before access. PreToolUse can block proposed calls, and permission deny rules can apply across tools.

Distractors:

- B: PostToolUse runs after the access has happened.
- C: Prompt reminders are probabilistic.
- D: A command does not enforce all tool calls.

## Question 9

Scenario: A developer writes a PreToolUse hook that checks `tool_input.file_path` and blocks `.env`. Later Claude accesses secrets using Bash.

Question: What went wrong?

A. PreToolUse hooks cannot block any tool calls.

B. The hook assumed all tools use the same input shape; Bash uses a command string and needs separate handling or permissions.

C. Exit code 0 should have been used to block the call.

D. The hook should have been stored in `README.md`.

Correct answer: B

Explanation: Tool input fields differ. Read, Grep, and Bash require different inspections, or a uniform permission-deny rule.

Distractors:

- A: PreToolUse can block calls.
- C: Exit code 2 blocks; 0 allows.
- D: README is not hook configuration.

## Question 10

Scenario: After Claude edits a TypeScript function signature, one call site is missed and the repo no longer type-checks.

Question: Which hook pattern best catches this quickly?

A. A PreToolUse hook that blocks every Read operation.

B. A custom slash command that must be manually invoked days later.

C. A PostToolUse hook on edits that runs `tsc --noEmit` and returns diagnostics to Claude.

D. A `/clear` command after each edit.

Correct answer: C

Explanation: A post-edit type-check hook provides immediate feedback after changes and guides Claude to fix missed call sites.

Distractors:

- A: Blocking reads prevents context gathering and does not type-check.
- B: Manual delayed checks lose the advantage of immediate feedback.
- D: Clearing context after each edit removes useful state.

## Question 11

Scenario: A large codebase has many existing SQL query helpers. Claude often adds duplicate query functions when implementing features.

Question: What is the best hook design from the course pattern?

A. Run the expensive duplicate-query review after every file read in the repository.

B. Add a vague `CLAUDE.md` note saying "do not duplicate code" and avoid checks.

C. Disable all database-query edits.

D. Target query-directory edits and use an independent Claude/SDK review to check for reusable existing queries.

Correct answer: D

Explanation: The review should be targeted to high-value query files and can use an independent Claude instance to reduce generator bias.

Distractors:

- A: Running expensive review on every read is wasteful.
- B: A vague instruction is weaker than targeted feedback.
- C: Disabling all edits blocks useful work.

## Question 12

Scenario: A hook developer does not know what JSON fields a `Stop` hook or `TodoWrite` PostToolUse hook receives.

Question: What should they do before implementing logic?

A. Add a temporary logging helper hook, such as piping the JSON through `jq` into a file, and inspect the event shape.

B. Assume every hook contains `tool_input.file_path`.

C. Use exit code 2 for all hook events until fields are discovered.

D. Put the hook in `.claude/commands/`.

Correct answer: A

Explanation: Hook input shape varies by event and tool. Logging the JSON lets the developer implement against the actual contract.

Distractors:

- B: Many events do not have file paths.
- C: Blocking everything is disruptive and does not reveal safe behavior.
- D: Commands and hooks are different mechanisms.

## Question 13

Scenario: A team wants to share hook settings, but hook docs recommend absolute script paths and each engineer clones the repo to a different location.

Question: What is the best approach?

A. Commit one engineer's absolute home-directory paths and require everyone to match them.

B. Commit a template settings file with placeholders and generate local `settings.local.json` during setup.

C. Use relative paths everywhere and ignore path interception risk.

D. Remove hook scripts from source control.

Correct answer: B

Explanation: A template plus setup generation preserves shareability while producing local absolute paths.

Distractors:

- A: Machine-specific paths will break for teammates.
- C: Relative paths can introduce security and resolution risks.
- D: Removing scripts makes the workflow unreproducible.

## Question 14

Scenario: An SDK automation should add a package description and should not run shell commands or read unrelated files.

Question: How should tool access be configured?

A. Give the SDK full tool access because it is faster to configure.

B. Use an MCP server for every built-in file operation.

C. Pass `allowedTools` with only the needed tool, such as `Edit`.

D. Put the restriction in a screenshot.

Correct answer: C

Explanation: `allowedTools` enforces least privilege for programmatic Claude Code runs.

Distractors:

- A: Full access increases risk and decision complexity.
- B: Built-in file edits do not require MCP.
- D: Screenshots cannot enforce tool permissions.

## Question 15

Scenario: A CI job invokes Claude Code for automated PR review and hangs while waiting for user input. The team also needs machine-readable review findings.

Question: Which exam-guide topic should they study beyond this course?

A. `/rewind`, because CI jobs should rewind before every command.

B. `Ctrl+G`, because CI can open plans in a local editor.

C. User-level `~/.claude/CLAUDE.md`, because it is shared with all CI jobs automatically.

D. Non-interactive `claude -p` plus structured output options such as `--output-format json` and `--json-schema`.

Correct answer: D

Explanation: The course covers GitHub Actions integration, but the exam also tests non-interactive CLI execution and structured CI output contracts.

Distractors:

- A: `/rewind` is an interactive context-control feature.
- B: CI cannot depend on opening an editor.
- C: User-level memory is not a shared repo configuration.

## Question 16

Scenario: A long Claude Code session has valuable understanding of a legacy subsystem but is nearing context limits. The next task is related to the same subsystem.

Question: What is the best context-control command?

A. `/compact`

B. `/clear`

C. `/install-github-app`

D. `/effort low`

Correct answer: A

Explanation: `/compact` summarizes the useful session context so related work can continue with less token pressure.

Distractors:

- B: `/clear` is better for unrelated work.
- C: GitHub integration is unrelated.
- D: Lower effort does not preserve or compress context.

## Question 17

Scenario: Claude starts solving five independent UI issues at once, but you only want the first issue handled now.

Question: What is the best immediate intervention?

A. Add all five issues permanently to `CLAUDE.md`.

B. Press Escape and redirect Claude to the single issue.

C. Start a GitHub Action.

D. Install a new MCP server.

Correct answer: B

Explanation: Escape is the course pattern for stopping an unhelpful direction and narrowing the task.

Distractors:

- A: Temporary issue selection does not belong in persistent memory.
- C: CI is not needed for immediate interaction control.
- D: The problem is focus, not missing external capability.

## Question 18

Scenario: A code review workflow has high false positives because the same Claude instance generated and reviewed the code in one session.

Question: Which architecture is better aligned with the course and exam guide?

A. Ask the same session to "try harder" after generation.

B. Hide the generated code from the reviewer.

C. Use a separate independent Claude instance for review.

D. Disable review if generation succeeded.

Correct answer: C

Explanation: Independent review reduces self-review bias because the reviewer does not carry the generator's reasoning context.

Distractors:

- A: More effort in the same context does not remove self-review bias.
- B: A reviewer needs the code to review it.
- D: Successful generation does not imply correctness.
