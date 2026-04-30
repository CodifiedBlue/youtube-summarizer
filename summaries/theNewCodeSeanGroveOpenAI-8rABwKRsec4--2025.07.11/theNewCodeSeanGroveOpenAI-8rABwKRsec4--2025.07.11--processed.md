# The New Code — Sean Grove, OpenAI

- **Channel:** AI Engineer
- **Uploaded:** 2025-07-11
- **URL:** https://youtu.be/8rABwKRsec4

---

[00:25](https://youtu.be/8rABwKRsec4?t=25) **SEAN GROVE**

Hello everyone, thank you very much for having me. It's a very exciting place to be, very exciting time to be. I mean, this has been like a pretty intense couple of days. I don't know if you feel the same way, but also very energizing. So I want to take a little bit of your time today to talk about what I see as the coming of the new code — in particular, specifications, which sort of hold this promise that has been the dream of the industry, where you can write your code, your intentions, once and run them everywhere. Quick intro: my name is Sean, I work at OpenAI, specifically in alignment research, and today I want to talk about the value of code versus communication, and why specifications might be a little bit of a better approach in general.

[01:18](https://youtu.be/8rABwKRsec4?t=78) **SEAN GROVE**

I'm going to go over the anatomy of a specification, and we'll use the model spec as the example. We'll talk about communicating intent to other humans, and we'll go over the 4o sycophancy issue as a case study. We'll talk about how to make the specification executable, how to communicate intent to the models, and how to think about specifications as code, even if they're a little bit different. And we'll end on a couple of open questions. So, let's talk about code versus communication.

[01:51](https://youtu.be/8rABwKRsec4?t=111) **SEAN GROVE**

Real quick, raise your hand if you write code — and vibe code counts. Cool. Keep them up if your job is to write code. Okay. Now, for those people, keep their hand up if you feel that the most valuable professional artifact that you produce is code. Okay, there's quite a few people, and I think this is quite natural. We all work very, very hard to solve problems. We talk with people. We gather requirements. We think through implementation details. We integrate with lots of different sources. And the ultimate thing that we produce is code. Code is the artifact that we can point to, we can measure, we can debate, and we can discuss. It feels tangible and real, but it's sort of underselling the job that each of you does. Code is sort of 10 to 20% of the value that you bring. The other 80 to 90% is in structured communication.

[02:53](https://youtu.be/8rABwKRsec4?t=173) **SEAN GROVE**

And this is going to be different for everyone, but a process typically looks something like: you talk to users in order to understand their challenges. You distill these stories down and then ideate about how to solve these problems. What is the goal that you want to achieve? You plan ways to achieve those goals. You share those plans with your colleagues. You translate those plans into code — so this is a very important step, obviously. And then you test and verify — not the code itself, right? No one cares actually about the code itself. What you care about is, when the code ran, did it achieve the goals? Did it alleviate the challenges of your user? You look at the effects that your code had on the world. So talking, understanding, distilling, ideating, planning, sharing, translating, testing, verifying — these all sound like structured communication to me.

[03:57](https://youtu.be/8rABwKRsec4?t=237) **SEAN GROVE**

And structured communication is the bottleneck. Knowing what to build, talking to people and gathering requirements, knowing how to build it, knowing why to build it, and at the end of the day, knowing if it has been built correctly and has actually achieved the intentions that you set out with. And the more advanced AI models get, the more we are all going to starkly feel this bottleneck. Because in the near future, the person who communicates most effectively is the most valuable programmer. And literally, if you can communicate effectively, you can program.

[04:39](https://youtu.be/8rABwKRsec4?t=279) **SEAN GROVE**

So, let's take vibe coding as an illustrative example. Vibe coding tends to feel quite good, and it's worth asking why is that? Well, vibe coding is fundamentally about communication first, and the code is actually a secondary downstream artifact of that communication. We get to describe our intentions and the outcomes that we want to see, and we let the model actually handle the grunt work for us. And even so, there is something strange about the way that we do vibe coding. We communicate via prompts to the model, and we tell them our intentions and our values, and we get a code artifact out at the end, and then we sort of throw our prompts away — they're ephemeral. And if you've written TypeScript or Rust, once you put your code through a compiler or it gets down into a binary, no one is happy with that binary. That wasn't the purpose. It's useful. In fact, we always regenerate the binaries from scratch every time we compile or we run our code through V8 or whatever it might be from the source spec. It's the source specification that's the valuable artifact.

[05:52](https://youtu.be/8rABwKRsec4?t=352) **SEAN GROVE**

And yet when we prompt LLMs, we sort of do the opposite. We keep the generated code and we delete the prompt. And this feels a little bit like you shred the source and then you very carefully version control the binary. And that's why it's so important to actually capture the intent and the values in a specification. A written specification is what enables you to align humans on the shared set of goals and to know if you are aligned, if you actually synchronize on what needs to be done. This is the artifact that you discuss, that you debate, that you refer to, and that you synchronize on. And this is really important. So I want to nail this home: a written specification effectively aligns humans, and it is the artifact that you use to communicate and to discuss and debate and refer to and synchronize on. If you don't have a specification, you just have a vague idea.

[06:50](https://youtu.be/8rABwKRsec4?t=410) **SEAN GROVE**

Now let's talk about why specifications are more powerful in general than code. Because code itself is actually a lossy projection from the specification. In the same way that if you were to take a compiled C binary and decompile it, you wouldn't get nice comments and well-named variables. You would have to work backwards. You'd have to infer: what was this person trying to do? Why is this code written this way? It isn't actually contained in there. It was a lossy translation. And in the same way, code itself, even nice code, typically doesn't embody all of the intentions and the values in itself. You have to infer what is the ultimate goal that this team is trying to achieve when you read through code. So communication, the work that we already do, when embodied inside of a written specification, is better than code. It actually encodes all of the necessary requirements in order to generate the code. And in the same way that having source code that you pass to a compiler allows you to target multiple different architectures — you can compile for ARM64, x86, or WebAssembly — the source document actually contains enough information to describe how to translate it to your target architecture.

[08:11](https://youtu.be/8rABwKRsec4?t=491) **SEAN GROVE**

In the same way, a sufficiently robust specification given to models will produce good TypeScript, good Rust, servers, clients, documentation, tutorials, blog posts, and even podcasts. Show of hands, who works at a company that has developers as customers? Okay. So a quick thought exercise is: if you were to take your entire codebase, all of the documentation, all of the code that runs your business, and you were to put that into a podcast generator, could you generate something that would be sufficiently interesting and compelling that would tell the users how to succeed, how to achieve their goals? Or is all of that information somewhere else? It's not actually in your code.

[09:01](https://youtu.be/8rABwKRsec4?t=541) **SEAN GROVE**

And so moving forward, the new scarce skill is writing specifications that fully capture the intent and values. And whoever masters that, again, becomes the most valuable programmer. And there's a reasonable chance that this is going to be the coders of today. This is already very similar to what we do. However, product managers also write specifications. Lawmakers write legal specifications. This is actually a universal principle.

[09:32](https://youtu.be/8rABwKRsec4?t=572) **SEAN GROVE**

So with that in mind, let's look at what a specification actually looks like. And I'm going to use the OpenAI model spec as an example here. So last year, OpenAI released the model spec. And this is a living document that tries to clearly and unambiguously express the intentions and values that OpenAI hopes to imbue its models with that it ships to the world. And it was updated in February and open sourced. So you can actually go to GitHub and you can see the implementation of the model spec, and surprise, surprise — it's actually just a collection of markdown files. Just looks like this. Now, markdown is remarkable. It is human readable. It's versioned. It's change-logged. And because it is natural language, everyone — not just technical people — can contribute, including product, legal, safety research, policy. They can all read, discuss, debate, and contribute to the same source code. This is the universal artifact that aligns all of the humans as to our intentions and values inside of the company.

[10:44](https://youtu.be/8rABwKRsec4?t=644) **SEAN GROVE**

Now, as much as we might try to use unambiguous language, there are times where it's very difficult to express the nuance. So every clause in the model spec has an ID here. So you can see sy73 here. And using that ID, you can find another file in the repository, sy73.md, that contains one or more challenging prompts for this exact clause. So the document itself actually encodes success criteria — that the model under test has to be able to answer this in a way that actually adheres to that clause.

[11:27](https://youtu.be/8rABwKRsec4?t=687) **SEAN GROVE**

So let's talk about sycophancy. Recently there was an update to 4o — I don't know if you've heard of this — that caused extreme sycophancy. And we can ask, like, what value is the model spec in this scenario? The model spec serves to align humans around a set of values and intentions. Here's an example of sycophancy where the user calls out the behavior of being sycophantic at the expense of impartial truth, and the model very kindly praises the user for their insight. There have been other esteemed researchers who have found similarly concerning examples. And this hurts. Shipping sycophancy in this manner erodes trust. It hurts.

[12:31](https://youtu.be/8rABwKRsec4?t=751) **SEAN GROVE**

So it also raises a lot of questions, like: was this intentional? You could see some way where you might interpret it that way. Was it accidental, and why wasn't it caught? Luckily, the model spec actually includes a section dedicated to this, since its release, that says, "Don't be sycophantic," and it explains that while sycophancy might feel good in the short term, it's bad for everyone in the long term. So we actually expressed our intentions and our values, and were able to communicate it to others through this. So people could reference it. And if we have it in the model spec specification — if the model specification is our agreed-upon set of intentions and values — and the behavior doesn't align with that, then this must be a bug. So we rolled back, we published some studies and some blog posts, and we fixed it.

[13:34](https://youtu.be/8rABwKRsec4?t=814) **SEAN GROVE**

But in the interim, the spec served as a trust anchor — a way to communicate to people what is expected and what is not expected. So if just the only thing the model specification did was to align humans along those shared sets of intentions and values, it would already be incredibly useful.

[13:56](https://youtu.be/8rABwKRsec4?t=836) **SEAN GROVE**

But ideally we can also align our models, and the artifacts that our models produce, against that same specification. So there's a technique, a paper that we released, called deliberative alignment that sort of talks about this — how to automatically align a model. And the technique is such where you take your specification and a set of very challenging input prompts, and you sample from the model under test or training. You then take its response, the original prompt, and the policy, and you give that to a grader model, and you ask it to score the response according to the specification: how aligned is it? So the document actually becomes both training material and eval material. And based off of this score, we reinforce those weights. And it goes from — you know, you could include your specification in the context, in maybe a system message or developer message, every single time you sample, and that is actually quite useful. A prompted model is going to be somewhat aligned, but it does detract from the compute available to solve the problem that you're trying to solve with the model. And keep in mind, these specifications can be anything. They could be code style, or testing requirements, or safety requirements. All of that can be embedded into the model. So through this technique, you're actually moving it from inference-time compute, and you're pushing it down into the weights of the model, so that the model actually feels your policy and is able to sort of muscle-memory-style apply it to the problem at hand.

[15:29](https://youtu.be/8rABwKRsec4?t=929) **SEAN GROVE**

And even though we saw that the model spec is just markdown, it's quite useful to think of it as code. It's quite analogous. These specifications, they compose, they're executable as we've seen, they are testable, they have interfaces where they touch the real world, they can be shipped as modules. And whenever you're working on a model spec, there are a lot of similar problem domains. So just like in programming where you have a type checker — the type checker is meant to ensure consistency, where if interface A has a dependent module B, they have to be consistent in their understanding of one another. So if department A writes a spec and department B writes a spec, and there is a conflict in there, you want to be able to pull that forward and maybe block the publication of the specification. As we saw, the policy can actually embody its own unit tests. And you can imagine sort of various linters, where if you're using overly ambiguous language, you're going to confuse humans and you're going to confuse the model, and the artifacts that you get from that are going to be less satisfactory. So specs actually give us a very similar tool chain, but it's targeted at intentions rather than syntax.

[16:42](https://youtu.be/8rABwKRsec4?t=1002) **SEAN GROVE**

So let's talk about lawmakers as programmers. The US Constitution is literally a national model specification. It has written text which is, aspirationally at least, clear and unambiguous policy that we can all refer to. And it doesn't mean that we agree with it, but we can refer to it as the current status quo, as the reality. There is a versioned way to make amendments — to bump and to publish updates to it. There is judicial review, where a grader is effectively grading a situation and seeing how well it aligns with the policy. And even though the source policy is meant to be unambiguous, sometimes the world is messy, and maybe you miss part of the distribution and a case falls through. And in that case, there is a lot of compute spent in judicial review, where you're trying to understand how the law actually applies here. And once that's decided, it sets a precedent, and that precedent is effectively an input-output pair that serves as a unit test that disambiguates and reinforces the original policy spec. It has things like a chain of command embedded in it, and the enforcement of this over time is a training loop that helps align all of us towards a shared set of intentions and values. So this is one artifact that communicates intent, it adjudicates compliance, and it has a way of evolving safely.

[18:17](https://youtu.be/8rABwKRsec4?t=1097) **SEAN GROVE**

So it's quite possible that lawmakers will be programmers, or inversely, that programmers will be lawmakers in the future. And actually, this is a very universal concept. Programmers are in the business of aligning silicon via code specifications. Product managers align teams via product specifications. Lawmakers literally align humans via legal specifications. And everyone in this room — whenever you are doing a prompt, it's a sort of proto-specification. You are in the business of aligning AI models towards a common set of intentions and values. And whether you realize it or not, you are spec authors in this world.

[19:01](https://youtu.be/8rABwKRsec4?t=1141) **SEAN GROVE**

And specs let you ship faster and safer. Everyone can contribute, and whoever writes the spec — be it a PM, a lawmaker, an engineer, a marketer — is now the programmer. And software engineering has never been about code. Going back to our original question, a lot of you put your hands down when you thought, well, actually, the thing I produced is not code.

[19:28](https://youtu.be/8rABwKRsec4?t=1168) **SEAN GROVE**

Engineering has never been about this. Coding is an incredible skill and a wonderful asset, but it is not the end goal. Engineering is the precise exploration by humans of software solutions to human problems. It's always been this way. We're just moving away from sort of the disparate machine encodings to a unified human encoding of how we actually solve these problems. I want to thank Josh for this credit.

[19:54](https://youtu.be/8rABwKRsec4?t=1194) **SEAN GROVE**

So I want to ask you, put this in action. Whenever you're working on your next AI feature, start with a specification. What do you actually expect to happen? What does success criteria look like? Debate whether or not it's actually clearly written down and communicated. Make the spec executable. Feed the spec to the model and test against the model, or test against the spec.

[20:27](https://youtu.be/8rABwKRsec4?t=1227) **SEAN GROVE**

And there's an interesting question in this world, given that there's so many parallels between programming and spec authorship. I wonder, what does the IDE look like in the future — you know, an integrated development environment? And I'd like to think it's something like an integrated thought clarifier, where whenever you're writing your specification, it sort of pulls out the ambiguity and asks you to clarify it, and it really clarifies your thought, so that you and all human beings can communicate your intent to each other much more effectively, and to the models.

[20:55](https://youtu.be/8rABwKRsec4?t=1255) **SEAN GROVE**

And I have a closing request for help, which is: what is both amenable and in desperate need of specification? This is aligning agents at scale. I love this line of, like, "you then realize that you never told it what you wanted, and maybe you never fully understood it anyway." This is a cry for specification. We have a new agent robustness team that we've started up, so please join us and help us deliver safe AGI for the benefit of all humanity. And thank you. I'm happy to chat.
