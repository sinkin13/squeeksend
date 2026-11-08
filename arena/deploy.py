#!/usr/bin/env python3
"""Compile + deploy SqueekArena to Ethereum Sepolia."""
import json, subprocess, time, sys
import solcx
from eth_account import Account
from eth_utils import to_checksum_address

RPC = "https://ethereum-sepolia-rpc.publicnode.com"
CHAIN = 11155111
SRC = "/root/squeek/arena/SqueekArena.sol"
W = json.load(open("/root/squeek/DEPLOYER-ARENA.json"))
A = Account.from_key(W["private_key"])
F = A.address


def rpc(m, p, t=30):
    b = json.dumps({"jsonrpc": "2.0", "id": 1, "method": m, "params": p})
    for _ in range(3):
        r = subprocess.run(["curl", "-sS", "-m", str(t), "-X", "POST",
                            "-H", "Content-Type: application/json", "-d", b, RPC],
                           capture_output=True, text=True).stdout
        try:
            return json.loads(r)
        except Exception:
            time.sleep(2)
    return {}


solcx.install_solc("0.8.26", show_progress=False)
out = solcx.compile_files([SRC], output_values=["abi", "bin"], solc_version="0.8.26", optimize=True)
key = [k for k in out if k.endswith("SqueekArena.sol:SqueekArena")][0]
abi, bytecode = out[key]["abi"], out[key]["bin"]
print(f"  compiled ✓ abi={len(abi)} entries · bytecode={len(bytecode)//2} bytes", flush=True)

bal = int(rpc("eth_getBalance", [F, "latest"]).get("result", "0x0"), 16) / 1e18
print(f"  deployer {F} · {bal:.6f} ETH", flush=True)

gas = int(rpc("eth_estimateGas", [{"from": F, "data": "0x" + bytecode}]).get("result", "0x0"), 16) or 800000
print(f"  gas estimate {gas:,}", flush=True)
gp = int(rpc("eth_gasPrice", []).get("result", "0x0"), 16) or 2 * 10**9
nonce = int(rpc("eth_getTransactionCount", [F, "pending"]).get("result", "0x0"), 16)

tx = {"data": "0x" + bytecode, "gas": int(gas * 1.25), "gasPrice": gp,
      "nonce": nonce, "chainId": CHAIN, "value": 0}
s = A.sign_transaction(tx)
raw = s.raw_transaction.hex() if hasattr(s, "raw_transaction") else s.rawTransaction.hex()
if not raw.startswith("0x"):
    raw = "0x" + raw
res = rpc("eth_sendRawTransaction", [raw])
if res.get("error"):
    print("  ❌ DEPLOY GAGAL:", str(res["error"].get("message", ""))[:120], flush=True)
    sys.exit(1)
h = res["result"]
print(f"  ✅ deploy tx: {h}", flush=True)

for _ in range(40):
    time.sleep(3)
    rc = rpc("eth_getTransactionReceipt", [h]).get("result")
    if rc and rc.get("status") == "0x1":
        addr = rc["contractAddress"]
        print(f"\n  🎉 CONTRACT: {addr}", flush=True)
        print(f"  block: {int(rc['blockNumber'],16)} · gasUsed: {int(rc['gasUsed'],16):,}", flush=True)
        json.dump({"address": to_checksum_address(addr), "abi": abi, "tx": h,
                   "deployer": F, "chainId": CHAIN},
                  open("/root/squeek/arena/deployment.json", "w"), indent=1)
        print("  ✅ saved: /root/squeek/arena/deployment.json", flush=True)
        sys.exit(0)
    if rc and rc.get("status") != "0x1":
        print("  ❌ reverted", flush=True)
        sys.exit(1)
print("  ⏳ belum mined", flush=True)
