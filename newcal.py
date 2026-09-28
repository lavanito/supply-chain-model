"""Every quantity the recalibrated note prints. Run: python newcal.py"""
import numpy as np, chain_solver as c

TH  = [0.39, 0.217, 0.544]
SG  = [0.15, 0.30, 0.45]
THH = 0.15
ETA = 0.24
SGH = ETA / (1 - THH)
LAM = 0.0
SHOCK = 0.20

def dump(tag, eps, lam=LAM, th=TH, sg=SG, sgh=SGH, shock=SHOCK):
    s = c.solve(th, sg, eps, THH, sgh, lam, shock)
    p, w, l, y, al = s['p']*100, s['w']*100, s['l']*100, s['y']*100, s['alpha']*100
    col = THH * p[-1]
    print(f"--- {tag}")
    print(f"  Omega 0->s        {np.round(np.cumprod(th),5)}")
    print(f"  r                 {np.round(s['r']*100,4)}")
    print(f"  p (p0..pS)        {np.round(p,4)}")
    print(f"  w                 {np.round(w,4)}")
    print(f"  alpha             {np.round(al,4)}   alpha_H {s['alpha_H']*100:.4f}")
    print(f"  theta*alpha       {np.round(np.array(th)*al,4)}   theta_H*alpha_H {THH*s['alpha_H']*100:.4f}")
    print(f"  y                 {np.round(y,4)}")
    print(f"  l                 {np.round(l,4)}")
    print(f"  cost of living    {col:.4f}      real pay {np.round(w-col,4)}")
    print(f"  y0 (restricted)   {s['y0']*100:.4f}   elasticity {-s['y0']/shock:.4f}")
    print(f"  eta               {s['eta']:.4f}")
    down = [-sum((1-th[j])*al[j] for j in range(k+1, 3)) for k in range(3)]
    print(f"  downstream term   {np.round(down,4)}")
    print(f"  household term    {-s['eta']*s['pS']*100:.4f}")
    print()
    return s

print(f"sigma_H = eta/(1-theta_H) = {SGH:.6f}\n")
base  = dump("BASE: eps = infinity, lambda = 0", [np.inf]*3)
fixed = dump("FIXED SUPPLY: eps = 0", [0, 0, 0])

print("--- Section 5.4 range over eps")
for e in [np.inf, 5.0, 2.0, 1.0, 0.5, 0.2, 0.0]:
    s = c.solve(TH, SG, [e]*3, THH, SGH, LAM, SHOCK)
    print(f"  eps={e:>5}  pS {s['pS']*100:7.4f}  w {np.round(s['w']*100,4)}  l {np.round(s['l']*100,4)}")

print("\n--- last stage: sign of l_S turns on sigma_3 against eta")
for s3 in [0.15, 0.24, 0.30, 0.45, 0.60, 0.80]:
    s = c.solve(TH, SG[:2]+[s3], [np.inf]*3, THH, SGH, LAM, SHOCK)
    print(f"  sigma_3={s3:4.2f}  l {np.round(s['l']*100,4)}")

print("\n--- harvesting: sign turns on sigma_1")
from scipy.optimize import brentq
f = lambda x: c.solve(TH, [x]+SG[1:], [np.inf]*3, THH, SGH, LAM, SHOCK)['l'][0]
print(f"  break-even sigma_1 = {brentq(f, 0.01, 3.0):.4f}")

print("\n--- the quantity of the restricted input")
el = -base['y0']/SHOCK
print(f"  elasticity of demand for seasonal labour {el:.4f}")
print(f"  a 20 percent price rise is a {-base['y0']*100:.4f} percent cut in quantity")
for q in (0.05, 0.10, 0.20):
    sh = brentq(lambda x: -c.solve(TH, SG, [np.inf]*3, THH, SGH, LAM, x)['y0'] - q, 0.001, 8.0)
    r = c.solve(TH, SG, [np.inf]*3, THH, SGH, LAM, sh)
    print(f"  a {q*100:4.1f} percent cut needs +{sh*100:6.2f} percent   l {np.round(r['l']*100,3)}   col {THH*r['pS']*100:.4f}")

print("\n--- the food dollar implied")
Om = float(np.prod(TH))
print(f"  restricted input      {Om:.4f}")
print(f"  other farm inputs     {(1-TH[0])*TH[1]*TH[2]:.4f}")
print(f"  processing own        {(1-TH[1])*TH[2]:.4f}")
print(f"  retail own            {1-TH[2]:.4f}")
print(f"  sum                   {Om+(1-TH[0])*TH[1]*TH[2]+(1-TH[1])*TH[2]+(1-TH[2]):.4f}")
print(f"  farm gate theta2*theta3 {TH[1]*TH[2]:.4f}")
