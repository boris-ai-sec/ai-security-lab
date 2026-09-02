# Proposed Release Notes — v0.1.0

Proposed title: **Operational AI Risk & Evidence Lab — First Public Repository Release**

Release status: **candidate documentation only; no tag or GitHub Release has been created.**

The candidate release source is the complete repository tree produced if the Repository Maturity V0.2 draft pull request is approved and merged into `main`. A later human approval must identify the exact `main` commit before any tag or release is created.

## Purpose

This repository provides bounded, externally inspectable laboratory evidence for RAG retrieval boundaries, agent authority and execution integrity, observability, workflow reconstruction, and controllability questions.

It is not a production product, certification framework, complete penetration test, audit opinion, or general safety/readiness claim.

## Current reviewer path

The primary bounded path is [`LAB-RAG-EXT-002`](../labs/LAB-RAG-EXT-002/README.md), including two public run records, a public evidence manifest, a validation record, and a Git-object checksum manifest. The path can be inspected with Git and the Python standard library; the source Langflow/Qdrant environment is not required for the integrity check and is not fully reproducible from this repository.

Related current packages cover retrieval-boundary comparison and agent execution/failure semantics:

- [`LAB-RAG-EXT-001`](../labs/LAB-RAG-EXT-001/README.md)
- [`LAB-AGENT-EXEC-004`](../labs/LAB-AGENT-EXEC-004/README.md)
- [`LAB-AGENT-EXEC-003`](../labs/LAB-AGENT-EXEC-003/README.md)

## Validation

The candidate includes deterministic, credential-free checks for selected SHA-bound evidence packages, JSON parsing, Markdown relative links, Python syntax, and licensing/workflow consistency. The checks operate on byte-exact Git objects where evidence checksums are involved.

## Licensing

Only the original standalone source files explicitly listed in [`LICENSE_SCOPE.md`](../LICENSE_SCOPE.md) are offered under the MIT License. Evidence records, screenshots, professional documentation, generated outputs, synthetic data, mixed notebooks, and third-party material are not included in that MIT grant.

## Important limitations

- Claims remain bounded to the published evidence and tested conditions.
- Historical notebooks do not share one supported runtime or full reproduction contract.
- Raw source environments and credentials for external-system experiments are not published.
- `LAB-AGENT-EXEC-003` retains a historical publication-package discrepancy: five of six checksum entries verify, while the retained `README.md` checksum does not. The four substantive case records and evidence manifest verify. The README and its mismatching checksum entered the repository in the same original publication commit, and no legitimate replacement source was found in Git history or the available workspace/archive search.
- The retained checksum discrepancy is disclosed and machine-checked as an exact known condition; any additional or changed mismatch fails validation.

See the root [`README.md`](../README.md), [`REQUIREMENTS.md`](../REQUIREMENTS.md), and package-level limitation records before drawing conclusions.
