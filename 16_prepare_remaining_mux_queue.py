#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


WORKDIR = Path(__file__).resolve().parent
RESCAN_DIR = WORKDIR / "rescan-plan"
LOG_DIR = WORKDIR / "logs"
QUEUE_FILE = Path(os.environ.get("QUEUE_FILE", str(WORKDIR / "remaining_mux_clean_queue.tsv")))
DRY_RUN = os.environ.get("DRY_RUN", "1") != "0"
RESCAN_TSV = os.environ.get("RESCAN_TSV", "")
MOVES_TSV = os.environ.get("MOVES_TSV", "")


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


RUN_LOG = LOG_DIR / f"prepare-remaining-mux-queue-{stamp()}.log"


def log(message: str) -> None:
    line = f"[{timestamp()}] {message}"
    print(line, flush=True)
    with RUN_LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def latest(pattern: str) -> Path:
    matches = sorted(RESCAN_DIR.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"no file matched {pattern} in {RESCAN_DIR}")
    return matches[-1]


def target_for_movie(movie: Path) -> Path:
    return movie.parent.parent / f"{movie.stem}.mkv"


def apply_moves(moves_tsv: Path) -> tuple[int, int]:
    moved = 0
    skipped = 0
    with moves_tsv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            src = Path(row["source"])
            dst = Path(row["destination"])
            if not src.exists():
                skipped += 1
                log(f"SKIP move missing source: {src}")
                continue
            if dst.exists():
                skipped += 1
                log(f"SKIP move destination exists: {dst}")
                continue
            if DRY_RUN:
                moved += 1
                log(f"DRY_RUN would move subtitle: {src} -> {dst}")
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            moved += 1
            log(f"Moved subtitle: {src} -> {dst}")
    return moved, skipped


def prepare_queue(rescan_tsv: Path) -> tuple[int, int]:
    if QUEUE_FILE.exists():
        backup = QUEUE_FILE.with_name(f"{QUEUE_FILE.name}.before-prepare-{stamp()}.tsv")
        shutil.copy2(QUEUE_FILE, backup)
        log(f"Backed up existing queue: {backup}")

    added = 0
    skipped = 0
    with rescan_tsv.open("r", encoding="utf-8", newline="") as in_fh, \
        QUEUE_FILE.open("w", encoding="utf-8", newline="") as out_fh:
        reader = csv.DictReader(in_fh, delimiter="\t")
        out_fh.write("# status\tfolder\tmessage\n")
        for row in reader:
            folder = Path(row["folder"])
            movie = Path(row["movie"])
            target = target_for_movie(movie)
            if not folder.is_dir():
                skipped += 1
                log(f"SKIP missing folder: {folder}")
                continue
            if not movie.is_file():
                skipped += 1
                log(f"SKIP missing movie: {movie}")
                continue
            if target.exists():
                skipped += 1
                log(f"SKIP parent target exists: {target}")
                continue
            if any(folder.glob("OG.*")):
                skipped += 1
                log(f"SKIP folder already has OG file: {folder}")
                continue
            msg = f"prepared from {rescan_tsv.name}; root_subtitles={row['root_subtitle_count']}; moved_subtitle_files={row['subdir_move_count']}"
            out_fh.write(f"PENDING\t{folder}\t{msg}\n")
            added += 1
    return added, skipped


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    rescan = Path(RESCAN_TSV) if RESCAN_TSV else latest("remaining_mux_candidates_*.tsv")
    moves = Path(MOVES_TSV) if MOVES_TSV else latest("remaining_subtitle_moves_*.tsv")
    if not rescan.is_file():
        log(f"ERROR: missing candidate TSV: {rescan}")
        return 1
    if not moves.is_file():
        log(f"ERROR: missing moves TSV: {moves}")
        return 1

    log(f"DRY_RUN={1 if DRY_RUN else 0}")
    log(f"Candidates: {rescan}")
    log(f"Moves: {moves}")
    log(f"Queue: {QUEUE_FILE}")

    moved, move_skipped = apply_moves(moves)
    added, queue_skipped = prepare_queue(rescan)

    log(f"Move rows handled: {moved}")
    log(f"Move rows skipped: {move_skipped}")
    log(f"Queue rows added: {added}")
    log(f"Queue rows skipped: {queue_skipped}")
    log(f"Log: {RUN_LOG}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
