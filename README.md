# Supply restrictions: where employment falls, and why

[![verify](https://github.com/lavanito/supply-chain-model/actions/workflows/verify.yml/badge.svg)](https://github.com/lavanito/supply-chain-model/actions/workflows/verify.yml)

The model, tests and paper source behind

> Mahadeva, L. (2026). *Supply restrictions: where employment falls, and why.*
> Working note v1.0. DOI: [10.5281/zenodo.22836881](https://doi.org/10.5281/zenodo.22836881)

Lavan Mahadeva · ORCID [0009-0007-8976-6617](https://orcid.org/0009-0007-8976-6617)

| | |
|---|---|
| **Paper** | [doi.org/10.5281/zenodo.22836881](https://doi.org/10.5281/zenodo.22836881) |
| **Interactive version** | *link to the app, to be added* |
| **Blog post** | *link to the Substack post, to be added* |

## What the paper argues

Restrict the supply of one input at the top of a production chain and employment
falls at every stage of the chain, not only at the stage the restriction applies
to. In percentage terms it falls most at that stage and less at each stage
further downstream. The more closely pay follows the cost of living, the deeper
the losses and the more evenly they spread. At full indexation every stage loses
the same amount and no stage substitutes at all.

The model has `S` producing stages and a household. The cost share, the
elasticity of substitution and the elasticity of supply of own inputs are all
free to differ between stages, and the whole model reduces to `S` linear
equations in `S` unknowns. It is calibrated to the American H-2B seasonal visa
cap, using the randomised visa lottery studied by Clemens and Lewis (2026,
*American Economic Journal: Applied Economics* 18(3), 43–82,
[doi:10.1257/app.20250049](https://doi.org/10.1257/app.20250049)), and to the
USDA food dollar series.

## Why this repository exists

Every number printed in the paper is computed by code. None is typed in. Every
time this repository changes, GitHub runs four checks automatically, and the
badge above turns red if any of them fails:

1. **The Python model reproduces all 66 figures printed in the paper**, to the
   precision the paper prints them. `python/verify.py`
2. **The JavaScript port reproduces 38 of them independently.**
   `javascript/chainSolver.test.js`
3. **The two implementations agree** over 4,000 randomly generated chains, to
   within 1e-9; in practice the largest difference is about 1e-15.
   `python/crosscheck.py`
4. **The figure in the paper redraws** from the model. `python/fig_solve.py`

The JavaScript port exists so the model can run in a web browser. It was written
separately from the Python, with its own linear solver, so that agreement between
the two is evidence rather than repetition.

External facts — figures taken from published sources rather than produced by
the model — cannot be checked by code, so they are checked by hand. `fact-check.md`
lists all 23, the source checked against each, what was verified and what was
not, and every correction made while drafting.

## Contents

| Path | What it is |
|---|---|
| `python/chain_solver.py` | The model. numpy only. |
| `python/verify.py` | Recomputes every figure printed in the paper. 66 checks. Exits non-zero on any mismatch. |
| `python/crosscheck.py` | Compares the JavaScript port with the Python over 4,000 random chains. |
| `python/fig_solve.py` | Draws the figure in Section 4 of the paper. |
| `javascript/chainSolver.js` | The same model in JavaScript, no dependencies. The web app imports this file unchanged. |
| `javascript/chainSolver.test.js` | 38 checks against the published figures. |
| `paper/` | LaTeX source of the paper and its figure. |
| `fact-check.md` | Every external claim, its source, its status, and the corrections log. |
| `.github/workflows/verify.yml` | The automatic checks. |

## Running it yourself

You need Python 3.10 or later, and Node.js 18 or later for the JavaScript checks.

```
pip install -r requirements.txt
python python/verify.py        # 66 checks
npm test                       # 38 checks
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

s = c.solve([0.40, 0.60, 0.50],   # theta: cost share of the input each stage buys
            [0.15, 0.30, 0.45],   # sigma: elasticity of substitution at each stage
            [np.inf] * 3,         # eps: supply of each stage's own inputs, here perfectly elastic
            0.15, 0.50 / 0.85,    # theta_H, sigma_H: the household, giving eta = 0.5
            0.15,                 # lambda: how far pay follows the restricted input's price
            0.20)                 # a 20 percent rise in the restricted input's price
print(s['l'] * 100)               # [-2.21 -1.03 -0.32]  employment, percent
```

```javascript
import { solveChain } from './javascript/chainSolver.js';

const s = solveChain({ theta: [0.40, 0.60, 0.50], sigma: [0.15, 0.30, 0.45],
                       eps: [Infinity, Infinity, Infinity],
                       thetaH: 0.15, sigmaH: 0.5 / 0.85, lam: 0.15, shock: 0.20 });
console.log(s.l.map(v => (v * 100).toFixed(2)));   // [ '-2.21', '-1.03', '-0.32' ]
```

The stages run from the restricted input downstream: in the paper's calibration,
harvesting, processing and packing, and retail and food service.

## How to read the results

`l` is the proportional change in each stage's employment, as a fraction of that
stage's own employment. The model contains no employment levels, so it says
which stage loses the largest **percentage** of its jobs and does not say which
stage loses the largest **number** of workers. A stage with a smaller percentage
loss and a much larger workforce can lose more people.

`l` also covers equipment as well as workers: it is the change in each stage's
own input bundle. Reading it as headcount assumes the two move together.

## Limitations

- The elasticities of substitution are argued rather than estimated, and the sign
  of the employment change at each end of the chain turns on them.
- Abnormal profit is assumed zero or constant, which assumes away the bargaining
  and monopsony objections rather than answering them.
- The restricted input cannot be imported, stored or bought forward.
- The 20 percent rise in the price of seasonal labour is a guess.

Section 7 of the paper discusses each.

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
