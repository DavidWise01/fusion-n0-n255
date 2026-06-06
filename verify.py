#!/usr/bin/env python3
"""
verify.py — re-derive ROOT0 from the rule, trusting nothing in this repo.

This does NOT import fusion.py and does NOT trust the stored leaf hashes.
It takes only the artifact's *labels*, recomputes every hash from the
documented rule, rebuilds the Merkle tree from scratch, and checks that the
root it gets is the canonical ROOT0. If a single byte of the register or a
single stored hash were altered, this fails.

    rule:        leaf_i = SHA256("NODE_iii:DOMAIN:NAME")
    pair:        SHA256(a + b)            (odd layer -> duplicate last)
    domain d:    16 TOPH leaves + 16 Patricia mirror leaves -> sub-Merkle
    ROOT0:       Merkle over the 8 domain roots

Usage:  python verify.py        (exit 0 = verified, 1 = drift)
"""
import hashlib, json, io, sys

CANONICAL_ROOT0 = "c6f487e36599d44d19c7926fc329c8de34322f7551f7be43e813ea8c7eff05df"

def H(s):       return hashlib.sha256(s.encode("utf-8")).hexdigest()
def Hpair(a, b): return hashlib.sha256((a + b).encode("utf-8")).hexdigest()

def merkle(layer):
    layer = layer[:]
    while len(layer) > 1:
        if len(layer) % 2:
            layer = layer + [layer[-1]]          # duplicate last on odd
        layer = [Hpair(layer[i], layer[i+1]) for i in range(0, len(layer), 2)]
    return layer[0]

def main():
    art = json.load(io.open("fusion_leaves.json", encoding="utf-8"))
    leaves_in = art["leaves"]
    if len(leaves_in) != 256:
        print(f"✗ expected 256 leaves, got {len(leaves_in)}"); return 1

    # 1 — recompute every leaf hash from the rule, using only the labels
    recomputed, bad = [], 0
    for L in leaves_in:
        want = H(f"NODE_{L['idx']:03d}:{L['domain']}:{L['label']}")
        recomputed.append(want)
        if want != L["hash"]:
            bad += 1
            print(f"  ✗ leaf {L['idx']:>3} ({L['label']}): stored hash does not match rule")
    print(f"leaves : {256 - bad}/256 reproduce from SHA256('NODE_iii:DOMAIN:NAME')")

    # 2 — rebuild the 8 domain sub-trees and ROOT0 from the recomputed leaves
    DOMAINS = art["domains"]
    droots = [merkle(recomputed[d*16:(d+1)*16] + recomputed[128 + d*16:128 + (d+1)*16])
              for d in range(8)]
    root0 = merkle(droots)

    # 3 — compare to the stored artifact and the canonical anchor
    dr_ok   = all(droots[i] == art["domain_roots"][DOMAINS[i]] for i in range(8))
    stored_ok = (root0 == art["ROOT0"])
    anchor_ok = (root0 == CANONICAL_ROOT0)
    print(f"domains: {'all 8 reproduce' if dr_ok else 'MISMATCH'}")
    print(f"ROOT0  : {root0}")
    print(f"         matches stored artifact : {stored_ok}")
    print(f"         matches canonical anchor : {anchor_ok}")

    ok = (bad == 0) and dr_ok and stored_ok and anchor_ok
    print("\n" + ("✓ VERIFIED — the artifact reproduces from the rule, bit for bit."
                  if ok else "✗ FAILED — drift detected; this is not the canonical fusion."))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
