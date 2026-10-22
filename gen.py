# WARNING: no at-most-one-colour clauses are imposed.
# Decoding the lowest true colour preserves sum-freeness but may violate
# forced frame colours. Check the decoded frame, or add pairwise AMO clauses.
# CNF for frame g at n = 537 (N = 538, Q = 151, d = 38), and decoding of a solver model.
#   python3 gen.py cnf [--nopal] [--nomid] > g.cnf     (--nopal: family F3, --nomid: family F4)
#   kissat --seed=1 g.cnf > g.out ; python3 gen.py decode g.out [--nopal]   -> word c(1)...c(537)
import sys
n, N, Q, d = 537, 538, 151, 38
f = lambda x: min(x, N - x)
nopal, nomid = '--nopal' in sys.argv, '--nomid' in sys.argv
pos = (lambda x: x) if nopal else f                    # palindromic: one variable set per fold
var = lambda x, k: 6 * (pos(x) - 1) + k                 # colour k in 1..6
xs = range(1, n + 1) if nopal else range(1, N // 2 + 1)

def clauses():
    for x in xs:
        yield [var(x, k) for k in range(1, 7)]          # at least one colour
    for x in range(1, n + 1):                           # no monochromatic x + y = z (mod N if nopal)
        for y in range(x, n + 1):
            z = x + y if x + y <= n else (x + y - N if nopal else 0)
            if z >= 1:
                for k in range(1, 7):
                    yield [-var(x, k), -var(y, k), -var(z, k)]
    for x in range(1, n + 1):                           # frame g, stated on f(x)
        fx = f(x)
        for j in (1, 2, 3, 4):
            if fx < j: yield [-var(x, j)]
        if fx < d or Q - d < fx < Q: yield [-var(x, 5)]
        if fx in (d, N - 2 * Q): yield [var(x, 5)]
        if fx < Q: yield [-var(x, 6)]
        if fx == Q or (fx > N - 2 * Q and not nomid): yield [var(x, 6)]

if sys.argv[1] == 'cnf':
    cl = sorted({tuple(sorted(c)) for c in clauses()})
    print('p cnf %d %d' % (6 * max(xs), len(cl)))
    for c in cl: print(' '.join(map(str, c)), 0)
else:
    true = {int(t) for l in open(sys.argv[2]) if l.startswith('v') for t in l.split()[1:] if int(t) > 0}
    print(''.join(str(next(k for k in range(1, 7) if var(x, k) in true)) for x in range(1, n + 1)))
