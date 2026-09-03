# Team Enablement and Operational Productivity Practice Questions

## Question 1

Scenario: An Architect is rolling Claude Code out to four engineering departments (120 developers total). Leadership wants "everyone live by Monday" and proposes sending one enablement email with login instructions to the whole org at once.

Question: What is the strongest objection to this plan, based on the module's guidance?

A. Email is the wrong communication channel; it should be a company-wide meeting instead.

B. A single mass switch-on skips the champion-and-batch pattern, risking a spike of confused first-time prompts and a quiet retreat to old habits, with no local expert or working example in any department.

C. 120 developers is too many people for Claude Code to support technically.

D. The rollout should wait until every department has written its own CLAUDE.md first.

Correct answer: B

Explanation: The module's worked example directly contrasts a single mass rollout (which produces confusion and retreat) with champion-then-batch, where each champion proves a real workflow and builds local expertise before the broader group gets access.

Distractors:

- A: The failure isn't the communication medium, it's the absence of a phased adoption pattern; a well-run meeting would have the same problem.
- C: The module never suggests a technical scaling limit on team size; the issue is adoption design, not capacity.
- D: A CLAUDE.md is part of the shared environment, but the module's fix for this scenario is champions proving the workflow first, not requiring every department to pre-author documentation before anyone gets access.

## Question 2

Scenario: A platform team wants to distribute a release-notes-generation procedure to their 40-engineer group. It must be centrally updatable, and if a future edit breaks the output format, they need to roll it back without touching every engineer's setup individually.

Question: Which distribution mechanism fits, and why?

A. An org-provisioned Skill under Organization settings > Skills, because it reaches everyone at once.

B. A Claude Code project Skill committed to the team's repository, because it versions with git.

C. A plugin assigned to the 40-engineer group, because plugins provide group targeting, version-controlled updates, and rollback.

D. An API Skill called through the Messages API, because it can be updated centrally.

Correct answer: C

Explanation: The scenario needs group-scoped access plus centrally managed versioning and rollback — exactly the governance a plugin provides. This mirrors the module's cautionary example, where a Skill pushed as a flat bundle (skipping plugin governance) had no way back when an edit broke it.

Distractors:

- A: Org-provisioned Skills reach the whole organization, not a scoped 40-engineer group, and don't emphasize rollback as their defining feature.
- B: A project Skill versions with a specific repository via git, but it isn't the mechanism for group-targeted, centrally revocable distribution across a defined group of people.
- D: API Skills are for programmatic use by a partner's own products, not for a team of engineers to use directly, and the scenario doesn't describe programmatic invocation.

## Question 3

Scenario: A team has had Claude Code licenses for three months. Usage logs show developers only ever paste error messages into a chat panel and read back suggested fixes manually; no one uses file edits, test runs, or the team's packaged Skills.

Question: What best names this failure and what is the underlying cause?

A. Lumpy adoption — a few developers are overusing the tool while most ignore it.

B. Stalling at basic chat — the team has access but was never configured or enabled for deeper workflow integration.

C. Judgment erosion — the team is shipping code it doesn't understand.

D. A spend posture failure — the team is using an overly expensive model tier for chat.

Correct answer: B

Explanation: This is the textbook description of stalling at basic chat: the team has access to the tool but never advanced past question-answering because no one enabled or configured for real workflow enablement (repository-aware assistance, tool use, packaged Skills).

Distractors:

- A: Lumpy adoption is about uneven usage across the team (some heavy, some none); here everyone uses it the same shallow way.
- C: Judgment erosion is about accepting AI-generated output without understanding it; this scenario describes underuse, not unchecked merges.
- D: Nothing in the scenario describes model tier or cost; the failure is workflow depth, not spend.

## Question 4

Scenario: A team ships an AI-generated change quickly. It passes code review and the automated test suite, and goes to production, where it later leaks data through an input it never validated. In the post-incident review, the original author cannot explain why the code handled that input the way it did.

Question: What control, if it had existed, was most directly designed to catch this before it shipped?

A. A faster model that would have generated better code the first time.

B. A verification checklist covering correctness, security, maintainability, and human understanding, including the question of whether the person merging can explain what the code does and why.

C. A stricter code-review SLA requiring two approvers instead of one.

D. Disabling AI-assisted coding until a formal audit is completed.

Correct answer: B

Explanation: The scenario is the module's own cautionary example. Tests were green and review passed (shallow checks), but no one asked the human-understanding question the checklist would have forced. The checklist's four dimensions, especially human understanding, are the control built specifically to catch this failure mode.

Distractors:

- A: A more capable model doesn't guarantee the author understands or can explain the resulting code; this doesn't address the root cause (unverified understanding).
- C: More approvers doesn't fix the gap if none of them are prompted to ask whether the code's behavior is understood — the missing check is substantive, not just a headcount issue.
- D: Disabling AI-assisted coding is not the module's guidance; the fix is a verification discipline, not abandoning the workflow.

## Question 5

Scenario: A support engineer tells the Architect: "Answer quality on our production deployment has been sliding for two months. No code has changed. Dashboards have stayed green the whole time." The team wants to know where to look first.

Question: What is the best first step, based on the module's symptom-to-cause reasoning?

A. Immediately upgrade to the most capable model available; a stronger model will compensate for whatever is wrong.

B. Roll back the last code deployment, since that is the usual cause of production issues.

C. Treat this as a candidate case of model, prompt, or retrieval drift — since the corpus likely grew and the retrieval index may not have kept pace — and investigate those architecture causes first.

D. Disable caching so every call pulls fresh content, on the assumption that stale cached responses are the cause.

Correct answer: C

Explanation: This mirrors the module's own "drift that waited for a quarterly review" example: gradual quality decline with no code change is a canonical symptom that traces to model change, prompt change, or retrieval drift as the corpus grows. This is exactly the kind of symptom-to-cause mapping a runbook should capture.

Distractors:

- A: Upgrading the model treats a possible symptom with brute force without diagnosing the actual cause, and doesn't address retrieval drift if that's the real issue.
- B: The scenario explicitly states no code has changed, so a code rollback is not indicated and wastes time chasing the wrong cause.
- D: There's no evidence in the scenario pointing to caching; this jumps to an unrelated fix without diagnosis.

## Question 6

Scenario: An Architect resolves a recurring "tool started failing" incident for a team for the third time this quarter, each time by personally investigating and applying a fix.

Question: What is missing from the Architect's approach, based on the module's guidance on operational support?

A. Nothing — resolving the incident quickly each time is exactly what good operational support looks like.

B. The Architect should hand the incident off to a different team member each time, to spread the workload.

C. The Architect should capture the symptom-to-cause-to-action path in a runbook so the team can resolve the recurring issue without the Architect next time.

D. The Architect should switch the team to a different tool to eliminate the recurring failure.

Correct answer: C

Explanation: The module distinguishes firefighting (resolving one incident yourself) from support that lasts (teaching the team the symptom-to-cause path they can follow again). A recurring issue resolved the same way three times is a clear signal that a runbook entry — not repeated personal firefighting — is overdue.

Distractors:

- A: Repeatedly resolving the same issue personally is explicitly the firefighting pattern the module says to move past, since it keeps the team dependent on the Architect for a now-familiar problem.
- B: Rotating who does the firefighting doesn't address the root gap — no one on the team can resolve it without direct investigation each time.
- D: Nothing in the scenario indicates the tool itself is unfixable; the module's fix for a recurring, diagnosable issue is documentation and self-sufficiency, not necessarily replacement.

## Question 7

Scenario: A partner company wants to let their own product call a specific Claude capability programmatically, without any of their end users interacting with Claude Code or an Organization settings panel directly.

Question: Which of the four Skills distribution mechanisms fits this need?

A. Org-provisioned Skill.

B. Claude Code project Skill.

C. Plugin distributed to a group.

D. API Skill, invoked via the Messages API.

Correct answer: D

Explanation: API Skills are the mechanism built for programmatic invocation by a partner's own products — exactly the scenario described, where the capability is called by the partner's product rather than accessed by human team members through an org panel or a repository.

Distractors:

- A: Org-provisioned Skills are for organization members using Claude directly, not for a partner's product calling a capability programmatically.
- B: Project Skills are filesystem artifacts scoped to a Claude Code project repository, not something a partner's separate product calls via API.
- C: Plugins target human groups with install preferences and versioning; they aren't the programmatic invocation path a partner's own product would use.

## Question 8

Scenario: A team lead says: "We gave everyone Claude Code access and let each developer pick whichever model they like for every task, with no caps. Adoption is high and everyone loves it." Three months later, finance flags a large and unexpected increase in AI spend.

Question: What team-setup decision was most likely skipped?

A. Skills distribution — the team should have used a plugin instead of an org-provisioned Skill.

B. Spend posture — model defaults, allowlists, effort guidance, and spend/rate/per-user caps were never set.

C. Rollout — the team should have used a champion-and-batch approach instead of enabling everyone at once.

D. Diligence — the team should have implemented a verification checklist for AI-generated code.

Correct answer: B

Explanation: Unmanaged model choice at team scale is the exact failure the module warns about: leaving model defaults, allowlists, effort guidance, and caps unset lets work quietly route to more expensive tiers, and that choice multiplies across every member and request. High adoption with no caps is the setup for exactly this outcome.

Distractors:

- A: The scenario is about cost, not about how a Skill was packaged or governed; Skills distribution mechanism choice doesn't explain a spend spike.
- C: High adoption suggests rollout worked fine; the problem described is purely a cost-control gap, not an adoption-pacing gap.
- D: Diligence and the verification checklist address code quality and trustworthiness, not AI spend; they don't explain a billing surprise.
