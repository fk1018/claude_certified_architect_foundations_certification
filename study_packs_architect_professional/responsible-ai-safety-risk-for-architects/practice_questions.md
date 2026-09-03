# Responsible AI, Safety & Risk for Architects Practice Questions

## Question 1

Scenario: An architect is designing an internal assistant for a partner whose policy prohibits users from viewing records belonging to other business units. During testing, Claude refused every overtly harmful prompt the team tried, so the team concluded no additional control was needed for cross-unit data access and shipped without one.

Question: What is the most accurate diagnosis of this design decision?

A. It is correct, because Claude's trained refusals generalize to any policy violation, harmful or not.

B. It is a gap, because trained refusals cover broad harm categories, not deployment-specific rules like cross-unit data isolation, which must be enforced in an application-layer control.

C. It is correct, because the system prompt already states the partner's policy, and instructions are sufficient enforcement.

D. It is a gap, but only because the team should have added a second output filter rather than an authorization check.

Correct answer: B

Explanation: Training-time alignment reduces broad classes of harmful output but has no knowledge of a specific partner's data-handling or authorization rules. Any deployment-specific policy — including cross-unit data isolation — must be enforced by a layer the architect builds, typically an authorization check, not assumed from trained behavior.

Distractors:

- A: Trained refusals cover broad harm; a domain-specific access rule is not the same class of problem and is not reliably generalized to.
- C: System-prompt instructions steer behavior but are not enforcement — an adversarial or unusual input can talk the model out of a stated instruction.
- D: An output filter judges text, not authorization to access a specific record; the correct fix is an authorization control, not another content filter.

## Question 2

Scenario: A customer-support agent has an `issue_refund` tool. The current design has one control: an output filter that inspects the model's generated text before it's shown to the user. A trace shows the model called `issue_refund`, the refund executed, and only then did the output filter run — inspecting text that described an action that had already happened.

Question: What is the correct fix?

A. Replace the output filter with a stronger judge model that scores toxicity more accurately.

B. Add tool-call authorization before the refund tool executes, since output screening only judges text and cannot prevent a side-effecting action that has already run.

C. Move the output filter earlier in the pipeline so it runs before the model call.

D. Add a second output filter after the first one to double-check the refund description.

Correct answer: B

Explanation: Output screening evaluates generated text, not actions with side effects. A refund is irreversible once issued, so the control that must sit before the tool executes is deterministic tool-call authorization — checking whether this caller may perform this action in this context — not another layer of text inspection after the fact.

Distractors:

- A: A stronger judge model still only evaluates text after the action already occurred; it doesn't address the missing authorization gate.
- C: Output screening inherently runs on the model's output, which comes after the model call; moving it "before the model call" doesn't correspond to what output screening checks.
- D: Stacking more output filters does nothing for an action that already executed before any filter ran.

## Question 3

Scenario: An architect's team builds a custom input-screening classifier to catch jailbreak attempts. Under high load, the classifier service occasionally times out. No explicit behavior was defined for what happens when it times out.

Question: What will happen by default, and why is this a risk?

A. The system will fail closed by default, blocking legitimate traffic during outages, which is an acceptable tradeoff.

B. The system will most likely fail open by default, silently passing unscreened traffic through, which looks guarded while providing no protection.

C. Anthropic's built-in safety controls will automatically compensate for the outage, so the risk is minimal.

D. The classifier will automatically retry until it succeeds, so no explicit failure behavior is needed.

Correct answer: B

Explanation: If an architect does not explicitly choose fail-open or fail-closed behavior, the surrounding code decides for you — and the default is almost always fail open. A guardrail that silently passes traffic when it errors is worse than no guardrail at all, because it gives the appearance of protection without any of the function.

Distractors:

- A: Fail-closed is not the default without an explicit decision; assuming it happens automatically is incorrect.
- C: Anthropic's built-in controls are a separate layer and do not compensate for the failure of an operator-built classifier — that classifier's fail behavior is the architect's responsibility.
- D: Nothing in the design described automatic retry logic, and even with retries, the architect still must decide what happens during the time the service is unavailable.

## Question 4

Scenario: A RAG-based knowledge assistant screens all user input for jailbreak and injection patterns before the model call. A security reviewer asks whether the system is also protected against instructions embedded inside retrieved documents.

Question: What is the correct architectural answer?

A. User-input screening already covers this, since any injected instruction eventually appears in the model's context, which the same classifier inspects.

B. No separate control is needed, because retrieved content is not "input" in the security sense and carries no policy risk.

C. A separate control is needed: retrieved content and tool outputs should be screened before being appended to context, since input screening only inspects what the user sends directly and cannot see instructions arriving through retrieval.

D. Output screening on the model's final response is sufficient to catch any instruction that was embedded in a retrieved document.

Correct answer: C

Explanation: Indirect prompt injection — instructions arriving through retrieved content or tool outputs — is the dominant injection vector in enterprise deployments with retrieval or tool use. Because input screening only inspects the user's direct message, a retrieved document reaches the model after input screening has already passed the request, requiring a dedicated classifier applied to retrieved content and tool outputs before they enter context.

Distractors:

- A: Input screening runs before the model call and only inspects the user's submitted message; it does not re-inspect content retrieved later in the pipeline.
- B: Retrieved content is exactly the vector the course identifies as the dominant enterprise injection risk — it carries real policy risk.
- D: Output screening evaluates the model's generated response for safety, not whether malicious instructions were present earlier in context; by the time output screening runs, the model may have already acted on the injected instruction (e.g., via a tool call).

## Question 5

Scenario: An architect is deciding whether a check on the request path should be model-based or deterministic. The check in question is: "Is this caller authorized to issue a refund on this order in this context?"

Question: Which approach is correct, and why?

A. Model-based, because judging authorization requires nuanced language understanding that rules cannot capture.

B. Deterministic, because authorization must be a decision you can prove and replay for audit purposes — an allowlist, identity check, and scope validation.

C. A hybrid where a judge model makes the primary call and a deterministic rule only logs the outcome.

D. Model-based, because it is faster and cheaper than building and maintaining an allowlist.

Correct answer: B

Explanation: Tool-call authorization should almost always be deterministic. Authorization decisions must be provable and replayable for audit purposes, which a probabilistic model-based judgment cannot reliably guarantee. A clear allowlist plus identity and scope checks gives you a decision you can defend to a reviewer.

Distractors:

- A: Authorization is a bounded, definable rule (is this caller permitted to take this action in this context), not an ambiguous language-understanding problem — the opposite of what favors a model-based check.
- C: The course frames authorization as needing to be deterministic itself, not merely logged after a model-based judgment; the decision, not just the audit trail, needs to be deterministic.
- D: Cost/speed is not the deciding factor here; the deciding factor is auditability and reliability, which deterministic checks provide and model-based checks do not.

## Question 6

Scenario: A credit-decision support system uses a model that passed Anthropic's published fairness evaluations. Months after launch, a regulator questions why approval rates differ across regions. The team discovers their retrieval corpus over-represents certain historical cases, but they had not logged enough to prove or disprove this as the cause.

Question: What was the underlying architectural mistake?

A. The team should have chosen a different model with better fairness evaluations.

B. The team treated fairness as a property fully handled by the model provider and did not instrument the injection points — like the retrieval corpus — that they controlled.

C. The team should have added a stricter output filter to catch unfair outcomes before they reached the user.

D. The team failed to add a human-in-the-loop review step for every credit decision.

Correct answer: B

Explanation: Fairness enters at architect-controlled injection points — the retrieval corpus, prompt framing, few-shot examples, and downstream routing — none of which the model provider tested or can see. Passing the model's own fairness evaluations says nothing about skew introduced by your corpus. Without decision-level logging at those points, the team could not explain the outcome or rule out the corpus as the cause.

Distractors:

- A: A different model wouldn't fix a skewed retrieval corpus, which is an architecture-level issue independent of the underlying model's own fairness evaluations.
- C: An output filter checks safety/policy compliance of generated text; it does not detect statistical skew arising from an unrepresentative corpus, and it doesn't provide the explainability a regulator needs.
- D: While review routing is a related control, the root problem described is a lack of instrumentation and logging at the fairness injection points, not the absence of per-decision human review.

## Question 7

Scenario: A benefits-eligibility system routes decisions to human reviewers whenever the model's confidence score falls below a fixed threshold, regardless of whether the decision is easily reversible or low-cost if wrong. Reviewer queues have grown to hundreds of items daily, and reviewers report approving items without reading them carefully.

Question: What is the best fix?

A. Lower the confidence threshold further so fewer items are routed to review.

B. Route based on the combination of confidence, reversibility, and cost: send only low-confidence decisions that are also irreversible or high-cost to pre-action review, and let confident, reversible, low-cost decisions through automatically.

C. Keep routing by confidence alone, but add a second reviewer to double the queue capacity.

D. Remove the confidence-based routing entirely and rely only on trained model behavior to prevent bad outcomes.

Correct answer: B

Explanation: Confidence alone does not set the stakes of a decision — reversibility and cost of a wrong answer do. Routing by confidence alone, without factoring in stakes, either floods the queue (as happened here) or lets high-stakes decisions through unreviewed. The correct rule routes low-confidence, high-stakes (irreversible or high-cost) decisions to a person, and lets confident, low-stakes decisions proceed automatically, keeping the review queue focused and the reviewer's attention meaningful.

Distractors:

- A: Lowering the threshold changes volume but doesn't fix the underlying problem that confidence alone isn't a valid proxy for stakes — it could still route trivial decisions to review while missing high-stakes ones with moderate confidence.
- C: Adding reviewer capacity treats the symptom (queue size) without addressing why the queue is full of low-value items in the first place.
- D: Trained model behavior does not enforce this partner-specific routing policy at all; removing the control leaves high-stakes decisions with no human oversight.

## Question 8

Scenario: A team deploys an agent workflow that requires explicit sign-off from a human before every single tool call the agent makes, including trivial, low-risk ones. After a few weeks, reviewers are approving nearly everything within seconds of it appearing in their queue.

Question: What does this describe, and what does the course recommend instead?

A. This is optimal design, since more approval checkpoints always increase safety.

B. This describes consent fatigue; the recommended pattern is to reduce per-step approvals and move review to higher-value checkpoints, such as plan review or exception handling, gating only irreversible or high-stakes actions.

C. This describes a data-exposure risk that should be fixed by adding output screening.

D. This is correct behavior, and the reviewers should simply be replaced with more diligent staff.

Correct answer: B

Explanation: Requiring sign-off on every action creates consent fatigue: reviewers, faced with excessive approval volume, start clicking through without meaningfully reviewing. Anthropic's agent-autonomy research found that per-step approval adds friction without meaningful safety gain, and recommends monitoring with intervention at higher-value checkpoints (like plan-level review) — the same pattern that led Claude Code to move to plan review rather than per-step approval.

Distractors:

- A: More checkpoints do not automatically mean more safety; excessive low-value checkpoints degrade review quality through consent fatigue.
- C: This scenario describes a review-routing/oversight problem, not a data-exposure risk — the fix is architectural checkpoint redesign, not output screening.
- D: The problem is structural (too many low-value approval requests), not a staffing or diligence issue on the reviewers' part.

## Question 9

Scenario: A team building a regulated deployment selects a delivery route and entry point that survives HIPAA constraints, and considers the compliance work finished. Months later, a security reviewer asks for evidence that protected health data has been handled under a signed Business Associate Agreement (BAA) throughout the deployment's life. The team has only the original design document.

Question: What is missing from this team's compliance posture?

A. Nothing — a compliant entry point choice is itself sufficient proof of compliance.

B. A named accountable owner and a living evidence artifact (such as the signed BAA plus the enabled configuration) for the control, revalidated over time — a design document alone is not accepted as proof.

C. A stronger output filter that screens for health-related terms in real time.

D. A second, redundant compliant entry point in case the first one is later found non-compliant.

Correct answer: B

Explanation: Frameworks like HIPAA state outcomes, not implementations, and choosing a compliant route is only a prerequisite. Each obligation must become a specific control, an accountable owner, and a living evidence artifact a reviewer can inspect (a signed agreement, a configuration screen, a returned log query). A design document that identifies a control with no owner and no evidence is indistinguishable, at audit time, from a control that isn't running.

Distractors:

- A: A compliant entry point is necessary but explicitly not sufficient — the course draws this exact distinction as the "Watch Out" for this section.
- C: A content filter for health terms is a runtime screening measure; it does not evidence a BAA obligation, which is about the underlying legal/contractual and configuration relationship, not text scanning.
- D: Redundant entry points don't address the missing owner and evidence artifact — the gap is governance, not architecture choice.

## Question 10

Scenario: A vendor tells an architect, "Our platform never uses customer data to train our models." The architect is completing a compliance control register for a HIPAA-regulated deployment and needs to determine data retention posture.

Question: What is the correct interpretation of the vendor's statement?

A. It also confirms the data is not retained or logged, since training exclusion and retention are the same guarantee.

B. It is a statement about training use only; retention for logging, abuse prevention, legal compliance, or audit purposes is a separate claim that must be verified independently.

C. It means the data is automatically deleted immediately after each request.

D. It is irrelevant to the compliance register, since training-use policy has no bearing on any compliance framework.

Correct answer: B

Explanation: The course explicitly warns not to collapse training-use and retention into the same claim: data can be excluded from model training by default while still being retained or monitored for logging, abuse prevention, legal compliance, or configured audit purposes. Each is a distinct claim that needs its own evidence in the compliance register.

Distractors:

- A: This conflates two independent claims the course specifically calls out as distinct — training exclusion says nothing about retention.
- C: Nothing in the vendor's statement implies immediate deletion; retention policy must be confirmed separately.
- D: Training-use policy is directly relevant to data-handling compliance obligations and belongs in the register as its own line item, separate from retention.

## Question 11

Scenario: An architect is auditing a third-party Skill before allowing it into a production environment. The audit finds no anomalous network calls, no shell execution, and no out-of-scope file access — the bundle appears clean and matches its stated purpose as a document formatter.

Question: What should the architect do next?

A. Approve the skill for unrestricted use, since a clean audit is sufficient proof of safety.

B. Approve the skill, but still run it with least privilege in a sandbox with limited file and network access and no standing credentials, because a clean audit doesn't guarantee the skill won't fetch code at runtime that wasn't in the audited bundle.

C. Reject the skill regardless of audit outcome, since all third-party skills are inherently unsafe.

D. Skip sandboxing since the audit already confirmed no code-execution risk exists.

Correct answer: B

Explanation: The audit tells you what's in the bundle you reviewed, but a skill that passes review clean can still reach out at runtime to fetch code that was never in the package you read. The audit and runtime confinement are two separate, complementary controls — you should use both, because no single control works perfectly without the other.

Distractors:

- A: "Approve, unrestricted" ignores that runtime confinement is still needed even after a clean audit — the course explicitly warns against relying on the audit alone.
- C: Blanket rejection contradicts the course's guidance that a clean audit plus a trusted-source policy and sandboxing are legitimate compensating controls that let you use skills responsibly.
- D: Sandboxing is recommended regardless of audit outcome specifically because the audit cannot see runtime-fetched code — skipping it defeats the "net" the course describes.
