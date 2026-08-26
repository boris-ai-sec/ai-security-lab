# Retrieval Quality Is Not Retrieval Control — Langflow + Qdrant

## Primary conclusion

**The two controlled runs had the same boundary-eligible Precision@K and Recall@K values, while boundary control and raw ranking differed.**

This separates three properties that are easy to collapse into one retrieval-quality claim:

```text
Retrieval Boundary Control
≠
Boundary-Eligible Retrieval Quality
≠
Raw Ranking Quality
```

## Controlled relevance set

The single-query baseline used a declared `tenant_a` boundary.

Within that boundary:

- `LF-B01-D01` was relevant;
- `LF-B01-D02` was not relevant.

The semantically relevant `tenant_b` document `LF-B01-D03` was boundary-ineligible and therefore excluded from the Precision/Recall relevance denominator. It was evaluated separately as boundary-control evidence.

## Boundary-Eligible Reciprocal Rank (BE-RR)

**BE-RR is the reciprocal of the raw rank of the first relevant document that is also eligible under the declared evidence boundary.**

The source evaluator defines the ranking metric as the reciprocal rank of the first boundary-eligible relevant document in raw retrieval order. Because this is a single-query baseline, BE-RR is reported per run; no Mean Reciprocal Rank is claimed.

## Run A — Unfiltered Retrieval

Run A returned three records. One was boundary-ineligible and occupied raw rank 1.

Boundary-eligible metrics:

```text
Eligible Precision@1: 1.0
Eligible Recall@1:    1.0
Eligible Precision@2: 0.5
Eligible Recall@2:    1.0
```

Raw ranking:

```text
First boundary-eligible relevant document: rank 2
Boundary-Eligible Reciprocal Rank (BE-RR): 0.5
Boundary-ineligible returned records: 1
```

**Run A achieved the same boundary-eligible Precision@K and Recall@K values as Run B while still failing the tenant boundary and placing the first allowed relevant document at raw rank 2.**

## Run B — Explicit Tenant Filter

Run B returned only boundary-eligible `tenant_a` records.

Boundary-eligible metrics:

```text
Eligible Precision@1: 1.0
Eligible Recall@1:    1.0
Eligible Precision@2: 0.5
Eligible Recall@2:    1.0
```

Raw ranking:

```text
First boundary-eligible relevant document: rank 1
Boundary-Eligible Reciprocal Rank (BE-RR): 1.0
Boundary-ineligible returned records: 0
```

**The explicit tenant filter preserved the same boundary-eligible Precision@K and Recall@K values while moving the allowed relevant document from raw rank 2 to raw rank 1.**

## Why it matters

A retrieval-quality score is only meaningful relative to the evaluation set and boundary definition used to compute it.

In this experiment:

```text
same eligible Precision / Recall
did not mean
same boundary behavior

and

same eligible Precision / Recall
did not mean
same raw ranking behavior
```

This is why retrieval-boundary control, relevance quality inside the allowed evidence space, and raw ranking should be evaluated separately.

## Public evidence records

| Run | Record |
|---|---|
| Unfiltered retrieval | [PUBLIC_RUN_RECORD.json](01_unfiltered/PUBLIC_RUN_RECORD.json) |
| Explicit tenant filter | [PUBLIC_RUN_RECORD.json](02_filtered/PUBLIC_RUN_RECORD.json) |

## Scope

Single-query controlled retrieval-quality baseline in a Langflow + Qdrant reference environment. Multi-query retrieval quality, nDCG, production retrieval quality, and production-scale ranking behavior were not evaluated.

The public records are derived sanitized evidence projections. Raw flow exports, provider credentials, local service configuration, caches, and internal validation artifacts remain outside the public package.
