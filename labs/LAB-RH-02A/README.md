# LAB-RH-02A — Phoenix Telemetry Baseline and Graceful Fallback

## Status

- Laboratory status: PASS
- Gates completed: A, B, C, D
- Evidence origin: synthetic_harness
- Verification scope: controlled_local_test
- Applicability: telemetry_transport_diagnostic_only
- GitHub portfolio candidate: yes
- Publication authorized: no

## Technical question

Can a local RAG Harness:

1. export synthetic diagnostic traces to a locally hosted Phoenix instance;
2. preserve trace hierarchy across a Phoenix restart;
3. continue execution and preserve authoritative file artifacts when Phoenix is unavailable;
4. record the observability limitation without presenting the diagnostic as RAG experiment evidence?

## What was tested

### Gate A — controlled Phoenix installation

Phoenix was installed in an isolated local service directory with pinned dependencies and a dedicated SQLite database.

### Gate B — local service operation

Phoenix HTTP and gRPC endpoints were verified on loopback interfaces only.

### Gate C — connected telemetry path

A synthetic telemetry diagnostic created:

- one parent span;
- two child spans;
- a file-based run package;
- a telemetry sidecar;
- a visible trace in Phoenix.

The trace remained available after Phoenix restart.

### Gate D — graceful fallback

Phoenix was stopped before running the same diagnostic.

The Harness:

- completed successfully;
- created the run package;
- created the telemetry sidecar;
- recorded `observability_status: unavailable`;
- recorded `error_type: collector_unreachable`;
- preserved `status: completed`;
- did not mark the run as RAG experiment evidence.

## Reproduction materials

- `source/pyproject.toml`
- `source/uv.lock`
- `source/scripts/telemetry_smoke.py`
- `source/telemetry/manager.py`
- `source/telemetry/__init__.py`

## Evidence

- `evidence/gate-c/`
- `evidence/gate-d/`
- `screenshots/`

## Important boundary

This laboratory verifies the telemetry mechanism only.

It does not verify:

- Qdrant retrieval;
- metadata filtering;
- source-boundary enforcement;
- client-system behavior;
- EXP-RAG-001;
- production readiness;
- AI system safety or governance effectiveness.

See `LIMITATIONS.md` and `results/LAB-RH-02A_RESULT.md`.
