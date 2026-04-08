# Codex Cloud Relay Setup

This repository is the minimal cloud-safe base for Codex automations that need to send messages to the Phone1 relay.

## Files

- `relay_post.py` sends one message to the relay using only the Python standard library.
- `automation_smoke.py` sends a timestamped smoke-test message.

## Required environment variables

Set these in the Codex Cloud environment, not in the repository:

- `PHONE1_RELAY_URL`
- `PHONE1_RELAY_INGEST_TOKEN`
- `PHONE1_CHANNEL` (optional, default: `main`)

## Internet access

The Codex Cloud environment must allow outbound access to your relay host. At minimum, allow:

- `POST` to the relay ingest endpoint host

## Manual smoke test

```bash
python3 automation_smoke.py --label manual-test
```

## Automation prompt example

Use a Codex automation prompt like this:

```text
In the repository root, run `python3 automation_smoke.py --label nightly-check`. Confirm whether the relay accepted the message and summarize the result in one short sentence.
```
