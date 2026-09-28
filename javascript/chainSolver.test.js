/**
 * Self-test: reproduces the published figures from the working note
 *   Mahadeva (2026), DOI 10.5281/zenodo.23019960
 * Run with:  node chainSolver.test.js
 * Exits non-zero if any number moves.
 */
import { solveChain, employmentRecursion, lastStageClosedForm } from './chainSolver.js';

let fails = 0, checks = 0;
const pc = (x) => +(x * 100).toFixed(4);
// the note prints two decimals, so the bound is a shade over half the last digit
function eq(label, got, want, tol = 5.1e-3) {
  const g = Array.isArray(got) ? got : [got], w = Array.isArray(want) ? want : [want];
  const ok = g.length === w.length && g.every((v, i) => Math.abs(v - w[i]) <= tol);
  checks++; if (!ok) fails++;
  console.log(`  ${ok ? 'ok  ' : 'FAIL'} ${label.padEnd(46)} ${JSON.stringify(g.map(v => +v.toFixed(4)))}`);
}

const ETA = 0.24;
const BASE = { theta: [0.390, 0.217, 0.544], sigma: [0.15, 0.30, 0.45],
               eps: [Infinity, Infinity, Infinity],
               thetaH: 0.15, sigmaH: ETA / 0.85, lam: 0.0, shock: 0.20 };
// pay is not indexed, so the model's cpi is zero; the cost of living the note
// reports is the food share of the basket times the price households pay
const costOfLiving = (q) => pc(BASE.thetaH * q.pS);

console.log('\nThe calibration of Section 5');
const s = solveChain(BASE);
eq('eta',                          s.eta, 0.24, 5e-4);
eq('sigma_4 = eta / (1 - theta_4)', BASE.sigmaH, 0.282, 5e-4);
eq('cumulative cost shares',       s.Omega, [0.3900, 0.0846, 0.0460], 5e-5);
eq('farm gate, theta_2 theta_3',   BASE.theta[1] * BASE.theta[2], 0.118, 5e-4);
eq('effective share Omega~ equals Omega', s.OmegaTilde, 0.046, 5e-4);
eq('prices, percent',              s.p.map(pc), [20.00, 7.80, 1.69, 0.92]);
eq('cost of living, percent',      costOfLiving(s), 0.14);
eq('factor prices, percent',       s.w.map(pc), [0.00, 0.00, 0.00]);
eq('real factor prices, percent',  s.w.map((v, i) => pc(v) - costOfLiving(s)), [-0.14, -0.14, -0.14]);
eq('output, percent',              s.y.map(pc), [-2.40, -0.57, -0.22]);
eq('EMPLOYMENT, percent',          s.l.map(pc), [-1.23, -0.06, 0.19]);
eq('input mix alpha, percent',     s.alpha.map(pc), [3.00, 2.34, 0.76]);

console.log('\nThe food dollar the calibration implies');
const th = BASE.theta;
eq('restricted input, cents',      pc(th[0] * th[1] * th[2]), 4.6, 5e-2);
eq('other farm inputs, cents',     pc((1 - th[0]) * th[1] * th[2]), 7.2, 5e-2);
eq('processing and between, cents', pc((1 - th[1]) * th[2]), 42.6, 5e-2);
eq('retail and food service, cents', pc(1 - th[2]), 45.6, 5e-2);

console.log('\nThe three terms, and the recursion');
eq('employment per unit of output', s.terms.map(t => pc(t.own)), [1.17, 0.51, 0.41]);
eq('output lost: stages downstream', s.terms.map(t => pc(t.down)), [-2.18, -0.35, 0.00]);
eq('output lost: households',        s.terms.map(t => pc(t.household)), [-0.22, -0.22, -0.22]);
eq('three terms sum to employment',  s.terms.map(t => pc(t.total)), [-1.23, -0.06, 0.19]);
const rec = employmentRecursion(BASE.theta, BASE.thetaH, s.alpha, s.alphaH);
eq('recursion gives the same',       rec.stages.map(pc), [-1.23, -0.06, 0.19]);
eq('household entry l_4, percent',   pc(rec.household), 0.04);
eq('last stage closed form, percent',
   pc(lastStageClosedForm(BASE.sigma[2], BASE.sigmaH, BASE.thetaH, Infinity, s.pS, BASE.lam)), 0.19);

console.log('\nThe supply elasticity, Section 5.3');
for (const [e, retail, w, l] of [[Infinity, 0.92, [ 0.00,  0.00, 0.00], [-1.23, -0.06, 0.19]],
                                 [5,   0.92, [-0.23, -0.01, 0.04], [-1.17, -0.05, 0.18]],
                                 [2,   0.91, [-0.54, -0.02, 0.08], [-1.09, -0.04, 0.16]],
                                 [1,   0.90, [-0.98, -0.03, 0.13], [-0.98, -0.03, 0.13]],
                                 [0.5, 0.87, [-1.62, -0.04, 0.19], [-0.81, -0.02, 0.10]],
                                 [0.2, 0.83, [-2.70, -0.04, 0.27], [-0.54, -0.01, 0.05]],
                                 [0,   0.72, [-4.87, -0.02, 0.33], [ 0.00,  0.00, 0.00]]]) {
  const q = solveChain({ ...BASE, eps: [e, e, e] });
  eq(`eps = ${e}: retail price, factor prices, employment`,
     [pc(q.pS), ...q.w.map(pc), ...q.l.map(pc)], [retail, ...w, ...l]);
}

console.log('\nThe sign at the last stage turns on sigma_3 against eta');
for (const [s3, l3] of [[0.15, -0.08], [0.24, 0.00], [0.45, 0.19], [0.80, 0.52]]) {
  const q = solveChain({ ...BASE, sigma: [0.15, 0.30, s3] });
  eq(`sigma_3 = ${s3}: retail employment`, pc(q.l[2]), l3);
}
const q80 = solveChain({ ...BASE, sigma: [0.15, 0.30, 0.80] });
eq('sigma_3 = 0.80: the two upstream stages', [pc(q80.l[0]), pc(q80.l[1])], [-1.50, -0.33]);
const qHi = solveChain({ ...BASE, sigma: [0.85, 0.85, 0.85] });
eq('sigma = 0.85 everywhere: every stage gains', qHi.l.map(pc), [0.56, 0.56, 0.56]);

console.log('\nFixed supply of own inputs');
const fx = solveChain({ ...BASE, eps: [0, 0, 0] });
eq('employment, percent',      fx.l.map(pc), [0.00, 0.00, 0.00]);
eq('factor prices, percent',   fx.w.map(pc), [-4.87, -0.02, 0.33]);
eq('output, percent',          fx.y.map(pc), [-1.45, -0.32, -0.17]);
eq('cost of living, percent',  costOfLiving(fx), 0.11);
eq('real factor prices, percent', fx.w.map(v => pc(v) - costOfLiving(fx)), [-4.97, -0.12, 0.23]);

console.log(`\n${checks} checks, ${fails} failures`);
if (fails) process.exit(1);
console.log('The JavaScript model reproduces every published figure.');
