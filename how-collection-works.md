# How collection works

Collection gathers the public record of the event once, checks it and freezes it, so that every later reader works from the same copy. A Collection handler, a model conversation with shell access, follows the data recipes. The census of communities is not a download: it is a set of research judgements, each recorded with its evidence.

## Its instructions

- [The Collection handler's brief](agents/collection.html): what it reads, what it checks, what it hands over, and when it stops.
- [The data recipes](sources/data-README.html): seven stores, the scripts that build each, where each comes from and what was tested.
- [Start from raw data](agents/download.html): the reading key, with the inputs and access a collection needs.

## The steps

| Step | What it gives | Size in the study |
|---|---|---|
| 1. The pixel record | every placement, with the placer's hashed name, and the table of usernames behind the hashes | 16,559,897 placements |
| 2. The atlas | 1,473 artworks, their outlines and the subreddits they name, checked byte for byte against the study's copy | 675 KB |
| 3. The placer accounts | everything each placer wrote on Reddit in 24 days around the canvas; days at the archive's pace, resumable | 1,101,801 accounts, about 14 GB |
| 4. Venues, placers only | what placers wrote in each subreddit | 50,936 venues, 13.6 GB |
| 5. Venues in full | everything anyone wrote in each subreddit in the 24 days; days, resumable | 24,093 venues, about 51 GB |
| 6. Pixels per artwork | every placement inside each artwork's outline, and a 30-minute panel per artwork; about four minutes | 23,058,857 rows, 1.1 GB |
| 7. Hourly pixels per community | placements in each community's region by hour, by anyone and by its own members; about a minute | 67,907 rows, 1.4 MB |
| 8. The census | which credited subreddits count as communities: [from 2,796 subreddits to 705 communities](results/population-record.html#census) | judgements with evidence |
| 9. Freeze and hand over | every file hashed; `HANDOFF-collection.md` records each input's path, source, bytes, hash, time window, version, checks, gaps and status | |

Every text record came through the public Arctic Shift archive, which serves Reddit's record as it was ingested at the time, before later deletions. The pixel record is Reddit's own release; the atlas is the 2017 Place Atlas.

## When it stops

The handler stops a route when access is missing, archived bytes are unavailable, a check fails or the choice of collection is unresolved. It names the missing store and the next action. It never infers a census decision and never counts an incomplete download as ready.

[How it was done, with r/PlaceNL beside it](study/record.html) · [Run it](guides/download.html)
