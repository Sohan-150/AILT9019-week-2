# Topic shortlist (2–3 directions) — done before Week 3

Method: for each idea, one sentence naming the single user group and single task, then
one line naming the dataset (source + permission).

---

## 1. Bin-finder · recycling rules helper — **PREFERRED** (from idea #2, Easy)

**User group + task:** Hall residents who need to know which bin a specific item goes in
under published campus recycling rules.

**Dataset:** Self-curated item→bin rule table (JSON), to be derived line-by-line from the
published campus recycling guide (public webpage/PDF) before Week 4. Seed version for the
prototype is self-curated placeholder data — permission: self-curated.

**Explicit "does not":** Does not handle hazardous-waste disposal, does not override
building staff instructions, and **does not invent a rule** — if an item is not in the
published source it says so and hands off to staff.

**Why this one:** the refusal case is the whole product, not a bolt-on. "Which bin does an
unknown item go in" is exactly the failure mode the course wants us to design for, and the
Easy band means it can actually be finished and evaluated this semester.

**Risk to resolve:** I must swap the seed data for the real published guide, or the
proposal's dataset line is weak.

---

## 2. Course policy explainer (from the sample proposals, Medium)

**User group + task:** Students reading a fixed set of public course policy documents who
need a plain-language answer to "what does this policy actually say about X", with a
paragraph citation.

**Dataset:** The public course policy / handbook PDF set (public, published by the
university). Permission: public documents.

**Explicit "does not":** Does not interpret personal cases, does not make appeal decisions,
does not answer when the policy set has no relevant paragraph.

**Why it is second choice:** it is printed in the handout as a *sample* of what good looks
like, so a meaningful share of the cohort will build it — the handout explicitly warns
against this ("a third of the cohort building the same project helps nobody").

---

## 3. Budget-policy Q&A (idea #3, Medium) — **REJECTED**

Society officers looking up a spending rule in public budget/policy PDFs.

Rejected because it is the worked example inside the proposal template itself (blue text),
so it is almost certainly the most crowded choice in the cohort. The underlying technique
— retrieval + citation over a fixed PDF set — is good; the topic is the problem, not the
method.

---

## Decision
Proceed with **#1 Bin-finder**. Easy band, distinct enough to avoid the crowd, and its
"does not" is testable rather than decorative. The prototype this week is a single page
that answers one question: *which bin does this item go in?*
