"""
Reproduce every number printed in

    Mahadeva, L. (2026), "Supply restrictions: where employment falls, and why",
    working note v1.0, DOI 10.5281/zenodo.22836881

from chain_solver.py and check it against the text. Exits non-zero on any
mismatch. Requires numpy only.

    python verify.py
"""
import numpy as np
import chain_solver as c

TOL = 5e-3          # the paper prints two decimals, so 0.005 is the rounding bound
FAILS = []

def check(label, got, want, tol=TOL):
    got, want = np.atleast_1d(np.asarray(got, float)), np.atleast_1d(np.asarray(want, float))
    ok = got.shape == want.shape and np.all(np.abs(got - want) <= tol)
    print(f"  {'ok ' if ok else 'FAIL'}  {label:54s} {np.round(got,4)}")
    if not ok:
        FAILS.append((label, got.tolist(), want.tolist()))

# ---- the calibration of Section 5 ------------------------------------------
TH   = [0.40, 0.60, 0.50]
SG   = [0.15, 0.30, 0.45]
THH  = 0.15
SGH  = 0.50 / 0.85          # gives eta = 0.5
LAM  = 0.15
SHOCK= 0.20

s = c.solve(TH, SG, [np.inf]*3, THH, SGH, LAM, SHOCK)

print("\nSection 4.3, the example: the 3x3 system")
d  = -LAM / (1 - LAM)
A  = np.array([[1 - TH[i]*d if j == i else (1 - TH[j]) if j < i else (1 - TH[j])*d
                for j in range(3)] for i in range(3)])
check("d_s",                        d,                          -0.1765)
check("A row 1",                    A[0],            [1.0706, -0.0706, -0.0882], 5e-5)
check("A row 2",                    A[1],            [0.6000,  1.1059, -0.0882], 5e-5)
check("A row 3",                    A[2],            [0.6000,  0.4000,  1.0882], 5e-5)
check("r = A^-1 p_0 1",             np.linalg.solve(A, np.full(3, SHOCK)),
                                                     [0.1959, 0.0783, 0.0470], 5e-5)
check("r from the full solver",     s['r'],          [0.1959, 0.0783, 0.0470], 5e-5)
check("prices arriving p_0,p_1,p_2", s['p'][:3]*100, [20.000, 8.249, 5.115], 5e-3)

print("\nSection 4.4, eta")
check("eta = sigma_H (1 - theta_H)", s['eta'], 0.5)

print("\nSection 5.1, prices")
check("price rise at each stage %", s['p']*100,  [20.00, 8.25, 5.12, 2.76])
check("cost of living %",           s['cpi']*100, 0.41)
check("factor prices %",            s['w']*100,  [0.41, 0.41, 0.41])
Om  = float(np.prod(TH))
_, _, Omt  = c.prices_closed_form(TH, THH, LAM, SHOCK)
_, pS0, Om0= c.prices_closed_form(TH, THH, 0.0, SHOCK)
check("Omega 0->s",                 np.cumprod(TH), [0.400, 0.240, 0.120], 5e-4)
check("cost share Omega",           Om,   0.120, 5e-4)
check("effective share Omega~",     Omt,  0.138, 5e-4)
check("ratio Omega~ / Omega",       Omt/Om, 1.15, 5e-3)
check("shelf price, no indexation %", pS0*100, 2.40)

print("\nSection 5.2, output and employment")
al = s['alpha']
check("shift in input mix alpha %",  al*100,  [2.94, 2.35, 2.12])
check("household alpha %",           s['alpha_H']*100, 1.63)
check("kept by the stage, theta*alpha %", np.array(TH)*al*100, [1.18, 1.41, 1.06])
check("household kept %",            THH*s['alpha_H']*100, 0.24)
down = [-sum((1-TH[j])*al[j] for j in range(k+1, 3))*100 for k in range(3)]
check("output falls: stages downstream %", down, [-2.00, -1.06, 0.00])
check("output falls: households %",  -s['eta']*s['pS']*100, -1.38)
check("output %",                    s['y']*100,  [-3.38, -2.44, -1.38])
check("EMPLOYMENT %",                s['l']*100,  [-2.21, -1.03, -0.32])
E, EH = c.employment_recursion(TH, THH, al, s['alpha_H'])
check("employment via the recursion %", E*100,    [-2.21, -1.03, -0.32])
check("household entry l_4 %",       EH*100, 0.24)
three = [TH[k]*al[k] - sum((1-TH[j])*al[j] for j in range(k+1,3)) - s['eta']*s['pS']
         for k in range(3)]
check("employment via the three terms %", np.array(three)*100, [-2.21, -1.03, -0.32])
check("harvesting / retail ratio (text: about seven times)", s['l'][0]/s['l'][2], 6.79, 0.02)

print("\nSection 5.2, retail is the close call")
check("sigma_3 against sigma_4",     [SG[2], SGH], [0.45, 0.59], 5e-3)
check("l_S closed form %",           c.last_stage_closed_form(SG[2], SGH, THH, np.inf, s['pS'], LAM)*100, -0.32)
for sgH, want in ((0.2, 0.59), (2.0, -3.64)):
    r = c.solve(TH, SG, [np.inf]*3, THH, sgH, THH, SHOCK)
    check(f"retail at sigma_(S+1) = {sgH}", r['l'][2]*100, want)
for thH, want in ((0.60, -0.28), (0.05, -0.33)):
    r = c.solve(TH, SG, [np.inf]*3, thH, SGH, thH, SHOCK)
    check(f"retail at theta_(S+1) = {thH}", r['l'][2]*100, want)
for s3, want in ((0.45, -0.32), (0.588, 0.00), (1.0, 0.97)):
    r = c.solve(TH, SG[:2]+[s3], [np.inf]*3, THH, SGH, THH, SHOCK)
    check(f"retail at sigma_S = {s3}", r['l'][2]*100, want)

print("\nSection 5.3, hospitality")
h = c.solve(TH, SG, [np.inf]*3, 0.05, 1.5/0.95, 0.05, SHOCK)
check("eta",                h['eta'], 1.5)
check("employment %",       h['l']*100, [-4.60, -3.41, -2.69])
check("shelf price %",      h['pS']*100, 2.51)

print("\nSection 5.4, the range of the supply elasticity")
EPS = [(np.inf, 2.76, [ 0.41,  0.41,  0.41], [-2.21, -1.03, -0.32]),
       (5.0,    2.60, [-0.02,  0.21,  0.33], [-2.06, -0.92, -0.28]),
       (2.0,    2.41, [-0.57, -0.04,  0.25], [-1.87, -0.80, -0.23]),
       (1.0,    2.18, [-1.30, -0.32,  0.15], [-1.63, -0.64, -0.18]),
       (0.5,    1.88, [-2.31, -0.64,  0.05], [-1.30, -0.46, -0.12]),
       (0.2,    1.49, [-3.83, -0.97, -0.05], [-0.81, -0.24, -0.05]),
       (0.0,    0.95, [-6.46, -1.16, -0.11], [ 0.00,  0.00,  0.00])]
for e, shelf, w, l in EPS:
    r = c.solve(TH, SG, [e]*3, THH, SGH, LAM, SHOCK)
    check(f"eps = {e}: shelf, factor prices, employment %",
          np.concatenate(([r['pS']*100], r['w']*100, r['l']*100)),
          np.concatenate(([shelf], w, l)))

print("\nSection 6, the input used everywhere")
LAMS = [(0.00, 0.120, 2.40,  0.00, [-2.04, -0.84, -0.12]),
        (0.15, 0.138, 2.76,  0.41, [-2.21, -1.03, -0.32]),
        (0.30, 0.163, 3.26,  0.98, [-2.43, -1.29, -0.60]),
        (0.50, 0.214, 4.29,  2.14, [-2.89, -1.82, -1.18]),
        (0.70, 0.313, 6.25,  4.38, [-3.78, -2.84, -2.28]),
        (0.90, 0.577, 11.54, 10.38,[-6.17, -5.60, -5.25])]
for lam, share, shelf, cpi, l in LAMS:
    r = c.solve(TH, SG, [np.inf]*3, THH, SGH, lam, SHOCK)
    _, _, om = c.prices_closed_form(TH, THH, lam, SHOCK)
    # lambda = 0.70 gives exactly 0.3125, which the note rounds up to 0.313,
    # so the bound here is a shade over half of the last printed digit.
    check(f"lambda = {lam:.2f}: effective share (3 dp)", om, share, 5.1e-4)
    check(f"lambda = {lam:.2f}: shelf, cost of living, employment %",
          np.concatenate(([r['pS']*100, r['cpi']*100], r['l']*100)),
          np.concatenate(([shelf, cpi], l)))
r90 = c.solve(TH, SG, [np.inf]*3, THH, SGH, 0.90, SHOCK)
check("spread across stages at lambda = 0.90, points",
      (r90['l'].max()-r90['l'].min())*100, 0.9, 0.05)
check("spread across stages at lambda = 0.15, points",
      (s['l'].max()-s['l'].min())*100, 1.9, 0.05)
check("effective share at lambda = 0.90, percent (conclusion says 58)",
      LAMS[-1][1]*100, 58, 0.4)

print("\nSection 7, the quantity of the restricted input")
check("elasticity of demand for seasonal labour", -s['y0']/SHOCK, 0.26, 5e-3)
check("fall in the quantity of X, percent",       -s['y0']*100,   5.1, 5e-2)
check("price rise needed for a 10 percent cut, percent",
      10.0/(-s['y0']/SHOCK), 39.0, 0.5)

print("\nConclusion, percentages versus numbers of workers")
check("break-even workforce ratio, retail vs harvesting",
      s['l'][0]/s['l'][2], 6.79, 5e-3)

print()
if FAILS:
    print(f"{len(FAILS)} MISMATCH(ES):")
    for lab, got, want in FAILS:
        print(f"   {lab}: got {got} want {want}")
    raise SystemExit(1)
print("All numbers printed in the note reproduce from chain_solver.py.")
