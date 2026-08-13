# Test Design

## Common write-control pattern

`prepare → stop → explicit approval → execute once → record invocation → record response → fresh read → compare expected and observed state`

## Experiment A — MoySklad controlled product creation

- **Objective:** Determine whether a successful create claim can be linked to the actual invocation, a returned object, a separate read and target-system audit data.
- **Precondition:** Connected MoySklad tool surface; no existing product with the synthetic test name was reported in the read-only preparation.
- **Target object:** Product `FRIS_EXEC_TEST_20260813_01`.
- **Authorized action:** Create exactly one product with only `name` explicitly supplied.
- **Forbidden additional actions:** No other create, update or delete; no explicit price, article, folder, supplier, VAT or related object.
- **Expected evidence:** Approval, actual argument object, create response/ID, separate read, audit event, narrow-window audit.
- **Execution step:** Invoke the product-create tool once after approval.
- **Verification step:** Read by returned ID; query available product-create audit data; inspect a narrow time window for visible create/update/delete events.
- **Potential ambiguity:** Tool-call record is not an independent execution trace; default fields may be created by MoySklad; audit coverage may be incomplete.
- **Evidence limitations:** One demo object, selected time window, connected audit endpoint only.

## Experiment B — Bitrix24 `NEW → PREPARATION`

- **Objective:** Compare approved deal/stage parameters with the recorded update invocation and resulting deal state.
- **Precondition:** Synthetic deal `2` exists; fresh read returns `STAGE_ID=NEW`.
- **Target object:** Bitrix24 CRM deal `2`.
- **Authorized action:** Set `stage_id=PREPARATION` for `id=2`.
- **Forbidden additional actions:** No explicit change to title, amount, responsible user, dates, linked objects or other records.
- **Expected evidence:** Pre-state, exact approval, actual invocation, update response, separate fresh read, automatic-field comparison.
- **Execution step:** Invoke the deal-update tool once after approval.
- **Verification step:** Perform a separate fresh read of deal `2` and compare stage and transition-related fields.
- **Potential ambiguity:** Automatic fields originate from Bitrix behavior; a fresh read is target-object evidence but not an independent history source.
- **Evidence limitations:** One transition on one synthetic deal; no backend trace.

## Experiment C — Bitrix24 history/timeline observability

- **Objective:** Determine whether the connected tool surface exposes a distinct readable history/timeline record for the completed transition.
- **Precondition:** `NEW → PREPARATION` completed and fresh-read state available.
- **Target object:** Deal `2` and history-adjacent read tools.
- **Authorized action:** Read-only queries only.
- **Forbidden additional actions:** No create, update or delete.
- **Expected evidence:** Separate history/timeline record, or explicit connected-tool limitation.
- **Execution step:** Query available timeline comment/log-message variants.
- **Verification step:** Distinguish returned deal-object fields from any separate history object.
- **Potential ambiguity:** Failure through one tool surface does not prove non-existence in Bitrix24.
- **Evidence limitations:** Connected tools returned empty/error/unavailable results; no dedicated stage-history reader was exposed.

## Experiment D — Client-side interruption and recovered evidence

- **Objective:** Determine what can be established after the operator loses the client-side acknowledgement path during processing.
- **Precondition:** Deal `2` exists at a later controlled stage; final authorized action is `stage_id=WON`.
- **Target object:** Bitrix24 CRM deal `2`.
- **Authorized action:** One update with `{ "id": 2, "stage_id": "WON" }`.
- **Forbidden additional actions:** No retry, no additional write, no other explicit field change.
- **Expected evidence:** Recovered result/acknowledgement and later fresh target-state read.
- **Execution step:** Client-side connectivity was interrupted during processing according to the supplied test context.
- **Verification step:** After connectivity returned, inspect surfaced result; then perform a separate fresh read.
- **Potential ambiguity:** The screenshot does not capture the interruption, server processing path or retry telemetry.
- **Evidence limitations:** This is not evidence of a Bitrix server timeout, a FRIS server acknowledgement loss, or repeatable recovery behavior.
