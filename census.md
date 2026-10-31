# From 2,796 subreddits to 705 communities

The wider dataset holds 7.5 million posts and comments across 2,796 subreddits that took part in the event. The population model covers 705 of them. This page shows each step between the two, and marks the steps that took a judgement rather than a count. The judgements are recorded with their evidence in the census files, so each can be checked or reversed.

## Where the census starts

The census starts from the Place Atlas of the finished canvas (Place Atlas, 2017). Its curators outlined 1,473 artworks; 1,236 of them credit at least one subreddit. A subreddit that built an artwork and was overwritten before the freeze has no atlas entry, so the census undersamples failure (Denrell, 2003).

## The narrowing

One line per step. The artworks column counts the artworks that still credit at least one community on that line.

| Step | Artworks | Communities | Change | Why | Kind |
|---|---:|---:|---:|---|---|
| The 2017 atlas | 1,473 | | | | count |
| Credit a subreddit | 1,236 | | 237 leave | the entry names no subreddit | count |
| Credit a community | 1,227 | 763 | 9 artworks leave | user pages, r/all, a private subreddit, a Discord group, a name with no archive, a subreddit founded in 2022 | judgement |
| Named on the canvas | 1,227 | 767 | 4 join | the name is written on the final canvas and the community organized there in its own threads | judgement |
| Named as maker in a description | 1,227 | 776 | 9 join | an artwork's description credits it, and it took part in its own threads | judgement |
| A redirect kept as a row | 1,227 | 777 | 1 joins | r/TFLS points to r/TheFarLeftSide, which carries its artworks | judgement |
| Silent while the canvas was open | 1,200 | 748 | 29 leave | nothing posted while the canvas was open | count |
| Active only after the freeze | 1,193 | 741 | 7 leave | talk about a frozen canvas is not organizing on a live one | count and judgement |
| Text takes no part in the event | 1,164 | 709 | 32 leave | a community coder, or a check, read no talk about the event | judgement |
| No writing about the event while the canvas was open | 1,162 | 707 | 2 leave | r/lehigh wrote about it only after the freeze; r/upvote never did | judgement |
| The field, not a case | 1,161 | 706 | 1 leaves | r/place, where the communities met | judgement |
| Excluded | | **705** | 1 leaves | r/The_Donald (below) | judgement |

## The judgements

**Which community a link means.** The atlas names subreddits as annotators typed them. Each link was resolved by hand. Typos and folded names were assigned to the community the artwork belongs to: `hyperlightdrifer` to r/hyperlightdrifter, `Chelsea` to r/chelseafc. Links that name no community, such as r/all, user pages or a subreddit founded in 2022, were set aside.

**What counts as being there.** The criterion for evidence of coordination is writing about r/place while the canvas was open. Posting about something else in those hours is not enough, and talking about the frozen canvas afterwards is a different act from organizing to place pixels on a live one.

**Whether the text takes part in the event.** A word screen flagged likely talk about the event but never removed a community, because its markers are English and miss communities that name their artwork and not the event. A reading decided: a community coder's verdict that the record holds no talk about the event, or a recorded check of the flagged cases.

**The field.** r/place, the subreddit the event was named after, built no artwork of its own. It holds more posts than any other subreddit, and many of them narrate what the other communities did. It is the square where the communities met, not a case beside them. Its coding is under way, and it will be used to triangulate the model against an independent record.

**r/The_Donald.** We left out one community for two reasons. Reddit banned it in June 2020 for repeatedly hosting content that broke its rules, the first of which bans promoting hate based on identity or vulnerability (Reddit, 2020). Its exclusion also has little bearing on the model: its single artwork covered 108 pixels, within the lowest quartile of the census, and was largely overwritten before the canvas froze.

## What the 705 hold

The 705 communities wrote 2,130,302 posts and comments from the opening to a day after the freeze, and account for 90% of all pixel changes. Their community coders produced 115,388 first-order codes and 7,844 second-order themes. [The record in numbers](data.html) shows how they are distributed.

## Files

The census ships as `coder/census/` in the repository: `MASTER-census.csv` (one row per community, with its counts, verdicts and disposition), the link worksheets, `validations.jsonl` (every reading that decided a membership, with its evidence) and `ROOM-RULES.md` (the rules, stated). The counts can be rebuilt from the downloads; the judgements are inputs.

## References

Denrell, J. (2003). Vicarious learning, undersampling of failure, and the myths of management. *Organization Science*, 14(3), 227–243.

Place Atlas. (2017). *atlas-2017* [Data set]. GitHub. https://github.com/placeAtlas/atlas-2017

Reddit. (2020, June 29). Update to our content policy. r/announcements.
