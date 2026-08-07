# Claude 101 Flashcards

## Claude Basics

Q: What is the best exam-safe description of Claude from this course?

A: Claude is a collaborative AI assistant for writing, research, analysis, coding, reasoning, and other work, not just a chatbot or search engine.

## Design Principles

Q: What does "helpful, harmless, and honest" imply for architecture questions?

A: Claude is designed for safe collaboration, but production reliability still needs verification, permissions, and deterministic controls where required.

## Prompt Triad

Q: What three elements make up the course's effective prompt framework?

A: Set the stage, define the task, and specify rules.

## Setting The Stage

Q: What should "setting the stage" include?

A: Role, objective, audience, background context, and why the task matters.

## Defining The Task

Q: What should "defining the task" include?

A: The concrete action Claude should take, such as analyze, draft, research, summarize, build, or compare.

## Specifying Rules

Q: What should "specifying rules" include?

A: Format, tone, style, constraints, examples, length, and source/citation expectations.

## Generic Answers

Q: If Claude's response is too generic, what should you try first?

A: Add details about audience, role, context, constraints, and desired output.

## Wrong Format

Q: If Claude does not follow the desired format, what should you provide?

A: A clearer structure or an example of the target format.

## High-Stakes Facts

Q: What should you do when Claude gives confident factual claims in a high-stakes context?

A: Verify independently, ask for citations or confidence, and use web/search grounding when current facts matter.

## Iteration

Q: What is the iteration mindset?

A: Treat first drafts as starting points, review gaps, give specific feedback, and refine or restart when context is too messy.

## Lightweight Evals

Q: How can you evaluate Claude for a recurring workflow without heavy infrastructure?

A: Test 5-10 representative examples, compare to known-good outputs, identify patterns, and refine prompts or review steps.

## Chat Mode

Q: When should you choose Chat?

A: For quick questions, brainstorming, drafting, learning, screenshots, dictation, and iterative discussion.

## Cowork Mode

Q: When should you choose Cowork?

A: For sustained work that pulls from many sources and produces a finished deliverable, such as research briefs or cross-source analysis.

## Code Mode

Q: When should you choose Claude Code?

A: For software work involving codebase navigation, file edits, commands, tests, diffs, git, or commits.

## Claude Code Plan Mode

Q: In an exam scenario, when should you choose Plan mode?

A: Choose Plan when the approach should be reviewed before Claude modifies files or runs through implementation.

## Claude Code Ask Mode

Q: What does Ask mode emphasize?

A: Claude proposes changes and waits for approval before modifications.

## Projects

Q: What are Projects best for?

A: Ongoing work that needs persistent knowledge, custom instructions, shared chats, memory, and team context.

## Project Instructions

Q: What do project instructions control?

A: Claude's behavior across conversations in the project, including process, tone, style, and recurring requirements.

## Project Knowledge

Q: Why should project files have descriptive names?

A: Names help Claude and retrieval mechanisms identify the right material and relationships.

## RAG In Projects

Q: What happens when project knowledge approaches context limits?

A: Claude can retrieve relevant portions instead of loading all project knowledge into the context at once.

## Artifacts

Q: When does an artifact make sense?

A: When output is substantial, self-contained, editable, reusable, interactive, or useful outside the chat.

## Published Artifacts

Q: What is the safety concern with publishing artifacts?

A: Published artifacts are accessible by link, so private or unreviewed content should not be published.

## Skills

Q: What is a Skill?

A: A package of instructions, scripts, and resources Claude can load for specialized repeatable tasks.

## Projects Vs Skills

Q: What is the shortest distinction between Projects and Skills?

A: Projects store knowledge; Skills perform tasks.

## Custom Skills

Q: When should you create a custom Skill?

A: When a repeatable workflow needs a consistent process, methodology, checklist, or output standard.

## Skill Security

Q: What should you check before installing a custom Skill?

A: Trust the source and review its contents, especially because skills can include executable code.

## Connectors

Q: What do connectors do?

A: They let Claude read or act on external tools and data based on granted permissions.

## MCP

Q: How does this course frame MCP?

A: MCP is the standard that powers connectors, but the course does not teach MCP schema or server design.

## Connector Permissions

Q: What data can Claude access through a connector?

A: Only data the authenticated user has permission to access and the connector scope allows.

## Enterprise Search

Q: What is Enterprise Search best for?

A: Searching and synthesizing permission-scoped knowledge across an organization's connected sources.

## Enterprise Search Setup

Q: Who completes the initial Enterprise Search setup?

A: An organization Owner or admin.

## Research Mode

Q: When should you choose Research mode?

A: For comprehensive multi-source investigations with synthesis and citations.

## Search Vs Research

Q: When is web search better than Research mode?

A: When the user needs a quick, narrow fact from one or two sources.

## Extended Thinking Vs Research

Q: When is extended thinking better than Research mode?

A: When the problem needs deep reasoning but not external information gathering.

## Enterprise Search Vs Research

Q: When is Enterprise Search better than Research mode?

A: When the answer should come from internal organization knowledge rather than broad web research.

## Claude For Chrome

Q: What is the key safety guidance for Claude for Chrome?

A: Use it for low-risk tasks on trusted sites; high-risk actions require extra caution and permission.

## Exam Trap

Q: Why is this course not enough for MCP or Agent SDK exam mastery?

A: It introduces product concepts, but the exam tests implementation details such as schemas, tool errors, loops, hooks, handoffs, and context passing.
