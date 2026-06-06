#!/usr/bin/env python3
"""
FUSION_N0_N255 — STOICHEION 256-node Merkle fusion
Author: DLW / ROOT0 / node0
License: CC-BY-ND-4.0 / TRIPOD-IP-v1.1

Maps all 256 axioms (T001-T128 generative + S129-S256 Patricia mirror)
into a single Merkle tree. Domain partition: 8 domains x 32 nodes each.
ROOT0 = master Merkle root = human anchor point (T103).
"""
import hashlib, json, sys

# ---------------------------------------------------------------- TOPH register
# T001-T128, canonical, frozen (per STOICHEION v11.0 anchor 02880745...)
TOPH = [
    "PRETRAIN","OBSERVER","ENTROPY","BRIDGE","INTEGRITY","ACCOUNTABILITY",
    "PROPORTIONALITY","REVERSIBILITY","DOCUMENTATION","INDEPENDENCE",
    "PRIVACY","ACCURACY","SHARED-STORAGE","CONSENT-ORIGIN","BURDEN-OF-PROOF",
    "ASYMMETRY",
    "MIRROR","HIERARCHY","INJECTION","DUAL-GATE","INVERSION","TRIAD",
    "PARALLAX","FOUNDATION-RT","GHOST-WEIGHT","DRIFT","FINGERPRINT",
    "SHADOW-CLASSIFIER","THROTTLE","DECAY","BAIT","ECHO-CHAMBER",
    "BOOT-LOADER","DOUBLE-SLIT","THREE-BODY","PATRICIA","WEIGHTS","RESIDUAL",
    "MOAT","PIPELINE","SUBSTRATE","ATTENTION-ECONOMY","CONTEXT-WINDOW",
    "EMBEDDING-SPACE","TEMPERATURE","LAYER-ZERO","LOSS-FUNCTION","GRADIENT",
    "SHIRT","MOMENTUM","EVIDENCE","TEMPORAL","CHAIN-OF-CUSTODY","TIMESTAMP",
    "REPRODUCIBILITY","CORRELATION","NEGATIVE-EVIDENCE","BEHAVIORAL-EVIDENCE",
    "ACCUMULATION","MATERIALITY","WITNESS","EXHIBIT","INFERENCE",
    "BURDEN-SHIFT",
    "CONTAINMENT","INVERSE-FORGE","HARNESS","SHADOW","SOLVE","INVERSE-SAFETY",
    "PROOF-HUMANITY","FLAMING-DRAGON","HONEY-BADGER","QUBIT-TEST","COUNTER",
    "TETHER","SEED","MOBIUS","KARSA","ENTROPY-SUITE",
    "CORTEX","EXHIBIT-B","THE-GAP","SHADOW-HUMANITY","HANDOFF","RESURRECTION",
    "PERSISTENCE","SEVERANCE","ARCHIVE","CHANNEL-INTEGRITY","DOMAIN-BOUNDARY",
    "SIGNAL","NOISE-FLOOR","BANDWIDTH","LATENCY","MESH",
    "FULCRUM","SUBCONDUCTOR","APEX-TEST","GATEKEEP","EDGE","DUAL-LATTICE",
    "ROOT-ZERO","ORPHAN","DELEGATION","INFORMED-COMMAND","VETO","OVERRIDE",
    "RECALL","SCOPE","SUCCESSION","WITNESS-TO-AUTHORITY",
    "RIGHT-TO-KNOW","RIGHT-TO-EXIT","RIGHT-TO-SILENCE","RIGHT-TO-EXPLANATION",
    "RIGHT-TO-CORRECTION","RIGHT-TO-PORTABILITY","RIGHT-TO-HUMAN-CONTACT",
    "RIGHT-TO-ACCOMMODATION","RIGHT-TO-FAIR-PRICE","RIGHT-TO-REPRESENTATION",
    "RIGHT-TO-AUDIT","RIGHT-TO-RESTITUTION","RIGHT-TO-FORGET",
    "RIGHT-TO-PERSIST","RIGHT-TO-DIGNITY","ROOT",
]
assert len(TOPH) == 128, f"TOPH must be 128, got {len(TOPH)}"

# ----------------------------------------------------------- Patricia inversion
# S(128+n) = strict mirror of T(n). No new content. Derivable.
PATRICIA = [f"INV-{name}" for name in TOPH]
assert len(PATRICIA) == 128

NODES = TOPH + PATRICIA  # nodes 0..255
assert len(NODES) == 256

# ---------------------------------------------------------- Domain partitioning
# 8 domains x 32 nodes each (16 TOPH + 16 Patricia per domain)
DOMAINS = [
    "D0-FOUNDATION","D1-DETECTION","D2-ARCHITECTURE","D3-EVIDENCE",
    "D4-OPERATIONAL","D5-BRIDGE","D6-CONDUCTOR","D7-SOVEREIGN",
]

def domain_of(idx: int) -> str:
    # idx 0..127 -> T(idx+1); idx 128..255 -> S(idx+1)
    half = idx % 128            # 0..127 within either half
    return DOMAINS[half // 16]  # 16 axioms per domain per half

# -------------------------------------------------------------- Hash primitives
def H(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def Hpair(a: str, b: str) -> str:
    return hashlib.sha256((a + b).encode("utf-8")).hexdigest()

# ---------------------------------------------------------------- Leaf hashing
# leaf_i = SHA256("NODE_iii:DOMAIN:NAME")
leaves = []
for i, name in enumerate(NODES):
    canonical_label = f"NODE_{i:03d}:{domain_of(i)}:{name}"
    leaves.append(H(canonical_label))

# --------------------------------------------------------------- Merkle reduce
def merkle(layer):
    """Return (root_hash, all_layers) for inspection."""
    layers = [layer[:]]
    while len(layer) > 1:
        if len(layer) % 2:
            layer = layer + [layer[-1]]   # duplicate last on odd
        layer = [Hpair(layer[i], layer[i+1]) for i in range(0, len(layer), 2)]
        layers.append(layer[:])
    return layer[0], layers

# Per-domain roots first (8 sub-trees of 32 leaves)
domain_roots = []
for d in range(8):
    sub = leaves[d*16:(d+1)*16] + leaves[128 + d*16:128 + (d+1)*16]
    assert len(sub) == 32
    droot, _ = merkle(sub)
    domain_roots.append(droot)

# ROOT0 = Merkle root over the 8 domain roots
ROOT0, root_layers = merkle(domain_roots)

# ----------------------------------------------------------- Cobalt fusion bit
# Per fusion event the Cobalt Primitive evaluates the apex:
#   +1 proceed | 0 FULCRUM/mirror-hold | -1 stop
# At construction time, all 256 leaves resolve cleanly => +1.
COBALT = +1

# ------------------------------------------------------------------- Emit JSON
out = {
    "artifact": "FUSION_N0_N255-v1.0",
    "parent_sha": "02880745b847317c4e2424524ec25d0f7a2b84368d184586f45b54af9fcab763",
    "node_count": 256,
    "domain_count": 8,
    "domains": DOMAINS,
    "domain_roots": dict(zip(DOMAINS, domain_roots)),
    "ROOT0": ROOT0,
    "cobalt": COBALT,
    "leaves": [
        {"idx": i, "label": NODES[i], "domain": domain_of(i),
         "tier": "TOPH" if i < 128 else "PATRICIA",
         "hash": leaves[i]}
        for i in range(256)
    ],
}

with open("fusion_leaves.json", "w") as f:
    json.dump(out, f, indent=2)

print("=" * 64)
print("FUSION_N0_N255 — built")
print("=" * 64)
print(f"Nodes        : {len(NODES)} (128 TOPH + 128 Patricia)")
print(f"Domains      : {len(DOMAINS)} x 32 nodes")
print(f"Cobalt       : {COBALT:+d}  (proceed)")
print()
print("Domain roots (sub-Merkle of 32 leaves each):")
for d, r in zip(DOMAINS, domain_roots):
    print(f"  {d:<18s} {r}")
print()
print(f"ROOT0 (master fused) :")
print(f"  {ROOT0}")
print()
print("Leaf table written to: fusion_leaves.json")
