#!/usr/bin/env python3
"""
reorg_haws.py — Reorganize the HAWS / Visual Systems Designer folders into a clean, versioned structure.

USAGE (dry run by default):
  python reorg_haws.py --src /path/to/source --dst /path/to/organized

Options:
  --apply           Actually move files (default is dry-run)
  --by-type         Organize by file type buckets under /library (pdf, md, xlsx, etc.)
  --by-domain       Organize by domain buckets under /domains (docs, templates, schemas, config, samples, trackers)
  --keep-tree       Preserve subfolder context under each bucket
  --lowercase       Lowercase filenames when moving
  --manifest        Output manifest CSV (default: manifest.csv in --dst)
  --undo-script     Emit a shell undo script to restore moves
  --ignore-locks    Ignore temp/lock files (e.g., ~$*.xlsx)
  --verbose         Print each planned move

Design:
- You can combine --by-type and --by-domain to produce two parallel views:
    organized/library/...            (filetype view)
    organized/domains/...            (domain/role view)
- When both are selected, a single pass computes move targets for each view, and files are placed in both trees (copy) unless --link is used.
  To keep it simple and reliable across platforms, this tool moves to the *domain* tree by default and *copies* to the *type* tree when both are requested.
- Deduplication is content-hash based; duplicates are skipped with a pointer in the manifest.
"""

import argparse
import csv
import hashlib
import os
import shutil
from pathlib import Path
from typing import Dict, Tuple

DOMAIN_MAP = {
    "docs": ("docs", ".pdf", ".docx", ".pptx", ".txt", ".rtf"),
    "templates": ("templates", ".md"),
    "schemas": ("schemas", ".json"),
    "config": ("config", ".yml", ".yaml"),
    "samples": ("samples", ".jsonl"),
    "trackers": ("trackers", ".csv"),
    # default / unknowns fall back to docs
}

TYPE_BUCKETS = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".xlsx": "xlsx",
    ".csv": "csv",
    ".jsonl": "jsonl",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "md",
    ".zip": "zip",
    ".rtf": "rtf",
    ".txt": "txt",
}

LOCK_PREFIXES = ("~$",)
IGNORED_NAMES = {"__MACOSX", ".DS_Store"}

def sha256sum(path: Path, block_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(block_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def guess_domain(ext: str, rel: Path) -> str:
    ext = ext.lower()
    # strong hints from path segments
    for segment in rel.parts:
        seg = segment.lower()
        if "template" in seg or seg.endswith("templates"):
            return "templates"
        if "schema" in seg or seg.endswith("schemas"):
            return "schemas"
        if seg in ("config", "configs"):
            return "config"
        if "sample" in seg or seg.endswith("samples"):
            return "samples"
        if "tracker" in seg or "trackers" in seg:
            return "trackers"
        if seg in ("docs", "doc", "documents"):
            return "docs"

    # fallback to extension-based
    for domain, (_folder, *exts) in DOMAIN_MAP.items():
        if ext in exts:
            return domain
    return "docs"

def normalize_name(name: str, lowercase: bool) -> str:
    return name.lower() if lowercase else name

def safe_copy_or_move(src: Path, dst: Path, apply: bool, move: bool) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not apply:
        return
    if move:
        shutil.move(str(src), str(dst))
    else:
        shutil.copy2(str(src), str(dst))

def build_undo_line(src: Path, dst: Path, moved: bool) -> str:
    if moved:
        # reverse the move
        return f'mkdir -p "{src.parent}" && mv "{dst}" "{src}"'
    else:
        # reverse the copy (delete the destination)
        return f'rm -f "{dst}"'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, type=Path, help="Source root")
    ap.add_argument("--dst", required=True, type=Path, help="Destination root (will be created)")
    ap.add_argument("--apply", action="store_true", help="Perform changes (default: dry-run)")
    ap.add_argument("--by-type", action="store_true", help="Build a filetype library under organized/library")
    ap.add_argument("--by-domain", action="store_true", help="Build a domain library under organized/domains")
    ap.add_argument("--keep-tree", action="store_true", help="Preserve partial original subfolders under each bucket")
    ap.add_argument("--lowercase", action="store_true", help="Lowercase filenames on write")
    ap.add_argument("--manifest", default="manifest.csv", help="Manifest CSV filename (in --dst)")
    ap.add_argument("--undo-script", action="store_true", help="Also write an undo.sh in --dst")
    ap.add_argument("--ignore-locks", action="store_true", help="Ignore temp/lock files (e.g., ~$*.xlsx)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not args.by_type and not args.by_domain:
        # default to domain view
        args.by_domain = True

    src = args.src.resolve()
    dst = args.dst.resolve()
    dst.mkdir(parents=True, exist_ok=True)

    manifest_path = dst / args.manifest
    undo_path = dst / "undo.sh" if args.undo_script else None

    # content hash registry to skip duplicates
    seen_hashes: Dict[str, Path] = {}
    entries = []  # rows for manifest
    undo_lines = []

    for root, dirs, files in os.walk(src):
        # skip junk dirs
        dirs[:] = [d for d in dirs if d not in IGNORED_NAMES]
        for fname in files:
            if fname in IGNORED_NAMES:
                continue
            if args.ignore-locks and fname.startswith(LOCK_PREFIXES):
                continue

            spath = Path(root) / fname
            if not spath.is_file():
                continue

            rel = spath.relative_to(src)
            ext = spath.suffix.lower()
            domain = guess_domain(ext, rel)

            # compute content hash for dedupe check
            try:
                file_hash = sha256sum(spath)
            except Exception:
                # if unreadable, skip gracefully
                if args.verbose:
                    print(f"[skip] unreadable: {rel}")
                continue

            # decide base names
            base_name = normalize_name(spath.name, args.lowercase)

            # DOMAIN TARGET (primary move target when --by-domain)
            domain_target = None
            if args.by_domain:
                domain_root = dst / "domains" / domain
                if args.keep_tree:
                    # preserve up to one level of original folder context
                    preserved = Path(*rel.parts[:-1]) if len(rel.parts) > 1 else Path()
                    domain_target = domain_root / preserved / base_name
                else:
                    domain_target = domain_root / base_name

            # TYPE TARGET (secondary copy target when both views requested)
            type_target = None
            if args.by_type:
                type_bucket = TYPE_BUCKETS.get(ext, "other")
                type_root = dst / "library" / type_bucket
                if args.keep_tree:
                    preserved = Path(*rel.parts[:-1]) if len(rel.parts) > 1 else Path()
                    type_target = type_root / preserved / base_name
                else:
                    type_target = type_root / base_name

            # dedupe by content hash (only for the primary domain move)
            moved = False
            if domain_target is not None:
                if file_hash in seen_hashes:
                    # skip moving duplicate content into domain tree; track as duplicate
                    entries.append({
                        "source": str(rel),
                        "action": "duplicate-skip",
                        "domain_dst": "",
                        "type_dst": "",
                        "hash": file_hash,
                    })
                    if args.verbose:
                        print(f"[dup] {rel} matches {seen_hashes[file_hash].relative_to(src)}; skipping domain move")
                else:
                    seen_hashes[file_hash] = spath
                    # ensure unique filename if conflict at destination
                    final_domain_target = domain_target
                    i = 1
                    while final_domain_target.exists() and sha256sum(final_domain_target) != file_hash:
                        stem = final_domain_target.stem
                        final_domain_target = final_domain_target.with_name(f"{stem}__{i}{final_domain_target.suffix}")
                        i += 1

                    if args.verbose:
                        print(f"[{'MOVE' if args.apply else 'DRY'}] {rel} -> domains/{domain}/{final_domain_target.name}")
                    safe_copy_or_move(spath, final_domain_target, args.apply, move=True)
                    moved = True
                    if args.undo_script:
                        undo_lines.append(build_undo_line(spath, final_domain_target, moved=True))
                    domain_target = final_domain_target

            # TYPE COPY (optional)
            type_written = ""
            if type_target is not None:
                # copy to type view, dedupe by hash + name
                final_type_target = type_target
                i = 1
                while final_type_target.exists() and sha256sum(final_type_target) != file_hash:
                    stem = final_type_target.stem
                    final_type_target = final_type_target.with_name(f"{stem}__{i}{final_type_target.suffix}")
                    i += 1

                if args.verbose:
                    print(f"[{'COPY' if args.apply else 'DRY'}] {rel} -> library/{TYPE_BUCKETS.get(ext, 'other')}/{final_type_target.name}")
                safe_copy_or_move(spath, final_type_target, args.apply, move=False)
                type_written = str(final_type_target.relative_to(dst))
                if args.undo_script:
                    undo_lines.append(build_undo_line(spath, final_type_target, moved=False))

            entries.append({
                "source": str(rel),
                "action": "moved" if moved else "skipped",
                "domain_dst": "" if domain_target is None else str(domain_target.relative_to(dst)),
                "type_dst": type_written,
                "hash": file_hash,
            })

    # write manifest
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "action", "domain_dst", "type_dst", "hash"])
        writer.writeheader()
        writer.writerows(entries)

    if undo_path is not None:
        with open(undo_path, "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env bash\nset -euo pipefail\n\n")
            for line in undo_lines:
                f.write(line + "\n")
        os.chmod(undo_path, 0o755)

    print(f"Done. Manifest: {manifest_path}")
    if undo_path is not None:
        print(f"Undo script: {undo_path}")

if __name__ == "__main__":
    main()
