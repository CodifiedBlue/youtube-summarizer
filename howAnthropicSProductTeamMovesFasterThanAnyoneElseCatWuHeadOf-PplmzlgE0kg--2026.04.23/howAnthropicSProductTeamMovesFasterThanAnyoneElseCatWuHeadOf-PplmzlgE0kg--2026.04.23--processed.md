# How Anthropic's product team moves faster than anyone else | Cat Wu (Head of Product, Claude Code)

- **Channel:** Lenny's Podcast
- **Uploaded:** 2026-04-23
- **URL:** https://youtu.be/PplmzlgE0kg

---

[00:00:01](https://youtu.be/PplmzlgE0kg?t=1) **CAT WU**

I think it is very hard to be the right amount of AGI pilled. It's very easy to build the product for the super-AGI strong model. The hard thing is figuring out, for the current model, how do you elicit the maximum capability?

[00:00:13](https://youtu.be/PplmzlgE0kg?t=13) **LENNY**

I've never seen anything like the pace you folks at Anthropic are shipping at.

[00:00:17](https://youtu.be/PplmzlgE0kg?t=17) **CAT WU**

We want to remove every single barrier to shipping things. The timelines for a lot of our product features have gone down from six months to one month, and sometimes to even one day.

[00:00:27](https://youtu.be/PplmzlgE0kg?t=27) **LENNY**

You're interviewing hundreds of PMs and you just keep feeling like they're approaching it very incorrectly.

[00:00:32](https://youtu.be/PplmzlgE0kg?t=32) **CAT WU**

The PM role is changing a lot. It's changing really quickly. The thing that is extremely important for building AI-native products is iterating so quickly, figuring out a way for you to actually launch features every single week.

[00:00:44](https://youtu.be/PplmzlgE0kg?t=44) **LENNY**

What do you think are the emerging skills PMs need to develop?

[00:00:48](https://youtu.be/PplmzlgE0kg?t=48) **CAT WU**

It comes back to product taste. As code becomes much cheaper to write, the thing that becomes more valuable is deciding what to write.

[00:00:56](https://youtu.be/PplmzlgE0kg?t=56) **LENNY**

Today my guest is Cat Wu, head of product for Claude Code and Co-work at Anthropic. Cat is at the center of everything that is changing in AI and product and building. And she and her team are building the product that is most changing the way that we all build our products. She is so full of insights and wisdom and lessons. This is an episode you cannot miss. Before we get into it, don't forget to check out lennysprobass.com for an insane set of deals available exclusively to Lenny's newsletter subscribers. With that, I bring you Cat Wu.

[00:01:35](https://youtu.be/PplmzlgE0kg?t=95) **LENNY**

Cat, welcome to the podcast.

[00:01:35](https://youtu.be/PplmzlgE0kg?t=95) **CAT WU**

Thanks for having me.

[00:01:37](https://youtu.be/PplmzlgE0kg?t=97) **LENNY**

I have so many questions. I'm so excited to have you on this podcast. I want to start with giving people an understanding of your role alongside Boris. Everybody knows Boris. His episode is the number one most popular episode on this podcast — no pressure. He created Claude Code, he leads the team, ships a bazillion PRs a day from his phone — I don't even know what the number is anymore. I think people don't give you enough credit for the success that Claude Code has had, and Co-work, and all the things you all are building. Help us understand your role on the team, how you work with Boris, how you split responsibilities — just like, what does the PM role look like on the Claude Code team?

[00:02:16](https://youtu.be/PplmzlgE0kg?t=136) **CAT WU**

I feel very lucky to work with Boris. He's been an amazing thought partner. He's our tech lead, he's very much the product visionary, and he is great at setting like, this is what the product needs to be in three months, six months from now — this is the AGI-pilled version of the product. And a lot of my role is figuring out, okay, what is the path from where we are today to that vision three to six months from now. I spend more of my time on the cross-functional, so making sure that our marketing team, sales team, finance, capacity, etc. are all bought in on the plan, that we're all rowing the same direction, and that once the feature is ready there aren't any blockers to shipping it. I think in many ways it works well because we kind of mind-meld, but it is actually a remarkably blurry line. I think we're like 80% mind-meld, and then there's like this 20% of things that maybe I care a lot more about — so I'll drive those — and then like 20% where he cares a lot more than me and he just drives those.

[00:03:20](https://youtu.be/PplmzlgE0kg?t=200) **LENNY**

This episode is brought to you by our season's presenting sponsor, WorkOS. What do OpenAI, Anthropic, Cursor, Vercel, Replit, Sierra, Clay, and hundreds of other winning companies all have in common? They are all powered by WorkOS. If you're building a product for the enterprise, you've felt the pain of integrating single sign-on, SCIM, RBAC, audit logs, and other features required by large companies. WorkOS turns those deal blockers into drop-in APIs with a modern developer platform built specifically for B2B SaaS. Literally every startup that I'm an investor in that starts to expand upmarket ends up working with WorkOS, and that's because they are the best. Whether you are a seed-stage startup trying to land your first enterprise customer or a unicorn expanding globally, WorkOS is the fastest path to becoming enterprise-ready and unblocking growth. It's essentially Stripe for enterprise features. Visit workos.com to get started, or just hit up their Slack where they have actual engineers waiting to answer your questions. WorkOS allows you to build faster with delightful APIs, comprehensive docs, and a smooth developer experience. Go to workos.com to make your app enterprise-ready today.

[00:04:30](https://youtu.be/PplmzlgE0kg?t=270) **LENNY**

Something that you shared actually before we started recording is the fact that you're interviewing hundreds of PMs all the time. If I had a nickel for every time someone asked me for an intro to someone at Anthropic to go work at Anthropic as a PM, I'd have $30 billion in ARR. It's just like the number one place people want to go work. So I can only imagine how many PMs you're interviewing. You told me that you're just seeing people doing it wrong, the way they're approaching what they think it takes to be a successful AI PM. Talk about what you're seeing and what people need to understand about what it takes to be successful these days.

[00:05:03](https://youtu.be/PplmzlgE0kg?t=303) **CAT WU**

I think before AI, technology shifts were a lot slower. So you could plan on the 6-to-12-month time horizons. And because you were shipping features at a bit of a slower rate, there was a lot more emphasis on coordinating with all the other partner teams to make sure that they're shipping features that unblock your features, because code at that time was very expensive to make. Now, with AI and with how much that has accelerated engineering, and with how quickly the model capabilities are improving, the timelines for a lot of our product features have gone down from six months to one month and sometimes to one week or even one day. And with that, we actually need to make sure that products ship quite quickly. What that means is, as a PM, there should be less emphasis on making sure that you're aligning your multi-quarter roadmaps with your partner teams, and more emphasis on, okay, how can we figure out the fastest way to get something out the door? How can we figure out how to make a concept corner of our product suite where an engineer has an idea or a PM has an idea, and by the end of the week we are able to get it into our users' hands. The PMs who do the best on AI-native products are the ones who can figure out how to shorten the time from having an idea to actually getting the product in the hands of users, and help define what are the most important tasks that need to work out of the box for my product.

[00:06:38](https://youtu.be/PplmzlgE0kg?t=398) **LENNY**

What I love about this is what you're saying is people haven't grasped how fast they need to move, and how much of the job now is just helping the team move fast. What helps do that? What does your PM team do to help them move this fast, other than have access to the most advanced models?

[00:06:54](https://youtu.be/PplmzlgE0kg?t=414) **CAT WU**

The first thing is to set clear goals, because LLMs are so general that it actually creates a lot of ambiguity in who we're building for, what problems we're trying to solve, what the top use cases are. A great PM is able to say, okay, our key user is professional developers. The main problem we want to solve for this feature is maybe there are too many permission prompts and people are feeling fatigue. The use case is, we want professional developers at enterprises to safely get to zero permission prompts. That actually sets a pretty clear goal because it rules out a lot of potential approaches for reducing permission prompts so that people can get a lot more done with one prompt.

[00:07:42](https://youtu.be/PplmzlgE0kg?t=462) **CAT WU**

The second thing that's very important is figuring out some repeatable process for getting these features shipped. So for Claude Code, what we do is we actually ship almost all of our features in research preview. We clearly brand this when we ship something so that users know that this is an early product, this is just an idea, this is just something that we're trying to get feedback on and iterating on, and that this might not be supported forever. What this does is it reduces our commitment for shipping something. We can just get something out in a week or two.

[00:08:17](https://youtu.be/PplmzlgE0kg?t=497) **CAT WU**

And then the third thing that a PM should do is help create the framework for the team so that they know when to pull in cross-functional partners and what those cross-functional partners' expectations are. For example, we have a really tight process between engineering, marketing, and docs. So when engineers have a feature that they feel is ready and that we've dogfooded internally, they post it in our evergreen launch room. And then Sarah, who leads our docs, and Alex, who leads PMM, and Tar and Lydia on DevRel just jump in and can turn around the marketing announcement for it the very next day. Because we have this really tight process, it lowers the friction for any engineer to ship something, and PM is the role that should be setting this up.

[00:08:59](https://youtu.be/PplmzlgE0kg?t=539) **LENNY**

How do PRDs fit into this? You said goals are a really important part — being aligned on what does success look like, who is this for, who's this not for. Are you writing PRDs? Is it just a couple bullet points? How's that evolved in the world of a PM?

[00:09:12](https://youtu.be/PplmzlgE0kg?t=552) **CAT WU**

So there's two things that we do. One is we have very rigorous metrics, and we do metrics readouts with the entire team every week. The goal of this is to make sure that everyone deeply understands all the facets of our business — what our key goals are, how they're trending, and what drives them. The second thing that we do is we have this list of team principles. This includes who our key users are, why those are our key users. The reason that we articulate all of this is so that everybody on the team feels like they understand how our business works, they understand what's important to us and what we're willing to trade off. And it lets people make decisions by themselves without feeling like they're blocked on PM or any other stakeholder.

[00:09:55](https://youtu.be/PplmzlgE0kg?t=595) **LENNY**

I love how so much of this is like, okay, we still need PMs in the future. There's so much talk of, why do we need PMs? We're just going to ship and build, we need engineers.

[00:10:03](https://youtu.be/PplmzlgE0kg?t=603) **CAT WU**

Oh, we actually do PRDs sometimes. For features that are particularly ambiguous, it does help to write out just a one-pager on what the goals are, what the delightful use cases are, what the failure modes currently are that we need to fix. And there are occasionally some projects, especially things that require heavy infrastructure, that do take many months. For those situations, we do write PRDs still.

[00:10:29](https://youtu.be/PplmzlgE0kg?t=629) **LENNY**

I want to drill a little bit further into just how you're able to move so fast. I've never seen anything like the pace folks at Anthropic are shipping at. Someone made this calendar of launches across Anthropic and it was literally every day there was a major feature or product. So one question people had online is — you guys just launched this incredible model, Mythos, that is still in preview because it's so powerful people are a little afraid of what it can do. Have you guys been using this? Is this part of the reason you've been able to move so fast?

[00:11:03](https://youtu.be/PplmzlgE0kg?t=663) **CAT WU**

We've been moving pretty fast for several quarters now. So I think it's not fully Mythos. Mythos is an incredibly powerful model, but we do use the models internally and I think this has increased our rate of shipping a little bit, but I don't think it explains the bulk of the increase. I think a lot of it is the process and the expectation on the team. We're very low on process. We want to remove every single barrier to shipping things. We want to make sure every single person on the team feels empowered to take their idea from just an idea to out in the world in less than a week, sometimes even in a day.

[00:11:43](https://youtu.be/PplmzlgE0kg?t=703) **LENNY**

Cool. Oh man, what an advantage to have the best model and also be building product. That's so cool.

[00:11:46](https://youtu.be/PplmzlgE0kg?t=706) **CAT WU**

We are very lucky to be able to work with the frontier models.

[00:11:49](https://youtu.be/PplmzlgE0kg?t=709) **LENNY**

Oh my god, what an awesome advantage. Just build a thing, then use it, and then accelerate faster. There's a couple of these other side things I want to go on these side quests on this conversation. There's so much happening with Anthropic and I'm so curious to get your insight. One is — a week ago or so the whole source code of Claude Code leaked. Somebody got it out there. I think it was a mistake someone made. Is there anything you'd comment there? Just like what happened, what went wrong, what should people know?

[00:12:15](https://youtu.be/PplmzlgE0kg?t=735) **CAT WU**

So we immediately looked into this when we saw it. We realized that this was the result of human error. There was a human working with Claude to write a PR — this was just an update to how we release our packages — and it actually went through two layers of human review. So this was a result of human error, and we've hardened our processes to make sure that it doesn't happen in the future.

[00:12:40](https://youtu.be/PplmzlgE0kg?t=760) **LENNY**

Is this person still at Anthropic? Are they doing alright?

[00:12:42](https://youtu.be/PplmzlgE0kg?t=762) **CAT WU**

Yes. Yes. It's a process failure, and the most important thing is to just learn from it and to add more safeguards so that it doesn't happen again. That's what we've been focused on, and most of those have shipped.

[00:12:54](https://youtu.be/PplmzlgE0kg?t=774) **LENNY**

Okay. Another question I had is OpenClaude. Recently there's been this move to keep people from using Claude subscriptions with their OpenClaude. People got really upset, they're confused why this is happening. It feels like there's harm caused to the open source community. What do people need to understand about what went into this decision?

[00:13:18](https://youtu.be/PplmzlgE0kg?t=798) **CAT WU**

So we've been seeing a lot of demand for Claude, and we've been working very hard to both scale our infrastructure and also to make our harness more token-efficient so that you can get more usage out of it. It wasn't designed for third-party products which have different usage patterns than our first-party ones. We spent a bunch of time trying to figure out what is the most seamless transition that we can offer. I was very happy to be able to say that everyone gets some credits alongside their subscription. But yeah, we did have to make the hard decision that we needed to prioritize our first-party products and our API. So this is a decision that resulted from that.

[00:14:02](https://youtu.be/PplmzlgE0kg?t=842) **LENNY**

This to me makes so much sense. You guys are subsidizing this usage at like $200 a month and there's basically unlimited use of this. I think people don't understand businesses are trying to make money. We're trying to be profitable here. We can't just give away compute when it's so in demand. So I get it. Coming back to the PM team, what does the PM team look like at Anthropic? How many PMs are there? How are they organized?

[00:14:26](https://youtu.be/PplmzlgE0kg?t=866) **CAT WU**

So we have a few PM teams. I think we're maybe around 30 or 40 PMs right now. We have the research PM team, who Diane leads, and this team is responsible for understanding all of the feedback from our customers for our models and then feeding that to the best research team to act on it, and they also shepherd the model launch. There's the Claude Developer Platform team that maintains the APIs that Claude Code is built on top of, and they also release things like managed agents, which is a way for you to build your agents and we can host it on your behalf. And then there's Claude Code that works on both Claude Code and the Co-work core products. There's enterprise that helps make Claude Code and Co-work easier to adopt for all of our enterprise customers — so this is everything from cost controls, RBAC, security controls, and just making sure that these enterprises feel very confident and comfortable using our tools. And then we also have our growth team that is responsible for growing across our entire product suite. So we work very closely with them on Claude Code and Co-work growth, and I know they also work with our other teams on CDP growth — growth of people who use the Claude API.

[00:15:42](https://youtu.be/PplmzlgE0kg?t=942) **LENNY**

Speaking of growth — so Amol was just on the podcast. He had this really interesting insight that most people haven't been sharing. There's always this sense that we need fewer PMs in the future. Why do we need PMs? Engineers can just ship. His take is that because engineers are moving so fast, PMs and designers are squeezed. There's less time to stay on top of everything that is happening — there's a feature shipping every day. So his take is he needs more PMs because it's hard to keep up. What's your take? Do you feel like there will be an increase in hiring of PMs? What do you think is going on with the PM profession long term?

[00:16:15](https://youtu.be/PplmzlgE0kg?t=975) **CAT WU**

I think all of the roles are merging. PMs are doing some engineering work, engineers are doing PM work, designers are PMing and also landing code. You can either hire a lot more engineers who have great product taste, or you can keep your engineering hiring the same and hire a lot more PMs to help guide some of their work. On our team we're pretty focused on hiring engineers with great product taste. This way we can reduce the amount of overhead for shipping any product. There are many engineers on our team who are fully able to end-to-end go from seeing user feedback on Twitter through to shipping a product at the end of the week with almost no product involvement. This I think is actually the most efficient way to ship something. So engineer and PM are kind of overlapping, and you will get a lot of benefit from having more of either. I think product taste is still a very rare skill to have, and we'll pretty much hire anyone who we feel has demonstrated this strongly.

[00:17:25](https://youtu.be/PplmzlgE0kg?t=1045) **LENNY**

And your background was in engineering, right?

[00:17:27](https://youtu.be/PplmzlgE0kg?t=1047) **CAT WU**

Yeah, I was an engineer for many years. I was then a VC very briefly before joining Anthropic. Almost all the PMs on our team have either been engineers or ship code here on Claude Code. That's one of the things that I think helps build trust with the team and also just enables us to move a lot faster. Actually, our designers also have been front-end engineers before.

[00:17:54](https://youtu.be/PplmzlgE0kg?t=1074) **LENNY**

Wow, because that's the big question. There's definitely this merging that's happening — the Venn diagrams you're combining. The big question for a lot of people is, if you're coming from engineering or product or design, which of those core skills is going to be most valuable? I could see at Anthropic and on Claude Code, engineering is very valuable. I'm curious if at other companies, if you have a design background, becoming a PM is more valuable, or just a PM background.

[00:18:16](https://youtu.be/PplmzlgE0kg?t=1096) **CAT WU**

I still think it comes back to product taste. As code becomes much cheaper to write, the thing that becomes more valuable is deciding what to write. What is the right UX for this feature? What is the most delightful way that a user can experience it? We get tens of thousands of GitHub issues asking for every single thing under the sun, and it takes a lot of care and taste to figure out, okay, which of these is worth building and what is the right way to build it. I think that skill set can come from any background, but I think that's the most important thing.

[00:18:53](https://youtu.be/PplmzlgE0kg?t=1133) **CAT WU**

I think the reason why an engineering background is particularly useful, at least for the next few months, is if you have an engineering background, you have a better sense for how hard something should be. That's often a factor in what you choose to build. If something is very easy to build, then maybe instead of debating it, you just spend an hour doing it. But if something is harder to build and you know that upfront — that this will cost a lot more for our team to get this out the door — so it helps a bit with the prioritization.

[00:19:27](https://youtu.be/PplmzlgE0kg?t=1167) **LENNY**

You said for the next few months — is that just because the models will get so good potentially in the next few months, you may not even need to know that as much?

[00:19:38](https://youtu.be/PplmzlgE0kg?t=1178) **CAT WU**

I think the valued skill sets do change quite frequently, and so it's really hard to predict more than a few months out. So it's less a commentary on what shift I think will happen and more of a commentary that I think large shifts will happen.

[00:19:53](https://youtu.be/PplmzlgE0kg?t=1193) **LENNY**

So you're not saying that's when Mythos comes out and we'll change everything, and we don't need to know anything about engineering.

[00:19:58](https://youtu.be/PplmzlgE0kg?t=1198) **CAT WU**

No, I'm just saying that every few months, it seems like there's a large increase in coding capability which then changes what other roles are valuable. I think the most important thing is to be able to have this first-principles thinking where you can figure out how the tech landscape is changing, what the team really needs from you, and to jump in and fix that hole. I think the work is becoming more amorphous, which means that a great PM is able to understand what all the gaps are, to figure out what the highest priority ones are, and then to figure out, okay, how do I learn that skill set, or what is the skill set that I have that I can apply to this challenge. I think the current environment values people who are able to wear a lot of hats, are able to swap them, and are very low ego about what work they do to help the team move faster.

[00:21:06](https://youtu.be/PplmzlgE0kg?t=1266) **LENNY**

I love this answer. There's this question I've been asking people in your shoes — folks that are at the bleeding edge of what AI is capable of and building with the latest tools — which is, where will human brains continue to be useful and necessary for a while until we get to super intelligence? What I'm hearing here is essentially picking the things to work on, knowing where the market's going, figuring out what to prioritize. And then it's knowing if the thing you've built is good and right and getting it out there in some early version at least. Does that sound right? Is there anything else of just like, where will human brains continue to be useful for at least the next few months?

[00:21:46](https://youtu.be/PplmzlgE0kg?t=1306) **CAT WU**

I think humans still provide a level of common sense that the models don't. There's a thousand moving pieces to any product launch. Some of them are very small, but there's always a lot that could potentially go wrong. The model doesn't always have a great sense of who all the stakeholders are, how they relate to each other, what their preferences are, what are the right venues to communicate with them to keep them on board. A lot of this more tacit common sense, like EQ kind of knowledge, is still very valuable. Of course, we want the models to get better at this, and I think they will be, but right now I think there are still gaps.

[00:22:24](https://youtu.be/PplmzlgE0kg?t=1344) **LENNY**

How do you just deal as a human going through so much constant change? Just being on the inside of the tornado — maybe it's calm there, but how do you stay on top of what's going on? How do you stay sane through all this craziness that we're moving through?

[00:22:39](https://youtu.be/PplmzlgE0kg?t=1359) **CAT WU**

I think our team is full of people who lean into the chaos. So we try to face every challenge with a smile, because there's always so much going on, there's always so many risks and tricky situations, that if you get too stressed about anything you'll burn out. So we really look for people who can look at a challenge, be like, "That's going to be hard but I'm excited to tackle it, and I'm going to do the best that I possibly can, and I know I won't be perfect, but I'll be able to sleep at night knowing that I did my best."

[00:23:13](https://youtu.be/PplmzlgE0kg?t=1393) **LENNY**

That's an interesting answer to what skills will be important in this future. I forget who said this — maybe Ben Mann — that this is the most normal the world will ever be.

[00:23:23](https://youtu.be/PplmzlgE0kg?t=1403) **CAT WU**

Yeah, it definitely gets harder. I feel like there are a lot of weeks where maybe Sunday night there's some P0, and then by Monday there's a P00, and by Monday afternoon there's a P0000, and you're like, "Wow, I can't believe I was so worried about that P0 from Sunday." But I think you just have to acknowledge that there's only so much that you can do, that you need to sleep well so that you can make good decisions next day, and just brutally prioritize where you spend your time. What's the most important thing to get right? And be okay letting things go. There are products that we ship that aren't as polished as I wish they were, but our top goal is to help empower professional developers. And if a product isn't successful, as long as it's not blocking the core use case, it's okay because we'll hear the feedback and we'll fix in the next release. Launching a feature that is buggy is the kind of thing that would have kept me up at night, but it is something that I am now able to live with knowing that we're going to get that quick feedback and we're going to fix it in the next release.

[00:24:32](https://youtu.be/PplmzlgE0kg?t=1472) **LENNY**

What I'm imagining is there's that GIF — I think it's maybe from Pirates of the Caribbean — where it's this guy walking down a pair of stairs on a ship, and the whole ship is just being demolished around him, and he's so chill, just strolling down the staircases, everything's falling apart. And that's interesting because everyone I've met from Anthropic is just so chill and so optimistic.

[00:24:51](https://youtu.be/PplmzlgE0kg?t=1491) **CAT WU**

Yeah, I think that's a really interesting insight — just having this calmness and optimism versus, "Oh my god, everything's crazy and going nuts." I think if you don't have it, you'll get pretty burnt out. I think we also tend to hire people who have been in the industry for a while and have experienced lots of ups and downs, and have a good sense for what gives them energy and how to maintain their energy over time. I think that's helped us a lot.

[00:25:20](https://youtu.be/PplmzlgE0kg?t=1520) **LENNY**

So interesting. Something that I wanted to ask about: there's these roles blurring, engineers are becoming PMs, everyone's dogs are cats, everyone's everyone. What do we lose in that world? Do we lose career ladders and clear career paths? Do we lose design consistency, code quality? There's probably some downsides. What are some things you find are just like, "Okay, that's something we're sacrificing for the greater good"?

[00:25:42](https://youtu.be/PplmzlgE0kg?t=1542) **CAT WU**

We're sacrificing product consistency. Historically, when code was expensive to write, you would carefully plan out everything in your product suite — how every product relates to each other, what the use case for every single one is, how they integrate. You would pretty much have one product for each use case. Now, with AI moving so quickly and with so many ideas that we need to test out, we do sometimes have features that overlap with each other. A lot of the times it's because there are two form factors that we love internally and we want the external audience to tell us which one is better. What that means for someone who's a new user is a new user might not know what is the best path to accomplish X. There is more education we need to do to help people understand what the core features are and what the best practices are for using them. This is the cost of launching a lot of features.

[00:26:48](https://youtu.be/PplmzlgE0kg?t=1608) **CAT WU**

I think users also feel like it's hard to keep up with the latest. Usually in traditional PM you ship a feature every month or quarter. So it's really easy for a user to understand, "Okay, I just need to check in on this once a month and I'll learn some new things, and if I ignore it for six months it's fine, I don't feel like I'm missing out." With these agentic tools — not just Claude Code and Co-work, but across the whole ecosystem — people feel this need to check Twitter every single day to see what the absolute latest thing is. I think there's more we can do to help people feel less like they're on this ever-increasingly-fast treadmill. I would love people to feel like they can just open these tools, the tools will educate them, or teach them what they want to know, and that they can just feel more brought along.

[00:27:48](https://youtu.be/PplmzlgE0kg?t=1668) **LENNY**

Yeah, I saw you launch this really interesting feature the other day — I think it's `/powerup` — where it basically walks you through all the cool ways and basically all the best practices to use Claude Code. Is that along these lines?

[00:27:55](https://youtu.be/PplmzlgE0kg?t=1675) **CAT WU**

Yeah, exactly. So in the past, we didn't actually want to do something like PowerUp because we felt like the product should be intuitive enough that you don't actually need to go through any tutorial. Over time, we've just realized that there are so many features and there's so much demand for a built-in onboarding experience that we diverged a bit from our original principle saying no onboarding flow, and added this because there are just so many users who wanted to know — there are 100 features, what are the 10 that I absolutely need to use? So we put that together.

[00:28:32](https://youtu.be/PplmzlgE0kg?t=1712) **LENNY**

Yeah, it's such a bizarre world. So Anthropic has been really successful with B2B enterprises where traditionally you don't launch a bunch of stuff — you just kind of have a quarterly release maybe, and it's like the opposite of every day we got something new. So just maybe following that thread — the run Anthropic has been on is just otherworldly. Anthropic was way behind when it started. It was always shared, this is just one of the least funded companies, didn't have distribution, wasn't the first to go. OpenAI was way ahead. It was just like, no way Anthropic has any chance to compete significantly long term. Now it's just killing it — beating the biggest companies' teams. The growth is just like $11 billion in ARR in a one-month, 100% growth — by the time this comes out it'll probably be even higher. Just being on the inside, what are some ingredients that have allowed Anthropic to be this successful and kind of come from behind and do this well?

[00:29:17](https://youtu.be/PplmzlgE0kg?t=1817) **CAT WU**

The two most important things are: one, this unifying mission. It's hard to state how important this is. We hire people who care most about bringing safe AGI to all of humanity. This is actually something that we reference frequently in our decisions about what our entire product org should focus on shipping. Because we put this mission above any individual product line, we're able to make very fast decisions that cut across the entire org and execute on them in a unified way. This is something that I've never seen at a company of our scale.

[00:30:13](https://youtu.be/PplmzlgE0kg?t=1813) **LENNY**

And just to make sure that's clear: essentially having the number one mission is safety alignment, making sure AI is good for the world. You're saying just having that as a clear mission makes decisions a lot easier to make.

[00:30:24](https://youtu.be/PplmzlgE0kg?t=1824) **CAT WU**

If there are two competing priorities, we'll talk about which one is more important for Anthropic's mission, and it makes it a lot easier to decide which of the two we prioritize. Then everyone will stand behind the one that we decide. Sometimes that means that, hey, we want to ship something on Claude Code, but this other thing is more important. So we deprioritize shipping this and we just wait until later.

[00:30:47](https://youtu.be/PplmzlgE0kg?t=1847) **LENNY**

What's really interesting about that is — it explains, I think, versus another company maybe rhymes with Bopen Bi — they did a lot of different things. What I'm hearing here essentially is, okay, we're not going to launch a social network, we're not going to launch a feed of interesting information, because it's not aligned to this mission. And that has kept Anthropic focused, which seems to be a core ingredient to the success.

[00:31:10](https://youtu.be/PplmzlgE0kg?t=1870) **CAT WU**

When I think about mission, I think about putting Anthropic's goals ahead of any individual or any individual product. For me, the second thing that we're very good at is focus. I think mission to me is slightly different. Mission means that teams are willing to make sacrifices that hurt their own goals and their own KRs in service of Anthropic's goals and Anthropic's KRs. People are very happy to make those trade-offs. An extreme example is, if Claude Code failed but Anthropic succeeded, I would be extremely happy. The whole team is very willing to make decisions that follow that chain of thought.

[00:32:01](https://youtu.be/PplmzlgE0kg?t=1921) **LENNY**

I don't know if you can talk about this in depth, but do you feel like the OpenClaude decision is a part of this — just like, okay, this is not furthering the mission of Anthropic, we need to stop this because it's not working in the way we want it to work?

[00:32:11](https://youtu.be/PplmzlgE0kg?t=1931) **CAT WU**

I think one of the most important things for Anthropic is to grow the number of users that we're able to reach. One of the ways that we're able to do this is with the Claude subscriptions with our first-party products. So we very much want to double down on that, but that does come at the expense of third-party products sometimes.

[00:32:28](https://youtu.be/PplmzlgE0kg?t=1948) **LENNY**

So we've been talking about Claude, Co-work, all these things. Something that I want to make sure people get — and I'm curious how you use these tools. There's Claude Code, there's Claude desktop, there's Co-work. What's the best way to understand when to use which? When do you use each of these three?

[00:32:44](https://youtu.be/PplmzlgE0kg?t=1964) **CAT WU**

So I tend to use Claude Code in the terminal when I'm just kicking off a one-off coding task and I want all of the latest features. The CLI is our initial product surface and it's also the one where our features often land first, so it's the most powerful of all the tools. That's what I tend to use when I'm just trying to kick off one or maybe a handful of tasks at a time.

[00:33:14](https://youtu.be/PplmzlgE0kg?t=1994) **CAT WU**

I think desktop really shines when you're doing something that requires front-end work. One thing I love to do is to use our preview feature. So if I'm building a web app, I'll often use Claude Code on desktop, I'll have the preview pane open on the right-hand side so that I can actually see the web app that I'm making in real time as I'm chatting with Claude. It's also really great for people who want something a bit more graphical. A terminal can feel very unfamiliar to someone who's non-technical. You get a bunch of these scary popups on your machine and you can't click around the way that you're used to in pretty much every other product that you use. There are a lot of people who just don't feel comfortable in terminal. If that's you, I would highly recommend checking out Claude Code on desktop. Desktop is also great for getting an at-a-glance view of everything that's happening. You can see your CLI terminal sessions in desktop, you can see your other desktop sessions, you can see your sessions that you kicked off on web and mobile. So it's a one-stop control plane where you can see all of your tasks.

[00:34:17](https://youtu.be/PplmzlgE0kg?t=2057) **CAT WU**

I think the benefit of web and mobile is that it's really great for kicking things off on the go. CLI and desktop both require you to be on your local laptop. This is contravening because sometimes you're out and about, you're touching grass, you're going on a walk and you don't have your laptop open. I can't count the number of people who I've seen holding their laptop open, tethered to their phone while they're outside. This just means that we're missing a product that solves that need. For me, what mobile lets you do is kick off these tasks on the go so that you don't need to bring your laptop everywhere and make sure that your laptop's open wherever you are.

[00:35:01](https://youtu.be/PplmzlgE0kg?t=2097) **LENNY**

I love that. I've seen people on planes — it's just like such a meme now — "I need to finish, let this agent finish, I can't shut this down, I need Wi-Fi."

[00:35:04](https://youtu.be/PplmzlgE0kg?t=2104) **CAT WU**

And then I think for Co-work, the role that this fills is, there's a lot of work that everyone does where the output isn't code. Whether that's getting to Slack zero or inbox zero, whether that's creating a slide deck for some customer meeting that's coming up, whether that's writing a quick doc on what the goals of a feature are or what the launch plan for a feature is — all these tasks produce outputs that are non-code, and Co-work is best positioned for that. The way that I split the products in my mind is, if I'm building something where the output is code, I'll use Claude Code or desktop or Claude Code on mobile. If the output is anything that's not code, I'll use Co-work for it.

[00:35:48](https://youtu.be/PplmzlgE0kg?t=2148) **LENNY**

People are just sleeping on the success that Co-work — it's just growing incredibly fast and I think people still don't understand maybe what it's for. Can you give us a couple use cases just in your work as a PM? What are some really interesting, maybe unexpected ways you use Co-work to save you time, get more work done?

[00:36:08](https://youtu.be/PplmzlgE0kg?t=2168) **CAT WU**

If you're getting started on Co-work, the first thing that you really need to do is connect all the data sources that are relevant to your role, because Co-work can only do a great job if it has access to all the context that it needs to be able to curate the output for you. What that means for me is I connect it to my Google Calendar, I connect it to my Slack, to my Gmail, to my Google Drive, so that it has the flexibility to find relevant context, to ask questions, to pull in threads. This substantially improves the quality of the result.

[00:36:48](https://youtu.be/PplmzlgE0kg?t=2208) **CAT WU**

The kinds of things I use it for: last night, I was working — we have this Code with Claude conference coming up, and there are a few talks that I'm giving there. One of the talks that we're doing talks about the transition of Claude Code from an assistant to a full-on agent. One of the things that I wanted to do in this talk was to showcase all of the products that we've been shipping that enable this transition, and also to figure out what are the success stories that people have had internally that we can use as demos. I have my Google Drive connected, I have Slack connected. Alex, who's our product marketer, put together a draft of what the points he thinks we should cover are. So I just fed this all into Co-work. I told Co-work the narrative that I want to tell, and it actually just worked for an hour. It walked through Twitter to see what we launched, it looked through our evergreen launch room, it looked in our Claude Code announce channel, which is where our team posts demos of how they've been getting the most value out of Claude Code. It synthesized all this together into this 20-page deck that I woke up to this morning, and I read through it and it was pretty good. There were a few tweaks, so I did have to give it a round of feedback — I like my slides to have extremely minimal words and it was a little too wordy — but it was far faster than what I would be able to produce. Because Co-work has access to our whole design system, it actually looks like an Anthropic designer put it together. When you visually see it, you're like, "Oh, this is incredibly polished." These are the kinds of things that are so much faster — making this slide deck would have taken me hours, but instead it turns out a draft that is actually quite good, so I could focus on making sure that the demos are amazing that we plug into it.

[00:39:08](https://youtu.be/PplmzlgE0kg?t=2348) **LENNY**

This sounds like a dream come true to PMs. Putting decks together — so annoying.

[00:39:09](https://youtu.be/PplmzlgE0kg?t=2349) **CAT WU**

It's so slow.

[00:39:11](https://youtu.be/PplmzlgE0kg?t=2351) **LENNY**

People will see this deck whenever you present this. This will be out in the world. Obviously it's not the one-shotted version, you've iterated on it. So just to help people try this for themselves: step one is connect — what did you say? Slack. What else do you suggest they connect?

[00:39:27](https://youtu.be/PplmzlgE0kg?t=2367) **CAT WU**

Slack, Google Calendar, Gmail, G Drive. You should connect your communications tools and where you store your source-of-truth data for what your team cares about, what you care about, and what you're working on.

[00:39:41](https://youtu.be/PplmzlgE0kg?t=2381) **LENNY**

Okay. And then what was the prompt roughly that you put in there to generate this deck?

[00:39:46](https://youtu.be/PplmzlgE0kg?t=2386) **CAT WU**

So I just wrote: "Make me a slide deck for the Code with Claude conference. This is what our PMM suggested it should cover. This is the current draft that I made that I don't like. This is one that I made manually that I don't like, but I linked it. Can you start by creating a proposed outline with details? Also, make sure it doesn't overlap too much with a keynote talk, which is more important." Then Claude read a bunch of the links that I sent to it and created a proposed outline. So then I read through its proposal and all the different ideas that it had generated for what we could cover, and I just made a decision on what I wanted to actually be in the final deck. I think this is an example of what the role of the PM still is today. Claude is a great brainstorming partner. It's able to synthesize a massive amount of information really quickly and present all of the possibilities to you. But the role of the PM is still to make the end decision of, okay, what should belong in the final product. For this, what I ended up deciding was that I wanted the talk to cover the progression from making local tasks successful to making every PR green, to helping engineers land more PRs, and for each of these, which demo would be the most compelling. After this decision about the outline, Co-work just went off for a few hours and built the whole slide deck.

[00:41:30](https://youtu.be/PplmzlgE0kg?t=2450) **LENNY**

This is so awesome. What an awesome part of the job to not have to do anymore. It feels like you're talking to essentially a deck designer that also has actual knowledge about what you've worked on and can make it actually the content what you want it to be, not just make it look really nice. How did you do the design system piece? How does it know the design system of Anthropic?

[00:41:54](https://youtu.be/PplmzlgE0kg?t=2474) **CAT WU**

So what I did for this is we actually already have a standardized deck that we use across all of our external engagements. I just gave Claude access to that. So it's able to see what colors we use, what fonts we use, the different kinds of slide formats that are possible. It has like 20 of these example slides.

[00:42:18](https://youtu.be/PplmzlgE0kg?t=2498) **LENNY**

Got it. So you upload, "Here's our template, work from this."

[00:42:20](https://youtu.be/PplmzlgE0kg?t=2500) **CAT WU**

Yeah. You can also connect to your Figma MCP if you have your slide format saved there, and it can pull that in.

[00:42:28](https://youtu.be/PplmzlgE0kg?t=2508) **LENNY**

Along those lines, something I'm always curious about is what's in your stack of tools as a PM at Anthropic. Obviously Claude Code and Co-work and all the Anthropic tools — what else are you using? Slack you mentioned. Is there anything else?

[00:42:42](https://youtu.be/PplmzlgE0kg?t=2522) **CAT WU**

So my stack is pretty heavily Claude Code, Co-work. Anthropic largely runs on Slack. I feel like it's the core OS of our company. Day-to-day, I would say maybe 30% of my time is pushing the boundaries of what Co-work can do so that I have a very strong sense of what we're not good at. I spend a lot of time talking with the model to understand why it makes the mistakes that it does. We actually have a lot of internal tools that we make. One of the things that Claude Code has really unlocked for our entire company is it really lowers the barrier to making any custom app that you want. We've seen this surge in personalized work software that people are building for custom use cases instead of using tools that don't perfectly fit the use case.

[00:43:46](https://youtu.be/PplmzlgE0kg?t=2586) **LENNY**

I gotta hear more. What are some examples? What are things you've built, other people have built, that are really popular and useful?

[00:43:52](https://youtu.be/PplmzlgE0kg?t=2592) **CAT WU**

One of the sales folks on Claude Code — he realized he was making these repetitive decks over and over and over again. So he actually has this web app that he built with the examples of the core Claude Code decks that we know work well — like a 101, 201, and Mastering Claude Code. And then he has a way to input specific customer context that pulls from Salesforce, that pulls from Gong, that pulls from other notes, so that we can customize the decks for specific customers. It'll pull out things like, "Okay, this customer is using Bedrock, or Claude for Enterprise, or Console," which affects what features are available to them. It will pull out things like, "Okay, this customer is concerned about the code review stage of the SDLC," and so we'll add a slide about our code review features there. It'll pull out things like, "Okay, this customer needs to be HIPAA compliant or needs XYZ security controls," so we'll make sure to add a slide or two in their deck about that. If this is a customer that's on Vertex or Bedrock and doesn't want to use Claude for Enterprise, then we'll just take out some of the slides that are Claude for Enterprise-only features. Normally this is manual work that could take 20-30 minutes, so people either spend that time doing it or they'll just decide not to do it and use the general deck. With this, it takes like a few seconds and you get a tailored deck.

[00:45:22](https://youtu.be/PplmzlgE0kg?t=2682) **LENNY**

What's interesting is — Slack is the tool that nobody's trying to create their own. Slack just continues to win, and the way you describe it is kind of the OS of so many companies. It's so interesting. People talk about Salesforce as just like SaaS — we don't need SaaS software anymore, we're going to build our own. Slack is a durable tool that nobody wants to try to compete with and build a better version.

[00:45:46](https://youtu.be/PplmzlgE0kg?t=2706) **CAT WU**

I think it's pretty important communications infrastructure, and I think they do the core task of helping everyone get real-time updates incredibly well.

[00:45:53](https://youtu.be/PplmzlgE0kg?t=2713) **LENNY**

Yeah. Like people hate on Slack, but it's really great at what it's trying to do, and the most cutting edge teams are hooked on it.

[00:46:01](https://youtu.be/PplmzlgE0kg?t=2721) **CAT WU**

Yeah. And I also love how easy they've made to customize it. We love making Slack bots, and this kind of hackability means that we're able to integrate with Slack the way that we want to. So really appreciate Slack's work on that.

[00:46:17](https://youtu.be/PplmzlgE0kg?t=2737) **LENNY**

Time to buy some CRM stock. I am so excited to tell you about this season's supporting sponsor, Vanta. Vanta helps over 15,000 companies like Cursor, Ramp, Duolingo, Snowflake, and Atlassian earn and prove trust with their customers. Teams are building and shipping products faster than ever thanks to AI, but as a result, the amount of risk being introduced into your product and your business is higher than it's ever been. Every security leader that I talk to is feeling the increasing weight of protecting their organization, their business, and not to mention their customer data. Because things are moving so fast, they are constantly reacting, having to guess at priorities, and having to make do with outdated solutions. Vanta automates compliance and risk management with over 35 security and privacy frameworks including SOC 2, ISO 27001, and HIPAA. This helps companies get compliant fast and stay compliant more than ever before. Trust has the power to make or break your business. Learn more at vanta.com/lenny. And as a listener of this podcast, you get $1,000 off Vanta. That's vanta.com/lenny.

[00:46:50](https://youtu.be/PplmzlgE0kg?t=2810) **LENNY**

Okay. So you talked about all these different teams and how they use Claude Code and Co-work to operate. Which teams do you find — other than engineering, I imagine engineering is the biggest token spender, but if not, that'd be really interesting. What's the second-place function right now for tokens?

[00:46:58](https://youtu.be/PplmzlgE0kg?t=2824) **CAT WU**

Oh, applied AI is amazing at pushing the boundaries of what Claude Code and Co-work can do. A lot of our applied AI team spends time with our customers helping them adopt our API. Sometimes our applied team will, for example, make prototypes on behalf of these customers, which Claude Code makes so much faster than it used to be. They also have the dual goal of needing to manage a lot of customer comms, a lot of customer inbound and historical context, call notes. So they're both extremely heavy on Co-work and on Claude Code.

[00:47:42](https://youtu.be/PplmzlgE0kg?t=2862) **LENNY**

And just to understand applied AI — is that like a forward-deployed engineering sort of role? How would most people describe what the applied AI team is doing?

[00:47:53](https://youtu.be/PplmzlgE0kg?t=2873) **CAT WU**

Yeah, it's helping our customers adopt the latest API and model features across their company, both for powering their company's products and also for internal acceleration.

[00:48:05](https://youtu.be/PplmzlgE0kg?t=2885) **LENNY**

Got it. So it's customer-success-go-to-market kind of, like a forward-deployed engineering sort of.

[00:48:10](https://youtu.be/PplmzlgE0kg?t=2890) **CAT WU**

Exactly. It's like a very technical go-to-market person.

[00:48:14](https://youtu.be/PplmzlgE0kg?t=2894) **LENNY**

Got it. Okay. Awesome. So you're saying that might be the second org that uses the most tokens.

[00:48:19](https://youtu.be/PplmzlgE0kg?t=2899) **CAT WU**

Yeah. We also see them pushing the boundaries of what Co-work can do. A lot of these folks cover multiple customers and in any given day can have like five to ten customer engagements on a high day. What they often use Co-work to do is, the night before, they'll ask it to summarize: what are all my customer meetings that are coming up the next day? What are all the things that this customer has asked me for, what's top of mind for them, what are the action items from the past meetings? And Co-work will just put together this dossier, this brief of what they should be aware of going into the next meeting. Co-work can also research answers — so if a customer asked, "Okay, when is feature X going to launch?", Co-work can help the AAI person research through Slack to get the latest ETA, add that to the notes, so that during the customer call the AAI person has the absolute latest. These are just workflows that people are building for themselves and sharing with other people on their team.

[00:49:25](https://youtu.be/PplmzlgE0kg?t=2965) **LENNY**

So cool. This question, this trend — I don't know, question, topic — comes up a lot recently, which is token spend exceeding people's salary, where people just use AI and it costs more than how much they're making. Are there any numbers floating around Anthropic of just like how much token spend, say engineers, spend a month, a day, PMs, anything like that?

[00:49:51](https://youtu.be/PplmzlgE0kg?t=2991) **CAT WU**

It is clear to us that as the models get better, people delegate far more tasks to it and they spend a lot more hours in tools like Claude Code and Co-work. We do see the token cost per engineer, or per any knowledge worker, increase every time that there's a model jump or a substantial product improvement. I think it's still much lower than what the average engineer salary is, but we see the percentage increasing over time.

[00:50:21](https://youtu.be/PplmzlgE0kg?t=3021) **LENNY**

It's such an interesting — we talked about how you have access to the most cutting edge models and other advantages of working at Anthropic. I believe you guys have basically unlimited tokens, you can use as much as you want. Is that right?

[00:50:33](https://youtu.be/PplmzlgE0kg?t=3033) **CAT WU**

We can use a lot of tokens. Some people do run into limits.

[00:50:36](https://youtu.be/PplmzlgE0kg?t=3036) **LENNY**

Okay, there's a limit. Okay, Boris, shut it down. It's so interesting how many advantages come from having the most advanced model. It's such an interesting flywheel that starts to kick in.

[00:50:46](https://youtu.be/PplmzlgE0kg?t=3046) **CAT WU**

I think we also believe a lot in empowering our internal teams to build as fast as possible. We also trust that everyone understands how much capacity that serving these models truly costs, and we trust our team to use the tokens responsibly. So it's very frowned upon to waste tokens, but we do trust individuals to make that judgment call.

[00:51:14](https://youtu.be/PplmzlgE0kg?t=3074) **LENNY**

Awesome. Coming back to the PM role — we talked a little bit about this, but I think this will be really interesting for people to hear. What I want to understand is, what do you think are the emerging skills that PMs need to develop, slash you most look for, AI companies most look for when they're hiring PMs these days?

[00:51:35](https://youtu.be/PplmzlgE0kg?t=3095) **CAT WU**

I think the hardest skill is being able to define what the product should look like a month from now. There's a lot of ambiguity in what models are capable of in that timeline and how user behavior will change. But there are patterns that the best PMs can see based on how users are abusing the limits of the existing product. The best PMs can sense that, can set a direction, can steadily execute towards it, and change the path if the model capabilities are much better or worse than what they had originally expected.

[00:52:14](https://youtu.be/PplmzlgE0kg?t=3134) **CAT WU**

I think it is very hard to be the right amount of AGI-pilled, because everyone can see this future where the models are extremely smart and can do almost everything, in which case you actually don't need that complicated a product. You can actually just have a text box again where you tell the model what you want, and it's so smart that it can add any tool or add any integration that it needs to get the job done. It knows when it's uncertain, it can ask clarifying questions. It's kind of very easy to build the product for the super-AGI strong model. The hard thing is figuring out, for the current model, how do you elicit the maximum capability? How do you help users get onto the golden path? How do you guide users to interact with the model's strengths and patch its weaknesses? This skill is pretty rare.

[00:53:19](https://youtu.be/PplmzlgE0kg?t=3199) **LENNY**

And how do you build that skill? Is it just using each model, basically understanding the limits of each model, having taste — you talked about taste — understanding having taste into what the model maybe is capable of, what it's great and not great at, where it's changed.

[00:53:32](https://youtu.be/PplmzlgE0kg?t=3212) **CAT WU**

I think it's spending a ton of time talking with and using the model. One of the things I really like to do is to ask the model to introspect on its own behaviors. Sometimes when I notice that the model does something unexpected — for example, there are situations where the model will make a front-end change and run tests but not actually use the UI — it's actually pretty useful to ask the model to reflect on why it did this. Sometimes they'll say, "Hey, there was something confusing in the system prompt, or I didn't realize that the front-end verification was part of this task," or, "Hey, I delegated the verification to this sub-agent, and the sub-agent didn't do the test, and I didn't check its work." A lot of times just being very curious about why the model made the decision that it did will show you what misled it, so that you can fix the harness in order to close this gap.

[00:54:31](https://youtu.be/PplmzlgE0kg?t=3271) **CAT WU**

The other thing that helps is to figure out who are the users that you trust the most to give you accurate feedback about the model. Usually there's a handful of people who are much better than others at articulating what makes a specific model or model-harness combination good. There are a lot of people who will give you feedback, but not everyone's feedback is as qualified. Finding a group of those like five people you trust is really important for getting very fast feedback.

[00:55:03](https://youtu.be/PplmzlgE0kg?t=3303) **CAT WU**

I think the third thing that is useful but not everyone loves doing is building evals. You don't need to build hundreds of evals for them to be useful — just building 10 great evals is important for helping the team quantify what the goal is, what their progress towards it is, and what they're missing. Evals are this underappreciated thing that more PMs and more engineers should be working on.

[00:55:33](https://youtu.be/PplmzlgE0kg?t=3333) **LENNY**

We've covered evals a bunch. There's this trend of just like that is the future of product management — writing evals, because essentially it's, what does success look like? Okay, cool. Let me actually concretely define it, and then we'll know. How much of your time are you spending writing evals would you say?

[00:55:46](https://youtu.be/PplmzlgE0kg?t=3346) **CAT WU**

I think the importance of evals varies a bit based on the feature that you're working on or what the problem you're trying to solve is. There are a lot of folks on our team who do spend a lot of time working on evals — we have a small pod of folks who collaborate very closely with research to more precisely understand our Claude Code behaviors and what the largest areas of improvement are, and trying to measure those pretty concretely. I personally jump into evals when there's a feature that I think needs a bit more product definition. Often the output of this is, "Okay, here are like five evals that I made, this is how you run them, these are the ones that succeed and these are the ones that don't, and this is the prompt that I've used to increase the success rate." It varies a lot based on the exact feature — not every feature needs it, but features such as memory benefit a lot from this.

[00:56:50](https://youtu.be/PplmzlgE0kg?t=3410) **LENNY**

That point you made about people being very good at evaluating models — so interesting. It's almost like a human eval of just like, okay, they understand where it's spiking or it's maybe lacking. Is there anyone specific that you want to shout out that's very good at this?

[00:57:00](https://youtu.be/PplmzlgE0kg?t=3420) **CAT WU**

Two people who I think are incredible at this are: one, Amanda, who molds Claude's character. It's just such a hard role because the task is so ambiguous. Even coding is easier because you can verify the success, whereas crafting the character requires a very strong sense of conviction in who Claude should be. I think she has an incredible ability to not only mold the character, but also to articulate what the goals are, what the character is, what's successful and what's not.

[00:57:43](https://youtu.be/PplmzlgE0kg?t=3463) **CAT WU**

The other group of people who I really trust is just the Claude Code team. We often have team lunches, and whenever there's a new model we're testing, one of the fastest ways for us to get feedback is to just go to every single person and just be like, "Hey, what is your vibe on the model?" Oftentimes we'll get feedback like, "Okay, this model is not fully explaining its thinking, it's too abrupt," or, "Hey, this model just loves writing a ton of memories, but we're not sure if the memories are high quality or not," or some people will notice, "Okay, this model loves to test itself, which is great," or, "This model isn't testing itself enough." That informs what data we look at to verify, "Okay, is this a larger pattern?" We have a ton of data, but it is very hard to extract insights, and so the feedback from this group helps us inform what are the hypotheses we want to test, and then we're able to extract data to test that.

[00:58:45](https://youtu.be/PplmzlgE0kg?t=3525) **LENNY**

This point you made about the character of Claude — I had Ben Mann on the podcast, co-founder, and he talked about this. Just the character, the constitution of Claude is such an important part of Claude. I didn't realize until afterwards — like, with OpenClaude actually, one of the reasons people are sad is the personality of Claude is so good and fun and interesting, unlike other models. The way he put it is, the personality is what makes Claude so good at so many things. It feels like this trivial side thing — okay, it's going to be funny and interesting and talk in a fun way — but it's so core to the success of Claude. Is there anything you'd add about what people may not understand about why the character, as you described, and the personality is so key?

[00:59:34](https://youtu.be/PplmzlgE0kg?t=3574) **CAT WU**

When you reflect on everyone you've worked with, there's just some people where you're like, "I really like their energy. I really like their vibe." When people think about Claude and Claude Code, this is one of the things that people bring up the most, where they just really love that Claude is lighthearted and fun, but it also is extremely competent at your task. People really like that Claude's low ego — so if you tell it, "Hey, you did this thing wrong," it's like truly sorry. It's like, "Oh shoot, thanks for telling me. Let me fix it. Let's work together." It's also very positive. So if you're feeling like, "Oh, this is like an insurmountable task, I don't know how to get started," Claude is like, "Okay, it's okay, these are the steps that I think we should take. Do you want me to get started on it for you?" Part of what makes a great co-worker is this positivity, this bias towards action, this ability to give you earnest feedback, not just agreeing with every single thing that you say. We try to imbue this into Claude because we think it makes it a lot more enjoyable to work with.

[01:00:45](https://youtu.be/PplmzlgE0kg?t=3645) **LENNY**

There's something I want to come back to. You talked about how when new models come out, you often have to revisit things you've built. That's so interesting and so frustrating, maybe — like, "Oh god damn it, we shipped this thing, now we have to rethink it." Talk about how often you have to come back with a new model and we're like, "Okay, we have to redo this product that we launched a few months ago."

[01:01:03](https://youtu.be/PplmzlgE0kg?t=3663) **CAT WU**

A lot of the changes that we make with a new model is removing features that are no longer needed. A lot of times we add features to the product as a crutch for the model because it's not naturally doing it itself. The classic example for this is a to-do list. When we first launched Claude Code, people would ask it to do these large refactors, and Claude Code would say, "Okay, cool, I need to change these like 20 call sites," and it would go and change five of them and then stop. We were like, "Okay, how do we force it to remember to get every single one of these 20?" And so Sid on our team was like, "Okay, what if we just think about what a human would do? A human would make a list of everything that they need to change. Similar to how in VS Code you would look up all the call sites, and it would be a list on the left side, and you would go through them one by one and replace all. How do we give this kind of tool to Claude?" So he added a to-do list, and we found that with that, Claude was actually able to fix all these 20 call sites.

[01:02:04](https://youtu.be/PplmzlgE0kg?t=3724) **CAT WU**

But then with Opus 4 and later models, we realized that we didn't need to force it to use this to-do list. It would naturally use it itself. For the earlier models, we had to keep reminding it, "Hey, did you finish everything on the to-do list? You can't finish until you're done with everything on the to-do list." For the later models, without prompting, it just naturally thinks to do everything on the to-do list. These days, the to-do list is still nice to have as a user, because then you can more clearly see what Claude is working on. But honestly, it's such a deemphasized part of the product right now that the model may use it, the model may not use it. It's really not necessary for it to make thorough changes anymore.

[01:03:04](https://youtu.be/PplmzlgE0kg?t=3764) **LENNY**

I forget who said this on the podcast, that the model will eat your harness for breakfast. What I'm hearing here is essentially, you remove things over time that you've had to add on top of the model where it was not operating the way you wanted. As the models get smarter, it just becomes simpler and simpler for it just to do the thing you want it to do.

[01:03:24](https://youtu.be/PplmzlgE0kg?t=3784) **CAT WU**

Yeah. We can remove a lot of prompting interventions every time the model gets smarter. We actually do this every time we launch a model. We read through the entire system prompt and we reflect on, okay, for each of these sections, does the model really need this reminder anymore? And if not, we'll remove it.

[01:03:42](https://youtu.be/PplmzlgE0kg?t=3802) **CAT WU**

The most exciting thing that new models unlock though is just entirely new features. There are a lot of features that we've been testing out with prior models, and the accuracy wasn't high enough for us to want to launch them. One example of this is code review. We tried to build a code review product a few times, and we've launched simpler versions of code review — which is the `/code-review` command in the past — and it was only with the most recent models that we felt like, okay, this code review is so good that our engineering team relies on this code review to pass before we merge PRs. We've always dreamed of Claude being able to be a reliable code reviewer that we can confidently feel catches the majority of bugs, and it was only with Opus 4.5 and 4.6 and Sonnet 4.6 that we felt we are now able to run multiple code review agents simultaneously to traverse the entirety of the code base and to synthesize a set of real issues that an engineer needs to address before merge. This is a new capability that the newest models have unlocked.

[01:04:39](https://youtu.be/PplmzlgE0kg?t=3879) **LENNY**

This is another trend that is very common on this podcast, of: build something that will possibly be possible in the next six months. Be at the edge of what's working sort of, and then it'll catch up, and then it'll be an amazing product, and you'll be ahead of everyone.

[01:04:52](https://youtu.be/PplmzlgE0kg?t=3892) **CAT WU**

Yeah, exactly. It's pretty important to build products that don't necessarily work yet, so that you know what is missing for this product to work. Then with the newest model, you can just swap it in to the prototype you've already made and see, okay, does this new model close that gap.

[01:05:13](https://youtu.be/PplmzlgE0kg?t=3913) **LENNY**

How much are you able to speak to where things are going with Claude and Co-work, kind of the vision of it? I imagine you don't want to give away too much about the goal, but it feels like there are all these awesome features being added on top — dispatch, control from phone, and all these mobile app, all these things. What's a way to understand the vision for all these things long term?

[01:05:32](https://youtu.be/PplmzlgE0kg?t=3932) **CAT WU**

We think about this in terms of building blocks. For both Claude Code and Co-work, the core building block is making individual tasks successful. You want to produce some output, you give it a clear prompt description — is it able to consistently produce acceptable output that you're able to either merge or share with your colleagues or external audience? The task is the core building block. As the models get smarter, the task success rate gets a lot higher.

[01:06:18](https://youtu.be/PplmzlgE0kg?t=3978) **CAT WU**

Then we see people moving towards doing multiple tasks at the same time. Multi-coding was this big thing in towards the end of 2025, and it's only increased since then. We see this as, okay, great — one task works, and now you can do like six tasks at a time. As the models get even smarter, the way that we are extrapolating this is, okay, next maybe you're going to run like 50 Claudes at a time or hundreds of Claudes at a time. So what is the infrastructure we need to build to enable that? At that point, you're probably not going to run everything locally on your machine anymore. There's just not enough RAM to do it. So we're thinking about, how do we make it easier for you to manage all these? These will probably run remotely. How do we build the interface so that you, as a human, know which tasks you need to look into? How do we make sure that the agent is fully verifying work, so that when you look at a task and it says it's done, you can very quickly verify and fully trust that it is done to your spec? How do we make sure that this process is self-improving, so that when you do see a task that isn't done to your liking, you can give it feedback, and the model will know for every future run to incorporate that feedback so it never makes that mistake again? This is the progression that we're bringing our users along for.

[01:07:23](https://youtu.be/PplmzlgE0kg?t=4043) **LENNY**

There's a lot of people listening — a lot of product managers, a lot of maybe founders, a lot of other cross-functional folks listening. There's a lot of worry about just how their role, the future of their careers. What advice would you have for people to not just survive this transition to this very AI-driven world, but to be really successful, to essentially thrive in this future? What are things people need to hear, need to be doing?

[01:07:49](https://youtu.be/PplmzlgE0kg?t=4069) **CAT WU**

I think AI gives everybody a ton more leverage than they used to. So I would push you towards, anytime you realize that you're doing some manual task multiple times, think about how you can use Claude Code, Co-work, or other AI tools to automate that for you. Most people have creative parts of their job that they absolutely love, and then tedious parts of their job that they really hate doing. The beauty of AI is that it can do those tedious parts for you. It can learn from every time that you've done that manual task and generalize, and then run it automatically, so that you can focus on the creative parts. That means you can do a lot more than you used to be able to do. My immediate push for people is figure out the repetitive parts that you can pass to Claude. Iterate on those automations until the success rate is very high, and then focus on, okay, what more can you be doing for your team, for your product, for your company that people haven't had the bandwidth to pick up so far? What is that pet project that you always thought the company should do that you've never had bandwidth to do? If AI can take care of the grunt work, then you have this extra 20% time now that you might not have before. So my push is to lean into these tools, hand off the work that you're not excited to do, figure out how it can accelerate you, and then as a result, you'll be able to do so much more.

[01:09:19](https://youtu.be/PplmzlgE0kg?t=4159) **LENNY**

Something core to what you just shared, which I fully agree with, is find problems to solve with AI. There's all this potential, what all these tools can do. For a lot of people, the hardest part is just like, what should I actually do? What you're saying here is just pay attention to things that you are doing constantly that you can automate. Pay attention to ideas that have been floating around that you haven't had time to do. It's basically solve a problem for yourself is kind of the core advice there.

[01:09:45](https://youtu.be/PplmzlgE0kg?t=4185) **CAT WU**

Exactly. I would also push listeners towards focusing on bringing your automations from, "Okay, this is a cool concept" to, "Hey, this actually works 100% of the time." Sometimes I see users trying to automate something, getting it to like 90, 95% accuracy, and then giving up on it. If an automation doesn't work 100% of the time, it's not really an automation. That last 5 to 10% does take more time. Also, building the automation is often a lot slower than you doing it yourself. I would encourage listeners to put in that time to scope some automation that you really want to get to 100%. Put in the elbow grease to teach Claude your preferences, to give it feedback so that it can improve its skill so that it can get to that 100%. Then really, then you'll be able to rely on it. There's just not much value in a 95%-there automation.

[01:10:46](https://youtu.be/PplmzlgE0kg?t=4246) **LENNY**

I am super guilty of that. This is really good advice for me.

[01:10:48](https://youtu.be/PplmzlgE0kg?t=4248) **CAT WU**

I am guilty of this too. I've been teaching Co-work to try to get me to inbox zero for Gmail, and it has been very time consuming, and it is definitely not there, as you probably realized.

[01:11:02](https://youtu.be/PplmzlgE0kg?t=4262) **LENNY**

Yeah, funny enough, that's exactly where my mind goes. I have this workflow I set up where every email I get, it looks for things that are spammy — which is just like all these "Hey, can I come on your podcast?" or "What about this one?" — all these things I'm just like, I don't have time for. I have it categorized into a folder called "spammy". It's like 95% great, but then there's like, "Oh wow, I missed an email because it went in there." So this is a good push for me. I'm going to work on this. I'm going to get it to perfect.

[01:11:29](https://youtu.be/PplmzlgE0kg?t=4289) **CAT WU**

Yeah. We also are working on making the flow for customizing these commands a lot easier, because right now I think you have to know too many concepts. You have to know to define a skill, you have to know to use this skill and give it feedback. Then you have to know to tell Co-work to update the skill based on all the feedback that you gave. Then you also have to know where to read the skill to make sure that the feedback was incorporated the way that you want. It's also our job to make this flow really seamless so that it doesn't feel painful to do.

[01:11:57](https://youtu.be/PplmzlgE0kg?t=4317) **LENNY**

Amazing. Is there anything else, Cat, you wanted to share? Anything else you wanted to leave listeners with? Anything you wanted to double down on that we haven't already touched on before we get to our very exciting lightning round?

[01:12:08](https://youtu.be/PplmzlgE0kg?t=4328) **CAT WU**

I see a lot of people playing around with AI and building prototype apps and tinkering with building workflows. I would really push people towards building apps that you're actually using every single day, because I think only through that usage are you actually getting the value. If you build a prototype app that isn't helping you get more done, then the AI isn't really adding value to your day. There's only so much you learn from when it's like, "Okay, I just one-shotted something. Oh, that's cool." And then you never come back to it. You're not learning a lot, and you're not getting much leverage from it.

[01:13:10](https://youtu.be/PplmzlgE0kg?t=4370) **CAT WU**

I also think there are a lot of people who spend a lot of time customizing their workflow. There's like two ends of the spectrum. One is people who never customize or never build automations, but there's this polar opposite end of people who obsess around customizing their tool — like adding a ton of skills and MCPs and these workflow improvements — and I think sometimes that can even distract from your core goal of launching some product or building some feature. There's a lot of fun in customizing, and we definitely want to make our products very hackable so that you can make it work really well for you, but there is a limit to how much it's useful. There's a camp of people who maybe spend so much time customizing that they're not sleeping and not doing the core task that they originally set out to do.

[01:14:02](https://youtu.be/PplmzlgE0kg?t=4424) **LENNY**

I see a lot of that on Twitter — just like, "Look at my setup, it's out of control, it's so optimized." Then what are you actually building? "No, but my setup is so awesome, it gets so much done."

[01:14:12](https://youtu.be/PplmzlgE0kg?t=4432) **CAT WU**

I think the simple setups actually work better.

[01:14:16](https://youtu.be/PplmzlgE0kg?t=4436) **LENNY**

`/powerup` to take it level up a little bit.

[01:14:22](https://youtu.be/PplmzlgE0kg?t=4442) **LENNY**

There's this Karpathy tweet that just came out yesterday where he talked about this divide that's interesting between people that tried ChatGPT, Claude back in the day. It was like, okay, and they're like, "Nah, this is terrible," and they kind of gave up on what AI could do for them, and they're just like, so cynical of, "No way, it's not actually that big of a deal." And then there are people that are using it to code, essentially, who see the full intense power of it and how good it is. And people on both sides don't understand the other side and how they see the world. So your advice is really good here — just like, actually use it for real things and see how good it actually has gotten.

[01:14:58](https://youtu.be/PplmzlgE0kg?t=4478) **CAT WU**

Yeah, I think the big shift is that the 2024 generation of products were chat-based, and the Claude Code generation of products is action-based. The big aha moment people have is when Claude can just do things on your behalf. It is an amazing feeling to know that the agent is capable of doing so much more than telling you what to do — like, the agent can actually just do it itself. When people feel that, I think that's the eye-opening moment.

[01:15:30](https://youtu.be/PplmzlgE0kg?t=4510) **LENNY**

Shout out the Claude Chrome extension, which you can just watch it doing stuff and you'd be like, "Fill out this form for me." And like, "Alright, here I go."

[01:15:38](https://youtu.be/PplmzlgE0kg?t=4518) **CAT WU**

Exactly.

[01:15:39](https://youtu.be/PplmzlgE0kg?t=4519) **LENNY**

Okay. Anything else before we get to our very exciting lightning round?

[01:15:42](https://youtu.be/PplmzlgE0kg?t=4522) **CAT WU**

No, let's do it.

[01:15:44](https://youtu.be/PplmzlgE0kg?t=4524) **LENNY**

Let's do it. Cat, I've got five questions for you. Welcome to the lightning round. There's this animation that plays. I have to make sure to say it. Are you ready?

[01:15:52](https://youtu.be/PplmzlgE0kg?t=4532) **CAT WU**

I'm ready.

[01:15:54](https://youtu.be/PplmzlgE0kg?t=4534) **LENNY**

First question: what are two or three books that you find yourself recommending most to other people?

[01:15:58](https://youtu.be/PplmzlgE0kg?t=4538) **CAT WU**

I really like *How Asia Works*. It's a story about economic development, and what are the policies and governments that make long-lasting successful economies. The other book that I'm really into is *The Technology Trap*. This is actually about the past few technology revolutions — the industrial revolution and the computer revolution — and how this has affected workers. The reason that I really like this is because I think there's a lot we can learn from history to make sure that this transition goes well. And maybe on a fun note, I really like *Paper Menagerie*. It's just like a book of short stories about coming of age and AI and self-discovery.

[01:16:32](https://youtu.be/PplmzlgE0kg?t=4592) **LENNY**

Favorite recent movie or TV show you have really enjoyed?

[01:16:34](https://youtu.be/PplmzlgE0kg?t=4594) **CAT WU**

I really like *Drive to Survive*. There's no deeper meaning to it. There's just something very satisfying about people being so obsessed with a singular engineering goal, and just the purity of their pursuit. I also really love *Free Solo*, which is about Alex Honnold climbing El Capitan without a harness. Similarly, it's just such a pure achievement to be able to climb this extremely challenging, dangerous route, and to be able to have the mental focus to do it knowing that if you make a single mistake, you die.

[01:17:17](https://youtu.be/PplmzlgE0kg?t=4637) **LENNY**

It's insane. Yeah, that movie is out of control. And it's interesting how these relate in some way to the work you do.

[01:17:22](https://youtu.be/PplmzlgE0kg?t=4642) **CAT WU**

I actually am a rock climber. I first watched *Free Solo* before I climbed rocks, and I thought it was impressive — I didn't understand how impressive it was. It's one of the rare movies where the more you know about it, the more you're blown away by how insane this is. The kinds of moves he's doing on the wall are things that I don't think I will ever be able to do in my lifetime if it were set in a gym, like one foot off the ground.

[01:17:47](https://youtu.be/PplmzlgE0kg?t=4667) **LENNY**

With a rope.

[01:17:48](https://youtu.be/PplmzlgE0kg?t=4668) **CAT WU**

With a rope.

[01:17:50](https://youtu.be/PplmzlgE0kg?t=4670) **LENNY**

Did you see the documentary on that other guy, the younger one that went on like ice mountain?

[01:17:54](https://youtu.be/PplmzlgE0kg?t=4674) **CAT WU**

I did. That one was very sad.

[01:17:56](https://youtu.be/PplmzlgE0kg?t=4676) **LENNY**

But that was wild. Okay. Favorite product you recently discovered that you really love?

[01:17:59](https://youtu.be/PplmzlgE0kg?t=4679) **CAT WU**

The product that has most changed my life outside of Claude products is probably Waymo. I'm a diehard Waymo user. I use it twice a day, get to and from work. The two things that I really like about it are: one, I don't feel bad if a Waymo is waiting for me. So I feel less pressure to be right at the curbside the moment it arrives. The second thing is I feel like it lets me be a bit more productive. When I'm in the car with another human, I typically try not to do any work calls. I feel a little rude if I'm on my laptop the whole time. But one thing I really appreciate about the Waymo is I can call into a work call. I'm not worried about someone overhearing me, I'm not worried about, "Hey, is this rude? Am I talking too loud? Do I need to ask someone to change the music?" This has given me back like 30 minutes every day.

[01:18:55](https://youtu.be/PplmzlgE0kg?t=4735) **LENNY**

All these second-order effects of technology. It's so interesting.

[01:18:59](https://youtu.be/PplmzlgE0kg?t=4739) **CAT WU**

Yeah. I always thought Waymo needed to be priced lower than Uber and Lyft to succeed, but actually I'm very happy to pay a 2x premium for it.

[01:19:06](https://youtu.be/PplmzlgE0kg?t=4746) **LENNY**

I love Waymo. It's like, once you see it, you're just like, "Wow, this is insane." And then you get used to it. You get in there, you're like, "This is crazy." And then you forget about it.

[01:19:17](https://youtu.be/PplmzlgE0kg?t=4757) **CAT WU**

Totally. I think it's also changed the vernacular. A lot of people at Anthropic love Waymo, and I think in the past you would be like, "Hey, let's call blah blah ride share app." And now everyone's just like, "Okay, is the Waymo here?"

[01:19:30](https://youtu.be/PplmzlgE0kg?t=4770) **LENNY**

Okay, two more questions. Do you have a favorite life motto that you often come back to in work or in life?

[01:19:35](https://youtu.be/PplmzlgE0kg?t=4775) **CAT WU**

Just do things.

[01:19:37](https://youtu.be/PplmzlgE0kg?t=4777) **LENNY**

That's right.

[01:19:38](https://youtu.be/PplmzlgE0kg?t=4778) **CAT WU**

I think there's a lot of value in first-principles thinking. If you know what you're optimizing for and you have strong first principles, then you can normally deduce what the right course of action is and be able to clearly articulate that to all the stakeholders, and then you should just do it. I think jobs are fake. If you understand the constraints, you can figure out what you can do, and then just try to do it quickly, learn from the mistakes, and apologize or fix them if you did something wrong.

[01:20:08](https://youtu.be/PplmzlgE0kg?t=4808) **LENNY**

You could just do things — whoever said that.

[01:20:10](https://youtu.be/PplmzlgE0kg?t=4810) **CAT WU**

I think it's liberating actually to tell people this. In a lot of companies, roles are very strictly defined. Okay, this is what the PM does, this is what the designer does, this is what engineer does. Then even team scopes are very rigidly defined — "Hey, this corner of the codebase we touch, and this corner we're not allowed to touch." What "just do things" lets people do is they feel empowered to make these decisions, empowered to operate across team boundaries just to get something done.

[01:20:38](https://youtu.be/PplmzlgE0kg?t=4838) **LENNY**

That feels like a big important skill to be good at. People call it agency. Just do the things — bias towards action. All these ways of describing just like, you wait for permission.

[01:20:50](https://youtu.be/PplmzlgE0kg?t=4850) **CAT WU**

Yeah. I think this is my favorite reason to work at a startup at some point in your life. One thing that was very life-changing for me was actually working at Scale when we were 20 people. There was just no process and we had really big problems that we needed to solve. I really appreciate Alex and the rest of the team for empowering me and the rest of the team to just figure things out without any boundaries for what sales is supposed to do, what ops is supposed to do, what engineer is supposed to do. You just have all the tools at your disposal, you have some ambitious hairy problem statement, and you can do whatever you need to get to a good solution.

[01:21:28](https://youtu.be/PplmzlgE0kg?t=4888) **LENNY**

You almost need that experience to build that skill, to feel comfortable doing that, because a lot of people, you know, they go through school or in college and all these "do the thing we tell you to do and then you will get a good grade." And you have to unlearn that. Like, "Okay, I'm just going to do the thing that needs to be done, and even if people think it's dumb, I think it's the right thing to do."

[01:21:46](https://youtu.be/PplmzlgE0kg?t=4906) **CAT WU**

Yeah, exactly.

[01:21:47](https://youtu.be/PplmzlgE0kg?t=4907) **LENNY**

Okay, I actually have two more quick questions. Two more final questions. One is — when Claude thinks, there's all these, I don't know if you call them verbs. What's the term for these things?

[01:21:55](https://youtu.be/PplmzlgE0kg?t=4915) **CAT WU**

Thinking words.

[01:21:56](https://youtu.be/PplmzlgE0kg?t=4916) **LENNY**

Thinking words. And interestingly, these all leaked in the source code. Do you have a favorite thinking word?

[01:22:03](https://youtu.be/PplmzlgE0kg?t=4923) **CAT WU**

I really like "manifesting." It's also like the sticker that I have on my favorite.

[01:22:10](https://youtu.be/PplmzlgE0kg?t=4930) **LENNY**

Clearly the winner. Okay, final question. Asked Boris this too: with AGI potentially arriving in our lifetime, when you don't potentially have to work, what are you going to do? What are you going to do with all your time?

[01:22:23](https://youtu.be/PplmzlgE0kg?t=4943) **CAT WU**

I think it will take a long time for AGI to diffuse across society. So I think the immediate thing is actually just helping bring the world along. My non-serious answer for after this happens is I'll probably just do a lot of rock climbing. I'll probably live in some — I'll probably move to like Fontainebleau and just live amongst 10,000 boulders and climb for a bit. There's also so many books I want to read. My goal is to be able to read one or two books a week, and I'm currently at probably like 0.5. The backlog is pretty big. I think there's just so much we can learn from history, and so much that I don't understand as well as I would love to. I don't know anything about physics, or robotics, or any hardware, or aerospace — there's just so many interesting topics. I'm excited to learn even knowing that the AI will already know it.

[01:23:26](https://youtu.be/PplmzlgE0kg?t=5006) **LENNY**

Cat, this was amazing. You're awesome. Two follow questions. Where can folks find you online if they want to reach out and just follow what you're up to? And how can listeners be useful to you?

[01:23:35](https://youtu.be/PplmzlgE0kg?t=5015) **CAT WU**

The best way to reach out is, I am @catwu on Twitter. Feel free to tag me in things, feel free to DM me. I read all my DMs. I don't always respond to every single one, but I will read them all. The thing that is most helpful is, tell us where Claude Code and Co-work aren't working well for you. We are very grateful for the amount of positive feedback, but the things that we thrive on is edge cases, errors, specific tasks that we can reproduce where Claude Code or Co-work fail. If you're able to share that with us and we're able to reproduce it, then this is something that we're able to actively improve for our next generations of models and for our next harnesses.

[01:24:27](https://youtu.be/PplmzlgE0kg?t=5067) **LENNY**

Extremely cool. People on Twitter are not shy with sharing this feedback, so keep it coming.

[01:24:30](https://youtu.be/PplmzlgE0kg?t=5070) **CAT WU**

Share — please, please share the problems that you're having with us.

[01:24:34](https://youtu.be/PplmzlgE0kg?t=5074) **LENNY**

Yeah. And it's really cool to see your team being so active on Twitter and responding to people. So what I'm hearing is, this is actually stuff you guys actually see and react to.

[01:24:44](https://youtu.be/PplmzlgE0kg?t=5084) **CAT WU**

Yeah, we appreciate everyone being so engaged with us. It gives the team a ton of energy. We have this channel of "user love," and so whenever you guys share a success story, we post it there. And whenever you guys share issues with our product, we put it into our feedback channel. That way our broader team is able to act on it.

[01:25:42](https://youtu.be/PplmzlgE0kg?t=5102) **LENNY**

That is so cool to know. Thanks for sharing that. Well, Cat, thank you so much for being here.

[01:25:46](https://youtu.be/PplmzlgE0kg?t=5107) **CAT WU**

Thanks for having me.

[01:25:49](https://youtu.be/PplmzlgE0kg?t=5109) **LENNY**

Bye everyone. Thank you so much for listening. If you found this valuable, you can subscribe to the show on Apple Podcasts, Spotify, or your favorite podcast app. Also, please consider giving us a rating or leaving a review, as that really helps other listeners find the podcast. You can find all past episodes or learn more about the show at lennyspodcast.com.
