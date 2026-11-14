# T4 Pilot — §10/F6 Scoped Permissions Notice (V0.1)

**Prepared by:** Boris Abuzov · **14 November 2026**  
**Status:** `REVIEW_DRAFT / NON_OPERATIVE / ACCEPTANCE_PENDING`  
**Scope:** T4 C0–C3 design, ARC G1 × Guardian/Gateway R1 × isolated synthetic ERP  
**Technical baseline:** [Test Contract V0.3.4](https://github.com/boris-ai-sec/ai-security-lab/blob/cf45e063a4cbed022bce7f6f730c025f642d6613/labs/aimm-p2-executable-evidence/TEST_CONTRACT_V0.3.4.md) at `cf45e063a4cbed022bce7f6f730c025f642d6613`; SHA-256 `e42e29e016126a9c66fc9c7df0aa22038243f1f15366419ab1a9a7a8a2f82611`.

This notice makes the file- and participant-specific scope requested by §10/F6 concrete. It is consistent with the published [Rights & Permissions V0.1](https://github.com/boris-ai-sec/ai-security-lab/blob/1c2d59060b97da8a2ea29bc4bf9faaf8035a064c/labs/aimm-p2-executable-evidence/T4_RIGHTS_AND_PERMISSIONS.md), which remains a non-operative shared reference. **This draft grants no new rights and does not authorize implementation or lab runs.** It can become operative only when its exact scope and terms are accepted by the relevant rights holders and recipients, approved by Boris, and pinned to an immutable version.

## 1. Participants

- **Boris Abuzov:** T4 integrator; identifies and approves inclusion of material for which he has granting authority.
- **Tomohiro Iida:** ARC/F1 review; prospective recipient of specifically covered T4 materials, subject to acceptance. No additional rights over ARC are assumed.
- **Malachi Kopman:** Guardian/F2–F5 review; prospective author/recipient for the Gateway-to-Guardian seam, Fixture Controller interface and Compose/network components. No implementation permission has yet been given.
- **Paolo Costanzo:** provenance and claim-boundary review **attribution only**. As Paolo requested, his review text and separately published research do not enter the §3 reciprocal code inventory; he is not a §2 recipient.

Participation does not imply a grant on behalf of an employer, another contributor, or OWASP. Any additional holder or recipient must be identified and agree explicitly.

## 2. Inventory and allowed scope

| Exact material / version | Rights holder / status | Scope now or proposed upon acceptance |
|---|---|---|
| `labs/aimm-p2-executable-evidence/TEST_CONTRACT_V0.3.4.md` at `cf45e063a4cbed022bce7f6f730c025f642d6613` (SHA-256 above) | Boris, **only for his original integration text**; others retain rights to separately authored material | **Proposed:** named accepted recipients may copy, annotate and adapt covered text for T4 research, design, training and professional assurance/consulting. No source distribution or blanket repo grant |
| `T4_RIGHTS_AND_PERMISSIONS.md` at `1c2d59060b97da8a2ea29bc4bf9faaf8035a064c`, SHA-256 `721f2a2ceeeab951f35e5a8b9a73a04922753b9afdba474f1c68ee25ee82efd5` | Boris-authored review draft | Shared reference only; **not** an existing permission grant |
| `t4-freeze-manifest-f2-f5-v0.1.md`, SHA-256 `b8956f01e13e7fb945ccf597861fe361d19bb57a2bb022f96443da41c6827f8d` | Draft by Malachi; holder and use scope to be confirmed | Review and propose edits; any wider copying, commercial adaptation or redistribution requires his authorized acceptance |
| ARC reference `suirindo/agent-role-contracts@873b4104a95e443ba22367cf8378deb7dcbe6cfd`; Guardian reference `Noctis-dev1/acs-conformance@943a495eefa4447667cc335ce1362e90390705e6` | Existing MIT and Apache-2.0 terms respectively, subject to exact licensed content | Existing license rights only; preserve license notices. This notice grants **no extra rights** |
| **Future new T4 files:** Gateway/Guardian adapter; Fixture Controller interface and activation/read log; Compose/network isolation; proxy, observer and verifier | **PENDING** — no pinned file list or established future holder yet | Add exact paths, commits/digests, author/holder, recipients, permissions and notices to an approved inventory **before copying/adapting code or beginning implementation** |
| Historical HABR003 / `labs/shared-cumulative-authority/**`; old runs, and future raw T4 evidence | Historic and third-party terms; future evidence release **PENDING** | **Excluded** from automatic T4 copying/relicensing or public release. Historic runs are not T4 results |

The published repository is **not MIT-licensed as a whole**: `LICENSE_SCOPE.md` excludes laboratories, reports and evidence from its enumerated MIT grant. Public visibility does not create additional permissions.

## 3. Proposed terms for files explicitly admitted to an operative inventory

Within each accepted file's precise scope: **non-exclusive, royalty-free copy/use/adaptation** for synthetic research, internal assessment, technical assurance, professional consulting, education and demonstrations. Contributor ownership remains unchanged. There is no revenue share merely for permitted consulting services. Commercial services do **not** imply rights to deliver restricted source code to clients.

**Not automatically allowed:** sale or sublicensing of code; standalone software redistribution or product packaging; adapting restricted historical HABR003 source; release of confidential material or raw logs; and use of production/customer systems. Existing open-source licenses apply independently. Each new contribution requires identified authorship, granting authority, exact files/versions and explicit holder and recipient acceptance. Duration, survival and termination conditions must be agreed before the permission becomes operative; this draft grants no perpetual rights.

Independent articles and case studies may use **specifically cleared public** T4 results and methodology with accurate attribution and evidence limitations. No collective publication veto is proposed for already cleared materials; restricted disclosures still require the relevant holder's clearance. Credit Paolo as **“provenance and claim-boundary review.”** Do not claim official OWASP/AIMM approval, group co-authorship or unperformed ERP results.

## 4. Gates that remain separate

1. **Rights:** accept/pin this notice and exact file inventory (including any new code), holders, recipients, permitted use and duration.
2. **Design freeze:** participants explicitly accept their scoped technical decisions on one pinned contract and manifest.
3. **Implementation:** separately authorize the new isolated T4 lab and name an implementer, exact code scope and independent QC reviewer. The author of a component is not its independent QC.
4. **Code/QC:** review the actual implementation and isolation, with no change to historical HABR003.
5. **Run:** separately authorize synthetic C0–C3 and diagnostic runs. No production data, secrets in evidence, or third-party systems.
6. **Publication:** independently verify evidence, clear exact release artifacts and attribute actual contributions.

**Outstanding before this notice can be made operative:** Boris's final owner approval; each affected holder/recipient's explicit acceptance; complete future file inventory and third-party checks; agreed duration/termination terms; named independent QC; immutable pinned approved notice. Silence or friendly design-review comments do **not** satisfy these conditions.

**Current state:** `NOT_FROZEN / LAB_NOT_AUTHORIZED / ERP_NOT_RUN`; this document is a prepared §10/F6 review draft, **not** completion of F6.
