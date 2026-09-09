# Figure 1 — anatomy of an AI agent (labelled from memory)

Week 2 goal: *"Explain what context, skills and MCP tools are — you can label Figure 1
without looking."*

```
        PLAIN CHAT                          AGENT
   ┌────────────────────┐        ┌──────────────────────────────┐
   │                    │        │                              │
   │   Language model   │        │       Language model         │
   │   (frozen weights) │        │   ← identical, NOT the diff  │
   │         │          │        │              │               │
   │         ▼          │        │              ▼               │
   │  Your typed msg    │        │   ┌────────────────────────┐ │
   │         │          │        │   │ CONTEXT                │ │
   │         ▼          │        │   │ what the model reads   │ │
   │   An answer        │  add   │   ├────────────────────────┤ │
   │   (guesses what    │ ┈┈┈┈►  │   │ SKILLS                 │ │
   │    you meant)      │  these │   │ instructions you write │ │
   │                    │  three │   ├────────────────────────┤ │
   │                    │        │   │ MCP TOOLS              │ │ ──► external
   │                    │        │   │ calls it may make      │ │      calls
   └────────────────────┘        └──────────────────────────────┘
```

## The three labels, in one sentence each

| Label | What it is | What I built this week that is one |
|---|---|---|
| **Context** | Everything the model reads before it answers: your session instruction, files, tool results. It is the spec the model resolves ambiguity against. | `instruction-v1.md` vs `instruction-v2.md` in this folder — same task, different context, different output. |
| **Skills** | Reusable instructions *you* write, in a `SKILL.md`, that the tool loads when the task matches. Progressive disclosure: only the description sits in context until it is needed. | `part-b-skill/my-skill/SKILL.md` — the `pdf-summarizer`. |
| **MCP tools** | External calls the model may make, over a standard protocol (JSON-RPC over stdio). How a model reaches facts it cannot hold in its weights. | `part-c-mcp/server.py` — `today`, `current_time`, `days_until`. |

## The one-line version
A plain chat and an agent use the same model; the agent is the same model **given your
instructions as context, your skills to follow, and tools to call** — and that right-hand
half is entirely supplied by you, which is why it is portable: the same `SKILL.md` ran in
WorkBuddy and loaded into Pi with zero edits.
