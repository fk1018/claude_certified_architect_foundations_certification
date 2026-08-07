# Claude with Amazon Bedrock Practice Questions

## Question 1

Scenario: A team is building a customer-facing assistant on Amazon Bedrock. Most requests are simple account questions, but 8% require multi-step reasoning over policy, order history, and exception handling. The team proposes using the most capable model for every request to maximize quality.

Question: What is the best architecture decision?

A. Use the most capable model for every request because quality always matters more than latency.

B. Use the fastest model for every request because customer-facing applications should always optimize latency.

C. Route simple requests to a faster/lower-cost model and reserve stronger models for complex reasoning cases.

D. Randomly split traffic across all available models and choose the one with the lowest average cost.

Correct answer: C

Explanation: The course frames model selection as a tradeoff among intelligence, speed, and cost. A routed multi-model design lets each subtask use the smallest model that meets quality requirements while preserving stronger reasoning for harder cases.

Distractors:

- A: Overpays in latency and cost for simple cases.
- B: Under-serves complex cases that need stronger reasoning.
- D: Random allocation ignores task requirements and makes quality less predictable.

## Question 2

Scenario: A Bedrock chat app answers "What is 1+1?" correctly. The user then asks "And 3 more?" but Claude responds as if it has no prior context.

Question: What is the root cause?

A. Bedrock and Claude automatically store state, so the model must have selected the wrong tool.

B. The application failed to resend the relevant conversation history in the follow-up request.

C. The model needs a higher temperature to remember conversational context.

D. Streaming must be enabled for multi-turn conversations.

Correct answer: B

Explanation: Claude API calls are stateless from the application perspective. The app must preserve and resend relevant user, assistant, and tool messages.

Distractors:

- A: The course explicitly emphasizes application-managed message history.
- C: Temperature affects sampling, not persistence of prior messages.
- D: Streaming affects response delivery, not memory.

## Question 3

Scenario: A workflow generates AWS EventBridge JSON rules. Claude often wraps the JSON in markdown fences and explanatory prose, causing downstream parsing failures. The team wants a quick improvement for a low-risk internal tool.

Question: Which first change best matches the course material?

A. Use assistant message prefilling plus a stop sequence to steer raw JSON output and trim extra prose.

B. Increase temperature so Claude explores more output formats.

C. Add a disclaimer telling users to manually remove markdown before parsing.

D. Switch to streaming because streamed responses are easier to parse.

Correct answer: A

Explanation: The course shows prefilled assistant messages and stop sequences as direct controls for reducing unwanted wrappers around structured output. For production-grade extraction, tool/schema enforcement and validation would still be stronger.

Distractors:

- B: Higher temperature generally reduces repeatability.
- C: Manual cleanup does not fix the workflow.
- D: Streaming changes delivery timing, not output structure.

## Question 4

Scenario: A production extraction system sends Claude's JSON output into a downstream database. The team already uses a prompt that says "return only valid JSON," but occasional malformed or semantically wrong values still slip through.

Question: What is the best exam-oriented improvement?

A. Use a tool with a JSON schema for structured output, then validate the result before writing downstream.

B. Tell Claude that invalid JSON is not allowed under any circumstances.

C. Use the same prompt with lower temperature and remove all validators.

D. Ask users to check the database after each extraction.

Correct answer: A

Explanation: Tool-based structured output improves schema compliance, and validation catches semantic or business-rule errors that schemas alone may not prevent.

Distractors:

- B: Prompt-only enforcement is probabilistic.
- C: Low temperature helps repeatability but does not replace validation.
- D: Manual cleanup after writes is weaker than pre-write validation.

## Question 5

Scenario: You are designing a reminder assistant with three possible operations: get the current time, add a duration to a date, and create a reminder. Claude frequently chooses the wrong operation because the tool descriptions are short and similar.

Question: What is the best first fix?

A. Combine all operations into one generic `do_datetime_stuff` tool.

B. Expand each tool description with purpose, inputs, outputs, boundaries, and examples.

C. Remove all descriptions so Claude relies only on tool names.

D. Force the create-reminder tool for every request.

Correct answer: B

Explanation: Tool descriptions are a primary signal for selection. Clear boundaries are especially important when tools are related but not interchangeable.

Distractors:

- A: A generic tool hides intent and creates ambiguous inputs.
- C: Removing descriptions worsens selection reliability.
- D: Forced selection is useful only when a specific required tool must run.

## Question 6

Scenario: Claude may answer a user directly or request one or more tools. The current application looks for phrases like "I need to use a tool" in assistant text to decide whether to execute tools.

Question: What should the application do instead?

A. Inspect response structure and `stop_reason`, execute requested tools, return `tool_result`, and continue until final answer.

B. Increase max tokens so Claude has enough room to describe tool requests.

C. Require users to type "tool mode" before asking operational questions.

D. Execute every available tool on every turn and let Claude choose from the results.

Correct answer: A

Explanation: Reliable tool loops inspect structured tool-use responses and stop reasons rather than parsing natural language hints.

Distractors:

- B: More tokens do not solve control-flow detection.
- C: Users should not manage internal tool modes.
- D: Running every tool wastes resources and pollutes context.

## Question 7

Scenario: A RAG system uses only embeddings. It performs well for conceptual questions but fails when users ask about exact incident IDs such as `INC-2023-Q4-011`.

Question: What is the best retrieval improvement?

A. Add lexical search such as BM25 and merge it with embedding results.

B. Increase the model temperature so it considers more possible chunks.

C. Remove chunk metadata to reduce prompt size.

D. Replace all retrieval with a single prompt containing the full document collection.

Correct answer: A

Explanation: Embeddings capture semantic similarity, while BM25 is strong for exact terms, IDs, and names. Hybrid retrieval combines both strengths.

Distractors:

- B: Temperature affects generation, not retrieval matching.
- C: Removing metadata weakens provenance and filtering.
- D: Full-context prompting is often impractical and can degrade attention.

## Question 8

Scenario: A document assistant retrieves chunks that contain the right words but lack enough surrounding context to answer accurately. The source document has strong section-level meaning that gets lost when chunks are split.

Question: Which technique best addresses this?

A. Contextual retrieval: add short source-aware context to chunks before indexing.

B. Remove section headings so every chunk looks uniform.

C. Use only size-based chunks with no overlap.

D. Disable citations to save tokens.

Correct answer: A

Explanation: Contextual retrieval situates each chunk within the larger source before indexing, making retrieved chunks more meaningful in isolation.

Distractors:

- B: Headings often provide important context.
- C: Fixed-size chunks alone may split semantic units.
- D: Citations support trust and do not fix lost context.

## Question 9

Scenario: A team is building an MCP server for a document system. They need Claude to edit documents, the application to include selected document contents when users mention them, and users to invoke a tested "convert to markdown" template.

Question: How should these be modeled?

A. Document editing as a tool, document contents as resources, and markdown conversion as a prompt.

B. Document editing as a resource, document contents as a prompt, and markdown conversion as a tool.

C. Make everything a tool because tools are the only MCP primitive Claude can see.

D. Make everything a prompt because prompts are easier to test.

Correct answer: A

Explanation: MCP tools are model-controlled actions, resources are app-controlled context, and prompts are reusable user/client-invoked templates.

Distractors:

- B: Editing is an action, not read-only context.
- C: MCP also exposes resources and prompts.
- D: Prompts cannot replace actions or context catalogs.

## Question 10

Scenario: An engineer writes a new MCP server with read and edit tools. They immediately connect it to Claude Code and ask it to modify project files. The first run fails because the edit tool schema is wrong.

Question: What should they have done first?

A. Test the MCP server primitives with the inspector before relying on them in a client workflow.

B. Give Claude Code more tools so it can recover from the bad schema.

C. Remove schemas from the MCP tools.

D. Use a user-level server only, because project-level servers cannot be tested.

Correct answer: A

Explanation: The course presents the MCP inspector as a development/debugging tool for validating server behavior before integration.

Distractors:

- B: More tools do not fix a broken interface.
- C: Schemas are part of reliable tool contracts.
- D: Server scope and testability are separate concerns.

## Question 11

Scenario: A team wants three Claude Code instances to work on separate improvements at the same time. They plan to run all three in the same checkout to save disk space.

Question: What is the best course-aligned advice?

A. Use separate git worktrees so each instance has an isolated workspace, then review and merge deliberately.

B. Run all instances in one checkout because Claude Code automatically coordinates file locks.

C. Disable tests until all three instances finish.

D. Ask each instance not to edit the same files and trust the instruction.

Correct answer: A

Explanation: The course uses git worktrees to prevent concurrent Claude Code instances from overwriting or conflicting with each other's file changes.

Distractors:

- B: Automatic coordination should not be assumed.
- C: Tests are important verification, not optional cleanup.
- D: Prompt instructions are weaker than workspace isolation.

## Question 12

Scenario: A production service sends error logs to Claude, which proposes code fixes automatically. Leadership wants the system to deploy every generated fix immediately.

Question: What is the best reliability critique?

A. Automated debugging can help, but production-affecting fixes need guardrails, tests, review, and controlled deployment.

B. Immediate deployment is safe because Claude inspected the logs.

C. The system should use higher temperature to find more creative fixes.

D. Automated debugging should never be used for production systems.

Correct answer: A

Explanation: The course shows automated debugging as powerful, but the exam rewards reliability judgment: production workflows need verification and human or programmatic controls.

Distractors:

- B: Log inspection alone is insufficient.
- C: More creativity does not improve deployment safety.
- D: The pattern can be useful when constrained and verified.

## Question 13

Scenario: A developer asks whether to study the course's computer-use implementation details for the Claude Certified Architect - Foundations exam.

Question: What is the best answer?

A. Study every computer-use limit and API detail because it is a primary exam domain.

B. Ignore the entire agents section because computer use appears there.

C. Keep the transferable tool-loop and agent-design lessons, but do not over-study computer use because the exam guide marks it out of scope.

D. Replace MCP study time with computer-use practice because both involve tools.

Correct answer: C

Explanation: The exam guide explicitly excludes computer use, but the surrounding lessons still reinforce useful ideas about tool calls, environment observation, focused tools, and evaluation.

Distractors:

- A: Computer use is out of scope.
- B: The agents section contains exam-relevant Claude Code, tool-loop, and agent-quality ideas.
- D: MCP is explicitly in scope and should not be displaced.

## Question 14

Scenario: A prompt engineering team keeps improving a meal-plan prompt by intuition. Each iteration sounds better in demos, but regressions appear when users have allergies, unusual goals, or strict constraints.

Question: What should they add?

A. A repeatable prompt evaluation workflow with representative test cases, graders, and iteration.

B. More adjectives in the prompt, such as "excellent" and "high quality."

C. A higher context window so the model sees more examples at once.

D. Streaming to expose partial results sooner.

Correct answer: A

Explanation: The course emphasizes evaluation as the way to measure prompt quality and catch regressions across representative scenarios.

Distractors:

- B: Vague quality words do not measure behavior.
- C: More context does not replace test coverage.
- D: Streaming changes latency, not correctness.
