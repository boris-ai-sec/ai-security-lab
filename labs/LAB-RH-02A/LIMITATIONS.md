# Limitations and Prohibited Claims

## Verified

This laboratory verifies local Phoenix telemetry, trace persistence, and graceful fallback when the collector is unavailable.

## Not verified

This laboratory does not verify Qdrant retrieval, metadata filtering, source-boundary enforcement, EXP-RAG-001, production deployment, client-system behavior, or operational readiness.

## Known ambiguity

The degraded sidecar records observability_status unavailable, error_type collector_unreachable, and export_ok true.
Until Build clarifies the field semantics, export_ok true must not be treated as proof that spans reached Phoenix.

## Publication boundary

Publication requires sanitization, Build review, and Project Owner approval.
