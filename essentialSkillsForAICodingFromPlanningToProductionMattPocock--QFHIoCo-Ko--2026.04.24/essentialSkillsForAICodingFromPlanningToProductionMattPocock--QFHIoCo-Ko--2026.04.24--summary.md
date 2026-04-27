# Essential Skills for AI Coding from Planning to Production — Matt Pocock (@mattpocockuk ) — Summary

- **Channel:** AI Engineer
- **Uploaded:** 2026-04-24
- **URL:** https://youtu.be/-QFHIoCo-Ko

## Summary

Matt Pocock's AI Engineer workshop argues that traditional software engineering fundamentals — the practices in books like *The Pragmatic Programmer*, *Refactoring*, *The Design of Design*, and *The Philosophy of Software Design* — work surprisingly well with AI agents and are essential to getting good output from them. He frames LLM coding around two hard constraints: a "smart zone" (~100k tokens) where the model performs well versus a "dumb zone" beyond it, and the fact that LLMs reset to a base state every session like the protagonist of *Memento*. From those constraints he derives a workflow that splits effort into a human-in-the-loop "day shift" (alignment, PRD, Kanban planning) and an AFK "night shift" (implementation by sandboxed agents), with QA and taste re-imposed by humans at the end.

Concretely, he demos a stack of skills built around this philosophy: a `grill-me` skill that interviews the user relentlessly to reach a shared "design concept" (he opposes the specs-to-code movement); a `write-a-PRD` skill that produces a destination document the user is not expected to re-read; a `prd-to-issues` skill that breaks work into vertical-slice "tracer bullet" issues that can be parallelized; a Ralph-loop AFK runner; a TDD red-green-refactor skill; and an `improve-codebase-architecture` skill aimed at converting shallow modules into deep ones for testability. He closes by introducing Sand Castle, his TypeScript library for orchestrating parallel sandboxed agents with separate planner, implementer, reviewer, and merger roles, and warns about "doc rot" from keeping old PRDs around in a repo.

## Key Takeaways

- LLMs operate well only in a "smart zone" of roughly 100k tokens — past that they make stupid decisions, regardless of advertised context windows. Bigger context mostly means more dumb zone, useful for retrieval but not coding.
- Prefer clearing context over compacting. Compaction creates a degraded "history" of the session; clearing returns the model to its strongest state.
- Specs-to-code is vibe coding by another name. The code is your battleground — keep it in mind throughout, never just edit specs and pray.
- Reach a *shared design concept* with the AI before generating any artifacts. A relentless grilling session is more valuable than a polished plan.
- Plan as a Kanban board of independently grabbable, vertical-slice ("tracer bullet") issues, not a numbered phase list — sequential plans can only be picked up by one agent.
- Human-in-the-loop tasks (alignment, taste, QA) cannot be Ralph-looped. Implementation can. Plan accordingly: day shift human, night shift AFK.
- Bad codebases make bad agents. The quality of your feedback loops is the ceiling on AI's output. Deep modules with simple interfaces beat shallow modules with sprawling internals.
- Code review by an AI must happen in a *fresh* context, otherwise the reviewer is dumber than the implementer.
- Push coding standards to your automated reviewer; let the implementer pull them via skills. Different tasks need different information shapes.
- Doc rot is real — old PRDs in a repo can mislead future agents. Closing/deleting them is often safer than keeping them around.

## Action Items

- [MATT POCOCK — [00:03:27](https://youtu.be/-QFHIoCo-Ko?t=207)] Size every AI coding task to fit in ~100k tokens (the smart zone); never let context drift past it.
- [MATT POCOCK — [00:09:55](https://youtu.be/-QFHIoCo-Ko?t=595)] Watch your token-usage status line every session so you know exactly how close you are to the dumb zone.
- [MATT POCOCK — [00:10:38](https://youtu.be/-QFHIoCo-Ko?t=638)] Default to *clearing* context rather than compacting between subtasks.
- [MATT POCOCK — [00:12:17](https://youtu.be/-QFHIoCo-Ko?t=737)] Start every meaningful piece of AI work by invoking a grill-me skill on the brief before generating any plan.
- [MATT POCOCK — [00:23:26](https://youtu.be/-QFHIoCo-Ko?t=1406)] Own your planning stack rather than leaning on a single framework — keep observability over the whole pipeline so you can fix it when it breaks.
- [MATT POCOCK — [00:35:15](https://youtu.be/-QFHIoCo-Ko?t=2115)] Don't read the PRD output of a write-a-PRD skill. If you've reached a shared design concept, you're only checking summarization quality.
- [MATT POCOCK — [00:42:27](https://youtu.be/-QFHIoCo-Ko?t=2507)] Break PRDs into vertical-slice ("tracer bullet") issues that touch every layer, not horizontal layer-by-layer phases.
- [MATT POCOCK — [00:55:57](https://youtu.be/-QFHIoCo-Ko?t=3357)] Run your AFK loop in human-in-the-loop mode (`once.sh`) repeatedly first, so you can tune the prompt before letting it run unattended in Docker.
- [MATT POCOCK — [01:06:08](https://youtu.be/-QFHIoCo-Ko?t=3968)] Always do automated code review in a fresh, cleared context — never let the implementer review its own work in the dumb zone.
- [MATT POCOCK — [01:06:41](https://youtu.be/-QFHIoCo-Ko?t=4001)] Use TDD red-green-refactor for AI implementations — write the failing test first to make it harder for the AI to cheat its tests.
- [MATT POCOCK — [01:13:39](https://youtu.be/-QFHIoCo-Ko?t=4419)] Manually QA the working feature yourself; this is where you re-impose taste so you don't end up with slop.
- [MATT POCOCK — [01:22:55](https://youtu.be/-QFHIoCo-Ko?t=4975)] If you take one thing away: run `improve-codebase-architecture` on your own repo and see what it finds.
- [MATT POCOCK — [01:24:08](https://youtu.be/-QFHIoCo-Ko?t=5048)] Don't keep finished PRDs in the repo as living docs — close or remove them to avoid doc rot misleading future agents.
- [MATT POCOCK — [01:29:38](https://youtu.be/-QFHIoCo-Ko?t=5338)] Push coding standards to your reviewer agent and let your implementer pull them via skills.
- [MATT POCOCK — [01:32:23](https://youtu.be/-QFHIoCo-Ko?t=5543)] Use a smarter model (e.g. Opus) for review and a cheaper one (e.g. Sonnet) for implementation.
- [MATT POCOCK — [01:35:30](https://youtu.be/-QFHIoCo-Ko?t=5730)] Buy and read pre-AI software engineering classics — the language they give you for software practice is gold for prompting AI.

## Lists Mentioned

### Stages every LLM session passes through — MATT POCOCK ([00:07:54](https://youtu.be/-QFHIoCo-Ko?t=474))

1. System prompt (always-in-context, keep tiny)
2. Exploration (agent reads the codebase)
3. Implementation
4. Testing / feedback loops

### Two types of tasks in the AI age — MATT POCOCK ([00:26:32](https://youtu.be/-QFHIoCo-Ko?t=1592))

- Human-in-the-loop tasks (alignment, planning, QA) — cannot be Ralph-looped
- AFK tasks (implementation) — can be delegated to looping agents

### Two essential documents per feature — MATT POCOCK ([00:29:13](https://youtu.be/-QFHIoCo-Ko?t=1753))

1. Destination document (PRD — what "done" looks like, including out-of-scope)
2. Journey document (Kanban board of independently grabbable issues)

### AFK Ralph-loop task priority order — MATT POCOCK ([00:57:10](https://youtu.be/-QFHIoCo-Ko?t=3430))

1. Critical bug fixes
2. Development infrastructure
3. Traceable-bullet (vertical-slice) issues
4. Polishing, quick wins, refactors

### Sand Castle agent roles — MATT POCOCK ([01:30:25](https://youtu.be/-QFHIoCo-Ko?t=5385))

1. Planner — picks parallelizable issues from the backlog
2. Implementer — runs in a sandboxed worktree per issue (Sonnet)
3. Reviewer — checks commits against pushed coding standards (Opus)
4. Merger — merges branches and resolves conflicts/type/test issues

### Books Matt recommends buying — MATT POCOCK ([01:35:30](https://youtu.be/-QFHIoCo-Ko?t=5730))

- *The Pragmatic Programmer* (origin of "tracer bullets" / vertical slices)
- *Refactoring* — Martin Fowler
- *The Design of Design* — Frederick P. Brooks (the "design concept" idea)
- *A Philosophy of Software Design* — John Ousterhout (deep vs shallow modules)

## Salient Quotes

> "Software engineering fundamentals — the stuff that's really crucial to working with humans — also works super well with AI."
> — MATT POCOCK, [00:00:50](https://youtu.be/-QFHIoCo-Ko?t=50). Standalone insight; the thesis of the entire talk.

> "I much prefer my AI to behave like the guy from Memento, because this state is always the same."
> — MATT POCOCK, [00:10:38](https://youtu.be/-QFHIoCo-Ko?t=638). Standalone insight; argues for clearing over compacting.

> "The code is your battleground."
> — MATT POCOCK, [00:13:39](https://youtu.be/-QFHIoCo-Ko?t=819). Standalone insight; rebuttal to the specs-to-code movement.

> "I needed to reach a shared understanding. I didn't need an asset, I didn't need a plan. I needed to be on the same wavelength as the AI, as my agent."
> — MATT POCOCK, [00:17:22](https://youtu.be/-QFHIoCo-Ko?t=1042). Standalone insight; the design-concept argument behind the grill-me skill.

> "Bad codebases make bad agents. If you have a garbage codebase you're going to get garbage out of the agent that's working in that codebase."
> — MATT POCOCK, [00:36:54](https://youtu.be/-QFHIoCo-Ko?t=2214). Standalone insight; one of his most-repeated principles.

> "You don't have the whole feedback loop."
> — AUDIENCE, [00:44:00](https://youtu.be/-QFHIoCo-Ko?t=2600). Matt reacted with "Exactly" — the audience nailed why horizontal slicing fails before he could spell it out.

> "AI loves to code horizontally."
> — MATT POCOCK, [00:43:33](https://youtu.be/-QFHIoCo-Ko?t=2573). Standalone insight; his core argument for forcing vertical slices in PRD-to-issues prompting.

> "If you're getting bad outputs from your AI, you often need to increase the quality of your feedback loops."
> — MATT POCOCK, [01:09:55](https://youtu.be/-QFHIoCo-Ko?t=4225). Standalone insight; framed as the ceiling on AI quality in any codebase.

> "You end up with apps that I feel just lack taste and are bad… without that you just end up with slop."
> — MATT POCOCK, [01:13:18](https://youtu.be/-QFHIoCo-Ko?t=4398). Standalone insight; argues that humans must remain in the QA loop.

> "We end up losing a sense of our codebase. And if we lose the sense of our codebase, we're not going to be able to improve it."
> — MATT POCOCK, [01:19:43](https://youtu.be/-QFHIoCo-Ko?t=4783). Standalone insight; motivation for designing module *interfaces* yourself even when delegating implementation.

> "If you take one thing away from today, just try running this skill on your repo and see what happens."
> — MATT POCOCK, [01:23:04](https://youtu.be/-QFHIoCo-Ko?t=4984). Standalone insight; his strongest concrete recommendation, referring to the improve-codebase-architecture skill.
