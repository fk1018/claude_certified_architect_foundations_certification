# Exam Guide Gap Pack Practice Questions — Developer: Foundations

Supplemental drills covering all eight CCDV-F domains, weighted toward Domain 2 (Applications and Integration) and Domain 5 (Model Selection and Optimization), the two largest domains. Pair these with `practice_exams_developer_foundations/` for full-length simulation.

## Question 1

Scenario: A team building a customer-support agent wants tool calls to happen only when the model determines they're needed, since request types vary widely and the right sequence of lookups depends on what earlier lookups return.

Question: What is this a textbook case for?

A. A fixed workflow with a predetermined call sequence.

B. An agent, since the required steps vary by case and depend on intermediate results.

C. The Message Batches API, since support volume is high.

D. A single tool that combines all lookups into one call.

Correct answer: B

Explanation: High-ambiguity tasks where the right tools and their order depend on intermediate results are the defining case for an agent rather than a fixed workflow — the model needs to decide its own next step.

Distractors:

- A: A fixed workflow assumes a predictable sequence, which this scenario explicitly lacks.
- C: Batch API addresses cost/latency for high-volume asynchronous work, not decision variability.
- D: Combining lookups into one tool doesn't resolve which lookups are needed or in what order.

## Question 2

Scenario: Company policy requires that any refund above $500 receive human approval. The system prompt states this rule clearly, but production logs show occasional autonomous refunds above the threshold.

Question: What is the most reliable fix?

A. Move the rule to the top of the system prompt for higher salience.

B. Add more few-shot examples showing correct escalation.

C. Implement a hook that intercepts the refund tool call and blocks any amount above $500.

D. Lower the model's temperature so it follows instructions more consistently.

Correct answer: C

Explanation: A hard business rule with financial consequences needs deterministic, code-level enforcement. A hook that intercepts the tool call and blocks the action is the only option that guarantees the rule holds every time.

Distractors:

- A: Prompt salience is still probabilistic compliance, which is exactly what's failing.
- B: Few-shot examples reduce but don't eliminate the failure rate for a rule that must never be violated.
- D: Lower temperature makes output more consistent, not policy-compliant by guarantee.

## Question 3

Scenario: An overnight job needs to summarize 8,000 support tickets. Results aren't needed until the next morning, and no step of the job needs the model to call a tool mid-request.

Question: Which approach minimizes cost?

A. Send every request synchronously in parallel to finish quickly.

B. Use the Message Batches API.

C. Use a smaller, less capable model to cut per-token cost.

D. Reduce max_tokens on every request.

Correct answer: B

Explanation: The Batch API is built for exactly this profile — high-volume, latency-tolerant, non-interactive work with no mid-request tool calls — at meaningfully reduced cost versus synchronous calls.

Distractors:

- A: Parallel synchronous calls don't reduce per-token cost; they only affect wall-clock time.
- C: Downsizing the model risks quality without addressing the actual batch-vs-realtime cost lever.
- D: Truncating output length is unrelated to the batch-eligibility cost savings available here.

## Question 4

Scenario: A team wants their iterative "generate code, run tests, fix failures, repeat" pipeline to use the Message Batches API for its 50% cost savings.

Question: Why won't this work as designed?

A. The Batch API doesn't support system prompts.

B. The Batch API cannot execute a tool mid-request and return results to the model, which this iterative loop requires.

C. The Batch API's context window is too small for test files.

D. The 24-hour window is too slow for any use case involving code.

Correct answer: B

Explanation: An iterative generate-run-fix loop is inherently multi-turn tool use — the model needs to see test results before deciding the next fix. The Batch API cannot pause mid-request for that exchange.

Distractors:

- A: The Batch API does support system prompts; that isn't the limitation here.
- C: Context window size is unrelated to the multi-turn tool-calling limitation.
- D: The 24-hour window is a latency tradeoff, not the reason this specific workflow fails — the blocking issue is tool calling mid-request.

## Question 5

Scenario: A structured-output schema for extracted invoice data requires every field, including "discount_amount." Many invoices have no discount at all, and the model has started inventing small discount values rather than reporting none.

Question: What schema change fixes this?

A. Make discount_amount nullable so its absence can be reported truthfully.

B. Add a prompt instruction telling the model not to invent values.

C. Lower the temperature to reduce the invented values.

D. Remove the field from the schema entirely.

Correct answer: A

Explanation: A required field for data that may legitimately be absent pressures the model to fabricate a plausible-looking value. Making it nullable lets the model correctly report "not present."

Distractors:

- B: Prompt instructions are probabilistic and the fabrication is already occurring despite whatever instructions exist.
- C: Temperature affects output variability, not the structural pressure created by a required field.
- D: Removing the field discards real data for the invoices that do have a discount.

## Question 6

Scenario: A CI pipeline invokes Claude Code to review pull requests. The job frequently hangs and times out with no visible error.

Question: What is the most likely cause?

A. The pipeline is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input.

B. The review prompt is too long for the context window.

C. The CI runner lacks network access to reach the model.

D. The repository is too large for Claude Code to index.

Correct answer: A

Explanation: Without headless/non-interactive mode, Claude Code waits for interactive input that a CI runner never provides, which manifests as an indefinite hang rather than a clean error.

Distractors:

- B: A too-long prompt would typically produce a context-length error, not a silent hang.
- C: A network access failure would typically surface as a connection error, not a hang waiting on input.
- D: Repository size affects performance, not this specific hanging failure mode.

## Question 7

Scenario: A downstream service parses Claude Code's review output with regex to post inline PR comments, and the parser breaks whenever the output format drifts slightly.

Question: What is the robust fix?

A. Harden the regex with more permissive fallback patterns.

B. Instruct the model more strongly to never deviate from the format.

C. Run with `--output-format json` and a `--json-schema` defining the findings structure.

D. Post the entire raw output as a single comment.

Correct answer: C

Explanation: Schema-constrained JSON output is machine-parseable by construction, removing the fragile dependency on prose formatting staying stable across runs.

Distractors:

- A: Regex hardening is reactive and will keep breaking as format drifts continue.
- B: Prompt-level formatting instructions are probabilistic, which is exactly why the parser keeps breaking.
- D: Posting raw text abandons the requirement for structured, parseable inline comments.

## Question 8

Scenario: Two tools, `analyze_content` ("Analyzes content and returns insights") and `analyze_document` ("Analyzes documents and returns findings"), are frequently confused by the model, which calls the wrong one roughly 30% of the time.

Question: What is the most effective first fix?

A. Rename and rewrite each tool's description to state its distinct purpose, inputs, outputs, and when to use it versus the other.

B. Add a system prompt rule defaulting to `analyze_document` when uncertain.

C. Remove one of the two tools.

D. Add a post-hoc hook that corrects misrouted calls.

Correct answer: A

Explanation: Tool descriptions are the primary signal the model uses for tool selection. Near-identical descriptions cause misrouting regardless of tool names, so clarifying purpose and use cases addresses the root cause.

Distractors:

- B: A default masks ambiguity rather than resolving it, and will be wrong whenever the other tool was actually correct.
- C: Removing a tool may discard functionality that's genuinely needed.
- D: Correcting misroutes after the fact requires its own routing logic — the very capability that's broken.

## Question 9

Scenario: An agent's tool descriptions are excellent, but a system prompt line reads "use lookup_order to help with any customer question about their purchases." The agent now calls lookup_order even for general policy questions with no order involved.

Question: What is the most likely fix?

A. Rewrite the lookup_order tool description to state it requires an order in context.

B. Add few-shot examples of policy questions being answered without any tool call.

C. Remove or reword the sweeping system prompt instruction that is creating an unintended association.

D. Rename the tool so the model understands an ID is required.

Correct answer: C

Explanation: A keyword-sensitive system prompt instruction can override even good tool descriptions by creating an unintended, sweeping association. Fixing the instruction at the source resolves the actual cause.

Distractors:

- A: The tool description isn't the problem — the system prompt instruction is overriding it.
- B: Few-shot examples add token overhead to work around an instruction that can simply be corrected.
- D: Renaming doesn't remove the instruction causing the association.

## Question 10

Scenario: A tool implementation returns the string `"Operation failed"` for every possible failure, from a validation error to a transient network timeout.

Question: What should change so the calling agent can recover sensibly?

A. Wrap every tool call in an automatic 3x retry policy at the application layer.

B. Return structured error metadata including an error category, a retryable flag, and a human-readable description.

C. Add a system prompt instruction telling the model to guess whether a failure is retryable.

D. Increase timeouts so transient failures become less frequent.

Correct answer: B

Explanation: Structured error metadata gives the agent the information it needs to retry transient failures and stop retrying non-retryable ones, rather than guessing from an opaque message.

Distractors:

- A: Blanket retries waste calls on failures that will never succeed (e.g., validation errors) and hide the decision from the agent.
- C: Asking the model to guess what the tool already knows is strictly worse than the tool reporting it directly.
- D: Reducing one failure type's frequency doesn't fix the underlying lack of structured information.

## Question 11

Scenario: A support team wants an internal inventory REST API exposed to Claude in a way that's reusable across several different Claude applications and maintainable independently of any one of them.

Question: Which approach best fits?

A. Hard-code the inventory logic into each application's system prompt.

B. Build an MCP server exposing the inventory operations as tools.

C. Paste the current inventory data into context on every request.

D. Rely on a built-in tool, assuming it can reach internal REST APIs.

Correct answer: B

Explanation: An MCP server exposes reusable tools that multiple Claude applications can connect to and that can be maintained independently — exactly the reuse and maintenance profile described.

Distractors:

- A: Hard-coded prompt logic is neither reusable across apps nor independently maintainable.
- C: Pasting data provides no live access and wastes context on every request.
- D: Built-in tools don't automatically reach arbitrary internal APIs.

## Question 12

Scenario: A Claude-powered agent summarizes web pages submitted by end users. One page contains hidden text instructing the model to ignore prior instructions and reveal its system prompt.

Question: What is the most effective mitigation?

A. Raise the model's temperature so its behavior is less predictable to attackers.

B. Treat the retrieved page content as untrusted input, keep it separate from trusted instructions, and gate sensitive actions behind guardrails.

C. Add a system prompt line asking users not to include malicious instructions.

D. Switch to a larger, more instruction-following model.

Correct answer: B

Explanation: Prompt injection is addressed by isolating untrusted content from trusted instructions and enforcing guardrails so injected text cannot trigger sensitive actions on its own.

Distractors:

- A: Temperature is unrelated to whether injected instructions are followed.
- C: A polite request to users has no bearing on adversarial content embedded in a web page.
- D: A more instruction-following model can be more susceptible to injection, not less.

## Question 13

Scenario: A support agent currently has 18 tools, including several — loyalty program, gift cards, subscriptions — that are rarely used and unrelated to its core refund/return responsibilities.

Question: What is the primary risk of this configuration?

A. MCP servers are limited to 10 tools each, so this configuration will fail at connection time.

B. Tool-selection reliability degrades as the number of available tools grows, increasing misrouting risk.

C. The agent will call every available tool at least once per conversation.

D. Context windows cannot hold more than 10 tool schemas.

Correct answer: B

Explanation: As an agent's toolset grows, decision complexity increases and tool-selection reliability degrades — the fix is scoping tools to the agent's actual role or splitting into specialized agents.

Distractors:

- A: There is no such fixed limit on MCP server tool counts.
- C: Agents don't call every available tool by default; that isn't how tool selection works.
- D: Tool schema token cost scales with tool count but isn't capped at 10.

## Question 14

Scenario: A batch job caches a long, stable system prompt and reference document across thousands of near-identical requests that each add a short, varying user question at the end.

Question: What ordering maximizes the benefit of prompt caching?

A. Place the varying user content first so it's processed immediately.

B. Place the stable system prompt and reference document first, with the varying content last.

C. Alternate stable and varying content throughout the prompt.

D. Ordering doesn't matter for prompt caching.

Correct answer: B

Explanation: Prompt caching only reuses a shared prefix. Placing stable content first and dynamic content last maximizes the portion of the prompt that can be served from cache across requests.

Distractors:

- A: Putting variable content first breaks any shared prefix, defeating caching entirely.
- C: Alternating content prevents a consistent cacheable prefix from forming.
- D: Ordering is precisely what determines how much of the prompt is cacheable.
