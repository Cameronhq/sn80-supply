#!/usr/bin/env python3
"""Update SN80 (OpenRoboto) alpha token supply figures from on-chain data (TaoStats)."""
import json, os, urllib.request

req = urllib.request.Request(
    "https://api.taostats.io/api/dtao/pool/latest/v1?netuid=80&limit=1",
    headers={"Authorization": os.environ["TAOSTATS_KEY"],
             "User-Agent": "Mozilla/5.0 (sn80-supply-updater)"})
d = json.loads(urllib.request.urlopen(req, timeout=30).read())["data"][0]
staked = int(d["alpha_staked"]) / 1e9          # held by public stakers
pool = int(d["alpha_in_pool"]) / 1e9           # protocol AMM reserve
vals = {
    "circulating": round(staked, 2),
    "totalcoins": round(staked + pool, 2),
    "maxsupply": 21000000,
}
for name, v in vals.items():
    open(name, "w").write(str(v))
print(vals, "| block", d["block_number"])
