# Closed validation summary — HABR003 V0.1

Accepted disposition (2026-10-11): **VALIDATION PASS WITH NON-BLOCKING LIMITATIONS — READY FOR PUBLICATION DEVELOPMENT**. Publication gate open; no blocking validation issue. This summary projects the closed validation record, not a newly executed study.

| Accepted fact | Result |
|---|---|
| Frozen specification | V0.2; SHA-256 84f9c79a44b407de97ef6cf17654aaee666b28b37ee96dac7e9f1b5dd3a160af |
| Implementation | V0.1; PostgreSQL SELECT FOR UPDATE reservation |
| Source provenance | Content-addressed snapshot c2328a15864cfbbb761c01d618324e5e03447416cd0d50313b2dd9d30081988a |
| Existing acceptance tests | 44 PASS; 0 failures/errors/skips |
| Supplementary frozen acceptance groups | 6 PASS, including actual gateway process restart retaining charged RESERVED |
| Complete canonical suites | 2: initial and additional fresh-runtime suite |
| Additional main-scenario repetitions | 10 groups / 30 runs |
| Formal scenario runs | 38 valid / 0 invalid / 0 failed |
| Fresh-runtime repeat | PASS — same validation operator |
| Independent raw/persisted recomputation | PASS |
| Implementation/spec modified during validation | NO / NO |

The two approved claims are:

> In the controlled concurrent scenario, each vulnerable request passed the enforcement check against the grant state it actually observed. Because admission was not atomically tied to consuming shared authority before consequential execution, aggregate execution exceeded the human-granted cumulative limit.

> Pre-execution atomic reservation preserved the tested cumulative authority invariant under the controlled scenarios.

The source review excluded alternative runtime mechanisms: no pre-charge in vulnerable admission, no post-effect capacity recheck, no lost-update assignment, no double charge; corrected reservation/lifecycle/charge commit atomically before ERP, without a process mutex, queue, SERIALIZABLE substitute, injected zero values or ERP-side grant enforcement. Destination totals came from independently read complete durable ERP records. Planner boundary and read-only write rejection checks passed.

## Evidence selection and validation history

Published raw bundles: sequential e19bb65, vulnerable e466251, corrected e304011, resource eef688a. All eight files per bundle are original bytes and retain original timestamps, operation/order IDs, quantities, lifecycle/revisions, labels and input hashes. The [38-run results index](evidence/FORMAL_RUN_INDEX.json) retains every approved formal run identity/result; 34 additional raw bundles remain private. This public subset supports direct inspection of the four representative runs; it is not a public raw recomputation of all 38 runs.

Two earlier preflight attempts were inconclusive because Git provenance was absent and Docker's Linux engine was unavailable. The expressly authorized exact content-addressed snapshot resolved source provenance; a later working runtime enabled the formal gate. Those records were preserved, not overwritten.

One external-validator interruption initially marked e304011 FAIL under a strict Windows-finished-time >= Linux-final-observation assertion; the canonical run itself exited 0. The difference was 0.292540 seconds. The unsupported cross-clock assumption was corrected, the original failed assessment retained, and the **same untouched bundle** revalidated without rerunning it. This is not an unexplained failed canonical scenario. The representative bundle retains the original timestamps.

An auxiliary acceptance preparation also failed before executing any case because a mounted external script could not import lab. Its failed preparation was retained; only the external invocation was corrected, then a different fresh auxiliary project passed all six groups. There were two auxiliary preparation attempts, one failed preparation and one successful execution. These are distinct from the 38 formal scenario counts and do not represent a repaired implementation defect.

## Non-blocking limitation and scope

Windows-host and Linux-VM timestamps must not be treated as a globally synchronized clock. Read/hook sequences, within-runtime timing, persisted matching operations/orders and synchronous canonical reader/planner staging establish the tested causal chain. Absolute host-vs-container timestamps do not support global latency/simultaneity claims. The limitation remains visible and does not undermine the approved controlled results.

Other frozen limits: synthetic grant and Demo ERP; deterministic planner/no LLM; one resource/unit and supplier allow-list; logically separate databases on one server; unprivileged planner boundary excluding host/Docker administrator; no expiry/dynamic revocation/overlapping grants; no general recovery or availability architecture. Repeated forced scheduling is neither natural failure-frequency measurement nor exhaustive concurrency proof. Same-operator fresh-runtime repetition is not independent human reproduction. No production, formal assurance, standards-compliance or universal agent-system claim is made.
