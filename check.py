# Checks the explicit certificates and the reported family properties.
# Python 3, standard library only. Run in this folder: python3 check.py
import sys
if not __debug__:
    raise SystemExit("Run without -O: this checker uses assertions")

N = 538
f = lambda x: min(x, N - x)

def sumfree(S):
    S = set(S)
    return not any(x + y in S for x in S for y in S)          # x = y included

def classes(c):
    return [{x for x in range(1, N) if c[x - 1] == k} for k in range(1, 7)]

def sumfree_mod(c):
    return all(not (c[x - 1] == c[y - 1] == c[(x + y) % N - 1])
               for x in range(1, N) for y in range(x, N) if (x + y) % N)

def renumber(c):   # colours 1..6 in the order of their least elements
    order = []
    for v in c:
        if v not in order:
            order.append(v)
    return [order.index(v) + 1 for v in c]

def in_frame_g(c, Q=151, d=38, middle=True):
    for x in range(1, N):
        fx, cx = f(x), c[x - 1]
        if any(fx < j and cx == j for j in (1, 2, 3, 4)): return False
        if (fx < d or Q - d < fx < Q) and cx == 5: return False
        if fx in (d, N - 2 * Q) and cx != 5: return False
        if fx < Q and cx == 6: return False
        if fx == Q and cx != 6: return False
        if middle and fx > N - 2 * Q and cx != 6: return False
    return True

def middle_gaps(c):   # values f(x) > N - 2Q that do not get colour 6
    return len({f(x) for x in range(1, N) if f(x) > N - 2 * 151 and c[x - 1] != 6})

A = {1, 5, 12, 15, 19, 21, 23, 25, 29, 32, 39, 43, 45, 49}
B = A | {151 - a for a in A} | {151 + a for a in A if a <= 29} | {151 - 56}
Cstar = {x for x in range(1, N) if f(x) in B}
assert len(B) == 38 and len(Cstar) == 76

# Theorem 1: the example partition (certificate.col: "537 6", then colours 0..5)
tok = open('certificate.col').read().split()
assert tok[:2] == ["537", "6"]
assert len(tok[2:]) == 537 and all(t in ("0", "1", "2", "3", "4", "5") for t in tok[2:])
ex = renumber([int(t) for t in tok[2:]])
assert len(ex) == 537 and all(sumfree(C) for C in classes(ex)) and sum(map(len, classes(ex))) == 537
print("Theorem 1: the example is a partition of [1,537] into 6 sum-free sets")

# Corollary: S(8) >= 10*537 + 2 = 5372, by the width-10 template of Bengone et al. (Table II)
T = {'F': ['B', 'A', 'P0', 'P0', 'B', 'A', 'A', 'B', 'P0', 'P0'],
     'M': ['P-1', 'B', 'P0', 'P0', 'B', 'A', 'A', 'B', 'P0', 'P0'],
     'L': ['P-1', 'B', 'P0', 'P0', 'B', 'A', 'A', 'B', 'P0', 'P0']}
h = []
for a in range(1, 538):
    for lab in T['F'] if a == 1 else T['L'] if a == 537 else T['M']:
        h.append(7 if lab == 'A' else 8 if lab == 'B' else ex[a + int(lab[1:]) - 1])
h += [7, 8]                                                   # tail (A, B)
assert len(h) == 5372
assert open('data/S8_n5372.txt').read().strip() == ''.join(map(str, h))
assert all(sumfree({x for x in range(1, 5373) if h[x - 1] == k}) for k in range(1, 9))
print("Corollary: partition of [1,5372] into 8 sum-free sets built and checked")

# Section 3: all partitions in solutions537.txt
sols = {}
for line in open('solutions537.txt'):
    if line.startswith('#') or not line.strip():
        continue
    pid, s = line.split()
    c = [int(ch) for ch in s]
    assert len(c) == 537 and set(c) == set(range(1, 7)) and c == renumber(c)
    assert all(sumfree(C) for C in classes(c)), pid
    assert sumfree_mod(c), pid
    sols[pid] = c
assert len(sols) == 131 and len({tuple(c) for c in sols.values()}) == 131
assert sols['F1.001'] == ex
print("131 distinct partitions, all sum-free and sum-free modulo 538")

# no partition is obtained from another by x -> r*x mod 538 (r a unit) and renumbering
from math import gcd
units = [r for r in range(1, N) if gcd(r, N) == 1]
canon = lambda c: min(tuple(renumber([c[(r * x) % N - 1] for x in range(1, N)])) for r in units)
assert len({canon(c) for c in sols.values()}) == 131
print("no two of them are related by x -> r*x mod 538 (r a unit, includes r = -1)")

def pal_defects(c):
    return sum(c[x - 1] != c[N - x - 1] for x in range(1, N)) // 2

starts = lambda c: sorted(min(C) for C in classes(c))
count = {}
for pid, c in sols.items():
    fam = pid.split('.')[0]
    count[fam] = count.get(fam, 0) + 1
    one = classes(c)[0]
    if fam == 'F5':
        img = renumber([c[(43 * x) % N - 1] for x in range(1, N)])
        assert starts(c) == [1, 2, 3, 4, 7, 16] and starts(img) == [1, 2, 3, 4, 38, 151]
        assert len(classes(img)[0] ^ Cstar) == 3 and pal_defects(img) == 5
        continue
    assert starts(c) == [1, 2, 3, 4, 38, 151], pid
    if fam == 'F1':
        assert pal_defects(c) == 0 and in_frame_g(c) and one == Cstar, pid
    if fam == 'F2':
        assert pal_defects(c) == 0 and in_frame_g(c) and len(one ^ Cstar) == 2, pid
    if fam == 'F3':
        assert 2 <= pal_defects(c) <= 12 and in_frame_g(c) and one == Cstar, pid
    if fam == 'F4':
        assert pal_defects(c) == 0 and in_frame_g(c, middle=False) and 1 <= middle_gaps(c) <= 13, pid
        assert 2 <= len(one ^ Cstar) <= 8, pid
assert count == {"F1": 107, "F2": 14, "F3": 5, "F4": 4, "F5": 1}
print("family sizes", dict(sorted(count.items())))
far = max(sum(a != b for a, b in zip(c, ex)) for p, c in sols.items() if not p.startswith('F5'))
assert far <= 75
print("largest number of positions in which a partition of F1-F4 differs from the example:", far)

print("all checks passed")
