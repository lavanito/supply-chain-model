# Supply restrictions: where employment falls, and why

[![verify](https://github.com/lavanito/supply-chain-model/actions/workflows/verify.yml/badge.svg)](https://github.com/lavanito/supply-chain-model/actions/workflows/verify.yml)

The model, tests and paper source behind

> Mahadeva, L. (2026). *Supply restrictions: where employment falls, and why.*
> Working note v1.1. DOI: [10.5281/zenodo.23019960](https://doi.org/10.5281/zenodo.23019960)

Lavan Mahadeva · ORCID [0009-0007-8976-6617](https://orcid.org/0009-0007-8976-6617)

| | |
|---|---|
| **Paper, this version** | [doi.org/10.5281/zenodo.23019960](https://doi.org/10.5281/zenodo.23019960) |
| **Paper, all versions** | [doi.org/10.5281/zenodo.22836880](https://doi.org/10.5281/zenodo.22836880) |
| **Interactive version** | [supplyrestrictions.lavanito.com](https://supplyrestrictions.lavanito.com) |
| **Blog post** | *link to the Substack post, to be added* |

## What the paper argues

Restrict the supply of one input at the top of a production chain and **output falls
at every stage of the chain**, not only at the stage the restriction applies to.
Employment falls at the stages nearest the restriction. At the far end of the chain it
can rise, and does on this calibration, because the last producing stage has no
producing customer cutting its purchases — it carries only the fall in household
demand, and against that it has its own switch away from the input that has become
dearer. The last stage gains employment whenever its own elasticity of substitution
exceeds the price elasticity of final demand.

The model has `S` producing stages and a household. The cost share, the elasticity of
substitution and the elasticity of supply of own inputs are all free to differ between
stages, and the whole model reduces to `S` linear equations in `S` unknowns.

It is calibrated to the **USDA food dollar** and to a proposed cap on the American
**H-2A** agricultural visa (H.R. 7541, introduced February 2026), using the behaviour
measured in the randomised **H-2B** visa lottery studied by Clemens and Lewis (2026,
*American Economic Journal: Applied Economics* 18(3), 43–82,
[doi:10.1257/app.20250049](https://doi.org/10.1257/app.20250049)). H-2A has never been
capped, so there is no experiment on it; the paper says plainly that it borrows
behaviour from one programme and cost shares from a chain the other supplies.

## Why this repository exists

Every number printed in the paper is computed by code. None is typed in. Every time
this repository changes, GitHub runs four checks automatically, and the badge above
turns red if any of them fails:

1. **The Python model reproduces all 61 figures printed in the paper**, to the
   precision the paper prints them. `python/verify.py`
2. **The JavaScript port reproduces 41 of them independently.**
   `javascript/chainSolver.test.js`
3. **The two implementations agree** over 4,000 randomly generated chains, to
   within 1e-9; in practice the largest difference is about 1e-15.
   `python/crosscheck.py`
4. **The figure in the paper redraws** from the model. `python/fig_solve.py`

The JavaScript port exists so the model can run in a web browser. It was written
separately from the Python, with its own linear solver, so that agreement between
the two is evidence rather than repetition.

External facts — figures taken from published sources rather than produced by the
model — cannot be checked by code, so they are checked by hand. `fact-check.md`
lists them all, the source checked against each, what was verified and what was not,
and every correction made while drafting.

## Contents

| Path | What it is |
|---|---|
| `python/chain_solver.py` | The model. numpy only. |
| `python/verify.py` | Recomputes every figure printed in the paper. 61 checks. Exits non-zero on any mismatch. |
| `python/newcal.py` | Prints every quantity the paper reports, in one pass, without the checks. |
| `python/crosscheck.py` | Compares the JavaScript port with the Python over 4,000 random chains. |
| `python/fig_solve.py` | Draws the figure in Section 4 of the paper. |
| `javascript/chainSolver.js` | The same model in JavaScript, no dependencies. The web app imports this file unchanged. |
| `javascript/chainSolver.test.js` | 41 checks against the published figures. |
| `paper/` | LaTeX source of the paper and its figure. |
| `fact-check.md` | Every external claim, its source, its status, and the corrections log. |
| `.github/workflows/verify.yml` | The automatic checks. |

## Running it yourself

You need Python 3.10 or later, and Node.js 18 or later for the JavaScript checks.

```
pip install -r requirements.txt
python python/verify.py        # 61 checks
npm test                       # 41 checks
python python/crosscheck.py    # Python against JavaScript
```

Each prints `ok` against every figure and ends with a single line saying whether
everything reproduced.

To compile the paper, run `pdflatex supply-restrictions-employment.tex` three
times from inside `paper/`.

## Using the model

```python
import numpy as np
import chain_solver as c          # run from inside python/

s = c.solve([0.390, 0.217, 0.544],  # theta: cost share of the input each stage buys
            [0.15, 0.30, 0.45],     # sigma: elasticity of substitution at each stage
            [np.inf] * 3,           # eps: supply of each stage's own inputs, here perfectly elastic
            0.15, 0.24 / 0.85,      # theta_H, sigma_H: the household, giving eta = 0.24
            0.0,                    # lambda: how far pay follows the restricted input's price
            0.20)                   # a 20 percent rise in the restricted input's price
print(s['l'] * 100)                 # [-1.23 -0.06  0.19]  employment, percent
print(s['y'] * 100)                 # [-2.40 -0.57 -0.22]  output, percent
```

```javascript
import { solveChain } from './javascript/chainSolver.js';

const s = solveChain({ theta: [0.390, 0.217, 0.544], sigma: [0.15, 0.30, 0.45],
                       eps: [Infinity, Infinity, Infinity],
                       thetaH: 0.15, sigmaH: 0.24 / 0.85, lam: 0.0, shock: 0.20 });
console.log(s.l.map(v => (v * 100).toFixed(2)));   // [ '-1.23', '-0.06', '0.19' ]
```

The stages run from the restricted input downstream: in the paper's calibration,
harvesting, processing and packing, and retail and food service.

## The calibration

| | Value | Where it comes from |
|---|---|---|
| `theta` | 0.390, 0.217, 0.544 | The last two multiply to the USDA farm share of the food dollar, 0.118. The first is the labour share of total cash expenses on specialty crop farms. All three multiply to 0.046, seasonal farm labour's share of the food dollar. |
| `sigma` | 0.15, 0.30, 0.45 | Argued, not estimated. Short-run values, well below published estimates of the same parameter. |
| `eps` | perfectly elastic | Employment takes the whole adjustment. The paper varies this down to fixed supply, where pay adjusts instead. |
| `lambda` | 0 | Pay does not follow the cost of living. |
| `eta` | 0.24 | Measured. The compensated own-price elasticity of aggregate US food demand, USDA ERS Technical Bulletin 1929. |
| shock | +20% | A guess. The model maps it to a quantity: a 4.23 percent cut in the seasonal labour the chain wants. |

The implied food dollar is 4.6 cents to seasonal farm labour, 7.2 to the farm's other
inputs, 42.6 to processing and everything between it and the shop, and 45.6 to retail
and food service. That it sums to 100 is one of the 61 checks.

## How to read the results

`l` is the proportional change in each stage's employment, as a fraction of that
stage's own employment. The model contains no employment levels, so it says which
stage loses the largest **percentage** of its jobs and does not say which stage loses
the largest **number** of workers, nor whether the chain gains or loses jobs overall.

`l` also covers equipment as well as workers: it is the change in each stage's own
input bundle. Reading it as headcount assumes the two move together.

## Limitations

- The elasticities of substitution are argued rather than estimated, and the sign of
  the employment change at each end of the chain turns on them. Harvesting loses
  employment only while `sigma_1` is below 0.308; retail gains only while `sigma_3` is
  above `eta`. Atalay (2017) estimates this parameter at 0.84 to 0.88 across thirty US
  industries, and at 0.85 everywhere every stage in this chain would gain employment.
  The defence is the horizon: Boehm, Flaaen and Pandalai-Nayar (2019) find that over
  months firms substitute between inputs barely at all.
- The supply of each stage's own inputs is perfectly elastic in the main case, which
  puts the whole adjustment into employment. Section 5.3 varies it.
- Abnormal profit is assumed zero or constant, which assumes away the bargaining and
  monopsony objections rather than answering them.
- The restricted input cannot be imported, stored or bought forward.
- The 20 percent rise in the price of seasonal labour is a guess.
- The cost shares come from a food chain; the behaviour comes from firms in the H-2B
  programme, which is non-agricultural.

Section 6 of the paper discusses each.

## How this was built

The model, the tests and the paper were written by me, with an AI assistant
(Claude) used for drafting, derivation checks and code. Every number it produced
is checked by the tests above rather than taken on trust. The interactive version
is a separate repository whose interface was built with Lovable; it imports
`javascript/chainSolver.js` from here unchanged.

## Citing

Cite the paper for the results and this repository for the code. `CITATION.cff`
gives both, and GitHub's "Cite this repository" button reads it.

## Licence

Code: MIT. The paper is licensed CC BY 4.0 on its Zenodo record.
