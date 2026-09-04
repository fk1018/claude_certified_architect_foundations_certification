# Team Enablement and Operational Productivity Flashcards

## Team Environment

Q: What does "deploying the environment as a shared configuration" mean for a Claude Code team?

A: The team agrees on a project-level baseline — a shared CLAUDE.md, an agreed set of tools/MCP servers, and a permission posture — that is centrally reviewable, versionable, and improvable, instead of everyone drifting into personal setups.

Domain: D7

Example: Instead of each engineer configuring their own MCP servers and permissions, the team commits one CLAUDE.md and permission profile to the repo that every new hire starts from.

## Champion-And-Batch Rollout

Q: What is the recommended pattern for rolling Claude out to multiple departments?

A: Grant a champion per department first, let them prove the workflow on a real task, then seed adoption batch by batch rather than switching everyone on at once.

Domain: D7

Example: A 200-person org enables one champion per department for two weeks to convert a real workflow, then has each champion run a peer session before the next batch gets access.

## Four Team-Setup Decisions

Q: What four decisions does the Architect own when setting up Claude for a team?

A: Environment (shared config), rollout (champion + batches), Skills distribution (which mechanism), and spend posture (model defaults, allowlists, effort guidance, caps).

Domain: D7

Example: Before letting a team log in, the Architect finalizes the CLAUDE.md, names department champions, decides how the release-notes skill will be distributed, and sets a per-user monthly spend cap.

## Org-Provisioned Skill

Q: When should a Skill be distributed as an owner-provisioned, org-wide Skill?

A: When the capability genuinely should reach every member of the organization at once, with no particular need for group targeting, versioning, or rollback.

Domain: D7

Example: A general "summarize meeting notes" Skill that every employee, regardless of team, should be able to use is uploaded under Organization settings > Skills.

## Plugin Distribution

Q: What does bundling a Skill into a plugin provide that an org-provisioned Skill or a flat bundle does not?

A: Group targeting, install preferences (required, installed-by-default, available, not available), version-controlled updates, and rollback.

Domain: D7

Example: A compliance-review Skill that must be centrally updatable and revocable is bundled into a plugin and assigned to the compliance group, so a bad edit can be rolled back org-wide.

## Project Skill

Q: What is a Claude Code project Skill and when does it fit?

A: A filesystem artifact living in the project repository (`.claude/skills/`) that versions with the repo and is scoped to the projects that carry it — fits a coding convention or tool set one team shares on every project.

Domain: D7

Example: An engineering team commits a `.claude/skills/` folder with their code-review checklist so it travels with the repo and updates through normal pull requests.

## API Skill

Q: What is an API Skill and who uses it?

A: A Skill called programmatically via the Messages API by a partner's own products, rather than accessed by human team members directly.

Domain: D7

Example: A partner's SaaS product calls a packaged Skill through the Messages API container every time a user in their own app triggers a document-generation feature.

## Centrally Managed Configuration Is Not Skills Distribution

Q: Is centrally managed Claude Code configuration one of the four Skills distribution mechanisms?

A: No — it is a separate settings channel: server-managed settings delivered from Anthropic's servers on an hourly polling cycle when users authenticate, distinct from org Skills, plugins, project Skills, and API Skills.

Domain: D7

Example: An exam question that lists "centrally managed configuration" as a Skills-distribution option alongside plugins is testing whether you know it's actually a settings mechanism, not a Skills path.

## The Skill With No Way Back

Q: What went wrong when a platform team's release-notes Skill was bundled and assigned to a 40-engineer group without going through proper plugin governance?

A: The Skill was pushed as a flat bundle without version-controlled updates or rollback; a bad prompt edit broke the output format across every team using it, and the fix required manual re-editing while bad output kept shipping.

Domain: D7

Example: This is why any shared asset more than one person depends on needs versioning and rollback — distribute it inside a governed plugin with an identified owner.

## Spend Posture

Q: What four levers make up a team's spend posture?

A: Model defaults (which model a session starts on), model allowlists/restrictions (which models the team may switch to), effort guidance (how hard the model works), and spend/rate/per-user caps.

Domain: D7

Example: An admin sets Sonnet as the default model, restricts the team from switching to the most expensive tier without approval, and caps per-user monthly spend.

## Unmanaged Model Choice At Scale

Q: Why does unmanaged model choice matter more at team scale than for an individual user?

A: Leaving model choice unmanaged can quietly route work to a more capable, more expensive tier than the task requires — and at team scale that choice multiplies across every member and every request.

Domain: D7

Example: If ten developers each occasionally switch to the priciest model for routine tasks, the org absorbs that markup across thousands of requests per month.

## Workflow Integration

Q: Where should AI assistance live to actually pay off for a developer team?

A: Inside the existing workflow — the editor, the review process, the test loop — rather than in a separate chat window visited occasionally.

Domain: D7

Example: Claude reviews a pull request automatically as part of the existing review process, instead of a developer having to remember to paste the diff into a chat window.

## Lumpy Adoption

Q: What is "lumpy adoption" and how is it avoided?

A: A failure mode where a few developers use AI tooling heavily while the rest barely touch it, so the team never realizes the real gain and practice never standardizes; avoided by the champion-and-batch rollout, which spreads usage deliberately.

Domain: D7

Example: Without a batch rollout, two enthusiastic engineers use Claude Code daily while the other eight on the team never open it, and the team can't tell if the tool actually helps.

## Stalling At Basic Chat

Q: What does "stalling at basic chat" mean and why does it happen?

A: The team uses Claude only as a question-answering box and never advances to higher-value workflows like tool use, repository-aware assistance, or packaged Skills, because no one configured for enablement past the first step — access alone is not adoption.

Domain: D7

Example: A team has Claude Code licenses for everyone but only ever pastes error messages into chat, never using it to edit files, run tests, or apply a shared Skill.

## Diligence

Q: What is diligence, as one of Anthropic's four AI Fluency competencies, and what does it mean for deployment specifically?

A: Diligence is taking responsibility for what we do with AI and how we do it; deployment diligence means taking responsibility for verifying and vouching for the outputs we use or share.

Domain: D7

Example: A developer who merges AI-generated code personally verifies it meets the same bar as hand-written code, rather than assuming it's fine because it compiled.

## Verification Checklist

Q: What is the verification checklist and what four dimensions must it cover?

A: The explicit set of checks AI-generated output must pass before reaching production, built internally by the team, covering correctness, security, maintainability, and human understanding.

Domain: D7

Example: A team's checklist requires a passing regression suite (correctness), a vulnerability scan (security), a readability/style check (maintainability), and the author explaining the change in review (human understanding).

## Automating The Checklist

Q: How does a team turn the verification checklist from a judgment call into a repeatable gate?

A: Automate whatever check can be automated — a regression test suite and an eval set turn correctness and behavior verification into a gate that runs on every change, rather than something a reviewer has to re-derive by hand each time.

Domain: D7

Example: Instead of a reviewer manually re-checking behavior on every AI-generated pull request, CI runs the existing regression suite plus a small eval set automatically.

## Judgment Erosion

Q: What is judgment erosion and what incident illustrates it?

A: The risk that a team ships AI-generated output it no longer understands because it passed shallow checks (green tests, a passed review) — illustrated by a generated change that passed review and tests but leaked data through an unvalidated input, because the author could not explain why the code handled that input the way it did.

Domain: D7

Example: A reviewer approves a PR because "the tests are green," without ever asking whether the author can explain the logic — exactly the gap a human-understanding check would have caught.

## Operational Support As Translation

Q: What is the Architect's core value when an operational issue lands, versus what the team typically identifies?

A: The team identifies a symptom (latency spike, degraded output, tool failure), not a cause; the Architect's value is connecting that symptom to its architecture cause. Resolving one incident yourself is firefighting — teaching the symptom-to-cause path is support that lasts.

Domain: D7

Example: A team reports "the chatbot's answers got worse," and the Architect traces it to the retrieval index falling behind a growing document corpus, then shows the team how to check for that next time.

## Runbooks And Escalation Paths

Q: What do runbooks and escalation paths each provide for team self-sufficiency?

A: A runbook captures known symptom-to-cause-to-action paths so the team can resolve recurring issues without the Architect; an escalation path identifies who handles what and when an issue must leave the team.

Domain: D7

Example: A runbook entry states "gradual quality decline with no code change → check model, prompt, or retrieval drift → re-index or review recent prompt edits," letting a first-line engineer resolve it without paging the Architect.

## Drift That Waited For A Quarterly Review

Q: What operational failure illustrates why a missing runbook entry matters?

A: A deployment's dashboards stayed green for a quarter while answer quality quietly declined due to a growing retrieval corpus the index hadn't kept pace with; because the runbook lacked an entry linking gradual quality decline to model/prompt/retrieval drift, the issue wasn't caught until a scheduled review, though a first-line engineer could have resolved it in an afternoon had the path been written down.

Domain: D7

Example: This is why the Architect should write the symptom-to-cause path into the runbook the first time it's diagnosed, not just fix it and move on.
