# Licensing Scope and Content Inventory

This repository uses a scoped licensing model. Publication in this repository does not by itself grant reuse rights.

## MIT-licensed source files

The MIT License in [`LICENSES/MIT.txt`](LICENSES/MIT.txt) applies only to the following original, standalone source files:

- `tools/verify_git_object_checksums.py`
- `tools/validate_repository.py`
- `notebooks/04_local_ollama_api.py`
- `labs/LAB-RH-02A/source/scripts/telemetry_smoke.py`
- `labs/LAB-RH-02A/source/telemetry/__init__.py`
- `labs/LAB-RH-02A/source/telemetry/manager.py`
- `labs/LAB-RH-02A/source-correction/scripts/telemetry_smoke.py`
- `labs/LAB-RH-02A/source-correction/telemetry/__init__.py`
- `labs/LAB-RH-02A/source-correction/telemetry/manager.py`

Repository history attributes these files to Boris Abuzov's repository identities, and no embedded third-party copyright or license notice was found in them during the V0.2 inventory. The MIT scope covers the listed source files, not the third-party packages, services, interfaces, protocols, or generated data with which they interact.

## Inventory and treatment

| Category | Repository material | Provenance / rights observation | Treatment |
|---|---|---|---|
| A. Original reusable source code | The explicitly listed `.py` files | Repository history attributes authorship to Boris Abuzov's repository identities; third-party libraries are imported but not incorporated into the license grant | MIT, only for the exact files listed above |
| B. Notebooks / executable examples | Root and `notebooks/*.ipynb` notebooks | Mixed code, narrative, stored outputs, model interactions, and historical environment context; cell-level provenance was not independently resolved | Excluded from MIT pending any later file-level owner review |
| C. Laboratory evidence records | `labs/**` case records, run records, manifests, validation and provenance records | Authored or curated laboratory publications that may include third-party system facts and generated results | Excluded from MIT |
| D. Reports / professional documentation | Root and lab Markdown other than this license-scope file | Professional explanatory, assessment, methodology-like, and publication text | Excluded from MIT |
| E. Screenshots / product-interface captures | `screenshots/**` and lab evidence PNG files | Captures may contain third-party product interfaces, names, marks, or generated responses even where the capture and redaction work are original | Excluded from MIT; third-party rights may apply |
| F. Generated outputs | Notebook outputs, run packages, traces, and other tool/model outputs | Produced through tools, models, services, or laboratory executions; generation does not establish unrestricted reuse rights | Excluded from MIT |
| G. Synthetic test data | `data/clean_docs/synthetic_company_policy.txt` and synthetic objects described in evidence | Created for controlled testing, but not designated reusable software | Excluded from MIT |
| H. Third-party or externally derived material | Product-interface content, service responses, names, marks, protocols, and externally derived facts | Subject to applicable third-party rights and terms | Not relicensed by this repository |
| I. Referenced dependencies | Packages named in `requirements.txt`, `pyproject.toml`, and `uv.lock` | Referenced by name/version or registry metadata; their source distributions are not presented as repository-authored code | Each dependency remains under its own license terms |
| J. Ambiguous items | Mixed notebooks, generated material, and any item without sufficiently resolved file-level provenance | Ownership or licensing scope is not established by repository publication alone | Excluded from MIT unless later reviewed and expressly added |

Except for the exact MIT-scoped files above, no repository-wide license grant is made. Evidence, screenshots, assessment records, professional documentation, publication artifacts, synthetic data, and generated outputs remain outside the MIT scope unless a later explicit notice states otherwise.

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for the bounded third-party and dependency notice.
