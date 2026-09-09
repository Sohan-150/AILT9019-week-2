# Part D · Run Pi Agent — status

## Done

**1. Installed.**
```
npm install -g @earendil-works/pi-coding-agent
```
→ `added 131 packages`. Binary resolves at
`C:\Users\sohan\.workbuddy-ai\binaries\node\versions\22.22.2-2\pi`, and
`pi --version` reports **0.85.1**. `pi --help` lists read / bash / edit / write tools.

**2. Skill copied into `.pi/skills/`** — this is the portability test, and it passed
structurally: the identical `SKILL.md` from Part B now lives in two Pi locations and
needed **zero edits** to move.

| Location | Scope |
|---|---|
| `part-d-pi/practice/.pi/skills/pdf-summarizer/SKILL.md` | project (loads after the project is trusted) |
| `~/.pi/agent/skills/pdf-summarizer/SKILL.md` | global (loads everywhere) |

Per Pi's docs, a directory containing `SKILL.md` is discovered recursively, and the
frontmatter needs a non-empty `description` — mine has one, so it is spec-valid.

**3. Practice folder ready:** `part-d-pi/practice/`.

## Blocked — needs your API key

`pi auth check` returns `not_ready` for google, anthropic, and openai; no
`*_API_KEY` is set in the environment and `~/.pi/agent/auth.json` is `{}`. Running pi in
the practice folder gives:

```
No API key found for the selected model.
Use /login to log into a provider via OAuth or API key.
```

So steps 2–4 of Part D (configure a provider, have pi write + run a script, run the
skill inside a pi session) cannot complete until a provider is configured. **I can't do
that for you — the key is yours.**

## Runbook to finish Part D (about 5 minutes)

```bash
# pick ONE provider and set its key (default provider is google)
export GEMINI_API_KEY=...      # or ANTHROPIC_API_KEY / OPENAI_API_KEY

cd "part-d-pi/practice"
pi --approve                   # trust the project so .pi/skills/ loads
```

Then inside pi:
1. `/skill:pdf-summarizer` — confirm it loads the Part B skill.
2. *"Write a script that counts words in a file, run it, and explain what you changed."*
3. Confirm the run and its explanation both appear.

Or use the OAuth flow: start `pi` and run `/login`.

**Acceptance still outstanding:** pi running a session that follows the skill. Everything
up to the model call is verified.
