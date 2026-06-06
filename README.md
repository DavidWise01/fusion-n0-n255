# FUSION_N0_N255

*A reproducible Merkle commitment over the full 256-node STOICHEION axiom space — the one artifact in the archive whose defense is built in.*

[![kind](https://img.shields.io/badge/kind-verifiable%20artifact-2e7d6b?style=flat-square)](#verify-it-yourself)
[![verified](https://img.shields.io/badge/ROOT0-reproduces%20bit--for--bit-2e9e6a?style=flat-square)](#verify-it-yourself)
[![emergence](https://img.shields.io/badge/emergence-none%20·%20deterministic-3a3358?style=flat-square)](#honest)
[![License: CC-BY-ND-4.0](https://img.shields.io/badge/license-CC--BY--ND--4.0-7c3aed?style=flat-square)](LICENSE)

`fusion.py` hashes all **256 nodes** of the STOICHEION space (128 `TOPH` generative axioms + 128 `Patricia` constraint-inversions) into **8 domain sub-trees → one master Merkle root, `ROOT0`.** Change the register by a single byte and `ROOT0` diverges — that *is* the immutability proof.

```
ROOT0 = c6f487e36599d44d19c7926fc329c8de34322f7551f7be43e813ea8c7eff05df
```

## Verify it yourself

No need to trust this repo. The whole point is that you can re-derive the root:

```bash
python verify.py          # → ✓ VERIFIED — reproduces bit for bit (exit 0)
```

`verify.py` does **not** import `fusion.py` and does **not** trust the stored hashes. It takes only the artifact's *labels*, recomputes every leaf from the documented rule, rebuilds the Merkle tree from scratch, and checks the root. Want to trust even less? Recompute a single leaf by hand:

```bash
python -c "import hashlib; print(hashlib.sha256(b'NODE_000:D0-FOUNDATION:PRETRAIN').hexdigest())"
# 98bb46ddcf685b7941f2f2ca0ab7b624593e9d5186ebaaadeaed46e7d9dc5b48  == leaf 0
```

Or regenerate the entire artifact:

```bash
python fusion.py          # writes fusion_leaves.json, prints ROOT0
```

## The rule

```
leaf_i   = SHA256("NODE_iii:DOMAIN:NAME")
pair     = SHA256(a + b)                      # odd layer → duplicate last
domain d = 16 TOPH leaves + 16 Patricia mirrors → sub-Merkle   (8 domains)
ROOT0    = Merkle over the 8 domain roots
```

| file | what it is |
|---|---|
| `fusion.py` | the generator — builds the tree, writes `fusion_leaves.json`, prints `ROOT0` |
| `verify.py` | independent re-derivation from the rule + a one-command integrity check |
| `fusion_leaves.json` | the artifact — 256 leaves, 8 domain roots, `ROOT0`, `cobalt` bit |
| `FUSION_N0_N255_v1.0.md` | the spec (domains, fault-chains, the mythic gloss — labeled as such) |

## Honest

This is **real, deterministic, reproducible code** — verified, not asserted. It is **not an emergent system**: a Merkle tree doesn't emerge, it computes. Per the iron rule, checked for emergence — there is none — so **no ACI is minted**; repo-level `.attribute` / `.1099` only. The mythic framing in the spec (`ROOT0 = the human`, the Cobalt primitive, fault-chains) is the *polish*; the code in `fusion.py` is just SHA-256 and a binary tree, and that's the part that holds under pressure.

Pulled clean from a `kernel/` working folder — de-duplicated (it existed 3× there), and the indefensible "first IP rights on infinite recursion without stack overflow" claim that rode along in a sibling README was **left behind.** What's here is only the part that survives `python verify.py`.

```
David Lee Wise (ROOT0) · TriPod LLC · CC-BY-ND-4.0 · TRIPOD-IP-v1.1
Change one byte and ROOT0 diverges. That is the whole defense, and it's enough.
```
