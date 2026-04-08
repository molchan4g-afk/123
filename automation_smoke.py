#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import socket

from relay_post import send_message


def build_text(label: str) -> str:
    now_utc = dt.datetime.now(dt.timezone.utc)
    return (
        f"Codex automation OK\n"
        f"label: {label}\n"
        f"utc: {now_utc.isoformat()}\n"
        f"host: {socket.gethostname()}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a smoke-test message through Phone1 relay.")
    parser.add_argument("--label", default="smoke")
    args = parser.parse_args()

    payload = send_message(
        text=build_text(args.label),
        sender="bot",
        source="codex-cloud",
        channel="main",
        metadata={"kind": "automation_smoke", "label": args.label},
    )
    print(payload)


if __name__ == "__main__":
    main()
