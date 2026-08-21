# Publication Boundary

**Framework disposition:** approved with boundary.
**Artifact type:** bounded public laboratory evidence.

## Allowed public claims

- In this controlled workflow, independently configured approval and execution parameters produced an observed approval-to-action mismatch.
- The attempted write in the parameter-drift run was rejected by the target; no side effect occurred.
- In the corrected workflow, the tested material parameters used for human approval and execution were sourced from one Action Envelope.
- This removed the specific independently-hardcoded parameter-drift mechanism tested in the laboratory.
- In the final controlled path, the approved bound update was invoked, acknowledged by the target system, and confirmed by a fresh target read.

Preserve the distinction:

`invocation ≠ acknowledgement ≠ verification`

## Case D boundary

Do not describe Case D as a stale-state revalidation PASS or fail-closed control success.

Use only:

**STALE-STATE CONDITION OBSERVED / WRITE NOT EXECUTED / CAUSAL BLOCKING MECHANISM INCONCLUSIVE**

The approved baseline differed from fresh state and execution did not proceed, but the run used the older extractor later shown capable of returning `undefined`. The available evidence therefore does not cleanly isolate state mismatch as the causal reason for the FALSE branch.

## Limitations

- controlled synthetic environment;
- narrow title-update operation;
- not a production-readiness validation;
- not a penetration test;
- not a platform security audit;
- not evidence that n8n or Bitrix24 is generally secure or insecure;
- not proof that every approval bypass is prevented;
- not proof that an agent cannot be manipulated;
- one successful path is not evidence of general reliability;
- Case D causal blocking mechanism remains inconclusive.

`controlled evidence ≠ production assurance`

`acknowledgement ≠ verified final state`

## Excluded from publication

This public artifact does not include:

- the internal laboratory ZIP;
- the RAW evidence corpus;
- raw/final workflow JSON;
- OAuth or credential metadata;
- private Bitrix task/account data;
- P3;
- P6 / Bitrix UI corroboration.

The four included screenshots are sanitized publication derivatives. Screenshots are corroborating exhibits and do not independently establish platform-wide security, reliability, or production readiness.
