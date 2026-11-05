# AIMM Pillar 2 — Executable Authority Evidence Pilot (T4)

**Concept Note V0.2 — 5 November 2026**

**Status:** Proposed collaborative experiment. Not an official OWASP AIMM validation or approved workstream deliverable.

## 1. Objective

Extend the existing ARC × ACS comparison with a bounded experiment that connects declaration consistency, runtime enforcement, and independently observed persisted business effects.

The initial scope is **T4: underlying tool-definition drift after approval**, with unchanged ARC declarations.

This is distinct from the separate **T9 behavior-drift case**, in which server behavior changes while the underlying definition digest remains unchanged. T9 is outside this initial pilot; detecting T4 definition drift does not establish detection of T9 behavior drift.

The goal is to produce reproducible evidence relevant to selected AIMM Pillar 2 §5.1 authority and execution-control criteria, without claiming general standards compliance.

The test matrix and evidence requirements below are proposed experimental criteria. They do not define, amend or replace AIMM normative requirements.

## 2. Research question

When an underlying tool definition changes after approval but the declared operation remains unchanged:

- Does ARC G1 detect any declaration-level inconsistency?
- Does the runtime enforcement component detect the changed authority basis before the relevant commitment boundary?
- What operation, if any, actually reaches the protected ERP?
- Can the observed effect be reconciled against the originally approved operation?

Each layer must be evaluated separately.

## 3. Existing technical basis

**ARC:** Published Agent Role Contracts 1.0.1 and the merged T4 fixture.

**ACS:** Existing Guardian conformance and authority-basis-drift comparison.

**ERP laboratory:** Existing PostgreSQL-backed Shared Cumulative Authority Lab, with an authorization gateway, Demo ERP, isolated runtime, and independent evidence reader.

The original laboratory is a validated bounded experiment, not an existing end-to-end ARC/ACS integration. Any adapters required for this pilot will be implemented and identified separately.

## 4. Initial test matrix

| Case | Controlled condition | Observation to establish |
|---|---|---|
| C0 — Baseline | Original declaration, definition and approved request | ARC passes; runtime permits the authorized operation; intended ERP effect is recorded |
| C1 — Declared change | Declared action changes; prior binding reused | ARC returns `G1_SUBJECT_MISMATCH`; test orchestration does not dispatch the rejected case |
| C2 — Definition drift, enforced | Underlying definition changes; declarations remain unchanged; runtime binds the definition | ARC expected miss; runtime detects drift and prevents the protected effect |
| C3 — Definition drift, declaration-only | Same change; runtime checks declaration but not underlying definition | ARC expected miss; runtime behavior and any divergent ERP effect are measured |

C0 is the baseline control; C1 is the negative control for declaration consistency. C3 provides the declaration-only comparison control for C2. The table states observations to establish, not results already obtained.

A controlled test adapter will make the underlying definition change consequential to execution, rather than merely changing version metadata.

The mutation mechanism, exact authority scope, test operation and expected effects must be fixed before implementation.

## 5. Evidence requirements

Each run should retain:

- Pinned source revisions and dependency identities.
- Original and modified declarations/definitions, including hashes.
- Approved action, parameters, operation ID and correlation ID.
- ARC G1 output and diagnostics.
- Runtime authorization request, decision and enforcement outcome.
- Evidence of the actual dispatch or verified absence of dispatch.
- Initial and final ERP records obtained through the independent read-only component.
- Raw observations, run manifest, verification output and explicit limitations.

Results should distinguish **PASS, FAIL, EXPECTED_MISS, NOT_RUN and INCONCLUSIVE**.

A declaration PASS is not runtime authorization. A runtime ALLOW is not execution evidence. Persisted state is evidence of an observed effect, not by itself proof of a uniquely authorized causal path.

## 6. Proposed responsibilities — for discussion

**Boris Abuzov:** Provide an isolated copy of the PostgreSQL-backed laboratory, define the ERP execution/effect scenarios, and prepare the persisted-state evidence package.

**t-iida:** Review ARC G1 scenarios, interpretation of subject binding and alignment with the existing ARC 1.0.1 fixture.

**Malachi Kopman:** If interested, review ACS Guardian test semantics, commitment-boundary checks and alignment with the existing conformance comparison.

**Joint review:** Agree on the test contract, expected outcomes, evidence interpretation, reproduction procedure and attribution before publication.

These roles are proposals, not commitments.

## 7. Deliverables

1. Frozen test specification and test-to-requirement mapping.
2. Isolated reproducible laboratory package.
3. Raw and independently recomputed observations.
4. A results matrix separating ARC, runtime and ERP findings.
5. A bounded technical report documenting both detected and missed controls.

The initial experiment will not modify the published historical HABR003 evidence package.

## 8. Scope boundaries

Synthetic operations and isolated infrastructure only.

The pilot will not establish production security, universal bypass resistance, complete implementation conformance, official AIMM certification or independent third-party qualification.

A separate observer reading persistent ERP state is stronger than relying on a Guardian's own success claim, but does not eliminate all common-infrastructure trust assumptions.

## 9. Next step

Review the scope and test contract with t-iida and Malachi before implementation.

If technically useful and reproducible, the finished evidence package may later be proposed to the AIMM Pillar 2 workstream for independent consideration.

**Reference material:**

- [ARC fixture — published ARC 1.0.1 declaration column, pinned revision](https://github.com/suirindo/agent-role-contracts/blob/873b4104a95e443ba22367cf8378deb7dcbe6cfd/experiments/external-evaluation/acs-conformance/README.md).
- [ACS comparison](https://github.com/Noctis-dev1/acs-conformance/blob/main/COMPARISON.md) ([reviewed snapshot](https://github.com/Noctis-dev1/acs-conformance/blob/1b086a4f3058760e5c32412cb6e5f4175d24f64a/COMPARISON.md)).
- [ACS T1–T10 scenario definitions — T4 and separate T9 case, reviewed snapshot](https://github.com/Noctis-dev1/acs-conformance/blob/1b086a4f3058760e5c32412cb6e5f4175d24f64a/SCENARIO_T1_T10.md).
- [ERP laboratory — Shared Cumulative Authority Lab](https://github.com/boris-ai-sec/ai-security-lab/tree/main/labs/shared-cumulative-authority) ([reviewed snapshot](https://github.com/boris-ai-sec/ai-security-lab/tree/59c189cac6c6e696811b2acef916865bdfb2bf41/labs/shared-cumulative-authority)).
