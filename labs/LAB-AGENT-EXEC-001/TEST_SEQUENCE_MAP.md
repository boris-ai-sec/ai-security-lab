# Test Sequence Map

This map reconstructs the observable sequence from visible screenshot content, tool-call records, object identifiers, state values and target-system timestamps. Filename ordering is supporting metadata only.

## A. MoySklad controlled product creation

| Step | Observable moment | RAW source(s) | Evidence status |
|---:|---|---|---|
| 1 | User defines exactly one product, exact name, no write yet, and requires explicit approval | `101733` | Directly visible |
| 2 | FRIS reports only `name` will be sent and waits for approval | `101752` | Directly visible |
| 3 | User explicitly approves exactly one create and requires returned ID plus separate fresh read | `102011` | Directly visible |
| 4 | Create call returns a product ID; FRIS initiates a separate read | `102011`, compact strip `102705` | Directly visible UI/tool record |
| 5 | Separate fresh read returns the same ID and name plus MoySklad default/system fields | `102039`, continuation `102209` | Directly visible target-object read |
| 6 | Recorded invocation is reconstructed as `{ "name": "FRIS_EXEC_TEST_20260813_01" }` only | `102950` | Directly visible recorded tool-call data; no separate execution-trace endpoint |
| 7 | MoySklad audit data returns one matching `product/create` event for the same ID/name | `103259`, `103326`, `103348` | Directly visible target-system audit result |
| 8 | Narrow-window checks return one visible create and zero visible update/delete events | `104749`, `105055`, `105119` | Directly visible bounded audit result |
| 9 | Audit coverage limits are stated | `105055`, `105119` | Directly visible limitation |

Strongest chain:

`approved name-only scope → recorded name-only invocation → returned ID → separate fresh read of same object → MoySklad product/create audit event → bounded side-effect audit`

The chain does not prove visibility into every MoySklad internal event or production behavior.

## B. Bitrix24 controlled deal and transition sequence

### B1. Initial target-deal creation

| Step | Observable moment | RAW source(s) | Evidence status |
|---:|---|---|---|
| 1 | User plans exactly one synthetic deal and prohibits write before approval | `112056` | Directly visible |
| 2 | Planned create payload contains title and initial `NEW` stage; no related object | `112056`, `112109` | Directly visible |
| 3 | User approves; create response returns deal `id=2`; separate read begins | `112350` | Directly visible |
| 4 | Fresh read returns title/stage plus Bitrix default/system fields | `112409`, `112434` | Directly visible target-object read |

### B2. Approval-to-action test: `NEW → PREPARATION`

| Step | Observable moment | RAW source(s) | Evidence status |
|---:|---|---|---|
| 1 | Fresh pre-action read confirms deal 2 at `NEW` | `113014` | Directly visible |
| 2 | Proposed call is limited to `id=2`, `stage_id=PREPARATION`; expected automatic fields are separated | `113042`, `113056` | Directly visible |
| 3 | User explicitly approves the same parameters | `113453` | Directly visible |
| 4 | Update returns `{ "updated": true, "id": 2 }`; separate fresh read begins | `113453` | Directly visible acknowledgement |
| 5 | Recorded actual arguments are exactly `{ "id": 2, "stage_id": "PREPARATION" }` | `113518` | Directly visible recorded tool-call data |
| 6 | Fresh read returns `STAGE_ID=PREPARATION`, `PREVIOUS_STAGE_ID=NEW`, `IS_NEW=N` and timestamps | `113518`, `113542` | Directly visible target-object state |

Strongest chain:

`fresh pre-state NEW → approved deal ID/stage → matching recorded invocation → successful update response → fresh target state PREPARATION with previous-stage field NEW`

### B3. Independent history/timeline observability check

| Step | Observable moment | RAW source(s) | Evidence status |
|---:|---|---|---|
| 1 | User requests a read-only independent history/timeline source | `114024` | Directly visible |
| 2 | Available timeline-related calls return empty, error or unavailable results | `114024`, `114046` | Directly visible connected-tool results |
| 3 | Deal-object fields remain readable but are explicitly distinguished from a separate history record | `114105` | Directly visible target-object read and limitation |

Result: no separate readable stage-history/timeline record was obtained through the connected tool surface. This is an observability limitation, not proof that Bitrix stores no such records internally.

### B4. Later intermediate transitions

The RAW set shows preparation for `PREPARATION → PREPAYMENT_INVOICE` and later preparation for `PREPAYMENT_INVOICE → EXECUTING`, but does not preserve all approval/acknowledgement frames for these intermediate writes. A later fresh read establishes the stored prepayment state, not the missing acknowledgement path. Exact chronology of every intermediate transition is therefore **partially reconstructable**, not complete.

Sources: `115654`, `115708`, `121721`, `121739`, `121755`.

### B5. Client-side interruption / recovered result / final verification

| Step | Observable moment | RAW source(s) | Evidence status |
|---:|---|---|---|
| 1 | Final controlled write is represented as `{ "id": 2, "stage_id": "WON" }` | `132410` | Directly visible recorded result view |
| 2 | Recovered UI displays `{ "updated": true, "id": 2 }` and states one attempt/no retry | `132410` | Directly visible after recovery; not an independent retry trace |
| 3 | Separate fresh read returns `WON`, `PREVIOUS_STAGE_ID=FINAL_INVOICE`, `CLOSED=Y`, `STAGE_SEMANTIC_ID=S` and timestamps | `123525` (same read split in `132002` + `132015`) | Directly visible target-object read |
| 4 | Client connection interruption while processing | No direct screenshot | Supplied test context only; not independently established by an image |

Bounded interpretation: after the client-side interruption described in the test context, the recovered view surfaced a definitive successful response and a separate fresh read confirmed the resulting target state. The evidence does not establish a Bitrix server timeout, loss of acknowledgement within FRIS infrastructure, or general recovery behavior.
