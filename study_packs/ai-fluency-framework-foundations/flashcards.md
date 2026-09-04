# AI Fluency: Framework & Foundations Flashcards

## AI Fluency

Q: What does AI Fluency mean in this course?

A: Working with AI effectively, efficiently, ethically, and safely.

Domain: General

Example: A support lead uses Claude to draft replies (efficient), checks each one against the customer's actual issue before sending (effective and ethical), and never pastes in a customer's SSN (safe).

## AI Fluency Trap

Q: What is AI Fluency not?

A: It is not memorizing prompts or becoming an AI model developer.

Domain: General

Example: Someone who memorized "act as an expert in X" as a magic phrase but can't judge whether the resulting answer is actually correct has not developed AI Fluency.

## Interaction Modes

Q: What are the three broad ways people interact with AI in this course?

A: Automation, Augmentation, and Agency.

Domain: General

Example: A batch script that auto-tags support tickets is Automation, a writer co-editing an essay with Claude is Augmentation, and an autonomous coding agent that plans and runs its own tool calls to fix a bug is Agency.

## Automation

Q: What is Automation?

A: AI performs a specific task based on instructions.

Domain: General

Example: A script calls Claude to classify each incoming email as "billing," "technical," or "sales" and route it automatically, with no human in the loop per email.

## Augmentation

Q: What is Augmentation?

A: Human and AI collaborate as thinking and execution partners.

Domain: General

Example: A product manager brainstorms feature tradeoffs with Claude in a back-and-forth chat, revising the plan together before either of them commits to a final doc.

## Agency

Q: What is Agency in this course?

A: Configuring AI to work more independently within defined knowledge and behavior patterns.

Domain: D1

Example: Setting up a Claude project with a knowledge base of company policies and standing instructions so it can triage refund requests within pre-approved limits without a human checking every case.

## Agency Exam Trap

Q: Why is course "Agency" not enough for Architect agentic-system questions?

A: The exam expects implementation details: agent loops, tool calls, context passing, safeguards, and reliability controls.

Domain: D1

Example: An exam question about a research agent expects you to know it runs a loop of calling a search tool, feeding results back into context, and stopping via a max-iteration guardrail, not just that "the AI works independently."

## The 4Ds

Q: What are the four AI Fluency competencies?

A: Delegation, Description, Discernment, and Diligence.

Domain: General

Example: Before using AI to draft a legal memo, you decide what to hand off (Delegation), write a clear prompt with context and format (Description), check the draft for accuracy (Discernment), and disclose AI involvement to the client (Diligence).

## Delegation

Q: What does Delegation decide?

A: What humans do, what AI does, and where collaboration is best.

Domain: General

Example: A manager decides Claude will draft the first pass of a performance review summary, but the manager alone will write the sensitive feedback on interpersonal conflicts.

## Delegation Components

Q: What are the three components of Delegation?

A: Problem Awareness, Platform Awareness, and Task Delegation.

Domain: General

Example: Before asking Claude to write code, you first clarify what "done" looks like (Problem Awareness), confirm Claude can execute code in this tool (Platform Awareness), then decide you'll write tests while Claude writes the implementation (Task Delegation).

## Problem Awareness

Q: What is Problem Awareness?

A: Clarifying goals, success criteria, and required work before involving AI.

Domain: General

Example: Before prompting Claude to "improve this report," you first define that success means cutting it to two pages and making it readable by non-technical executives.

## Platform Awareness

Q: What is Platform Awareness?

A: Understanding the capabilities and limits of the chosen AI system.

Domain: D5

Example: Knowing that a particular Claude deployment has no internet access, so you don't ask it to pull today's stock price and instead paste the data in yourself.

## Task Delegation

Q: What is Task Delegation?

A: Splitting work based on human strengths, AI strengths, risk, and review needs.

Domain: General

Example: For a low-risk internal newsletter draft you let Claude write it end-to-end, but for a customer-facing legal disclosure you have Claude draft only an outline and a human writes and reviews the final text.

## Delegation Anti-Pattern

Q: What is the main Delegation anti-pattern?

A: Automating everything without considering risk, expertise, or review.

Domain: General

Example: A team lets an AI agent auto-approve expense reports of any size with no human check, then discovers it approved a duplicate five-figure reimbursement.

## Description

Q: What does Description cover?

A: Communicating what you want, how Claude should approach it, and how it should collaborate.

Domain: D4

Example: A prompt that says "write a 300-word press release (product), using our brand's punchy tone by first listing three angles then picking one (process), and push back if the announcement sounds exaggerated (performance)."

## Product Description

Q: What is Product Description?

A: Defining the desired output, format, audience, style, and level of detail.

Domain: D4

Example: "Write a one-page executive summary for non-technical investors, in plain language, with no jargon and no more than three bullet points per section."

## Process Description

Q: What is Process Description?

A: Guiding methods, steps, assumptions, or frameworks Claude should use.

Domain: D4

Example: "First list every assumption behind this financial forecast, then check each one against the attached data, then only build the projection."

## Performance Description

Q: What is Performance Description?

A: Defining collaboration behavior, such as concise vs detailed or challenging vs supportive.

Domain: D4

Example: "Be terse, no preamble" versus "walk me through your reasoning step by step and challenge any weak assumptions in my plan" are two different performance instructions for the same task.

## Prompting Techniques

Q: Name the six prompting techniques from the course.

A: Context, examples, constraints, task steps, think-first planning, and role/tone.

Domain: D4

Example: A prompt that gives background on the target audience (context), shows a sample email (examples), caps the length at 150 words (constraints), lists numbered steps to follow, asks Claude to outline before writing (think-first), and specifies "write as a friendly support agent" (role/tone).

## Prompt Iteration

Q: What is the course's "secret weapon" for improving prompts?

A: Ask the AI to help improve the prompt.

Domain: D4

Example: After a vague prompt produces a mediocre draft, you ask Claude "what information would have helped you write this better?" and use its answer to rewrite the prompt.

## Examples

Q: Why provide examples in prompts?

A: Examples show the desired output pattern and reduce ambiguity.

Domain: D4

Example: Instead of asking for "a good product title," you paste three sample titles in the exact style you want so Claude matches the pattern instead of guessing.

## Constraints

Q: Why specify constraints?

A: Constraints bound the answer so the model can optimize for the right shape and tradeoffs.

Domain: D4

Example: "Answer in under 100 words and cite only sources from the attached document" prevents a sprawling, unsourced essay.

## Discernment

Q: What does Discernment evaluate?

A: AI outputs, reasoning/process, and interaction behavior.

Domain: General

Example: Reviewing a Claude-generated sales forecast, you check whether the final number is plausible (output), whether the growth-rate assumptions it used make sense (process), and whether it flagged its own uncertainty (behavior).

## Product Discernment

Q: What does Product Discernment check?

A: Accuracy, relevance, coherence, appropriateness, and fit to requirements.

Domain: D5

Example: You verify that a Claude-written market analysis cites real competitors (accuracy), stays on the assigned industry (relevance), flows logically (coherence), uses a tone fit for a board deck (appropriateness), and covers everything the brief asked for (fit to requirements).

## Process Discernment

Q: What does Process Discernment check?

A: Whether the AI's reasoning approach has gaps, faulty assumptions, or poor logic.

Domain: D5

Example: Claude recommends a pricing change, but its reasoning assumed flat demand elasticity; catching that assumption is Process Discernment, even if the final recommendation "sounds" reasonable.

## Performance Discernment

Q: What does Performance Discernment check?

A: Whether Claude's communication and collaboration behavior are useful for the task.

Domain: D5

Example: Noticing that Claude keeps agreeing with every idea you propose instead of pushing back, and telling it to be more critical, is Performance Discernment.

## Domain Expertise

Q: Why does domain expertise matter for Discernment?

A: Experts can catch subtle errors and omissions that non-experts may miss.

Domain: D5

Example: A radiologist reviewing an AI-drafted scan summary notices a subtly mischaracterized shadow that a non-specialist reviewer would have missed entirely.

## Description-Discernment Loop

Q: What are the steps in the Description-Discernment loop?

A: Describe, discern, refine, and integrate human judgment.

Domain: General

Example: You prompt for a blog outline (describe), spot that it ignores SEO keywords (discern), ask Claude to add them (refine), then personally decide which keyword to lead with (integrate human judgment).

## Refinement

Q: What should feedback include when refining an AI response?

A: Specific issues, what worked, what failed, and adjusted requirements.

Domain: D4

Example: "The intro paragraph was great, but the third section misstates our refund policy — it's 30 days, not 60 — please rewrite just that section using the correct number."

## Diligence

Q: What does Diligence add beyond effectiveness and efficiency?

A: Ethics, safety, transparency, verification, and accountability.

Domain: General

Example: A journalist using AI to draft an article fact-checks every claim (verification), tells readers AI was used (transparency), avoids feeding it a source's private data (safety), and puts her own name behind the final piece (accountability).

## Diligence Components

Q: What are the three components of Diligence?

A: Creation Diligence, Transparency Diligence, and Deployment Diligence.

Domain: General

Example: Choosing not to paste client contract data into a public chatbot (Creation), telling teammates a document was AI-drafted (Transparency), and proofreading the final output before emailing a client (Deployment).

## Creation Diligence

Q: What is Creation Diligence?

A: Choosing appropriate AI systems and being careful about how and what you share.

Domain: General

Example: Using an enterprise Claude deployment with a data-retention agreement for confidential HR data instead of a free consumer chatbot with no such guarantees.

## Transparency Diligence

Q: What is Transparency Diligence?

A: Being clear about AI's role with audiences who need to know.

Domain: General

Example: A company adds a footnote to a customer-facing chatbot transcript stating "this response was generated by AI and reviewed by a support agent."

## Deployment Diligence

Q: What is Deployment Diligence?

A: Verifying and taking responsibility for AI-assisted outputs before sharing them.

Domain: D5

Example: Before publishing an AI-drafted blog post, the author fact-checks every statistic and signs off as the accountable author, rather than posting it unread.

## Personal AI Policy

Q: What should a personal AI policy define?

A: Use cases, sensitive-data boundaries, quality checks, disclosure rules, and ethical criteria.

Domain: General

Example: A freelancer's personal policy might say: use AI for first drafts and research, never paste client NDAs into it, always proofread before sending, disclose AI use if a client asks, and never use it to impersonate someone's writing style without consent.

## Architect Prompting Overlay

Q: When is course-style prompting not enough for the certification exam?

A: When downstream systems require guaranteed structured output or deterministic compliance.

Domain: D4

Example: A payment pipeline that parses Claude's response as JSON needs a validated schema and retry logic, not just a friendly prompt asking for "JSON please."

## Structured Output

Q: What should you add for machine-reliable structured output?

A: Tool use, JSON schemas, validation, and retry feedback.

Domain: D4

Example: Defining a tool with a strict JSON schema for `{"order_id": string, "status": enum}`, validating Claude's output against it, and automatically re-prompting with the validation error if it fails.

## Reliability Cue

Q: What limitations should trigger verification or human review?

A: Hallucinations, stale knowledge, context limits, complex reasoning, and high-risk decisions.

Domain: D5

Example: A Claude-drafted legal citation should be manually verified against a real case database, since fabricated citations are a known hallucination risk in high-stakes documents.

## Source Provenance

Q: How does Diligence connect to provenance?

A: It requires tracking AI contribution, review steps, and responsibility for shared outputs.

Domain: D5

Example: A team keeps a changelog noting which sections of a report Claude drafted, who reviewed each section, and who signed off before it went to the client.
