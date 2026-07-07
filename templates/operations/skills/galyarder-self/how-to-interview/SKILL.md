---
description: Use when preparing for coding interviews, mock screen diagnostics, recruiter
  negotiations, or offer tactics.
metadata:
  hermes:
    category: galyarder-self
name: how-to-interview
---


# How To Pass Any Coding Interview

## The Truth

Interview is NOT a skill test. Interview is a **2-person improv theater** where:
- You = actor playing the role of "the best candidate"
- Interviewer = audience who wants to believe you're the one

LeetCode is just the ticket to enter. What determines pass/fail:
- How you make the interviewer FEEL during the session
- Whether they want to work with you every day
- Whether you make them look good to their team

## 4-Round Standard Loop

| Round | Time | What They Really Test | Format |
|-------|------|-----------------------|--------|
| 1. Resume Deep Dive | 30-45 min | "Is this person real or full of shit?" | Walk through 2-3 projects |
| 2. Technical Screen | 45-60 min | "Can they actually code?" | 1-2 LC Easy/Medium |
| 3. Behavioral | 30-45 min | "Do I want to work with this person?" | STAR format questions |
| 4. System Design | 45-60 min | "Can they think like an architect?" | Open-ended design |

## Question Taxonomy (Every Question Falls Into One)

### Type 1: Icebreaker
**Trigger:** "Walk me through your resume", "Tell me about yourself"
**Approach:** Quick win. 2 minutes. Show you can communicate like a human.
**Structure:**
1. Current role + company (1 sentence)
2. One recent project relevant to the role (1-2 sentences)
3. Why you're here (1 sentence)

**Example:**
"I'm currently a software engineer at X, building real-time data pipelines. Most recently I built an event-driven system that handles 50k events/sec. I'm here because this role's focus on distributed systems aligns with where I want to grow."

### Type 2: Domain Knowledge
**Trigger:** "Explain how X works", "What's the difference between X and Y"
**Approach:** Depth + breadth. Use analogies. Diagrams. You're a consultant, not a textbook.

### Type 3: Technical (Coding)
**Trigger:** "Given an array...", "Design a function that..."
**Approach:** 4-stage protocol (below). This is where 90% of preparation goes.

### Type 4: Behavioral
**Trigger:** "Tell me about a time when...", "Describe a situation where..."
**Approach:** STAR format. Story bank (5-7 stories covers 95% of questions).

### Type 5: System Design
**Trigger:** "Design a URL shortener", "How would you build..."
**Approach:** Structured framework (below). Requirements → High-level → Deep dive → Trade-offs.

## Coding Problem: 4-Stage Response Protocol

### Stage 1: Problem Comprehension (2-3 min)
```
"What I'm hearing is: [restate problem in own words]. 
 The input is [X], and I need to return [Y].
 Edge cases: [empty input, single element, duplicates, negatives, overflow].
 Constraints: [size limits, time/space requirements]."
```

**Key:** Don't touch the keyboard until you've confirmed understanding with the interviewer.

### Stage 2: Solution Design (3-5 min)
```
"Brute force would be [X] with O(Y) time/space.
 I think we can optimize by [Z] approach.
 The key insight is [W].
 This brings us to O(V) time and O(U) space."
```

**Always ask:** "Does this approach make sense before I code it?"

### Stage 3: Implementation (10-15 min)
- Think out loud while coding
- Use meaningful variable names (not `i, j, k` for everything)
- If stuck, verbalize what you're stuck on
- Don't go silent — silence = panic signal to interviewer

### Stage 4: Verification (2-3 min)
- Walk through with a concrete example
- Check edge cases
- State time/space complexity

## Technical Knowledge: Structured Approach

**For "How does X work" questions:**

1. **One-liner definition** — what it is in 1 sentence
2. **Why it exists** — what problem it solves
3. **How it works** — the mechanism (analogies help)
4. **Trade-offs** — pros/cons vs alternatives
5. **Real-world use** — when you'd use it, when you wouldn't

**Example: "How does garbage collection work?"**

> "GC automatically reclaims memory that's no longer referenced. It exists because manual memory management (C/C++) leads to leaks and dangling pointers. The two main approaches are reference counting (Python, Swift) and tracing (Java, Go — mark-and-sweep). Reference counting can't handle cycles. Tracing has pause-time issues but handles cycles. Modern collectors like G1 and ZGC use region-based concurrent collection to minimize pauses. In practice, you'd choose GC'd languages when developer velocity matters more than microsecond latency control."

## System Design: Framework

### Step 1: Requirements Clarification (3-5 min)
```
Functional: What does the system DO?
- Users can [X]
- System supports [Y]
- Scale: [Z] users, [W] requests/sec

Non-functional: What qualities matter?
- Latency: <200ms p99
- Availability: 99.9%
- Consistency: eventual vs strong
```

### Step 2: High-Level Design (10 min)
```
Client → Load Balancer → API Gateway → [Services] → Database
                                                    → Cache
                                                    → Queue
```
Draw the boxes. Label them. Show data flow arrows.

### Step 3: Deep Dive (15-20 min)
Pick the most interesting/hardest component and go deep:
- Database schema
- API design
- Scaling strategy
- Failure handling

### Step 4: Trade-offs & Bottlenecks (5-10 min)
```
"We chose [X] because [reason], but the trade-off is [Y].
 At scale, the bottleneck would be [Z]. We could mitigate by [W]."
```

## Self-Awareness Practice

### The 5 Essential Questions (Write answers before any interview)

**1. "What's your greatest strength?"**
→ Pick ONE. Back with a specific example. Not a list.

**2. "What's your weakness?"**
→ Real weakness + what you're doing about it. Not "I work too hard."

**3. "Tell me about a failure."**
→ STAR format. Focus on what you LEARNED, not the failure itself.

**4. "Why this company?"**
→ Specific. Reference their product, mission, recent news, tech stack.

**5. "Where do you see yourself in 5 years?"**
→ Show ambition + alignment with the role. Don't say "your chair."

### Story Bank (Prepare 5-7 stories covering these)

| Story Theme | Covers |
|---|---|
| Conflict resolution | "Tell me about a disagreement with a teammate" |
| Leadership/initiative | "Describe a time you led something" |
| Failure/learning | "Tell me about a mistake" |
| Tight deadline | "How did you handle pressure?" |
| Cross-team collaboration | "Working with other teams" |
| Technical challenge | "Hardest bug/problem you solved" |
| Mentoring/helping | "Helping a teammate grow" |

Each story should cover multiple themes through different angles.

## Mock Interview Protocol

### Solo Mock (Daily, 45 min)
1. Pick 1 LC Medium (blind — no preview)
2. Set timer: 45 min
3. Record yourself (screen + voice) — `obs-studio` or `asciinema`
4. Talk out loud the entire time
5. Review recording after. Note:
   - How long were you silent?
   - Did you explain your thought process?
   - Did you check edge cases?
   - How many "um"s and "uh"s?

### Partner Mock (Weekly if possible)
- Use pramp.com, interviewing.io, or a friend
- Real human feedback > solo practice

### Mock System Design (2x/week)
1. Pick a topic: URL shortener, Twitter feed, chat system, rate limiter
2. 45 min timer
3. Draw on whiteboard/paper while talking
4. Review: did you cover requirements? Did you deep dive? Trade-offs?

## Pre-Interview Ritual (24h Before)

### Day Before
- [ ] Review company: product, tech stack, recent news, Glassdoor interview reviews
- [ ] Review your resume line by line — be ready to deep dive any bullet
- [ ] Prepare 3 questions to ask THEM (not generic — specific to team/product)
- [ ] Lay out clothes, charge devices, test camera/mic if remote
- [ ] Light review only — NO new material. Trust your prep.
- [ ] Sleep 7-8 hours. Non-negotiable.

### Morning Of
- [ ] Wake up 2h before interview
- [ ] Exercise (even 15 min walk) — burns cortisol
- [ ] Eat protein-heavy breakfast
- [ ] Warm up: 1 easy LC problem (confidence boost, not learning)
- [ ] Review your 3 questions for them
- [ ] Arrive/log in 10 min early

### During Interview
- **First 2 minutes:** Smile, firm handshake (or confident virtual greeting), energy UP
- **When you don't know:** "That's a great question. I haven't worked with X directly, but here's how I'd approach it..."
- **When you're stuck:** "Let me think about this for a moment... [30 sec pause is OK]. I'm considering approach A and B..."
- **Energy management:** If it's a long loop (4-5 rounds), eat snacks between rounds. Hydrate.

## Post-Interview Ritual

### Immediately After (within 1 hour)
- [ ] Write down EVERY question you were asked (exact wording if possible)
- [ ] Write down your answers — how would you improve them?
- [ ] Note any areas where you struggled
- [ ] Rate yourself: what went well, what didn't

### Within 24 Hours
- [ ] Send thank-you email to recruiter (not interviewer unless specifically asked)
- [ ] Note any follow-up items promised
- [ ] Update your preparation notes

### If You Don't Get the Offer
- [ ] Ask for feedback (politely — many won't give it but some will)
- [ ] Analyze which round you failed
- [ ] Target that weakness in next prep cycle
- [ ] **Move on. One rejection is one data point, not a verdict.**

## Offer Strategy

### When You Get an Offer
1. **Never accept immediately.** "Thank you so much. I'm very excited. When do you need a decision by?"
2. **Get everything in writing** before negotiating.
3. **Negotiate.** Always. Even if the offer is great. The worst they say is "this is our best."

### Negotiation Levers
- Base salary (least flexible)
- Signing bonus (more flexible)
- Equity/RSUs (most flexible)
- Start date
- Remote/hybrid arrangement
- Title
- PTO/vacation

### Multiple Offers = Maximum Leverage
- Be transparent: "I'm in final stages with another company"
- Don't lie about offers — it gets checked
- Use offers to accelerate timelines, not to bluff

## The Recruiter Rule

> "If the recruiter says you should practice LeetCode because the interview will be hard, you should practice LeetCode."

They're telling you the truth. Listen. Don't dismiss. Don't rationalize. Don't say "I'm different." They've seen hundreds of candidates. They know the pass rates. **Humble yourself and do the work.**

## The Commitment Statement

"I will do whatever it takes to pass the interview."

This means:
- Practice even when it's boring
- Record yourself even when it's cringe
- Ask for feedback even when it's uncomfortable
- Study fundamentals even when you think you know them
- Do mocks even when you'd rather LeetCode alone

**There is no hack. There is no shortcut. There is only preparation + execution + feedback loop.**

## Quick Reference: Pre-Interview Checklist

```
□ Company research done (product, tech, news, culture)
□ Resume stories prepared (STAR format for each bullet)
□ 5-7 story bank covers all behavioral themes
□ 3 specific questions to ask them
□ Warm-up problem done (1 easy LC)
□ Clothes ready, tech tested
□ 7-8 hours sleep
□ Ate breakfast, hydrated
□ Arrived/logged in 10 min early
□ Energy: HIGH. Confidence: BUILT. Ego: CHECKED.
```

## Asuka's Final Line

> "Practice this like you already failed the last one. Because confidence without preparation is just arrogance with a deadline."
