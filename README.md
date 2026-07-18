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
├── 14_run_mux_clean_queue.sh          # Runs the mux/verify/cleanup queue
├── 15_rescan_remaining_subtitles.py   # Scans the library and writes audit files
├── 16_prepare_remaining_mux_queue.py  # Moves subtitle-only subfolders and builds queue
├── README.md
├── RUNBOOK_MUX_CLEAN.md
├── remaining_mux_clean_queue.tsv      # Current queue
├── rescan-plan/                       # Latest audit result
├── docs/                              # Project notes and status snapshots
└── archive/                           # Older scripts, queues, and reports
```

Ignored local-only paths:

- `logs/`
- `tools/`
- `downloads/`
- temporary MKV/media output

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
./14_run_mux_clean_queue.sh
```

With the default `DRY_RUN=1`, this command should only print what it would do.

If MKVToolNix is not in `PATH`, either place `MKVToolNix.app` under:

```text
tools/MKVToolNix.app
```

or pass explicit tool paths:

```bash
MKVMERGE=/path/to/mkvmerge \
MKVEXTRACT=/path/to/mkvextract \
./14_run_mux_clean_queue.sh
```

## Configuration

The scanner defaults to:

```text
/Volumes/导演们
/Volumes/分类
```

Override roots with a newline-separated `ROOTS` value:

```bash
ROOTS=$'/Volumes/导演们\n/Volumes/分类' DRY_RUN=1 ./15_rescan_remaining_subtitles.py
```

The runner defaults to:

```text
remaining_mux_clean_queue.tsv
```

Override it with `QUEUE_FILE`:

```bash
QUEUE_FILE=/path/to/queue.tsv ./14_run_mux_clean_queue.sh
```

## Full Workflow

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

Automatic queue:

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
- multi-CD layouts
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
