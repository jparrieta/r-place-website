# Run log

Every stage of the study in one place: when it ran, how long it took, how many sessions it used, and its tokens. All dates are 2026 and all times UTC. The records behind this page are in the research repository ([github.com/jparrieta/r-place](https://github.com/jparrieta/r-place); private, access on request).

## Community coding

| Phase | Dates | Communities | Model | Tokens |
|---|---|---|---|---|
| Earlier contracts, v16 to v29 | 18 Aug to 5 Sep | 347 communities in 462 runs, later redone | Claude Opus 5 (323 runs), Claude Sonnet (20), unrecorded (112) | not recorded |
| Final coding, v30 to v32 | 7 Sep to 4 Oct | 738 finished, the 705 among them | gpt-5.6-sol: 5,097 agents at medium effort, 65 at extra high | 15.89 billion, cached input included |
| The aggregator's frame | 4 Oct | 705 | | |

The final coding finished 138, 128 and 133 communities in its first three weeks. The fourth week counts 339, but 326 of those are dated 30 September, the day a list of 299 earlier communities was redone, so that week's count may include records closed rather than coded. Coding hours were not logged.

## The return to the model

| Step | Dates | Communities | Model |
|---|---|---|---|
| D1, tasks prepared | 15 Oct, 15:54 to 19:49 | 705 | Claude Opus 5.5 |
| D2, first return | sent 15 Oct; compiled 16 Oct, 08:53 | 705 | gpt-6.1-sol |
| D3, re-check sent | 21 Oct, 12:40 | 705 | gpt-6.1-sol |
| D3, first batch back | by 21 Oct, 19:26 | 472; the account then ran out of tokens | |
| D3, second batch back | 22 Oct, 19:10 | all 705 | |

Tokens for the returns were not recorded.

## The aggregator, run claude-v43-1

Claude Opus 5.5 ran every stage, from 6 Oct 12:14 to 28 Oct 00:38: 21.5 days and 316 sessions. Session hours run from launch to close and include waits for our rulings. Tokens are in millions. The run's own counter, `RUN.json`, counts most calls two or three times; the figures in brackets are deduplicated counts, which exist for A1 to C3 only.

| Stage | Start | End | Session hours | Sessions | Cache read | Output |
|---|---|---|---:|---:|---:|---:|
| [A1, community notes](stages/A1.html) | 6 Oct 12:14 | 7 Oct 13:02 | 18.9 | 57 | 7,550 (3,482) | 12.9 (5.0) |
| [B1, third-order scheme](stages/B1.html) | 7 Oct 13:11 | 11 Oct 14:49 | 91.2 | 45 | 12,873 (5,961) | 37.0 (13.4) |
| [B2, pilot](stages/B2.html) | 11 Oct 14:57 | 12 Oct 14:09 | 7.5 | 12 | 978 (334) | 2.5 (0.7) |
| [B3, fleet](stages/B3.html) | 12 Oct 14:17 | 12 Oct 21:18 | 2.3 | 3 | 204 (63) | 0.8 (0.2) |
| [B4, adjudication and freeze](stages/B4.html) | 12 Oct 21:19 | 13 Oct 17:47 | 18.5 | 12 | 2,208 (1,066) | 18.3 (6.6) |
| [C1, structuring](stages/C1.html) | 13 Oct 18:17 | 14 Oct 00:56 | 5.8 | 11 | 1,086 (456) | 4.8 (1.7) |
| [C2, the loop](stages/C2.html) | 14 Oct 06:04 | 14 Oct 13:49 | 5.5 | 7 | 1,483 (753) | 3.5 (1.4) |
| [C3, literature](stages/C3.html) | 14 Oct 13:59 | 14 Oct 15:16 | 1.2 | 3 | 278 (116) | 0.9 (0.2) |
| [C4, the field](stages/C4.html) | 14 Oct 22:35 | 14 Oct 23:03 | 0.5 | 1 | 57 | 0.2 |
| [C5, account](stages/C5.html) | 14 Oct 23:30 | 15 Oct 15:00 | 5.8 | 21 | 1,205 | 3.3 |
| [D1, return build](stages/D1.html) | 15 Oct 15:54 | 15 Oct 19:49 | 3.9 | 1 | 108 | 0.3 |
| [D2, labelers and verdicts](stages/D2.html) | 16 Oct 08:59 | 16 Oct 10:21 | 1.4 | 1 | 56 | 0.2 |
| [D3, adjudication and re-check](stages/D3.html) | 16 Oct 11:00 | 24 Oct 10:54 | 171.6 | 59 | 12,796 | 55.7 |
| [D4, the tree](stages/D4.html) | 24 Oct 11:39 | 26 Oct 22:05 | 7.0 | 8 | 821 | 2.0 |
| [D5, branch accounts](stages/D5.html) | 25 Oct 21:01 | 27 Oct 03:20 | 23.4 | 42 | 2,618 | 7.8 |
| [D6, the retelling](stages/D6.html) | 27 Oct 03:28 | 27 Oct 15:41 | 6.7 | 19 | 1,014 | 2.9 |
| [E1, audit](stages/E1.html) | 27 Oct 16:56 | 27 Oct 23:52 | 4.5 | 12 | 511 | 1.5 |
| [E2, feedback](stages/E2.html) | 27 Oct 23:55 | 28 Oct 00:38 | 0.7 | 2 | 99 | 0.2 |
| **Total** | 6 Oct | 28 Oct | **376.5** | **316** | **45,947** | **154.9** |

Notes:

- D4 and D5 overlap on 26 October.
- Three D3 sessions that waited on our rulings hold 104 of the 376.5 hours. The median session took 34 minutes.
- Deduplicating at the A1 to C3 ratios (2.18 for cache read, 2.78 for output) gives an estimated run total of about 21,000 million cache-read tokens and 56 million output tokens. This is an estimate.
- Other models: DeepSeek V4.1 Flash made 1,573 calls at B2 and B3 (139.6 million prompt and 44.6 million completion tokens), and an audit at E1 used 3.2 million tokens at a cost of US$1.73.

## Accounts

The work ran on a Claude subscription (the aggregator and the earlier coding), a Codex account (the final coding and the returns) and OpenRouter (DeepSeek).

## Sources

In the research repository: the coding handler's `STATUS.tsv`, `CODING-PROGRESS.json` and `PRIOR-RUNS.tsv`; the run's session log, `handover-events.log` and `RUN.json`; the token analyses in the aggregator handler's memory; the stage notes `notes-D2.md` and `notes-D3.md`; and the git history of the run's branch.
