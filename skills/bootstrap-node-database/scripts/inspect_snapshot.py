#!/usr/bin/env python3
"""Verify a Leios snapshot artifact and inspect its tar.zst without extracting it."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CHUNK_BYTES = 8 * 1024 * 1024


def fail(message: str) -> None:
    raise ValueError(message)


def load_manifest(metadata_path: Path, checksum_path: Path, archive: Path) -> dict[str, Any]:
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read snapshot metadata: {exc}")

    if not isinstance(metadata, dict):
        fail("snapshot metadata must be a JSON object")
    artifact = metadata.get("artifact")
    digest = metadata.get("sha256")
    size = metadata.get("bytes")
    if artifact != archive.name:
        fail(f"metadata artifact {artifact!r} does not match archive basename {archive.name!r}")
    if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
        fail("metadata bytes must be a positive integer")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        fail("metadata sha256 must be 64 lowercase hexadecimal characters")

    try:
        fields = checksum_path.read_text(encoding="utf-8").split()
    except OSError as exc:
        fail(f"cannot read checksum manifest: {exc}")
    if len(fields) != 2 or fields != [digest, artifact]:
        fail("checksum manifest must contain exactly the metadata digest and archive basename")
    return metadata


def hash_file(path: Path, expected_bytes: int) -> tuple[str, os.stat_result]:
    try:
        before = path.stat(follow_symlinks=False)
    except OSError as exc:
        fail(f"cannot stat archive: {exc}")
    if not path.is_file() or path.is_symlink():
        fail("archive must be a regular file, not a symlink")
    if before.st_size != expected_bytes:
        fail(f"archive size {before.st_size} differs from metadata size {expected_bytes}")

    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(CHUNK_BYTES):
                digest.update(chunk)
    except OSError as exc:
        fail(f"cannot hash archive: {exc}")
    return digest.hexdigest(), before


def validate_member(member: tarfile.TarInfo) -> tuple[str, tuple[str, ...]]:
    raw_name = member.name
    if not raw_name or "\x00" in raw_name or "\\" in raw_name:
        fail(f"invalid archive member name: {raw_name!r}")
    if raw_name.startswith("/"):
        fail(f"absolute archive member path: {raw_name!r}")

    parts = raw_name.split("/")
    if parts[-1] == "":
        parts.pop()  # A trailing slash is normal for a directory entry.
    if not parts or any(part in ("", ".", "..") for part in parts):
        fail(f"unsafe archive member path: {raw_name!r}")
    path = PurePosixPath(*parts)
    if path.is_absolute() or ".." in path.parts:
        fail(f"unsafe archive member path: {raw_name!r}")
    if not (member.isfile() or member.isdir()):
        fail(f"unsupported archive member type at {raw_name!r}")
    if member.isfile() and member.size < 0:
        fail(f"negative file size at {raw_name!r}")
    return raw_name, tuple(parts)


def inspect_tar(
    archive: Path,
    zstd: str,
    expected_root: str | None,
    required_directories: list[str],
    required_files: list[str],
) -> dict[str, Any]:
    try:
        process = subprocess.Popen(
            [zstd, "-dc", str(archive)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        fail(f"cannot start zstd decompressor {zstd!r}: {exc}")
    assert process.stdout is not None
    assert process.stderr is not None

    count = 0
    expanded_bytes = 0
    roots: Counter[str] = Counter()
    kinds: Counter[str] = Counter()
    seen: dict[tuple[str, ...], str] = {}
    top_directory_roots: set[str] = set()

    try:
        with tarfile.open(fileobj=process.stdout, mode="r|") as archive_stream:
            for member in archive_stream:
                raw_name, parts = validate_member(member)
                if parts in seen:
                    fail(f"duplicate archive member path: {raw_name!r}")
                seen[parts] = "directory" if member.isdir() else "file"
                count += 1
                roots[parts[0]] += 1
                if member.isdir():
                    kinds["directory"] += 1
                    if len(parts) == 1:
                        top_directory_roots.add(parts[0])
                else:
                    kinds["file"] += 1
                    expanded_bytes += member.size
                    if len(parts) == 1:
                        fail(f"archive has a file outside its top-level database directory: {raw_name!r}")

        process.stdout.close()
        return_code = process.wait()
        stderr = process.stderr.read().decode("utf-8", errors="replace")
        if return_code != 0:
            fail(f"zstd exited with status {return_code}: {stderr[:500]}")
    except BaseException:
        if process.poll() is None:
            process.kill()
        process.wait()
        raise

    if count == 0:
        fail("archive is empty")
    if len(roots) != 1:
        fail(f"expected one top-level database directory; found {sorted(roots)}")
    root = next(iter(roots))
    if top_directory_roots != {root}:
        fail(f"top-level member {root!r} is not an explicit directory entry")
    if expected_root is not None and root != expected_root:
        fail(f"archive database root {root!r} differs from expected root {expected_root!r}")

    def validate_required(relative_path: str, expected_kind: str) -> None:
        raw_parts = relative_path.split("/")
        if (
            not relative_path
            or relative_path.startswith("/")
            or "\\" in relative_path
            or any(part in ("", ".", "..") for part in raw_parts)
        ):
            fail(f"invalid required {expected_kind} path: {relative_path!r}")
        key = (root, *raw_parts)
        if seen.get(key) != expected_kind:
            fail(f"required {expected_kind} is missing or has the wrong type: {relative_path!r}")

    for relative_path in required_directories:
        validate_required(relative_path, "directory")
    for relative_path in required_files:
        validate_required(relative_path, "file")

    return {
        "members": count,
        "member_types": dict(sorted(kinds.items())),
        "top_level_member_counts": dict(sorted(roots.items())),
        "database_root": root,
        "expanded_file_bytes": expanded_bytes,
        "required_directories": required_directories,
        "required_files": required_files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--checksum", required=True, type=Path)
    parser.add_argument("--zstd", default="zstd", help="zstd executable (default: zstd on PATH)")
    parser.add_argument("--expected-root", help="require this exact observed top-level database directory")
    parser.add_argument("--require-dir", action="append", default=[], help="require a directory path relative to the detected database root")
    parser.add_argument("--require-file", action="append", default=[], help="require a regular file path relative to the detected database root")
    args = parser.parse_args()

    try:
        metadata = load_manifest(args.metadata, args.checksum, args.archive)
        digest, initial_stat = hash_file(args.archive, metadata["bytes"])
        if digest != metadata["sha256"]:
            fail(f"archive SHA-256 {digest} differs from metadata {metadata['sha256']}")
        archive_info = inspect_tar(
            args.archive,
            args.zstd,
            args.expected_root,
            args.require_dir,
            args.require_file,
        )
        final_stat = args.archive.stat(follow_symlinks=False)
        if (initial_stat.st_dev, initial_stat.st_ino, initial_stat.st_size, initial_stat.st_mtime_ns) != (
            final_stat.st_dev,
            final_stat.st_ino,
            final_stat.st_size,
            final_stat.st_mtime_ns,
        ):
            fail("archive changed during inspection; discard and restage it")
    except (OSError, ValueError, tarfile.TarError, subprocess.SubprocessError) as exc:
        print(f"snapshot inspection failed: {exc}", file=sys.stderr)
        return 1

    result = {
        "status": "verified",
        "artifact": metadata["artifact"],
        "bytes": metadata["bytes"],
        "sha256": digest,
        "node_version": metadata.get("node_version"),
        "node_rev": metadata.get("node_rev"),
        "snapshot_created": metadata.get("snapshot_created"),
        **archive_info,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
