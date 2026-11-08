# SqueekSend 🐹

A tiny, honest **ETH** transfer tool for **Squeekchain**, the hamster-powered proof-of-work toychain
that runs on **Ethereum Sepolia (chain id 11155111)**.

Connect a wallet, see what is in it, send ETH. No backend, no tracking, no sign-up, no proxying —
every read and every write goes straight to the wallet provider you already trust.

## Why this exists

Most chain tools want an account, an RPC key, or a signature you did not ask for. SqueekSend does one
thing: move ETH from your wallet to another address, on the Sepolia network Squeekchain lives on, with
the chain id checked before anything is signed.

## What it uses from Squeekchain

| Call | Where it goes |
|---|---|
| `eth_chainId` | your wallet provider — must be `0xaa36a7` (11155111, Sepolia) |
| `eth_getBalance` | your wallet provider — balance of the connected address |
| `eth_sendTransaction` | your wallet provider — plain ETH transfer, no calldata |

There is no hidden batch call, no approval, no `transferFrom`. The only thing the page can ever ask you
to sign is a native ETH transfer to an address you typed.

If the wallet is on another network, the page calls `wallet_switchEthereumChain` and falls back to
`wallet_addEthereumChain` so a fresh wallet can jump straight onto Sepolia.

## Features

- Connect / reconnect wallet, with automatic network detection
- One-click `wallet_switchEthereumChain` / `wallet_addEthereumChain` for Sepolia
- Live balance in ETH, refreshed after each send
- Address validation before the wallet prompt appears
- Zero dependencies, zero build step, one HTML file (7 KB)

## Run locally

```bash
git clone https://github.com/sinkin13/squeeksend
cd squeeksend
python3 -m http.server 8080
# open http://localhost:8080
```

## Live

https://neikuu.bond

## Notes

- Sepolia testnet only. Nothing here touches real value.
- The page never reads, stores or transmits a private key.
- No contract addresses ship with this page on purpose — it only moves native ETH.

```
squeekchain-project: ef49d289-7dae-4374-87b2-ac6188a2159d
```

## Licence

MIT
