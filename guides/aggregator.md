# 3. Open the existing aggregator handler

Open a third Codex or Claude chat. Name it **Aggregator handler** and give it the collection handoff and the coding handler's output locations. Paste:

```text
You are the aggregator handler for my r/place study. Use the existing handler in https://github.com/jparrieta/r-place. Read FOR-AGENTS.md, aggregator/FOR-AGENTS.md and aggregator/handler/HANDLER.md first, including its memory and open items.

Read my collection and coding handoffs. Obtain any missing instrument folders and required inputs, record their versions, and prepare a separate run using the chosen platform's existing controller. Follow its build and acceptance procedure before opening analysis. Keep your head, decisions and progress on disk. Deliver the prescribed stage cards and inputs, check each close, and preserve the declared checkpoints. Bring research decisions and unresolved failures to me. Do not operate the repository's historical run or rewrite its protocol.
```

The aggregator handler already exists. Choose its existing Claude or Codex route and confirm that route's requirements. The chat coordinates the run; the aggregator works in its own stage or leg session.

**Start with:** checked community outputs, the census and the context required by the instrument.

**Do:** the handler prepares a separate run, checks the build and opens stages in order. The aggregator reads, codes, builds a model, returns it to cases, and writes the resulting account.

The **aggregator** develops the interpretation. The **handler** is a separate coordinating agent that operates the run and brings decisions to the researcher. A **stage card** gives the full instructions for one stage; an **agent reading key** lists what the agent must read.

**Keep:** each stage’s outputs, reasoning record and declared checkpoints. A stage is a part of the analysis; legs divide larger tasks within it.

**Advance when:** the stage’s outputs and checks meet its contract and the handler records the close. The aggregator owns the interpretation.

## Starting from communities already coded

You can open this handler directly with checked coded inputs; a new collection is not required. Use the [start-from-coded reading key](../agents/aggregator.html) to inventory the inputs and boundaries before launch. It covers the pristine starting folder, original leads for D2, the field package or recorded decision for C4, and proposal material for E2.

The 14 shared community checkpoint pairs do not supply every original community coder for the 705-community frame. Missing community coders limit later returns, even if the earlier aggregator stages can run. The handler requests the missing packages and records the last runnable stage. It does not replace a saved original community coder with a fresh agent.

## Return the model to communities

At D1 close, give `out/handoff-D/HANDLER.md` to the chat that holds the original community leads. It acts as the **adaptation handler**. At D3b, give that chat `out/handoff-D/recheck/HANDLER.md` so it can return to the D2 sessions. The researcher dispatches the verdict fleet through `dispatch.sh`. The aggregator does not replace the saved community leads.

## Full instructions

[Handler protocol](../sources/handler.html) · [Build and run](../sources/how-to-run.html) · [Agent reading key](../agents/aggregator.html)

## Stage map

Choose a stage for its purpose, expected outputs, full card and saved checkpoints. Status describes the indexed publication, not a live process.
