# MSO Foundations Flashcards

## Tokens As The Unit Of Cost

Q: What does Claude actually read and price its usage in, instead of characters or words?

A: Tokens. Everything the model processes — prompt, conversation history, tool definitions, tool results, and the response itself — is counted in tokens, and tokens are the unit of both pricing and the context-window budget.

Domain: D5

Example: When estimating whether a feature will fit in the context window or what it will cost per call, an engineer counts tokens across the system prompt, history, and tool results, not word count.

## Chars-Per-Token Is Not Fixed

Q: Why shouldn't you memorize a fixed characters-per-token ratio?

A: The characters-per-token average depends on the tokenizer of the specific model and differs between model generations, so any ratio rule of thumb is model-dependent and should be confirmed at build time.

Domain: D5

Example: A cost estimate built on a "4 characters per token" rule from an older model generation may be inaccurate for a newer model with a different tokenizer.

## Context Window As A Fixed Budget

Q: What does the context window hold, and what kind of budget is it?

A: A fixed total-token budget per request that holds the system prompt, the full conversation so far, any injected documents, every tool result, and the model's output all at once.

Domain: D5

Example: A support-bot session with a long system prompt, ten turns of history, and three tool results all draw from the same single context-window budget on the next call.

## Context Window Failure Mode 1: Oversized Input

Q: What happens when a request's input is already larger than the context window before generation starts?

A: The request is rejected with a validation error before any generation begins.

Domain: D5

Example: Pasting an entire 500-page manual plus a long conversation history into one call that exceeds the model's window returns an error immediately, with no partial output.

## Context Window Failure Mode 2: Mid-Generation Ceiling

Q: What happens when input fits inside the context window but generation reaches the ceiling mid-response?

A: The model stops and returns the output generated so far, with a `model_context_window_exceeded` stop reason, rather than raising an error.

Domain: D5

Example: A long multi-turn agent session that fit on input starts a very long response, hits the token ceiling partway through, and the application receives a truncated answer instead of an exception.

## Managing Long Sessions

Q: Who is responsible for keeping a long-running session's context from exceeding the window, and how?

A: The application, by trimming or summarizing conversation history before each call — the context window does not manage this automatically.

Domain: D5

Example: A chat app that has run 200 turns starts summarizing the earliest 150 turns into a condensed note before each new API call, instead of resending the full raw history.

## Sampling Mechanics

Q: How does the model choose the next token during generation?

A: At each step it produces a probability distribution over possible next tokens and samples from that distribution, rather than always picking one fixed token.

Domain: D5

Example: Given the same prompt prefix, the model might sample "quickly" one run and "rapidly" the next, since both are plausible continuations under the distribution.

## Temperature's Effect

Q: How does temperature shape the token-sampling distribution?

A: Lower temperature concentrates probability on the most likely tokens, making output more repeatable; higher temperature spreads probability out, making output more varied.

Domain: D5

Example: A classification prompt run at temperature 0 tends to return the same label across repeated runs far more consistently than the same prompt run at temperature 1.

## Sampling Parameters Are Model-Dependent

Q: What happens if you set temperature, top_p, or top_k on the newest Claude models?

A: The newest models do not accept non-default sampling parameters — setting them returns a 400 error, and behavior on those models is steered through prompting instead.

Domain: D5

Example: A developer migrating an app from an older model to the newest generation removes a hardcoded `temperature=0.7` parameter after it starts returning 400 errors.

## Temperature 0 Is Not A Determinism Guarantee

Q: Does setting temperature to 0 guarantee identical outputs across calls?

A: No — temperature 0 makes outputs more repeatable but does not guarantee identical output across calls; confirm current parameter support in the API reference at build time.

Domain: D5

Example: A test suite that hardcodes an exact expected response string at temperature 0 still occasionally fails because output isn't perfectly deterministic.

## Non-Determinism Defined

Q: What is non-determinism, and what causes it?

A: Non-determinism is the property that identical inputs do not guarantee identical outputs; it is the direct consequence of sampling.

Domain: D5

Example: Running the exact same customer-support prompt twice can return two differently worded (but both correct) replies.

## Testing Non-Deterministic Output

Q: Why is asserting exact response text a poor test strategy for a Claude feature, and what should you assert instead?

A: Exact-text assertions are unreliable because the model can express the same correct answer many ways; instead assert on the property that must hold — a required field is present, a value is in range, or the structure parses — and use a model-graded eval when you need to judge meaning.

Domain: D4

Example: A test for an extraction feature checks that the returned JSON has a valid `email` field matching an email pattern, rather than checking for one exact JSON string.

## The Four Model Tiers

Q: What are the four tiers in the Claude model family, from most to least capable?

A: Fable (most capable, for the most demanding reasoning/coding/agentic work), Opus (demanding work above Sonnet's envelope), Sonnet (balanced default for most production workloads), Haiku (speed and cost efficiency within its capability envelope).

Domain: D5

Example: A team building a customer-facing chat feature defaults to Sonnet, reserves Fable for a complex agentic code-refactoring tool, and routes simple FAQ lookups to Haiku.

## Model Tier Selection Discipline

Q: What is the practical default process for choosing which model tier to run?

A: Start with Sonnet; move up a tier only when an eval shows the current tier missing your quality bar; move down to Haiku only when an eval shows the quality drop is acceptable for the task.

Domain: D5

Example: A team drops from Sonnet to Haiku for a bulk-classification job only after running an eval that confirms Haiku's accuracy on that specific task is still acceptable.

## Model Choice Vs. Reasoning Mode

Q: Why are model choice and reasoning mode considered separate, composable decisions?

A: Choosing which model runs is one decision; whether the model reasons before answering (adaptive thinking) is a separate decision made per call, so any supporting model can run with reasoning on or off independent of which tier it is.

Domain: D5

Example: A developer runs the same Sonnet model with reasoning off for quick classification calls and reasoning on with higher effort for a harder multi-step analysis call, without switching models.

## Adaptive Thinking And Effort

Q: How is reasoning depth tuned on current Claude models, and what happened to the old approach?

A: The model decides when and how much to think (adaptive thinking), and depth is tuned with an effort setting rather than a fixed token budget — the older `budget_tokens` control is deprecated and returns a 400 error on the newest model generations.

Domain: D5

Example: A developer upgrading an integration replaces a hardcoded `budget_tokens=4000` thinking parameter with an `effort` setting to avoid the 400 error on the newest models.

## Thinking Content Visibility

Q: Is thinking content shown in the response by default on the newest Claude models?

A: No — thinking content is omitted from responses by default; a developer must request summarized display to see it.

Domain: D5

Example: A debugging tool that expects to inspect the model's raw reasoning trace gets no thinking content back until the request explicitly asks for the summarized display.

## When Reasoning Earns Its Cost

Q: On what kind of tasks does enabling reasoning mode earn its cost, versus waste it?

A: Reasoning earns its cost on hard, multi-step problems, and is wasted on lookups and classification.

Domain: D5

Example: Enabling extended thinking for a multi-step financial reconciliation task is worthwhile; enabling it for a simple "is this email spam?" classification is wasted spend.

## Zero-Shot Prompting

Q: What is zero-shot prompting?

A: Giving the instruction with no worked examples — you describe the task and ask for the result directly.

Domain: D6

Example: "Summarize this email in two sentences" with no example summary attached is a zero-shot prompt.

## One-Shot And Multi-Shot Prompting

Q: What distinguishes one-shot from multi-shot (few-shot) prompting?

A: One-shot adds a single example of input paired with the desired output; multi-shot (also called few-shot) includes several such examples to more firmly pin down the output shape.

Domain: D6

Example: Providing three sample support tickets each paired with their correctly formatted triage labels before asking Claude to triage a new ticket is multi-shot prompting.

## Examples Are Not Training Data

Q: Are the examples used in one-shot/multi-shot prompting a form of training the model?

A: No — the examples are not training data; they sit in the prompt itself and show the model the exact shape of the answer wanted, which a description alone often fails to pin down.

Domain: D6

Example: Adding two example rows of a target CSV format inside the prompt does not permanently change the model's behavior on future, separate API calls.

## Shot-Prompting Cost/Quality Trade-Off

Q: What is the core trade-off in deciding how many examples to add to a prompt?

A: Each example costs tokens on every call and consumes context budget, so more examples trade quality (structure reliability) against cost; the discipline is to add the smallest amount of prompt that produces a reliable result.

Domain: D6

Example: A team drops from five examples to two after confirming via eval that two examples already produce reliably structured output, cutting token cost on every future call.

## When To Move Beyond Zero-Shot

Q: When should you move from zero-shot to one-shot or multi-shot prompting?

A: When the task output has a specific structure, casing, or edge case that a description alone keeps missing — often one or two correct examples fix the issue faster than adding another paragraph of instructions.

Domain: D6

Example: After several attempts to describe the exact date format needed fail, adding one example row with that exact date format fixes the output reliably.

## Prompting Mode Interacts With Model Choice

Q: How does model capability interact with the choice of zero-shot vs. multi-shot prompting?

A: A more capable model often succeeds zero-shot on a task where a smaller model needs a few examples to match the required structure, so adding examples can let a cheaper model do the job that would otherwise require a larger model.

Domain: D5

Example: Instead of upgrading from Haiku to Sonnet to fix a formatting problem, a developer first tries adding two examples to the Haiku prompt and finds that alone resolves it.

## REST API Fundamentals

Q: At its core, how is Claude reached over the network?

A: Over an HTTP REST API — code sends a request to an endpoint with an API key and a JSON body, and reads a JSON response back; this can be called directly with any HTTP client.

Domain: D2

Example: A developer without access to an official SDK writes a raw `curl` POST request with a JSON body to the Claude API endpoint and parses the JSON response manually.

## What The SDK Actually Provides

Q: What does the official Claude SDK add on top of the raw REST API?

A: A thin convenience layer over the same REST API that handles authentication, request construction, retries, and response parsing, so developers write less boilerplate — SDK and raw REST reach the identical API and model.

Domain: D2

Example: A Python developer uses the Anthropic SDK to avoid manually writing retry logic and JSON serialization that a raw REST integration would require by hand.

## Synchronous Requests

Q: When is a synchronous request pattern the right fit?

A: For short responses and backend jobs where no one is waiting — you send the request and wait for the complete response to come back in one piece before acting on it.

Domain: D2

Example: A nightly script that calls Claude once to generate a short summary report and writes it to a file uses a simple synchronous call.

## Streaming Responses

Q: When should you use streaming instead of a synchronous call, and what transport does it use?

A: When a response is long or a user is watching, so output appears immediately instead of after a blank-screen wait; Claude exposes streaming over the same HTTP connection using server-sent events (SSE), and the application reassembles the pieces into the final message.

Domain: D2

Example: A chat UI streams Claude's answer token-by-token to the screen as it's generated, rather than showing a blank screen until the full response arrives.

## Async/Await For Concurrency

Q: What problem do the async SDK patterns (AsyncAnthropic in Python, the Promise-based TypeScript client) solve?

A: They let an application make API calls without tying up the application thread while waiting, enabling concurrency — the request still returns in real time, but the app can do other work meanwhile.

Domain: D2

Example: A web server handling many simultaneous user requests uses `AsyncAnthropic` so one slow Claude call doesn't block it from serving other requests concurrently.

## TypeScript Has No Separate Async Client

Q: Does the TypeScript SDK have a separate async client class like Python's AsyncAnthropic?

A: No — the standard Anthropic TypeScript client is already Promise-based, so you `await` calls directly; there is no separate async client class needed.

Domain: D2

Example: A TypeScript developer porting Python code that uses `AsyncAnthropic` simply uses the standard client with `await` instead of looking for an equivalent async class.

## Message Batches API

Q: What is the Message Batches API for, and what's the trade-off?

A: A separate pattern for bulk offline workloads: submit a large set of requests in one call, receive an identifier, and poll for completion. Jobs can take up to 24 hours and run at a lower per-token cost, trading latency for cost savings.

Domain: D5

Example: A team runs an overnight evaluation job classifying 50,000 documents via the Batches API instead of a synchronous loop, accepting next-morning results for a lower total bill.

## Choosing Batch Vs. Async Vs. Streaming

Q: Given a workload where no user is waiting on individual results and cost matters more than turnaround time, which request pattern fits best, and why not the alternatives?

A: The Message Batches API fits: submit and poll, accepting latency for lower per-token cost. A synchronous loop would hit rate limits and tie up the application; streaming buys nothing because no user is watching results arrive incrementally.

Domain: D5

Example: A pipeline processing 50,000 documents overnight submits them as one batch rather than looping synchronous calls or streaming each response.

## Model Family And Path Structure

Q: What comes after Module 1 (MSO Foundations) in the Developer Foundations path?

A: Module 2 covers Production-Grade Prompting, Agents & Tool-use (prompting craft, extended thinking, tool schemas, streaming, context engineering, agent construction); later modules cover Claude Code/MCP/Integration (M3), Production Engineering/Evals/Security (M4), and Accelerators/IP Contribution (M5).

Domain: General

Example: A learner who just finished Module 1's context-window and sampling basics expects Module 2 to build directly on those concepts when introducing tool schemas and agent construction.
