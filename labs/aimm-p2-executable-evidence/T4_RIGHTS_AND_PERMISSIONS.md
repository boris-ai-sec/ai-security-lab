# T4 Research Collaboration — Rights & Permissions V0.1

**Date:** 2026-11-12  
**Prepared for participant review by:** Boris Abuzov  
**Status:** `REVIEW_DRAFT / NON_OPERATIVE / PARTICIPANT_ACCEPTANCE_PENDING`

**Publication of this review draft does not itself grant any new license, transfer intellectual property, establish participant consent or authorize implementation or experimental execution. Existing licenses and permissions remain unaffected.** This is a T4-specific collaboration proposal, not a general open-source license or signed agreement.

**Technical reference:** [Test Contract V0.3.4, immutable commit `cf45e063a4cbed022bce7f6f730c025f642d6613`](https://github.com/boris-ai-sec/ai-security-lab/blob/cf45e063a4cbed022bce7f6f730c025f642d6613/labs/aimm-p2-executable-evidence/TEST_CONTRACT_V0.3.4.md), particularly §10/F6; document SHA-256 `e42e29e016126a9c66fc9c7df0aa22038243f1f15366419ab1a9a7a8a2f82611`. Its status remains `FINAL_FREEZE_CANDIDATE / NOT_FROZEN / LAB_NOT_AUTHORIZED / ERP_NOT_RUN`. This draft does not close F6.

## 1. Ownership and existing terms

**Background intellectual property remains with its original owner.** Pre-existing code, designs, laboratory infrastructure, documentation and other IP retain their existing ownership and licensing conditions. Boris retains rights in his independently developed historical laboratory materials and other original background contributions; this does not assert ownership of embedded third-party material. ARC, Guardian, protocols, libraries and dependencies remain governed by their respective rights holders and applicable terms.

Participation creates no IP assignment, automatic joint ownership or broad relicensing. Each contributor retains their separately authored contributions unless a separate explicit agreement provides otherwise. Reviewing a design does not make the reviewer a software co-author. Joint authorship and rights must be established from actual contributions, not presumed.

The repository's [LICENSE_SCOPE.md](https://github.com/boris-ai-sec/ai-security-lab/blob/cf45e063a4cbed022bce7f6f730c025f642d6613/LICENSE_SCOPE.md) limits MIT to enumerated files; laboratories, reports and evidence are excluded. [THIRD_PARTY_NOTICES.md](https://github.com/boris-ai-sec/ai-security-lab/blob/cf45e063a4cbed022bce7f6f730c025f642d6613/THIRD_PARTY_NOTICES.md) preserves third-party terms. Historical HABR003/shared-cumulative-authority is **excluded from any automatic new commercial grant**, consistent with its [historical licensing boundary](https://github.com/boris-ai-sec/ai-security-lab/blob/524db880699655b76d5021b967c4118370702e58/LICENSE_SCOPE.md).

Source review found ARC's pinned [MIT license](https://github.com/suirindo/agent-role-contracts/blob/873b4104a95e443ba22367cf8378deb7dcbe6cfd/LICENSE), naming Netsujo株式会社, and the Guardian reference's pinned [Apache-2.0 license](https://github.com/Noctis-dev1/acs-conformance/blob/943a495eefa4447667cc335ce1362e90390705e6/LICENSE) and [README attribution to Malachi Zion Kopman](https://github.com/Noctis-dev1/acs-conformance/blob/943a495eefa4447667cc335ce1362e90390705e6/README.md#license). These observations do not establish authority to grant additional rights in every component or future contribution. Existing license permissions and obligations apply independently; this proposal neither narrows nor enlarges them.

## 2. Proposed reciprocal permission

**Proposed model: reciprocal, non-exclusive, royalty-free research and commercial use of expressly designated T4 contributions.** Upon operative approval by the relevant rights holders, identified participating recipients would receive permission, within the accepted inventory scope, to copy and use covered components for independent research, experimentation, professional consulting and technical assurance, internal assessment/diagnostics, training, demonstrations and professional education, and further development/adaptation. Permitted use would include commercial client services, subject to third-party terms and confidentiality restrictions.

No revenue sharing would be required merely because a permitted component supports a consulting service. Using code to provide a service does not transfer ownership or give the client a code license. Sale of code, redistribution, sublicensing, standalone software-product packaging, or disclosure of previously restricted source requires authorization under an applicable existing license or a separately agreed permission. Delivering code or embedded restricted material to a client must be covered separately from providing the service. This draft creates neither unrestricted sublicensing nor rights to the entire T4 laboratory.

## 3. Proposed scope and contribution inventory

The categories below are a planning matrix, **not an operative grant or an approved file inventory**. Future files and contributors remain pending.

| Material | Rights holder / provenance | Proposed use | Distribution / reuse boundary | Additional permission required |
|---|---|---|---|---|
| Boris's background laboratory materials, including HABR003 | Boris for his original material; third-party rights retained | Existing permissions only; any T4 reuse separately specified | No automatic new commercial or whole-lab grant | Boris's file-specific approval and applicable third-party clearance |
| ARC / Guardian background references | Respective holders; pinned notices in §1 | Existing MIT / Apache-2.0 permissions where applicable | Preserve applicable notices and conditions; no new rights inferred | Verify exact component/version coverage; extra rights only from authorized holders |
| Newly created T4 adapters, fixtures or infrastructure | Future authors/holders pending identification | Proposed §2 reciprocal use for listed components | No blanket inclusion of future files or client source delivery | Accepted versioned inventory and holder approval |
| Independently authored T4 contributions | Identified contributor or other established holder | Proposed §2 use within recorded scope | Contributor retains ownership; restrictions recorded per item | Explicit holder acceptance; employer/other rights checked where relevant |
| Jointly authored contributions, if established | Actual authorship and rights unresolved until recorded | Only the scope approved by the required holders | No presumed joint ownership or unilateral whole-work grant | Resolve authorship, granting authority and all necessary consents |
| Generated synthetic evidence, diagrams and reports | Provenance and any applicable rights determined per artifact | Cleared research, service and publication uses | Raw logs are not automatically public; confidential content excluded | Rights/provenance review, release clearance and reuse scope |
| Third-party dependencies, protocols and incorporated material | Their respective rights holders | Applicable existing terms only | No relicensing through T4 | Component/version review and any missing permissions |

Before material enters the arrangement, an approved versioned inventory/contribution record must identify: exact files/artifacts and commit or digest; background/new status and dependencies; author and authorized rights holder; named recipients; permitted copying, use, adaptation, execution and distribution; restrictions/notices; public-release status; and explicit acceptance evidence referencing the operative terms. All four conditions are required: identified contribution, identified authorized holder, recorded scope and explicit holder acceptance. Unknown rights stay **PENDING**, outside the proposed grant until resolved. Attribution follows actual contributions and retained notices.

## 4. Independent publications

**Independent publication permitted; proper attribution required; joint endorsement requires explicit consent.** Under the accepted operative arrangement, each participant would be free to publish independent articles, analyses, conference presentations, educational materials, portfolio descriptions and professional case studies using T4 material cleared for public release and authorized for that reuse. No blanket collective prepublication approval, general participant veto or mandatory waiting period would apply.

Publications must accurately attribute relevant contributions, preserve actual outcomes, limitations and evidence status, distinguish individual conclusions from collective findings, respect third-party copyrights/licenses, and avoid implying another participant's approval or official OWASP/AIMM endorsement. Naming the group as co-authors or claiming collective endorsement requires consent from the relevant named authors/endorsers. Disclosure of restricted material needs its rights holder's permission, not automatically unanimous group approval. Courtesy notification before major publications is encouraged without creating a veto or waiting period.

The proposed **preapproved public research materials** category comprises specifically cleared final research conclusions, publicly approved synthetic evidence packages, public architecture descriptions/diagrams, reproducible methodology descriptions and publicly released non-sensitive experiment outputs. Record exact artifacts/versions, authorized reuse and clearance by relevant holders in the inventory; subsequent independent publications need no repeated group approval within that scope. Public repository visibility alone does not supply missing reuse rights. Unpublished/confidential artifacts, private correspondence, restricted code and uncleared raw evidence remain outside this category.

## 5. Confidentiality and security

No participant may disclose credentials, signing keys, private data, unpublished restricted material or another participant's confidential information without appropriate authorization. No real customer or production data is covered. Executions remain confined to separately approved synthetic laboratory environments. Permission to inspect or use research materials does not authorize access to third-party production systems.

## 6. Separate authorization stages

Keep distinct: **(1)** rights/permissions acceptance; **(2)** joint Test Contract design freeze; **(3)** implementation authorization and participant admission; **(4)** independent code/QC acceptance; **(5)** explicit experimental-run authorization; **(6)** publication of observed results under the accepted release/publication rules. A permission agreement does not approve experiment execution. Technical review does not grant commercial rights in another participant's code. This V0.1 accomplishes none of these approvals.

## 7. Duration and ending collaboration

Propose that legitimately granted rights to accepted, identified contributions remain usable within the agreed scope after collaboration ends; merely leaving T4 should not allow unrestricted retroactive withdrawal. The operative terms must expressly settle duration, survival, termination for material breach, notice/remedy procedure, and treatment of previously distributed material and authorized adaptations. This review draft creates no binding perpetual or irrevocable license and does not alter duration or termination under existing licenses.

## 8. Acceptance required before operation

A later operative version requires explicit acceptance by each relevant rights holder for their covered material and by participating recipients for their conditions; an approved inventory identifying materials, recipients and permitted uses; immutable version/commit/document-hash references; recorded acceptance of commercial-use, publication and duration/termination terms; resolution of third-party rights; and any additional legal review participants deem necessary. Verify each representative's granting authority. Silence, participation, review comments and publication of this draft are **not acceptance**.

**Outstanding:** participant/holder identities and authority; covered inventory and reciprocal recipient scope; any separate distribution/product permissions; public-release clearances; duration/survival/breach terms; third-party compatibility and any requested legal review. No cross-jurisdiction legal effectiveness is asserted. V0.1 remains **NON-OPERATIVE**, with participant acceptance pending, no joint freeze and no implementation or run authorization.
