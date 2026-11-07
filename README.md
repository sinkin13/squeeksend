# SqueekSend 🐹

A tiny, honest HYPE transfer tool for **Squeekchain** (chain id 99901).

Connect a wallet, see what is in it, send HYPE with a memo. No backend, no tracking, no sign-up, no
proxying — every read and every write goes straight to the wallet provider you already trust.

## Why this exists

Most chain tools want an account, an RPC key, or a signature you did not ask for. SqueekSend does one
thing: move HYPE from your wallet to another address, on Squeekchain, with the chain id checked before
anything is signed.

## What it uses from Squeekchain

| Call | Where it goes |
|---|---|
| `eth_chainId` | your wallet provider — must be `0x1863d` (99901) |
| `eth_getBalance` | your wallet provider — balance of the connected address |
| `eth_sendTransaction` | your wallet provider — plain HYPE transfer, no calldata |

There is no hidden batch call, no approval, no `transferFrom`. The only thing the page can ever ask you
to sign is a native HYPE transfer to an address you typed.

## Features

- Connect / reconnect wallet, with automatic **Squeekchain** network detection
- One-click `wallet_addEthereumChain` if the chain is missing from your wallet
- Live balance, refreshed after each send
- Address validation before the wallet prompt appears
- Optional off-chain memo (kept in the page only — never transmitted)
- Zero dependencies, zero build step, one HTML file

## Run locally

```bash
git clone <this repo>
cd <this repo>
python3 -m http.server 8080
# open http://localhost:8080
```

## Deploy

Static. Any host works — GitHub Pages, Cloudflare Pages, Netlify, or your own server.

## Notes

- Testnet only. Squeekchain is a Sepolia testnet chain; nothing here touches real value.
- The page never reads, stores or transmits a private key.
- Contract addresses, if you add them later, must be checked by hand — this page ships with none on purpose.

## Licence

MIT

---

squeekchain-project: ef49d289-7dae-4374-87b2-ac6188a2159d
