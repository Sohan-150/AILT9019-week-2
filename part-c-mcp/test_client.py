#!/usr/bin/env python3
"""Minimal MCP client: spawns server.py over stdio, does a real handshake,
lists tools, and calls each one. Proves the server works before registering it."""

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SERVER = HERE / "server.py"
PYTHON = sys.executable


class Client:
    def __init__(self):
        self.proc = subprocess.Popen(
            [PYTHON, str(SERVER)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        self._id = 0

    def send(self, method, params=None, notify=False):
        msg = {"jsonrpc": "2.0", "method": method}
        if not notify:
            self._id += 1
            msg["id"] = self._id
        if params is not None:
            msg["params"] = params
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        if notify:
            return None
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("server closed stdout")
            resp = json.loads(line)
            if resp.get("id") == self._id:
                return resp

    def close(self):
        self.proc.stdin.close()
        self.proc.terminate()


def main():
    c = Client()

    init = c.send("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "week2-test-client", "version": "1.0"},
    })
    print("1) initialize ->", json.dumps(init["result"]["serverInfo"]),
          "| protocol", init["result"]["protocolVersion"])
    c.send("notifications/initialized", notify=True)

    tools = c.send("tools/list")["result"]["tools"]
    print("2) tools/list ->", ", ".join(t["name"] for t in tools))

    for call in (("today", {}), ("current_time", {}), ("days_until", {"date": "2026-09-25"})):
        name, args = call
        res = c.send("tools/call", {"name": name, "arguments": args})["result"]
        text = res["content"][0]["text"]
        print(f"3) tools/call {name}{args if args else ''} -> {text}")
        assert res.get("isError") is not True, f"{name} returned an error"

    bad = c.send("tools/call", {"name": "nope", "arguments": {}})
    print("4) unknown tool ->", json.dumps(bad.get("error", {})))

    c.close()
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
