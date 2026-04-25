# The New Code — Sean Grove, OpenAI — Summary

- **Channel:** AI Engineer
- **Uploaded:** 2025-07-11
- **URL:** https://youtu.be/8rABwKRsec4

## Summary

Sean Grove, an alignment researcher at OpenAI, argues that the most valuable artifact a software engineer produces is not code but the specification behind it. Code is a lossy projection of intent — like a compiled binary that has lost its source — while a written specification captures the goals, values, and success criteria that let humans align with each other and align AI models with the team. He estimates that 80–90% of engineering work is already structured communication (gathering requirements, planning, sharing, testing against intent), and predicts that as models get more capable, whoever writes the clearest spec — engineer, PM, lawmaker, or marketer — is the programmer.

He grounds the argument in the OpenAI Model Spec, an open-sourced collection of markdown clauses (each with an ID and paired challenge prompts) that anyone at the company can contribute to. He uses the recent 4o sycophancy regression as a case study: because the spec already said "don't be sycophantic," the rollback was unambiguously a bug, not a debate. He then ties the same pattern to deliberative alignment (specs as training and eval material), to spec-as-code tooling (type checkers, linters, unit tests for prose), and finally to the US Constitution as a national-scale spec graded by judicial review, with precedents as its unit tests.

## Key Takeaways

- Code is only 10–20% of an engineer's value; the other 80–90% is structured communication — talking to users, distilling, planning, sharing, translating, testing, verifying intent.
- We treat prompts the wrong way around: we keep the generated code and discard the prompt, "shredding the source while version-controlling the binary."
- A sufficiently robust specification can be compiled into many artifacts — TypeScript, Rust, servers, clients, docs, tutorials, even podcasts — the way C source compiles to ARM64 or x86.
- The OpenAI Model Spec is just markdown, which makes it readable, versioned, change-logged, and contributable by non-engineers (legal, safety, policy, product).
- Deliberative alignment turns the spec into both training and eval material, pushing policy out of inference-time prompts and down into the model's weights.
- Specs deserve a code-like tool chain: type checkers for cross-team consistency, linters for ambiguous language, unit tests via challenge prompts.
- The US Constitution is a national model spec — written text, versioned amendments, judicial review as the grader, precedents as unit tests, enforcement as a training loop.
- Engineering has never been about code; it's "the precise exploration by humans of software solutions to human problems," and specs are how we move from disparate machine encodings to a unified human encoding.

## Action Items

- [SEAN GROVE — [19:54](https://youtu.be/8rABwKRsec4?t=1194)] Start your next AI feature by writing a specification first — define what you actually expect to happen and what success looks like.
- [SEAN GROVE — [19:54](https://youtu.be/8rABwKRsec4?t=1194)] Debate whether the spec is clearly written down and unambiguously communicated before writing code.
- [SEAN GROVE — [19:54](https://youtu.be/8rABwKRsec4?t=1194)] Make the spec executable: feed it to the model and test the model's output against the spec.
- [SEAN GROVE — [05:52](https://youtu.be/8rABwKRsec4?t=352)] Stop discarding prompts after vibe coding — treat the prompt/spec as the source-of-truth artifact, not the generated code.
- [SEAN GROVE — [20:55](https://youtu.be/8rABwKRsec4?t=1255)] Join OpenAI's new agent robustness team if you want to work on aligning agents at scale.

## Lists Mentioned

### The structured-communication process every engineer already runs — SEAN GROVE ([02:53](https://youtu.be/8rABwKRsec4?t=173))

1. Talk to users to understand their challenges.
2. Distill the stories.
3. Ideate about how to solve the problem.
4. Plan ways to achieve the goals.
5. Share the plans with colleagues.
6. Translate the plans into code.
7. Test and verify — not the code itself, but whether it achieved the goals in the world.

### What a sufficiently robust spec can compile to — SEAN GROVE ([08:11](https://youtu.be/8rABwKRsec4?t=491))

- Good TypeScript
- Good Rust
- Servers
- Clients
- Documentation
- Tutorials
- Blog posts
- Podcasts

### Specs viewed as code — the analogous tool chain — SEAN GROVE ([15:29](https://youtu.be/8rABwKRsec4?t=929))

- They compose
- They are executable
- They are testable
- They have interfaces with the real world
- They can be shipped as modules
- Type checker — for cross-spec consistency between teams
- Unit tests — challenge prompts attached to each clause
- Linters — for overly ambiguous language

### The US Constitution as a national model spec — SEAN GROVE ([16:42](https://youtu.be/8rABwKRsec4?t=1002))

- Written text — aspirationally clear, unambiguous policy
- Versioned amendments — a way to bump and publish updates
- Judicial review — a grader scoring real situations against the policy
- Precedent — input/output pairs that serve as unit tests
- Chain of command — embedded in the document
- Training loop — enforcement over time aligns the population

### Who writes specs (and is therefore "the programmer") — SEAN GROVE ([18:17](https://youtu.be/8rABwKRsec4?t=1097))

- Programmers align silicon via code specifications.
- Product managers align teams via product specifications.
- Lawmakers align humans via legal specifications.
- Prompt writers align AI models — every prompt is a proto-specification.

### Put this in action — SEAN GROVE ([19:54](https://youtu.be/8rABwKRsec4?t=1194))

1. Start with a specification.
2. Define what you expect to happen and what success criteria look like.
3. Debate whether it's clearly written and communicated.
4. Make the spec executable.
5. Feed the spec to the model.
6. Test against the model — or test against the spec.

## Salient Quotes

> "The person who communicates most effectively is the most valuable programmer. And literally, if you can communicate effectively, you can program."
> — SEAN GROVE, [04:24](https://youtu.be/8rABwKRsec4?t=264). Standalone insight — the thesis of the talk in two sentences.

> "We keep the generated code and we delete the prompt. And this feels a little bit like you shred the source and then you very carefully version control the binary."
> — SEAN GROVE, [05:55](https://youtu.be/8rABwKRsec4?t=355). Standalone insight — the central metaphor for why prompts deserve to be first-class artifacts.

> "If you don't have a specification, you just have a vague idea."
> — SEAN GROVE, [06:45](https://youtu.be/8rABwKRsec4?t=405). Standalone insight.

> "Specs actually give us a very similar tool chain, but it's targeted at intentions rather than syntax."
> — SEAN GROVE, [16:39](https://youtu.be/8rABwKRsec4?t=999). Standalone insight — the case for treating spec authoring as engineering.

> "Software engineering has never been about code."
> — SEAN GROVE, [19:19](https://youtu.be/8rABwKRsec4?t=1159). Standalone insight — delivered as a callback to the show-of-hands at the start.

> "Engineering is the precise exploration by humans of software solutions to human problems."
> — SEAN GROVE, [19:35](https://youtu.be/8rABwKRsec4?t=1175). Standalone insight — his working definition of the discipline.

> "You then realize that you never told it what you wanted, and maybe you never fully understood it anyway. This is a cry for specification."
> — SEAN GROVE, [21:11](https://youtu.be/8rABwKRsec4?t=1271). Standalone insight — closing framing for the agent-alignment problem.
