"""
Reproduce every number printed in

    Mahadeva, L. (2026), "Supply restrictions: where employment falls, and why",
    working note v1.1

from chain_solver.py and check it against the text. Exits non-zero on any
mismatch. Requires numpy only.

    python verify.py
"""
import numpy as np
import chain_solver as c

TOL = 5e-3          # the note prints two decimals, so 0.005 is the rounding bound
FAILS = []

def check(label, got, want, tol=TOL):
    got, want = np.atleast_1d(np.asarray(got, float)), np.atleast_1d(np.asarray(want, float))
    ok = got.shape == want.shape and np.all(np.abs(got - want) <= tol)
    print(f"  {'ok ' if ok else 'FAIL'}  {label:58s} {np.round(got,4)}")
    if not ok:
        FAILS.append((label, got.tolist(), want.tolist()))

# ---- the calibration of Section 5 ------------------------------------------
TH    = [0.390, 0.217, 0.544]
SG    = [0.15, 0.30, 0.45]
THH   = 0.15
ETA   = 0.24                 # measured: ERS TB-1929, United States
SGH   = ETA / (1 - THH)      # 0.282353, printed as 0.282
LAM   = 0.0
SHOCK = 0.20

s = c.solve(TH, SG, [np.inf]*3, THH, SGH, LAM, SHOCK)

print("\nSection 5, the calibration table")
check("theta_1, theta_2, theta_3",        TH,            [0.390, 0.217, 0.544], 5e-4)
check("farm gate, Omega 1->3 = th2*th3",  TH[1]*TH[2],   0.118, 5e-4)
check("Omega 0->3, the restricted input", float(np.prod(TH)), 0.046, 5e-4)
check("sigma_4 = eta / (1 - theta_4)",    SGH,           0.282, 5e-4)
check("eta = sigma_4 (1 - theta_4)",      s['eta'],      0.24,  5e-4)

print("\nSection 5, the food dollar the calibration implies")
fd = [float(np.prod(TH)), (1-TH[0])*TH[1]*TH[2], (1-TH[1])*TH[2], 1-TH[2]]
check("restricted input, other farm, middle, retail", np.array(fd)*100,
                                                 [4.6, 7.2, 42.6, 45.6], 5e-2)
check("the four shares sum to one",       sum(fd), 1.0, 1e-12)

print("\nSection 4.3, the example: A is lower triangular with a unit diagonal")
d  = 0.0            # lambda = 0 and eps infinite, so d_s = sigma_hat = 0
A  = np.array([[1.0 if j == i else (1 - TH[j]) if j < i else 0.0
                for j in range(3)] for i in range(3)])
check("A row 1",                    A[0], [1.000, 0.000, 0.000], 5e-4)
check("A row 2",                    A[1], [0.610, 1.000, 0.000], 5e-4)
check("A row 3",                    A[2], [0.610, 0.783, 1.000], 5e-4)
check("r = A^-1 p_0 1",             np.linalg.solve(A, np.full(3, SHOCK)),
                                          [0.2000, 0.0780, 0.0169], 5e-5)
check("r from the full solver",     s['r'], [0.2000, 0.0780, 0.0169], 5e-5)
check("r_s equals the price entering stage s", s['r'][1:], s['p'][1:3], 1e-12)
check("prices entering, p_0 p_1 p_2 %", s['p'][:3]*100, [20.00, 7.80, 1.69])

print("\nSection 5.1, prices")
check("Omega 0->s",                 np.cumprod(TH), [0.3900, 0.0846, 0.0460], 5e-5)
check("price rise at each stage %", s['p']*100, [20.00, 7.80, 1.69, 0.92])
check("cost of living %",           THH*s['pS']*100, 0.14)
check("nominal pay %",              s['w']*100, [0.00, 0.00, 0.00])
check("real pay %",                 s['w']*100 - THH*s['pS']*100, [-0.14, -0.14, -0.14])
check("share of the rise reaching the shop", s['pS']/SHOCK, 0.046, 5e-4)
check("share absorbed along the chain %", (1 - s['pS']/SHOCK)*100, 95.4, 5e-2)

print("\nSection 5.2, output and employment")
al = s['alpha']
check("shift in input mix alpha %",  al*100,  [3.00, 2.34, 0.76])
check("household alpha %",           s['alpha_H']*100, 0.26)
check("kept by the stage, theta*alpha %", np.array(TH)*al*100, [1.17, 0.51, 0.41])
check("household kept %",            THH*s['alpha_H']*100, 0.04)
down = [-sum((1-TH[j])*al[j] for j in range(k+1, 3))*100 for k in range(3)]
check("output falls: stages downstream %", down, [-2.18, -0.35, 0.00])
check("output falls: households %",  -s['eta']*s['pS']*100, -0.22)
check("output %",                    s['y']*100,  [-2.40, -0.57, -0.22])
check("EMPLOYMENT %",                s['l']*100,  [-1.23, -0.06, 0.19])
E, EH = c.employment_recursion(TH, THH, al, s['alpha_H'])
check("employment via the recursion %", E*100,    [-1.23, -0.06, 0.19])
check("household entry l_4 %",       EH*100, 0.04)
three = [TH[k]*al[k] - sum((1-TH[j])*al[j] for j in range(k+1,3)) - s['eta']*s['pS']
         for k in range(3)]
check("employment via the three terms %", np.array(three)*100, [-1.23, -0.06, 0.19])
check("own inputs per unit, the printed range %", [al[2]*TH[2]*100, al[0]*TH[0]*100],
                                                  [0.41, 1.17])

print("\nSection 5.2, the last stage is the close call")
check("sigma_3 against eta",         [SG[2], s['eta']], [0.45, 0.24], 5e-3)
check("l_S closed form %",           c.last_stage_closed_form(SG[2], SGH, THH, np.inf, s['pS'], LAM)*100, 0.19)
for s3, want in ((0.15, -0.08), (0.24, 0.00), (0.45, 0.19), (0.80, 0.52)):
    r = c.solve(TH, SG[:2]+[s3], [np.inf]*3, THH, SGH, LAM, SHOCK)
    check(f"retail at sigma_S = {s3}", r['l'][2]*100, want)
r80 = c.solve(TH, SG[:2]+[0.80], [np.inf]*3, THH, SGH, LAM, SHOCK)
check("upstream at sigma_S = 0.80 %", r80['l'][:2]*100, [-1.50, -0.33])

print("\nSection 5.4, the range of the supply elasticity")
EPS = [(np.inf, 0.92, [ 0.00,  0.00, 0.00], [-1.23, -0.06, 0.19]),
       (5.0,    0.92, [-0.23, -0.01, 0.04], [-1.17, -0.05, 0.18]),
       (2.0,    0.91, [-0.54, -0.02, 0.08], [-1.09, -0.04, 0.16]),
       (1.0,    0.90, [-0.98, -0.03, 0.13], [-0.98, -0.03, 0.13]),
       (0.5,    0.87, [-1.62, -0.04, 0.19], [-0.81, -0.02, 0.10]),
       (0.2,    0.83, [-2.70, -0.04, 0.27], [-0.54, -0.01, 0.05]),
       (0.0,    0.72, [-4.87, -0.02, 0.33], [ 0.00,  0.00, 0.00])]
for e, pS, w, l in EPS:
    r = c.solve(TH, SG, [e]*3, THH, SGH, LAM, SHOCK)
    check(f"eps = {e}: retail price, factor prices, employment %",
          np.concatenate(([r['pS']*100], r['w']*100, r['l']*100)),
          np.concatenate(([pS], w, l)))

print("\nSection 6, the objections")
def bisect(f, lo, hi, n=200):
    for _ in range(n):
        mid = 0.5*(lo+hi)
        if f(lo)*f(mid) <= 0: hi = mid
        else: lo = mid
    return 0.5*(lo+hi)

f1 = lambda x: c.solve(TH, [x]+SG[1:], [np.inf]*3, THH, SGH, LAM, SHOCK)['l'][0]
check("harvesting break-even sigma_1", bisect(f1, 0.01, 3.0), 0.308, 5e-4)
hi = c.solve(TH, [0.85]*3, [np.inf]*3, THH, SGH, LAM, SHOCK)
check("every stage at sigma = 0.85 %", hi['l']*100, [0.56, 0.56, 0.56])
check("restricted share at the all-farm labour share, cents",
      0.13*TH[1]*TH[2]*100, 1.5, 5e-2)

print("\nSection 6, the quantity of the restricted input")
el = -s['y0']/SHOCK
check("elasticity of demand for seasonal farm labour", el, 0.21, 5e-3)
check("fall in the quantity of X, percent",           -s['y0']*100, 4.23, 5e-3)
for cut, want in ((0.05, 23.6), (0.10, 47.3), (0.20, 94.6)):
    g = lambda x: -c.solve(TH, SG, [np.inf]*3, THH, SGH, LAM, x)['y0'] - cut
    check(f"price rise for a {int(cut*100)} percent cut, percent",
          bisect(g, 0.001, 8.0)*100, want, 0.05)

print("\nSection 5.4 and the conclusion, fixed supply")
fx = c.solve(TH, SG, [0, 0, 0], THH, SGH, LAM, SHOCK)
check("employment %",            fx['l']*100, [0.00, 0.00, 0.00])
check("factor prices %",         fx['w']*100, [-4.87, -0.02, 0.33])
check("output %",                fx['y']*100, [-1.45, -0.32, -0.17])
check("cost of living %",        THH*fx['pS']*100, 0.11)
check("real factor prices %",    fx['w']*100 - THH*fx['pS']*100, [-4.97, -0.12, 0.23])

print("\nConclusion, percentages versus numbers of workers")
l = s['l']*100
check("retail size that offsets both upstream losses",
      (-l[0]-l[1])/l[2], 6.7, 0.05)

print()
if FAILS:
    print(f"{len(FAILS)} MISMATCH(ES):")
    for lab, got, want in FAILS:
        print(f"   {lab}: got {got} want {want}")
    raise SystemExit(1)
print("All numbers printed in the note reproduce from chain_solver.py.")
