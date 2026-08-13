# Publication Boundary

This curated Lab is approved for public GitHub release. FRIS publication permission has been confirmed by the Project Owner. Final publication sanitization has been completed for the 13 selected evidence artifacts.

The public release remains a **bounded technical evidence study**. Permission to publish does not strengthen the evidentiary claims or expand the tested scope.

| Artifact | GitHub release | FRIS permission | Sanitization | Publication note |
|---|---:|---:|---:|---|
| MS01 pre-action scope | Yes | Obtained | PASS | Synthetic test object |
| MS02 approval/execution | Yes | Obtained | PASS | Synthetic test object |
| MS03 invocation | Yes | Obtained | PASS | Exact invocation retained for evidence linkage |
| MS04 fresh read | Yes | Obtained | PASS | Synthetic object ID/default codes retained where evidentially useful |
| MS05 target audit | Yes | Obtained | PASS | Actor/user and IP-like value redacted in curated copy |
| MS06 side-effect limit | Yes | Obtained | PASS | Bounded audit-window limitation preserved |
| BTX01 deal creation | Yes | Obtained | PASS | Synthetic deal ID/title |
| BTX02 pre-state/plan | Yes | Obtained | PASS | Synthetic deal ID/title |
| BTX03 approval/response | Yes | Obtained | PASS | Synthetic deal ID |
| BTX04 invocation/fresh state | Yes | Obtained | PASS | System-generated actor values retained only where non-sensitive and evidentially useful |
| BTX05 observability limit | Yes | Obtained | PASS | Negative/limited evidence intentionally preserved |
| BTX06 recovered result | Yes | Obtained | PASS | Interruption remains supplied test context, not screenshot-proven fact |
| BTX07 final fresh state | Yes | Obtained | PASS | Synthetic deal ID and target timestamps retained for evidence linkage |

## Public evidence set

- Curated GitHub evidence artifacts: **13** (`6 MoySklad`, `7 Bitrix24`).
- RAW corpus reviewed during curation: **48 screenshots**.
- The complete RAW corpus is **not** part of the public repository release.
- Unused/setup/redundant RAW evidence is intentionally excluded from publication.

## Claim boundary

This Lab is not:

- a penetration test;
- a certification;
- a full security assessment of FRIS;
- a platform benchmark;
- production validation;
- evidence of overall FRIS reliability;
- evidence of universal control effectiveness;
- evidence that the same results generalize to other agent architectures.

Negative and limited evidence remains part of the result, including the unavailable separately readable Bitrix history source, bounded MoySklad audit coverage, and the fact that the client-side interruption itself is not captured in the screenshots.

## Release status

Technical package: **PASS**
Framework publication review: **PASS**
Final sanitization: **PASS**
FRIS publication permission: **OBTAINED**
Project Owner authorization: **APPROVED**
GitHub disposition: **READY FOR PUSH**
