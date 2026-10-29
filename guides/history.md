# Historical context for this study

Target length: under 1,200 words. Updated 28 October 2026. These notes describe the recorded study; they do not amend the contracts or authorize a run.

## Publications and closure

The run finished at E2b on 28 October 2026. Final publication `f27566528a5102d944c6ddc3d2e2e98b839cbab8` records all 18 stages closed. The earlier catalogue baseline, `c070d990be88234ccd74101d4104160e71a28c5e`, ends during D3. Its accepted checkpoints and proofs remain unchanged; later records identify their own commits.

Final stage boundaries are D4a-08, D5a-41, D6a-18, E1e and E2b. D5b and D6b closed earlier, before further work in those stages. They remain available as historical legs, not as the final versions. A checkpoint that also closes a stage appears once. [Read the completed run](study.html).

Every checkpoint displays its source commit and commit date. Saved-state dates have their own basis, or say “not recorded”. A commit date is not a scientific close. For D3c, the [checkpoint metadata](../history-evidence/D3c-checkpoint.json), [validation receipt](../history-evidence/D3c-validation.json) and [stage close marker](../history-evidence/D3-FINISHED.txt) support the dated status. The metadata hash matches the admitted checkpoint.

The [C5d-p2 account](../records/aggregator--claude-v43-1--C4-field--C5.C5d-p2.html), saved on 15 October, is partly superseded. D3 revised R01 and P05, bounded A21 and added fifteen candidates. The [D3 handback](../records/aggregator--claude-v43-1--C4-field--D3.D3c/07-handback-D3.html) records those revisions. The [final D6 account](../records/aggregator--claude-v43-1--C4-field--D6.D6a-18.html) and E1/E2 audits now document the later account and its limits.

## C4 and the unfinished Field analysis

The Field agent had not finished its analysis when it supplied its reading and comments to C4. The investigator clarified this distinction on 29 October 2026. The saved C4 account calls the supplied material a field model, but that label does not establish that the Field agent's full model was complete. C4's close records the aggregator's handling of the interim material.

[Read what that comparison changed](../stages/C4.html#what-v43-received). The saved files and their wording remain intact. Comparison with the completed Field model is still pending.

## Models and lineage

The canonical instruction says to restore the original lead on its recorded model and effort. This study used dated operational decisions, retained in [handler decision rows 155 and 248](../history-evidence/handler-decisions.tsv). On 15 October, J specified a GPT-5.6 Sol resume followed by GPT-6.1 Sol medium for the return. On 21 October, the re-check was corrected to GPT-6.1 Sol medium; the earlier 5.6 launch wording was superseded. The [correction message](../history-evidence/D3-model-correction.md) records why `resumed_with` is unreliable as a description of an answer turn.

This website review inspected the D2 archives of all 14 shared communities. Each archive hash matched its custody receipt. In each, the source proof names the same archive used for the shared coding close; the native fork identifies its original session and boundary ordinal; and the D2 turn contexts record GPT-6.1 Sol, medium. Thus `run.json`'s `model=6.1` describes these returns, while `resumed_with=5.6` is retained historical metadata, not proof that their answers used 5.6.

The verified relationship for these communities is:

```text
Original coding close
  +-- R6: same original session continued for the local model
  +-- D2: fork from the coding close for the global return
        +-- D3: same D2 session ID in the re-check return record
```

D2 did not fork from R6. A shared source identity does not mean the D2 branch held the later R6 local model. The D3 records name GPT-6.1 Sol and the same D2 session IDs. They omit effort; medium was prescribed, not independently checked in those D3 transcripts by this website review. The review did not inspect all 705 D2 native histories. These limits must not be generalized into a claim about every room.

| Shared community | D2 source and native-turn evidence |
|---|---|
| r/PlaceNL | [Fork, source archive and turn settings](../history-evidence/PlaceNL-D2-lineage.json) |
| r/thenetherlands | [Fork, source archive and turn settings](../history-evidence/thenetherlands-D2-lineage.json) |
| r/cirkeltrek | [Fork, source archive and turn settings](../history-evidence/cirkeltrek-D2-lineage.json) |
| r/norge | [Fork, source archive and turn settings](../history-evidence/norge-D2-lineage.json) |
| r/norway | [Fork, source archive and turn settings](../history-evidence/norway-D2-lineage.json) |
| r/sweden | [Fork, source archive and turn settings](../history-evidence/sweden-D2-lineage.json) |
| r/greece | [Fork, source archive and turn settings](../history-evidence/greece-D2-lineage.json) |
| r/czech | [Fork, source archive and turn settings](../history-evidence/czech-D2-lineage.json) |
| r/armenia | [Fork, source archive and turn settings](../history-evidence/armenia-D2-lineage.json) |
| r/indonesia | [Fork, source archive and turn settings](../history-evidence/indonesia-D2-lineage.json) |
| r/placehearts | [Fork, source archive and turn settings](../history-evidence/placehearts-D2-lineage.json) |
| r/mindcrack | [Fork, source archive and turn settings](../history-evidence/mindcrack-D2-lineage.json) |
| r/blackmirror | [Fork, source archive and turn settings](../history-evidence/blackmirror-D2-lineage.json) |
| r/Goodboye | [Fork, source archive and turn settings](../history-evidence/Goodboye-D2-lineage.json) |

These are selected metadata fields, not complete agent transcripts. Their member hashes and archive hashes identify the retained evidence. Reading them starts no agent.

## Instruction versions

The canonical source copies on this site remain unchanged. Historical checkpoints preserve the files they actually held. A stage-file hash is evidence of a saved file, not proof that the analyst read it or that no later instruction was delivered.

**B1.** Saved card SHA-256: `246c890d13c93007d92a27d29c76be7814281d946bc014c23dc96496e0819f97`. Current canonical card SHA-256: `a2b733dded3046ba611c65e979beb597ef8ef26e8b625dea28469a254219f8a0`. [Saved card](../history-evidence/saved-STAGE-B1-coding-third-order-scheme.md); [current canonical card](../sources/stage-B1.md). The saved hash is confirmed in all three shared B1 checkpoints.

**B4.** Saved card SHA-256: `bb5cc6a5690643e43d2e8a600efb4c750fc499bf2c2abea6c90a94861f0e1357`. Current canonical card SHA-256: `7fb68adfcd6a1dab15368728559d3eb3c91162c555a8a69b26a53571dfd16ebe`. [Saved card](../history-evidence/saved-STAGE-B4-coding-adjudication-and-freeze.md); [current canonical card](../sources/stage-B4.md). The saved hash is confirmed in all three shared B4 checkpoints.

B1b-32, B1d-07 and B1e predate the 11 October amendment. B1e closed at 14:49Z; decision row 75 follows at 15:51Z. The 16:25Z delivery puts the gate and member-recheck changes into the next B2 leg. Those later checks must not be imposed retrospectively on B1.

Decision row 96 introduced B4's three-placement rule on 12 October. The 21:19Z handler delivery explicitly opens B4a-01 under that amendment. The saved notes record its use. A further ruling changed packet 4 from item 401 and sent earlier affected rulings back at B4a-05. Thus the B4a-07, B4b-p4 and B4c checkpoints follow those changes; their original stage-file hash alone does not encode the delivered amendments. This review did not reconstruct every tool read of every intermediate leg.

Evidence: [exact selected decision rows](../history-evidence/handler-decisions.tsv), [dated handler deliveries](../history-evidence/amendment-deliveries.jsonl), and [notes-B4 at the B4c source commit](https://github.com/jparrieta/r-place/blob/3bbef7ebf1a23d8ea0d051c18d0ef83dab9037f0/aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/out/notes-B4.md). The delivery's label can name the outgoing leg; its text names the incoming leg.

## Release access

This is a private review build. Saved reading pages, their Markdown and JSONL downloads, and the PlaceNL example replace recorded participant handles with pixel-stream IDs: `base64(SHA1(username))`, preserving case, with no salt. Profile links are removed. These are linkable pseudonyms, not anonymity; quoted text remains searchable. The original bundles, transcripts and old manual are unchanged. They would be visible to anyone who could reach an unprotected static host. A private download repository does not protect a public copy of those pages.

Public release has not been approved. Ethics and data-protection clearance, or an explicitly approved publication treatment, remains a release decision. Original research files retain their verified bytes. Reading manifests distinguish original-source hashes from hashes of the derived copies. Private reviewer hosting needs access control for the whole static site as well as interviews. A link token for an interview does not protect static records. No public host or guest service is enabled by this build.

[Machine-readable history and evidence hashes](../history.json). New records extend the catalogue; earlier checkpoint identities, accepted bundles and source recipes remain unchanged. Additional runtime proofs, when available, name the exact executable tested.
