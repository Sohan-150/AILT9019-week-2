# Part C · A tiny MCP tool — acceptance

## What I built
`server.py` — a Model Context Protocol server, **stdlib only** (no pip packages, so it
cannot break on a dependency install). Speaks JSON-RPC 2.0 over stdio.

Three tools:

| Tool | Returns |
|---|---|
| `today` | today's real date, weekday name, ISO week |
| `current_time` | current local time as ISO 8601 with UTC offset |
| `days_until` | whole days from today until a `YYYY-MM-DD` date |

## Registration
Added to **`~/.workbuddy-ai/mcp.json`** (the MCP config file, not `.mcp.json`):

```json
{
  "mcpServers": {
    "week2-tiny-tools": {
      "command": "C:\\Users\\sohan\\.workbuddy-ai\\binaries\\python\\envs\\default\\Scripts\\python.exe",
      "args": ["C:\\Users\\sohan\\WorkBuddy AI\\...\\ailt9019-week2\\part-c-mcp\\server.py"],
      "env": { "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1" }
    }
  }
}
```

Verified the registration by launching the server **exactly as the config describes** —
same command, same args, neutral working directory — and reading a `tools/list` response
back. It answered, so the config is correct.

## Real tool output
`test_client.py` performs a genuine MCP handshake (`initialize` →
`notifications/initialized` → `tools/list` → `tools/call`). Full log in
`tool-output.txt`:

```
1) initialize -> {"name": "week2-tiny-tools", "version": "0.1.0"} | protocol 2024-11-05
2) tools/list -> today, current_time, days_until
3) tools/call today          -> 2026-09-09 (Wednesday), ISO year 2026 week 37
3) tools/call current_time   -> 2026-09-09T21:51:36+08:00 (UTC+0800)
3) tools/call days_until{2026-09-25} -> 16 day(s) until 2026-09-25 (today is 2026-09-09).
4) unknown tool -> {"code": -32601, "message": "Unknown tool: nope"}
```

## Acceptance — which part came from the tool?
Answering *"What date is it today? Use the date tool, do not guess."*:

> Today is **2026-09-09 (Wednesday)**, ISO year 2026 week **37**.

- **From the tool:** the date `2026-09-09`, the weekday `Wednesday`, and `week 37`. These
  are produced by Python's `datetime` reading this machine's clock — the model has no
  way to know them and would be guessing.
- **From me (the model):** only the words "Today is" and the punctuation.

Second proof, same point: `days_until 2026-09-25` returned **16 days** — the arithmetic
on the proposal deadline was done by the tool, not estimated by me.

**Takeaway:** MCP is how you give a model access to facts it cannot hold in its weights.
The contract is explicit — the tool returns a string, and the model's job is to report
it, not to reconstruct it.

## Note
I first tried `pip install mcp` (the official SDK) and it failed on this machine. I wrote
the server against the raw protocol instead, which turned out better for the lab: you can
see the whole handshake rather than a framework doing it for you.
