# How community coding works

Each community is read by its own community coder, a model conversation that sees no other community and no earlier coding. A scheduler prepares each community, launches its coder, checks the result and keeps the record. Communities with more than 500 items divide their threads among fleet coders, and the community coder brings their work together. In this study: 705 communities, coded from 7 September to 4 October 2026, with 115,388 first-order codes and 7,844 second-order themes.

## Its contracts

- [The coder contract](sources/coder-contract.html), version 32 (version 30 for 102 communities): the method, the rules, the five steps and the outputs.
- [The community coder's contract](sources/case-lead.html), which the run calls the case lead's: the gate between working alone and with a fleet, and the order of work in each branch.
- [The fleet coder's contract](sources/fleet-coder.html): one slice of whole threads, coded, and nothing else.
- [The scheduler's contract](sources/scheduler.html): the cycle for one community, the checks, and what happens when one fails.

## The steps

| Step | What happens | In the contract |
|---|---|---|
| 1. The briefing | The coder reads a brief of the community's ordinary week before the event, written by a different reader, and flags any claim without a quote. | [coder contract, step 1](sources/coder-contract.html#4-step-1--the-briefing) |
| 2. Every thread | It passes over every thread in time order, twenty-five at a time, and records whether each belongs to the case. Nothing is coded yet. | [coder contract, step 2](sources/coder-contract.html#5-step-2--go-through-every-thread-and-decide-what-this-case-is) |
| The gate | Above 500 items, a fixed gate divides whole threads among fleet coders; below it, the community coder works alone. Decided once and recorded. | [community coder, the gate](sources/case-lead.html#1b-the-gate-decided-once-and-recorded) |
| 3. First-order codes | Codes stay close to how members put it. A code cites its item by reference; no coder types quotation text. | [coder contract, step 3](sources/coder-contract.html#6-step-3--first-order-codes) |
| 4. Themes | Codes are grouped into second-order themes, named in the members' words where they have one. | [coder contract, step 4](sources/coder-contract.html#7-step-4--themes) |
| 5. The case account | A chronology, then what set off what, with a stated reason for each relation, and a counter-reading before the verdict. | [coder contract, step 5](sources/coder-contract.html#8-step-5--the-within-case-account) |
| Checks and close | The scheduler resolves every cited quote against the record and runs end checks; a failed check sends the work back. | [scheduler, the checks](sources/scheduler.html#3-the-checks) |

## After the coding: the return

At the return ([D2](stages/D2.html)), an adaptation handler forks, for each community, the checkpoint of the community coder that coded it, with its conversation and files, and gives it a new task in a separate folder. This is not another coding pass. Under the return contract the coder recodes its whole community in the population model's terms. It reads its own case account, themes, codes, brief and reply trees against the model, the coding ladder and the model's vocabulary of element and arrow ids. It then writes two files:

- a room model: its case account rewritten section by section in the model's terms, each claim tied to an element id or marked as new and cited to the community's own codes, ending with its own grade and the exceptions it found;
- one line for each change the model needs: an element instantiated, marked absent, given a condition or a finer step, linked, restricted or contradicted, or a new element proposed.

A script checks every return, and the same session repairs what fails. Two separate readers judge, from the evidence, whether the model composes the community. The aggregator rules on every line and revises the model ([D3](stages/D3.html)); each community's return checkpoint then continues with the revised model for the re-check. The results are on [the population return page](results/population-return.html).

To do: the local model (R6), a separate continuation from the coding close. Its contract and how it was run are not yet described here.

[How it was done, with r/PlaceNL beside it](study/coding.html) · [Run it](guides/communities.html)
