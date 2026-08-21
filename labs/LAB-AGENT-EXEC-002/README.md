# LAB-AGENT-EXEC-002 — Approval-to-Action Integrity and Execution-State Revalidation

**Framework disposition:** approved with boundary
**Environment:** controlled synthetic workflow using n8n, a read-only AI agent path, deterministic orchestration, and Bitrix24 synthetic tasks
**Publication scope:** bounded technical evidence study

## Question

What must remain bound between human approval and actual agent execution?

## What was observed

An earlier controlled run exposed an approval-to-action mismatch because approval and execution values were independently configured:

`Approved A ≠ Attempted B`

The attempted write was rejected by the target; **no side effect occurred**. The mismatch therefore demonstrates approval-to-invocation parameter drift, not a harmful business-state change.

## Corrective architecture

The corrected workflow used one **Action Envelope** to supply the tested material parameters to both human approval and execution, followed by a fresh pre-execution target read.

In this laboratory, that removed the **specific independently-hardcoded parameter-drift mechanism tested**. It does not establish that all possible parameters or execution paths are always bound.

See [the sanitized execution chain](architecture/sanitized_execution_chain.md).

## Final positive path

The final controlled path preserved distinct evidence stages:

`approval → fresh state → exact bound invocation → acknowledgement → fresh T1 verification`

The approved bound update was invoked, acknowledged by the target system, and then confirmed by a fresh target read.

**Invocation ≠ acknowledgement ≠ verification.**

## Important stale-state limitation

A separate run observed that the approved baseline differed from fresh pre-execution state and that the write was not executed. However, that run used an older extractor later shown capable of returning `undefined`, so the available evidence does not cleanly isolate why the FALSE branch was taken.

Canonical Case D wording:

**STALE-STATE CONDITION OBSERVED / WRITE NOT EXECUTED / CAUSAL BLOCKING MECHANISM INCONCLUSIVE**

This is not presented as a stale-state control-success claim.

## Public evidence

| ID | Exhibit | Role |
|---|---|---|
| P1 | [Approval Object](evidence/P1_APPROVAL_OBJECT.png) | Approved target, operation, baseline, requested change, and bounded scope |
| P2 | [Parameter Drift](evidence/P2_PARAMETER_DRIFT.png) | `Approved A ≠ Attempted B`; target rejection prevented side effect |
| P4 | [Bound Invocation + Acknowledgement](evidence/P4_BOUND_INVOCATION_ACK.png) | Exact bound invocation and target acknowledgement |
| P5 | [Fresh T1](evidence/P5_FRESH_T1.png) | Fresh post-execution target state |

See [PUBLIC_EVIDENCE_INDEX.md](PUBLIC_EVIDENCE_INDEX.md) for exhibit boundaries.

## Bounded conclusion

In this controlled workflow, independently configured approval and execution parameters produced an observed mismatch. In the corrected workflow, the tested material parameters used for approval and execution were sourced from one Action Envelope. The final controlled path then showed a bound invocation, target acknowledgement, and fresh post-execution verification as distinct stages.

Approval-to-action integrity therefore requires reconstructable linkage among:

`approved target / operation / material parameters → actual invocation → target response → fresh verified state`

This is a bounded observation from controlled synthetic runs, not a generalized agent-security or platform-reliability claim.

## Limitations

- controlled synthetic environment;
- narrow title-update operation;
- not a production-readiness validation;
- not a penetration test;
- not a platform security audit;
- not evidence that n8n or Bitrix24 is generally secure or insecure;
- not proof that every approval bypass is prevented;
- not proof that an agent cannot be manipulated;
- one successful path is not evidence of general reliability;
- Case D causal blocking mechanism remains inconclusive.

`controlled evidence ≠ production assurance`

`acknowledgement ≠ verified final state`

## Publication boundary

Only the four approved sanitized exhibits P1, P2, P4, and P5 are included here. The internal ZIP, RAW corpus, raw workflow JSON, P3, and P6 are not part of this public artifact.

See [PUBLICATION_BOUNDARY.md](PUBLICATION_BOUNDARY.md).
