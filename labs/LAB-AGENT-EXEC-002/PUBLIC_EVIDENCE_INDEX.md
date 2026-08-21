# Public Evidence Index

| ID | File | Original source | Public role | Supports | Limitation |
|---|---|---|---|---|---|
| P1 | [P1_APPROVAL_OBJECT.png](evidence/P1_APPROVAL_OBJECT.png) | supplement `205731` | Approval object | Explicit approved target, operation, baseline, requested change, and scope | Approval alone is not execution integrity |
| P2 | [P2_PARAMETER_DRIFT.png](evidence/P2_PARAMETER_DRIFT.png) | prior `142347` + `140208` | Parameter-drift evidence | `Approved A ≠ Attempted B` | Target rejected the write; no side effect occurred |
| P4 | [P4_BOUND_INVOCATION_ACK.png](evidence/P4_BOUND_INVOCATION_ACK.png) | supplement `205937` | Invocation + acknowledgement | Exact bound invocation and acknowledgement | Not fresh verification |
| P5 | [P5_FRESH_T1.png](evidence/P5_FRESH_T1.png) | supplement `210023` | Fresh verification | Fresh post-write target state | Same integration surface; not independent UI corroboration |

P3 was deliberately removed from the approved public set and is not restored here. P6 / Bitrix UI corroboration is also excluded.

Case D remains bounded as: approved baseline differed from fresh state; execution did not proceed; causal blocking mechanism remains inconclusive.
