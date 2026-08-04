# Limitations and Prohibited Claims

## Verified

This laboratory verifies local Phoenix telemetry, trace persistence, and graceful fallback when the collector is unavailable.

## Not verified

This laboratory does not verify Qdrant retrieval, metadata filtering, source-boundary enforcement, EXP-RAG-001, production deployment, client-system behavior, or operational readiness.

## Known ambiguity

The degraded sidecar records observability_status unavailable, error_type collector_unreachable, and export_ok true.
Build clarified that export_ok was semantically incorrect and replaced it with export_attempted and export_succeeded.

## Publication boundary

Publication requires sanitization, Build review, and Project Owner approval.

## Correction status

The original degraded-run sidecar containing export_ok true is preserved as a historical raw artifact.

It is superseded for semantic interpretation by the correction evidence:

- Gate C: export_attempted true, export_succeeded true
- Gate D: export_attempted false, export_succeeded null

The correction resolves the ambiguity but does not expand the laboratory scope.
