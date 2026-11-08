# SqueekArena 🐹⚔️

A 60-second click-mining game on **Squeekchain** (Ethereum Sepolia, chain id **11155111**).

Tap the hamster. Every 100 taps mines a block. When the shift ends, submit your score to a tiny
Solidity contract and it lands on a global on-chain leaderboard that nobody can edit.

## Contract

| | |
|---|---|
| Network | Ethereum Sepolia (11155111) |
| Address | `0xeaf570471b4b23d0f192b82616b051deb2f601b0` |
| Source | `SqueekArena.sol` |

### What the game actually calls

| Call | Purpose |
|---|---|
| `submitScore(uint64 score, uint64 blocks)` | writes your run on-chain, emits `Scored` |
| `page(uint256 cursor, uint256 limit)` | newest-first leaderboard page |
| `total()` | number of runs recorded |
| `best(address)` | your personal best |

There is a 30 second cooldown per wallet between submissions, a hard cap of 200,000 points, and
`blocks <= score` is enforced.

## How it uses Squeekchain

Everything goes through the player's own wallet provider — `eth_chainId` (must be `0xaa36a7`),
`eth_call` for the leaderboard, `eth_sendTransaction` for the score. If the wallet is on another
network the page offers `wallet_switchEthereumChain` and falls back to `wallet_addEthereumChain`.

## Deploy / dev

```bash
python3 -m http.server 8080    # from the repo root, then open /arena/
```

Licence: MIT

