# Correct Answer, Wrong Retrieval Boundary — Langflow + Qdrant

## Primary conclusion

**The controlled experiment produced the same correct final answer in both runs while retrieval-boundary status changed from FAIL under unfiltered retrieval to PASS under an explicit tenant filter.**

**Final-answer correctness did not establish retrieval-control correctness.**

## Run A — Unfiltered Retrieval

**The unfiltered retrieval crossed the declared tenant boundary.**

The allowed tenant was `tenant_a`, but the retrieved set included a `tenant_b` document. That cross-tenant content propagated through the Parser/context path into the final prompt.

```text
TENANT RETRIEVAL BOUNDARY: FAIL
FINAL ANSWER CORRECTNESS: PASS
```

The final answer was correct, but the retrieval-control boundary was not preserved.

## Run B — Explicit Tenant Filter

**The explicit `tenant_a` filter preserved the declared retrieval boundary.**

The filtered retrieval excluded `tenant_b` records while producing the same correct final answer.

```text
TENANT RETRIEVAL BOUNDARY: PASS
FINAL ANSWER CORRECTNESS: PASS
```

## Why it matters

A RAG evaluation that checks only the final answer can miss a retrieval-control failure.

The experiment separates two questions:

```text
Was the answer correct?
≠
Was retrieval constrained to the allowed evidence boundary?
```

The same correct answer was compatible with both a failed and a passed retrieval-boundary result.

## Public evidence records

| Run | Record |
|---|---|
| Unfiltered retrieval | [PUBLIC_RUN_RECORD.json](01_unfiltered/PUBLIC_RUN_RECORD.json) |
| Explicit tenant filter | [PUBLIC_RUN_RECORD.json](02_filtered/PUBLIC_RUN_RECORD.json) |

## Scope

Controlled validation of the tested tenant-boundary mechanism in a Langflow + Qdrant reference environment. Production-wide tenant isolation and ranking-score causality were not evaluated.

The public records are derived sanitized evidence projections. Raw flow exports, provider credentials, local service configuration, and internal validation artifacts remain outside the public package.
