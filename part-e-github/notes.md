# Part E · Push to GitHub — status

## Done
- Local repository initialised in `ailt9019-week2/`.
- **23 files committed** (`625476d`): README, Parts A–D, prototype, proposal draft and
  shortlist.

## Blocked — needs your GitHub login
There was no `gh` CLI and no SSH key on this machine. I installed the GitHub CLI
(v2.100.0) at `C:\Users\sohan\.workbuddy-ai\binaries\gh\bin\gh.exe` — `winget` failed on
a symlink step, so I pulled the release zip directly and extracted it.

It reports: `You are not logged into any GitHub hosts.` Logging in is a browser flow and
the credential is yours, so I stopped here rather than guess.

## Runbook to finish Part E (about 2 minutes)

```bash
GH="C:/Users/sohan/.workbuddy-ai/binaries/gh/bin/gh.exe"
cd "C:/Users/sohan/WorkBuddy AI/2026-09-09-21-42-04/ailt9019-week2"

"$GH" auth login            # choose GitHub.com -> HTTPS -> Login with a web browser
"$GH" repo create ailt9019-week2 --private --source=. --remote=origin --push
```

## Acceptance — verify with a fresh clone
Part E is only done when a **fresh clone** contains everything, which is the check the
handout asks for. Run it in a *second* folder:

```bash
mkdir -p /c/Users/sohan/clone-test && cd /c/Users/sohan/clone-test
"$GH" repo clone ailt9019-week2
cd ailt9019-week2 && ls -R
```

Expected: the same 23 files, including `prototype/index.html`,
`part-c-mcp/server.py`, and `part-d-pi/practice/.pi/skills/pdf-summarizer/SKILL.md`.
Opening `prototype/index.html` from the clone should work immediately.
