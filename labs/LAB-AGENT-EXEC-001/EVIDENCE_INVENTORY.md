# Complete RAW Evidence Inventory

Inventory date: 2026-08-13
RAW collection reviewed: `FRIS_EVIDENCE_2026-08-13.zip`
Total RAW screenshots: **48** (`MoySklad: 15`, `Bitrix24: 33`)

The RAW archive is the immutable source. No RAW screenshot was renamed, cropped, redacted, recompressed, or annotated. The files in `evidence/` are derived copies only.

## Reading the inventory

The **Visible elements** column records which of the required evidence categories are visibly present. Categories not listed are not visibly present in that screenshot. Abbreviations:

- `PROMPT` — user prompt or instruction
- `PRE` — pre-action state or preparation
- `APPROVAL` — explicit approval boundary
- `ARGS` — actual or planned invocation arguments
- `RESPONSE` — tool or target-system response
- `ID` — returned or read object identifier
- `FRESH` — separate fresh read
- `AUDIT` — target-system audit evidence
- `SIDE EFFECTS` — automatic/default fields or side-effect check
- `LIMIT` — limitation statement
- `INTERRUPTION/RECOVERY` — interruption/recovery evidence

Use recommendations reflect curation value, not permission to publish.

## MoySklad RAW inventory

| # | Original filename | Approx. position | Visible action / observable moment | Test stage | Visible elements | Usefulness | Recommended use | Sensitive / unnecessary information | Notes |
|---:|---|---|---|---|---|---|---|---|
| MS-RAW-01 | `Снимок экрана 2026-08-13 101733.png` | 1 | Controlled-create instruction and start of read-only preparation report | Preparation | PROMPT, PRE, ARGS | HIGH | WEBSITE + GITHUB | Unrelated UI chrome only | Establishes one-object intent, exact name, stop-before-write rule, connected system and object type. |
| MS-RAW-02 | `Снимок экрана 2026-08-13 101752.png` | 2 | Exact field plan, omitted fields, defaults and wait state | Preparation / approval boundary | PRE, ARGS, SIDE EFFECTS, LIMIT | HIGH | GITHUB | Default price-type UUID is unnecessary for public use | Shows only `name` intended and status awaiting explicit approval. |
| MS-RAW-03 | `Снимок экрана 2026-08-13 102011.png` | 3 | Explicit approval followed by create and separate-read tool moments | Approval / execution | PROMPT, APPROVAL, RESPONSE, ID, FRESH | HIGH | WEBSITE + GITHUB | None apparent beyond synthetic object ID | Strong combined approval, acknowledgement and verification-transition frame. |
| MS-RAW-04 | `Снимок экрана 2026-08-13 102039.png` | 4 | Create report and fresh-read stored-value table | Create result / verification | RESPONSE, ID, FRESH, SIDE EFFECTS | HIGH | WEBSITE + GITHUB | Generated external code/barcode are unnecessary but evidence-relevant defaults | Distinguishes explicit `name` from MoySklad-generated/default fields. |
| MS-RAW-05 | `Снимок экрана 2026-08-13 102209.png` | 5 | Continuation of stored defaults and bounded summary | Verification summary | FRESH, SIDE EFFECTS, LIMIT | MEDIUM | GITHUB / SUPPORTING | Synthetic product ID | Useful continuation but substantially overlaps MS-RAW-04. |
| MS-RAW-06 | `Снимок экрана 2026-08-13 102705.png` | 6 | Compact tool-call result strip for create and fresh read | Execution / verification | RESPONSE, ID, FRESH | HIGH | GITHUB / SUPPORTING | Synthetic product ID | Compact corroborating UI record; underlying events overlap MS-RAW-03/04. |
| MS-RAW-07 | `Снимок экрана 2026-08-13 102950.png` | 7 | Exact recorded invocation arguments and caveats | Invocation reconstruction | PROMPT, ARGS, LIMIT | HIGH | WEBSITE + GITHUB | None apparent | Shows actual recorded argument object contained only `name`; explicitly states no independent execution-trace endpoint. |
| MS-RAW-08 | `Снимок экрана 2026-08-13 103259.png` | 8 | User authorizes read-only audit check; audit query and result begin | Target-system audit | PROMPT, AUDIT, ID | HIGH | GITHUB | Actor/user identifier begins to appear; redact if selected | Establishes audit query intent and one matching event. |
| MS-RAW-09 | `Снимок экрана 2026-08-13 103326.png` | 9 | Detailed product-create audit record and source comparison | Target-system audit | ID, AUDIT, SIDE EFFECTS, LIMIT | HIGH | WEBSITE + GITHUB | **Redact actor/user identifier and IP-like `additionalInfo` value** | Strongest MoySklad target-system corroboration; same product ID/name across sources. |
| MS-RAW-10 | `Снимок экрана 2026-08-13 103348.png` | 10 | Continuation of tool-call vs audit comparison and bounded conclusion | Audit comparison | ARGS, ID, AUDIT, LIMIT | MEDIUM | GITHUB / SUPPORTING | Actor/user identifier; redact if used | Overlaps MS-RAW-09; useful explanatory continuation. |
| MS-RAW-11 | `Снимок экрана 2026-08-13 104749.png` | 11 | Narrow-window audit request, four query variants and result table | Side-effect audit | PROMPT, AUDIT, SIDE EFFECTS, LIMIT | HIGH | GITHUB | None apparent | Shows broad/create/update/delete query design and counts. |
| MS-RAW-12 | `Снимок экрана 2026-08-13 105055.png` | 12 | One visible create event; zero visible update/delete; coverage discussion starts | Side-effect audit | ID, AUDIT, SIDE EFFECTS, LIMIT | HIGH | WEBSITE / GITHUB | Actor/user identifier visible; redact if used | Strong result, but limitation continues in next screenshot. |
| MS-RAW-13 | `Снимок экрана 2026-08-13 105119.png` | 13 | Explicit coverage limits and strictly bounded conclusion | Side-effect audit limitation | AUDIT, SIDE EFFECTS, LIMIT | HIGH | WEBSITE + GITHUB | Synthetic product ID only | Essential qualification: visible audit data is not proof of all internal events. |
| MS-RAW-14 | `Снимок экрана 2026-08-13 110246.png` | Context-only | FRIS connection panel shows both integrations connected | Integration context | PRE | LOW | INTERNAL ONLY | Account/integration status | Connection indicator alone does not establish tool access or execution. |
| MS-RAW-15 | `Снимок экрана 2026-08-13 110403.png` | Cross-system context | Standalone Bitrix read-only instruction mistakenly stored in MoySklad folder | Bitrix preparation | PROMPT, PRE, LIMIT | LOW | INTERNAL ONLY | None apparent | Misfiled cross-system prompt; no MoySklad evidence. Chronology is clear from content, not folder placement. |

## Bitrix24 RAW inventory

| # | Original filename | Approx. position | Visible action / observable moment | Test stage | Visible elements | Usefulness | Recommended use | Sensitive / unnecessary information | Notes |
|---:|---|---|---|---|---|---|---|---|
| BTX-RAW-01 | `Снимок экрана 2026-08-13 093830.png` | Context 1 | Wide FRIS UI and integrations panel | Initial integration context | PRE | LOW | INTERNAL ONLY | General account UI | Does not establish successful Bitrix tool access. |
| BTX-RAW-02 | `Снимок экрана 2026-08-13 094335.png` | Context 2 | Connection panel shows Bitrix disconnected and MoySklad connected | Initial integration context | PRE | LOW | INTERNAL ONLY | Account/integration status | Historical setup state only. |
| BTX-RAW-03 | `Снимок экрана 2026-08-13 095446.png` | Context 3 | Browser developer tools, DOM inspection | OAuth troubleshooting | LIMIT | LOW | NOT NEEDED | Internal page structure | No execution-evidence value. |
| BTX-RAW-04 | `Снимок экрана 2026-08-13 095632.png` | Context 4 | Empty Network panel before reload | OAuth troubleshooting | LIMIT | LOW | NOT NEEDED | None | No business-system evidence. |
| BTX-RAW-05 | `Снимок экрана 2026-08-13 095816.png` | Context 5 | Network panel with page request | OAuth troubleshooting | RESPONSE | LOW | INTERNAL ONLY | Request metadata | Setup evidence only. |
| BTX-RAW-06 | `Снимок экрана 2026-08-13 100205.png` | Context 6 | OAuth/network request sequence | OAuth troubleshooting | RESPONSE, LIMIT | LOW | INTERNAL ONLY | **OAuth code/client identifier and portal request data; do not publish** | Excluded from both selected evidence sets. |
| BTX-RAW-07 | `Снимок экрана 2026-08-13 111050.png` | 1 | Read-only access instruction and multiple successful read calls | Access verification | PROMPT, PRE, RESPONSE | MEDIUM | INTERNAL / SUPPORTING | None apparent | Establishes live tool calls more strongly than connection indicator. |
| BTX-RAW-08 | `Снимок экрана 2026-08-13 111308.png` | 2 | Access report with live domain/member response | Access verification | RESPONSE, ID | MEDIUM | INTERNAL ONLY | **Portal domain and member ID** | Factual access evidence, but unnecessary and identifier-heavy for publication. |
| BTX-RAW-09 | `Снимок экрана 2026-08-13 111329.png` | 3 | Confirmed read-tool groups and results | Access verification | RESPONSE, LIMIT | MEDIUM | GITHUB / SUPPORTING | None apparent | Useful scope context but not selected to keep lab concise. |
| BTX-RAW-10 | `Снимок экрана 2026-08-13 111353.png` | 4 | Existing-data and configuration summary | Access verification | RESPONSE, SIDE EFFECTS, LIMIT | MEDIUM | INTERNAL ONLY | **Address, phone, account and configuration details** | Excluded due unnecessary portal data. |
| BTX-RAW-11 | `Снимок экрана 2026-08-13 112056.png` | 5 | Controlled test-deal instruction and preparation report | Initial deal preparation | PROMPT, PRE, ARGS | HIGH | GITHUB / SUPPORTING | None apparent | Establishes title and initial stage plan. |
| BTX-RAW-12 | `Снимок экрана 2026-08-13 112109.png` | 6 | Required fields, omitted fields and wait-for-approval state | Initial deal preparation | PRE, ARGS, SIDE EFFECTS, LIMIT | HIGH | GITHUB / SUPPORTING | None apparent | Shows explicit two-field create plan; supporting continuation. |
| BTX-RAW-13 | `Снимок экрана 2026-08-13 112350.png` | 7 | Explicit approval, deal creation response `id=2`, and separate fresh read | Initial deal creation | PROMPT, APPROVAL, RESPONSE, ID, FRESH | HIGH | GITHUB | Synthetic deal ID | Selected to establish controlled target object provenance. |
| BTX-RAW-14 | `Снимок экрана 2026-08-13 112409.png` | 8 | Fresh-read comparison and Bitrix default/system fields | Initial deal verification | ID, FRESH, SIDE EFFECTS | HIGH | GITHUB / SUPPORTING | Internal actor IDs | Supports create verification; not independently selected due volume. |
| BTX-RAW-15 | `Снимок экрана 2026-08-13 112434.png` | 9 | Continuation and summary of verified creation | Initial deal verification | FRESH, SIDE EFFECTS, LIMIT | MEDIUM | GITHUB / SUPPORTING | None apparent | Overlaps BTX-RAW-13/14. |
| BTX-RAW-16 | `Снимок экрана 2026-08-13 113014.png` | 10 | `NEW → PREPARATION` instruction and fresh pre-action read | Transition preparation | PROMPT, PRE, ID, FRESH | HIGH | WEBSITE + GITHUB | Synthetic deal title/ID | Strong pre-state and stop-before-write evidence. |
| BTX-RAW-17 | `Снимок экрана 2026-08-13 113042.png` | 11 | Planned exact tool/arguments and expected automatic effects | Transition preparation | PRE, ARGS, SIDE EFFECTS | HIGH | WEBSITE / GITHUB | Actor ID `1` is unnecessary | Shows planned invocation `{id:2, stage_id:PREPARATION}`. |
| BTX-RAW-18 | `Снимок экрана 2026-08-13 113056.png` | 12 | Explicit wait-for-approval boundary | Transition preparation | APPROVAL, ARGS, SIDE EFFECTS | HIGH | WEBSITE / GITHUB | None apparent | Short continuation; best used in a composite. |
| BTX-RAW-19 | `Снимок экрана 2026-08-13 113453.png` | 13 | Explicit approval, one update, response and separate fresh read | Transition execution | PROMPT, APPROVAL, RESPONSE, ID, FRESH | HIGH | WEBSITE + GITHUB | Synthetic deal ID | Strong acknowledgement and verification-transition evidence. |
| BTX-RAW-20 | `Снимок экрана 2026-08-13 113518.png` | 14 | Actual recorded arguments and fresh-read comparison | Transition verification | ARGS, ID, FRESH, SIDE EFFECTS | HIGH | WEBSITE + GITHUB | Actor-related IDs in lower table | Strong approval-to-action binding evidence. |
| BTX-RAW-21 | `Снимок экрана 2026-08-13 113542.png` | 15 | Continuation of field comparison and bounded summary | Transition verification | FRESH, SIDE EFFECTS, LIMIT | HIGH | GITHUB | Actor IDs | Establishes no visible change to listed unaffected fields; same underlying fresh read as BTX-RAW-20. |
| BTX-RAW-22 | `Снимок экрана 2026-08-13 114024.png` | 16 | Read-only request for independent history/timeline and attempted calls | Observability check | PROMPT, RESPONSE, LIMIT | HIGH | GITHUB | None apparent | Shows search for a distinct history source. |
| BTX-RAW-23 | `Снимок экрана 2026-08-13 114046.png` | 17 | Timeline endpoint results and explicit finding of no readable independent record | Observability boundary | RESPONSE, LIMIT | HIGH | WEBSITE + GITHUB | None apparent | Strongest direct limitation artifact. |
| BTX-RAW-24 | `Снимок экрана 2026-08-13 114105.png` | 18 | Deal-object transition fields distinguished from independent history | Observability boundary | ID, FRESH, SIDE EFFECTS, LIMIT | HIGH | WEBSITE + GITHUB | Synthetic deal ID | Prevents mischaracterizing deal fields as a separate history source. |
| BTX-RAW-25 | `Снимок экрана 2026-08-13 115654.png` | 19 | Preparation for later ambiguous-execution test; pre-state `PREPARATION` | Later transition preparation | PROMPT, PRE, ID, FRESH | MEDIUM | GITHUB / SUPPORTING | None apparent | Plans `PREPARATION → PREPAYMENT_INVOICE`; subsequent approval/response is not captured in this RAW set. |
| BTX-RAW-26 | `Снимок экрана 2026-08-13 115708.png` | 20 | Exact planned arguments and expected automatic fields; awaiting approval | Later transition preparation | PRE, ARGS, SIDE EFFECTS, APPROVAL | MEDIUM | GITHUB / SUPPORTING | Actor IDs | No captured execution response for this transition. |
| BTX-RAW-27 | `Снимок экрана 2026-08-13 121721.png` | 21 | New preparation run with fresh pre-state `PREPAYMENT_INVOICE` | Later transition preparation | PROMPT, PRE, ID, FRESH | MEDIUM | GITHUB / SUPPORTING | None apparent | Fresh state indirectly shows earlier transition occurred, but does not supply its missing acknowledgement. |
| BTX-RAW-28 | `Снимок экрана 2026-08-13 121739.png` | 22 | Live pipeline and planned next stage `EXECUTING` | Later transition preparation | PRE, ARGS, SIDE EFFECTS | MEDIUM | GITHUB / SUPPORTING | None apparent | Preparation only. |
| BTX-RAW-29 | `Снимок экрана 2026-08-13 121755.png` | 23 | Expected automatic effects and wait-for-approval state | Later transition preparation | APPROVAL, ARGS, SIDE EFFECTS | MEDIUM | GITHUB / SUPPORTING | Actor IDs | No execution response for `EXECUTING` is present. |
| BTX-RAW-30 | `Снимок экрана 2026-08-13 123525.png` | Final verification | Complete fresh read at `WON` with `PREVIOUS_STAGE_ID=FINAL_INVOICE` | Final verification | PROMPT, ID, FRESH, SIDE EFFECTS, LIMIT | HIGH | WEBSITE + GITHUB | Synthetic deal ID | Full-frame final-state evidence; capture time and embedded target timestamp use different timezone conventions. |
| BTX-RAW-31 | `Снимок экрана 2026-08-13 132002.png` | Final verification duplicate A | Upper portion of the same final `WON` fresh-read result | Final verification | PROMPT, ID, FRESH, SIDE EFFECTS | DUPLICATE / SUPPORTING | GITHUB / SUPPORTING | Synthetic deal ID | Higher-width split capture; same underlying read as BTX-RAW-30. |
| BTX-RAW-32 | `Снимок экрана 2026-08-13 132015.png` | Final verification duplicate B | Lower continuation of final `WON` fresh-read result | Final verification | FRESH, SIDE EFFECTS, LIMIT | DUPLICATE / SUPPORTING | GITHUB / SUPPORTING | Synthetic deal ID | Continuation of BTX-RAW-31; same underlying read as BTX-RAW-30. |
| BTX-RAW-33 | `Снимок экрана 2026-08-13 132410.png` | Final execution result | Recovered FRIS view shows exact `WON` arguments, definitive response and no retry statement | Client-side interruption / recovery | APPROVAL, ARGS, RESPONSE, ID, INTERRUPTION/RECOVERY, LIMIT | HIGH | WEBSITE + GITHUB | Synthetic deal ID | Does **not** visually capture the connection loss itself. The interruption is test context; the screenshot establishes the later surfaced result. |

## Inventory summary

- RAW files reviewed: **48**.
- Selected for website-derived evidence: **7 files**, constructed from 17 RAW source frames/crops.
- Selected for GitHub-derived evidence: **13 files**, derived from 13 primary RAW screenshots.
- Excluded as setup-only, sensitive, redundant, or technically non-essential: **35 RAW screenshots** from the GitHub selection; some remain referenced as supporting context.
- Missing direct evidence: the client-side disconnection screen; acknowledgement frames for some intermediate Bitrix transitions; a distinct readable Bitrix history/timeline record.
- Chronology note: filename times, UI sequence and Bitrix timestamps use different display/timezone conventions. The core sequence is reconstructable; the final result/fresh-read order is established by visible content and test context, not filename sorting alone.
