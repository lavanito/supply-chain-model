"""
Sequential production chain with pay indexed to the consumer price index and an
upward-sloping supply of each stage's own inputs.

Replaces the earlier real-producer-wage specification (phi) with two parameters:

    lambda  in [0,1]   the share of the consumer basket whose price moves with
                       the restricted input, times the degree of indexation.
                       Only the product is identified, so it is one parameter.
    eps_s   in [0,inf] the elasticity of supply of stage-s own inputs.
                       eps = inf : supply perfectly elastic, employment adjusts.
                       eps = 0   : supply fixed, the wage adjusts and l_s = 0.

Supply curve:   l_s = eps_s (w_s - pi),  pi = lambda p_S
Unit cost:      p_s = theta_s p_{s-1} + (1 - theta_s) w_s
Own input:      l_s - y_s     =  theta_s alpha_s
Intermediate:   y_{s-1} - y_s = -(1 - theta_s) alpha_s
with alpha_s = sigma_s r_s and r_s = p_{s-1} - w_s.
Household is stage S+1 with y_{S+1} = 0 and w_{S+1} = 0, giving y_S = -eta p_S
and eta = sigma_{S+1}(1 - theta_{S+1}).

WHAT SURVIVES FROM THE PHI VERSION

1. The employment recursion is untouched and holds for ANY wage rule, because it
   uses only the first-order conditions and the unit-cost identity:

       E_{S+1} = theta_{S+1} alpha_{S+1},
       E_k     = E_{k+1} + theta_k alpha_k - alpha_{k+1}.

2. Prices no longer work forwards, because w_s depends on the final price. But when
   supply is perfectly elastic the whole price path is still closed form:

       p_s = Omega(0->s) p_0 + lambda p_S (1 - Omega(0->s))
       p_S = Omega(0->S) p_0 / [1 - lambda (1 - Omega(0->S))]

   Each stage's price is a cost-share weighted average of the restricted input's
   price and the consumer price index. The effective cumulative share is

       Omega~(0->S) = Omega(0->S) / [1 - lambda(1 - Omega(0->S))]  >=  Omega(0->S).

3. The last producing stage has its own closed form at any supply elasticity:

       E_S = p_S (1 - theta_{S+1})(sigma_S - sigma_{S+1}) eps_S / (eps_S + sigma_S)

   so employment at the last stage rises exactly when sigma_S > sigma_{S+1}:
   when the retailer substitutes away from what it buys faster than the household
   substitutes away from what the retailer sells. The budget share cancels because
   it both protects the wage and makes demand less elastic, by equal amounts.

Requires numpy only.
"""

import numpy as np


def _nu(eps):
    """Inverse of the supply elasticity, with the two limits handled."""
    e = np.asarray(eps, float)
    return np.where(np.isinf(e), 0.0, 1.0 / np.maximum(e, 1e-12))


def solve(theta, sigma, eps, theta_H, sigma_H, lam, shock=1.0):
    """
    theta, sigma, eps   : sequences of length S, most upstream stage first
    theta_H, sigma_H    : household budget share and elasticity of substitution
    lam                 : share of the consumer basket whose price moves
    shock               : d ln P_X on the restricted primary input

    Returns a dict of log changes: p (p[0] = shock), w, r, alpha, y, l, plus the
    household's alpha, eta, the consumer price index rise, and the quantity of the
    restricted input y0.
    """
    th = np.asarray(theta, float)
    sg = np.asarray(sigma, float)
    nu = _nu(eps)
    S = len(th)
    if not (len(sg) == len(nu) == S):
        raise ValueError("theta, sigma and eps must have equal length")
    if np.any((th <= 0) | (th >= 1)):
        raise ValueError("each theta must lie strictly between 0 and 1")
    if not (0.0 <= lam <= 1.0):
        raise ValueError("lambda must lie in [0,1]")

    eta = sigma_H * (1.0 - theta_H)

    # unknowns x = [p_1..p_S, w_1..w_S, y_1..y_S]
    n = 3 * S
    A = np.zeros((n, n))
    b = np.zeros(n)
    P = lambda s: s - 1
    W = lambda s: S + s - 1
    Y = lambda s: 2 * S + s - 1
    r = 0
    for s in range(1, S + 1):                                  # unit cost
        A[r, P(s)] = 1.0
        A[r, W(s)] = -(1.0 - th[s - 1])
        if s == 1:
            b[r] = th[0] * shock
        else:
            A[r, P(s - 1)] = -th[s - 1]
        r += 1
    for s in range(1, S + 1):                                  # wage rule
        k = s - 1                                              # l = y + sigma(p-w)
        A[r, W(s)] = 1.0 + nu[k] * sg[k]
        A[r, Y(s)] = -nu[k]
        A[r, P(s)] -= nu[k] * sg[k]
        A[r, P(S)] -= lam
        r += 1
    for s in range(2, S + 1):                                  # intermediate demand
        A[r, Y(s - 1)] = 1.0
        A[r, Y(s)] = -1.0
        A[r, P(s)] = -sg[s - 1]
        A[r, P(s - 1)] = sg[s - 1]
        r += 1
    A[r, Y(S)] = 1.0                                           # household demand
    A[r, P(S)] = eta

    x = np.linalg.solve(A, b)
    p_in, w, y = x[:S], x[S:2 * S], x[2 * S:]
    p = np.concatenate(([shock], p_in))
    rr = p[:-1] - w
    alpha = sg * rr
    l = y + th * alpha
    alpha_H = sigma_H * p[S]
    y0 = y[0] - (1.0 - th[0]) * alpha[0]
    return dict(p=p, w=w, r=rr, alpha=alpha, y=y, l=l, y0=y0,
                alpha_H=alpha_H, eta=eta, cpi=lam * p[S], pS=p[S])


def employment_recursion(theta, theta_H, alpha, alpha_H):
    """E_{S+1} = theta_H alpha_H ;  E_k = E_{k+1} + theta_k alpha_k - alpha_{k+1}.
    Holds for any wage rule."""
    th = list(theta)
    S = len(th)
    E = [0.0] * (S + 2)
    E[S + 1] = theta_H * alpha_H
    nxt = alpha_H
    for k in range(S, 0, -1):
        E[k] = E[k + 1] + th[k - 1] * alpha[k - 1] - nxt
        nxt = alpha[k - 1]
    return np.array(E[1:S + 1]), E[S + 1]


def prices_closed_form(theta, theta_H, lam, shock=1.0):
    """Perfectly elastic supply only.  p_s = Om(0->s) p_0 + lam p_S (1 - Om(0->s))."""
    th = np.asarray(theta, float)
    Om = np.concatenate(([1.0], np.cumprod(th)))
    OmS = Om[-1]
    pS = OmS * shock / (1.0 - lam * (1.0 - OmS))
    return Om[1:] * shock + lam * pS * (1.0 - Om[1:]), pS, OmS / (1.0 - lam * (1.0 - OmS))


def last_stage_closed_form(sigma_S, sigma_H, theta_H, eps_S, pS, lam):
    """The last producing stage, at any supply elasticity:

        E_S = p_S [ sigma_S (1 - lambda) - eta ] * eps_S / (eps_S + sigma_S),
        eta = sigma_H (1 - theta_H).

    So E_S > 0 exactly when sigma_S (1 - lambda) > eta.  When only this sector's
    price moves, lambda = theta_H, the budget share cancels from both sides and
    the condition collapses to sigma_S > sigma_H: the last stage gains employment
    when it substitutes away from what it buys faster than the household
    substitutes away from what it sells.
    """
    eta = sigma_H * (1.0 - theta_H)
    scale = 1.0 if np.isinf(eps_S) else eps_S / (eps_S + sigma_S)
    return pS * (sigma_S * (1.0 - lam) - eta) * scale
