# Prompt for the website handler

Target length: under 450 words.

Update the website's **Save checkpoint / Chat Locally** instructions using this handoff. Work from the current website source on a separate branch. Do not replace the site with the older runtime package, merge into main, deploy, or publish draft checkpoint assets without J's approval.

Read `HANDOFF.md`, `STATUS.json`, `COMMANDS.md` and the evidence. Run `python3 tools/verify_handoff.py` first. The selected set is 63 checkpoints: 35 aggregator boundaries through E2b, plus coding-close and R6 for 14 communities. Keep one main checkpoint per stage and other selected boundaries in the existing disclosure. Do not add intermediate pauses or community D2/D3 returns.

J wants the files to come from their original positions in `jparrieta/r-place`. E2b is already there. **Use its direct-Git command**, pinned to commit `f27566528a5102d944c6ddc3d2e2e98b839cbab8`, rather than the new full-snapshot supplement. It restores the published workspace and the unchanged E2b conversation, then opens a separate native Claude interview. Its small launcher contains code and metadata, not a repackaged research model. State that this is the published workspace; do not describe it as every file from the original local snapshot.

Put the exact one-command Bash instruction first, with a copy button, then the step-by-step route and prerequisites. Keep the stage identity visible. E2b currently opens Claude CLI; do not label it a browser chat. If integrating this route into the browser interview service, preserve its source distinction, isolation and checks, and test that integration before advertising it. Claude checkpoints must use Claude, community checkpoints Codex. A version or login failure must stop, not start a new analyst.

Keep publication honest: 52 older routes were already public. Eleven full-snapshot supplements are still draft. Commands that fetch the draft launcher require authorized GitHub access. Do not expose those as ordinary public reviewer downloads. E2b's direct-Git alternative does not publish its draft supplement.

Carry over the bounded Git-fetch fix from `code/originals-bounded-fetch.diff`. Preserve current page prose, design, source hashes, session identities and backend boundaries. Do not alter research files or copy new interview replies, credentials or local paths into the website.

Audit command copying, the 63 IDs/provider choices, downloads, draft-access errors, required disk space, original-session forking and stage links. Report which checks ran now versus retained earlier proofs. Return the proposed diff and any remaining blocker. This handoff branch itself must not change the live site.
