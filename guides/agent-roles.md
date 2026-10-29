# Agents and their roles

The work is divided so that preparing evidence, interpreting it and checking an interpretation are distinct jobs. A handler manages the process. A lead owns an account. A reader answers a bounded question from specified evidence. The researcher sets the study’s scope and remains responsible for its claims.

An agent is a model conversation with a task and permitted files. These are roles, not model brands. Checkpoint records identify the model and saved state used at a particular point.

[Prepare the record](#prepare-the-record) · [Understand a community](#understand-a-community) · [Build the shared model](#build-the-shared-model) · [Return and audit](#return-and-audit) · [Interview a saved agent](#interview-a-saved-agent)

## AI use in v43

The paper reports this division of work. Exact settings, changes of model and fork boundaries belong to each saved checkpoint; this summary does not replace that history.

| Work | Model and environment |
|---|---|
| Community coding | GPT-5.6 Sol in Codex. |
| Community returns to the population model | GPT-6.1 Sol in Codex. |
| Population analysis | Claude Opus 5.5 in Claude Code. |
| Routine reading checks and classification fleet | DeepSeek V4.1 Flash. |

The authors designed the instrument and ruled on questions during the run. The agents code and compose descriptions; the authors judge the theoretical contribution and answer for the claims. Claude and Codex also helped edit the paper and build the figures and website. [Inspect recorded model settings and lineage](history.html#models-and-lineage).

## Prepare the record

### Collection handler

Obtains the selected pixel, Reddit and atlas data through the repository’s download routes, checks what arrived and records gaps. Its handoff gives the coding handler verified input paths and versions. It does not choose new research categories or interpret communities. [Collection brief](../agents/collection.html).

### Community brief writer

Reads the community’s record from before the event and writes a background brief. This gives the coding lead context about the community without supplying an interpretation of its later r/place activity. The brief and its quotations are checked before coding begins. [Brief writer’s role](../Manual-html/files/coder/contract-brief-writer.html).

## Understand a community

### Coding handler, also called the scheduler

Prepares each community’s working folder, launches its agents, checks their outputs and keeps the progress record. It manages failed jobs and preserves completed work. It does not decide what a quotation means or rewrite an aggregator’s answer to make a check pass. [Scheduler contract](../sources/scheduler.html).

### Community reader, or fleet coder

Reads an assigned part of one community’s record and develops codes tied to participants’ words. In a large community, readers receive slices of whole threads. Their work passes to the case lead. This community-coding fleet is different from the aggregator’s later classification readers. [Reader contract](../sources/fleet-coder.html).

### Case lead

Owns the community’s whole account. It reads a small community itself; for a larger community it assembles the fleet’s work, groups codes into local themes and writes the case narrative. Its saved conversation and matching files support later continuation and interviews. [Case-lead contract](../sources/case-lead.html).

### Standalone community coder

Develops a model of organizing within one community, using its coded evidence. The recorded R6 close is a later milestone than the initial coding close. It belongs to a separate local-model workflow, not an extra step silently added to the coding scheduler. Compare [PlaceNL after coding](../records/community--PlaceNL--coding-close.html) with [its R6 model](../records/community--PlaceNL--R6.html).

## Build the shared model

### Aggregator handler

Builds the population-level run, opens and closes its legs, supplies permitted inputs and dispatches reader jobs. It records checks, preserves checkpoints and brings research decisions to the investigator. Passing its file checks does not establish that an explanation is true. [Handler protocol](../sources/handler.html).

### Aggregator

Reads across communities, builds common categories, develops the population model, assesses returns and explains organizational forms. Stages divide this work into inspectable steps. A new stage or leg does not by itself mean a fresh aggregator: saved conversation, files and recorded lineage carry the work forward. [Follow the stages](aggregator.html#stage-map).

### Classification readers

Use the common scheme to assign local themes to categories. They test the rules in [B2](../stages/B2.html), apply them across the collection in [B3](../stages/B3.html), and check settled placements in [B4](../stages/B4.html). Separate readings expose disagreement. They do not settle it by vote; the aggregator returns to the evidence.

### Critical readers

Challenge a developing explanation rather than build the whole model themselves. The [C2](../stages/C2.html) reader examines the model; [C5](../stages/C5.html) readers test claims in the integrated account against cases. Their replies remain alongside the aggregator’s responses, including criticism that remains unresolved.

### Field agent and its separate workflow

Studies the central r/place forum, where communities recruit, negotiate and discuss the event. It supplied an interim reading and comments at [C4](../stages/C4.html) while its own analysis remained unfinished. A comparison with its completed model is still pending. Its role is to offer a view between communities. This website does not yet supply a standalone Field launch guide.

## Return and audit

### Adaptation handler

Delivers the fixed population model to each matching saved community lead, checks returns and routes required repairs back to that lead. It keeps local histories separate and records missing returns. It does not summarize the model for the lead or decide which corrections the aggregator should accept. [Return preparation](../stages/D1.html).

### Returning community lead

The saved case agent reads the population model against its own community and writes a local account in the model’s terms. It records needed detail, conditions, contradictions or missing ideas. If the model changes, affected leads return for the [D3 recheck](../stages/D3.html). These are model-to-record comparisons, not interviews with the original participants.

### Verdict readers

Independently judge how well the model accounts for each community from specified evidence. Their reasons can disagree with each other or with the returning lead. [D2](../stages/D2.html) preserves these judgments; D3 assesses disputed ones. A verdict is not permission to change the model.

### Reconstruction readers

In [E1](../stages/E1.html), check whether the shared model plus supported local adaptations can account for claims in a sample of community narratives. They help reveal missing links between population explanations and local evidence. Their bounded test does not certify every claim in the study.

## Interview a saved agent

A checkpoint interview opens a disposable fork of a saved agent with its matching historical files. It is the aggregator at a chosen point, not a new agent asked to imitate it from a summary. Its answers are new interview responses; they do not alter or become part of the original analysis.

The [interview catalogue](../interviews.html) distinguishes available community and aggregator checkpoints. It does not promise a conversational checkpoint for every brief writer or fleet reader. [Reading keys for agents](../agents.html) provide the operational instructions; this page explains the division of work.
