# Requirements and Reproduction Limits

## Recommended external-review path

The bounded inspection path documented in the root README requires:

- Git;
- Python 3.9 or newer;
- a local clone of this repository.

It does not require Langflow, Qdrant, Ollama, Phoenix, model weights, credentials, or network access after cloning.

Run from the repository root:

```bash
python tools/verify_git_object_checksums.py labs/LAB-RAG-EXT-002/SHA256SUMS.txt
```

The verifier reads bytes directly from Git objects. This avoids checkout-dependent newline conversion and does not modify retained evidence.

## Reproduction boundary

The recommended path supports:

- checksum verification of retained Git objects;
- inspection of sanitized public run records;
- comparison of declared results;
- review of the evidence manifest, validation status, and limitations.

It does not support a full replay of the source Langflow/Qdrant experiment because raw flow exports, local service configuration, credentials, caches, and internal validation artifacts are intentionally outside the public package.

## Other repository paths

- [`labs/LAB-RH-02A/source/`](labs/LAB-RH-02A/source/) has its own `pyproject.toml` and `uv.lock`; follow that lab's publication boundary and correction notes before execution.
- Historical notebooks may depend on Ollama, Jupyter, local model files, GPU-specific packages, or services that are not covered by a single supported repository-wide setup.
- Root [`requirements.txt`](requirements.txt) is an early environment snapshot retained for provenance. It is not a minimal dependency set and should not be treated as the supported installation contract for current evidence packages.

Do not infer full reproducibility where a package provides only retained evidence inspection or bounded reconstruction.
