#!/usr/bin/env python3
"""Run deterministic, credential-free repository maturity checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote


ROOT = Path(
    subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout.strip()
)

CHECKSUM_MANIFESTS = (
    "labs/LAB-RAG-EXT-001/SHA256SUMS.txt",
    "labs/LAB-RAG-EXT-002/SHA256SUMS.txt",
    "labs/LAB-AGENT-EXEC-003/SHA256SUMS.txt",
    "labs/LAB-AGENT-EXEC-004/SHA256SUMS.txt",
)

KNOWN_CHECKSUM_CONDITIONS = {
    "labs/LAB-AGENT-EXEC-003/README.md": (
        "11d45333c895a2a3cce0d4439efcc66d08310ad399b949a19169c7ad9767b397",
        "02bae20fd994620cb2de57f98372264ecebd7a4e8acbb9e1c61d45d912bc604b",
    )
}

MIT_SCOPED_FILES = (
    "tools/verify_git_object_checksums.py",
    "tools/validate_repository.py",
    "notebooks/04_local_ollama_api.py",
    "labs/LAB-RH-02A/source/scripts/telemetry_smoke.py",
    "labs/LAB-RH-02A/source/telemetry/__init__.py",
    "labs/LAB-RH-02A/source/telemetry/manager.py",
    "labs/LAB-RH-02A/source-correction/scripts/telemetry_smoke.py",
    "labs/LAB-RH-02A/source-correction/telemetry/__init__.py",
    "labs/LAB-RH-02A/source-correction/telemetry/manager.py",
)

CHECKOUT_ACTION_SHA = "11d5960a326750d5838078e36cf38b85af677262"
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def git_bytes(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return result.stdout


def tracked_files(pattern: str) -> list[str]:
    output = git_bytes("ls-files", "-z", "--", pattern)
    return sorted(item.decode("utf-8") for item in output.split(b"\0") if item)


def git_object(path: str) -> bytes:
    return git_bytes("show", f"HEAD:{path}")


def check_checksum_manifests(errors: list[str]) -> None:
    known_seen: set[str] = set()
    total = 0
    verified = 0

    for manifest in CHECKSUM_MANIFESTS:
        parent = PurePosixPath(manifest).parent
        for line_number, raw_line in enumerate(git_object(manifest).splitlines(), start=1):
            if not raw_line.strip() or raw_line.lstrip().startswith(b"#"):
                continue
            total += 1
            expected_raw, separator, relative_raw = raw_line.partition(b"  ")
            if not separator:
                errors.append(f"{manifest}:{line_number}: malformed checksum line")
                continue
            try:
                expected = expected_raw.decode("ascii").lower()
                relative = relative_raw.decode("utf-8")
            except UnicodeError as error:
                errors.append(f"{manifest}:{line_number}: {error}")
                continue
            target_path = (parent / PurePosixPath(relative)).as_posix()
            actual = hashlib.sha256(git_object(target_path)).hexdigest()
            if actual == expected:
                verified += 1
                continue
            if KNOWN_CHECKSUM_CONDITIONS.get(target_path) == (expected, actual):
                known_seen.add(target_path)
                print(
                    "KNOWN CHECKSUM CONDITION: "
                    f"{target_path} expected={expected} actual={actual}"
                )
                continue
            errors.append(
                f"unexpected checksum mismatch: {target_path} "
                f"expected={expected} actual={actual}"
            )

    missing_known = set(KNOWN_CHECKSUM_CONDITIONS) - known_seen
    for path in sorted(missing_known):
        errors.append(f"declared checksum condition was not observed exactly: {path}")

    print(
        f"Checksums: {verified}/{total} entries verify; "
        f"known conditions={len(known_seen)}; unexpected={len(errors)}"
    )


def check_json(errors: list[str]) -> None:
    files = tracked_files("*.json")
    failures = 0
    for path in files:
        try:
            json.loads(git_object(path).decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"JSON parse failure: {path}: {error}")
            failures += 1
    print(f"JSON: {len(files) - failures}/{len(files)} files parse")


def normalized_link_target(source: str, raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    combined = Path(source).parent / Path(target.replace("/", str(Path("/").anchor or "/")))
    try:
        resolved = (ROOT / combined).resolve().relative_to(ROOT.resolve())
    except ValueError:
        return "__OUTSIDE_REPOSITORY__"
    return resolved.as_posix()


def check_markdown_links(errors: list[str]) -> None:
    files = tracked_files("*.md")
    checked = 0
    broken = 0
    for source in files:
        text = git_object(source).decode("utf-8")
        for match in LINK_PATTERN.finditer(text):
            target = normalized_link_target(source, match.group(1))
            if target is None:
                continue
            checked += 1
            if target == "__OUTSIDE_REPOSITORY__":
                errors.append(f"Markdown link escapes repository: {source}")
                broken += 1
                continue
            result = subprocess.run(
                ["git", "cat-file", "-e", f"HEAD:{target}"],
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            if result.returncode != 0:
                errors.append(f"broken Markdown link: {source} -> {target}")
                broken += 1
    print(f"Markdown: {len(files)} files; {checked} relative links; broken={broken}")


def check_python_syntax(errors: list[str]) -> None:
    files = tracked_files("*.py")
    failures = 0
    for path in files:
        try:
            compile(git_object(path), path, "exec")
        except (SyntaxError, ValueError, TypeError) as error:
            errors.append(f"Python syntax failure: {path}: {error}")
            failures += 1
    print(f"Python syntax: {len(files) - failures}/{len(files)} files compile")


def check_maturity_contract(errors: list[str]) -> None:
    scope = git_object("LICENSE_SCOPE.md").decode("utf-8")
    for path in MIT_SCOPED_FILES:
        if f"`{path}`" not in scope:
            errors.append(f"MIT-scoped file missing from LICENSE_SCOPE.md: {path}")
        try:
            git_object(path)
        except RuntimeError:
            errors.append(f"MIT-scoped file does not exist at HEAD: {path}")

    license_text = git_object("LICENSES/MIT.txt").decode("utf-8")
    if not license_text.startswith("MIT License\n"):
        errors.append("LICENSES/MIT.txt does not contain the standard MIT heading")
    if "Copyright (c) 2026 Boris Abuzov" not in license_text:
        errors.append("LICENSES/MIT.txt copyright attribution is missing")

    workflow = git_object(".github/workflows/repository-validation.yml").decode("utf-8")
    if f"actions/checkout@{CHECKOUT_ACTION_SHA}" not in workflow:
        errors.append("checkout action is not pinned to the reviewed commit")
    if "contents: read" not in workflow:
        errors.append("workflow does not declare read-only contents permission")
    if "secrets." in workflow:
        errors.append("workflow must not reference repository secrets")

    print(f"Maturity contract: scoped_files={len(MIT_SCOPED_FILES)}")


def main() -> int:
    errors: list[str] = []
    checks = (
        check_checksum_manifests,
        check_json,
        check_markdown_links,
        check_python_syntax,
        check_maturity_contract,
    )
    for check in checks:
        try:
            check(errors)
        except Exception as error:  # deterministic reporting at the CI boundary
            errors.append(f"{check.__name__} failed: {error}")

    if errors:
        print("\nVALIDATION FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("\nVALIDATION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
