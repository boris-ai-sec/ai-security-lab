# Lab Objectives and Status Vocabulary

Status: **REPOSITORY SCOPE / REFERENCE**

## Objectives

The lab is used to produce and retain bounded technical evidence about:

- RAG retrieval quality, source handling, and evidence boundaries;
- agent authority, approval binding, execution verification, and retry ambiguity;
- prompt injection and context contamination;
- observability, trace completeness, and incident reconstruction;
- the limitations of available evidence and the next evidence needed for a decision.

The intended output is evidence that can inform a human risk or readiness assessment. A laboratory result is not itself a production approval or a general claim about a model, platform, or system.

## Status vocabulary

| Label | Meaning in this repository |
|---|---|
| `CURRENT` | A current reviewer-facing entry point or recently committed public package |
| `HISTORICAL` | Retained earlier work; useful for provenance but not the preferred current entry point |
| `REFERENCE ONLY` | Context or an environment snapshot, not an authoritative setup or result |
| `RETAINED` | Preserved evidence or documentation that must not be silently rewritten or discarded |
| `CORRECTED` | Historical material remains present, while an explicit correction governs interpretation |
| `SYNTHETIC TEST DATA` | Non-client data created for controlled laboratory use |
| `GENERATED OUTPUT` | Output produced by a run or tool; it is not reusable source code by itself |

Package-specific README, manifest, validation, provenance, and limitation files define the authoritative status for that package.

## Non-objectives

This repository is not intended to provide:

- a production AI application;
- a reusable universal benchmark;
- a certification or compliance decision;
- a guarantee of safety, security, reliability, or readiness;
- general conclusions beyond the tested evidence and operating conditions.
