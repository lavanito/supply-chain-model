"""Compare the JavaScript port against the Python solver over random chains."""
import json, os, subprocess, sys
import numpy as np, chain_solver as c

rng = np.random.default_rng(2026)
cases = []
for _ in range(4000):
    S = int(rng.integers(1, 6))                     # the app allows up to 5 stages
    cases.append(dict(
        theta=[float(v) for v in rng.uniform(.05,.95,S)],
        sigma=[float(v) for v in rng.uniform(0,3,S)],
        eps=[(float('inf') if rng.random()<.25 else float(v)) for v in rng.uniform(0,20,S)],
        thetaH=float(rng.uniform(.02,.6)), sigmaH=float(rng.uniform(0,3)),
        lam=float(rng.uniform(0,1)), shock=float(rng.uniform(.01,.5))))

JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'javascript', 'chainSolver.js')
JS_URL = 'file://' + os.path.abspath(JS)

js = subprocess.run(['node','--input-type=module','-e', """
import { solveChain } from '__JS__';
let raw=''; process.stdin.on('data',d=>raw+=d).on('end',()=>{
  const out = JSON.parse(raw).map(k=>{
    const q = {...k, eps: k.eps.map(v => v === null ? Infinity : v)};
    const s = solveChain(q);
    return {p:s.p, w:s.w, l:s.l, y:s.y, pS:s.pS, cpi:s.cpi, y0:s.y0};
  });
  process.stdout.write(JSON.stringify(out));
});""".replace('__JS__', JS_URL)], input=json.dumps([{**k,'eps':[None if np.isinf(e) else e for e in k['eps']]} for k in cases]),
  capture_output=True, text=True)
if js.returncode: sys.exit(js.stderr)
res = json.loads(js.stdout)

worst = {k: 0.0 for k in ('p','w','l','y','pS','cpi','y0')}
for k, j in zip(cases, res):
    py = c.solve(k['theta'], k['sigma'], k['eps'], k['thetaH'], k['sigmaH'], k['lam'], k['shock'])
    for f in ('p','w','l','y'):
        worst[f] = max(worst[f], float(np.abs(np.array(j[f]) - py[f]).max()))
    for f in ('pS','cpi','y0'):
        worst[f] = max(worst[f], abs(j[f] - py[f]))
print("JavaScript port vs the Python solver, 4,000 random chains, S = 1..5")
for f, v in worst.items():
    print(f"  {f:4s} max absolute difference {v:.3e}")
TOL = 1e-9
w = max(worst.values())
print(f"\nWORST OVERALL: {w:.3e}  (tolerance {TOL:.0e})")
if w > TOL:
    sys.exit("The JavaScript port and the Python solver disagree.")
print("The JavaScript port agrees with the Python solver.")
