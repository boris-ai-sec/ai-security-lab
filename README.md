# AI Systems Risk & Evidence Lab

This repository contains bounded laboratory evidence for RAG, agent, execution-integrity, and observability questions. It is intended for technical inspection and evidence review—not as a production AI platform, a complete penetration test, or a certification environment.

The governing rule is:

```text
CLAIM STRENGTH <= EVIDENCE STRENGTH
```

## Start here: one bounded inspection path

The clearest current reviewer path is the SHA-bound Langflow + Qdrant retrieval-quality package:

```text
README.md
→ tools/verify_git_object_checksums.py
→ labs/LAB-RAG-EXT-002/README.md
→ two public run records
→ public evidence manifest
→ validation record
→ explicit scope boundary
```

Prerequisites: Git and Python 3.9 or newer. No model, vector database, API credentials, or external service is required for this inspection path.

From the repository root:

```bash
python tools/verify_git_object_checksums.py labs/LAB-RAG-EXT-002/SHA256SUMS.txt
```

Expected result:

```text
PASS 5/5 Git object checksums verified
```

Then inspect, in order:

1. [Primary result and metric definitions](labs/LAB-RAG-EXT-002/README.md)
2. [Unfiltered retrieval record](labs/LAB-RAG-EXT-002/01_unfiltered/PUBLIC_RUN_RECORD.json)
3. [Filtered retrieval record](labs/LAB-RAG-EXT-002/02_filtered/PUBLIC_RUN_RECORD.json)
4. [Evidence manifest](labs/LAB-RAG-EXT-002/PUBLIC_EVIDENCE_MANIFEST.json)
5. [Validation record](labs/LAB-RAG-EXT-002/VALIDATION_RECORD.md)

This is a **bounded evidence inspection and integrity check**, not a full experiment replay. It establishes that the retained public files match their declared Git-object SHA-256 values and lets a reviewer inspect the approved comparison. It does not reproduce the source Langflow/Qdrant environment, prove production tenant isolation, establish multi-query retrieval quality, or support general RAG safety claims.

## What the repository contains

| Path | Status | Purpose |
|---|---|---|
| [`labs/LAB-RAG-EXT-002/`](labs/LAB-RAG-EXT-002/) | CURRENT / SHA-BOUND PUBLIC EVIDENCE | Most recent committed retrieval-quality comparison |
| [`labs/LAB-RAG-EXT-001/`](labs/LAB-RAG-EXT-001/) | CURRENT RELATED EVIDENCE | Retrieval-boundary comparison with answer correctness held constant |
| [`labs/LAB-AGENT-EXEC-004/`](labs/LAB-AGENT-EXEC-004/) | CURRENT / SHA-BOUND PUBLIC EVIDENCE | ServiceNow portability and failure semantics |
| [`labs/LAB-AGENT-EXEC-003/`](labs/LAB-AGENT-EXEC-003/) | PUBLIC EVIDENCE / README CHECKSUM DISCREPANCY NOTED | HubSpot execution, stale-state, parameter-drift, and target-drift cases; 5/6 package checksum entries verify, with the mismatch confined to the retained `README.md` checksum |
| [`labs/LAB-AGENT-EXEC-001/`](labs/LAB-AGENT-EXEC-001/) and [`002`](labs/LAB-AGENT-EXEC-002/) | RETAINED VALIDATION EVIDENCE | Earlier execution-evidence and approval-binding studies |
| [`labs/LAB-RH-02A/`](labs/LAB-RH-02A/) | RETAINED / CORRECTED | Phoenix telemetry baseline; historical raw output is retained and correction evidence governs interpretation |
| [`notebooks/`](notebooks/) and [`15_workflow_telemetry_openinference_phoenix.ipynb`](15_workflow_telemetry_openinference_phoenix.ipynb) | HISTORICAL / EXPERIMENTAL | Earlier local-model, prompt-injection, RAG, governance, and telemetry notebooks |
| [`screenshots/`](screenshots/) | RETAINED SUPPORTING OUTPUT | Visual records associated with historical experiments |
| [`data/clean_docs/`](data/clean_docs/) | SYNTHETIC TEST DATA | Synthetic input used by earlier laboratory work |
| [`requirements.txt`](requirements.txt) | REFERENCE ONLY | Historical environment snapshot; not a repository-wide supported install contract |

See [Lab objectives and status vocabulary](LAB_OBJECTIVES.md) and [requirements and reproduction limits](REQUIREMENTS.md).

## Current evidence packages

- [LAB-RAG-EXT-002](labs/LAB-RAG-EXT-002/) separates retrieval-boundary control, boundary-eligible Precision/Recall, and raw ranking in a single-query controlled comparison.
- [LAB-RAG-EXT-001](labs/LAB-RAG-EXT-001/) shows that the same correct answer can coexist with failed or passed retrieval-boundary control.
- [LAB-AGENT-EXEC-004](labs/LAB-AGENT-EXEC-004/) retains PASS, FAIL, and INCONCLUSIVE cases for execution, authority, invariant, and retry-ambiguity semantics.
- [LAB-AGENT-EXEC-003](labs/LAB-AGENT-EXEC-003/) retains controlled HubSpot execution and drift cases. Five of six package checksum entries verify. The mismatch is confined to the retained `README.md` checksum; the four substantive case records and the evidence manifest verify. The README and its mismatching checksum were introduced together in original publication commit `34f679ff158b76ca593c990ef875d7246131fb06`. No historical evidence should be modified as part of this normalization.

Each package defines its own evidence basis, validation status, and limitations. Package-level wording takes precedence over any short repository summary.

## Evidence discipline

The intended reasoning chain is:

```text
Experiment
→ retained evidence
→ evidence quality and completeness
→ bounded conclusion
→ explicit limitations
→ next evidence request
```

Important boundaries:

```text
Model output ≠ finding
Configuration ≠ runtime behaviour
Log entry ≠ complete trace
Correct answer ≠ correct retrieval boundary
Observed target state ≠ proven controlled execution
Lab PASS ≠ production readiness
```

The repository does not independently provide:

- formal certification or an audit opinion;
- legal or regulatory conclusions;
- a complete penetration test;
- production-wide security, reliability, readiness, or safety claims;
- evidence for untested models, configurations, workflows, tenants, or operating conditions.

## Setup and execution scope

There is no single supported runtime for every historical notebook and lab. Use the package-specific instructions and pinned files where they exist. The recommended external-review path above is intentionally inspection-only and uses only Git plus the Python standard library.

Do not install the root [`requirements.txt`](requirements.txt) as a default repository setup step. It is retained as an older environment snapshot. See [REQUIREMENTS.md](REQUIREMENTS.md) before attempting other paths.

## Licensing and reuse status

Selected original standalone source files are available under the MIT License only as explicitly listed in [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md); the standard text is retained at [`LICENSES/MIT.txt`](LICENSES/MIT.txt). Laboratory evidence, assessment records, screenshots, professional documentation, publication artifacts, generated outputs, synthetic data, mixed notebooks, and ambiguous material are outside that MIT grant.

Third-party materials, product interfaces, and dependencies remain subject to applicable third-party rights and license terms and are not relicensed by this repository. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for the bounded inventory and exclusions.

## Security and release status

Repository-specific security and integrity concerns can be reported through the routes in [`SECURITY.md`](SECURITY.md). This does not make the repository owner a security contact for third-party products.

Versioned release notes are maintained under [`docs/`](docs/), including the bounded [`v0.1.0` release notes](docs/RELEASE_NOTES_V0.1.0.md). GitHub Releases is the authoritative source for whether a version has been published. [`CHANGELOG.md`](CHANGELOG.md) records unreleased repository changes.

## Repository status

This is an active laboratory repository with retained historical material and newer governed public evidence packages. No GitHub Release or production tag is implied by a package being present in the repository.

Author: **Boris Abuzov — AI Risk & Governance Consultant** · [Website](https://borisabuzov.com) · [GitHub](https://github.com/boris-ai-sec)
