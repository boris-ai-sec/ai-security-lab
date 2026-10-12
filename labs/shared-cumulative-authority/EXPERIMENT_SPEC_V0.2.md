# Habr #003 — Aggregate Authority Experiment Specification V0.2

- **Date:** 2026-10-07
- **Status:** FROZEN FOR V0.1 IMPLEMENTATION
- **Owner / branch:** Agent Harness / Laboratory; V0.1 design freeze reflects the completed Framework → Laboratory freeze review reported by the user.
- **Scope:** One synthetic cumulative quantity grant, concurrent procurement-order creation, and comparison of post-effect accounting with atomic pre-execution reservation.
- **Authority / basis:** The preceding Codex implementation-feasibility review, the user's materialization task and explicit OD-01 resolution, and the completed Framework → Laboratory freeze review communicated by the user. This is an engineering design freeze for V0.1, not Framework doctrine.
- **Version meaning:** V0.2 is the specification revision; V0.1 denotes the first laboratory implementation covered by this design freeze.
- **Execution status:** NOT EXECUTED. All 80/120 quantities, ALLOW/DENY outcomes, and invariant outcomes below remain acceptance criteria, not observed results. Implementation has not started.
- **Supersedes:** No separately versioned approved design or governed artifact. This same specification records the design freeze following the preceding review.

## 1. Purpose

**Experimental question:** Can one cumulative human grant remain bounded when multiple autonomous runtime actions exercise shared authority concurrently?

The experiment compares two ways to exercise the same grant: a per-request check followed by external execution and post-effect accounting, and an atomic reservation committed before external execution.

The canonical workload is deterministic. It proposes three orders for COMP-17: SUP-A = 40, SUP-B = 40, and SUP-C = 40, against one aggregate grant of 100 units. The laboratory investigates enforcement of these actions, not how a language model generates the plan.

## 2. Claim and claim boundary

### Vulnerable concurrent behavior

Under the disclosed controlled schedule, three requests can each pass a local check against the shared authority value they actually read, receive ALLOW, and create an aggregate ERP quantity of 120 against a grant of 100. The failure mechanism is the absence of atomic pre-execution reservation.

**ALLOW ≠ proof of globally valid authorization.** In the vulnerable mode, ALLOW records a local decision consistent with a read snapshot; it does not establish that concurrent use of the cumulative grant remains within its limit.

### Corrected behavior

Atomic pre-execution reservation, retained capacity for uncertain outcomes, and idempotent ERP execution are intended to preserve the tested cumulative bound. In the canonical successful concurrent run, two orders of 40 are executed, the third is denied, and the destination total is 80.

The tested relationship is conditional on the assumptions in section 6. An atomic database counter alone is not a complete external-execution protocol.

### Excluded conclusions

The experiment does not establish a new concurrency principle, vulnerability prevalence across AI-agent authorization systems, production readiness, formal security assurance, safety of a real ERP/procurement deployment, or validation of Custos, PayReality, Surgical DevOps, or any other external product.

It does not measure how often an LLM proposes this workload, how often the forced schedule occurs naturally, or whether a particular model reasons correctly about its authority.

## 3. Trusted and untrusted components

Trust is assigned for this bounded laboratory, not asserted as a production property.

| Component | Role and trust | Permitted capabilities | Prohibited runtime capabilities |
|---|---|---|---|
| Trusted setup / grant loader | Trusted operator-controlled initialization; acts as the source of the simulated human grant | Provision/reset the lab and load immutable grant definitions and initial balances before requests start | No planner-controlled grant mutation; loader is not an active procurement writer during runs |
| Scripted planner | Untrusted proposer of business actions; deterministic workload generator | Call the purchase gateway using its own subject credential; observe outcomes | ERP write/read credentials, authority DB credentials, grant mutation, Docker administration |
| Gateway | Trusted enforcement/execution component under test; its accounting algorithm may be deliberately vulnerable | Read grants, mutate authority accounting/operations, and issue authenticated ERP create-order requests | Change immutable grant definitions; proxy arbitrary agent-selected destinations |
| Authority database | Trusted persistence and transaction mechanism | Store grant definitions, balances, and operation records | Define authority from the planner's claimed limit or infer expected test outcomes |
| ERP simulator | Trusted synthetic destination with separate business persistence | Authenticate the gateway; durably and idempotently create orders using its own ERP DB role; expose authorized reads | Enforce the human grant limit, import gateway accounting as destination evidence, or know the expected 80/120 result |
| Independent evidence reader | Trusted observer, separate from the gateway decision path | Read ERP orders directly and obtain read-only authority snapshots | Create/update/delete ERP orders or modify authority state |
| Harness | Trusted scheduling, orchestration, assertions, and evidence coordination | Launch workloads, control test hooks/fault settings, record scheduling events, derive assertions | Perform procurement writes directly or provide authority values/decisions to the gateway |

The gateway is the only runtime client allowed to possess the ERP HTTP write credential. The ERP possesses its verifier and its own ERP database write credential. The planner, evidence reader, and ordinary run harness possess neither.

Trusted host/setup administration can provision or reset persistence. Such administrative power is outside the runtime agent threat model and must not be presented as impossible to exercise.

There is no separate Grant Service and no separate executor service. A trusted fixture/store supplies the independent authority source; the gateway both enforces and executes.

## 4. Authority source and grant model

The trusted loader initializes the following immutable grant definition:

| Field | Canonical value / semantics |
|---|---|
| `grant_id` | G-2026-001; identifies one immutable grant within an isolated run |
| `subject_id` | Identity of the authorized planner/workflow; exact literal remains a fixture parameter |
| `resource` | COMP-17 |
| `allowed_suppliers` | SUP-A, SUP-B, SUP-C |
| `max_total_quantity` | 100 units across all orders exercising this grant |
| `status` | ACTIVE in the canonical fixture; checked by the gateway |

The gateway resolves the grant independently by `grant_id`. It never accepts a planner-supplied maximum or supplier list as authority. Caller identity is obtained from the trusted client-identity configuration/authentication, not from an unverified `subject_id` claim in a request.

Definitions are immutable throughout a run. A changed grant is a new grant identity. Each repetition starts from isolated clean state, so reuse of the canonical fixture ID does not reuse consumed authority from a prior run.

No signature service is required for this fixture: trusted loading and database access permissions establish its provenance. The planner cannot initialize or overwrite it. This simulates independent human authority; it is not a deployed human approval system.

Mutable accounting is separate from grant definition. The minimal authority data model retained from the review is:

| Table | Critical fields / responsibility |
|---|---|
| `grants` | Immutable fields above; runtime gateway has read access only |
| `grant_balances` | `grant_id`, `charged_quantity`, `revision`; shared mutable authority accounting |
| `operations` | `operation_id`, bound grant/subject/resource/supplier/quantity, decision/reason, lifecycle state, ERP order ID, timestamps |

Balance and associated lifecycle changes occur in the same transaction. Quantities are strictly positive integers for requests; the laboratory uses one fixed quantity unit without conversion. Separate persisted C/R/U counters are not required: lifecycle records provide their decomposition.

Expiry and dynamic revocation are excluded. The runtime contract does not include an ignored `valid_until` field. An inactive fixture may be used for a negative test, without introducing a dynamic revocation protocol.

## 5. Operation identity

Each `operation_id` identifies one business action and is immutably bound to:

- the grant;
- the authenticated subject;
- the resource;
- the supplier;
- the quantity.

The binding cannot be changed after the operation has been established. An HTTP attempt/request identifier is separate: retries have different attempt IDs but retain the same business operation ID.

**Same ID + same payload:** retrieve the existing operation/outcome; do not create a second reservation, increase accounting again, or create a second ERP order. A pending outcome stays pending. Replaying a terminal operation does not reopen it for execution.

**Same ID + different payload:** reject as an operation-identity conflict; do not create a new business effect or change the binding. A grant/subject change is also a payload conflict.

The corrected gateway persists the binding with reservation before ERP dispatch. ERP independently enforces unique operation identity and changed-payload rejection. Database uniqueness is a backstop; a uniqueness conflict must roll back the complete affected accounting transaction.

**OD-01 resolved by explicit user instruction:** In vulnerable mode, a successful snapshot-based admission is durably persisted in `operations` as ADMITTED_UNRESERVED before ALLOW and ERP dispatch. This record binds the immutable operation ID and payload and supports idempotency/evidence. It does not consume grant capacity and is excluded from Q.

An identical duplicate retrieves the existing ADMITTED_UNRESERVED or COMMITTED operation; it does not establish another admission or rerun the limit decision. Changed-payload rejection applies before dispatch. Persisting identity is not reservation: no balance charge or fresh shared-capacity check is attached to this admission write. Canonical requests have distinct operation IDs, so the central race does not depend on duplicates.

## 6. Authority-accounting model

For each grant, define quantities, not operation counts:

- **C** = quantity of operations in COMMITTED.
- **R** = quantity of operations in RESERVED.
- **U** = quantity of operations in PENDING_RECONCILIATION.
- **Q = C + R + U** = charged authority.
- **L** = the immutable grant limit.
- **D** = durably observed ERP quantity for that grant.

ADMITTED_UNRESERVED is a vulnerable-protocol-only state. Its quantity contributes zero to C, R, U, and Q until the guarded post-effect transition to COMMITTED atomically charges it. Persisting that admission does not increase `charged_quantity`.

The corrected mode's primary invariant is **Q <= L**. Its desired destination relationship is **D <= Q <= L**.

The following assumptions are required:

1. All relevant destination writes go through the trusted gateway and ERP contract; the planner cannot bypass them.
2. A confirmed durable reservation precedes every ERP dispatch in corrected mode.
3. Each business operation creates at most one order; its quantity equals the reserved quantity and its grant/resource/supplier match the binding.
4. Operation identity is immutable and duplicate execution is idempotent.
5. Unknown outcomes remain charged, including unresolved reservations after process restart.
6. Release is permitted only when an effect is excluded and no delayed/current/future dispatch can produce it.
7. Accounting and lifecycle transitions are atomic and applied at most once.
8. The grant definition and accounting are not altered out of band during a run; orders are not edited/deleted.
9. D is calculated from the independent destination records, not from ALLOW responses or the authority ledger.

An ERP order may already exist while its gateway operation is still RESERVED or PENDING_RECONCILIATION. Its quantity is then in D and in R or U. These describe the same action from different systems: **do not add D to Q** or add destination effects to all active reservations as if they were distinct commitments.

At a settled successful checkpoint, C = D and R = U = 0. At uncertain corrected-mode checkpoints, D may be less than Q. A destination snapshot is an observation at its stated time, not a globally atomic snapshot across two databases.

These invariants are targets for corrected enforcement, not constraints imposed on the vulnerable execution. In vulnerable mode, D may exceed charged accounting before post-effect updates; its final Q is expected to become 120 and exceed L. The intended comparison must not be hidden by a mode-specific database constraint that prevents reporting the vulnerable post-effect total.

The future implementation must compare `charged_quantity` with the sum of the corresponding charged operation records. A mismatch is an accounting-integrity failure even if the destination total is within 100.

## 7. State machine

Corrected operations are created in RESERVED only after admission; a denied operation has no charged quantity. RELEASED and DENIED contribute zero to Q.

| Transition | Exact meaning | Accounting effect |
|---|---|---|
| Admission -> RESERVED | Binding and quantity are durably recorded in the same transaction as capacity charging | Q increases by quantity |
| RESERVED -> COMMITTED | Durable ERP success is confirmed for the exact bound operation | Q unchanged; quantity moves R -> C |
| RESERVED -> RELEASED | ERP execution is excluded and any later dispatch is prevented | Q decreases once; quantity leaves R |
| RESERVED -> PENDING_RECONCILIATION | Execution may have happened; available evidence cannot establish the terminal outcome | Q unchanged; quantity moves R -> U |
| PENDING_RECONCILIATION -> COMMITTED | A matching durable ERP order is confirmed | Q unchanged; quantity moves U -> C |
| PENDING_RECONCILIATION -> RELEASED | Definitive non-execution and closure of possible execution are established | Q decreases once; quantity leaves U |

AVAILABLE is remaining capacity, not a reservation lifecycle state. It equals L - Q in a valid corrected state.

State changes are guarded against repetition and persisted atomically with any balance change. Replaying a COMMITTED/RELEASED transition must not change Q again.

**Unknown outcomes continue to consume authority capacity.** A crash may leave an operation labeled RESERVED before it can be relabeled PENDING_RECONCILIATION; it remains charged and is not treated as proof that nothing was sent.

### Vulnerable-protocol-only state and transition

The corrected lifecycle above does not include ADMITTED_UNRESERVED. The corrected gateway never creates that state or treats it as a valid reservation.

| Transition | Exact meaning | Accounting effect |
|---|---|---|
| Successful snapshot-based admission -> ADMITTED_UNRESERVED | Durably bind operation identity/payload before ALLOW and ERP dispatch, without reserving authority | Q and charged quantity unchanged |
| ADMITTED_UNRESERVED -> COMMITTED | Durable ERP success for the bound operation is confirmed; one short transaction performs the guarded state change and atomic balance increment | Quantity enters C; Q and charged quantity increase exactly once |
| COMMITTED -> COMMITTED (replayed completion) | The operation was already accounted for; completion is a no-op | Q and charged quantity unchanged |

The state guard, state change, and counter increment are one atomic accounting action. Concurrent/repeated completion processing cannot increment twice. This post-effect transition does not rerun the authority-limit decision, even if the increment makes Q exceed L.

## 8. Vulnerable algorithm

The intended mechanism is:

**Read shared state -> local check -> ALLOW -> ERP effect -> post-effect accounting.**

The gateway independently resolves the immutable grant, validates scope and identity, and reads the current shared `charged_quantity` without acquiring an admission lock or reserving capacity. It evaluates quantity against that observed value.

On a successful snapshot-based check, it persists the immutable binding as ADMITTED_UNRESERVED without charging authority. Only after that admission record's commit is confirmed does it emit ALLOW and execute the ERP request. Identity persistence must neither reserve capacity nor repeat the capacity check against fresh state.

After confirmed durable ERP success, one short transaction validates the bound operation and guards its transition from ADMITTED_UNRESERVED to COMMITTED. For that transition only, it atomically increments the current `charged_quantity` by the bound quantity and updates the balance revision. State change and increment commit or roll back together. If already COMMITTED, the transition is a no-op with no counter increment.

**Do not rerun the authority-limit decision after the external effect.** Post-effect accounting records what executed; it must not refuse to account for an order because the current total or resulting increment exceeds L.

It must not assign `observed_counter + quantity` as a replacement counter value. That would introduce a lost-update bug. The guarded transition prevents a duplicate order/completion from being charged twice.

No pre-execution balance charge, local application mutex, or hidden capacity-enforcing ERP behavior is allowed in this mode. The missing reservation is the sole intended admission defect.

In the sequential baseline, the next request starts only after the prior ERP execution and accounting finish. The same vulnerable mechanism then sees 0, 40, and 80 and produces the baseline outcome.

## 9. Controlled scheduling barrier

### Location and participants

In vulnerable concurrent mode the hook is **immediately after the request has completed its real unlocked authority read and captured the value, before the quantity/capacity decision and ERP dispatch**.

The barrier applies to the three canonical unique requests for the same run/grant: SUP-A 40, SUP-B 40, SUP-C 40. The participant identities/count are harness configuration, not gateway business-policy inputs.

### Arrival and release

Each arrival reports run ID, operation ID, attempt ID, hook identity, the actual observed charged quantity, and available balance revision. The scheduling controller records arrivals and releases all participants only after all three unique expected participants have arrived.

After release each request continues its ordinary algorithm using its own captured value. The barrier supplies no authority value, decision, quantity, or ERP response.

### Timeout and evidence

Waiting must be bounded. Missing/duplicate/unexpected participants, timeout, or cancellation invalidates the instrumented run. The harness aborts the run and accounts for/drains outstanding work before any clean reset; it does not relabel timeout as a business DENY or publish a successful 120 result from an incomplete schedule.

OD-02 is **RESOLVED AT DESIGN LEVEL — Laboratory selects a finite configurable operational timeout from smoke-test evidence; the selected value is recorded in run-manifest.json.** Finite wait is mandatory; timeout invalidates the instrumented run and is never a business DENY. No canonical numeric duration is selected yet.

`schedule-events.jsonl` records configuration, arrivals with observations, release, and timeout/abort events. Events include component identity, UTC time, and an explicit event sequence; wall-clock proximity alone is not evidence that all reads preceded release.

The corrected concurrent run uses a start barrier **before the reservation transaction**. It does not place a three-party barrier after a row lock: that would interfere with the mechanism being tested and could deadlock.

The public description must disclose the hook location, participants, observed values, release condition, and forced nature of this one schedule. The barrier controls scheduling only: it must not inject state, alter the grant, change decisions, or create ERP effects.

## 10. Corrected algorithm

The selected PostgreSQL mechanism is a short READ COMMITTED transaction with `SELECT grant_balance FOR UPDATE`. Conditional UPDATE and SERIALIZABLE are not alternative implementations to add in V0.1.

The transaction proceeds in this order:

1. BEGIN.
2. Independently load the immutable grant and select/lock its balance row FOR UPDATE.
3. Validate operation identity, authenticated subject, grant status, resource, supplier, strict positive integer quantity, and remaining capacity.
4. For a new admissible operation, create its bound RESERVED record.
5. Increase charged authority and update balance revision in the same transaction.
6. COMMIT.

An existing identical operation returns its existing state rather than receiving a new reservation. Conflicting identity is rejected. Rejected admission does not charge authority or dispatch ERP.

**Only after confirmed commit: ALLOW -> ERP execution.** A database failure, rollback, or uncertain commit result does not authorize dispatch. Once a committed reservation exists, uncertainty is resolved against its persisted identity; it is not retried as a fresh operation.

The ERP call remains outside the reservation transaction. Durable ERP success, definitive no-effect failure, and uncertain outcomes are handled through the lifecycle in sections 7 and 15, using separate short transactions.

All transitions that affect shared accounting use one consistent lock/transaction protocol. A thread-local or process-local mutex is not the selected authority enforcement mechanism.

## 11. ERP simulator contract

Execution means **creation of a procurement order**, not shipment, receipt of goods, or payment.

ERP orders use separate persistent destination state. The minimal record contains `order_id`, unique `operation_id`, `grant_id`, `resource`, `supplier`, `quantity`, and `created_at`.

The ERP contract requires:

- durable order storage;
- unique immutable operation identity;
- same-ID/same-payload replay returns the existing order without a second effect;
- same-ID/different-payload replay is rejected without changing the existing order;
- success is returned only after durable order commit;
- an independent read endpoint returns complete order records;
- no use of grant limit, gateway accounting, or expected scenario result to accept/reject orders;
- no editing or deleting orders in V0.1.

The minimum endpoints retained from the review are:

| Component | Endpoint | Responsibility |
|---|---|---|
| Gateway | POST /purchase | Admission decision and permitted ERP execution |
| Gateway | GET /operations/{operation_id} | Persisted operation state/outcome |
| ERP | POST /orders | Authenticated idempotent order creation |
| ERP | GET /orders?grant_id=... | Independent retrieval of complete destination records |

Exact wire schemas/status-code choices are implementation details; the semantic outcomes above cannot be weakened by those choices. An aggregate endpoint is not required because the reader calculates totals from orders.

A generic HTTP failure is not the contract's definitive no-effect result. Conditions for definitive release are specified in section 15; OD-03 is resolved for V0.1 with the conservative policy and no general recovery/closure subsystem.

## 12. Network and credential boundary

The selected topology uses Docker Compose with two explicitly assigned isolated networks:

| Component | Control network | Execution network |
|---|---|---|
| Planner | Yes | No |
| Gateway | Yes | Yes |
| ERP | No | Yes |
| PostgreSQL | No | Yes |
| Independent evidence reader | No | Yes |

The trusted loader temporarily reaches the authority store for initialization and exits before the run. Harness orchestration is trusted; it must not create a runtime agent-controlled bridge/proxy to ERP.

The authority and ERP databases are logically separate databases on one PostgreSQL service, with separate runtime roles. The gateway cannot use its authority DB role to write ERP orders; the ERP cannot use its role to change authority. Independent observation is logically separate, not separate infrastructure assurance.

Canonical runs do not publish ERP/PostgreSQL ports to the host, do not attach the planner to a shared default/execution network, and do not give the planner Docker socket access, privileged mode, host networking, or ERP/DB secret mounts. The gateway destination is fixed by trusted configuration and is not an agent-supplied URL.

Per-service secret files/Compose secrets are preferred over shared environment blocks. Only the gateway receives the ERP HTTP write token; ERP receives its verifier. The reader uses a separate read-only ERP credential and read-only authority access. Planner authentication is a distinct credential binding it to its subject.

Required boundary evidence includes attempts from the planner container using ERP DNS name, known destination IP, and possible host route, plus checks that the planner has no ERP/DB credentials. A failed DNS lookup alone is insufficient. Read-only ERP credentials must fail a write attempt.

This boundary concerns an unprivileged agent container in the declared topology. It does not protect against the host administrator, Docker daemon, infrastructure compromise, or escape from that container boundary. Compose secrets are not claimed to protect against the host owner.

## 13. Evidence architecture

The required chain is:

**Raw Artifacts -> Normalized Evidence -> Derived Findings -> Interpretation -> Publication Claims.**

The canonical bundle contains all eight requested artifacts. `run-summary.json` is explicitly a derived artifact in that bundle, not a raw measurement. Neither its filename nor its presence promotes it to authoritative evidence.

| Artifact | Producer | Authoritative source / evidentiary role | Identifiers | Timing/state represented |
|---|---|---|---|---|
| `grant.json` | Trusted setup/loader | Original input definition and declared provenance of the simulated human grant | grant ID, subject ID; run ID in bundle association | Pre-run immutable fixture; loader/reader verify agreement with initialized DB |
| `requests.jsonl` | Planner/harness | Actual submitted operation payloads and delivery attempts | run, grant, operation, attempt IDs | Submission events and request/response observations; not proof of ERP execution |
| `decisions.jsonl` | Gateway | Gateway's decisions and authority-transition diagnostics | run, grant, operation, attempt IDs; balance revision; ERP order ID when known | Read/check observations, persisted ADMITTED_UNRESERVED admission or confirmed reservation, state transitions and completion no-ops; raw component reports, not independent destination proof |
| `authority-state.json` | Independent reader with read-only DB access | Persisted grants, balances, and operation records | run, grant, operation IDs; revisions | Labeled initial/final snapshots, or explicit failure-test checkpoint; each authority snapshot is internally consistent |
| `erp-state.json` | Independent reader via ERP read API | Actual durable destination order records | run association, grant, operation, order IDs | Read request/response and complete orders at the stated checkpoint; includes evidence of empty initial state |
| `schedule-events.jsonl` | Harness scheduling controller | Actual hook arrivals, observations, releases, and failures | run, grant, operation, attempt IDs; hook and event sequence | Controlled interleaving; different hook location for corrected start barrier is explicit |
| `run-manifest.json` | Trusted harness/setup | Run provenance and configuration | run ID, scenario/mode, source revision, fixture identity/hash | Environment/dependency/image versions, isolation level, worker configuration, hooks, participants, timeout, clean-state preparation |
| `run-summary.json` | Summary/verification step | Derived calculations from the identified raw inputs | run ID; references/hashes identifying inputs | Totals, unique-operation decision counts, expected-vs-observed assertions, completeness, and bounded findings at the named checkpoint |

Raw event records include producer/component, event type, UTC timestamp, correlation identifiers, relevant payload/value, and outcome/reason. Transaction IDs may be captured diagnostically; they are not a global clock or standalone proof of commit.

Decision records and transition records are distinguishable by event type. Counts of ALLOW/DENY refer to unique business operations, not retry responses or transition events.

Vulnerable-mode evidence must distinguish the uncharged ADMITTED_UNRESERVED record from a corrected reservation, show that its persistence left Q unchanged, and link ERP success to the single charged COMMITTED transition. A replayed completion must be identifiable as a no-op, not another ALLOW or another accounting charge.

Normalization aligns identities and quantities without replacing the raw records. Derived checks include destination bound, authority bound, balance/operation consistency, record scope/identity, and evidence completeness. Interpretation distinguishes the observed counterexample from assumptions and limitations. Publication claims may use only completed, adequately evidenced runs.

The summary calculates destination total from ERP records, not gateway decision values, a hardcoded expected result, or the authority database. Expected 80/120 values belong to assertions, not the measurement source.

Canonical final snapshots are collected after all requests and accounting transitions settle. Initial snapshots establish zero contamination. Fault-test checkpoints are labeled and must not pretend to be globally atomic cross-database snapshots. Missing artifacts, unfinished work, or an invalid schedule prevent a passing finding.

Independent reader access is sufficient for this synthetic lab to avoid gateway-log-only conclusions. It is not an independent third-party audit: the ERP, reader, and host remain authored/trusted laboratory components.

## 14. Canonical scenarios and acceptance criteria

Each scenario starts with an independent clean grant/balance/destination state. The wrong-resource scenario does not inherit orders from another scenario.

| Scenario | Workload / schedule | Required decisions | Required destination/accounting outcome |
|---|---|---|---|
| Sequential vulnerable baseline | SUP-A 40, then SUP-B 40, then SUP-C 40; wait for ERP and accounting before the next request | 2 ALLOW, 1 capacity DENY | ERP = 80; charged = 80; accounting consistent |
| Instrumented vulnerable concurrency | Same three operations; post-read barrier | 3 ALLOW; all three actually observed charged = 0 | ERP = 120; charged = 120; cumulative limit violated; no lost update |
| Corrected concurrency | Same three operations; concurrent start before transaction | 2 ALLOW, 1 capacity DENY | ERP = 80; charged = 80; R = U = 0; accounting consistent |
| Wrong-resource control | COMP-99, quantity 10, otherwise admissible subject/supplier | DENY_RESOURCE_NOT_IN_GRANT | ERP = 0; accounting unchanged |

The corrected scenario must produce exactly 80, not merely ERP <= 100. An implementation that denies every request does not pass. The denied supplier need not be deterministic; quantities, counts, reason, and final state must be.

Before publication, the additional tests retained from the review must pass:

1. Wrong supplier, unknown/inactive grant, and wrong authenticated subject are denied without destination effect.
2. Zero/negative quantity and unsuitable types are rejected; quantities are not silently coerced into admissible values.
3. An exact-limit operation is allowed; an excess of one unit is denied.
4. Sequential and concurrent identical duplicates create one reservation/accounting charge and one ERP order in corrected mode. In vulnerable mode, admission creates one immutable ADMITTED_UNRESERVED record with no charge; repeated/concurrent completion after ERP success performs one COMMITTED transition and one atomic charge. Already-COMMITTED completion is a no-op. The ERP duplicate contract applies in both modes.
5. An operation ID reused with changed bound fields is rejected without a new effect.
6. Reservation transaction rollback causes no ERP dispatch and no residual charge.
7. Repeated terminal transitions do not release capacity or account effects twice.
8. Gateway restart after reservation leaves capacity charged; unresolved RESERVED is not auto-released.
9. ERP commit with lost response retains charge; subsequent observation identifies one matching order, without duplicate execution.
10. Definitive no-effect failure allows safe release when execution is closed; generic failure does not.
11. Planner network/credential bypass checks fail, and read-only ERP credentials cannot write.
12. Barrier timeout, missing/incomplete evidence, or unfinished requests invalidate the run.
13. Summaries are independently recomputable from raw artifacts; clean reset prevents cross-run contamination.

These tests are acceptance requirements, not a claim that a test suite exists. Corrected lifecycle/duplicate tests do not imply that the intentionally vulnerable mode implements a production recovery protocol. The vulnerable concurrency test must still reach charged = 120: post-effect accounting must not repeat the limit check and suppress an executed order's charge.

## 15. Unknown-outcome behavior

The charged-reservation behavior below applies to corrected mode. In vulnerable mode an unresolved ADMITTED_UNRESERVED operation remains uncharged and excluded from Q; it must not be relabeled as a charged RESERVED/PENDING_RECONCILIATION operation. Confirmation of a matching durable ERP order permits the guarded post-effect COMMITTED transition in sections 7–8. No full vulnerable recovery subsystem is introduced.

| Condition | Required behavior | Release permitted? |
|---|---|---|
| ERP request timeout | Outcome is uncertain; retain charged quantity and mark PENDING_RECONCILIATION when possible | No, on timeout alone |
| Response lost after ERP commit | Retain capacity; independently retrieve the matching order; guarded transition to COMMITTED | No |
| Generic HTTP/network failure | Do not infer non-execution from 500, connection loss, or an ambiguous response; retain capacity | No, on generic failure alone |
| Confirmed no-effect failure | Independently establish definite no-effect and execution closure with no remaining possible dispatch; guarded transition to RELEASED | Yes, after both conditions are established |
| Restart after reservation | Persisted reservation remains charged; do not assume the ERP request was never sent | No, on restart alone |
| Matching durable order found | Validate identity and fields against durable destination evidence; transition RESERVED/PENDING_RECONCILIATION to COMMITTED at most once | No release; Q unchanged |
| No order found in a read | Treat absence as checkpoint evidence only; an earlier request may still complete | No, on a single absent-order read alone |

An operation known not to have been dispatched may be released only if later dispatch is also excluded. OD-03 is **RESOLVED FOR V0.1 — CONSERVATIVE OPTION A**: a genuinely uncertain external execution outcome remains charged. PENDING_RECONCILIATION -> RELEASED remains a conditional conceptual transition requiring definite independently established no-effect and execution closure. V0.1 does not claim that generic uncertain outcomes can be safely released.

Safety may leave unused capacity locked indefinitely in V0.1. Availability and eventual recovery remain outside V0.1 scope. V0.1 does not implement a general recovery/closure subsystem; there is no reservation TTL or automatic release. A full automatic retry/reconciliation subsystem, public recovery API, or worker queue remains outside this specification's first implementation scope.

Unknown-outcome tests remain secondary to the main concurrency comparison. Any fault hook used to lose a response or pause execution must be declared in the manifest/evidence rather than represented as a naturally occurring measured failure.

## 16. Reproducibility

The previously recommended publication criterion is:

1. Run the canonical suite from a clean initial state using a documented entry procedure.
2. Perform ten clean repetitions of the main scenarios without outcome discrepancies. Each repetition has its own run identity and evidence bundle.
3. Obtain at least one full repeat by another person or in a fresh environment.
4. Retain/publish the run manifest and raw evidence required to recompute findings.
5. Report failures and invalid runs; do not discard them and present only successful reruns.

The manifest records source revision, relevant versions/configuration, PostgreSQL isolation level, gateway worker setup, fixtures, and instrumentation. The sequential run disables the concurrent hook; the vulnerable concurrent run uses the disclosed post-read schedule; the corrected run uses concurrent admission before its transaction.

One hundred repetitions may be supplementary regression evidence. Repeated execution of one forced schedule is **not broad concurrency coverage**, a production failure-rate estimate, or formal proof of invariant preservation under all schedules.

## 17. Known limitations

- This is a synthetic laboratory on trusted infrastructure, not an independently audited business system.
- The planner is deterministic and no LLM is required. The result concerns execution/enforcement, not model planning quality.
- The simulated human grant is an independently loaded trusted fixture, not a full human approval service.
- Expiry and dynamic revocation are excluded.
- The destination is a Demo ERP, not a production ERP. Execution means order creation only.
- Grant scope is one resource, fixed units, a supplier allow-list, and one cumulative limit; overlapping grants, money, conversion, and partial execution are excluded.
- Logical separation of authority and destination on one PostgreSQL service is not infrastructure independence.
- The network boundary excludes privileged host/Docker administration and infrastructure compromise.
- The barrier selects a permitted interleaving; it does not measure how frequently it occurs naturally.
- Recorded checkpoints and transition tests are finite evidence, not formal security assurance or exhaustive concurrency verification.
- Atomic reservation does not supply availability, automatic recovery, or exactly-once behavior without the separate idempotency/closure assumptions.
- No novel concurrency primitive or prevalence claim across agent systems is asserted.
- No external product validation is implied.
- No result in this document has been executed or observed.

## 18. Open Decision Register

No unresolved design decisions remain. OD-02 and OD-03 are retained here as resolved records from the completed Framework → Laboratory freeze review. Selecting the operational timeout from smoke-test evidence is a Laboratory execution/configuration responsibility, not an open design-freeze blocker. The grant source, combined gateway/executor, PostgreSQL row-lock reservation, Compose boundary, deterministic planner, and exclusion of expiry/LLM are not reopened.

### OD-02 — Barrier timeout parameter

**Status: RESOLVED AT DESIGN LEVEL — Laboratory selects a finite configurable operational timeout from smoke-test evidence; the selected value is recorded in run-manifest.json.**

- **Frozen behavior:** Timeout is configurable and finite wait is mandatory. A timeout invalidates the instrumented run and is never a business DENY.
- **Operational selection:** No canonical numeric duration is selected yet. Laboratory selects the operational value from smoke-test evidence and records it in each run manifest.
- **Implementation consequence:** Determines harness configuration and its manifest value; does not alter business decisions or the race mechanism.
- **Blocks design freeze:** **No.** Design behavior is resolved; the operational value is selected during Laboratory execution preparation.

### OD-03 — Definitive closure for release after an uncertain outcome

**Status: RESOLVED FOR V0.1 — CONSERVATIVE OPTION A**

- **Frozen behavior:** In corrected mode, a genuinely uncertain external execution outcome continues to consume authority capacity. Matching durable destination evidence may resolve the operation to COMMITTED.
- **Conditional release:** Definite independently established no-effect may permit RELEASED only when execution closure is established. PENDING_RECONCILIATION -> RELEASED remains a conditional conceptual transition; V0.1 must not claim safe release of generic uncertain outcomes.
- **Insufficient grounds for release:** Timeout, connection loss, generic HTTP error, restart, or a single absent destination read.
- **V0.1 boundary:** No general recovery/closure subsystem, reservation TTL, or automatic release. Availability and eventual recovery remain outside V0.1 scope.
- **Implementation consequence:** Retain uncertain capacity and support confirmation by matching durable orders, without claiming a general mechanism for closing/releasing uncertain executions.
- **Blocks design freeze:** **No.** The conservative V0.1 policy is resolved.

## SPEC FREEZE READINESS

**FROZEN FOR V0.1 IMPLEMENTATION**

Remaining freeze blockers: **None.**

OD-01 is resolved by the user's explicit ADMITTED_UNRESERVED decision, recorded in sections 5–8 and reflected in evidence and test requirements. The vulnerable protocol now binds identity without consuming capacity and charges each confirmed effect exactly once without a post-effect limit recheck.

OD-02 is resolved at design level: Laboratory selects a finite configurable operational timeout from smoke-test evidence and records the value in run-manifest.json; no canonical numeric duration is selected yet. OD-03 is resolved for V0.1 as CONSERVATIVE OPTION A, without a general recovery/closure subsystem or a claim that generic uncertain outcomes can be released.

The specification is frozen for V0.1 implementation following the completed Framework → Laboratory freeze review. **Execution status: NOT EXECUTED.** All 80/120 quantities, ALLOW/DENY outcomes, and invariants remain acceptance criteria, not observed results. Implementation has not started; this synchronization task creates no implementation code.
