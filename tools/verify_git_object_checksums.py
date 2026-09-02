#!/usr/bin/env python3
"""Verify a SHA256SUMS file against byte-exact Git object content."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import PurePosixPath
import subprocess
import sys


def git_output(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return result.stdout


def repository_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"path must be repository-relative: {value}")
    return path


def parse_checksum_line(line: bytes) -> tuple[str, str]:
    expected_raw, separator, relative_raw = line.partition(b"  ")
    if not separator:
        raise ValueError("expected '<sha256><two spaces><relative path>'")

    expected = expected_raw.decode("ascii").lower()
    if len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
        raise ValueError("invalid SHA-256 value")

    relative = relative_raw.decode("utf-8")
    repository_path(relative)
    return expected, relative


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify SHA256SUMS entries using raw bytes from Git objects."
    )
    parser.add_argument("checksum_file", help="repository-relative SHA256SUMS path")
    parser.add_argument(
        "--commit",
        default="HEAD",
        help="commit or tree to inspect (default: HEAD)",
    )
    args = parser.parse_args()

    try:
        checksum_path = repository_path(args.checksum_file)
        commit = git_output("rev-parse", args.commit).decode("ascii").strip()
        checksum_bytes = git_output("show", f"{commit}:{checksum_path.as_posix()}")
    except (RuntimeError, UnicodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    entries = 0
    failed = 0

    for line_number, line in enumerate(checksum_bytes.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith(b"#"):
            continue

        entries += 1
        try:
            expected, relative = parse_checksum_line(line)
            target = checksum_path.parent / repository_path(relative)
            data = git_output("show", f"{commit}:{target.as_posix()}")
        except (RuntimeError, UnicodeError, ValueError) as error:
            print(f"FAIL line {line_number}: {error}")
            failed += 1
            continue

        actual = hashlib.sha256(data).hexdigest()
        if actual == expected:
            print(f"PASS {target.as_posix()}")
        else:
            print(f"FAIL {target.as_posix()}")
            print(f"  expected: {expected}")
            print(f"  actual:   {actual}")
            failed += 1

    if entries == 0:
        print("ERROR: no checksum entries found", file=sys.stderr)
        return 2

    if failed:
        print(f"FAIL {failed}/{entries} Git object checksums did not verify")
        return 1

    print(f"PASS {entries}/{entries} Git object checksums verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
