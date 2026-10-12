# Publication boundary and provenance

This package represents the approved **HABR003 V0.1** implementation and byte-identical frozen **V0.2** spec, validated on 2026-10-11. Publication preparation took place on 2026-10-12 and performed no new scenarios, runtime tests, concurrency research or new findings.

## Included

- Original ten lab modules, two test modules, pinned requirements, Compose, Dockerfile, grant and source ignore definitions.
- Public README/reproduction/validation documents, frozen specification, original validated source manifest and explicit source correspondence.
- Four representative eight-file bundles (32 original files), plus compact index of all 38 already-approved outcomes.
- Package MANIFEST.sha256; package .gitattributes preserves byte-exact source/evidence in Git.

## Deliberate omissions

- Generated credentials, .venv, caches and generated runtime state: local/non-source/private; reproducible generation/setup is retained.
- Internal engineering README/implementation report, full formal report/index, operator scripts and transcripts: contain internal coordination or absolute workstation paths; replaced by narrowly scoped public documentation/projections. Original document hashes remain in the validated source manifest.
- Remaining 34 raw bundles, duplicated component logs/boundary diagnostic copies, full container/network inspections, earlier failed-preflight archives and auxiliary debugging artifacts: unnecessary for the small representative package. Failure history and accepted counts remain disclosed in VALIDATION_SUMMARY.md.
- All unrelated Framework material, experiments, notes, migration prompts, commercial analysis and workstation metadata.

The selected eight-file evidence has no absolute workstation paths/usernames/secrets and is published byte-identically. No substantive sanitization changed its results, clocks or correlation. The original source manifest has no local absolute paths and is copied unchanged: SHA-256 `c2328a15864cfbbb761c01d618324e5e03447416cd0d50313b2dd9d30081988a`.

## Exactly bounded layout adaptation

Original lab/run.py used the private project hierarchy to locate output and the frozen spec. Only these two host-runner constants changed:

```diff
-OUT = ROOT.parents[2] / '00_Laboratory' / 'HABR003'
-SPEC = ROOT.parents[1] / '00_Planning' / 'HABR003_AGGREGATE_AUTHORITY_EXPERIMENT_SPEC_V0.2.md'
+OUT = ROOT / 'out'
+SPEC = ROOT / 'EXPERIMENT_SPEC_V0.2.md'
```

No admission, scheduling, transaction, lifecycle, ERP, accounting, test, request, grant or result logic changed. [Code correspondence](provenance/code-correspondence.json) records original/public hashes for each included original file. Original private implementation/spec/validation archives were not edited. The spec's freeze-time NOT EXECUTED text is preserved rather than silently updated.

## Fixed Git state and licensing

Article tag `shared-cumulative-authority-v1.0` identifies the final metadata envelope. The README records the initial content-publication commit; a following metadata-only commit adds that SHA and regenerates checksums, without changing implementation, tests, spec or evidence. Resolve the final immutable article commit through the annotated tag; retain the full tag-target commit URL when citing the article. No published tag is rewritten.

Existing repository LICENSE_SCOPE.md governs. New files are not added to its MIT-scoped list by this publication. No third-party dependency source is vendored or relicensed. This is a public inspectable reproducibility artifact, not a new repository-wide license grant.
