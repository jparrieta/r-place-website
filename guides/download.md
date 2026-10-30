# 1. Open the Collection handler

Open a new Codex or Claude chat that can work with files and a shell. Name it **Collection handler**. Use an empty working folder for this study. A chat without file or shell access cannot run the collection scripts.

[Download the Collection handler brief](../agents/collection.md), attach it to the chat, then paste this prompt:

```text
You are the Collection handler for my r/place study. Read the attached Collection handler brief first. Obtain the instrument from https://github.com/jparrieta/r-place into a separate working folder, record its version, and follow that brief and the repository's data recipes.

Help me choose between the archived study inputs and a fresh collection. Obtain and check the required raw24, pixel, atlas and other inputs. Ask only for missing access or research decisions. Keep your head and action log on disk. Leave a checked handoff for the existing coding handler. Do not start coding or aggregation.
```

The handler can download the instrument and data. You do not need to assemble the folders first. If repository access is missing, grant it or provide the downloaded instrument. Credentials belong in the provider's sign-in flow, never in the prompt.

## Get the instrument

Open the [research repository](https://github.com/jparrieta/r-place), then choose **Code → Download ZIP**, or clone it if you use Git. Repository access is currently required. If GitHub shows “Page not found”, request project access; the site cannot grant it.

To use the original starting point, download the [verified pristine package](https://github.com/jparrieta/r-place/releases/download/checkpoint-cloud-test-20261024/pristine-start.tar.gz), then extract it in an empty folder. This is the initial instrument and prepared run at commit `f6588ae37d807884af5fdcc9f7e27a03b4ff253a`. It has no aggregator conversation. The archive SHA-256 is `1755f467ec0e2a3753a616b5eb19ccfa5b5e1af187a61ceef4ec449274a89b4c`. Give this folder to the existing aggregator handler when starting from the prepared inputs. A new collection still begins with the Collection handler.

The repository holds the instruments, scripts and recorded outputs. Large data stores and resumable checkpoint bundles are separate downloads. The **interview launcher** opens saved checkpoints; it does not install the research workflow.

Research runs need a computer with a shell, Python 3.11, the dependencies the package lists, and the model access required by your chosen platform. Use the current [handler instructions](../agents/aggregator.html) for the run you build. The pristine package passed all eight offline checks in a fresh Python 3.11 environment on the author's Mac, with its documented numpy, scipy and pandas dependencies. The harness used a simulated model. Provider access, recollection and installation on another operating system remain untested.

## Prepare the records

**Start with:** the public pixel record, atlas, Reddit archives and the study’s census decisions.

**Do:** follow the collection recipes, preserve the selected time window, then build each community’s record. Downloading source data does not recreate the judgments that define the census.

**Keep:** the prepared records, source versions, time window and census decisions.

**Advance when:** the recipes’ checks pass and the inputs and versions are recorded.

The handler distinguishes **the archived study inputs** from **a new collection**. Some archived stores still have no published download link. Recollection can lose records removed since the study. It is not a byte-for-byte replacement. The handler records these gaps instead of silently substituting inputs.

## Open the next chat

The Collection handler leaves `HANDOFF-collection.md` with input paths, versions, checks and unresolved gaps. Open the [existing coding handler](communities.html) and give it that file. Keep this collection chat for data questions.

## Read further

- [Full data recipes](../sources/data-README.html).
- [Full Collection handler brief](../agents/collection.html).
- [Complete data reading key](../agents/download.html).

Next: [code communities](communities.html).
