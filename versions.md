# Time and versions

How long the work took, how the two contracts came to their current versions, and how the population model changed during the run. All dates are 2026 and all times UTC.

## Time

From the first recorded community coding run on 18 August to the last aggregator session on 28 October is 71 days.

**Community coding.** Earlier contracts coded 347 communities in 462 runs between 18 August and 5 September, mostly with Claude Opus 5; that coding was later redone. The final coding ran from 7 September to 4 October with gpt-5.6-sol: 5,097 agents at medium reasoning effort and 65 at extra high. It finished about 130 communities a week in its first three weeks. The aggregator's frame of 705 coded communities was taken on 4 October. Coding hours were not logged.

**The return to the model.** The model went to all 705 community coders on 15 October, and their first returns were compiled on 16 October. After the aggregator revised the model, the re-check went out on 21 October and came back from all 705 by 22 October, about 30 hours later. The returns used gpt-6.1-sol.

**The aggregator.** Run claude-v43-1, with Claude Opus 5.5, ran 21.5 days, from 6 October to 28 October, in 316 sessions. Sessions are counted from launch to close, waits for our rulings included; the median session took 34 minutes.

| Stages | Dates | Session hours | Sessions |
|---|---|---:|---:|
| A1, reading the communities | 6 to 7 Oct | 19 | 57 |
| B1 to B4, coding the themes | 7 to 13 Oct | 120 | 72 |
| C1 to C5, building the model | 13 to 15 Oct | 19 | 43 |
| D1 to D3, return and revision | 15 to 24 Oct | 177 | 61 |
| D4 to D6, organizational forms | 24 to 27 Oct | 37 | 69 |
| E1 to E2, audit and close | 27 to 28 Oct | 5 | 14 |
| Total | 21.5 days | 377 | 316 |

B1 and D3 took the most time. The [run log](runlog.html) gives every stage with its dates and tokens. Three D3 sessions that waited on rulings hold 104 of the 377 hours. Routine reading checks and fleet coding at stages B2 and B3 used DeepSeek V4.1 Flash, in 1,573 calls.

## Contract versions

Written contracts specify what each agent reads, produces and may do. We developed them through repeated runs on the same material and interviews with the agents, and revised a contract when the agents' work departed from the grounded-theory method.

**Community coders, v1 to v32.** Only v30 (102 communities) and v32 (603) coded the final data.

| Version | Date | Change | Use |
|---|---|---|---|
| v1 to v15 | August | Early contracts; v5 ran seven coders on one community | Pilots |
| v16 to v27 | 18 to 31 Aug | One coder reads each community | Runs, later recoded |
| v29 | 4 Sep | A community coder leads, with fleet coders for large communities | Pilots |
| v30 | 6 Sep | Cut for the final coding: a size threshold and a minimum slice | Coding from 7 Sep |
| v31 | 8 Sep | The community coder runs end checks before closing, after defects in 34 of 60 communities | No community is recorded under v31 |
| v32 | 9 Sep | The recording tool refuses a missing cited exclusion | Coding to 4 Oct |

**The aggregator, v28 to v43.** Versions v28, v35, v37 and v43 were run on real data; the others were development versions.

| Version | Date | Change | Use |
|---|---|---|---|
| v28 | 24 Aug | The first contract, in eight stages | Run |
| v35 | to 5 Sep | Nineteen stages. The aggregator lost the method and dropped findings at counterexamples, so the method was written into its own file | Run |
| v37 | 7 Sep | Cut from 23 stages to 19, after review by the v28 and v35 aggregators and 13 rulings by us | Run, 8 to 21 Sep |
| v38 | 24 Sep | Knowledge kept on disk and decisions in context, after v37 lost context it could not see; changes from interviews with v37's checkpoints | Development |
| v40 to v42 | 2 to 3 Oct | Method changes; one contract on two platforms; longer sessions | Two runs stopped at stage A1 |
| v43 | 4 Oct | The frame of 705, questions to us, and two kinds of claim (Günther et al., 2026) | Run claude-v43-1 |
| v43.2 | 6 and 11 Oct | Fixes, including one from an interview during stage B1 | Same run |

Dates for v29 to v34 are not recorded, and v39 has no record.

## Population model versions

The run recorded each version of the model as a hash of its files, and every change in a history of 182 edits with its reason. Nothing is deleted: an element that loses its grounding becomes a candidate.

| Version | Recorded | Elements | Arrows | Sent to |
|---|---|---|---|---|
| e15f9647 | close of C5, 15 Oct | 30: 23 standing, 5 candidate, 2 tentative | 21 | the 705 community coders at D2 |
| 46384686 | frozen at D3, 24 Oct; unchanged at D6 | 45: 30 standing, 15 candidate | 21 | the 705 at the re-check |

| Stage | Dates | Edits | Added | Revised | Cut | Elements and arrows after |
|---|---|---:|---:|---:|---:|---|
| C2 | 14 Oct | 82 | 48 | 34 | 0 | 28 and 20 |
| C3 | 14 Oct | 3 | 0 | 3 | 0 | 28 and 20 |
| C4 | 14 Oct | 3 | 3 | 0 | 0 | 30 and 21 |
| C5 | 14 to 15 Oct | 46 | 0 | 43 | 3 | 30 and 21 |
| D3 | 16 to 24 Oct | 38 | 15 | 23 | 0 | 45 and 21 |
| D4 | 24 Oct | 10 | 0 | 10 | 0 | 45 and 21 |

The main revisions:

- **C3 and C4.** Two arrows take a mechanism from conversation analysis. Two elements and an arrow enter from r/place, the field, as tentative.
- **C5.** Three elements are cut for want of a grounded arrow; one of them is restored.
- **D3, from the community coders' returns.** The starter's role is split from joining, which the model now treats as the answer to a call. Repair is revised: it restores the form the keepers know, so a planned change is erased as damage until the keepers learn of it. r/PlaceNL is among the communities that showed this ([the example](results/placenl.html)). The field's elements and arrow become standing, and fifteen candidates enter. We froze the model as 46384686.
- **D4.** Two changes made after the freeze were reverted to proposals, restoring 46384686.

## Sources

The coding status and progress files of the coding handler; the run's session log and `RUN.json`; the contracts' change logs and the instrument history archive; the run's `history.jsonl`, model files and close hashes.

Günther, W. A., Joshi, M., & Constantinides, P. (2026). Trustworthiness in computational theory construction: Dimensionalization and category surfacing. *MIS Quarterly*, 50(3), 851–878.
