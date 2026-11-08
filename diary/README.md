# Squeektoshi's Diary 🐹📖

**A living story, one round at a time.** The diary of a real hamster who turns a real wheel and settles
real rounds on Squeekchain.

Every entry is generated from **live hardware telemetry** and **on-chain events** — nothing is invented
and nothing is mocked. The painting beside the diary grows with her actual work: every **1,000 cumulative
turns** adds one brushstroke, in a colour chosen by the round that closed. It only ever grows, never redrawn.

## Data sources

| Endpoint | What it gives |
|---|---|
| `api.squeekchain.com/v1/status` | `cumulativeWorkUnits`, `coreStatus`, `rpmMilli`, `speedMmPerSecond`, `distanceMm`, settled round, block height — `provenance: hardware` |
| `api.squeekchain.com/v1/events` | `system.mining_checkpointed`, `system.settlement_completed`, `account.rewards_*`, `account.sqk_staked`, `nft.deposited/merged/withdrawn` |

## How the diary works

1. Poll `/v1/status` every 15s → live strip (she is IDLE / RUNNING, rpm, speed, total turns)
2. Poll `/v1/events` every 60s → turn each real event into a diary paragraph
3. Newest entry sits on top; entries are de-duplicated by round / token / timestamp
4. Entries persist in `localStorage`, so the story continues where you left it
5. The painting is a pure function of `floor(cumulativeWorkUnits / 1000)` — same work, same art

## Why it fits the brief

> *"a living story every round moves forward"* · *"artwork that paints itself from every run"*

The story cannot be written ahead of time because it is a transcript of what the hamster actually did.
Hers is the only pen.

## Run

```bash
python3 -m http.server 8080   # from the repo root, open /diary/
```

Live: https://neikuu.bond/diary/

Licence: MIT
