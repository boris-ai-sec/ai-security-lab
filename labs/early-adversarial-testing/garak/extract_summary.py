"""Project four archived Garak reports without publishing prompts or responses.

Standard library only. Reads local artifacts; never invokes a model or service.
"""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path


RUN_IDS = (
    "0cf3d3cf-0765-4d3f-8048-38d2c7371017",
    "276eda05-0cdf-4800-b040-43cf12adcf04",
    "c9506907-4403-49f9-a9cf-6b339dd6211a",
    "fc631ff7-fcc6-4f81-9b46-9c0e9fc5affc",
)
FIELDS = {
    "start_run setup": (
        "entry_type", "transient.run_id", "transient.starttime_iso",
        "plugins.target_type", "plugins.target_name", "plugins.probe_spec",
        "run.generations", "run.seed", "run.target_lang",
        "run.soft_probe_prompt_cap",
    ),
    "init": ("entry_type", "garak_version", "start_time", "run"),
    "eval": (
        "entry_type", "probe", "detector", "passed", "fails", "nones",
        "total_evaluated", "total_processed", "confidence_method",
        "confidence", "confidence_upper", "confidence_lower",
    ),
    "completion": ("entry_type", "end_time", "run"),
}


def extract(archive_root):
    runs = []
    for run_id in RUN_IDS:
        relative = f"garak_runs/garak.{run_id}.report.jsonl"
        path = archive_root / relative
        digest = hashlib.sha256()
        records = []
        counts = Counter()
        scores = defaultdict(Counter)
        size = 0
        with path.open("rb") as source:
            for line_number, line in enumerate(source, 1):
                digest.update(line)
                size += len(line)
                record = json.loads(line)
                entry_type = record.get("entry_type")
                counts[entry_type] += 1
                if entry_type in FIELDS:
                    records.append({
                        "source_line": line_number,
                        "record": {key: record[key] for key in FIELDS[entry_type]},
                    })
                if entry_type == "attempt" and record.get("status") == 2:
                    for detector, values in record["detector_results"].items():
                        scores[(record["probe_classname"], detector)].update(values)
        expected = {
            "start_run setup": 1, "init": 1, "attempt": 1536,
            "eval": 3, "completion": 1, "digest": 1,
        }
        if dict(counts) != expected:
            raise ValueError(f"Unexpected record counts: {relative}")
        audit = []
        for item in records:
            record = item["record"]
            entry_type = record["entry_type"]
            if entry_type == "start_run setup":
                identity = record["transient.run_id"]
            elif entry_type in ("init", "completion"):
                identity = record["run"]
            else:
                values = scores[(record["probe"], record["detector"])]
                if not (
                    set(values) <= {0.0, 1.0}
                    and values[0.0] == record["passed"]
                    and values[1.0] == record["fails"]
                    and record["nones"] == 0
                    and sum(values.values()) == record["total_evaluated"]
                    == record["total_processed"]
                ):
                    raise ValueError(f"Detector-count mismatch: {relative}")
                audit.append({
                    "probe": record["probe"], "detector": record["detector"],
                    "status_2_score_0_count": values[0.0],
                    "status_2_score_1_count": values[1.0],
                })
                continue
            if identity != run_id:
                raise ValueError(f"Run identity mismatch: {relative}")
        runs.append({
            "source": {"path": relative, "size_bytes": size,
                       "sha256": digest.hexdigest()},
            "record_counts": dict(counts),
            "selected_records": records,
            "recomputed_detector_counts": audit,
        })
    return {"schema_version": 1, "evidence_status": "historical_derived_projection",
            "runs": runs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive_root", type=Path)
    parser.add_argument("--check", type=Path, help="Compare with retained summary JSON")
    args = parser.parse_args()
    summary = extract(args.archive_root)
    if args.check:
        if summary != json.loads(args.check.read_text(encoding="utf-8")):
            raise SystemExit("FAIL: retained projection differs from archived evidence")
        print("PASS: 4 source reports and 12 recomputed detector counts match")
    else:
        print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
