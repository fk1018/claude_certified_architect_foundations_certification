# Claude 101 Practice Questions

## Question 1

Scenario: A marketing manager asks Claude, "Write an email about the project delay." The result is generic and does not match the customer relationship or tone.

Question: What is the best next action?

A. Switch immediately to a different Claude product.

B. Add audience, role, delay context, tone, constraints, and desired length to the prompt.

C. Start a new chat and ask the same question again.

D. Use Research mode because the answer was not specific enough.

Correct answer: B

Explanation: The course's first troubleshooting step for generic output is to add missing context and constraints. The issue is prompt specificity, not product selection or research depth.

Distractors:

- A: A product switch does not fix missing prompt context.
- C: Restarting can help when context is messy, but repeating the same vague prompt preserves the problem.
- D: Research mode is for multi-source investigation, not basic tone/context repair.

## Question 2

Scenario: A team repeatedly asks Claude to draft client proposals using the same company positioning, proposal template, and tone rules.

Question: Which design best matches the course guidance?

A. Put reference materials in a Project and encode the repeatable drafting procedure as a Skill.

B. Use Research mode every time because proposals need comprehensive output.

C. Publish a reusable artifact containing the proposal template and client data.

D. Use only Chat because projects and skills are interchangeable.

Correct answer: A

Explanation: Projects store durable knowledge; Skills encode repeatable procedures. Combining them fits recurring work with both context and process.

Distractors:

- B: Research is for investigation, not a stable internal drafting workflow.
- C: Publishing may expose private client information.
- D: Projects and Skills solve different problems.

## Question 3

Scenario: An architect wants Claude to answer questions across Slack, Google Drive, and company email while respecting each employee's permissions.

Question: Which course concept best fits?

A. Public artifact publishing.

B. Enterprise Search with connected sources and user authentication.

C. A single uploaded PDF in a regular chat.

D. Claude for Chrome on financial services sites.

Correct answer: B

Explanation: Enterprise Search is designed for organization-wide knowledge retrieval with admin setup, user authentication, permission-scoped results, and citations.

Distractors:

- A: Artifacts are outputs, not organization search infrastructure.
- C: A single upload does not cover cross-tool organizational knowledge.
- D: Chrome automation is not the right pattern and has risk limits.

## Question 4

Scenario: A product lead needs a comprehensive market analysis comparing vendors, technology trends, and supply chain risks, with citations.

Question: Which Claude capability is the best fit?

A. Research mode.

B. Web search for one quick lookup.

C. Project instructions only.

D. A custom style setting.

Correct answer: A

Explanation: Research mode is meant for systematic, multi-source investigations that synthesize findings and cite sources.

Distractors:

- B: A quick lookup is too narrow for this task.
- C: Project instructions can shape behavior but do not perform broad research by themselves.
- D: Style affects tone, not research depth.

## Question 5

Scenario: A developer wants Claude to inspect an unfamiliar codebase, change files, run tests, show diffs, and create a commit.

Question: Which product should they choose?

A. Claude Code.

B. Claude for Excel.

C. Enterprise Search.

D. A published artifact.

Correct answer: A

Explanation: Claude Code is built for codebase navigation, file edits, terminal commands, diffs, tests, and git workflows.

Distractors:

- B: Excel is for spreadsheet workflows.
- C: Enterprise Search is for organization knowledge retrieval.
- D: Artifacts are standalone outputs, not a development environment.

## Question 6

Scenario: Before a risky refactor, a team wants Claude to explain its implementation strategy before any file changes.

Question: Which Claude Code interaction mode best fits?

A. Plan mode.

B. Code mode.

C. Ask mode for every terminal command only.

D. Research mode.

Correct answer: A

Explanation: Plan mode is for reviewing Claude's approach before it touches files. It is the right control point for higher-risk implementation planning.

Distractors:

- B: Code mode allows file changes automatically and checks before terminal commands.
- C: Ask mode can gate changes, but the scenario specifically asks for an upfront implementation strategy.
- D: Research mode is not the code execution workflow.

## Question 7

Scenario: Claude has access to a connected Google Drive account. A manager worries it can now see every document in the company.

Question: What is the best response based on the course?

A. Claude can access all data in the connected service.

B. Claude can access only what the authenticated user and granted connector scopes permit.

C. Claude stores a separate index of all connected data forever.

D. Claude can access only documents manually shared with Anthropic.

Correct answer: B

Explanation: Connector access is permission-scoped. Claude sees what the user can access and what the connector permissions allow.

Distractors:

- A: This overstates connector access.
- C: The course emphasizes permission-scoped access, not a separate permanent data copy.
- D: This understates connector functionality.

## Question 8

Scenario: A project knowledge base has grown large. The team asks how Claude can continue using the most relevant material without loading every document into every answer.

Question: Which concept from the course explains this?

A. Retrieval-augmented project knowledge.

B. Artifact remixing.

C. Claude for Chrome browser automation.

D. Slack thread summarization.

Correct answer: A

Explanation: Projects can retrieve relevant portions of a large knowledge base when context limits are approached.

Distractors:

- B: Artifact remixing concerns shared outputs, not context retrieval.
- C: Chrome automation interacts with web pages.
- D: Slack summarization is a connector use case, not the project scaling mechanism.

## Question 9

Scenario: A workflow extracts customer fields from scanned contracts and sends JSON to a downstream system. The team proposes using only the course's prompt triad and examples.

Question: What is the best exam-oriented critique?

A. Prompt clarity helps, but downstream reliability usually requires schemas, validation, retries, and error feedback.

B. The prompt triad is enough for all structured extraction workflows.

C. Research mode should always perform structured extraction.

D. Publishing the output as an artifact guarantees machine-readable JSON.

Correct answer: A

Explanation: Claude 101 covers useful prompting basics, but the certification guide expects stronger structured-output controls for machine-reliable extraction.

Distractors:

- B: This ignores exam requirements for structured output enforcement.
- C: Research is for investigation, not extraction architecture.
- D: Artifacts do not guarantee schema-valid output.

## Question 10

Scenario: A team wants Claude to review many internal launch documents, Slack decisions, and email threads, then produce a launch-readiness memo with cited internal sources.

Question: Which capability is the strongest fit if the organization has configured it?

A. Enterprise Search.

B. A public artifact.

C. A style preference.

D. A single prompt in an empty chat.

Correct answer: A

Explanation: Enterprise Search is built for synthesizing internal organizational knowledge across connected sources with citations and permission controls.

Distractors:

- B: Public artifacts are shareable outputs and may create data exposure risk.
- C: Style preferences change response voice, not data access.
- D: An empty chat lacks the internal source access needed.
