# Checkpoint interviews

Choose a community or an aggregator checkpoint. Each card shows what was saved and which routes are available.

**Read saved outputs** opens selected narrative files from that exact checkpoint in the browser, with provenance and hashes. It needs no model login. **Read the record** opens the original transcript or close receipt on GitHub. **Chat Locally** expands setup beneath the selected checkpoint, with one command first and a step-by-step guide below. The stage map and description stay on the page. **Chat Online** opens a new tab, asks for reviewer sign-in, and opens the selected checkpoint when its server is available. Your research page stays open. Hosted research access is still awaiting deployment and runtime checks.

Original GitHub transcripts and private downloads require repository access. The selected saved-output reading pages on this site do not. A GitHub “Page not found” response can mean you lack access. The local **Open the interview service on this computer** link works on this computer only. Phone access requires a separately configured private HTTPS service; it is not enabled by opening this local page.

A complete bundle contains the conversation and the filesystem at that checkpoint, plus a manifest and runtime provenance. Git history or a transcript alone is not that bundle. Historical files stay separate from current research and from other interviews.

For communities, the four slots are the 5.6 coding close, the 6.1 local model, the global return D2 and the re-check D3. The design forks D2 from the matching original case-lead checkpoint and resumes that D2 session at D3. For the 14 shared communities, archive and native-session evidence places the D2 fork at the coding close, before R6. R6 and D2 are separate continuations of that close. The D3 return records retain the D2 session IDs. [Inspect the lineage and model-setting evidence](history.html#models-and-lineage).

| Milestone | What the agent has done |
|---|---|
| Coding close | Consolidated codes, themes and a case account. |
| Local model, R6 | Built a standalone account of the community's organizing. |
| Global return, D2 | Compared its community with the shared model. |
| Re-check, D3 | Reconsidered its response against the revised shared model. |

Each aggregator stage shows its latest completed checkpoint first. **Other checkpoints in this stage** opens earlier legs and recovery closes. A direct link to an earlier checkpoint opens that list automatically. Each checkpoint retains its source commit, date and availability; none reports live progress.

## What an interview can and cannot do

Ask about an interpretation, its evidence, a discarded alternative or an unresolved question. The restored agent may be mistaken. Its answers are new interview responses, not original research findings or a guarantee that internal computation has been preserved.

The service creates a separate native conversation. It gives that conversation read access to the selected historical files, no research controls, no web access and no access to other checkpoints. Ending the interview removes its disposable workspace; export the interview first if you want to keep it.

Activity messages do not establish which sources were read. Compare an answer's references with the original files. [Audit the retained evidence](audit-evidence.html) distinguishes saved records from new interview claims.

Interviews depend on continued access to compatible models and software. A saved checkpoint alone cannot guarantee future resumption. Outputs and transcripts remain readable without a model call. The paper proposes an open-weight rerun with archived weights to reduce this dependency; that rerun is not yet part of the shared baseline. [Long-term access and resource limits](project.html#keeping-the-baseline-usable).

Reading pages replace participant handles with the pixel stream's IDs. They still contain Reddit text; original bundles and transcripts retain usernames. This private build is not approved for public hosting; [release access limits](history.html#release-access) apply to the whole site. Provider processing applies when you run an interview. Credentials are never included. Original records stay intact.

## Return to an online interview

After sign-in, **Open interviews** lists the chats still held by the server. Return opens the same interview, with its messages and historical files, without restoring again. Repeated clicks on Chat Online also reuse the existing chat for that checkpoint.

Close interview removes only that disposable copy. Export first to keep the conversation; typing `/exit` opens the same close controls. Closing a browser tab leaves the interview available until its idle timeout. An open chat or Open interviews page keeps it active; without either page connected, it expires after 30 minutes. A server restart also ends access. The pilot has three interview slots and restores one checkpoint at a time.

## Open an interview on your computer

Select **Chat Locally** on the checkpoint card and paste its single command into Terminal on a Mac or Linux computer. It downloads the launcher, verifies its SHA-256 and every packaged file, prepares a private Python environment, and checks the supported runtime. It asks for GitHub and model-provider sign-in when needed, then opens the interview page. You still complete sign-in yourself. No question is sent automatically.

Python 3.11 or newer, Bash, curl, Git, GitHub CLI and the checkpoint's supported native CLI must already be installed. The command reports missing tools or an unsupported version; it does not change system software or substitute another runtime. Community archive reading installs `zstandard` in the launcher's private environment when needed. The launcher is stored under `~/.local/share/rplace-interview-launchers/`; interview state remains under `~/.rplace-interviews/`. Subsequent launches reuse verified files and valid logins.

Below the single command, **Or follow these steps** gives the separate download, login and launch steps. Select Chat Locally again to close the instructions. Ask your question in the local interview page. Export before ending if you want to keep the new conversation.

The default route currently requires private repository access. If the study owner has already supplied the exact verified bundle, use the **Already downloaded the checkpoint?** command instead. That explicit offline route skips GitHub restoration; it still requires the provider login and supported runtime. The site cannot grant access. Expect a computer setup step, archive download time and disk space as listed by the launcher, rather than an immediate browser-only interview. [Launcher version and SHA-256](../downloads/launcher.json). A missing login or unsupported CLI stops the interview and reports the reason.

[Agent instructions for the three access routes](../agents/interview.html).
