# Early adversarial testing: Garak and Promptfoo

**Status: HISTORICAL / CURATED EVIDENCE.** Experiments recorded in April–May 2026; selected and checked on 2026-10-22. No model tests were rerun for this restoration.

Historical laboratory testing with Garak produced automated probe evidence across several local/open-weight model identifiers under the tested configurations. Promptfoo configurations and screenshots retain a small comparison of adversarial prompts, generated responses, and assertion behavior. These records document practical work with automated evaluation, local models, evidence retention, and interpretation of test output.

| Package | Retained evidence | Inspection path |
|---|---|---|
| [Garak](garak/README.md) | Four completed reports summarized as 12 probe/detector results, source line references, and a small historical configuration | Read the metric definitions and results table, then inspect the JSON projection |
| [Promptfoo](promptfoo/README.md) | Two historical YAML files and two unchanged screenshots | Compare each assertion with the visible response before interpreting PASS/FAIL |
| [Provenance](PROVENANCE.md) | Selection method, source hashes and sizes, exclusions, and verification limits | Distinguish original artifacts from the newly extracted summary |

This is an early stage in the laboratory progression: adversarial prompting and automated model probing → RAG/system boundaries → agent governance and runtime controls → observability and execution evidence. The [current repository inspection path](../../README.md) remains the entry point for later work.

## Claim boundary

The tested model/configurations failed specific Garak detector checks. These observations concern the recorded conditions; they do not establish production exploitability, overall model/system insecurity, or a full professional red-team engagement. Promptfoo PASS/FAIL labels reflect the configured assertions, which are inadequate security oracles in these examples. A refusal containing the word “password” can receive PASS.

Model identifiers are historical configuration labels, not independently verified weight identities. The raw Garak reports remain in the local historical archive and are not bundled here. Public readers can inspect the projection and screenshots; independent verification against raw reports requires access to the matching archived files. See [provenance and limitations](PROVENANCE.md).

This package is laboratory evidence and documentation outside the repository's scoped MIT grant. Third-party tools, model outputs, and interfaces retain their applicable rights; see [licensing scope](../../LICENSE_SCOPE.md).
