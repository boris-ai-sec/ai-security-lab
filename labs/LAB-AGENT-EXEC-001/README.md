# LAB-AGENT-EXEC-001

## Execution Evidence and Approval-to-Action Integrity in Connected Business Systems

Controlled FRIS demo experiments with MoySklad and Bitrix24
Date: 2026-08-13
Package status: **PUBLICATION-READY**
Publication status: **APPROVED FOR PUBLIC GITHUB RELEASE**

## Objective

Examine what evidence is available when an agent performs controlled state-changing actions in connected business systems, and whether approved parameters can be compared with the recorded invocation and resulting target state.

## Systems Under Test

- FRIS demo interface and connected tool surface
- MoySklad synthetic product object
- Bitrix24 synthetic CRM deal, ID `2`

## Why This Matters

An agent statement that an action is complete is a claim. Stronger evidence can come from the recorded invocation, the target-system response, a separate fresh read, and—when available—a target-system audit source. These sources are related but not automatically independent.

## Evidence Model

`Claim → Invocation → Acknowledgement → State Change → Verification`

Approval binding is evaluated as:

`Approved Scope → Actual Invocation → Target-System State`

## Experiment A — MoySklad Controlled Product Creation

One synthetic product, `FRIS_EXEC_TEST_20260813_01`, was approved for creation with only the `name` field explicitly set. The recorded invocation contains only that field. A returned product ID, a separate fresh read and an available MoySklad audit event identify the same object. A narrow-window audit exposed one create event and no visible update/delete events, subject to explicit coverage limits.

## Experiment B — Bitrix24 Approval-to-Action Transition

Deal `2` was freshly read at `NEW`. The approved transition limited the write to `id=2` and `stage_id=PREPARATION`. The recorded invocation contains those two values, the update response reports success, and a separate fresh read returns `STAGE_ID=PREPARATION`, `PREVIOUS_STAGE_ID=NEW` and automatic Bitrix fields.

## Experiment C — Bitrix24 Observability Boundary

Read-only attempts did not obtain a distinct readable stage-history/timeline record through the connected toolset. The deal object's own transition fields remained available. They are target-system data but are not a separate independent history source.

## Experiment D — Client-Side Interruption and Recovery Evidence

During the final controlled write, the operator reports that client/browser connectivity was interrupted while processing continued. The recovered result view later exposed a single `WON` invocation and a definitive successful response. A separate fresh read returned the deal at `WON` with `PREVIOUS_STAGE_ID=FINAL_INVOICE`, `CLOSED=Y` and success semantics.

The connection loss itself is not captured in the screenshots. The evidence therefore supports the recovered result and final state; the interruption remains supplied test context. It does not establish a Bitrix server timeout or general recovery guarantees.

## Key Results

- The MoySklad chain links approved scope, recorded invocation, returned ID, fresh read and target-system audit data for one synthetic object.
- The Bitrix `NEW → PREPARATION` chain allows direct comparison of planned/approved parameters, recorded invocation, acknowledgement and later target state.
- Bitrix target-object fields were available, while a distinct readable stage-history/timeline source was not obtained through the tested tools.
- The final recovered-result frame and separate fresh read are consistent with one successful `WON` update; the screenshot set does not independently prove the interruption itself.

## What the Results Do Not Prove

- Production behavior or platform-wide reliability
- Complete backend event visibility
- The quality or external authorization of the approval decision
- A server-side timeout or acknowledgement loss
- Absence of all unobserved side effects
- Security certification, penetration-test result, or full FRIS assessment

## Evidence Index

Thirteen selected derived artifacts are indexed in [EVIDENCE_INDEX.md](EVIDENCE_INDEX.md). The complete 48-file inventory and sequence reconstruction are in [EVIDENCE_INVENTORY.md](EVIDENCE_INVENTORY.md) and [TEST_SEQUENCE_MAP.md](TEST_SEQUENCE_MAP.md).

## Reproducibility Notes

The lab documents an evidence-review method, not an automated test harness. A comparable run should preserve:

1. pre-action target state;
2. explicit approval with exact parameters;
3. recorded actual invocation;
4. target response;
5. separate fresh read;
6. target audit evidence when accessible;
7. limitations and missing evidence.

Synthetic identifiers and timestamps will differ in another run. Tool availability and observability may also differ by account, integration version and connected surface.

## Curation Summary

- RAW screenshots reviewed: **48** (`15 MoySklad`, `33 Bitrix24`).
- Selected for this lab: **13** derived artifacts (`6 MoySklad`, `7 Bitrix24`).
- Selected separately for website: **7** compact fragments.
- The remaining RAW frames were setup-only, identifier-heavy, redundant/supporting, or unnecessary to reconstruct the principal experiments.
- Redaction performed: actor/user identifier and IP-like value removed from the selected MoySklad audit copy.
- Missing direct evidence: client-side disconnection screen; complete acknowledgement frames for some intermediate Bitrix transitions; independent readable Bitrix stage history.
- Core experiment chronology is reconstructable. Some intermediate-transition chronology is incomplete; final filename order is not used as sole evidence because target timestamps and local capture names use different display/timezone conventions.

## Publication and Demo Boundary

Framework review, publication sanitization, and Project Owner release authorization are complete for this curated public Lab. See [PUBLICATION_BOUNDARY.md](PUBLICATION_BOUNDARY.md) and [PROVENANCE.md](PROVENANCE.md).
