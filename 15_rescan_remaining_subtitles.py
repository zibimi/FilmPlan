#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


WORKDIR = Path(__file__).resolve().parent
OUT_DIR = WORKDIR / "rescan-plan"
LOG_DIR = WORKDIR / "logs"
ROOTS = [Path(p) for p in os.environ.get("ROOTS", "/Volumes/导演们\n/Volumes/分类").splitlines() if p]
DRY_RUN = os.environ.get("DRY_RUN", "1") != "0"

MOVIE_EXTS = {".mkv", ".mp4", ".avi"}
TEXT_SUB_EXTS = {".srt", ".ass", ".ssa"}
IMAGE_SUB_EXTS = {".idx"}
SIDECAR_EXTS = {".sub"}
SUBTITLE_LIKE_EXTS = TEXT_SUB_EXTS | IMAGE_SUB_EXTS | SIDECAR_EXTS | {".vtt", ".sup", ".smi"}
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
FEATURE_MARKERS = (
    "花絮", "特典", "特辑", "特輯", "幕后", "幕後", "extras", "extra", "bonus",
    "behind", "featurette", "making", "sample", "samples", "trailer", "trailers",
    "预告", "預告",
)


@dataclass
class FolderScan:
    folder: Path
    movies: list[Path]
    direct_subtitles: list[Path]
    sidecars: list[Path]
    unsupported_subtitles: list[Path]
    subdirs: list[Path]
    other_files: list[Path]


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


TS = now_stamp()
LOG_FILE = LOG_DIR / f"remaining-subtitle-audit-{TS}.log"
SUMMARY_MD = OUT_DIR / f"remaining_subtitle_audit_summary_{TS}.md"
ALL_TSV = OUT_DIR / f"remaining_subtitle_folders_{TS}.tsv"
QUEUE_TSV = OUT_DIR / f"remaining_mux_candidates_{TS}.tsv"
MOVE_TSV = OUT_DIR / f"remaining_subtitle_moves_{TS}.tsv"
COMPLEX_TSV = OUT_DIR / f"remaining_complex_cases_{TS}.tsv"


def log(message: str) -> None:
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(line, flush=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def ext(path: Path) -> str:
    return path.suffix.lower()


def is_ignored(path: Path) -> bool:
    return path.name in IGNORED_NAMES or path.name.startswith("._")


def is_movie(path: Path) -> bool:
    if ext(path) not in MOVIE_EXTS:
        return False
    name = path.name
    if name.startswith("OG."):
        return False
    if ".muxing.mkv" in name or ".abandoned." in name or ".failed." in name:
        return False
    return True


def is_feature_subdir(path: Path) -> bool:
    lower = path.name.lower()
    return any(marker in lower for marker in FEATURE_MARKERS)


def is_supported_subtitle(path: Path) -> bool:
    return ext(path) in TEXT_SUB_EXTS or ext(path) in IMAGE_SUB_EXTS


def is_subtitle_like(path: Path) -> bool:
    return ext(path) in SUBTITLE_LIKE_EXTS


def stem_key(path: Path) -> str:
    return path.with_suffix("").name.lower()


def scan_one(folder: Path) -> FolderScan:
    movies: list[Path] = []
    direct_subtitles: list[Path] = []
    sidecars: list[Path] = []
    unsupported_subtitles: list[Path] = []
    subdirs: list[Path] = []
    other_files: list[Path] = []

    try:
        entries = sorted(folder.iterdir(), key=lambda p: p.name.lower())
    except OSError as exc:
        log(f"WARNING: cannot read folder: {folder} ({exc})")
        return FolderScan(folder, [], [], [], [], [], [])

    for item in entries:
        if item.is_dir():
            if item.name == "#recycle":
                continue
            subdirs.append(item)
            continue
        if not item.is_file() or is_ignored(item):
            continue
        if is_movie(item):
            movies.append(item)
        elif is_supported_subtitle(item):
            direct_subtitles.append(item)
        elif ext(item) in SIDECAR_EXTS:
            sidecars.append(item)
        elif is_subtitle_like(item):
            unsupported_subtitles.append(item)
        else:
            other_files.append(item)

    return FolderScan(folder, movies, direct_subtitles, sidecars, unsupported_subtitles, subdirs, other_files)


def valid_root_subtitles(scan: FolderScan) -> tuple[list[Path], list[str]]:
    usable = list(scan.direct_subtitles)
    notes: list[str] = []
    idx_keys = {stem_key(p) for p in scan.direct_subtitles if ext(p) == ".idx"}
    for sidecar in scan.sidecars:
        if stem_key(sidecar) in idx_keys:
            notes.append(f"paired sidecar: {sidecar.name}")
        else:
            notes.append(f"unmatched .sub sidecar: {sidecar.name}")
    return usable, notes


def subtitle_only_subdir(subdir: Path) -> tuple[bool, list[Path], list[Path], list[Path]]:
    direct: list[Path] = []
    sidecars: list[Path] = []
    unsupported: list[Path] = []
    others: list[Path] = []
    try:
        entries = sorted(subdir.iterdir(), key=lambda p: p.name.lower())
    except OSError:
        return False, [], [], [subdir]
    for item in entries:
        if item.is_dir():
            others.append(item)
        elif is_ignored(item):
            continue
        elif is_supported_subtitle(item):
            direct.append(item)
        elif ext(item) in SIDECAR_EXTS:
            sidecars.append(item)
        elif is_subtitle_like(item):
            unsupported.append(item)
        else:
            others.append(item)
    idx_keys = {stem_key(p) for p in direct if ext(p) == ".idx"}
    unmatched_sidecars = [p for p in sidecars if stem_key(p) not in idx_keys]
    ok = bool(direct) and not unsupported and not others and not unmatched_sidecars
    return ok, direct + sidecars, unsupported + unmatched_sidecars, others


def write_row(writer: csv.writer, values: list[object]) -> None:
    writer.writerow(["" if v is None else str(v) for v in values])


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    counters = {
        "folders_scanned": 0,
        "folders_with_subtitle_files": 0,
        "queue_candidates": 0,
        "move_candidates": 0,
        "complex_cases": 0,
    }

    with ALL_TSV.open("w", encoding="utf-8", newline="") as all_fh, \
        QUEUE_TSV.open("w", encoding="utf-8", newline="") as queue_fh, \
        MOVE_TSV.open("w", encoding="utf-8", newline="") as move_fh, \
        COMPLEX_TSV.open("w", encoding="utf-8", newline="") as complex_fh:

        all_w = csv.writer(all_fh, delimiter="\t")
        queue_w = csv.writer(queue_fh, delimiter="\t")
        move_w = csv.writer(move_fh, delimiter="\t")
        complex_w = csv.writer(complex_fh, delimiter="\t")

        all_w.writerow(["folder", "movies", "root_subtitles", "sidecars", "unsupported_subtitles", "subdirs", "other_files"])
        queue_w.writerow(["folder", "movie", "root_subtitle_count", "subdir_move_count", "note"])
        move_w.writerow(["movie_folder", "source", "destination", "status"])
        complex_w.writerow(["folder", "reason", "detail"])

        log(f"DRY_RUN={1 if DRY_RUN else 0}")
        for root in ROOTS:
            if not root.is_dir():
                log(f"WARNING: root not mounted or missing: {root}")
                continue
            log(f"Scanning root: {root}")
            for folder, dirnames, _filenames in os.walk(root):
                if "#recycle" in dirnames:
                    dirnames.remove("#recycle")
                path = Path(folder)
                if is_feature_subdir(path):
                    continue
                scan = scan_one(path)
                counters["folders_scanned"] += 1
                if counters["folders_scanned"] % 500 == 0:
                    log(f"Scanned folders: {counters['folders_scanned']}")

                has_subtitle_files = bool(scan.direct_subtitles or scan.sidecars or scan.unsupported_subtitles)
                if has_subtitle_files:
                    counters["folders_with_subtitle_files"] += 1
                    write_row(all_w, [
                        path,
                        len(scan.movies),
                        ";".join(p.name for p in scan.direct_subtitles),
                        ";".join(p.name for p in scan.sidecars),
                        ";".join(p.name for p in scan.unsupported_subtitles),
                        len(scan.subdirs),
                        len(scan.other_files),
                    ])

                move_sources: list[Path] = []
                complex_subdirs: list[str] = []
                if len(scan.movies) == 1 and scan.subdirs:
                    for subdir in scan.subdirs:
                        if is_feature_subdir(subdir):
                            continue
                        ok, movable, bad_subs, other = subtitle_only_subdir(subdir)
                        if ok:
                            for src in movable:
                                dst = path / src.name
                                status = "DRY_RUN_WOULD_MOVE" if DRY_RUN else "MOVE_NOT_EXECUTED_BY_AUDIT"
                                write_row(move_w, [path, src, dst, status])
                                move_sources.append(src)
                            counters["move_candidates"] += 1
                        elif bad_subs or other:
                            complex_subdirs.append(
                                f"{subdir.name}: bad_subtitles={len(bad_subs)} other={len(other)}"
                            )

                usable_subs, notes = valid_root_subtitles(scan)
                if len(scan.movies) == 1 and (usable_subs or move_sources):
                    if scan.unsupported_subtitles:
                        counters["complex_cases"] += 1
                        write_row(complex_w, [
                            path,
                            "single movie with unsupported subtitle-like files",
                            ";".join(p.name for p in scan.unsupported_subtitles),
                        ])
                    elif any(note.startswith("unmatched") for note in notes):
                        counters["complex_cases"] += 1
                        write_row(complex_w, [path, "single movie with unmatched .sub sidecar", ";".join(notes)])
                    else:
                        counters["queue_candidates"] += 1
                        write_row(queue_w, [
                            path,
                            scan.movies[0],
                            len(usable_subs),
                            len(move_sources),
                            "; ".join(notes),
                        ])
                elif has_subtitle_files:
                    reason = "not a single movie folder"
                    detail = f"movies={len(scan.movies)} root_subtitles={len(scan.direct_subtitles)} sidecars={len(scan.sidecars)} unsupported={len(scan.unsupported_subtitles)} subdirs={len(scan.subdirs)} other_files={len(scan.other_files)}"
                    counters["complex_cases"] += 1
                    write_row(complex_w, [path, reason, detail])

                for detail in complex_subdirs:
                    counters["complex_cases"] += 1
                    write_row(complex_w, [path, "subdir is not subtitle-only or has unmatched sidecars", detail])

    with SUMMARY_MD.open("w", encoding="utf-8") as fh:
        fh.write("# Remaining Subtitle Audit\n\n")
        fh.write(f"- Generated: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n")
        fh.write(f"- DRY_RUN: `{1 if DRY_RUN else 0}`\n")
        fh.write("- Roots:\n")
        for root in ROOTS:
            fh.write(f"  - `{root}`\n")
        fh.write("\n## Counts\n\n")
        for key, value in counters.items():
            fh.write(f"- {key}: `{value}`\n")
        fh.write("\n## Files\n\n")
        fh.write(f"- All subtitle folders: `{ALL_TSV}`\n")
        fh.write(f"- Queue candidates: `{QUEUE_TSV}`\n")
        fh.write(f"- Subtitle move candidates: `{MOVE_TSV}`\n")
        fh.write(f"- Complex cases: `{COMPLEX_TSV}`\n")
        fh.write(f"- Log: `{LOG_FILE}`\n")

    log(f"Done. Summary: {SUMMARY_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
