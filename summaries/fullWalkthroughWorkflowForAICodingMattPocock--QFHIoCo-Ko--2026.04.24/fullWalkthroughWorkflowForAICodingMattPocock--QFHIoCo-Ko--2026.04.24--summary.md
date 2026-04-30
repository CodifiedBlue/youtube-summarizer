# Full Walkthrough: Workflow for AI Coding — Matt Pocock — Summary

- **Channel:** AI Engineer
- **Uploaded:** 2026-04-24
- **URL:** https://youtu.be/-QFHIoCo-Ko

## Summary

Matt Pocock walks through his end-to-end workflow for building a feature with AI coding agents, anchored on a single thesis: classical software-engineering fundamentals — taste, alignment, modular design, feedback loops, vertical slices — matter *more*, not less, in the AI age. He frames LLMs around two operational constraints: a "smart zone" that ends around ~100k tokens, and Memento-like amnesia between sessions. Around those constraints he builds a pipeline of human-in-the-loop planning (a "grill-me" skill, then a PRD, then a kanban of vertical-slice issues) followed by AFK implementation (Ralph-style loops, sandboxed Docker work-trees, parallelized via his Sand Castle TypeScript library), with TDD and human QA imposing taste at the end.

The deeper argument is that *bad codebases produce bad agents*. Shallow modules and weak feedback loops cap how good AI output can ever be, while deep modules with clean interfaces and strong test boundaries unlock both parallelization and reviewability. He warns against the "specs-to-code" temptation of ignoring the code itself, against documentation rot from keeping old PRDs in the repo, and against automating away the human touch that produces non-slop work — while accepting that the cost of all this is more code review than developers used to do.

## Key Takeaways

- LLMs have a smart zone (~100k tokens) and a dumb zone — once context grows past that, attention scales quadratically and quality collapses regardless of the advertised window.
- Reach a *shared design concept* with the AI before generating any plan — alignment beats artifacts.
- "Specs-to-code" is vibe coding by another name; the code is your battleground, not the spec.
- Plan as a kanban of vertical slices (tracer bullets), not horizontal layered phases — the AI will default to horizontal, which delays feedback until phase three.
- Bad codebases (shallow modules, weak tests) cap AI output quality; deep modules with clear interfaces are the single biggest lever for better agent performance.
- Design the interface, delegate the implementation — treat your own modules as gray boxes to retain a sense of the codebase while moving fast.
- Push coding standards to the *reviewer*; let the *implementer* pull them via skills. Use a fresh context for review so it lands in the smart zone, not the dumb zone.
- More AI coding means more code review — there's no clean way around it yet.

## Action Items

- [MATT POCOCK — [00:08:51](https://youtu.be/-QFHIoCo-Ko?t=531)] Watch your token count every session via a status line so you know how close you are to the dumb zone.
- [MATT POCOCK — [00:10:38](https://youtu.be/-QFHIoCo-Ko?t=638)] Prefer clearing context (Memento-style) over compacting — compacted state is sediment that drags quality down.
- [MATT POCOCK — [00:12:17](https://youtu.be/-QFHIoCo-Ko?t=737)] Start every piece of work with a "grill-me" skill that interrogates you until you and the AI share a design concept.
- [MATT POCOCK — [00:23:24](https://youtu.be/-QFHIoCo-Ko?t=1404)] Own your planning stack — don't lock yourself into a single framework you can't observe or fix.
- [MATT POCOCK — [00:34:42](https://youtu.be/-QFHIoCo-Ko?t=2082)] Don't bother reading the PRD the AI produces — if you reached alignment in the grilling session, you're only checking a summarization.
- [MATT POCOCK — [00:39:49](https://youtu.be/-QFHIoCo-Ko?t=2389)] Break the PRD into a kanban of independently grabbable issues with explicit blocking relationships, not a sequential multi-phase plan.
- [MATT POCOCK — [00:44:07](https://youtu.be/-QFHIoCo-Ko?t=2647)] Insist on vertical slices: schema + service + minimal UI in the first issue, so feedback arrives early.
- [MATT POCOCK — [01:06:28](https://youtu.be/-QFHIoCo-Ko?t=3988)] Use TDD with red-green-refactor — it's much harder for AI to cheat on tests written before the implementation.
- [MATT POCOCK — [01:12:28](https://youtu.be/-QFHIoCo-Ko?t=4348)] Always QA the result manually — that's where you impose taste and avoid producing slop.
- [MATT POCOCK — [01:17:34](https://youtu.be/-QFHIoCo-Ko?t=4614)] Build deep modules with small interfaces, then test at the module boundary — feedback-loop quality is the ceiling on AI quality.
- [MATT POCOCK — [01:21:14](https://youtu.be/-QFHIoCo-Ko?t=4874)] Run the "improve codebase architecture" skill on your repo to surface module-deepening candidates.
- [MATT POCOCK — [01:24:08](https://youtu.be/-QFHIoCo-Ko?t=5048)] Don't keep PRDs in the repo after implementation — close them as issues to avoid doc rot misleading future agents.
- [MATT POCOCK — [01:28:53](https://youtu.be/-QFHIoCo-Ko?t=5333)] Push coding standards to the automated reviewer; let the implementer pull skills as needed.
- [MATT POCOCK — [01:35:30](https://youtu.be/-QFHIoCo-Ko?t=5730)] Buy old software-engineering books (Pragmatic Programmer, A Philosophy of Software Design, The Design of Design) — they verbalize best practice in English that drops cleanly into prompts.

## Lists Mentioned

### LLM session stages — MATT POCOCK ([00:07:25](https://youtu.be/-QFHIoCo-Ko?t=445))

1. System prompt (always-on context — keep tiny).
2. Exploration (agent reading the codebase).
3. Implementation.
4. Testing / feedback loops.

### Two task types in the AI age — MATT POCOCK ([00:26:32](https://youtu.be/-QFHIoCo-Ko?t=1592))

1. Human-in-the-loop tasks (alignment, planning) — cannot be looped over.
2. AFK tasks (implementation) — can be delegated to a looped agent.

### End-to-end workflow — MATT POCOCK ([00:52:31](https://youtu.be/-QFHIoCo-Ko?t=3151))

1. Idea.
2. Grilling session (grill-me skill) — reach shared understanding.
3. (Optional) Research / prototype.
4. PRD (destination document).
5. Kanban board of vertical-slice issues (journey).
6. AFK implementation by agent(s).
7. Manual QA + code review (loops back into more kanban issues).
8. Team review and merge.

### Ralph-loop AFK prompt priorities — MATT POCOCK ([00:56:06](https://youtu.be/-QFHIoCo-Ko?t=3366))

1. Critical bug fixes.
2. Development infrastructure.
3. Tracer-bullet (vertical-slice) issues.
4. Polishing, quick wins, refactors.

### Sand Castle pipeline stages — MATT POCOCK ([01:30:46](https://youtu.be/-QFHIoCo-Ko?t=5446))

1. Planner — picks parallelizable issues from the backlog.
2. Sandbox + implement (worktree per issue).
3. Reviewer — reviews commits.
4. Merger — merges branches and resolves type/test conflicts.

### Push vs pull for coding standards — MATT POCOCK ([01:28:53](https://youtu.be/-QFHIoCo-Ko?t=5333))

- Implementer → **pull** (skills available on demand).
- Automated reviewer → **push** (standards always in context).

## Salient Quotes

> "AI is obviously changing a lot of things... when we talk about AI being a new paradigm, we forget that actually software engineering fundamentals, the stuff that's really crucial to working with humans, also works super well with AI."
> — MATT POCOCK, [00:00:50](https://youtu.be/-QFHIoCo-Ko?t=50). The thesis statement of the entire talk.

> "It's like you're adding a team to a football league. The number of matches that get added... just scales quadratically."
> — MATT POCOCK, [00:03:00](https://youtu.be/-QFHIoCo-Ko?t=180). Standalone insight — vivid analogy for why context windows degrade with length.

> "I needed to reach a shared understanding. I didn't need an asset. I didn't need a plan. I needed to be on the same wavelength as the AI, as my agent."
> — MATT POCOCK, [00:16:09](https://youtu.be/-QFHIoCo-Ko?t=969). Standalone insight — the central reframing behind the grill-me skill.

> "Bad codebases make bad agents. If you have a garbage codebase, you're going to get garbage out of the agent that's working in that codebase."
> — MATT POCOCK, [00:36:02](https://youtu.be/-QFHIoCo-Ko?t=2162). Standalone insight — distilled answer to "how deep does TypeScript knowledge still matter".

> "AI loves to code horizontally."
> — MATT POCOCK, [00:42:17](https://youtu.be/-QFHIoCo-Ko?t=2537). Standalone insight — the failure mode that vertical slicing is meant to counter.

> "You don't have the whole feedback loop."
> — AUDIENCE, [00:43:21](https://youtu.be/-QFHIoCo-Ko?t=2601). Matt reacted with "Exactly," validating that horizontal layering kills feedback until phase three.

> "If you try to automate the creation of the idea, automate the QA, automate the research, automate the prototype, you end up with apps that I feel just lack taste and are bad... you just end up with slop."
> — MATT POCOCK, [01:12:28](https://youtu.be/-QFHIoCo-Ko?t=4348). Standalone insight — the case for keeping a human in QA.

> "We're essentially delegating the shape of [the codebase] to AI. I don't think that's good."
> — MATT POCOCK, [01:19:04](https://youtu.be/-QFHIoCo-Ko?t=4744). Standalone insight — frames the "design the interface, delegate the implementation" rule.

> "Design the interface for these modules, but then delegate the implementation."
> — MATT POCOCK, [01:20:09](https://youtu.be/-QFHIoCo-Ko?t=4809). Standalone insight — the one-line rule for retaining codebase comprehension under AI velocity.

> "The quality of your feedback loops influences how good your AI can code. Essentially, that is the ceiling."
> — MATT POCOCK, [01:09:24](https://youtu.be/-QFHIoCo-Ko?t=4164). Standalone insight — the upper bound on AI coding quality.
