# SqueekScope 🔭🐹

**The wheel never stops.** A live, read-only observatory for the network Squeekchain lives on —
**Ethereum Sepolia (11155111)**.

Every block is rendered as one turn of the wheel. The page never writes, never asks for a wallet, and
never stores anything: the chain is the record, SqueekScope just watches it happen.

## What it does

| Panel | What it reads |
|---|---|
| The wheel | `eth_blockNumber` polling + the timestamp delta between blocks → real wheel speed |
| Wheel speed | seconds between consecutive blocks (the hamster's actual pace) |
| Turns seen | blocks observed since you opened the tab |
| Gas price | `eth_gasPrice` every turn |
| Heatmap | last 100 blocks, intensity = `gasUsed`, hidden tooltip = tx count |
| Almanac | newest turns first: block, hash, tx count, gas used, time |

## Design note

The whole thing is one HTML file with no dependencies and no build step. It seeds 100 blocks in
parallel on load, then polls every 4 seconds. Two public RPC endpoints are rotated automatically, so a
single endpoint going down does not kill the page.

## Run

```bash
python3 -m http.server 8080   # from the repo root, open /scope/
```

Live: https://neikuu.bond/scope/

Licence: MIT
