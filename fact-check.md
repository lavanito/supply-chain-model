# Fact check: every claim in the note that did not come from the solver

## CORRECTIONS LOG — all applied to version 1.0

Lavan held every correction until he had finished checking each item, then they were
applied in one batch on 19 September 2026. Seven edits across nine places, plus one
`\label`. All of them are in the published paper; the wording below is what went in.
The table further down is the original check, left as written so the reasoning that
produced each correction is on the record.

**1. Energy weight.** Lavan's wording, agreed 19 September: **"Energy is about 6
percent of American household consumption"**. BLS CPI-U relative importance,
December 2024, gives 6.216 percent.

It appears twice. Note that the first instance uses the figure **twice in one
sentence**, so the tail needs handling as well.

Section 4.2, the lambda paragraph (line 203). Read:

> "Energy is 6.3 percent of what American households buy directly and an input to
> most of the rest, so its $\lambda$ is well above 6.3 percent; getting it needs an
> input-output calculation rather than a reading off the published weights."

Now reads:

> "Energy is about 6 percent of American household consumption and an input to most
> of the rest, so its $\lambda$ is well above that; getting it needs an input-output
> calculation rather than a reading off the published weights."

Section 6, the Bruno and Sachs paragraph (line 628). Read:

> "Energy is 6.3 percent of what American households buy directly and an input to
> most of the rest, so its $\lambda$ is far above its direct weight."

Now reads:

> "Energy is about 6 percent of American household consumption and an input to most
> of the rest, so its $\lambda$ is far above its direct weight."

**2. Bruno and Sachs, Europe versus Japan.** Lavan has read the book and judges the
claim low risk, but chose the softer wording anyway. The country pair came out; the
mechanism stayed. Hicks is NOT to be added.

**Confirmed 19 September: the word is "unemployment".**

Two places, both to become the same clause:

Section 3, the second bullet (line 122). Ended:

> "Bruno and Sachs called the general version of this real wage resistance, and used
> it to explain why the oil shocks of the 1970s cost many jobs in Europe and few in
> Japan."

Now reads:

> "Bruno and Sachs called the general version of this real wage resistance, and used
> it to explain why the oil shocks of the 1970s led to much higher unemployment in some
> economies than in others, and attributed the difference to how far real wages
> adjusted."

Section 6 (line 628). Began:

> "This is oil, and it is what Michael Bruno and Jeffrey Sachs called real wage
> resistance in 1985, when they studied why the oil shocks cost many jobs in Europe
> and few in Japan."

Now reads:

> "This is oil, and it is what Michael Bruno and Jeffrey Sachs called real wage
> resistance in 1985, when they explained why the oil shocks of the 1970s led to much
> higher unemployment in some economies than in others, and attributed the difference to
> how far real wages adjusted."

What was checked: the NBER page confirms the book, year, publisher and the
supply-shock thesis, and confirms that the analysis "takes specific account of
institutional differences in the labor markets of the various economies". That same
summary names the divergence as between the United States and Europe, not Japan,
which is why the country pair was dropped. The chapter range 10 to 12 and the
attribution of the term to Hicks in 1974-75 were not confirmed and are not going in.

**3. Item 23, eta = 0.5.** The appeal to the literature was replaced with the
arithmetic, so no unverified external claim is made. The parameter table entry for
$\theta_4$, $\sigma_4$ ended:

> "That gives $\eta$ = 0.5, which matches measured food demand elasticities."

Now reads:

> "The demand elasticity follows from the two: $\eta = \sigma_4(1-\theta_4)
> = 0.59 \times 0.85 = 0.5$. I set $\sigma_4$ to reach 0.5, so that number is a
> choice rather than a measurement."

Arithmetic checked: the exact value used in the solver is $\sigma_4 = 0.5/0.85 =
0.58824$, printed in the table as 0.59. Using the printed 0.59 gives 0.5015, which
rounds to 0.50.

**4. Item 4 is VERIFIED, 19 September.** The origin of the 66,000 cap is in Clemens
and Lewis, NBER WP 30589, footnote 17. The paper says the cap "was set without any
quantitative empirical evidence of its effects on the U.S. labor market. The writers
of the law set the annual cap arbitrarily at triple the number of visas being used at
the time." The footnote gives the source figure - the 1988 INS Statistical Yearbook
reporting 22,115 H-2B nonimmigrants admitted - and credits "Personal communication
with Bruce Morrison, former Chair of the House Immigration Subcommittee and a
principal author of the Act, July 25, 2022." 22,115 x 3 = 66,345.

One detail in the note was not supported. It said Clemens "asked former congressional
staffers where the number came from and reached a subcommittee chairman who
remembered". The footnote records a personal communication with Bruce Morrison; it
does not describe a search through staffers. Naming Morrison is both shorter and
better sourced, so the note now reads:

> "Michael Clemens asked Bruce Morrison, who chaired the House Immigration
> Subcommittee and helped write the Act. The drafters took the 22,115 visas issued
> the previous year, tripled it, and assumed a ceiling that high would never be
> reached."

**5. Item 17, the "zero to five percent", CORRECTED to six, and SPLIT IN TWO.** Lavan
asked for the working to be shown, and showing it exposed an error of mine. I had
multiplied the elasticity by 50 percent. Elasticities multiply log changes, and losing
the draw cut H-2B employment by 0.62 in natural logs, not 0.50.

    e^-0.62       = 0.5379   ->  a 46.2 percent fall, their "about half"
    0.10  x 0.62  = 0.0620   ->  6.01 percent
    0.102 x 0.62  = 0.0632   ->  6.13 percent
    the wrong way, 0.102 x 50 = 5.10 percent   (the old text)

Either instrument rounds to six. Decision of 19 September: the plain statement stays
in Section 3, the arithmetic moves to Section 7.5 with the other caveats.

**(a) Section 3, inside the first bullet.** Read:

> "And native hiring did not rise when migrant hiring was cut; it fell, by between
> zero and five percent."

Now reads:

> "And native hiring did not rise when migrant hiring was cut, and may have fallen
> slightly. Section~\ref{sec:caveats} shows the arithmetic."

**(b) Section 7.5, a new paragraph.** Added near the top of Other caveats, after the
paragraph about the experiment restricting one firm:

> "On the employment of American workers, I said above that native hiring did not
> rise and may have fallen slightly. The arithmetic is this. Clemens and Lewis
> estimate how American employment moves with H-2B employment at +0.10, which is not
> statistically different from zero. Losing the draw cut H-2B employment by about
> half, a fall of 0.62 in natural logs. Multiplying the two gives 0.062, a fall of
> about 6 percent in American employment. Zero is still inside the range, and so is a
> fall of that size."

**(c) A label was needed.** The subsections inside Section 7 carried no labels, so
`\label{sec:caveats}` was added under `\subsection{Other caveats}`.

"Log points" dropped throughout. In Clemens and Lewis 0.62 log points means a
natural-log change of 0.62, which their own gloss confirms: they call the same figure
"about half", and e^-0.62 = 0.538. But the term is ambiguous across the literature -
some authors would write the same change as 62 log points - so the wording names the
units in words instead.

**6. Nothing left to check.** Items 4, 17, 19, 21, 22 and 23 are all settled.

All seven edits, across nine places, plus the label, are applied in version 1.0.

**7. The original check follows.** Items 4, 19 and 23 below, marked NOT VERIFIED, and
item 17, which is my arithmetic rather than a figure the authors print.

---

**The point of this table.** There are two kinds of number in the note and only one of
them can be wrong in the way you are worried about.

**Computed numbers cannot be hallucinated.** Every figure in Sections 4, 5 and 6 —
2.21, 1.03, 0.32, all the tables, the matrix, the elasticities — is an output of
`chain_solver.py`. `verify.py` recomputes all 65 of them and fails if any moves. You
can run it yourself in about ten seconds: `python verify.py`. No judgement required.

**External facts are the real risk**, and there are 23 of them. They are listed below
with what I checked them against. Three are marked NOT VERIFIED and one is marked
WRONG. If you check nothing else, check those four.

Status key: **OK** = I read the figure in the source named. **DERIVED** = I calculated
it from figures in the source; the arithmetic is shown. **NOT VERIFIED** = I did not
find a source; treat as unchecked. **WRONG** = the source contradicts the note.

---

## Section 2, the Clemens and Lewis study

| # | Claim in the note | Status | Source |
|---|---|---|---|
| 1 | 98% of H-2B jobs need no high school education; 1.2 months experience on average | OK | NBER WP 30589, quoted verbatim: "98% of all H-2B jobs do not even require a high school education; the mean months of experience required by employers is 1.2" |
| 2 | Cap of 66,000 a year, split 33,000 / 33,000 | OK | [USCIS cap count page](https://www.uscis.gov/working-in-the-united-states/temporary-workers/h-2b-non-agricultural-workers/cap-count-for-h-2b-nonimmigrants) |
| 3 | Cap set by the Immigration Act of 1990 | OK | Same page |
| 4 | Clemens asked former staffers; drafters took ~22,000 and tripled it | **NOT VERIFIED** | I could not find this in a source I read. It may be in the published paper or an interview. **Check this one.** |
| 5 | 136,555 workers requested against 33,000 places, 2H 2022 | OK | NBER WP 30589, quoted verbatim |
| 6 | 2026: statutory 66,000 plus a 64,716 supplement | OK | [Federal Register, 3 Feb 2026](https://www.federalregister.gov/documents/2026/02/03/2026-02131/exercise-of-time-limited-authority-to-increase-the-fiscal-year-2026-numerical-limitation-for-the) |
| 7 | 2019 server crash; random letters A–E in 2021, A–G in 2022 | OK | NBER WP 30589, quoted verbatim |
| 8 | 472 firms, 2021 and 2022 draws, pre-registered | OK | NBER WP 30589; pre-analysis plan at osf.io/zdyun |
| 9 | Losing the draw cut H-2B employment by about half | OK | NBER WP 30589: "–0.62 log points" |
| 10 | Revenue elasticity 0.20 to 0.22; halving cuts revenue about 12 percent | OK / DERIVED | Elasticity from the paper. The 12 percent is mine: 0.20 × 0.62 log points ≈ 0.124 ≈ 12% |
| 11 | US employment zero or positive; rural subsample 0.61 | OK | NBER WP 30589 and the AEA summary |
| 12 | Elasticity of substitution 0.8 to 2.2 | OK | [AEA research summary](https://www.aeaweb.org/research/immigration-restrictions-firms-workers): "roughly 0.8 to 2.2". **Note the older IZA working paper says 2.1** — if you cite that version, the number changes |
| 13 | Related studies typically find 4 to 10 | OK | AEA summary, quoted verbatim |
| 14 | Investment elasticity 1.5 to 2.1 | OK | NBER WP 30589 |
| 15 | Profit rate elasticity 0.15 | OK | NBER WP 30589 |
| 16 | de Haas, 22 myths, including that border restrictions reduce immigration and that immigrants take native jobs | OK | Penguin sample PDF, chapter list: Myth 8 and Myth 21 |

## Section 3

| # | Claim | Status | Source |
|---|---|---|---|
| 17 | Native hiring "fell, by between zero and five percent" | **DERIVED, and it is my arithmetic not theirs** | The paper reports an elasticity of +0.102 for US low-skill employment, statistically indistinguishable from zero (p = 0.305). Losing the draw halved H-2B employment, so 0.102 × 50 ≈ 5 percent. The paper does not print "zero to five percent" anywhere. Either attach this derivation or soften the claim — corrected, see item 5 above |
| 18 | Kremer 1993, O-ring, Challenger exploded in 1986 because of an O-ring seal | OK | Kremer's own words: "The space shuttle Challenger had thousands of components: it exploded because it was launched at a temperature that caused one of those components, the O-rings, to malfunction" |
| 19 | Bruno and Sachs, real wage resistance, oil shocks cost many jobs in Europe and few in Japan | **NOT VERIFIED** | I confirmed the book exists (Harvard UP, 1985). I did not read it and did not verify the Europe-versus-Japan claim or that they use the term "real wage resistance". **Check this one** |

## The calibration

| # | Claim | Status | Source |
|---|---|---|---|
| 20 | Farms received 11.8 cents of every dollar spent on domestically produced food in 2024 | OK | [USDA ERS](https://www.ers.usda.gov/data-products/charts-of-note/114074), verbatim: "In 2024, U.S. farm establishments received 11.8 cents per dollar spent on domestically produced food sold at places such as grocery stores and restaurants." **Note: USDA also publishes a "farm production" figure of 6.7 cents for 2024 from a different series.** Say which one you mean |
| 21 | "Food at home and at restaurants is about a seventh of total household consumption", so theta_H = lambda = 0.15 | **OK, resolved 19 Sep 2026** | BLS CPI-U relative importance, December 2024: food total, at home plus away, is **13.691 percent**. The earlier wording said "food at home", which is 8.0 percent, and said "what households buy", which understates the denominator because the CPI basket includes owners' equivalent rent. Both are corrected in version 1.0. Note 0.15 is a little above the measured 0.137; see below |
| 22 | Energy is 6.3 percent of what American households buy directly | **Close, check the vintage** | BLS CPI-U, December 2024: **6.2 percent**. Either round to "about 6 percent" or name the vintage |
| 23 | eta = 0.5 "matches measured food demand elasticities" | **NOT VERIFIED** | Plausible and conventional, but I did not check it against a source |

## Sources for the objections

| Claim | Status | Source |
|---|---|---|
| Acemoglu's condition: scarcity encourages technology only if strongly labour saving | OK | [JPE 118(6), 1037–1078](https://economics.mit.edu/sites/default/files/publications/when%20does%20labor%20scarcity%20encourage%20innovation.pdf), quoted |
| Habakkuk 1962 on American labour scarcity | OK | Via Acemoglu's own quotation of him |
| Bracero exclusion: tomatoes, cotton, sugar beets mechanised; asparagus, strawberries, lettuce, melons did not | OK | [NBER WP 23125](https://www.nber.org/system/files/working_papers/w23125/w23125.pdf), quoted verbatim |
| Groundskeeping 36 to 46 percent; seafood 6 to 10 percent | OK | Both paper versions: IZA gives 35.5 / 6.1, NBER gives 46.2 / 10.2 |
| Marshall's two quotations | OK | [Principles, Book V Ch. VI](https://www.marxists.org/reference/subject/economics/marshall/bk5ch06.htm), both verbatim |
| Rittel and Webber on wicked problems | OK | [Policy Sciences 4, 155–169](https://www.theisrm.org/documents/Rittel%20&%20Webber%20(1973)%20Dilemmas%20in%20a%20General%20Theory%20of%20Planning.pdf), quoted |

---

## The one that changed the wording, not the numbers

Item 21 was wrong and is now fixed. The note said food at home was a seventh of what
households buy. Food at home is 8.0 percent of the CPI. A seventh is food *including
restaurants*, 13.7 percent. And "what households buy" was the wrong denominator
anyway, because the CPI basket includes owners' equivalent rent.

The note now says "food at home and at restaurants is about a seventh of total
household consumption", which is right, and every number stands unchanged.

**One thing left to decide.** The note uses 0.15 where the measured weight is 0.137.
That is within "about a seventh", but it is rounded upward, and it makes the cost of
living effect slightly larger than the data would give:

| theta_H = lambda | shelf price | cost of living | effective share | employment |
|---|---|---|---|---|
| 0.15, as printed | 2.76% | 0.41% | 0.138 | -2.21, -1.03, -0.32 |
| 0.137, the measured weight | 2.73% | 0.37% | 0.136 | -2.19, -1.01, -0.30 |

The difference is immaterial to every conclusion. Moving to 0.137 would mean
re-running all 65 figures for a third decimal place. I would leave it at 0.15 and let
"about a seventh" carry it.

**A second consequence, worth a sentence somewhere.** The good is now all food,
restaurants included, but the last stage of the chain is still described as "transport
and retail", the price table calls it the "retail shelf", and Section 5.2 talks about
"a supermarket" switching to imported food. If the good includes restaurant meals then
the last stage is retail *and food service*. The model does not care; the labels do.
