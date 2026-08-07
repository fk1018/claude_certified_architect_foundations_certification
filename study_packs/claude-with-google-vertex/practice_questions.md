# Claude with Google Cloud's Vertex AI Practice Questions

## Question 1

Scenario: A team can call Claude successfully through Vertex AI after enabling Anthropic models and configuring `gcloud`. Their structured extraction app still sometimes returns malformed JSON that breaks downstream parsing.

Question: What is the best next design change?

A. Re-run `gcloud auth application-default login` before each extraction request.

B. Lower temperature to zero and keep asking for JSON in the prompt.

C. Use schema/tool-based structured output with deterministic parsing and validation.

D. Switch from Vertex AI to another provider because provider setup caused the malformed output.

Correct answer: C

Explanation: Provider authentication only enables access. Machine-consumed output needs schema enforcement, parsing, validation, and retry/review patterns.

Distractors:

- A: Authentication does not enforce output shape.
- B: Low temperature improves repeatability but does not guarantee valid or semantically correct JSON.
- D: The failure is output-control design, not necessarily provider choice.

## Question 2

Scenario: A Vertex-hosted chatbot loses track of a customer's previous order number after several turns. Logs show each request sends only the latest user message.

Question: What should the application change?

A. Store and resend relevant conversation history with each request.

B. Increase temperature so Claude can infer missing details.

C. Enable the model again in Vertex AI Model Garden.

D. Use streaming so earlier tokens are visible sooner.

Correct answer: A

Explanation: Conversation state is application-managed. The app must supply relevant prior user, assistant, and tool messages.

Distractors:

- B: Higher temperature worsens repeatability and does not recover missing context.
- C: Model access is already working.
- D: Streaming affects latency, not memory.

## Question 3

Scenario: An exam scenario mentions Google Cloud setup details, but the failure is that a customer-support agent refunds users before verifying identity.

Question: Which fix best matches the certification's tested architecture judgment?

A. Add a note in the Vertex setup guide reminding engineers to verify customers.

B. Enforce the verification step programmatically before refund tools can run.

C. Increase the model's context window so it remembers the policy.

D. Use a faster model so the agent checks identity sooner.

Correct answer: B

Explanation: Required business sequences need deterministic enforcement. Prompt-only or documentation-only approaches are weaker when mistakes have financial impact.

Distractors:

- A: Documentation does not enforce runtime behavior.
- C: More context does not guarantee sequence compliance.
- D: Speed does not enforce policy.

## Question 4

Scenario: A prompt evaluation suite checks whether generated JSON parses, contains required fields, and uses valid enum values.

Question: Which grading approach is best for these checks?

A. Model-based grading with a general rubric.

B. Code-based grading with deterministic validators.

C. Human review of every output before running tests.

D. Reranking outputs by likely quality.

Correct answer: B

Explanation: Parseability, required fields, and enum membership are objective and should be checked deterministically.

Distractors:

- A: Model judges are better for semantic quality, not exact validity.
- C: Human review is too slow for deterministic checks.
- D: Reranking is a retrieval technique, not an output validator.

## Question 5

Scenario: A documentation assistant uses embeddings for RAG but fails whenever users search exact policy IDs and ticket numbers.

Question: What should you add first?

A. BM25 or another lexical retrieval path, then combine it with semantic retrieval.

B. Prompt caching for the full document corpus.

C. Higher temperature to improve recall.

D. A longer system prompt listing every policy ID.

Correct answer: A

Explanation: Exact identifiers are a lexical-search strength. Hybrid retrieval handles both exact and semantic matching.

Distractors:

- B: Prompt caching optimizes repeated prompt prefixes, not retrieval accuracy.
- C: Temperature does not fix missing retrieval.
- D: Listing every ID in the system prompt is brittle and wastes context.

## Question 6

Scenario: An MCP server exposes `lookup_customer`, `get_order`, and `refund_order`. Claude often chooses the wrong lookup tool because descriptions are one sentence each and boundaries overlap.

Question: What is the most effective first improvement?

A. Give Claude access to more tools so it has alternatives.

B. Improve tool names/descriptions, input schemas, examples, and boundary conditions.

C. Disable all tools and ask the user to paste data manually.

D. Move the MCP server from project scope to user scope.

Correct answer: B

Explanation: Tool descriptions and schemas are the primary signals for tool selection. Clear boundaries reduce misrouting.

Distractors:

- A: More overlapping tools usually worsens selection.
- C: This avoids the integration instead of fixing it.
- D: Scope does not address ambiguous tool semantics.

## Question 7

Scenario: A synthesis agent needs verified source claims from RAG results. Current summaries omit source URLs and page references, making audit impossible.

Question: What should upstream retrieval/summarization produce?

A. Longer natural-language summaries without citations.

B. Structured claim-source mappings that downstream synthesis must preserve.

C. A cached prompt prefix with all document names.

D. A single confidence score without evidence.

Correct answer: B

Explanation: Provenance requires structured source metadata attached to claims, not unsupported summaries.

Distractors:

- A: Length does not guarantee provenance.
- C: Caching is not evidence tracking.
- D: Self-reported confidence is poorly calibrated and not auditable.

## Question 8

Scenario: A workflow asks Claude to run three independent compliance checks over the same document, then combine the results.

Question: Which architecture pattern fits best?

A. Parallelization for the independent checks, followed by synthesis.

B. Chaining all checks in a fixed sequence even though none depend on another.

C. Routing to only one checker based on document length.

D. A Vertex setup retry loop before each check.

Correct answer: A

Explanation: Independent subtasks can run in parallel, then be synthesized after all results are available.

Distractors:

- B: Chaining adds unnecessary latency for independent work.
- C: Routing chooses one path; the scenario needs all checks.
- D: Provider setup is unrelated to decomposition.

## Question 9

Scenario: A process has a predictable three-step path: extract metadata, validate fields, then enrich valid records. The team wants the simplest reliable design.

Question: What should they prefer?

A. A fixed chained workflow with validation gates.

B. A fully autonomous agent that decides whether validation is needed.

C. A high-temperature prompt that encourages creativity.

D. A web search tool for every record.

Correct answer: A

Explanation: Known sequences are good fits for workflows. Validation gates provide control and predictability.

Distractors:

- B: An agent adds unnecessary variability when the path is known.
- C: Creativity is not useful for deterministic processing.
- D: Search is irrelevant unless enrichment requires external lookup.

## Question 10

Scenario: Two Claude Code sessions need to implement unrelated features in the same repository at the same time.

Question: What is the safest workspace setup?

A. Run both sessions in the same checkout and resolve conflicts later.

B. Use separate git worktrees and merge after reviewing diffs and tests.

C. Ask both sessions to avoid editing the same files without checking.

D. Disable tests until both sessions finish.

Correct answer: B

Explanation: Worktrees isolate parallel edits and make review/merge boundaries explicit.

Distractors:

- A: Shared checkouts increase accidental collisions.
- C: Prompt instructions do not reliably prevent file conflicts.
- D: Tests are needed to verify independent work before merge.

## Question 11

Scenario: A team uses an MCP server to expose a large document catalog. Claude repeatedly calls exploratory search tools just to discover what documents exist.

Question: What MCP primitive should the server add?

A. A resource that exposes a catalog or hierarchy of available documents.

B. A refund tool with a broader schema.

C. A prompt caching rule for every user question.

D. A forced final-answer tool.

Correct answer: A

Explanation: MCP resources expose app-controlled context and catalogs, reducing unnecessary exploratory tool calls.

Distractors:

- B: Unrelated action tools do not improve catalog visibility.
- C: Caching does not reveal available documents.
- D: Forced final answers do not supply context.

## Question 12

Scenario: A certification question includes computer-use examples from a course section. The answer choices include detailed screen-control setup and a general agentic tool-loop design.

Question: How should you reason for this exam?

A. Prefer detailed computer-use setup because the course mentioned it.

B. Ignore all tool-loop concepts because computer use is out of scope.

C. Keep only the transferable observe-act-tool-loop concept and avoid provider/UI setup details.

D. Memorize the browser automation controls from the course.

Correct answer: C

Explanation: The exam guide excludes computer use specifics, but general agentic loop and tool-use principles remain relevant.

Distractors:

- A: The exam does not test computer-use setup details.
- B: Tool-loop reasoning is still in scope.
- D: UI-control details are not the certification focus.
