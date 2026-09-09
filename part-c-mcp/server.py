#!/usr/bin/env python3
"""Tiny MCP server - stdlib only, no pip install needed.

Speaks Model Context Protocol over stdio (newline-delimited JSON-RPC 2.0).
Exposes three read-only tools:
    today        - today's date, weekday, ISO week
    current_time - current local time as ISO 8601
    days_until   - whole days from today until a YYYY-MM-DD date

Anything that is not JSON goes to stderr so stdout stays a clean protocol channel.
"""

import json
import sys
from datetime import date, datetime

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "week2-tiny-tools"
SERVER_VERSION = "0.1.0"

# ---------------------------------------------------------------- tools


def tool_today(_args):
    d = date.today()
    return (
        f"{d.isoformat()} ({d.strftime('%A')}), "
        f"ISO year {d.isocalendar()[0]} week {d.isocalendar()[1]}"
    )


def tool_current_time(_args):
    now = datetime.now().astimezone()
    return f"{now.isoformat(timespec='seconds')} (UTC{now.strftime('%z')})"


def tool_days_until(args):
    raw = (args or {}).get("date", "")
    try:
        target = date.fromisoformat(str(raw))
    except ValueError:
        return f"ERROR: could not parse '{raw}' as YYYY-MM-DD."
    delta = (target - date.today()).days
    if delta > 0:
        return f"{delta} day(s) until {target.isoformat()} (today is {date.today().isoformat()})."
    if delta < 0:
        return f"{-delta} day(s) since {target.isoformat()} (today is {date.today().isoformat()})."
    return f"{target.isoformat()} is today."


TOOLS = [
    {
        "name": "today",
        "description": "Return today's real date, weekday name, and ISO week number. "
                       "Use this whenever asked what date it is - do not guess.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "current_time",
        "description": "Return the current local time as an ISO 8601 timestamp with UTC offset.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "days_until",
        "description": "Return the whole number of days from today until a given date. "
                       "Negative means the date has already passed.",
        "inputSchema": {
            "type": "object",
            "properties": {"date": {"type": "string", "description": "Target date, YYYY-MM-DD"}},
            "required": ["date"],
            "additionalProperties": False,
        },
    },
]

HANDLERS = {
    "today": tool_today,
    "current_time": tool_current_time,
    "days_until": tool_days_until,
}


# ------------------------------------------------------------- protocol


def reply(req_id, result):
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def error(req_id, code, message):
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def handle(message):
    """Route one JSON-RPC message. Returns None for notifications (no reply)."""
    method = message.get("method")
    req_id = message.get("id")

    if method == "initialize":
        return reply(req_id, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        })

    if method == "notifications/initialized" or (method or "").startswith("notifications/"):
        return None

    if method == "ping":
        return reply(req_id, {})

    if method == "tools/list":
        return reply(req_id, {"tools": TOOLS})

    if method == "tools/call":
        name = (message.get("params") or {}).get("name")
        args = (message.get("params") or {}).get("arguments") or {}
        handler = HANDLERS.get(name)
        if handler is None:
            return error(req_id, -32601, f"Unknown tool: {name}")
        try:
            text = handler(args)
        except Exception as exc:  # surface failures as tool errors, not a crashed server
            return reply(req_id, {
                "content": [{"type": "text", "text": f"Tool '{name}' failed: {exc}"}],
                "isError": True,
            })
        return reply(req_id, {"content": [{"type": "text", "text": text}], "isError": False})

    if req_id is not None:
        return error(req_id, -32601, f"Method not found: {method}")
    return None


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            sys.stderr.write(f"[server] bad JSON ignored: {line[:120]}\n")
            continue
        response = handle(message)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
