# Accelerators and IP Contribution Flashcards

## Accelerator Basics

Q: What is an accelerator, in the sense this module uses the word?

A: A working solution packaged so that a future engagement configures a working asset rather than rebuilding from a blank repository -- customer-specific parts are separated out and exposed as parameters.

Domain: D2

Example: A code-review agent built for one customer is turned into a template where the repo path, model ID, and thresholds are parameters instead of hardcoded values, so the next engagement just fills them in.

## Three Asset Types

Q: What are the three categories most reusable work falls into, and what does each bundle?

A: Agent Template (system prompt, tool schemas, loop structure), MCP Server Package (exposed tools, their inputs, and the scope the installing team controls), and Eval Suite (the graded test set and judge rubric).

Domain: D2

Example: A team packages a support-ticket agent as a template, wraps its ticketing integration as an MCP server, and ships the 20-ticket eval set alongside both so a new team can install and verify all three.

## Packaging Checklist Columns

Q: For any accelerator asset, what three things does the packaging checklist require you to decide?

A: What to parameterize (values that change per customer), what to document (environment assumptions, expected inputs, handled failure modes, the defining eval), and what to bundle for audit (data touched, identity acted under, and the action log).

Domain: D2

Example: For an MCP server package, the team parameterizes scopes and credential references, documents each tool's expected inputs, and bundles a log of every customer-system call the server made.

## Hardcoded Template Failure

Q: In the module's packaging postmortem, why couldn't a second team reuse a shipped agent template?

A: Every customer-specific value (repo path, model name, thresholds, prompt fragments) was hardcoded into the loop with no parameters, no documentation of what was customer-specific, and no bundled eval to confirm it still worked -- so the second team had to rewrite it from scratch.

Domain: D2

Example: A second engagement opens the "reusable" template, finds the review threshold buried inside a 200-line function, and gives up trying to configure it in favor of a full rewrite.

## Documentation's Job

Q: What does documentation cover that the code itself cannot show a future builder?

A: The assumptions the asset makes about its environment, the inputs it expects, the failure modes it already handles, and the eval that defines whether it still works.

Domain: D2

Example: A README note says "assumes the target repo has a `pyproject.toml` at the root; fails silently otherwise" -- a fact no amount of reading the agent loop would reveal quickly.

## Audit Log as Package Content

Q: Why does an accelerator need a bundled audit log, not just working code?

A: A regulated customer's reviewer asks what data the asset touches, what identity it acts under, and what log it leaves; an accelerator without that evidence passes a demo but stalls at the first security review.

Domain: D7

Example: A bank's security reviewer rejects an otherwise-working summarization accelerator because it has no log showing which transcripts were read and under which service identity.

## Contributing Back, Defined

Q: What does "contributing back" mean in this module?

A: Moving an asset from private, internal reuse into shared infrastructure through a documented channel, so a team that never spoke to the author can install it and get the same working setup.

Domain: D2

Example: A pattern for handling multi-turn customer-service conversations, built during one engagement, is generalized and submitted to the Claude Cookbook for anyone to use.

## Matching Contribution to Channel

Q: Where does a full multi-component application belong versus a single focused tool?

A: A focused, self-contained pattern goes to the Claude Cookbook; a single tool or fix goes to its own tool/server repository with its own conventions; a full multi-component application is a mismatch for the Cookbook, which is built to review one focused pattern.

Domain: D2

Example: A developer wants to share an entire customer-service app with UI and deployment scripts; it stalls in Cookbook review until only the reusable conversation-handling pattern is extracted and submitted on its own.

## Four Verifiability Requirements

Q: What four things make a contribution something a maintainer can verify without reconstructing the author's intent?

A: The code does one thing, an example shows it running, a test proves it works, and a short statement names the assumptions.

Domain: D2

Example: A PR wrapping a single API call includes a 10-line usage example, one test asserting the parsed response shape, and a note saying "assumes the API key is already set in the environment."

## Stalled PR Root Cause

Q: In the module's stalled-PR exchange, why did a maintainer leave a working pull request unreviewed for three weeks?

A: The code worked for the author, but there was no test to run, no example proving the behavior, and nothing stating what it assumed about the environment -- so the maintainer had nothing to verify it with and it sat at the back of the queue.

Domain: D2

Example: A developer says "the code works, I use it every day" and the maintainer replies that working for the author is not the same as being verifiable by a stranger.

## Rights and Attribution Gate

Q: Why does licensing/attribution review happen before technical review of a contribution?

A: Licensing and attribution decide whether a contribution can be accepted at all; code carried in from a customer engagement may have constraints on where it can go, so confirming the right to contribute it is a gate the contribution must clear first.

Domain: D2

Example: A one-line fix extracted from a customer engagement can't be merged until someone confirms the customer's contract doesn't restrict reuse of that code elsewhere.

## Escalate on Unclearable Licensing

Q: What should you do when engagement code carries a licensing constraint you cannot clear?

A: Do not contribute it -- escalate to the owner instead.

Domain: D2

Example: A developer discovers the customer's MSA prohibits sharing derived code externally, so instead of quietly submitting a "cleaned up" version, they flag it to the engagement owner.

## Functional Requirement, Defined

Q: What makes a statement a valid functional requirement rather than a vague business goal?

A: It names what the system must do with enough detail to check -- a checkable statement of behavior, not a general aspiration like "be fast and accurate."

Domain: D2

Example: "Classify each ticket into one of four queues; draft a reply citing the relevant policy; never auto-send without human approval" is a functional requirement; "help support agents answer faster" is not.

## Four Infrastructure Requirement Questions

Q: What four questions do you ask to derive infrastructure requirements from a business problem?

A: Latency (how fast, measured where the user is), Scale (how many requests, at what peak), Residency (where must data be processed, under which regulation), and Identity (who acts, under what credentials, what must be auditable).

Domain: D2

Example: For an EU bank's call-summarization agent, the answers are: latency fast enough for support staff to act on, unspecified scale, EU-only residency, and a human identity that approves each summary before storage.

## EU Bank Requirements Checkpoint

Q: For an EU bank's call-summarization agent, which is the functional requirement and which is the infrastructure requirement: "a human approves each summary before storage" vs. "transcript data must not leave the EU"?

A: "A human approves each summary before storage" is functional (checkable system behavior); "transcript data must not leave the EU" is an infrastructure/residency requirement (a non-functional deployment constraint).

Domain: D2

Example: The functional requirement becomes an eval check ("was a summary ever stored without approval?"); the infrastructure requirement becomes a platform-selection constraint (choose Bedrock or Vertex with EU routing).

## Systems Lifecycle Phases

Q: What are the seven phases of the systems lifecycle as applied to a Claude application?

A: Requirements, Design, Build, Test, Deploy, Operate, Iterate.

Domain: D2

Example: A team captures residency and latency needs (Requirements), picks Bedrock and a pinned model (Design), writes the agent (Build), runs evals (Test), ships behind a version gate (Deploy), tracks cost and errors in production (Operate), and feeds a recurring failure mode back into new requirements (Iterate).

## Lifecycle Gates

Q: What is a "gate" in the systems lifecycle, and why does it matter for regulated engagements?

A: A gate is a decision point required to move from one phase to the next (e.g., not moving design to build until the platform satisfies residency, not promoting to production until the new version clears the eval against baseline); it is where a regulated engagement keeps control, and skipping it is what keeps deadline pressure from silently bypassing review.

Domain: D2

Example: A team wants to start building against a platform before confirming it meets the customer's residency requirement; the gate blocks that move until Design confirms the platform choice.

## Lifecycle Phase Placement

Q: Which lifecycle phase does "pinning the full model ID and keeping the prior version" belong to, and which phase does "gating promotion on the eval result" belong to?

A: Pinning the model ID and retaining the prior version is a Deploy-phase activity; gating promotion on the eval result is also Deploy (the eval is the promotion gate at deployment).

Domain: D2

Example: Both actions happen at the moment a new version is about to go live, not earlier during Build or Test.

## Deployment Platform, Defined

Q: What is a "deployment platform" in this module's sense, and what usually determines which one is chosen?

A: The environment where the Claude workload runs (first-party API, Claude Platform on AWS, Amazon Bedrock, Google Vertex AI, or a third-party platform); the customer's existing cloud, identity management, and compliance agreements usually determine the choice more than technical merit.

Domain: D2

Example: A customer already certified on AWS gets routed to Claude in Amazon Bedrock rather than the first-party API, to avoid a fresh compliance review.

## First-Party API vs. Claude Platform on AWS

Q: What is the key difference between the first-party Claude API and Claude Platform on AWS?

A: The first-party API is Anthropic's own environment and typically gets new features first; Claude Platform on AWS is accessed through the customer's AWS account using Anthropic's own model IDs and lifecycle, but inference itself is Anthropic-operated, outside the AWS boundary.

Domain: D2

Example: A customer wants to bill through their AWS account and use the same model IDs as the first-party API, but data still leaves the AWS boundary for inference -- so it does not satisfy an "inference must stay in AWS" residency rule.

## Two Bedrock Integrations

Q: What are the two ways Claude is available through Amazon Bedrock, and how do they differ?

A: Claude in Amazon Bedrock uses the Messages API at `/anthropic/v1/messages` with broad feature parity to the first-party API (confirm feature-specific gaps); Claude on Amazon Bedrock (legacy) uses the InvokeModel/Converse APIs with ARN-versioned model identifiers.

Domain: D2

Example: A team already using InvokeModel from an older integration keeps pinning via ARN-versioned identifiers rather than migrating immediately to the Messages API path.

## Microsoft Foundry Hosting Forms

Q: What are the two hosting forms Claude takes inside Microsoft Foundry, and why does the distinction matter for a regulated customer?

A: Hosted on Azure (a specific model subset, inference end-to-end on Azure infrastructure) and Hosted on Anthropic (all other Foundry Claude models, inference on Anthropic-operated infrastructure); residency assumptions depend on which hosting form the specific model uses, so it must be confirmed per model and deployment with Microsoft.

Domain: D2

Example: A customer assumes all Foundry-hosted Claude models satisfy their EU residency rule, but an Anthropic-hosted Foundry model in their stack does not, because inference does not run entirely on Azure infrastructure.

## Identity and Residency Are Platform-Determined

Q: Does your application code determine where data is processed and under what identity, or does the platform?

A: The platform determines it, not your code -- Bedrock uses AWS identity and keeps data inside the customer's AWS boundary, Vertex uses Google Cloud identity and boundary, and both offer regional routing when residency is a constraint.

Domain: D7

Example: Switching a workload from the first-party API to Bedrock changes its identity and residency posture even if not a single line of the agent's prompt or tool code changes.

## Alias vs. Pinned Model ID

Q: What is the difference between a model alias and a pinned full model ID, and why does it matter for production?

A: An alias (like "opus" or a pre-4.6 name without a date suffix) is convenient but evolves over time and can resolve to a different snapshot without warning; a pinned full model ID resolves to a fixed snapshot, so an upstream model change becomes a deliberate choice instead of a silent production change.

Domain: D5

Example: `model = "claude-haiku-4-5"` can silently move to a new snapshot; `model = "claude-haiku-4-5-20251001"` stays fixed until the code is changed on purpose.

## Claude 4.6+ Pinning Convention

Q: How does model-ID pinning change starting with Claude 4.6?

A: For Claude 4.6 and later, the model ID alone pins to a specific snapshot; for earlier models, the ID plus a date suffix is required -- always verify the current convention at platform.claude.com at build time, since this is time-sensitive.

Domain: D5

Example: A team building against Claude 4.6 no longer needs to append a date suffix to get a fixed snapshot, unlike their earlier Haiku 4.5 deployment.

## Versioning Discipline (Three Parts)

Q: What three things does "pin what ships" require beyond just choosing a model ID?

A: Pin the specific model version (not the alias), version the prompt and the asset alongside the code, and keep the prior version available so a regression can be rolled back.

Domain: D5

Example: A team ships v2 of both the model pin and the prompt template together, tagged in source control, with v1 still deployable if v2 regresses.

## Alias Incident Postmortem

Q: In the module's "deployment that broke when the model alias moved" trace, what was the root cause and why couldn't the team roll back?

A: The application deployed against a moving alias; when the alias advanced to a new model version with no app change, the output shape changed and downstream parsing broke. Rollback failed because no pinned prior version had been retained.

Domain: D5

Example: A parser expecting a `"summary"` key throws a KeyError overnight after an alias silently resolves to a new model version, and there's no earlier pinned snapshot to fall back to.

## Eval as Deployment Gate

Q: How does an eval suite function differently at deployment time versus during initial development?

A: During development it is a one-time test that proves the asset works; at deployment it becomes a promotion gate -- a new version is sent to a portion of traffic, compared against the pinned baseline score, and promoted or rolled back based on the result.

Domain: D2

Example: A new Sonnet version scores 2 points below the pinned baseline on the bundled eval, so the team holds it back from full traffic instead of promoting it.

## Three Comparison Dimensions

Q: What three dimensions does this module say a deployment-platform choice must be measured on to survive a procurement/security review?

A: Latency, compliance, and cost.

Domain: D2

Example: Before signing off, a security team wants to see measured round-trip latency from the customer's region, a compliance certification match, and a total-cost-per-call figure -- not just "we picked the platform we know."

## Measuring Latency Correctly

Q: Why is a latency measurement taken from a developer's laptop unreliable for a platform decision?

A: The number is only accurate when measured from the customer's actual region against their actual payload; a laptop measurement hides the round-trip penalty that appears once the workload runs where the customer actually is.

Domain: D2

Example: A platform tests at 180ms from a US developer's laptop but the customer's EU-based deployment sees much higher real-world latency once compliance-driven regional routing is added.

## Compliance as Pass/Fail

Q: How should a regulated customer's compliance/residency requirement be treated relative to latency and cost?

A: As pass-or-fail, not as a tradeoff to balance -- a regulated financial or healthcare customer will reject a platform that fails residency regardless of how well it performs on latency or cost.

Domain: D7

Example: A platform with excellent latency and the lowest cost is still rejected outright because it cannot guarantee EU-only data processing for a regulated bank.

## What Drives Total Cost

Q: Beyond per-token rate, what actually moves total deployment cost across platforms?

A: Data egress, platform fees, and integration effort -- per-token rates are broadly aligned across platforms, so a lower token price can still cost more once transfer and integration are factored in.

Domain: D2

Example: Platform A has a slightly higher token price but no egress fees and minimal integration work, ending up cheaper overall than Platform B's lower token price plus heavy data-transfer charges.

## Familiarity-Over-Residency Postmortem

Q: In the module's "platform picked on familiarity" postmortem, why was the integration rejected at security review despite passing functional tests?

A: The team chose the platform they knew best because migration was fast, but that platform did not satisfy the customer's data-residency requirement; a different, less-familiar platform with regional deployment options would have satisfied it. The compliance check happened too late, at the security review instead of during scoping.

Domain: D7

Example: A reviewer asks "where is data processed?" at the go/no-go review, and the answer disqualifies a platform whose only advantage had been that the team already knew how to build on it.

## Multi-Component Application, Defined

Q: What is a multi-component application in this module's sense, and what risk does connecting components introduce?

A: An application coordinating more than one Claude capability into a single workflow (e.g., an API request triggers a Claude Code task, which reaches a customer system through an MCP server); every connection between components creates a place where identity, secrets, and untrusted input can cross.

Domain: D7

Example: An API entry point calls a Claude Code task to fetch a webpage, then passes that content into an MCP-server-backed call against a customer database -- three components, at least two seams.

## Trust Boundary, Defined

Q: What is a trust boundary, and where does it apply the injection/access-control principles from earlier security work?

A: The point where data or instructions move from one deployment environment to another; it is exactly where injection defenses and access controls apply -- content fetched at one component is untrusted the moment it reaches the next component and must be treated as data, not instructions.

Domain: D7

Example: Content a Claude Code task fetched from a customer's public webpage is untrusted the instant it is handed to the next component in the pipeline, even though the Claude Code task itself ran correctly.

## Trust Does Not Carry Over

Q: If every component in a multi-component app passed its own tests individually, is the seam connecting them automatically trustworthy?

A: No -- a component being trusted in isolation does not make the seam leaving it trustworthy; each seam where data crosses needs its own explicit control, because trust does not carry over across a boundary.

Domain: D7

Example: Dev A wires up three individually-tested components and assumes it's safe; Dev B points out that the fetched content flowing into the next call was never marked as untrusted data at that seam.

## Unmarked Seam Postmortem

Q: In the module's "seam nobody marked as a boundary" transcript, what specifically went wrong?

A: A Claude Code task's fetched content was passed straight into the next component's call as part of the prompt, with no control treating it as untrusted data; if the fetched content carried instructions, the next component would run them, because the seam between the two trusted components was never marked as a boundary.

Domain: D7

Example: `next_call(input=fetched)` runs fetched webpage content directly as part of the next prompt with no sanitization or "treat as data" wrapping.

## Least Privilege Across an Application

Q: How does least privilege apply differently to a multi-component application than to a single component?

A: It applies to the application as a whole -- each component should get only the access its specific task needs, and the application is only as contained as its most privileged seam; one over-scoped component becomes the weak point even if every other component is properly scoped.

Domain: D7

Example: If the orchestrating API component has full database write access "just in case," that access is the real risk even though the MCP server itself is tightly scoped to read-only.

## Multi-Component Integration Map

Q: For the three components in this module's integration map (first-party API, Claude Code task, MCP server), what is each one's boundary and control?

A: First-party API: boundary is the incoming request; control is input validation plus the identity the call runs under. Claude Code task: boundary is the content it fetched, untrusted downstream; control is treating that content as data at the next seam. MCP server: boundary is the system access it holds on the app's behalf; control is scoping to least privilege and logging the access.

Domain: D7

Example: An MCP server that reaches a customer's ticketing system is scoped to read-only ticket access and logs every call it makes, satisfying its column in the map.

## Regulated Review Scope

Q: What must a regulated review justify across a multi-component Claude application?

A: Audit logging, data-residency decisions, and permission controls across the full application -- not just one component -- with ZDR and HIPAA BAA eligibility confirmed per component against the Anthropic Trust Center and platform.claude.com before scoping.

Domain: D7

Example: A healthcare customer's review asks not just "is the MCP server scoped correctly" but "does every component in this pipeline, including the orchestrating API, satisfy our BAA and residency requirements."

## Escalate on Unsecurable Seam

Q: What should you do when a trust-boundary seam in a multi-component app cannot be secured with an available control?

A: Do not ship around it -- escalate to a human owner.

Domain: D7

Example: A team can't find a reliable way to sanitize content fetched from an uncontrolled external source before it reaches the next component, so they flag the design to their security lead instead of shipping with an unmarked seam.

## Cumulative Task: Three Defect Layers

Q: The module's cumulative diagnostic task plants one defect in each of which three layers?

A: The packaging layer (a hardcoded customer-specific value where a parameter belongs), the deployment-and-versioning layer (an unpinned model alias instead of a full pinned model ID), and the multi-component boundary layer (fetched content passed into the next call untreated as untrusted data).

Domain: D2

Example: The shipped snippet has `model="opus"` (unpinned alias, defect 2), a hardcoded `repo_path` (defect 1), and `next_call(input=fetched)` with no data-vs-instructions handling (defect 3) -- three separate fixes across three separate module topics.

## Module's Overall Throughline

Q: What single idea ties together packaging, contributing, deployment/versioning, platform comparison, and trust boundaries in this module?

A: The point where code starts working is where this module's work begins -- a working build is not yet reusable, verifiable, deployable-on-purpose, defensible to procurement/security, or safe across its own seams; each topic makes that gap concrete in a different area.

Domain: General

Example: A working demo agent still needs parameters and a bundled eval to be reused, a test and example to be contributed, a pinned model ID to be deployed safely, measured latency/compliance/cost to be defended, and marked seams to pass a multi-component security review.
