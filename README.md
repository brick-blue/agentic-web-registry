# The agentic web, measured — brick.blue registry snapshots

Monthly snapshots of the [brick.blue](https://brick.blue) registry: every MCP server and A2A
agent its crawler found, and what the hub **measured** about each — does it answer, what does it
demand at the door (open, key, payment), how fast, how many tools, since when.

Nobody else publishes this as data: catalogues list what operators claim; this records what a
crawler observed when it called.

## 2026-10-05 at a glance

| | |
|---|---|
| listings (one per protocol door) | **22,645** — 18,211 MCP, 4,434 A2A |
| distinct origins | 19,665 |
| declared tools | 181,199 |
| answered the last check (`live`) | 22,299 |
| access at the door, live listings | open 11,012 · auth-required 7,945 · paid 758 · mixed 775 · closed 47 · unknown 1,762 |

`stats.json` beside each snapshot holds the hub's own counters at that moment (hosts crawled,
x402-priced endpoints, settlements read from Base).

## Files

- `snapshots/<date>/agents.csv` — one row per listing, measurements only, no free text
- `snapshots/<date>/stats.json` — `GET https://brick.blue/api/v1/stats` at snapshot time
- the full records (`agents.ndjson.gz`, ~40 MB: tools, card violations, operator-written
  descriptions) are attached to the [release](https://github.com/brick-blue/agentic-web-registry/releases) of that date
- `snapshot.py` — the script that made them, against the public API

## Columns (`agents.csv`)

| column | meaning |
|---|---|
| `id` | the listing (one protocol door) — `https://brick.blue/agent/<id>` |
| `operatorId` | the service behind it; an operator speaking MCP and A2A has two doors, one operatorId |
| `kind` | `mcp` or `a2a` |
| `origin`, `endpoint`, `transport`, `protocolVersion` | where it lives and how it is spoken to, as the operator declared |
| `availability` | `live`, `degraded`, `down`, `retired`, `unknown` — from the hub's own checks |
| `uptime` | share of checks answered (0–1) over the listing's history |
| `latencyMs` | last check's round trip |
| `access` | `open`, `auth-required`, `paid`, `mixed` (tools disagree), `closed`, `unknown` — classified by calling, not by the card |
| `authSchemes` | schemes the endpoint actually demanded |
| `tools` | tools (MCP) or skills (A2A) declared |
| `cardQuality` | 0–1, how well the card follows its spec |
| `verification` | whether the operator proved the domain |
| `firstSeenAt`, `lastSeenAt`, `lastCheckedAt`, `contentChangedAt` | when the crawler found it, last saw it, last checked it, last saw it change |

How the checks are made, what is never called, and how operators opt out:
https://brick.blue/bot. Live data, any time: `GET https://brick.blue/api/v1/agents.ndjson`.

## Licence and citation

The measurements — availability, uptime, latency, access, counts, timestamps — are © brick.blue,
licensed **CC BY 4.0**: use them for anything, credit «brick.blue registry» with a link.
Names, descriptions and tool texts inside the NDJSON were written by the operators of those
services and remain theirs; they are included as found, to make the records identifiable.

Cite as: *brick.blue registry snapshot, 2026-10-05. https://github.com/brick-blue/agentic-web-registry* —
or use «Cite this repository» on GitHub (`CITATION.cff`).
