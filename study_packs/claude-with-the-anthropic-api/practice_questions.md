# Building with the Claude API Practice Questions

These questions are exam-aligned study material based on the captured course outline, the readable non-video API key lesson, quiz completion metadata, and `exam_guide_pdf.txt`. Video-specific lesson content was explicitly out of scope for this course.

## Question 1

Scenario: A team is building a support agent that must look up orders, issue refunds, and escalate unclear cases. Claude returns a response containing a `tool_use` block for `lookup_order`.

Question: What should the application do next?

A. Ignore the block and ask Claude to provide the answer in text.

B. Execute the requested tool, append a `tool_result` message, and call Claude again.

C. Run every available support tool so Claude has maximum information.

D. Convert the tool call into a system prompt for the next request.

Correct answer: B

Explanation: Tool use is an agentic loop: inspect `tool_use`, execute the requested operation, return `tool_result`, and let Claude reason over the result.

Distractors:

- A: The model explicitly requested a tool; ignoring it breaks the loop.
- C: Running every tool increases cost, risk, and irrelevant context.
- D: Tool results belong in conversation history as results, not system instructions.

## Question 2

Scenario: A document extraction pipeline often returns valid JSON syntax, but downstream systems reject records because totals do not add up.

Question: What is the best improvement?

A. Increase temperature so Claude explores more possibilities.

B. Add semantic validation and retry with specific validation feedback.

C. Ask Claude to be more careful in the system prompt.

D. Switch from JSON to free-form Markdown.

Correct answer: B

Explanation: Tool/schema enforcement prevents many syntax errors, but semantic errors require validation and targeted feedback.

Distractors:

- A: Higher temperature usually reduces repeatability.
- C: Vague caution is weaker than concrete validation errors.
- D: Free-form output makes downstream validation harder.

## Question 3

Scenario: A prompt-eval suite checks whether every generated record contains required fields and valid enum values.

Question: Which grading approach fits best?

A. Code-based grading.

B. Model-based grading.

C. Manual review only.

D. A higher model temperature.

Correct answer: A

Explanation: Required fields and enum validity are deterministic checks, so code-based grading is more reliable and cheaper than a model judge.

Distractors:

- B: Model grading is useful for semantic quality, not exact rules.
- C: Manual review does not scale for simple deterministic checks.
- D: Temperature is not an evaluation method.

## Question 4

Scenario: A team wants Claude to judge whether support replies are empathetic, accurate, and complete. The criteria require nuanced reading.

Question: What should the eval use?

A. Model-based grading calibrated with examples and review.

B. Only JSON schema validation.

C. Grep for positive words like "sorry" and "understand".

D. Disable evaluation because empathy is subjective.

Correct answer: A

Explanation: Semantic quality judgments are a good fit for model-based grading when calibrated with representative examples and human spot checks.

Distractors:

- B: Schema validation checks structure, not nuanced quality.
- C: Keyword checks are brittle and easy to game.
- D: Subjective qualities can still be evaluated with criteria and calibration.

## Question 5

Scenario: An API integration needs lower latency in a chat UI. The output is still free-form text for a human user.

Question: Which feature is most directly useful?

A. Prompt caching.

B. MCP resources.

C. Response streaming.

D. Batch processing.

Correct answer: C

Explanation: Streaming lets the UI show partial output as it is generated, improving perceived latency.

Distractors:

- A: Caching helps repeated stable prefixes, not necessarily first-token UX.
- B: Resources expose context catalogs; they do not stream output.
- D: Batch processing is for non-blocking offline workloads.

## Question 6

Scenario: A search agent often misses exact policy IDs but performs well on conceptual questions.

Question: What retrieval change is most appropriate?

A. Remove source citations.

B. Increase the embedding dimension only.

C. Ask Claude to infer policy IDs from context.

D. Add lexical search such as BM25 or hybrid retrieval.

Correct answer: D

Explanation: Lexical search is strong for exact identifiers, while embeddings are strong for semantic similarity. Hybrid retrieval can cover both.

Distractors:

- A: Removing citations reduces reliability.
- B: Larger embeddings do not guarantee exact-token matching.
- C: Inferring IDs risks hallucination.

## Question 7

Scenario: An MCP server exposes a list of available internal documents and a separate operation that updates a ticket.

Question: How should these be modeled?

A. Both as resources because they relate to external systems.

B. Document list as an MCP resource, ticket update as an MCP tool.

C. Both as tools because Claude can read them.

D. Put both into a system prompt.

Correct answer: B

Explanation: Resources expose contextual catalogs; tools perform actions.

Distractors:

- A: Updating a ticket is an action.
- C: A read-only catalog is better as a resource.
- D: System prompts are not dynamic integration interfaces.

## Question 8

Scenario: A coordinator agent has access to 18 tools. It frequently calls the wrong tool when several names overlap.

Question: What should the team do first?

A. Add all tool outputs to context before Claude chooses.

B. Force a random tool call to gather more data.

C. Raise temperature to improve exploration.

D. Scope tools by agent role and clarify names/descriptions.

Correct answer: D

Explanation: Tool selection reliability improves when tools are scoped, differentiated, and described with boundaries.

Distractors:

- A: More context can worsen noise and cost.
- B: Random tool calls are unsafe and inefficient.
- C: Higher temperature can make tool choice less predictable.

## Question 9

Scenario: A workflow always validates input, extracts metadata, enriches records, and writes a report in that order.

Question: What architecture is best?

A. A fully autonomous agent with every tool enabled.

B. A single prompt that asks for all steps at once.

C. A fixed chained workflow with validation at each step.

D. A RAG index with no workflow logic.

Correct answer: C

Explanation: Chaining is appropriate when the sequence is known and each step depends on the previous output.

Distractors:

- A: An adaptive agent is unnecessary for a predictable path.
- B: A single prompt reduces control and observability.
- D: RAG retrieves context; it does not enforce process order.

## Question 10

Scenario: A research system sends independent topic summaries to three specialized subagents before synthesis.

Question: Which workflow pattern is being used?

A. Chaining.

B. Parallelization.

C. Routing.

D. Prompt caching.

Correct answer: B

Explanation: Independent subagent work can be done in parallel, then combined by a synthesis step.

Distractors:

- A: Chaining is sequential dependency.
- C: Routing selects a path based on task type.
- D: Prompt caching is an API optimization.

## Question 11

Scenario: A code assistant should use different specialist flows for bug reports, refactors, and documentation updates.

Question: Which pattern fits the first step?

A. Streaming.

B. Code-based grading.

C. Prompt caching only.

D. Routing.

Correct answer: D

Explanation: Routing classifies the task and sends it to the appropriate specialist flow or tool set.

Distractors:

- A: Streaming affects output delivery, not task selection.
- B: Grading evaluates outputs after work is done.
- C: Caching does not choose a workflow path.

## Question 12

Scenario: A developer creates an Anthropic API key during a training exercise, closes the dialog, and did not copy it.

Question: What should they do?

A. Search browser history for the key.

B. Commit the visible key name and hope it is enough.

C. Delete the old key and generate a new one.

D. Ask Claude to reconstruct the key from the workspace name.

Correct answer: C

Explanation: The readable course page states the key is displayed once; if it is lost, generate a replacement.

Distractors:

- A: Secrets should not be recovered from insecure places.
- B: A key name is not a usable credential.
- D: Claude cannot reconstruct a secret API key.
