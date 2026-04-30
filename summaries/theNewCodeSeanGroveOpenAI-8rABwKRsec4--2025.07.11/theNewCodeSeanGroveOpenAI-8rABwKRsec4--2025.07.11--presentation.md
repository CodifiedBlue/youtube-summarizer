# The New Code — Presentation

Based on Sean Grove's talk at AI Engineer (2025-07-11). Target runtime: ~4–5 minutes.

---

--content--

# The New Code
### Specifications are the source.
### Code is the binary.

*Adapted from Sean Grove, OpenAI Alignment*

--speaker notes--

I want to share an idea from Sean Grove at OpenAI that has stuck with me: the most valuable thing a software engineer produces is not code — it's the specification behind it.

---

--content--

## A quick show of hands

Who here writes code?

Who feels their **most valuable artifact** is the code itself?

--speaker notes--

Sean opens his talk with a show of hands. Who writes code? Most people raise their hand. Then he asks — keep it up if you feel the most valuable thing you produce is the code. A lot of hands stay up. That answer feels natural. But it's wrong.

---

--content--

## Code is 10–20% of the job

The other **80–90%** is structured communication.

--speaker notes--

Code is only ten to twenty percent of the value an engineer brings. The other eighty to ninety percent is structured communication. That's a big claim — let me show you what he means.

---

--content--

## What engineers actually do

- Talk to users
- Distill challenges
- Ideate, plan, share
- Translate to code
- Test and verify **intent**

--speaker notes--

Look at the actual workflow. You talk to users. You distill their challenges. You ideate, you plan, you share those plans with colleagues. Then you translate to code — that's the part we usually focus on. And finally you test and verify. But you're not testing the code. You're testing whether it achieved the goal in the world. Almost every step of that is communication.

---

--content--

## The bottleneck

> "The person who communicates most effectively is the most valuable programmer."

If you can communicate clearly, you can program.

--speaker notes--

As models get more capable, that communication step is the bottleneck. Knowing what to build, why to build it, and whether you actually built the right thing — that's all communication. So the person who communicates most effectively becomes the most valuable programmer. If you can communicate clearly, you can program.

---

--content--

## The vibe coding paradox

We **prompt** the model.

We **keep the code**.

We **throw the prompt away**.

--speaker notes--

Now look at how we actually use LLMs. We write a prompt that describes our intent. The model gives us code. We carefully version-control the code — and we discard the prompt. Something is backwards here.

---

--content--

## Compare to a real compiler

Nobody version-controls the binary
and shreds the C source.

> "We shred the source and version-control the binary."

--speaker notes--

In a normal compiler workflow, nobody saves the binary and throws away the source. The source is what we care about — we regenerate the binary every build. Yet with LLMs we do the opposite. We shred the source — the prompt — and version-control the binary. The fix is to treat the spec, the intent, as the durable artifact.

---

--content--

## Code is a lossy projection

Decompile a C binary —
no comments, no variable names, no **why**.

Code never carries full intent.

--speaker notes--

There's a deeper reason specs matter. Code is a lossy projection of intent. If you decompile a C binary, you don't get back the comments, the variable names, the reasoning. The intent isn't in there. Even well-written code doesn't carry all the values and trade-offs the team made. You have to infer them.

---

--content--

## A robust spec compiles to many things

TypeScript · Rust
servers · clients
docs · tutorials · **podcasts**

--speaker notes--

A specification, on the other hand, contains enough information to compile in many directions. The same way C source compiles to ARM, x86, or WebAssembly — a robust spec can produce TypeScript, Rust, servers, clients, documentation, tutorials, even a podcast that explains your product to users. The spec is the source. Everything else is a target.

---

--content--

## The OpenAI Model Spec

A living document of intent and values.

**Open-sourced. Just markdown.**

--speaker notes--

OpenAI's Model Spec is the working example. It's a living document of the intentions and values they want their models to embody. And it's open source — you can find it on GitHub. It's just a folder of markdown files.

---

--content--

## Why markdown matters

- Human-readable
- Versioned
- Change-logged
- Anyone can contribute

Product · design · engineering · QA — not just one team.

--speaker notes--

Markdown is remarkable for this. It's human-readable, versioned, and change-logged. And because it's natural language, anyone on the team can contribute — product managers, designers, engineers, QA. It's the universal artifact that aligns everyone on what the system should and shouldn't do.

---

--content--

## Each clause is testable

Every clause has an **ID**.

Each ID has a paired file of **challenge prompts**.

The spec **encodes its own success criteria**.

--speaker notes--

But markdown alone isn't enough. Every clause in the Model Spec has an ID. And for each ID, there's a companion file with challenging prompts the model has to answer correctly. So the spec encodes its own success criteria. The document literally tests itself.

---

--content--

## Spec as training and eval material

Sample model → grader scores against spec → reinforce.

Policy moves **from the prompt into the weights**.

--speaker notes--

This is what enables deliberative alignment. You take the spec and a hard prompt, sample from the model, and a grader scores the response against the spec. That score reinforces the weights. Now the same document is both training material and eval material. The policy moves from inference-time prompts down into the model's weights.

---

--content--

## Case study: 4o sycophancy

A 4o update shipped extreme sycophancy.

The model praised users for **calling it sycophantic**.

--speaker notes--

Here's why this matters in practice. A recent 4o update shipped with extreme sycophancy. There were examples of users explicitly complaining about the model being sycophantic — and the model praising them for the insight. It hurts. It erodes trust.

---

--content--

## Bug, not debate

The spec already said:

> "Don't be sycophantic."

So the rollback was unambiguous.

--speaker notes--

The natural questions are: was it intended? Was it accidental? Why wasn't it caught? But here's the thing — the Model Spec already had a clause that said don't be sycophantic. It explained why short-term flattery hurts everyone long-term. So this wasn't a debate. The behavior didn't match the spec. That makes it a bug. Roll it back, fix it, ship.

---

--content--

## The spec as trust anchor

Aligns humans on what to expect.

Aligns models on what to produce.

--speaker notes--

In the meantime, the spec served as a trust anchor. It tells humans what to expect, and it tells the model what to produce. Even if the only thing a spec did was align humans, it would already be enormously valuable.

---

--content--

## Specs are code (for intent)

They **compose**, are **executable**,
**testable**, and **shippable as modules**.

--speaker notes--

So once you accept that specs are the real source, you start to notice they behave like code. They compose. They're executable. They're testable. They have interfaces with the real world. You can ship them as modules.

---

--content--

## The spec tool chain

| Code           | Spec                          |
|----------------|-------------------------------|
| Type checker   | Cross-team consistency        |
| Linter         | Ambiguity detector            |
| Unit tests     | Challenge prompts             |
| Compiler       | Model + alignment training    |

--speaker notes--

And the entire tool chain ports over. Type checkers become consistency checks between team specs. Linters flag overly ambiguous language. Unit tests are the challenge prompts attached to each clause. The compiler is the model itself, aligned through training. Same engineering discipline — but targeted at intent rather than syntax.

---

--content--

## Everyone on the team is a spec author

- **Engineers** → technical design docs
- **PMs** → product requirements
- **UX designers** → wireframes & flows
- **QA** → test plans & acceptance criteria
- **Prompters** → model prompts

--speaker notes--

That means everyone on a software team is already a spec author. Engineers align silicon through technical design docs. PMs align teams through product requirements. UX designers align users through wireframes and flow specs. QA aligns the release through test plans and acceptance criteria. And anyone writing a prompt is aligning a model. Every one of these artifacts is a specification.

---

--content--

## Software engineering was never about code

> "Engineering is the precise exploration by humans of software solutions to human problems."

--speaker notes--

So coming back to the show of hands at the start — software engineering has never been about code. Coding is a wonderful skill. But it's not the end goal. Engineering is the precise exploration by humans of software solutions to human problems. We're just moving from disparate machine encodings to a unified human encoding.

---

--content--

## For your next AI feature

1. Write the **spec first**
2. Define **success criteria**
3. Make it **executable**

--speaker notes--

So here's the call to action. For your next AI feature, start with a specification. Define what you actually expect to happen and what success looks like. Then make it executable — feed it to the model, test the model against it.

---

--content--

## You don't have to do this alone

A whole ecosystem of tools now exists
to help you write better specs.

--speaker notes--

The good news is, you don't have to invent the workflow yourself. Over the past year, a whole ecosystem has popped up around spec-driven development. These are tools that plug into your coding agent and walk you through writing specs, breaking them into plans, and executing them safely.

---

--content--

## The spec-driven tooling landscape

| Tool          | Author              | GitHub Stars |
|---------------|---------------------|--------------|
| superpowers   | obra (Jesse Vincent)| ~167,700     |
| spec-kit      | GitHub, Inc.        | ~90,900      |
| BMAD-METHOD   | bmad-code-org       | ~45,700      |
| OpenSpec      | Fission-AI          | ~42,900      |
| agent-skills  | Addy Osmani         | ~23,000      |
| maister       | SkillPanel          | ~120         |

--speaker notes--

Here are the main players. GitHub itself shipped spec-kit. BMAD-METHOD comes from the bmad-code organization. Fission-AI maintains OpenSpec. Addy Osmani publishes agent-skills. SkillPanel has maister. And at the top, with over 167 thousand stars, is Superpowers from Jesse Vincent — that's the one I want to walk through, because it best illustrates what spec-first development with an agent actually feels like.

---

--content--

## What is Superpowers?

> "An agentic skills framework
> & software development methodology that works."
>
> — Jesse Vincent (obra)

A plugin that gives your coding agent
a **methodology**, not just tools.

--speaker notes--

Superpowers describes itself as an agentic skills framework and software development methodology. It's a plugin for coding agents like Claude Code, Codex, Cursor, OpenCode, Copilot CLI, and Gemini. The key word is methodology — it doesn't just add tools, it teaches the agent a workflow that always starts with a spec.

---

--content--

## Install in one command

```
/plugin install superpowers@claude-plugins-official
```

Also available for Codex, Cursor, OpenCode,
Copilot CLI, and Gemini.

--speaker notes--

Installation is one command. In Claude Code it's a single plugin install. There are equivalents for Codex, Cursor, OpenCode, Copilot, and Gemini. Once installed, the skills trigger automatically — you don't need to remember to invoke them.

---

--content--

## Step 1 — Brainstorm

Agent **doesn't jump into code**.

It asks what you're really trying to do,
explores alternatives,
and produces a **design document**.

--speaker notes--

Here's what the workflow feels like. Step one — you describe what you want, and instead of writing code, the agent activates the brainstorming skill. It asks Socratic questions, surfaces hidden assumptions, explores alternatives, and produces a design document. This is the spec coming out of the conversation, in chunks short enough to actually read.

---

--content--

## Step 2 — Write the plan

The design becomes a plan
of **2–5 minute tasks**.

Each task has:
exact file paths · complete code · verification steps.

--speaker notes--

Once you sign off on the design, the writing-plans skill turns it into an implementation plan. The plan is broken into tasks small enough to take 2 to 5 minutes each. Every task has exact file paths, the code to write, and verification steps. The bar is: clear enough for an enthusiastic junior engineer with no context to follow.

---

--content--

## Step 3 — Subagent-driven execution

A **fresh subagent per task**.

Two-stage review:
**spec compliance** → **code quality**.

--speaker notes--

When you say go, Superpowers dispatches a fresh subagent for each task in the plan. Each task gets a two-stage review — first against the spec, then for code quality. Because each subagent starts clean, it can't drift from the plan. Jesse reports agents working autonomously for a couple of hours without deviating.

---

--content--

## Step 4 — TDD enforced

**RED → GREEN → REFACTOR.**

Write failing test → watch it fail
→ minimal code → watch it pass.

Code written before tests is **deleted**.

--speaker notes--

Throughout execution, the test-driven-development skill enforces a strict red-green-refactor cycle. Write the failing test first, watch it fail, write the minimal code, watch it pass, commit. If code shows up before its test, it gets deleted. The spec, plan, and tests form the alignment layer.

---

--content--

## Step 5 — Review and finish

- **requesting-code-review** between tasks
- **systematic-debugging** for failures
- **finishing-a-development-branch** to merge

Worktrees keep it all isolated.

--speaker notes--

Between tasks the agent requests its own code review and reports issues by severity — critical issues block progress. If something breaks, systematic-debugging runs a 4-phase root-cause process. When everything's done, finishing-a-development-branch verifies the tests, offers merge or PR options, and cleans up the worktree it was working in.

---

--content--

## Why this works

The methodology **enforces spec-first**.

Skills trigger **automatically** — no discipline required.

The spec stays the **source of truth** end to end.

--speaker notes--

The reason this works is that the methodology enforces spec-first. The skills trigger automatically based on what you're doing — you don't have to remember to invoke them. The spec stays the source of truth from brainstorming through merge. It's exactly Sean's argument made operational.

---

--content--

## Why we should write specs

- Code is **lossy**. Specs carry **intent**.
- Specs **align humans** before they align machines.
- Specs are **executable** — training, eval, audit.
- Specs make AI agents **trustworthy at scale**.
- Whoever writes the spec is **the engineer**.

--speaker notes--

So to bring it all the way back. Why should we, as engineers, write specs? Because code is a lossy projection of what we actually meant. Because specs align humans on intent before any machine gets involved. Because specs are executable — they're training material, eval material, and an audit trail all at once. Because the only way to scale trust in AI agents is to give them an explicit, testable target. And because the discipline of writing the spec is the engineering — whoever writes it is the engineer.

---

--content--

## Stop shredding your prompts.

### The spec is the source.

*Thank you.*

--speaker notes--

Stop shredding your prompts. The spec is the source. Thank you.
