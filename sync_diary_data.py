#!/usr/bin/env python3
"""Ambil data Squeekchain → tulis ke repo (data.json) supaya browser ngga perlu CORS."""
import json, subprocess, sys, time, os

API = "https://api.squeekchain.com"
REPO = "/root/squeek"
OUT = os.path.join(REPO, "diary", "data.json")


def get(path, t=25):
    for _ in range(3):
        r = subprocess.run(["curl", "-sS", "-m", str(t), "--compressed", API + path],
                           capture_output=True, text=True)
        try:
            return json.loads(r.stdout)
        except Exception:
            time.sleep(3)
    return None


def main():
    st = get("/v1/status")
    ev = get("/v1/events")
    if not st:
        print("  ❌ status gagal — batal update", flush=True)
        sys.exit(1)

    m = st.get("measurement") or {}
    b = (st.get("builder") or {}).get("anchor") or {}

    payload = {
        "fetchedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": {
            "coreStatus": m.get("coreStatus"),
            "rpmMilli": m.get("rpmMilli"),
            "speedMmPerSecond": m.get("speedMmPerSecond"),
            "distanceMm": m.get("distanceMm"),
            "cumulativeWorkUnits": m.get("cumulativeWorkUnits"),
            "freshness": m.get("freshness"),
            "provenance": m.get("provenance"),
            "observedAt": m.get("observedAt"),
            "round": b.get("settledThroughRound"),
            "blockHeight": b.get("blockHeight"),
            "workPerThousandBlocks": b.get("workPerThousandBlocks"),
        },
        "events": [],
    }

    if ev and isinstance(ev.get("events"), list):
        keep = ("system.", "account.", "nft.")
        for e in ev["events"]:
            t = e.get("type") or ""
            if not t.startswith(keep):
                continue
            payload["events"].append({
                "id": e.get("id"),
                "type": t,
                "occurredAt": e.get("occurredAt"),
                "payload": e.get("payload") or {},
            })

    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, separators=(",", ":"))
    os.replace(tmp, OUT)
    print(f"  ✅ {OUT} · {len(payload['events'])} events · round {payload['status']['round']} · work {payload['status']['cumulativeWorkUnits']}", flush=True)


if __name__ == "__main__":
    main()
