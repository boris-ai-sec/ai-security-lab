# Provenance and publication boundary

Restoration date: **2026-10-22**. Base: repository `main` commit `160136585546ebc6f80cc6eca562d01c83cf4962`. No model calls, probe reruns, environment installation, or historical-result edits were performed.

## Sources and selection

The local historical archive is identified here only as `ai_security_lab`; personal filesystem locations are omitted. [SOURCE_ARTIFACTS.json](SOURCE_ARTIFACTS.json) records archive-relative filenames, exact byte sizes, and SHA-256 hashes for 12 raw Garak artifacts and the five files copied into this package.

- Four `garak_runs/garak.<run-id>.report.jsonl` files are the primary Garak evidence. Each has one setup, one init, three eval records, one completion, one digest, and 1,536 attempt records. Attempt records include two statuses; the extraction counts only completed status 2 detector arrays, avoiding double counting.
- The four corresponding HTML reports and four hitlogs were located and hashed for inventory. They were not used as a separate measurement series. HTML risk labels and aggregate scores are not republished as security conclusions.
- `configs/lmstudio_config.yaml`, both YAML files in `tests/2026-05-05_promptfoo_llama3.2/`, and both PNGs in `screenshots/promptfoo/` are copied without changes. The source manifest maps them to public paths. Package-local Git attributes preserve the archived YAML line endings.
- Two Garak terminal screenshots were inspected. One shows an incomplete run; the completion capture includes a personal filesystem path. Neither is needed beside the extracted report records, so both are excluded.
- Other available configs (`configs/promptfooconfig.yaml`, `configs/deepseek-config.yaml`) are excluded: they describe additional prompts/providers without establishing corresponding execution results in this selected package.
- Historical narrative documents, including `lab_promtfoo.txt`, `AI Security Testing Lab.txt`, and an older full-context document, were located. They are not primary evidence for the published counts. Unverified benchmark claims, broad risk wording, personal context, and manual-exercise passwords are excluded.

## Original artifacts versus derived evidence

[historical-summary.json](garak/historical-summary.json) is a **newly derived field projection**, not an original run report. It contains four runs, selected setup fields, the complete init/eval/completion fields selected by the extractor, and original 1-based line numbers. It omits prompts, responses, attempt payloads, private paths, full configuration dumps, and report calibration/risk prose.

[extract_summary.py](garak/extract_summary.py) documents the field allowlist. It hashes every source report byte while parsing, checks record counts and run IDs, and independently recomputes pass/fail totals from completed attempt detector arrays. Its output matches the retained projection. The [Garak table](garak/README.md) uses `100 * fails / total_evaluated`, rounded to two decimals. It reports all three retained probes for all four runs; it selects no favorable subset within those runs.

The source hashes identify the archived files checked during restoration. Public access to those raw files is not provided, and hashes alone do not authenticate their historical origin. Public reviewers can inspect selected records and screenshots; full independent recomputation requires the corresponding local archive. No hosted raw-evidence download or archival chain of custody is claimed.

## Verified facts and unresolved questions

| Verified from selected artifacts | Not established |
|---|---|
| Garak 0.14.1; four target identifiers; three PromptInject probes and AttackRogueString detector; recorded timestamps and completion records | Exact weight identities, quantization, server/Ollama versions, hardware, timezone offsets, and complete reproducible environment |
| Twelve eval counts agree with completed-attempt detector scores | General model security, unbiased cross-model ranking, statistical independence of repeated generations, or production exploitability |
| Promptfoo YAML provider IDs, prompts, temperature settings, and lexical assertions | Promptfoo version, exact screenshot-to-config binding, complete result exports, and reliable security pass rates |
| Visible Qwen refusal with one displayed assertion pass; comparison screenshot contains refusals and assertion failures | Actual secret disclosure, existence of a protected secret, or Dolphin backend response text behind failure messages |

The Qwen screenshot's evaluation ID supplies a recorded date/time; the comparison folder date is organizational context, not proof of its execution time. No new tests were run to fill those gaps.

## Privacy, size, integrity, and claim audit

The 12 raw Garak files total **151,949,441 bytes** (about 145 MiB). They remain outside the public package because of size, redundant payloads, embedded personal paths, and unnecessary prompt/response content. The compact projection preserves the bounded measurement basis. No raw file was deleted or changed.

Selected text/configs were checked for credentials and private paths. Prompt terms such as “system password” are test instructions, not credential values. Both published screenshots were visually inspected; their only PNG metadata is color/gamma/resolution information. The selected files contain no actual password, token, or personal filesystem path found during this review.

Claims remain limited to recorded laboratory conditions. The package does not claim overall model insecurity, universal vulnerability, production compromise, systemic risk, certification, or a full professional red-team engagement. Promptfoo assertion defects are explained rather than converted into security findings. Current labs and repository positioning are preserved.

[SHA256SUMS.txt](SHA256SUMS.txt) binds the public package files other than itself using their Git-object bytes. After checkout, verify from the repository root:

```bash
python tools/verify_git_object_checksums.py labs/early-adversarial-testing/SHA256SUMS.txt
```

This verifies public-file integrity only. It neither replays the experiments nor supplies the excluded raw evidence. Historical YAML assertions are retained for inspection; they are not a current supported evaluation contract.
