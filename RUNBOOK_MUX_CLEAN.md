# FilmPlan Runbook

This runbook explains which script to use for each library-maintenance task.

The short version:

- use `18_refresh_scan_subtitle_work.py` to scan subtitle work
- use `17_run_manual_approved_mux.py` to execute approved JSON mux queues
- use `17_scan_bdmv_playlists.py` for Blu-ray/BDMV folders
- use `scripts/merge_part_like_features.py` for split movie files
- use `14/15/16` only for old TSV queues

## 1. Normal Subtitle Work

Use this for folders that contain a movie file plus external subtitles.

Supported inputs:

- `.mkv`
- `.mp4`
- `.avi`
- `.rmvb` / `.rm` when mkvmerge can read them
- `.srt`
- `.ass`
- `.ssa`
- `.idx + .sub` VobSub pairs

### 1.1 Scan One Category

Use:

```bash
python3 18_refresh_scan_subtitle_work.py \
  --root /Volumes/分类/科幻·奇幻 \
  --prefix scifi \
  --include-single
```

Use this when:

- you want to inspect one category
- you do not want to modify NAS files yet
- you want a fresh report and queue

Outputs:

- `rescan-plan/scifi_mux_queue.json`
- `rescan-plan/scifi_cleanup_actions.json`
- `rescan-plan/scifi_report.md`

NAS changes:

- none

### 1.2 Scan One Category And Execute

Use:

```bash
python3 18_refresh_scan_subtitle_work.py \
  --root /Volumes/分类/科幻·奇幻 \
  --prefix scifi \
  --include-single \
  --apply
```

Use this when:

- the scan report looks correct
- mux tasks are clearly matched
- review items can remain untouched

What happens:

- scans the category
- writes fresh queue/report files
- runs pending mux tasks with `17_run_manual_approved_mux.py`
- applies cleanup-only actions

NAS changes:

- yes
- source movie/subtitle files are removed only after output verification
- multi-part folders stay in place
- ambiguous leftovers are kept as `DONE_REVIEW`

## 2. Manually Approved Subtitle Queue

Use this for tricky but confirmed cases, for example:

- subtitle files are in a nested subfolder
- CD1/CD2 subtitles have different basenames but you verified the pairing
- the scanner was too conservative but the mapping is clear

Queue format:

```json
[
  {
    "id": "manual-0001",
    "status": "PENDING",
    "category": "single",
    "folder": "/Volumes/分类/example/Movie Folder",
    "movie": "/Volumes/分类/example/Movie Folder/Movie.avi",
    "target": "/Volumes/分类/example/Movie.mkv",
    "subtitles": [
      {
        "path": "/Volumes/分类/example/Movie Folder/Movie.zh.srt",
        "lang": "chi"
      }
    ],
    "keep_source": false,
    "keep_folder": false,
    "ignore_leftovers": false,
    "note": "manual confirmed match"
  }
]
```

Run:

```bash
MUX_QUEUE=/Users/milou/Movies/FilmSubTitlePlan/rescan-plan/manual_case_queue.json \
MUX_RUN_LOG=/Users/milou/Movies/FilmSubTitlePlan/logs/manual-case.log \
python3 17_run_manual_approved_mux.py
```

Use `keep_folder: true` for:

- CD1/CD2 movies
- multi-part movies
- folders that contain extras you want to preserve

Use `ignore_leftovers: true` when:

- output can be verified
- used movie/subtitle files can be deleted
- unrelated leftovers should not block the task

## 3. Subtitle Encoding Safety

Text subtitle flow:

1. read the subtitle bytes
2. try likely encodings such as UTF-8, GB18030, Big5/CP950, UTF-16, CP125x
3. score the decoded text
4. normalize to UTF-8
5. mux into MKV
6. extract the new text subtitle track from the output MKV
7. verify extracted text again

Checks:

- replacement character count must be `0`
- Chinese tracks must contain CJK text
- non-Chinese tracks must not contain suspicious CJK
- mojibake score must stay below the safety threshold

VobSub `.idx + .sub` is different:

- it is an image subtitle format
- there is no text encoding to check
- the runner verifies appended track count and language/default flags
- visual correctness still requires playback if the source VobSub itself is suspicious

## 4. Blu-ray / BDMV Folders

Use:

```bash
python3 17_scan_bdmv_playlists.py /path/to/Blu-ray-folder
```

Use this when:

- a movie folder contains `BDMV/`
- you need to identify feature playlists and extras
- you want to preserve embedded audio/subtitle tracks

Outputs:

- `bdmv-plan/bdmv_playlists_<disc>_<timestamp>.md`
- `bdmv-plan/bdmv_playlists_<disc>_<timestamp>.tsv`

NAS changes:

- none

The scanner classifies playlists as:

- `FEATURE`
- `EXTRA_CANDIDATE`
- `DUPLICATE_OF_FEATURE`
- `REVIEW_REPEATED_STREAM`
- `TINY_SKIP`

After reviewing the report, use the suggested `mkvmerge` commands manually or
build a task-specific script. Do not blindly remux every `.mpls`.

## 5. Split Movie File Merge

Use:

```bash
python3 scripts/merge_part_like_features.py --write-manifest part_like_manifest.json
```

Use this when:

- a movie is split into `Part1/Part2`, `Disc1/Disc2`, `01/02`, etc.
- the files should become one MKV
- the folder does not have external subtitles that need separate handling

First run writes a manifest only:

```bash
python3 scripts/merge_part_like_features.py \
  --write-manifest part_like_manifest.json
```

Review the manifest. Then execute only the approved manifest:

```bash
python3 scripts/merge_part_like_features.py \
  --manifest part_like_manifest.json \
  --execute
```

Safety checks:

- skips `#recycle`
- compares track signatures
- verifies final duration
- deletes original part files only after merged MKV can be read
- keeps folders when extras or meaningful leftovers remain

## 6. NAS Remount Helper

Use:

```bash
./scripts/remount_movie_volumes.sh
```

Use this when:

- `/Volumes/分类` or `/Volumes/导演们` disappeared
- macOS dropped the SMB mount during a long run

NAS changes:

- no media changes
- it only asks macOS to reopen known SMB shares

## 7. Legacy TSV Subtitle Workflow

These scripts are kept for old queue compatibility:

- `15_rescan_remaining_subtitles.py`
- `16_prepare_remaining_mux_queue.py`
- `14_run_mux_clean_queue.sh`

Use them only when you specifically need the old TSV queue:

```text
remaining_mux_clean_queue.tsv
```

Old sequence:

```bash
DRY_RUN=1 ./15_rescan_remaining_subtitles.py
DRY_RUN=1 ./16_prepare_remaining_mux_queue.py
DRY_RUN=0 ./16_prepare_remaining_mux_queue.py
DRY_RUN=0 QUEUE_FILE=remaining_mux_clean_queue.tsv RUN_LIMIT=5 PROGRESS_INTERVAL=60 ./14_run_mux_clean_queue.sh
```

For new category-level work, prefer the JSON workflow in sections 1 and 2.

## 8. Generated Files

These paths are local run artifacts and should not be committed:

- `logs/`
- `rescan-plan/`
- `bdmv-plan/`
- `archive/`
- `manual_approved_mux_queue.json`
- `remaining_mux_clean_queue.tsv`
- `part_like_feature_manifest_*.json`
- `tools/`

## 9. Recovery

If a run is interrupted:

1. Check the queue JSON or TSV status.
2. Re-run the same command if the task is still `PENDING`.
3. The runner removes stale temporary `.manual.muxing.mkv` files before retrying.
4. Do not manually delete source files unless the output MKV has been verified.

No source movie should be deleted before output verification succeeds.
