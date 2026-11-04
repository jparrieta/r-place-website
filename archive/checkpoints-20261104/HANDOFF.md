# Checkpoint handoff for the website handler

Target length: under 800 words.

## Scope and authority

There are **63 validated selections**: 35 aggregator final-stage or final-leg checkpoints through E2b, plus coding-close and R6 for 14 communities. The 52 older routes remain public. Eleven later full-snapshot supplements remain draft assets. Validation and publication are different states.

J requested this handoff in the website repository's archive on a separate branch. Do not merge into `main`, change Pages settings or publish the draft release under this handoff. The live site has not been changed. Start with `PROMPT-FOR-WEBSITE-HANDLER.md` and `STATUS.json`.

## E2b directly from r-place

J prefers the existing repository files. The preferred E2b command restores the published workspace and saved analyst conversation from immutable commit `f27566528a5102d944c6ddc3d2e2e98b839cbab8` in `jparrieta/r-place`. It downloads no checkpoint archive or supplement. The small launcher contains code and metadata only.

`E2b-PUBLISHED-GIT.json` pins the session, transcript checksum, source path, model and effort. `tools/e2b_from_rplace.py` checks every published Git object, verifies the conversation, prompts for a separate Claude login if needed, and opens a native interview fork in Claude CLI. It keeps new interviews outside the research checkout. Hooks, MCP, web, write tools and historical system-prompt snapshots are disabled through the existing interview isolation settings.

This is **the published workspace, not the complete local snapshot**. The 390 files outside the Git mapping include older conversations, local settings, bookkeeping and the original RUN.json version. The published RUN.json remains unchanged. The exact E2b conversation already passed a native interview test with the full snapshot. The direct-Git test verified 68,035 published files and links, loaded the E2b history in Claude CLI and reached the question prompt. Files remained unchanged after exit. No new model reply was requested for this route. First use can show Claude's terminal setup prompts.

## Startup commands and prerequisites

`COMMANDS.md` gives 63 exact Bash commands with their provider. E2b uses the direct-Git launcher. Other commands use the complete reviewed launcher through authenticated draft access. They restore files and open the local interview page; questions start model calls. Prepared public-release commands remain separately in `release-metadata/ALL-COMMANDS.md`, with inactive URLs until publication is approved.

Readers need Python 3.11 or newer, Git and the supported provider CLI. The complete launcher also needs GitHub CLI; draft access requires an authorized repository account. E2b requires Claude Code 2.1.300 and 22 GiB free. Other checkpoints retain their recorded or explicitly verified compatible versions. Do not substitute another model, provider or fresh session when a gate fails.

## Files for integration

- `release-metadata/catalog.json`: all 63 entries, identities, source bindings and compatibility proofs. `ready` means validated for the runtime, not permission to advertise draft downloads.
- `release-metadata/SOURCES.json`: immutable original Git commits for the full-snapshot route.
- `release-metadata/ASSETS.json`: all 20 draft assets pinned by ID, size and SHA-256.
- `code/`: runtime source and the narrow original-Git transport fix. Merge into the current source; do not overwrite the current site with an older build.
- `evidence/`: compact verification records, without private new replies or login data.

The eleven draft boundaries are D4a-08, D5a-41, D5b, D6a-18, D6b, E1b-08, E1c, E1d, E1e, E2a and E2b. Intermediate pauses and community D2/D3 returns are outside this selection. E2b's public-Git alternative does not publish its full-snapshot supplement.

## Retrieve full-snapshot runtime files

From the extracted handoff directory:

```bash
python3 tools/verify_handoff.py
python3 tools/download_assets.py --only launcher
```

The verified launcher is about 103 MB. Its SHA-256 is `1ac51f8ec770f43e0a29e65fe34e22de6e66443b423987691308f594cb71ad2c`. Use `--only all` to fetch all prepared assets, about 5.3 GB. Downloads stay outside Git. If draft access fails, report it; do not publish to gain access.

## Checks and limits

All eleven later archives passed member and source checks. All new assets passed download readback. The full E2b route restored 68,737 files with matching hashes and modes, without archive fallback. Transport now fetches missing Git objects in batches of at most 1,024 before checkout, avoiding GitHub's oversized lazy-fetch failure.

On 4 November, 28 community interviews and one E2b interview ran freshly. The other 34 selections retain earlier proofs. Seven older aggregator proofs ran on Linux, not freshly on this Mac. Recorded symlink-mode limits remain. These checks establish restoration and interview access, not scientific validity.
