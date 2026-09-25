# Financial model and reconciliation

This is the analytical core of the repository. It explains how the model is built, which source figures were used where the drafts disagreed, and what the numbers show once reconciled.

## Method

Every figure lives in `data/assumptions.yaml`. The Python package reads that file and computes the CAPEX plan, OPEX, revenue scenarios, operating position and ROI. No number is hard-coded in the code. Changing an assumption in the YAML updates every table and chart. This is a deliberate choice: an investment case is only as good as the ability to interrogate it, so the model is written to be interrogated.

Run it with `python scripts/run_model.py`, or step through it in `notebooks/nexus_financial_model.ipynb`.

## CAPEX

The £50m capital budget is a hard ceiling. The cost plan used here balances to exactly £50m:

| Component | £m |
|-----------|----|
| Construction (BREEAM Excellent) | 25.5 |
| Specialist lab fit-out & equipment | 8.5 |
| Risk allowance (10% NRM1) | 3.4 |
| Working capital reserve (Yr 1–5) | 3.2 |
| Professional fees & PM | 3.1 |
| External works & site enabling | 2.5 |
| Digital infrastructure | 2.3 |
| Community & engagement spaces | 1.5 |
| **Total** | **50.0** |

### Why this version of the cost plan

Three CAPEX structures appear across the challenge drafts:

1. The Pitch Deck breakdown, which sums to exactly £50.0m with a £3.4m risk line and no separate inflation line. This is the version used here.
2. The Executive Summary "TurningPoint" table, which lists risk at £5.0m plus a separate £1.75m inflation line. That combination overshoots the £50m ceiling by about £3.35m, so it does not balance.
3. A later NEXUS narrative that bakes fees, risk and inflation into a £32.8m NRM1 construction EAC.

The first is the only one that both balances and disaggregates cleanly, so the model treats it as canonical and notes the alternatives here rather than picking silently.

### The construction rate

The base construction rate is built from a 60/40 spatial split rather than asserted. Sixty per cent of the floor plate (3,600 m²) is high-specification lab space at £4,000/m²; forty per cent (2,400 m²) is offices, circulation and amenity at £3,000/m². The blended base rate is £3,600/m², which sits below the BCIS 2026 university-laboratory range of £4,000–£6,500/m² because of the mix of space, not a discount. Adding a 12% BREEAM Excellent premium and the fees, risk and inflation allowances brings the all-in figure to roughly £8,333/m² across the 6,000 m² building.

## OPEX

Two operating figures exist in the source material. The Layout Plan and Pitch Deck use £1.9m a year. The revised Executive Summary corrects this to £4.5m a year, which is the more credible figure for a facility with wet labs, ATEX zones, immersion cooling and a full research and facilities complement. The model keeps both as named cases and defaults to the revised £4.5m.

## Revenue

Revenue is built bottom-up, one stream at a time, each with a stated driver so the total is auditable rather than a single asserted number:

| Stream | Base £ | Basis |
|--------|--------|-------|
| Research grants | 1,200,000 | 3 projects × £500k FEC × 80% UKRI rate |
| Industry memberships | 365,000 | 2 Strategic + 5 Corporate + 6 SME tiers |
| Sponsored R&D | 500,000 | 5 industry-funded projects × £100k |
| Demonstrator access | 250,000 | 100 access days × £2,500 |
| Partner residency | 150,000 | Hot desks, sprint pods, lab-adjacent, strategic |
| Training & exec education | 100,000 | 10 cohorts × 25 × £400 |
| Events & conferences | 50,000 | 20 events × £2,500 net |
| Public / regional funding | 250,000 | Programme allowance |
| Commercialisation | 0 | Upside only, excluded from base |
| **Base total** | **2,865,000** | |

The membership tiers are benchmarked down from the National Composites Centre (Tier 1 £180k, Tier 2 £30k, SME £2.5k), treating NCC as an upper bound rather than a direct tariff because NEXUS is an early-stage regional centre. Sponsored R&D uses DETI's £3m+ Phase 1 industry leverage as its benchmark. Residency pricing is benchmarked against Innovation Birmingham.

Conservative and optimistic columns are held in the same file. The conservative total is £1.375m; the optimistic total, which is the only case that includes commercialisation upside, is £7.2m.

## The reconciliation issue

This is the finding worth stating plainly. The Executive Summary presents a £500k annual operating gap covered by the £3.2m working capital reserve for five years. That arithmetic only works if annual revenue is £4.0m against £4.5m OPEX.

The auditable bottom-up base case reaches £2.865m, not £4.0m. Against the revised £4.5m OPEX that produces an annual gap of about £1.635m, and the £3.2m reserve is exhausted inside two years rather than lasting five. The model surfaces this rather than adopting the rounded £4.0m headline.

There are three honest ways to close the gap, and a credible case would pick one:

1. Hold OPEX at the earlier £1.9m estimate, under which the base case turns a small surplus. This is the position the Pitch Deck actually presented, and the model reproduces it with the `early` OPEX case. It requires defending the lower operating cost for a facility of this specification, which is hard.
2. Reach the optimistic revenue case, the only scenario that covers the £4.5m OPEX, which depends on winning £2.0m of grants and £1.5m of memberships from year one.
3. Secure a standing institutional contribution beyond the five-year reserve. The Executive Summary hints at this (0.05% of the university's £1.1bn income), and making it explicit and permanent is the cleanest fix.

Naming the gap and the routes to close it is more useful to a decision-maker than a headline that does not reconcile with its own build-up.

## Societal return

The investment case is expressed as societal value, in the manner of an HM Treasury Green Book appraisal. Direct revenue, research income uplift, regional economic multiplier, student employability value and energy savings are estimated at £10.5m a year, a 4.8-year payback on £50m. These are indicative early-stage figures, not an audited forecast, and the repository presents them as such.
