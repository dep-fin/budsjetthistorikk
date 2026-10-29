"""Verify fixed Git artifact bytes, strict JSON and PNG envelopes."""

import argparse
import hashlib
import json
import struct
import subprocess
import zlib
from pathlib import Path


def strict(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError("duplicate key " + k)
        d[k] = v
    return d


def constant(value):
    raise ValueError("non-finite JSON " + value)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--base", required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    root, output = a.root.resolve(), a.output.resolve()
    assert not output.exists()

    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args])

    candidate = git("rev-parse", "--verify", a.candidate + "^{commit}").decode().strip()
    base = git("rev-parse", "--verify", a.base + "^{commit}").decode().strip()

    def blob(name):
        return git("show", candidate + ":" + name)

    path = "docs/research/proposisjon16-62/"
    manifest = json.loads(
        blob(path + "delivery-manifest.json"), object_pairs_hook=strict, parse_constant=constant
    )
    bound = []
    for entry in manifest["files"]:
        raw = blob(entry["path"])
        if entry["representation"] == "UTF-8/LF":
            assert b"\r" not in raw
        assert len(raw) == entry["bytes"], entry["path"]
        assert hashlib.sha256(raw).hexdigest() == entry["sha256"], entry["path"]
        assert (
            hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            == entry["git_blob_sha1"]
        )
        bound.append(entry["path"])
    added = git("diff", "--name-only", base, candidate).decode().splitlines()
    checked_json, checked_png = [], []
    for name in added:
        if name.endswith(".json"):
            raw = blob(name)
            json.loads(raw, object_pairs_hook=strict, parse_constant=constant)
            checked_json.append(name)
        if name.endswith(".png"):
            raw = blob(name)
            assert raw[:8] == b"\x89PNG\r\n\x1a\n"
            offset, chunks = 8, []
            while offset < len(raw):
                length = struct.unpack_from(">I", raw, offset)[0]
                kind = raw[offset + 4 : offset + 8]
                data = raw[offset + 8 : offset + 8 + length]
                crc = struct.unpack_from(">I", raw, offset + 8 + length)[0]
                assert zlib.crc32(kind + data) == crc
                if kind == b"IHDR":
                    width, height = struct.unpack_from(">II", data)
                    assert width < 4096 and height < 4096
                chunks.append(kind.decode())
                offset += length + 12
            assert offset == len(raw) and chunks[-1] == "IEND"
            checked_png.append({"path": name, "width": width, "height": height, "chunks": chunks})
    result = {
        "candidate": candidate,
        "base": base,
        "tree": git("rev-parse", candidate + "^{tree}").decode().strip(),
        "manifest_entries_match_git_bytes": bound,
        "strict_json": checked_json,
        "png": checked_png,
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), "utf8")
    print(
        json.dumps(
            {"manifest_entries": len(bound), "json": len(checked_json), "png": len(checked_png)}
        )
    )


if __name__ == "__main__":
    main()
