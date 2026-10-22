# The sixth Schur number is at least 537

**Authors:** Zhiyang Chen, Ligeng Zhu, and Fan Long.

This repository contains the explicit certificates and code for the paper
**The sixth Schur number is at least 537**.

The main certificate partitions the integers 1 through 537 into six sum-free
sets. No set contains `x`, `y`, and `x+y`, including the case `x=y`.
This gives **S(6) >= 537** under the maximum-feasible-interval convention.

## Paper and full results

- [Paper PDF](paper/main.pdf), with one complete explicit partition.
- [LaTeX source](paper/main.tex) and [partition table](paper/partition_blocks.tex).
- [Supplementary PDF](supplement/partitions.pdf), with all 131 partitions.
- [Complete machine-readable list](solutions537.txt).
- [Main certificate](certificate.col).
- [Eight-color certificate on 1 through 5372](data/S8_n5372.txt).
- [Machine-readable result summary](results.json).

The 131 retained partitions fall into families of sizes 107, 14, 5, 4, and 1.
No two are equivalent under color renaming and multiplication by a unit modulo
538. This is a collection found by the search, not an enumeration of all possible
six-color partitions of 1 through 537.

## Verify the results

Use Python 3 and its standard library. From the repository root, run:

```sh
python3 check.py
```

The checker validates the main certificate, all 131 partitions, their modular
sum-free property, inequivalence, the reported family properties, and the
explicit eight-color certificate. A successful run ends with `all checks passed`.
It uses assertions and rejects Python's `-O` mode.
The output from a successful run is saved in [verification.txt](verification.txt).

`solutions537.txt` has one record per line: an identifier, followed by 537
color digits numbered 1 through 6. Colors appear in the order of their first
uses. Lines beginning with `#` are comments.
`certificate.col` uses the original project format: the header `537 6`, followed
by 537 color codes numbered 0 through 5.
`data/S8_n5372.txt` is a word of 5372 digits numbered 1 through 8.

## Reproduce a search

With Kissat installed, run from the repository root:

```sh
python3 gen.py cnf > g.cnf
kissat --seed=1 g.cnf > g.out
python3 gen.py decode g.out
```

The successful frame uses `N=538`, `Q=151`, and `d=38`.
The generator supports `--nopal` to remove reflection symmetry and `--nomid`
to remove the rule that forces color 6 on the middle interval. Pass `--nopal`
to both generation and decoding when using that mode. Search times and the
returned coloring can vary.

### Decoder caveat

The historical `gen.py` does not impose at-most-one-color clauses. A satisfying
model can therefore assign more than one true color to a position. The decoder
selects the smallest true color. This preserves ordinary sum-freeness, but may
discard a color required by a positive unit clause and violate the frame rules.

For example, a model satisfying every generated clause can decode positions
237 and 301 as color 1, although frame g requires color 6 there. The supplied
certificates have been checked separately; this caveat does not invalidate them.

Run this demonstration without a SAT solver:

```sh
python3 decoder_caveat.py
```

To require the frame after decoding, add pairwise at-most-one-color clauses at
each position, or select a required color first and then check the decoded frame.
The historical generator is retained with an explanatory comment. Its algorithm
has not been changed. The demonstration output is in
[decoder_caveat.json](decoder_caveat.json).

## Derived bounds

The paper derives the following bounds from published constructions:

| Quantity | Lower bound | Evidence here |
|---|---:|---|
| S(6) | 537 | Explicit six-color certificate |
| S(8) | 5372 | Explicit eight-color certificate |
| S(11) | 204208 | Published recurrence applied to S(6) >= 537 |
| S(13) | 2042082 | Published recurrence applied to the S(11) bound |
| R_6(3) | 539 | Difference coloring of the edges of K_538 |

The references and recurrence details are in the paper. No exact value for S(6)
or impossibility result at 538 is claimed.

## Build the documents

Run pdfLaTeX twice in each document directory:

```sh
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ../supplement
pdflatex -interaction=nonstopmode -halt-on-error partitions.tex
pdflatex -interaction=nonstopmode -halt-on-error partitions.tex
```

File SHA-256 digests are recorded in [SHA256SUMS](SHA256SUMS).
