#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib import error, request


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def send_message(text: str, sender: str, source: str, channel: str, metadata: dict) -> dict:
    relay_url = required_env("PHONE1_RELAY_URL").rstrip("/")
    ingest_token = required_env("PHONE1_RELAY_INGEST_TOKEN")

    payload = {
        "text": text,
        "sender": sender,
        "source": source,
        "channel": channel,
        "metadata": metadata,
    }

    req = request.Request(
        f"{relay_url}/ingest",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Phone1-Ingest": ingest_token,
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Relay HTTP {exc.code}: {details}") from exc
    except error.URLError as exc:
        raise SystemExit(f"Relay network error: {exc}") from exc

    return json.loads(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Send one message to Phone1 relay.")
    parser.add_argument("--text", required=True, help="Message text to send.")
    parser.add_argument("--sender", default="bot", choices=["bot", "user", "system"])
    parser.add_argument("--source", default="codex-cloud")
    parser.add_argument("--channel", default=os.environ.get("PHONE1_CHANNEL", "main"))
    parser.add_argument("--metadata", default="{}", help="JSON object.")
    args = parser.parse_args()

    try:
        metadata = json.loads(args.metadata)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid metadata JSON: {exc}") from exc

    result = send_message(
        text=args.text,
        sender=args.sender,
        source=args.source,
        channel=args.channel,
        metadata=metadata,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8") if hasattr(sys.stdout, "reconfigure") else None
    main()
