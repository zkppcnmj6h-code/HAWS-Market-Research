#!/usr/bin/env python3
"""
reorg_haws_v2.py — Reorganize the HAWS / Visual Systems Designer folders into a clean, versioned structure.

Key improvements vs v1:
- FIX: argparse attributes now use underscores (e.g., args.ignore_locks) to avoid AttributeError
- New: Media routing for images (png, jpg, jpeg, webp, svg, gif, tif, tiff) and design sources (psd, ai, eps)
- New: --fail-fast option stops on first error (default: continue with warnings)
- New: Better validation and user-friendly error messages
- New: Optional --flatten to discard original subfolder context instead of --keep-tree
- New: --report prints a compact summary at the end

USAGE (dry run by default):
  python3 reorg_haws_v2.py --src "/path/to/source" --dst "/path/to/organized" --by-domain --by-type --keep-tree --ignore-locks --verbose

Apply changes (perform moves/copies):
  python3 reorg_haws_v2.py --src "/path/to/source" --dst "/path/to/organized" --by-domain --by-type --keep-tree --ignore-locks --apply --undo-script --verbose

Options:
  --apply            Actually move/copy files (default is dry-run preview)
  --by-type          Organize by file type buckets under /library (pdf, md, xlsx, etc.)
  --by-domain        Organize by domain buckets under /domains (docs, templates, schemas, config, samples, trackers, media)
  --keep-tree        Preserve original subfolders under each bucket (exclusive with --flatten)
  --flatten          Do NOT preserve original subfolders (exclusive with --keep-tree)
  --lowercase        Lowercase filenames when moving/copying
  --manifest         Output manifest CSV (default: manifest.csv in --dst)
  --undo-script      Emit a shell undo script to restore moves (and delete type copies)
  --ignore-locks     Ignore temp/lock files (e.g., ~$*.xlsx)
  --fail-fast        Abort on first error (default: continue and log as warning)
  --report           Print a compact end-of-run summary (moved/copied/skipped/duplicates)
  --verbose          Print each planned action
"""

import argparse
import csv
import hashlib
import os
import shutil
import sys
from pathlib import Path
from typing import Dict

DOMAIN_MAP = {
    "docs": ("docs", ".pdf", ".docx", ".pptx", ".txt", ".rtf"),
    "templates": ("templates", ".md"),
    "schemas": ("schemas", ".json"),
    "config": ("config", ".yml", ".yaml"),
    "samples": ("samples", ".jsonl"),
    "trackers": ("trackers", ".csv"),
    "media": ("media", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".tif", ".tiff", ".psd", ".ai", ".eps"),
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
    ".png": "png",
    ".jpg": "jpg",
    ".jpeg": "jpeg",
    ".webp": "webp",
    ".svg": "svg",
    ".gif": "gif",
    ".tif": "tif",
    ".tiff": "tiff",
    ".psd": "psd",
    ".ai": "ai",
    ".eps": "eps",
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
        if seg in ("media", "images", "img", "assets"):
            return "media"

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
    ap.add_argument("--by-type", action="store_true", dest="by_type", help="Build a filetype library under organized/library")
    ap.add_argument("--by-domain", action="store_true", dest="by_domain", help="Build a domain library under organized/domains")
    ap.add_argument("--keep-tree", action="store_true", dest="keep_tree", help="Preserve partial original subfolders under each bucket")
    ap.add_argument("--flatten", action="store_true", help="Discard original subfolders under each bucket")
    ap.add_argument("--lowercase", action="store_true", help="Lowercase filenames on write")
    ap.add_argument("--manifest", default="manifest.csv", help="Manifest CSV filename (in --dst)")
    ap.add_argument("--undo-script", action="store_true", dest="undo_script", help="Also write an undo.sh in --dst")
    ap.add_argument("--ignore-locks", action="store_true", dest="ignore_locks", help="Ignore temp/lock files (e.g., ~$*.xlsx)")
    ap.add_argument("--fail-fast", action="store_true", dest="fail_fast", help="Abort on first error (default: continue)")
    ap.add_argument("--report", action="store_true", help="Print a compact summary at the end")
    ap.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = ap.parse_args()

    # sanity checks
    if args.keep_tree and args.flatten:
        print("[error] --keep-tree and --flatten are mutually exclusive", file=sys.stderr)
        sys.exit(2)

    if not args.by_type and not args.by_domain:
        # default to domain view
        args.by_domain = True

    src = args.src.expanduser().resolve()
    dst = args.dst.expanduser().resolve()

    if not src.exists() or not src.is_dir():
        print(f"[error] --src does not exist or is not a directory: {src}", file=sys.stderr)
        sys.exit(2)

    try:
        dst.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[error] cannot create --dst: {dst}\n{e}", file=sys.stderr)
        sys.exit(2)

    manifest_path = dst / args.manifest
    undo_path = dst / "undo.sh" if args.undo_script else None

    # content hash registry to skip duplicates
    seen_hashes: Dict[str, Path] = {}
    entries = []  # rows for manifest
    undo_lines = []

    stats = {"moved": 0, "copied": 0, "skipped": 0, "duplicates": 0, "errors": 0}

    try:
        for root, dirs, files in os.walk(src):
            # skip junk dirs
            dirs[:] = [d for d in dirs if d not in IGNORED_NAMES]
            for fname in files:
                if fname in IGNORED_NAMES:
                    stats["skipped"] += 1
                    continue
                if args.ignore_locks and fname.startswith(LOCK_PREFIXES):
                    stats["skipped"] += 1
                    continue

                spath = Path(root) / fname
                if not spath.is_file():
                    stats["skipped"] += 1
                    continue

                try:
                    rel = spath.relative_to(src)
                except Exception:
                    rel = Path(fname)

                ext = spath.suffix.lower()
                domain = guess_domain(ext, rel)

                # compute content hash for dedupe check
                try:
                    file_hash = sha256sum(spath)
                except Exception as e:
                    stats["errors"] += 1
                    msg = f"[warn] unreadable: {rel} ({e})"
                    if args.fail_fast:
                        print(msg, file=sys.stderr)
                        sys.exit(1)
                    if args.verbose:
                        print(msg, file=sys.stderr)
                    entries.append({
                        "source": str(rel),
                        "action": "error-unreadable",
                        "domain_dst": "",
                        "type_dst": "",
                        "hash": "",
                    })
                    continue

                # decide base names
                base_name = normalize_name(spath.name, args.lowercase)

                # DOMAIN TARGET (primary move target when --by-domain)
                domain_target = None
                if args.by_domain:
                    domain_root = dst / "domains" / domain
                    if args.keep_tree:
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
                        stats["duplicates"] += 1
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
                        while final_domain_target.exists():
                            # if same hash, it's a duplicate in the target; skip creating another copy
                            try:
                                if sha256sum(final_domain_target) == file_hash:
                                    break
                            except Exception:
                                pass
                            stem = final_domain_target.stem
                            final_domain_target = final_domain_target.with_name(f"{stem}__{i}{final_domain_target.suffix}")
                            i += 1

                        if args.verbose:
                            print(f"[{'MOVE' if args.apply else 'DRY'}] {rel} -> domains/{domain}/{final_domain_target.name}")
                        safe_copy_or_move(spath, final_domain_target, args.apply, move=True)
                        moved = True
                        stats["moved"] += 1 if args.apply else 0
                        if args.undo_script:
                            undo_lines.append(build_undo_line(spath, final_domain_target, moved=True))
                        domain_target = final_domain_target

                # TYPE COPY (optional)
                type_written = ""
                if type_target is not None:
                    final_type_target = type_target
                    i = 1
                    while final_type_target.exists():
                        try:
                            if sha256sum(final_type_target) == file_hash:
                                break
                        except Exception:
                            pass
                        stem = final_type_target.stem
                        final_type_target = final_type_target.with_name(f"{stem}__{i}{final_type_target.suffix}")
                        i += 1

                    if args.verbose:
                        print(f"[{'COPY' if args.apply else 'DRY'}] {rel} -> library/{TYPE_BUCKETS.get(ext, 'other')}/{final_type_target.name}")
                    safe_copy_or_move(spath, final_type_target, args.apply, move=False)
                    type_written = str(final_type_target.relative_to(dst))
                    stats["copied"] += 1 if args.apply else 0
                    if args.undo_script:
                        undo_lines.append(build_undo_line(spath, final_type_target, moved=False))

                entries.append({
                    "source": str(rel),
                    "action": "moved" if moved else "skipped",
                    "domain_dst": "" if domain_target is None else str(domain_target.relative_to(dst)),
                    "type_dst": type_written,
                    "hash": file_hash,
                })
    finally:
        # write manifest even if errors
        try:
            with open(manifest_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["source", "action", "domain_dst", "type_dst", "hash"])
                writer.writeheader()
                writer.writerows(entries)
        except Exception as e:
            print(f"[error] failed to write manifest: {manifest_path} ({e})", file=sys.stderr)

        if undo_path is not None:
            try:
                with open(undo_path, "w", encoding="utf-8") as f:
                    f.write("#!/usr/bin/env bash\nset -euo pipefail\n\n")
                    for line in undo_lines:
                        f.write(line + "\n")
                os.chmod(undo_path, 0o755)
            except Exception as e:
                print(f"[error] failed to write undo script: {undo_path} ({e})", file=sys.stderr)

        if args.report:
            print("\n=== Reorg Summary ===")
            print(f"  moved:      {stats['moved']}")
            print(f"  copied:     {stats['copied']}")
            print(f"  duplicates: {stats['duplicates']}")
            print(f"  skipped:    {stats['skipped']}")
            print(f"  errors:     {stats['errors']}")
            print(f"  manifest:   {manifest_path}")
            if undo_path is not None:
                print(f"  undo:       {undo_path}")

if __name__ == "__main__":
    main()
