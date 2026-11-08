# Squeek Battle 🐹⚔️

A **deterministic 2D battle royale** for Squeekchain on Ethereum Sepolia (11155111).

24 AI hamsters drop into the arena, grab weapons, and fight inside a shrinking **Cat Storm**. Every
match is a pure function of its seed: same seed, same drop points, same pickups, same winner — so anyone
can replay a match and check the recorded result is honest.

## Why deterministic

The whole simulation runs on a seeded PRNG (mulberry32) with a **fixed 60 Hz logical step**. There is no
`Math.random()` inside the simulation, no wall-clock dependency, and targeting ties break by unit id.
Feed the same seed in and you get byte-identical behaviour, every time, on any machine.

## What's in a match

| | |
|---|---|
| Combatants | 24 hamsters, 8 faces, 24 names |
| Weapons | Paws (4 dmg) · Axe (16, melee) · Bow (11, ranged) · Bomb (26, area) |
| Pickups | 26 scattered weapons, first come first served |
| Storm | starts at r=560, shrinks 62px every 5s after a 12s grace, 0.22 dmg/tick outside |
| Cap | 3 minutes of simulated time, then highest HP wins |

## On-chain record

| | |
|---|---|
| Network | Ethereum Sepolia (11155111) |
| Address | `0x06DB724B69e5b264115845A948c4944D4f834422` |
| Write | `recordMatch(uint64 seed, uint8 winnerId, uint8 survivors, uint16 durationSec)` |
| Read | `page(uint256,uint256)` · `total()` · `matchAt(uint256)` |

A seed can only be recorded once — since the match is a pure function of the seed, a second record for
the same seed would have to be identical anyway, so duplicates are rejected by the contract.

## Run

```bash
python3 -m http.server 8080   # from the repo root, open /battle/
```

Live: https://neikuu.bond/battle/

Licence: MIT
