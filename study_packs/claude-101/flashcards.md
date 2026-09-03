# Claude 101 Flashcards

## Claude Basics

Q: What is the best exam-safe description of Claude from this course?

A: Claude is a collaborative AI assistant for writing, research, analysis, coding, reasoning, and other work, not just a chatbot or search engine.

Domain: General

Example: A user asks Claude to draft a project proposal, debug a Python script, and summarize a research paper in the same session, rather than treating it as a single-purpose search box.

## Design Principles

Q: What does "helpful, harmless, and honest" imply for architecture questions?

A: Claude is designed for safe collaboration, but production reliability still needs verification, permissions, and deterministic controls where required.

Domain: D5

Example: Before letting Claude auto-approve refunds in a support workflow, an architect still adds a human review step and an audit log, rather than trusting Claude's judgment alone.

## Prompt Triad

Q: What three elements make up the course's effective prompt framework?

A: Set the stage, define the task, and specify rules.

Domain: D4

Example: "You are a marketing analyst (stage). Summarize this quarterly report (task). Keep it under 200 words and use bullet points (rules)."

## Setting The Stage

Q: What should "setting the stage" include?

A: Role, objective, audience, background context, and why the task matters.

Domain: D4

Example: "You're a technical writer preparing onboarding docs for new engineers who have never used our internal API; this doc will be their first reference."

## Defining The Task

Q: What should "defining the task" include?

A: The concrete action Claude should take, such as analyze, draft, research, summarize, build, or compare.

Domain: D4

Example: "Compare these three vendor contracts and flag any clauses that differ from our standard terms."

## Specifying Rules

Q: What should "specifying rules" include?

A: Format, tone, style, constraints, examples, length, and source/citation expectations.

Domain: D4

Example: "Respond in a formal tone, as a numbered list, under 150 words, and cite the source document for each claim."

## Generic Answers

Q: If Claude's response is too generic, what should you try first?

A: Add details about audience, role, context, constraints, and desired output.

Domain: D4

Example: Instead of "write a blog post," try "write a 500-word blog post for first-time homebuyers, in a friendly tone, explaining closing costs."

## Wrong Format

Q: If Claude does not follow the desired format, what should you provide?

A: A clearer structure or an example of the target format.

Domain: D4

Example: If Claude returns a paragraph but you needed a table, paste a sample table with headers like "Feature | Cost | Notes" and ask Claude to match that layout.

## High-Stakes Facts

Q: What should you do when Claude gives confident factual claims in a high-stakes context?

A: Verify independently, ask for citations or confidence, and use web/search grounding when current facts matter.

Domain: D5

Example: When Claude states a specific regulatory deadline for a compliance filing, the user cross-checks it against the official agency website before relying on it.

## Iteration

Q: What is the iteration mindset?

A: Treat first drafts as starting points, review gaps, give specific feedback, and refine or restart when context is too messy.

Domain: D4

Example: Claude's first draft of an email is too formal, so the user replies "make paragraph two more casual and cut the last sentence" instead of starting over.

## Lightweight Evals

Q: How can you evaluate Claude for a recurring workflow without heavy infrastructure?

A: Test 5-10 representative examples, compare to known-good outputs, identify patterns, and refine prompts or review steps.

Domain: D5

Example: Before automating support ticket triage, a team runs 8 sample tickets through Claude, compares the labels to what a human agent chose, and tweaks the prompt where they diverge.

## Chat Mode

Q: When should you choose Chat?

A: For quick questions, brainstorming, drafting, learning, screenshots, dictation, and iterative discussion.

Domain: D1

Example: A user pastes a screenshot of an error dialog and asks Claude in Chat what it means, then brainstorms three possible fixes in the same conversation.

## Cowork Mode

Q: When should you choose Cowork?

A: For sustained work that pulls from many sources and produces a finished deliverable, such as research briefs or cross-source analysis.

Domain: D1

Example: An analyst uses Cowork to pull data from five spreadsheets and two PDFs and produce a single finished competitive-landscape brief.

## Code Mode

Q: When should you choose Claude Code?

A: For software work involving codebase navigation, file edits, commands, tests, diffs, git, or commits.

Domain: D3

Example: A developer asks Claude Code to find every file that imports a deprecated function, update the calls, run the test suite, and commit the fix.

## Claude Code Plan Mode

Q: In an exam scenario, when should you choose Plan mode?

A: Choose Plan when the approach should be reviewed before Claude modifies files or runs through implementation.

Domain: D3

Example: Before a large database migration, an engineer uses Plan mode so Claude outlines the steps and files it will touch, letting the engineer approve the approach first.

## Claude Code Ask Mode

Q: What does Ask mode emphasize?

A: Claude proposes changes and waits for approval before modifications.

Domain: D3

Example: In Ask mode, Claude suggests editing three lines in a config file and shows a diff, but does not save the file until the user clicks approve.

## Projects

Q: What are Projects best for?

A: Ongoing work that needs persistent knowledge, custom instructions, shared chats, memory, and team context.

Domain: D5

Example: A legal team sets up a Project with all their standard contract templates uploaded, so every new chat automatically has that context available.

## Project Instructions

Q: What do project instructions control?

A: Claude's behavior across conversations in the project, including process, tone, style, and recurring requirements.

Domain: D3

Example: A project instruction says "always respond in AP style and flag any unverified statistics," and every chat in that project follows it automatically.

## Project Knowledge

Q: Why should project files have descriptive names?

A: Names help Claude and retrieval mechanisms identify the right material and relationships.

Domain: D5

Example: Naming a file "2026-Q1-sales-report.pdf" instead of "document3.pdf" makes it far easier for Claude to find and cite the right source when asked about Q1 sales.

## RAG In Projects

Q: What happens when project knowledge approaches context limits?

A: Claude can retrieve relevant portions instead of loading all project knowledge into the context at once.

Domain: D5

Example: A project with 200 uploaded PDFs answers a question about warranty terms by pulling just the two relevant warranty documents rather than every file.

## Artifacts

Q: When does an artifact make sense?

A: When output is substantial, self-contained, editable, reusable, interactive, or useful outside the chat.

Domain: D4

Example: Asking Claude to build an interactive budget calculator produces an artifact the user can keep tweaking and reuse, rather than a one-off chat reply.

## Published Artifacts

Q: What is the safety concern with publishing artifacts?

A: Published artifacts are accessible by link, so private or unreviewed content should not be published.

Domain: D5

Example: A draft containing unredacted customer names should not be published as an artifact, since anyone with the link could view it.

## Skills

Q: What is a Skill?

A: A package of instructions, scripts, and resources Claude can load for specialized repeatable tasks.

Domain: D2

Example: A "weekly-report" Skill bundles the exact formatting rules, data sources, and a Python script Claude runs every time someone asks for the weekly status report.

## Projects Vs Skills

Q: What is the shortest distinction between Projects and Skills?

A: Projects store knowledge; Skills perform tasks.

Domain: D2

Example: A Project holds a company's style guide PDFs for reference, while a Skill actually reformats a document to match that style guide on command.

## Custom Skills

Q: When should you create a custom Skill?

A: When a repeatable workflow needs a consistent process, methodology, checklist, or output standard.

Domain: D2

Example: A support team creates a custom Skill so every bug triage follows the same checklist: reproduce, classify severity, assign owner, log in the tracker.

## Skill Security

Q: What should you check before installing a custom Skill?

A: Trust the source and review its contents, especially because skills can include executable code.

Domain: D2

Example: Before installing a third-party Skill that automates file cleanup, a security-conscious user reads its bundled script to confirm it doesn't delete anything unexpected.

## Connectors

Q: What do connectors do?

A: They let Claude read or act on external tools and data based on granted permissions.

Domain: D2

Example: With a Google Drive connector enabled, a user asks Claude to summarize a specific shared document without downloading or pasting it manually.

## MCP

Q: How does this course frame MCP?

A: MCP is the standard that powers connectors, but the course does not teach MCP schema or server design.

Domain: D2

Example: A user knows that the Slack connector they use in Claude runs on MCP under the hood, but this course won't teach them how to write an MCP server for Slack themselves.

## Connector Permissions

Q: What data can Claude access through a connector?

A: Only data the authenticated user has permission to access and the connector scope allows.

Domain: D2

Example: If a user can't open a particular shared folder in Google Drive directly, Claude also cannot read its contents through the Drive connector.

## Enterprise Search

Q: What is Enterprise Search best for?

A: Searching and synthesizing permission-scoped knowledge across an organization's connected sources.

Domain: D5

Example: An employee asks "what is our current parental leave policy?" and Enterprise Search pulls the answer from HR's Confluence space and a linked PDF, respecting that employee's access.

## Enterprise Search Setup

Q: Who completes the initial Enterprise Search setup?

A: An organization Owner or admin.

Domain: D3

Example: An IT admin, not an individual employee, is the one who connects the company's Google Workspace and Confluence to enable Enterprise Search org-wide.

## Research Mode

Q: When should you choose Research mode?

A: For comprehensive multi-source investigations with synthesis and citations.

Domain: D5

Example: A user asks Claude to research the competitive landscape for electric bike startups, pulling from a dozen news articles and company sites with citations for each claim.

## Search Vs Research

Q: When is web search better than Research mode?

A: When the user needs a quick, narrow fact from one or two sources.

Domain: D5

Example: "What's today's exchange rate between USD and EUR?" calls for a quick web search, not a full Research investigation.

## Extended Thinking Vs Research

Q: When is extended thinking better than Research mode?

A: When the problem needs deep reasoning but not external information gathering.

Domain: D1

Example: Solving a tricky multi-step logic puzzle or debugging a subtle algorithm calls for extended thinking, not pulling in outside sources.

## Enterprise Search Vs Research

Q: When is Enterprise Search better than Research mode?

A: When the answer should come from internal organization knowledge rather than broad web research.

Domain: D5

Example: "What was our Q2 internal revenue target?" should use Enterprise Search against internal finance documents, not a public web Research query.

## Claude For Chrome

Q: What is the key safety guidance for Claude for Chrome?

A: Use it for low-risk tasks on trusted sites; high-risk actions require extra caution and permission.

Domain: D1

Example: Using Claude for Chrome to summarize articles on a news site is low-risk, but letting it submit a payment form on a checkout page warrants explicit user approval first.

## Exam Trap

Q: Why is this course not enough for MCP or Agent SDK exam mastery?

A: It introduces product concepts, but the exam tests implementation details such as schemas, tool errors, loops, hooks, handoffs, and context passing.

Domain: D1

Example: This course explains what MCP connectors are, but an exam question about writing a correct JSON schema for a custom MCP tool requires knowledge from a different, more technical course.
