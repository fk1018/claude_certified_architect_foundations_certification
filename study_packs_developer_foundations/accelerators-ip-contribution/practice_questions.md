# Accelerators and IP Contribution Practice Questions

## Question 1

Scenario: A developer just finished a code-review agent for a customer engagement. It works well and the deadline is tomorrow. The team lead asks whether it should be packaged as a reusable accelerator before the engagement closes.

Question: According to the module, what is the strongest reason to package it now rather than later?

A. Packaging is required by the Claude Cookbook before any code can be contributed.

B. The knowledge of what is customer-specific is cheapest to capture while the build is fresh, and gets more expensive to reconstruct after the people who knew it have moved on.

C. A packaged accelerator automatically passes a security review, while an unpackaged one does not.

D. Packaging is only necessary if the code will be open-sourced externally.

Correct answer: B

Explanation: The module's core argument for packaging while the build is fresh is that the knowledge of which values are customer-specific and which are load-bearing is most expensive to reconstruct later, once the person who made those decisions has moved on to other work.

Distractors:

- A: Packaging for internal reuse and contributing to the Cookbook are related but separate motions; the Cookbook is not a prerequisite gate for packaging.
- C: Packaging helps a security review (via the bundled audit log) but does not automatically pass one; a reviewer still checks the specifics.
- D: The module frames packaging as valuable for any future engagement reuse, not only for external open-sourcing.

## Question 2

Scenario: A team ships an agent template with the customer's repository path, model name, and review thresholds hardcoded directly into the function body. Months later, a second team tries to reuse it for a similar engagement and cannot configure it.

Question: What is the most accurate diagnosis of what went wrong?

A. The template should have used a newer model version.

B. The template ran successfully, so it was already reusable; the second team simply lacked the context to use it.

C. A template that runs is not the same as a template packaged for reuse -- the customer-specific values needed to be parameters, and the assumptions and eval needed to be documented and bundled.

D. The template needed to be rewritten in a different programming language for portability.

Correct answer: C

Explanation: The module's postmortem makes this exact distinction: a working template and a reusable one are different finishing states. Hardcoded values with no documentation and no bundled eval leave the next team nothing to configure, forcing a rewrite.

Distractors:

- A: Model choice is unrelated to the packaging defect described.
- B: This is the trap the postmortem exists to correct -- running is not the same as reusable.
- D: Language choice was never the issue; the issue was hardcoded values and missing documentation/eval.

## Question 3

Scenario: A developer wants to share a small, focused utility function that wraps a single API call into a clean interface, built during a customer engagement. The code has no example, no test, and no note on what it assumes about its environment.

Question: What should the developer do before opening this as a contribution?

A. Submit it as-is, since a maintainer can read the function and infer its behavior.

B. Add a runnable example, a test that proves the behavior, and a short statement of assumptions, and confirm the right to contribute code that originated in an engagement.

C. Rewrite it as a full application with a UI so reviewers can see it in context.

D. Skip the Cookbook entirely and only distribute it privately within the team, since packaging for external contribution is optional.

Correct answer: B

Explanation: A maintainer accepts what they can verify. The module names four requirements for a verifiable contribution -- focused code, a runnable example, a test, and stated assumptions -- and requires the rights/attribution check before technical review, especially for engagement-derived code.

Distractors:

- A: This repeats the exact failure mode from the module's stalled-PR case; "the maintainer can figure it out" is what leaves a contribution at the back of the queue.
- C: A full application with a UI is a mismatch for a focused utility contribution and would itself violate the "match contribution to channel" guidance.
- D: The scenario asks what to do to make the contribution viable, not whether to contribute at all; nothing in the module makes external contribution optional once a team decides to pursue it.

## Question 4

Scenario: A developer wants to contribute an entire customer-service application -- including its UI and deployment scripts -- to the Claude Cookbook, because it is a working, well-tested system.

Question: What is the best assessment of this plan?

A. It is correct, because the Cookbook is designed to hold complete, deployable applications.

B. It is a mismatch: the Cookbook is built to review one focused, self-contained pattern, not an entire application, so the submission should be reduced to the reusable pattern before contributing.

C. It is correct, provided the application includes a full test suite.

D. It should go through the same repository as any open-source MCP server contribution.

Correct answer: B

Explanation: The module explicitly calls sending a full application to the Cookbook one of the most common reasons a contribution never gets reviewed, because the Cookbook's review process is built for a single focused pattern demonstrated end to end.

Distractors:

- A: This is the opposite of what the module states about Cookbook scope.
- C: A test suite does not resolve the channel mismatch -- the problem is scope, not verification quality.
- D: MCP servers and tools have their own separate repositories with their own conventions; a full customer-service application is neither an MCP server nor a simple tool fix.

## Question 5

Scenario: An EU-based regulated bank wants an agent that summarizes customer call transcripts, with each summary reviewed by a human before being stored, and all transcript data processed inside the EU.

Question: Which of the following is the infrastructure requirement (as opposed to the functional requirement) in this scenario?

A. The agent produces a summary that a human approves before it is stored.

B. Transcript data must be processed inside the EU.

C. The agent should be fast and accurate.

D. The agent uses a pre-approved prompt template.

Correct answer: B

Explanation: Infrastructure requirements are non-functional deployment constraints derived from questions like residency ("where must data be processed, under which regulation"). Requiring EU-only processing is a residency constraint, which is an infrastructure requirement.

Distractors:

- A: Human approval before storage describes checkable system behavior, making it a functional requirement, not an infrastructure one.
- C: "Fast and accurate" is not a valid requirement of either kind -- it's a vague goal that lacks the detail needed to check or design against.
- D: Using a pre-approved prompt template is closer to a functional/behavioral choice than an infrastructure constraint about where or under what identity the system runs.

## Question 6

Scenario: A team deploys a production application against the alias `"opus"` because it's convenient and automatically stays on the recommended model. Months later, the alias silently advances to a new underlying version, the output shape changes, and a downstream parser breaks. The team tries to roll back but finds no prior pinned version was retained.

Question: What is the root cause, and what should have been done differently?

A. The root cause was a parser bug; the fix is to make the parser more defensive against any output shape.

B. The root cause was using an unpinned alias with no prior version retained; the fix is to pin the full model ID and keep the prior pinned version available for rollback.

C. The root cause was choosing Opus over Sonnet; the fix is to switch model tiers.

D. The root cause was not running the eval suite in development; the fix is to add more unit tests to the agent's tool functions.

Correct answer: B

Explanation: This mirrors the module's alias-incident trace directly: the application never changed, but the alias did, and with no pinned prior version retained there was nothing to roll back to. The fix named in the module is pinning the full model ID, keeping the prior version, and gating promotion through the eval.

Distractors:

- A: A more defensive parser might reduce symptoms but does not address the root cause of an untracked, unpinned production change.
- C: The model tier (Opus vs. Sonnet) is unrelated to the alias-vs-pinned-ID problem described.
- D: The module frames the eval as the deployment gate for promoting new versions, not primarily as a unit-testing exercise for tool functions; the described failure is specifically about the absence of pinning and rollback capability.

## Question 7

Scenario: A team needs to choose a deployment platform for a customer who already runs entirely on AWS and holds an existing compliance certification there, and who also needs the ability to roll back a future model update.

Question: Which combination best satisfies this scenario, per the module's guidance?

A. First-party Claude API, using an Anthropic API key, with a moving alias for the model reference and no version retention.

B. Amazon Bedrock, using an AWS identity reference, with a pinned full model ID, retaining the prior pinned version for rollback.

C. Google Vertex AI, using an AWS identity reference, with a moving alias for the model reference.

D. First-party Claude API, using an AWS identity reference, with a pinned full model ID.

Correct answer: B

Explanation: The customer's existing AWS presence and compliance posture point to Amazon Bedrock, which uses AWS identity and keeps data inside the customer's AWS boundary. Rollback capability requires a pinned full model ID (not a moving alias) plus retaining the prior pinned version.

Distractors:

- A: The first-party API does not match an AWS-committed, already-certified customer, and a moving alias with no version retention makes rollback impossible -- the opposite of what the scenario needs.
- C: Vertex AI uses Google Cloud identity, not AWS identity; mixing an AWS identity reference with Vertex is not how the module describes the platforms working, and a moving alias again defeats rollback.
- D: The first-party API uses Anthropic identity and terms, not an AWS identity reference, so this combination misassigns the identity model to the platform.

## Question 8

Scenario: A team measures the latency of a candidate deployment platform from a developer's laptop in the United States and gets a fast result. The customer's actual users and data are in the EU, and the customer also holds an existing compliance certification on a different cloud provider.

Question: What is the strongest critique of this team's evaluation approach?

A. The latency measurement should have been taken from the customer's actual region against their actual payload, and the compliance certification the customer already holds should weigh heavily on the platform choice.

B. Latency measurements are irrelevant to platform choice; only compliance matters.

C. The team should optimize the parser to reduce measured latency further.

D. The measurement is valid as long as the platform is technically capable of running in the EU.

Correct answer: A

Explanation: The module is explicit that latency numbers are only accurate when measured from the customer's actual region against their actual payload, and that compliance often ends the debate because a customer already certified on one cloud is unlikely to re-certify on another.

Distractors:

- B: The module treats latency, compliance, and cost as three dimensions to measure together, not as one dimension replacing the others.
- C: Parser optimization does not address the fact that the measurement itself was taken from the wrong location, which is the actual defect here.
- D: Technical capability to run in the EU says nothing about the measured latency from the customer's actual location, nor about whether the platform matches the customer's already-held compliance certification.

## Question 9

Scenario: A multi-component application wires an API entry point to a Claude Code task that fetches a customer's public webpage, then passes that fetched content directly into the next component's call as part of its prompt. All three components individually passed their own unit tests before being connected.

Question: What is the security gap in this design, and what should be done about it?

A. There is no gap, because each component already passed its own tests before being wired together.

B. The fetched content is untrusted the moment it leaves the Claude Code task; the seam receiving it needs an explicit control treating that content as data, not as instructions, regardless of how well each component tested in isolation.

C. The gap is that the API entry point lacks a caching layer, which should be added to reduce redundant fetches.

D. The gap is that the MCP server was not used to fetch the content instead of the Claude Code task.

Correct answer: B

Explanation: This matches the module's "seam nobody marked as a boundary" case directly: a component being trusted in isolation does not make the seam leaving it trustworthy. Fetched content is untrusted downstream and must be explicitly treated as data at the next seam, exactly as the security-module injection principles require.

Distractors:

- A: This is precisely the mistaken reasoning the module's example dialogue calls out -- individual test passage says nothing about the untested seam between components.
- C: Caching addresses performance, not the trust-boundary problem of unmarked, unvalidated content crossing into the next component as if it were instructions.
- D: Which component fetches the content is not the issue; the issue is that whichever component fetches it, the receiving seam must treat that content as data.

## Question 10

Scenario: A regulated healthcare customer's security review requires justifying audit logging, data-residency decisions, and permission controls across an entire multi-component application: a first-party API entry point, a Claude Code task, and an MCP server that reaches a patient-records system with full read/write access "to keep things simple."

Question: Based on the module's guidance on least privilege, what is the most likely outcome of this review, and why?

A. The review passes, because the MCP server is the only component that touches sensitive data, and its correctness is what matters.

B. The review likely fails on the MCP server's scope: the application is only as contained as its most privileged seam, so full read/write access where read-only would suffice becomes the weak point even if the other components are well-scoped.

C. The review passes as long as the first-party API entry point performs input validation, regardless of how the MCP server is scoped.

D. The review outcome depends only on which deployment platform was chosen, not on how individual components are scoped.

Correct answer: B

Explanation: The module states directly that an application is only as contained as its most privileged seam -- a single component scoped too broadly becomes the weak point even when every other component is properly scoped. Full read/write access "to keep things simple" is exactly the over-scoping the least-privilege discipline is meant to prevent.

Distractors:

- A: The module rejects this framing; least privilege applies to the whole application, and an over-scoped component undermines the rest regardless of its own "correctness."
- C: Input validation at the entry point is one necessary control among several, but it does not compensate for an over-scoped MCP server elsewhere in the chain.
- D: Platform choice (e.g., Bedrock vs. Vertex) affects residency and identity models, but component-level scoping is a separate discipline that a platform choice alone does not resolve.
