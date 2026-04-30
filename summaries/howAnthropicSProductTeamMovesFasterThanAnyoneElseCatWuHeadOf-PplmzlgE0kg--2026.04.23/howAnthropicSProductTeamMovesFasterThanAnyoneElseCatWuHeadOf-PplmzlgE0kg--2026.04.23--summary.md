# How Anthropic's product team moves faster than anyone else | Cat Wu (Head of Product, Claude Code) — Summary

- **Channel:** Lenny's Podcast
- **Uploaded:** 2026-04-23
- **URL:** https://youtu.be/PplmzlgE0kg

## Summary

Cat Wu, head of product for Claude Code and Co-work at Anthropic, explains how the product organization compresses traditional six-month roadmaps into one-week (sometimes one-day) shipping cycles by deliberately stripping process, branding nearly every release as a research preview to lower commitment costs, and hiring engineers with strong product taste who can take an idea from Twitter feedback to launch with little PM involvement. She argues that role boundaries — engineer, PM, designer — are collapsing into a single low-ego, multi-hat profile where the durable skill is product taste: deciding what to build when code itself is cheap.

The conversation also covers the structural ingredients behind Anthropic's growth (a unifying mission that makes cross-org trade-offs easy, plus extreme focus), how Cat uses Co-work to generate a polished 20-page conference deck overnight by connecting Slack/Gmail/Drive/Calendar, why the "right amount of AGI-pilled" matters for products that must elicit maximum capability from today's model rather than tomorrow's, and concrete advice for thriving in this transition: automate the tedious 95% to 100% (anything less isn't really an automation), build apps you actually use daily, and resist the trap of over-customizing your setup instead of shipping.

## Key Takeaways

- The PM job is no longer aligning multi-quarter roadmaps; it is collapsing the time from idea to user, and shipping features as branded research previews to keep commitment low.
- Anthropic hires engineers with product taste so the most efficient features ship with no PM in the loop — taste, not role, is the rare skill.
- Mission and focus are the two ingredients Cat credits for Anthropic's growth: putting the org's goals above any individual product's KRs makes cross-functional trade-offs decisive instead of political.
- "Be the right amount of AGI-pilled" — building for the super-AGI model is easy; the hard, valuable work is eliciting maximum capability from the current model and patching its weaknesses.
- New models let you delete features, not just add them: crutches like the to-do list became unnecessary once Opus 4 naturally tracked subtasks. Re-read the system prompt with every model launch.
- Build products that don't quite work yet — code review only became reliable with Opus 4.5/4.6 — so the prototype is ready to swap in the next model and ship ahead of the field.
- A 95% automation isn't an automation. Pay the elbow-grease tax to push it to 100%, or don't ship it.
- Action-based products (Claude Code) feel categorically different from chat-based products (the 2024 generation); the aha moment comes the first time the agent does the thing instead of telling you how.

## Action Items

- [CAT WU — [00:06:54](https://youtu.be/PplmzlgE0kg?t=414)] Set clear goals: name your key user, the specific problem, and the concrete use case. LLM generality creates ambiguity; clarity rules out approaches.
- [CAT WU — [00:07:42](https://youtu.be/PplmzlgE0kg?t=462)] Ship features as research previews. Brand them clearly so users know they may not be supported forever — this lowers your team's commitment cost and gets things out in 1–2 weeks.
- [CAT WU — [00:08:17](https://youtu.be/PplmzlgE0kg?t=497)] Set up a tight PM-owned pipeline (e.g., evergreen launch room) so docs, PMM, and DevRel can turn around announcements the day after engineers are ready.
- [CAT WU — [00:36:08](https://youtu.be/PplmzlgE0kg?t=2168)] Connect Co-work to your communication tools and source-of-truth data (Slack, Gmail, Google Calendar, Google Drive) before doing anything else — output quality scales with context.
- [CAT WU — [00:53:32](https://youtu.be/PplmzlgE0kg?t=3212)] When the model does something unexpected, ask it to introspect on why. Use the answer to fix the harness, not just the output.
- [CAT WU — [00:55:03](https://youtu.be/PplmzlgE0kg?t=3303)] Build 10 great evals — not hundreds. They quantify what success looks like and surface what the team is missing.
- [CAT WU — [01:03:24](https://youtu.be/PplmzlgE0kg?t=3784)] Every time a new model lands, re-read the entire system prompt and delete reminders the model no longer needs.
- [CAT WU — [01:07:49](https://youtu.be/PplmzlgE0kg?t=4069)] Anytime you find yourself doing a manual task more than once, route it to Claude Code, Co-work, or another AI tool to automate.
- [CAT WU — [01:09:45](https://youtu.be/PplmzlgE0kg?t=4185)] Push automations to 100% reliability before relying on them. A 95% automation isn't an automation.
- [CAT WU — [01:12:08](https://youtu.be/PplmzlgE0kg?t=4328)] Build apps you actually use every day. One-shotted prototypes you never come back to don't teach you anything or give you leverage.
- [CAT WU — [01:13:10](https://youtu.be/PplmzlgE0kg?t=4370)] Resist the over-customization trap (skills, MCPs, workflow porn) when it's stealing time from the actual product or feature you set out to build. Simple setups work better.
- [CAT WU — [01:24:30](https://youtu.be/PplmzlgE0kg?t=5070)] Send Anthropic the edge cases and reproducible failures, not just the wins — that's the feedback the team can act on.

## Lists Mentioned

### Three things a PM should do to ship fast — CAT WU ([00:06:54](https://youtu.be/PplmzlgE0kg?t=414))

1. Set clear goals (key user, problem, use case) so the team can rule out wrong approaches.
2. Build a repeatable shipping process — e.g., almost everything ships as a research preview to lower commitment.
3. Build the cross-functional framework (when to pull in docs/PMM/DevRel and what they expect) so any engineer can ship without friction.

### How to build "the right amount of AGI-pilled" intuition — CAT WU ([00:53:32](https://youtu.be/PplmzlgE0kg?t=3212))

1. Spend a ton of time talking with and using the model; ask it to introspect on its own behavior when it does something unexpected.
2. Identify the ~5 trusted humans whose feedback on a model/harness combo is sharpest, and lean on them for fast vibe checks.
3. Build ~10 great evals to quantify the goal and what's missing.

### When to use which Anthropic surface — CAT WU ([00:32:44](https://youtu.be/PplmzlgE0kg?t=1964))

- **Claude Code (CLI):** one-off coding tasks; gets new features first; most powerful surface.
- **Claude Code on desktop:** front-end work with the live preview pane; a graphical entry point for non-terminal users; one-stop control plane for sessions across CLI, desktop, web, and mobile.
- **Web and mobile:** kicking off tasks on the go without your laptop.
- **Co-work:** anything where the output isn't code — slide decks, inbox/Slack zero, launch plans, customer briefs.

### Connect to Co-work first — CAT WU ([00:39:27](https://youtu.be/PplmzlgE0kg?t=2367))

- Slack
- Google Calendar
- Gmail
- Google Drive

### Anthropic's PM teams — CAT WU ([00:14:26](https://youtu.be/PplmzlgE0kg?t=866))

- Research PM team (Diane) — feedback to research, shepherds model launches.
- Claude Developer Platform team — APIs Claude Code is built on; managed agents.
- Claude Code team — Claude Code and Co-work core products.
- Enterprise team — cost controls, RBAC, security controls for adoption.
- Growth team — growth across the entire product suite, including the Claude API.

### Books Cat recommends most — CAT WU ([01:15:58](https://youtu.be/PplmzlgE0kg?t=4538))

1. *How Asia Works* — economic development and the policies behind long-lasting successful economies.
2. *The Technology Trap* — what the industrial and computer revolutions did to workers, and what history tells us about navigating this one.
3. *The Paper Menagerie* — short stories on coming of age, AI, and self-discovery (the fun pick).

## Salient Quotes

> "It is very hard to be the right amount of AGI-pilled. It's very easy to build the product for the super-AGI strong model. The hard thing is figuring out, for the current model, how do you elicit the maximum capability?"
> — CAT WU, [00:00:01](https://youtu.be/PplmzlgE0kg?t=1). The thesis statement of the episode — used twice, once in the cold open and again in full context.

> "As code becomes much cheaper to write, the thing that becomes more valuable is deciding what to write."
> — CAT WU, [00:18:16](https://youtu.be/PplmzlgE0kg?t=1096). The clearest one-line case for why product taste outlives any specific role.

> "If Claude Code failed but Anthropic succeeded, I would be extremely happy."
> — CAT WU, [00:31:42](https://youtu.be/PplmzlgE0kg?t=1906). Standalone insight on what "mission" actually buys you when teams have to make trade-offs.

> "If an automation doesn't work 100% of the time, it's not really an automation."
> — CAT WU, [01:09:45](https://youtu.be/PplmzlgE0kg?t=4185). Lenny reacted "I am super guilty of that. This is really good advice for me." — the rule that lands hardest in the conversation.

> "Jobs are fake. If you understand the constraints, you can figure out what you can do, and then just try to do it quickly, learn from the mistakes, and apologize or fix them if you did something wrong."
> — CAT WU, [01:19:38](https://youtu.be/PplmzlgE0kg?t=4778). Standalone insight — her unpacking of "just do things" as a working philosophy.

> "The 2024 generation of products were chat-based, and the Claude Code generation of products is action-based."
> — CAT WU, [01:14:58](https://youtu.be/PplmzlgE0kg?t=4478). Standalone insight framing the Karpathy "chatbot skeptics" divide that Lenny had just raised.

> "We try to face every challenge with a smile, because there's always so much going on… if you get too stressed about anything you'll burn out."
> — CAT WU, [00:22:39](https://youtu.be/PplmzlgE0kg?t=1359). Lenny reacted by comparing it to the Pirates of the Caribbean GIF of a man strolling calmly through a ship being demolished — "everyone I've met from Anthropic is just so chill."
