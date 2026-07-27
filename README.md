# FilmPlan

FilmPlan is a small command-line workflow for standardizing a movie library on a
Mac with movies stored on a NAS. It scans movie folders, finds external
subtitles, muxes them into MKV files as soft subtitles, verifies the result, and
only then cleans up the old loose files.

The project was built for this library layout:

- `/Volumes/导演们`
- `/Volumes/分类`

The scripts are plain Bash/Python and are designed to run locally on macOS. No
GUI workflow is required.

## What It Does

- Finds single-movie folders with external subtitles.
- Moves subtitle-only subfolder contents next to the movie file.
- Muxes subtitles into MKV with `mkvmerge`.
- Remuxes MP4/AVI/MKV without re-encoding video or audio.
- Detects text subtitle encoding before muxing.
- Converts text subtitles to UTF-8 for safer muxing.
- Verifies newly added text subtitle tracks by extracting them from the output.
- Handles VobSub subtitles as `.idx` plus matching `.sub`.
- Logs every run locally.
- Keeps risky cases out of the automatic cleanup path.

## Safety Model

FilmPlan is intentionally conservative.

- It does not hardcode subtitle burn-in.
- It does not re-encode video.
- It does not delete source files until the new MKV passes verification.
- It does not auto-process unmatched `.sub`, `.sup`, `.vtt`, or `.smi` files.
- It marks risky media warnings as `DONE_REVIEW` and keeps source files.
- It keeps generated logs and local tools out of Git.

Text subtitles are checked twice:

1. Before muxing, the script guesses the safest encoding and normalizes to UTF-8.
2. After muxing, the script extracts newly added text tracks and checks for
   replacement characters and obvious mojibake.

VobSub subtitles are image subtitles, so the script can verify track presence but
cannot OCR-check the rendered text.

## Requirements

### System

- macOS
- Python 3
- Bash
- NAS mounted under `/Volumes`
- Enough free NAS space for temporary remux output

### Media Tools

Required:

- `mkvmerge`
- `mkvextract`

Recommended:

- `mediainfo`
- `ffmpeg`

The runner looks for MKVToolNix in these places:

- `MKVMERGE` / `MKVEXTRACT` environment variables
- tools available in `PATH`
- `tools/MKVToolNix.app/Contents/MacOS`
- `/Users/milou/Documents/电影整理计划/tools/MKVToolNix.app/Contents/MacOS`

## Repository Layout

```text
.
├── 14_run_mux_clean_queue.sh          # Legacy TSV queue runner
├── 15_rescan_remaining_subtitles.py   # Legacy broad subtitle scanner
├── 16_prepare_remaining_mux_queue.py  # Legacy TSV queue builder
├── 17_run_manual_approved_mux.py      # Current JSON queue mux/verify runner
├── 17_scan_bdmv_playlists.py          # BDMV playlist scanner
├── 18_refresh_scan_subtitle_work.py   # Current category scanner/report generator
├── FINAL_REPORT_20260722.md           # Current cleanup status summary
├── README.md
├── RUNBOOK_MUX_CLEAN.md
├── docs/                              # Durable project notes
└── scripts/                           # Supporting utilities
```

Local-only generated paths are ignored by Git:

- `logs/`
- `tools/`
- `downloads/`
- `archive/`
- `rescan-plan/`
- `bdmv-plan/`
- queue files such as `manual_approved_mux_queue.json` and `remaining_mux_clean_queue.tsv`
- temporary MKV/media output

## Which Script Should I Use?

Use this table first. Most mistakes in this project come from running an old
scanner for a new task, or running a destructive step before reviewing the
generated queue.

| Situation | Use | What it does | Writes to NAS? |
|---|---|---|---|
| Scan one category for subtitle work | `python3 18_refresh_scan_subtitle_work.py --root <path> --prefix <name> --include-single` | Finds mux tasks, cleanup-only actions, and review items; writes JSON queues and Markdown reports under `rescan-plan/` | No |
| Scan and immediately run safe subtitle tasks for one category | `python3 18_refresh_scan_subtitle_work.py --root <path> --prefix <name> --include-single --apply` | Runs the scan, then calls `17_run_manual_approved_mux.py` and applies cleanup actions | Yes |
| Run an already approved JSON mux queue | `MUX_QUEUE=<queue.json> python3 17_run_manual_approved_mux.py` | Muxes subtitles, verifies output, updates queue status | Yes |
| Inspect a Blu-ray/BDMV disc folder | `python3 17_scan_bdmv_playlists.py <disc-folder>` | Classifies playlists as feature/extras/duplicates/review and writes a remux plan | No |
| Merge split feature files such as `Part1/Part2`, `Disc1/Disc2`, `01/02` | `python3 scripts/merge_part_like_features.py --write-manifest <manifest.json>` first, then `--manifest <manifest.json> --execute` | Finds and merges split movie files after track/duration verification | Manifest: No; execute: Yes |
| Remount NAS volumes after SMB disappears | `./scripts/remount_movie_volumes.sh` | Opens the previously observed SMB shares in Finder/macOS | No media changes |
| Use old TSV subtitle queue workflow | `15_rescan_remaining_subtitles.py`, `16_prepare_remaining_mux_queue.py`, `14_run_mux_clean_queue.sh` | Legacy broad scanner/queue/runner kept for old queues | Depends on `DRY_RUN` |

Recommended default today:

```bash
python3 18_refresh_scan_subtitle_work.py \
  --root /Volumes/分类/某个分类 \
  --prefix some_category \
  --include-single
```

Review the generated files under `rescan-plan/`. Only add `--apply` after the
queue and review items look right.

## Current Subtitle Workflow

For normal subtitle muxing, prefer the newer JSON workflow:

### 1. Scan One Category Without Changing NAS Files

```bash
python3 18_refresh_scan_subtitle_work.py \
  --root /Volumes/分类/科幻·奇幻 \
  --prefix scifi \
  --include-single
```

This creates local-only files under `rescan-plan/`:

- `<prefix>_mux_queue.json`
- `<prefix>_cleanup_actions.json`
- `<prefix>_report.md`

### 2. Review The Report

Open:

```text
rescan-plan/<prefix>_report.md
```

Check:

- `Mux Tasks`: items the script thinks are safe to process
- `Cleanup Actions`: cleanup-only moves/deletes after safety checks
- `Review Items`: ambiguous cases that should not be automated yet

### 3. Run The Category If It Looks Right

```bash
python3 18_refresh_scan_subtitle_work.py \
  --root /Volumes/分类/科幻·奇幻 \
  --prefix scifi \
  --include-single \
  --apply
```

`--apply` runs the generated mux queue and applies cleanup actions. It still
verifies outputs before deleting source movie/subtitle files.

### 4. Run A Manually Approved Queue

Use this when you manually create or edit a queue JSON, especially for nested
subtitle folders or CD1/CD2 cases:

```bash
MUX_QUEUE=/Users/milou/Movies/FilmSubTitlePlan/rescan-plan/manual_case_queue.json \
MUX_RUN_LOG=/Users/milou/Movies/FilmSubTitlePlan/logs/manual-case.log \
python3 17_run_manual_approved_mux.py
```

The runner updates each task status in the queue:

- `PENDING`: ready to process
- `DONE`: output verified and cleanup completed
- `DONE_REVIEW`: output created, but source files or leftovers were kept for manual review
- `FAILED`: failed safely; source files were kept

## Quick Start

Clone the repository:

```bash
git clone https://github.com/zibimi/FilmPlan.git
cd FilmPlan
```

Or enter the existing local project directory:

```bash
cd /Users/milou/Movies/FilmSubTitlePlan
```

Make sure your NAS roots are mounted:

```bash
ls /Volumes/导演们 /Volumes/分类
```

Check that MKVToolNix is available:

```bash
/Users/milou/Documents/电影整理计划/tools/MKVToolNix.app/Contents/MacOS/mkvmerge --version
```

Then run a no-write category scan:

```bash
python3 18_refresh_scan_subtitle_work.py \
  --root /Volumes/分类/科幻·奇幻 \
  --prefix smoke_test \
  --include-single
```

The scan should not modify NAS media files. It should only write local report and
queue files under `rescan-plan/`.

If MKVToolNix is not in `PATH`, either place `MKVToolNix.app` under:

```text
tools/MKVToolNix.app
```

or pass explicit tool paths:

```bash
MKVMERGE=/path/to/mkvmerge \
MKVEXTRACT=/path/to/mkvextract \
python3 17_run_manual_approved_mux.py
```

## Current Configuration

For `18_refresh_scan_subtitle_work.py`:

```bash
python3 18_refresh_scan_subtitle_work.py \
  --root /Volumes/分类/科幻·奇幻 \
  --prefix scifi \
  --include-single
```

- `--root`: category or root to scan. Can be repeated.
- `--prefix`: filename prefix for generated queue/report files.
- `--include-single`: include single-movie folders with external subtitles.
- `--apply`: execute generated queue and cleanup actions after scanning.

For `17_run_manual_approved_mux.py`:

```bash
MUX_QUEUE=/path/to/queue.json \
MUX_RUN_LOG=/path/to/run.log \
python3 17_run_manual_approved_mux.py
```

- `MUX_QUEUE`: JSON queue to execute.
- `MUX_RUN_LOG`: log path.
- `MKVMERGE`: optional override for `mkvmerge`.
- `MKVEXTRACT`: optional override for `mkvextract`.

The old TSV workflow uses `ROOTS`, `DRY_RUN`, and `QUEUE_FILE`; see the legacy
section below.

## Split-File Movie Merge

For movies split into `CD1/CD2`, `Part1/Part2`, `Disc1/Disc2`, `01/02`, or
multi-part variants, use the conservative merge scripts under `scripts/`.

The part-like merge runner is:

```bash
python3 scripts/merge_part_like_features.py
```

It scans `/Volumes/分类` and `/Volumes/导演们`, skips `#recycle`, verifies track
compatibility and final duration, and only deletes original part files after the
merged MKV can be read successfully.

If the NAS volumes disappear, `scripts/remount_movie_volumes.sh` can ask macOS
to reopen the SMB shares that were observed during the 2026-07-27 run.

Latest run note:

- `docs/PART_LIKE_MERGE_2026-07-27.md`

## Legacy TSV Subtitle Workflow

The older 14/15/16 workflow is still kept because some old local queue files
were generated with it. For new work, use `18_refresh_scan_subtitle_work.py`
and `17_run_manual_approved_mux.py` instead.

### 1. Scan Without Changing NAS Files

```bash
DRY_RUN=1 ./15_rescan_remaining_subtitles.py
```

This creates audit files under `rescan-plan/`, including:

- `remaining_subtitle_audit_summary_*.md`
- `remaining_mux_candidates_*.tsv`
- `remaining_complex_cases_*.tsv`
- `remaining_subtitle_moves_*.tsv`

### 2. Preview Queue Preparation

```bash
DRY_RUN=1 ./16_prepare_remaining_mux_queue.py
```

This shows which subtitle-only subfolder files would be moved and builds a fresh
queue preview.

### 3. Move Subtitle-Only Subfolder Files

```bash
DRY_RUN=0 ./16_prepare_remaining_mux_queue.py
```

This only moves files from subtitle-only subfolders into the corresponding movie
folder. It also rebuilds:

```text
remaining_mux_clean_queue.tsv
```

### 4. Dry-Run the First Queue Item

```bash
QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv \
RUN_LIMIT=1 \
./14_run_mux_clean_queue.sh
```

This does not modify media files. It confirms that the next folder can be parsed
and shows the exact `mkvmerge` command shape.

### 5. Run a Small Real Batch

```bash
DRY_RUN=0 \
QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv \
RUN_LIMIT=5 \
PROGRESS_INTERVAL=60 \
./14_run_mux_clean_queue.sh
```

### 6. Continue Larger Batches

```bash
DRY_RUN=0 \
QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv \
RUN_LIMIT=20 \
PROGRESS_INTERVAL=60 \
./14_run_mux_clean_queue.sh
```

Set `RUN_LIMIT=0` or omit it to keep processing until no `PENDING` rows remain.

## Queue Status

```bash
awk -F '\t' 'NR>1{c[$1]++} END{for(k in c) print k, c[k]}' remaining_mux_clean_queue.tsv
```

Common statuses:

- `PENDING`: ready to process
- `DONE`: output verified and cleanup completed
- `DONE_REVIEW`: output created, but source files were kept for manual review
- `FAILED`: skipped or failed; source files were kept

## Supported Subtitle Inputs

Current JSON workflow:

- `.srt`
- `.ass`
- `.ssa`
- `.idx` with matching `.sub`

Manual review:

- `.sup`
- `.vtt`
- `.smi`
- unmatched `.sub`
- mixed multi-movie folders
- CD/multi-part layouts without clear part tokens
- folders with target MKV already present
- folders with extras or ambiguous side files

## Network And Storage Notes

The workflow reads the source movie from NAS and writes a new MKV back to NAS.
Expect SMB traffic to be roughly the source size plus output size, with extra
protocol overhead. Large files can look slow if another upload/download is using
the same NAS connection.

The runner prints progress every `PROGRESS_INTERVAL` seconds:

```text
PROGRESS: temp output size=...; delta=...
```

## Recovery

If a run is interrupted:

1. Re-run the same command.
2. The script will inspect existing temporary `.muxing.mkv` files.
3. Valid temporary files may be reused.
4. Invalid or stale temporary files are moved aside and rebuilt.

No source movie should be deleted before output verification succeeds.

## More Detail

See [RUNBOOK_MUX_CLEAN.md](RUNBOOK_MUX_CLEAN.md) for the operational runbook and
encoding details.

## License

No open-source license has been selected yet. Treat this repository as personal
automation code unless a license file is added.
