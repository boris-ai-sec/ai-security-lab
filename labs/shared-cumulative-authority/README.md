# Shared Cumulative Authority — Reproducible Agentic Authorization Experiment

This bounded experiment tests one shared cumulative human grant across multiple concurrent actions. The simulated human grant authorizes **100 units** of COMP-17 across SUP-A/SUP-B/SUP-C. A deterministic scripted planner proposes **three orders of 40**. Execution means durable order creation in a Demo ERP; no LLM, shipment or payment is involved.

## Why local ALLOW decisions are insufficient

A per-request ALLOW can be consistent with the grant state that request actually read while the aggregate consequence exceeds the grant. In the tested vulnerable configuration, three actual reads of charged authority **0** preceded a disclosed post-read barrier release; each request then admitted 40, and ERP execution totaled **120** against **100**.

> For shared cumulative authority, admission to execution must be tied to an atomic transition of shared authority-accounting state before consequential execution.

## Experimental scenarios

| Scenario | Unique ALLOW / DENY | ERP total D | Charged Q | C / R / U |
|---|---|---:|---:|---|
| Sequential vulnerable | 2 / 1 | 80 | 80 | 80 / 0 / 0 |
| Instrumented concurrent vulnerable | 3 / 0 | 120 | 120 | 120 / 0 / 0 |
| Corrected concurrent reservation | 2 / 1 | 80 | 80 | 80 / 0 / 0 |
| Wrong resource | 0 / 1 | 0 | 0 | 0 / 0 / 0 |

The wrong-resource reason is DENY_RESOURCE_NOT_IN_GRANT. Corrected rejection is DENY_CAPACITY after two committed reservations; the denied supplier need not be deterministic. Q=C+R+U; destination effects are not added to Q a second time.

## Vulnerable mechanism

Real unlocked authority read → capture snapshot → local capacity decision → durable **ADMITTED_UNRESERVED** binding without charge → ALLOW → ERP execution → durable success → guarded COMMITTED transition and atomic increment of the current charged quantity. There is no pre-execution reservation, lost-update replacement write or fresh limit check after the effect. Repeated completion cannot charge the same operation twice.

The three-party scheduling hook follows each real read and precedes admission. It supplies no counter value or decision. This forces one disclosed interleaving; it does not measure its natural frequency.

## Corrected mechanism

At READ COMMITTED: BEGIN → **SELECT grant_balance FOR UPDATE** → validate → create **RESERVED** and charge authority in the same transaction → confirmed COMMIT → ALLOW → ERP execution outside the reservation transaction. Unknown outcomes remain charged. Destination operation IDs are idempotent; changed payloads conflict. No application mutex, queue or SERIALIZABLE redesign substitutes for the database reservation.

## Reproduction and inspection

Use [REPRODUCE.md](REPRODUCE.md) for the actual Python/Docker setup, unchanged canonical commands and expected outputs. [Frozen specification V0.2](EXPERIMENT_SPEC_V0.2.md) is byte-identical to the approved design; its NOT EXECUTED wording describes the freeze-time state, not the later validation.

[Representative evidence](evidence/EVIDENCE_INDEX.json) includes one complete eight-file retained bundle per scenario. [All 38 approved run IDs/results](evidence/FORMAL_RUN_INDEX.json) are listed compactly; the remaining 34 raw bundles are intentionally not public. Code/source mapping is in [provenance](provenance/code-correspondence.json). [MANIFEST.sha256](MANIFEST.sha256) binds public files.

## Validation status

**VALIDATION PASS WITH NON-BLOCKING LIMITATIONS — READY FOR PUBLICATION DEVELOPMENT.** Completed 2026-10-11: **44 tests PASS**, **38 formal scenario runs / 38 valid / 0 invalid / 0 failed**, two complete suites including a fresh-runtime suite, ten additional repetitions of the three main scenarios, and independent raw/persisted recomputation PASS. Six additional frozen acceptance groups passed, including actual gateway process restart with a charged RESERVED operation. No new experiment or runtime test campaign was performed for this publication. See [VALIDATION_SUMMARY.md](VALIDATION_SUMMARY.md).

## Limitations and scope

Windows-host and Linux-container clocks are separate domains: do not infer global causal ordering or latency from their absolute timestamps. Event sequences, within-runtime observations, committed records and the documented command sequence support the tested causal chain. This was a same-operator fresh-runtime repeat, not independent human reproduction.

The result is bounded to the disclosed synthetic grant, deterministic workload, forced schedule, Demo ERP and trusted infrastructure. Authority/ERP databases are logically separate on one PostgreSQL server. Host/Docker administration is outside the unprivileged planner boundary. Expiry, dynamic revocation, overlapping grants and general recovery/availability are excluded. Unknown outcomes may retain unused capacity indefinitely.

This is not a general authorization framework, production architecture, security product, benchmark, formal verification or universal proof about agent systems. It establishes neither vulnerability prevalence, exhaustive schedules, natural failure frequency, LLM reasoning failure, complete security nor standards compliance. Exactly-once statements are limited to the tested operation-id/accounting contract.

## Fixed publication identity

Repository: `boris-ai-sec/ai-security-lab`; directory: `labs/shared-cumulative-authority/`.
Experiment **HABR003 V0.1**; frozen spec **V0.2**; validated source ID `c2328a15864cfbbb761c01d618324e5e03447416cd0d50313b2dd9d30081988a`.
Article tag: **shared-cumulative-authority-v1.0**, intended as an annotated fixed reference; never rewrite this publication tag.
Content publication commit: **d799447d6b9cf3859d1e4e6ff376bb713c22aa72**. The final tag targets a metadata follow-up that records this content commit; source, tests, specification and evidence remain unchanged. Resolve the final article commit with `git rev-parse shared-cumulative-authority-v1.0^{commit}` or the [tagged Git state](https://github.com/boris-ai-sec/ai-security-lab/tree/shared-cumulative-authority-v1.0). A Git-tracked README cannot embed its own commit hash; the final tag/commit is also recorded in the publication report.

Licensing follows the existing [repository scope](../../LICENSE_SCOPE.md); this publication adds no MIT grant. Dependencies retain their own terms.
