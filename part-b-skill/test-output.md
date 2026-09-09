# Week 2 · Build Start · T-II Agents, Skills & Context

**What this is:** Student handout for week 2 of AILT9019 AI Literacy II — a lab on agent anatomy (context / skills / MCP), Pi Agent, plus the project-proposal brief due in week 4.
**Length:** 6 pages | **Read at:** full text extracted

## Bottom line
An AI agent is the same LLM as a chat window plus three things you supply: context, skills, and MCP tools. This week you assemble all three locally, shortlist 2–3 project directions, build one small working prototype, and push it to GitHub — because the proposal draft is due Fri 25 Sep and a small finished thing beats a big broken plan.

## Key points
- A plain chat and an agent differ only in what you hand the model: your instructions as context, your skills to follow, and tools to call — p.2
- Five tasks this week: tutorial (~90 min), read proposal requirements (~40 min), shortlist directions (~30 min), build a prototype (~2 h), push to GitHub (~15 min) — p.1
- Part B is a `SKILL.md` in a folder; acceptance is that the tool reproduces your specified format unprompted — p.2
- Part C is registering a small MCP server and proving you can point at output that came from the tool, not the model — p.3
- Part D installs Pi Agent globally and copies your Part B skill into `.pi/skills/` — p.3
- The proposal is one submission per team, due Fri 25 Sep (week 4), and must contain no names, UIDs, or emails — p.3
- Six required proposal sections: Background, Project pipeline, Evaluation and test, Distribution and accessibility, Ethics and risks, Checkpoints — p.4
- Every proposal needs an explicit "does not" that a peer reviewer can quote in one or two lines — p.4

## Section digest

| Section / pages | What it says | Why it matters |
|---|---|---|
| This week's goal + task table — p.1 | Learn agent anatomy, pick a direction, build and push a small local prototype | Sets the week's scope and time budget |
| The mental model / Figure 1 — p.2 | Context = what the LLM reads; skills = reusable instructions; MCP = external calls | The vocabulary the whole rest of the course uses |
| Part A · Context engineering — p.2 | Change only the session instruction, repeat the same task, explain the difference | Acceptance: you can predict how an instruction change changes the answer |
| Part B · Your first skill — p.2 | Create `my-skill/SKILL.md` with purpose, when-to-use, one concrete step | Produces your first reusable instruction file |
| Part C · A tiny MCP tool — p.3 | Register a small MCP server (e.g. date), force a tool call | Acceptance: output demonstrably from the tool, not the model |
| Part D · Run Pi Agent — p.3 | `npm install -g @earendil-works/pi-coding-agent`, configure a provider, reuse your skill | Proves the skill is portable across agents |
| Part E · Push to GitHub — p.3 | Push, then clone into a second folder and verify | Acceptance: a fresh clone contains everything |
| Proposal requirements — p.4 | Six sections, each with a stated requirement; pipeline and timeline figures encouraged | The actual marking criteria for weeks 3–4 |
| Sample proposals — p.5 | Campus navigator, course policy explainer, sustainable dining helper | Shows "good": named user, small task, public data, clear "does not" |
| Topic idea list — p.5–6 | Six ideas banded Easy / Medium / Challenging, each with a user group, task, and "does not" | Your shortlist source; the bands warn that a finished Easy beats an unfinished Challenging |
| How to choose + self-check — p.6 | Name the user group and task in one sentence, name the dataset and its permission in one line, avoid the crowd | The four checkboxes a proposal must pass |

## Action items
- Finish the T-II tutorial (context, skills, MCP, Pi Agent) — owner: student (individual) — due: this week, Sep 7–13
- Shortlist 2–3 project directions with user group, task, and dataset — owner: student/team — due: before Week 3
- Build a tiny local prototype and push it to GitHub — owner: student — due: this week, Sep 7–13
- Submit the project proposal via the Moodle form — owner: team (one submission) — due: Fri 25 Sep

## Open questions
- Part D says "configure a model provider" — p.3 — but the handout never names which provider or whether the department supplies an API key.
- "Distribution and accessibility" asks whether the work can sit in more than one agent environment "if that is in scope" — p.4 — so it is unclear whether a second environment is required or optional.
- The proposal must be submitted via "the Moodle form" — p.3 — but no link is given in this document.

## What I did not read
Nothing — full text extracted (12,557 chars, 6 pages, 0 pages without a text layer).
