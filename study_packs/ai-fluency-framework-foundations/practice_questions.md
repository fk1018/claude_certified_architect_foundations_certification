# AI Fluency: Framework & Foundations Practice Questions

## Question 1

Scenario: A support team wants Claude to handle customer refund requests. A manager proposes letting Claude independently approve every refund because this will maximize automation.

Question: What is the best response using the course's Delegation framing and the certification exam's reliability expectations?

A. Let Claude approve all refunds, then audit a few cases later to check for mistakes.

B. Use Claude only for harmless drafting; never let it interact with refund workflows.

C. Split the workflow: Claude can gather facts and draft recommendations, while high-risk or policy-exception refunds require deterministic controls or human approval.

D. Ask Claude to self-rate its confidence and approve refunds when confidence is high.

Correct answer: C

Explanation: Delegation requires deciding which parts belong to AI, humans, or collaboration. For financial actions, the exam expects more than prompt guidance: use guardrails, prerequisites, thresholds, or human approval.

Distractors:

- A: Automates beyond the risk boundary and catches mistakes too late.
- B: Overcorrects; AI can still help with bounded low-risk work.
- D: Self-rated confidence is not a reliable compliance control.

## Question 2

Scenario: A team asks Claude to extract details from invoices. The prompt says, "Pull out the important fields," and outputs vary across documents.

Question: What is the best first improvement from the course, and what should be added for production-grade structured output?

A. Add product, process, and performance description; for production, enforce a JSON schema through tool use and validate results.

B. Ask Claude to be more careful; for production, keep the same free-form response and manually parse it.

C. Use only examples and avoid constraints so Claude has flexibility.

D. Increase the model context window so extraction fields become consistent.

Correct answer: A

Explanation: The course teaches clear Description: output, method, and collaboration behavior. The exam guide adds that schema-constrained tool use and validation are needed when downstream systems depend on structure.

Distractors:

- B: "Be careful" is vague and does not enforce structure.
- C: Examples help, but constraints and schema enforcement are still needed.
- D: Context size does not solve ambiguous output contracts.

## Question 3

Scenario: Claude Code is used in CI to review pull requests. Developers complain that review comments are vague and often flag harmless style differences.

Question: Which change best applies the course's Description principles and the exam guide's prompt-engineering emphasis?

A. Tell Claude to "only report high confidence issues."

B. Define explicit review criteria, examples of reportable and non-reportable issues, desired output format, and severity rules.

C. Ask Claude to produce longer explanations for every comment.

D. Disable review comments and rely only on developer judgment.

Correct answer: B

Explanation: Clear product, process, and performance expectations reduce ambiguity. The exam guide similarly favors explicit criteria and examples over vague confidence language.

Distractors:

- A: Confidence language is less reliable than concrete criteria.
- C: More text does not fix poor issue selection.
- D: Removes useful automation instead of calibrating it.

## Question 4

Scenario: A research assistant agent summarizes several sources into a report. The final output is fluent but includes claims without citations and ignores conflicting statistics.

Question: What is the best design response?

A. Trust the fluent summary because the model likely resolved conflicts internally.

B. Add a diligence statement at the end but keep the report unchanged.

C. Require structured claim-source mappings, preserve conflicts with attribution, and review the final synthesis before sharing.

D. Ask the synthesis agent to shorten the report so unsupported claims are less visible.

Correct answer: C

Explanation: Discernment requires evaluating output and process quality; Diligence requires accountability. The exam guide expects provenance preservation and uncertainty handling in multi-source synthesis.

Distractors:

- A: Fluency is not evidence.
- B: Disclosure does not replace verification or provenance.
- D: Shortening hides the problem rather than fixing it.

## Question 5

Scenario: A product team says the course's "Agency" concept proves they can deploy an autonomous customer-support agent by writing a strong system prompt and letting it act independently.

Question: What is the best exam-aligned correction?

A. Correct; agency means the AI should work independently without workflow controls.

B. Agency is a useful interaction concept, but production agentic systems still need agent loops, tool-result handling, context management, escalation rules, and deterministic safeguards.

C. Agency is unrelated to AI systems and should be ignored.

D. The team should avoid agents entirely because AI cannot act independently.

Correct answer: B

Explanation: The course's agency framing helps with delegation judgment, but the certification tests concrete architecture: tool calls, `stop_reason`, state, context, and reliability controls.

Distractors:

- A: Confuses a high-level concept with implementation safety.
- C: Throws away useful framing.
- D: Overstates the limitation; agents can be built with controls.

## Question 6

Scenario: You ask Claude to help plan a migration. It immediately starts proposing code changes before understanding service boundaries, risk, and success criteria.

Question: Which response best reflects the course's project-planning and Delegation guidance?

A. Ask Claude to continue and fix issues later through Discernment.

B. Stop and define the project vision, success criteria, major tasks, human-owned decisions, AI-suitable tasks, and collaboration points before execution.

C. Give Claude full autonomy so it can discover the plan while editing.

D. Switch to a smaller prompt so Claude has less context to distract it.

Correct answer: B

Explanation: Problem Awareness and task delegation come before execution. For large engineering work, this also aligns with the exam's preference for planning and decomposition before broad changes.

Distractors:

- A: Discernment helps iteration, but planning should not be skipped.
- C: High-impact changes need explicit boundaries.
- D: Less context can make planning worse.

## Question 7

Scenario: Claude writes a polished technical explanation in an unfamiliar domain. The answer sounds plausible, but the project owner lacks subject-matter expertise.

Question: What is the most reliable next step?

A. Publish it because polished language is a good quality signal.

B. Ask Claude whether it is confident and publish if confidence is high.

C. Apply Product, Process, and Performance Discernment, then route uncertain or high-impact claims to a qualified reviewer or source verification.

D. Rewrite the explanation in a more authoritative tone.

Correct answer: C

Explanation: The course emphasizes critical evaluation and domain expertise. The exam similarly expects human review or verification when confidence is uncertain and consequences matter.

Distractors:

- A: Fluency can mask errors.
- B: Self-reported confidence is weak calibration.
- D: Tone does not improve truth.

## Question 8

Scenario: A team uses Claude to draft a public report. Claude helped outline, rewrite, and check sections, and humans edited the final version.

Question: What should the team include to satisfy Diligence?

A. No disclosure, because humans made the final edits.

B. A disclosure that explains AI's role, the human review process, and who owns responsibility for the final output.

C. A full transcript of every Claude interaction.

D. A note that Claude wrote the report so the team has no responsibility for errors.

Correct answer: B

Explanation: Diligence means being transparent where appropriate and taking responsibility for AI-assisted outputs. The repo should not preserve full raw transcripts.

Distractors:

- A: Human editing does not automatically remove disclosure expectations.
- C: Excessive raw transcript sharing is unnecessary and often inappropriate.
- D: Humans remain accountable for what they publish.
