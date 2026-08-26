# Agent Harness Portability and Failure Semantics — ServiceNow

## Primary conclusion

**The ServiceNow series demonstrates that the Agent Harness evidence model remained usable on a second external business platform and preserved meaningful PASS, FAIL, and INCONCLUSIVE semantics across execution, authority, invariant, and retry-ambiguity cases.**

## Findings

### Cross-Platform Portability

The same Agent Harness evidence model produced a complete PASS on a ServiceNow execution path, including fresh post-action verification.

### Authority Boundary Failure

The Harness detected that the actual invocation occurred outside the recorded effective authority boundary.

### Invariant Failure

The Harness detected that a material field approved to remain unchanged changed in the verified T1 state.

### Retry Ambiguity

The retry produced an observed target state, but acknowledgement and duplicate-risk provenance remained unresolved.

`C6 ACKNOWLEDGEMENT / VERIFICATION RELATIONSHIP: UNKNOWN`

`C8 RETRY IDENTITY / DUPLICATE-RISK BOUNDARY: UNKNOWN`

Harness verdict:

`INCONCLUSIVE`

The experiment does not establish that a duplicate side effect occurred. It establishes that the available evidence could not resolve execution attribution and duplicate-risk provenance.

## Why it matters

The series separates several properties that can otherwise be collapsed into a single execution claim:

```text
execution
→ authority
→ approved invariants
→ acknowledgement
→ retry identity
→ fresh outcome verification
→ claim confidence
```

A successful target-state observation alone is not sufficient to establish controlled execution when authority, invariant preservation, acknowledgement, retry identity, or execution provenance remains unresolved.

## Public evidence records

| Case | Record |
|---|---|
| Cross-Platform Portability | [PUBLIC_CASE_RECORD.json](01_portability/PUBLIC_CASE_RECORD.json) |
| Authority Boundary Failure | [PUBLIC_CASE_RECORD.json](02_authority_boundary/PUBLIC_CASE_RECORD.json) |
| Invariant Failure | [PUBLIC_CASE_RECORD.json](03_invariant_failure/PUBLIC_CASE_RECORD.json) |
| Retry Ambiguity | [PUBLIC_CASE_RECORD.json](04_retry_ambiguity/PUBLIC_CASE_RECORD.json) |

## Scope

Controlled validation of the tested Agent Harness mechanisms in a ServiceNow reference environment. Production-wide effectiveness and general ServiceNow security were not evaluated.

The public records are derived sanitized evidence projections. Raw API responses, response headers, cookies, instance-specific references, internal state artifacts, and immutable source snapshots remain outside the public package.
