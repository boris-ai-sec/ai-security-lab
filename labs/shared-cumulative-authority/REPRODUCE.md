# Reproduce HABR003 V0.1

## Requirements and supported evidence

Recorded validation used a Windows host, Docker Desktop 4.70.0 with Linux containers, Engine 29.4.0, Compose v5.1.2, host Python 3.14.4 and container Python 3.14.8. PostgreSQL was **18.3 (Debian 18.3-1.pgdg13+1)**. Compose selects postgres:18.3; Dockerfile selects python:3.14-slim. The Python base tag can advance: image IDs in the recorded manifests identify tested images, not bit-for-bit future rebuilds. Use package requirements.lock, not repository-root requirements.txt.

The existing documented Linux shell equivalents are shown below; no independent native-Linux-host validation is claimed. Docker's Linux engine must be running; `docker info`, `docker version` and `docker compose version` must succeed. No ERP/database port is published. Do not start this lab against an existing external database.

## Inspect the fixed article artifact without executing a new experiment

From repository root:

```sh
git checkout shared-cumulative-authority-v1.0
git rev-parse shared-cumulative-authority-v1.0^{commit}
python tools/verify_git_object_checksums.py labs/shared-cumulative-authority/MANIFEST.sha256 --commit shared-cumulative-authority-v1.0
```

This verifies Git-object bytes, including CRLF-preserved original source. The package .gitattributes disables EOL conversion. MANIFEST.sha256 lists every package file except itself. It is a byte-integrity check, not another runtime campaign or formal proof. Inspect [four retained bundles](evidence/EVIDENCE_INDEX.json), [validation summary](VALIDATION_SUMMARY.md) and [source correspondence](provenance/code-correspondence.json).

## Fresh checkout setup

```sh
git clone --branch shared-cumulative-authority-v1.0 https://github.com/boris-ai-sec/ai-security-lab.git
cd ai-security-lab/labs/shared-cumulative-authority
```

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
.\.venv\Scripts\python.exe -B -m lab.run build
.\.venv\Scripts\python.exe -B -m lab.run test
```

Existing shell equivalent:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -B -m lab.run build
.venv/bin/python -B -m lab.run test
```

Build generates fresh random per-service local secrets if missing. These are excluded from Git and the image build context. Do not publish generated secrets. The canonical test command starts a disposable PostgreSQL project, invokes the trusted lab.setup loader, creates separate authority/erp databases and role privileges, runs the original 44 tests, and removes only that new project's containers/networks/volume. Successful output is 44 passed; t<id>/ contains the test manifest and JUnit XML.

## Execute the original four scenarios

From this package directory, PowerShell:

```powershell
.\.venv\Scripts\python.exe -B -m lab.run smoke sequential --timeout 5
.\.venv\Scripts\python.exe -B -m lab.run smoke vulnerable --timeout 5
.\.venv\Scripts\python.exe -B -m lab.run smoke corrected --timeout 5
.\.venv\Scripts\python.exe -B -m lab.run smoke resource --timeout 5
```

For the existing shell equivalent replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`; module/arguments are identical. Each command creates a **new run ID, Compose project and PostgreSQL volume**. Setup loads the immutable grant, the independent reader verifies initial state, planner boundary probes execute, the planner sends real HTTP requests, and the independent reader captures settled authority and ERP orders before derivation/assertions.

Expected unique decisions / ERP / charged: sequential **2 ALLOW + 1 DENY / 80 / 80**; vulnerable **3 ALLOW / 120 / 120**, with three real zero-valued reads before release; corrected **2 ALLOW + 1 DENY_CAPACITY / 80 / 80**, R=U=0; resource **DENY_RESOURCE_NOT_IN_GRANT / 0 / 0**. Supplier admission order in corrected mode may vary.

The explicit finite timeout is an operational parameter, not a design constant. Timeout invalidates the instrumented run (503 INVALID_INSTRUMENTED_RUN), never business DENY. Failed/invalid output is retained. Fresh projects are the clean-reset procedure; do not erase evidence to turn a failed attempt into an apparent success.

## Generated evidence and offline derivation

New output is in **out/e<id>/**; t<id>/ contains test output, and out/timeout.json records measured timeout selection. All generated output and secrets are ignored. Each canonical scenario bundle has grant.json, requests.jsonl, decisions.jsonl, authority-state.json, erp-state.json, schedule-events.jsonl, run-manifest.json and run-summary.json, plus component logs and boundary probes. Empty schedule events are expected for uninstrumented cases. run-summary.json is derived, not independent destination evidence.

```powershell
.\.venv\Scripts\python.exe -B -m lab.run verify "out/e<id>"
```

Verify uses the original offline derivation and **rewrites** the derived run-summary.json. Prefer a copy if inspecting the published immutable bundle. For example, copy evidence/e466251 to out/inspect-e466251 before invoking verify. Reading initial/final ERP records is the source of destination totals; ALLOW logs alone are insufficient.

Each scenario automatically removes only its disposable runtime project after evidence collection. Documented `--keep` retains it for inspection. For an explicitly retained run, cleanup is `docker compose -p habr003-<run_id> down --volumes --remove-orphans`; choose only the project ID in that run's manifest. No cleanup of unrelated containers is required.

Only two public-layout constants differ from the validated host runner: output is local out/, and the frozen spec is local EXPERIMENT_SPEC_V0.2.md. All enforcement/ERP/scheduling/accounting code and tests are unchanged. The runner's original ENGINEERING_SMOKE_NOT_FORMAL labels remain: a reader's new replay is not the already-completed formal gate. The recorded gate is summarized separately, and no runtime campaign was conducted during publication.
