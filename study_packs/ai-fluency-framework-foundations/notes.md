# AI Fluency: Framework & Foundations

- Source URL: https://anthropic-partners.skilljar.com/ai-fluency-framework-foundations/291863
- Completed: 2026-07-05
- Study pack: `study_packs/ai-fluency-framework-foundations/`

## Captured Sections

- Public course overview: two high-level sections, instructor information, AI diligence statement
- Introduction to AI Fluency
- Why do we need AI Fluency?
- The 4D Framework
- Generative AI fundamentals
- Capabilities & limitations
- A closer look at Delegation
- Project planning and Delegation
- A closer look at Description
- Effective prompting techniques
- A closer look at Discernment
- The Description-Discernment loop
- A closer look at Diligence
- Conclusion
- Certificate of completion: content questions reviewed; subjective survey questions were not submitted
- Additional activities

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| Domain 1: Agentic Architecture & Orchestration | Medium | General task decomposition, delegation boundaries, human vs AI responsibility, and the course's "agency" interaction mode. Does not cover Agent SDK loops, subagents, hooks, or session forking. |
| Domain 2: Tool Design & MCP Integration | Low | Mentions that current AI systems can connect to tools, but does not teach MCP, tool schemas, tool descriptions, error responses, or scoped tool access. |
| Domain 3: Claude Code Configuration & Workflows | Low | Generic planning and iterative refinement concepts overlap with Domain 3.5, but the course does not teach Claude Code configuration, slash commands, skills, plan mode, or CI workflow mechanics. |
| Domain 4: Prompt Engineering & Structured Output | High | Strong coverage of clear prompting, examples, constraints, task breakdown, role/tone, iterative refinement, and output evaluation. Does not cover JSON schema/tool-use enforcement or batch processing. |
| Domain 5: Context Management & Reliability | Medium | Covers hallucinations, knowledge cutoffs, context-window limits, critical evaluation, human oversight, disclosure, verification, and accountability. Does not cover production escalation logic or structured error propagation. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| AI Fluency | Durable human-AI collaboration skill, not prompt memorization or technical AI development expertise. The course anchors fluency in effectiveness, efficiency, ethics, and safety. |
| Automation, Augmentation, Agency | Automation means AI performs a specified task. Augmentation means human and AI collaborate as thinking and execution partners. Agency means AI is configured to act more independently within knowledge and behavior boundaries. |
| 4D Framework | The four competencies are Delegation, Description, Discernment, and Diligence. Treat them as a cycle: decide the work split, communicate clearly, evaluate critically, and act responsibly. |
| Generative AI capabilities | Current systems can generate language, code, and other content, maintain conversational flow, switch across many tasks, and sometimes connect with external tools. |
| Generative AI limitations | Watch for stale knowledge, hallucinations, context-window limits, and reasoning failures. These limits are why verification, human review, and good context design matter in exam scenarios. |
| Delegation | Decide what humans should do, what AI should do, and where collaboration is best. Delegation depends on problem awareness, platform awareness, and task delegation. |
| Problem Awareness | Define goals, success criteria, and the work required before involving AI. This maps to exam task decomposition and plan-before-execution judgment. |
| Platform Awareness | Understand the capabilities and limitations of the selected AI system. In certification scenarios, this should extend to model limits, tool availability, context windows, and integration constraints. |
| Task Delegation | Assign subtasks based on human strengths, AI strengths, risk, and review needs. Avoid "AI handles everything" as the default. |
| Description | Communicate product, process, and performance expectations. Product = what output is needed. Process = how Claude should approach the work. Performance = how Claude should behave during collaboration. |
| Prompting Techniques | Provide context, examples, constraints, step breakdowns, think-first/planning instructions, and role/tone guidance. Asking Claude to help improve a prompt is useful during iteration. |
| Discernment | Evaluate product quality, process/reasoning quality, and collaboration behavior. Use domain expertise to catch factual errors, gaps, poor assumptions, and unhelpful interaction patterns. |
| Description-Discernment Loop | Describe the need, inspect the result, refine with specific feedback, and integrate human expertise. This resembles exam validation/retry loops, but the exam often expects stricter schema or programmatic validation. |
| Diligence | Responsible AI collaboration through creation choices, transparency, and deployment responsibility. Consider data shared with AI, disclosure expectations, review process, and accountability for final outputs. |
| Personal AI Policy | Set standards for when to use AI, sensitive-data boundaries, quality-control steps, disclosure rules, and field-specific ethical criteria. |

## Decision Rules

- If a task has high business, safety, legal, financial, or reputational risk, keep humans responsible for final approval and use AI for bounded support such as drafting, analysis, or option generation.
- If the output must be reliable, define product, process, and performance requirements before asking Claude to execute.
- If a response misses the mark, diagnose whether the issue came from an unclear description, missing context, model limitation, or weak discernment criteria; then refine with specific feedback.
- If the work depends on current facts, external truth, or sensitive claims, verify beyond the model response instead of trusting fluency or polish.
- If publishing or handing off AI-assisted work, disclose AI's role when the audience or context expects it, document review steps, and take ownership of accuracy.
- If an exam scenario uses "agent" or "agency," do not answer with the course's general agency framing alone. Architect exam questions usually require concrete agent-loop, tool, context, and reliability controls.
- If a prompt asks for structured output and downstream systems depend on it, course prompting techniques are not enough by themselves; the exam guide prioritizes tool use, JSON schemas, validation, and retry feedback.

## Anti-Patterns

- Treating AI Fluency as memorizing prompt recipes instead of learning transferable collaboration judgment.
- Automating every task because AI is available, without checking risk, expertise, or review needs.
- Treating Claude like a static database or vending machine instead of an interactive collaborator that needs context and feedback.
- Giving vague instructions such as "make it better" without output criteria, constraints, audience, style, or process guidance.
- Accepting polished AI output without product, process, and performance evaluation.
- Hiding AI involvement when the audience, institution, employer, or risk context calls for transparency.
- Using this course as evidence for MCP, Claude Code, Agent SDK hooks, or JSON-schema mastery; those topics need separate study packs.

## Scenario Traps

- Trap: "AI Fluency means becoming an AI engineer." Better: It means collaborating with AI effectively, efficiently, ethically, and safely.
- Trap: "Delegation means assigning the whole task to AI." Better: Delegation means choosing the right split between human work, AI work, and collaboration.
- Trap: "Description is just prompt wording." Better: Description includes the desired product, the process Claude should use, and the behavior expected during collaboration.
- Trap: "Discernment only checks the final answer." Better: It also checks the AI's process and interaction behavior.
- Trap: "Diligence is only about factual accuracy." Better: It includes system choice, privacy/security considerations, transparency, verification, and accountability.
- Trap: "Agency in this course equals production agentic architecture." Better: Course agency is a broad interaction mode; the exam tests implementation details such as `stop_reason`, tool execution, context passing, and safeguards.
- Trap: "Prompt iteration is enough for structured extraction." Better: The exam favors schemas, tool use, validation, and retry-with-error-feedback when structured data must be machine-reliable.

## Memorization Cues

- 4D cycle: Delegate, Describe, Discern, Do diligence.
- Description has 3 Ps: Product, Process, Performance.
- Discernment has the same 3 Ps: Product quality, Process quality, Performance/interaction quality.
- Diligence has 3 stages: Creation choices, Transparency, Deployment responsibility.
- Interaction modes: Automation = task execution; Augmentation = partnership; Agency = configured independent work.
- Architect overlay: Course judgment is useful, but exam answers often require programmatic controls when reliability must be guaranteed.

## Source References

- Introduction to AI Fluency: course purpose, 4D overview, practice expectations.
- Why do we need AI Fluency?: automation, augmentation, agency.
- The 4D Framework: Delegation, Description, Discernment, Diligence and scenario exercises.
- Generative AI fundamentals: LLM basics, training/fine-tuning, context windows.
- Capabilities & limitations: hallucination, knowledge cutoff, reasoning limits, tool connections, human oversight.
- A closer look at Delegation: problem awareness, platform awareness, task delegation.
- Project planning and Delegation: project vision, task breakdown, human/AI strength analysis.
- A closer look at Description: product, process, and performance description.
- Effective prompting techniques: context, examples, constraints, steps, think-first planning, role/tone, prompt improvement.
- A closer look at Discernment: product, process, and performance discernment.
- The Description-Discernment loop: describe, discern, refine, integrate.
- A closer look at Diligence: creation, transparency, deployment responsibility, diligence statements.
- Conclusion: synthesis, personal AI policy, ongoing practice.
- Additional activities: AI fluency plan, prompt/pattern library, puzzle-based Description and Discernment practice.

## Gaps / Follow-Up

- Study Agent SDK loops, `stop_reason`, tool execution, hooks, subagents, and session management separately.
- Study MCP tool design, schemas, structured error responses, resource catalogs, and tool scoping separately.
- Study Claude Code configuration, skills, slash commands, plan mode, CI usage, and test-driven iteration separately.
- Study structured-output enforcement with tool use, JSON schema, validation, retry feedback, batch processing, and multi-pass review separately.
