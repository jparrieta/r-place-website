# Audit the evidence

Use five questions from [TRACE](https://trace-os.org/start/principles/) to inspect this study. This is an evidence map, not a TRACE certification or a new protocol. Records show what was retained; they do not prove an explanation sound.

**Scope:** one C2 model-building example in the indexed publication, commit `c070d990be882`. These records come from the parent run before the C4 Field branch. They do not establish coverage of every stage or community. Saved-run links below require repository access. [Full instructions](../sources/contract.html) and [source hashes](../sources/manifest.json) are readable on this site; instructions describe what should happen, not proof that it happened.

[Evidence register](../evidence.json): exact file versions, hashes, checks and limits. It records this inspection, not an acceptance decision.

## T. Track records: what happened and why?

**Recorded example:** [Model history](https://github.com/jparrieta/r-place/blob/c070d990be88234ccd74101d4104160e71a28c5e/aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/model/history.jsonl) associates model changes with a leg, reasons and source communities. The [C2 close receipt](https://github.com/jparrieta/r-place/blob/c070d990be88234ccd74101d4104160e71a28c5e/aggregator/runs/claude-v43-1/CONTROL/close-status-C2.C2d-02.json) identifies a completed turn, validator and report hashes. The report hash was checked against its saved file for this guide on 24 October 2026.

**Limit:** a close receipt is a record of completion and checks, not a record of every inference or a resumable agent by itself.

## R. Review against sources: what was tested?

**Recorded example:** [The C2 review](https://github.com/jparrieta/r-place/blob/c070d990be88234ccd74101d4104160e71a28c5e/aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/review-C2.md) retains nine objections and discloses the ten model sections omitted from the review packet. [Reviewer metadata](https://github.com/jparrieta/r-place/blob/c070d990be88234ccd74101d4104160e71a28c5e/aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/_fleet_raw/C2/C2-reviewer/r1.meta.json) binds the reviewer to a packet hash; that hash and the returned model hash match their saved files.

**Limit:** the reviewer saw selected sections. Neither a favourable review nor valid file shapes establish the model's truth. [C2's full instructions](../sources/stage-C2.html) explain the review criterion.

## A. Accept independently: who could decide?

**Recorded example:** [QC2-001](https://github.com/jparrieta/r-place/blob/c070d990be88234ccd74101d4104160e71a28c5e/aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/_answers/QC2-001.md) identifies a handler ruling under J's delegation, including what the reviewer may see. [The handler protocol](../sources/handler.html) separates aggregator, handler and PI duties.

**Gap:** this demonstrates a delegated scope decision, not independent acceptance of the entire model. The aggregator answers the critic's objections. We have not established a separate, version-bound acceptance decision for every output. Critique, close and scientific acceptance must not be read as synonyms.

## C. Control transitions: what may advance?

**Recorded example:** [QC2-002](https://github.com/jparrieta/r-place/blob/c070d990be88234ccd74101d4104160e71a28c5e/aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/_answers/QC2-002.md) states J's direction for the final C2 pass and how to treat the stopping criterion. The [close report](https://github.com/jparrieta/r-place/blob/c070d990be88234ccd74101d4104160e71a28c5e/aggregator/runs/claude-v43-1/CONTROL/validation-C2.C2d-02.txt) preserves a warning even though the mechanical check passed. Read the ruling beside the warning; do not turn either into a blanket approval.

**Limit:** a stage gate differs from the decision to publish a checkpoint. A readable record does not imply a downloadable bundle or a live interview. [See available routes](../interviews.html).

## E. Evaluate corrections: did the repair work?

**Recorded example:** [The C2c response](https://github.com/jparrieta/r-place/blob/c070d990be88234ccd74101d4104160e71a28c5e/aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/notes-C2.md#L504-L516) accepts the reviewer's objection to the label “Present” and specifies a correction. [Pass 4](https://github.com/jparrieta/r-place/blob/c070d990be88234ccd74101d4104160e71a28c5e/aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/model-p4.md#L11) records that replacement as “order fails in”. The earlier version is retained. This audit checked the revised wording, not the underlying counts.

**Gap:** the later close report does not prove an independent, targeted recheck of every correction. That wider claim remains unverified.

## Use a checkpoint interview

Ask which evidence changed the account, what an objection exposed, and what remains uncertain. Check the reply against the saved record. New interview answers are private, later responses; they do not amend the original evidence or certify it. [Interview guide](interviews.html).
