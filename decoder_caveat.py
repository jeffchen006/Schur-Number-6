"""Reproduce the historical generator's frame-decoding caveat without a solver."""
import ast
import json
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parent
tree = ast.parse((root / "gen.py").read_text())
# Load definitions without executing the generator's final command-line block.
namespace = {"__name__": "generator_definitions"}
exec(compile(ast.Module(body=tree.body[:-1], type_ignores=[]), "gen.py", "exec"), namespace)
var = namespace["var"]
tokens = (root / "certificate.col").read_text().split()
colors = [int(t) + 1 for t in tokens[2:]]
true = {var(x, colors[x - 1]) for x in range(1, 538)}
true.add(var(237, 1))
clause_count = 0
for clause in namespace["clauses"]():
    clause_count += 1
    if not any(v in true if v > 0 else -v not in true for v in clause):
        raise SystemExit("The constructed model does not satisfy the generated formula")

with tempfile.TemporaryDirectory(prefix="schur537-decoder-") as directory:
    model = Path(directory) / "model.out"
    model.write_text("s SATISFIABLE\nv " + " ".join(map(str, sorted(true))) + " 0\n")
    result = subprocess.run([sys.executable, str(root / "gen.py"), "decode", str(model)],
                            check=True, capture_output=True, text=True)
decoded = [int(v) for v in result.stdout.strip()]
if len(decoded) != 537 or set(decoded) != set(range(1, 7)):
    raise SystemExit("Invalid decoded format")
if any(decoded[x - 1] == decoded[y - 1] == decoded[x + y - 1]
       for x in range(1, 538) for y in range(1, 538 - x)):
    raise SystemExit("The decoded coloring is not sum-free")
if decoded[236] != 1 or decoded[300] != 1:
    raise SystemExit("The expected frame violation was not reproduced")
print(json.dumps({"all_generated_clauses_satisfied": True,
                  "generated_clause_count": clause_count,
                  "decoded_partition_sum_free": True,
                  "decoded_color_at_237": decoded[236],
                  "decoded_color_at_301": decoded[300],
                  "frame_requires_color": 6,
                  "frame_violation_reproduced": True}, indent=2))
