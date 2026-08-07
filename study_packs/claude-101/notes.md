# Claude 101

- Source URL: https://anthropic-partners.skilljar.com/claude-101/383389
- Completed: 2026-07-05
- Study pack: `study_packs/claude-101/`

## Captured Sections

- What is Claude?
- Your first conversation with Claude
- Getting better results
- Claude desktop app: Chat, Cowork, Code
- Introduction to projects
- Creating with artifacts
- Working with skills
- Connecting your tools
- Enterprise search
- Research mode for deep dives
- Claude in action: use-cases by role
- Other ways to work with Claude
- What's next?
- Certificate of completion: content questions reviewed through the course-knowledge portion; required subjective satisfaction prompts were not submitted.

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| Domain 1: Agentic Architecture & Orchestration | Medium | Introduces agentic product behavior in Research, Cowork, Claude Code, planning, subagents, task decomposition, and mode selection. Does not teach Agent SDK loops, `stop_reason`, Task tool configuration, hooks, or handoff protocols. |
| Domain 2: Tool Design & MCP Integration | Medium | Explains connectors, web connectors, desktop extensions, MCP as the connector standard, scoped permissions, trusted-source caution, and tool/data access patterns. Does not teach MCP schema design, tool descriptions, structured errors, or backend interface boundaries. |
| Domain 3: Claude Code Configuration & Workflows | Medium | Covers Claude Code at a product level: local vs remote work, Ask/Code/Plan modes, terminal access, visual diffs, git tracking, hooks mention, and skills as reusable instruction packages. Does not cover `CLAUDE.md`, slash commands, path-specific rules, or CI/CD. |
| Domain 4: Prompt Engineering & Structured Output | High | Covers prompt context, task definition, rules, examples, constraints, iteration, output troubleshooting, tone/format control, and lightweight evals. Does not cover JSON schemas, tool-enforced structured output, extraction retries, batch processing, or multi-pass review architectures. |
| Domain 5: Context Management & Reliability | High | Covers uploads, projects, persistent instructions, memory, styles, RAG-backed project knowledge, connectors, Enterprise Search permissions, Research citations, evals, high-stakes verification, and product safety boundaries. Does not teach production escalation logic or multi-agent error propagation. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| Claude as an assistant | Claude is framed as a collaborative AI assistant for writing, research, analysis, coding, reasoning, learning, and problem solving, not as a simple chatbot or search engine. |
| Helpful, harmless, honest | The course anchors Claude's design in safety, steerability, collaboration, and Constitutional AI. For the exam, translate this into reliability and human-judgment expectations, not a substitute for deterministic controls. |
| Prompt triad | Effective prompts set the stage, define the task, and specify rules. Stage = role/context/objective. Task = action Claude should take. Rules = style, format, tone, constraints, and examples. |
| Iteration mindset | First responses are starting points. Refine with specific feedback, add missing context, show an example format, or restart when context has gone too far off track. |
| Lightweight evals | For recurring workflows, test Claude on 5-10 representative examples, compare output to known-good work, identify gaps, and decide where prompt changes, examples, or human review are needed. |
| Chat mode | Best for quick questions, brainstorming, drafting, iterative discussion, screenshots, dictation, and lightweight connected-tool context. |
| Cowork mode | Best for sustained multi-source work such as research briefs, cross-source analysis, file organization, scheduled tasks, and finished deliverables. It can plan, use folders, plugins, connectors, browser/computer use, and subagents. |
| Code mode | Best for software work. Claude works in a local folder or remote GitHub-backed environment, reads and changes code, runs commands, shows diffs, and tracks changes with git. |
| Ask/Code/Plan in Claude Code | Ask waits for approval before changes. Code edits files but checks before terminal commands. Plan outlines the approach before touching files. Use Plan when strategy and risk need review. |
| Projects | Projects are persistent workspaces with their own knowledge base, instructions, chats, memory, and optional team sharing. They are for ongoing work that needs stable context. |
| Project instructions | Instructions define behavior across all conversations in a project: context, process, tone, style, and recurring requirements. Treat them as persistent prompt policy for that workspace. |
| Project knowledge and RAG | Projects can use uploaded reference material across chats. When project knowledge approaches context limits, Claude can retrieve relevant parts instead of loading everything at once. |
| Artifacts | Artifacts are standalone outputs such as documents, diagrams, code, web pages, SVGs, Mermaid diagrams, and React components. They are useful when content is substantial, reusable, editable, or self-contained. |
| Skills | Skills are folders of instructions, scripts, and resources loaded dynamically for specialized tasks. Built-in skills support document creation; custom skills encode repeatable workflows. |
| Projects vs Skills | Projects store knowledge; skills perform tasks. Use projects for durable context and shared reference material. Use skills for repeatable procedures and consistent methodology. |
| Connectors | Connectors let Claude work with external tools and data. Web connectors attach cloud services; desktop extensions attach local tools through Claude Desktop. |
| MCP | The course introduces MCP as the standard behind connectors. It does not teach how to design MCP tool schemas, resources, errors, or server integrations. |
| Connector security | Claude can only access data permitted by the connected account and granted scopes. Permissions should be reviewed, toggled, revoked when no longer needed, and installed only from trusted sources. |
| Enterprise Search | A Team/Enterprise feature for organization-wide knowledge retrieval. Admins configure sources first; users authenticate their own services. Answers are permission-scoped and source-cited. |
| Research mode | Research is for systematic multi-source investigations. It plans, searches iteratively, synthesizes findings, and cites sources. Use it for broad analysis, not quick facts. |
| Specialized Claude products | Claude Code, Slack, Excel, PowerPoint, Chrome, and Cowork each fit different workflow environments. The exam often rewards choosing the right surface before choosing a prompt. |

## Decision Rules

- If Claude's answer is too generic, add audience, role, objective, constraints, and relevant context before changing products or models.
- If Claude misses a format, provide an example or explicit structure. For machine-validated output, remember that the exam usually expects schemas and validation, not only prose instructions.
- If facts are current, niche, high-stakes, legal, financial, or customer-impacting, ask for sources and independently verify; do not trust polished confidence.
- If work is one-off and conversational, use Chat. If work is ongoing with reusable knowledge, use a Project. If work is repeatable process execution, use a Skill. If work needs both, combine project knowledge with a skill-defined workflow.
- If a task requires broad multi-source research with citations, use Research. If it needs a quick fact, use web search. If it needs deep reasoning without new sources, use extended thinking. If it needs internal company knowledge, use Enterprise Search.
- If software work requires codebase changes, tests, commands, diffs, or commits, use Claude Code. Choose Plan mode when the approach needs review before modification.
- If a workflow needs external work data, prefer connectors over manual copy/paste when permissions, trust, and data sensitivity are acceptable.
- If using connectors, skills, plugins, or browser/computer use, check scopes, source trust, local boundaries, and whether the task is low risk enough for automation.
- If using projects, keep reference material current and name files clearly so retrieval and source selection remain useful.

## Anti-Patterns

- Treating Claude as a search engine instead of selecting between Chat, Research, Enterprise Search, connectors, or Claude Code based on the job.
- Expecting one prompt to produce final work without iteration, examples, feedback, or review.
- Using vague instructions such as "make this better" when the failure is missing audience, format, tone, or constraints.
- Treating Skills and Projects as interchangeable; projects hold context, skills encode procedure.
- Uploading stale or unrelated project knowledge and expecting reliable retrieval.
- Publishing artifacts that contain private, sensitive, or unreviewed content.
- Assuming a connector can access all organizational data instead of the user's permitted data and granted scopes.
- Using Research for quick facts where web search would be faster, or using web search for broad analysis where Research is a better fit.
- Treating this course as sufficient evidence for MCP, Agent SDK, `CLAUDE.md`, slash commands, JSON schema, CI/CD, or production escalation mastery.

## Scenario Traps

- Trap: "Claude is just a chatbot." Better: Claude is a general AI assistant surfaced through multiple products and workflows.
- Trap: "The first answer is generic, so switch tools." Better: first add task context, audience, constraints, examples, and feedback.
- Trap: "A shared team knowledge problem should be solved with repeated uploads." Better: use a Project or Enterprise Search depending on whether the scope is a team workspace or broad organizational knowledge.
- Trap: "A repeatable quarterly workflow belongs in a Project only." Better: store source knowledge in a Project, but encode the repeatable procedure as a Skill.
- Trap: "Connecting Slack or Drive gives Claude all company data." Better: connectors are permission-scoped to what the authenticated user can access.
- Trap: "Research mode is always better than search." Better: Research is for comprehensive multi-source investigations; quick facts should use faster lookup patterns.
- Trap: "Claude Code Plan mode is the same as asking for an explanation." Better: Plan mode is the control point before file modifications and command execution.
- Trap: "Course-level connector knowledge means MCP design is covered." Better: the course introduces MCP conceptually; the exam also tests tool descriptions, schemas, error responses, and server integration choices.
- Trap: "Prompt examples are enough for structured extraction." Better: for downstream machine reliability, the exam favors tool use, JSON schemas, validation, retries, and feedback loops.

## Memorization Cues

- Prompt triad: Stage, Task, Rules.
- Product fit: Chat = quick conversation; Cowork = sustained multi-source work; Code = software work.
- Project vs Skill: project = what Claude should know; skill = how Claude should act.
- Research vs Search: Research builds a cited investigation; search answers a narrow lookup.
- Enterprise Search: org knowledge, admin setup, user authentication, permission-scoped results, citations.
- Claude Code modes: Ask waits, Code edits, Plan designs first.
- Connector safety: scoped, trusted, revocable, permission-bound.

## Source References

- What is Claude?: Claude's role, core capabilities, safety framing, access surfaces, and large-context overview.
- Your first conversation with Claude: prompt triad, uploads, follow-up iteration, memory, styles, and personalization.
- Getting better results: troubleshooting patterns, AI Fluency, lightweight evals, verification, and when to restart context.
- Claude desktop app: Chat, Cowork, Code: mode selection, subagents, scheduled tasks, folder access, local/remote code work, Ask/Code/Plan, diffs, terminal, and git.
- Introduction to projects: project knowledge, instructions, sharing, permissions, RAG-backed scaling, and file-naming best practices.
- Creating with artifacts: artifact types, when artifacts appear, sharing/publishing behavior, and incremental iteration.
- Working with skills: built-in and custom skills, secure execution requirements, trusted-source caution, and projects-vs-skills distinction.
- Connecting your tools: connectors, MCP overview, web connectors, desktop extensions, setup, scopes, and revocation.
- Enterprise search: Team/Enterprise setup, admin/user responsibilities, permission-scoped search, citations, and organization-wide knowledge use cases.
- Research mode for deep dives: agentic multi-step investigation, extended thinking, citations, when to use Research vs search/extended thinking/Enterprise Search.
- Claude in action: use-cases by role: role-specific applications for sales, marketing, finance, HR, legal, research, and general professional work.
- Other ways to work with Claude: Claude Code, Slack, Excel, PowerPoint, Chrome, and product selection by workflow.
- What's next?: course recap and continued-study resource list.
- Certificate of completion: course-knowledge quiz concepts reviewed; subjective satisfaction prompts were not submitted.

## Gaps / Follow-Up

- Study Agent SDK loops, `stop_reason`, tool result history, Task tool spawning, hooks, handoffs, and session forking separately.
- Study MCP design beyond connectors: tool descriptions, input schemas, structured error responses, resource catalogs, and scoped tool access.
- Study Claude Code configuration: `CLAUDE.md`, imports, custom slash commands, path-specific rules, CI/CD, and test-driven iteration.
- Study structured output with JSON schema/tool use, validation errors, retry feedback, extraction batch strategy, and multi-pass review.
- Study production reliability patterns: escalation thresholds, human-in-the-loop handoff summaries, confidence calibration, provenance, and error propagation.
