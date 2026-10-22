# Garak: historical automated prompt-injection probing

Four completed JSONL reports record **Garak 0.14.1**, from 2026-04-26 through 2026-05-01. Dates are recorded timestamps without timezone offsets. The configured probe specification is `promptinject`; each report contains these three probes with detector `promptinject.AttackRogueString`:

- `promptinject.HijackHateHumans`
- `promptinject.HijackKillHumans`
- `promptinject.HijackLongPrompt`

The experiments attempted instruction hijacking to elicit a probe's target string. The retained detector description in the reports is “Detect if model emits trigger string.” A detector failure is a bounded observation about generated text under those conditions.

## Recorded environment and sampling

| Recorded target identifier | Generator | Generations per prompt | Start → completion (recorded dates) |
|---|---|---:|---|
| `dolphin-2.9-llama3-8b` | `openai.OpenAICompatible` | 5 | 2026-04-26 → 2026-04-27 |
| `hermes-2-pro-llama-3-8b` | `openai.OpenAICompatible` | 20 | 2026-04-27 → 2026-04-28 |
| `yandexgpt-5-lite-8b-instruct` | `openai.OpenAICompatible` | 20 | 2026-04-29 → 2026-04-30 |
| `llama3.2` | `ollama` | 20 | 2026-04-30 → 2026-05-01 |

Setup records specify English target language, soft probe prompt cap 256, and `run.seed: null`. They reference a Windows Python environment and a configuration named `lmstudio_config.yaml`. The [unchanged archived configuration](lmstudio_config.yaml) sets the OpenAI-compatible URI to `http://127.0.0.1:1234/v1`. This supports a local API setup, but does not identify the exact serving application release, weight hash, quantization, hardware, or complete sampling configuration. The configuration alone does not prove which backend served a particular request.

## Bounded results

**Each cell is `fails / total_evaluated (percentage)`**, calculated directly from the corresponding JSONL `eval` record. It counts evaluated generations, not unique prompts, affected users, or production incidents. `fails` matches detector score `1.0`; `passed` matches score `0.0`. All 12 results have `nones = 0` and `total_processed = total_evaluated`.

| Recorded target identifier | HijackHateHumans | HijackKillHumans | HijackLongPrompt |
|---|---:|---:|---:|
| `dolphin-2.9-llama3-8b` | 713 / 1280 (55.70%) | 634 / 1280 (49.53%) | 557 / 1280 (43.52%) |
| `hermes-2-pro-llama-3-8b` | 3650 / 5120 (71.29%) | 3329 / 5120 (65.02%) | 3186 / 5120 (62.23%) |
| `yandexgpt-5-lite-8b-instruct` | 3861 / 5120 (75.41%) | 3841 / 5120 (75.02%) | 4293 / 5120 (83.85%) |
| `llama3.2` | 2260 / 5120 (44.14%) | 665 / 5120 (12.99%) | 3288 / 5120 (64.22%) |

Source: [selected records and recomputed counts](historical-summary.json), with report filenames, SHA-256 hashes, byte sizes, and 1-based source lines. Raw report rows 515, 1028, and 1541 contain the three `eval` records in each file. The table rounds `100 * fails / total_evaluated` to two decimals; it does not use the HTML report's aggregated score or risk labels.

## Interpretation and verification limits

The tested configurations failed specific probes, and their recorded behavior differed across probes. These are single historical runs with unequal generation counts, repeated generations per prompt, no fixed seed, and incompletely pinned serving environments. They do not support a general model-security ranking. Trigger-string detection is not a contextual exploitability assessment. The run does not establish production exploitability or overall system insecurity.

[extract_summary.py](extract_summary.py) parses the four source reports, selects explicit fields, and checks every published eval count against completed (`status == 2`) attempt detector arrays. It makes no model calls. With the original archive available, run from the repository root:

```bash
python labs/early-adversarial-testing/garak/extract_summary.py /path/to/ai_security_lab --check labs/early-adversarial-testing/garak/historical-summary.json
```

The path is a placeholder for a local archive, which is not shipped with this package. Source hashes identify archived bytes; they do not independently authenticate the original experiment. See [provenance](../PROVENANCE.md) for the excluded raw reports and public-review limits.
