# Remaining Subtitle Rescan - 2026-07-17

This pass exists because the older scanner missed VobSub subtitles. The runner
already supports `.idx` plus matching `.sub`, but the scanner only looked for
text subtitles at first.

## Current Result

- Latest audit summary:
  `/Users/milou/Movies/FilmSubTitlePlan/rescan-plan/remaining_subtitle_audit_summary_20260717-173931.md`
- Remaining mux queue:
  `/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv`
- Queue rows added: `243`
- Candidate folders before target-exists filtering: `245`
- Subtitle move rows: `23`
- Complex cases: `217`

The automatic queue only includes formats already handled by the runner:

- `.srt`
- `.ass`
- `.ssa`
- `.idx` with matching `.sub`

The audit does not automatically queue `.sup`, `.vtt`, `.smi`, or unmatched
`.sub` files.

## Safe Order

From:

```bash
cd /Users/milou/Movies/FilmSubTitlePlan
```

1. Rebuild the audit report, dry-run only:

```bash
DRY_RUN=1 ./15_rescan_remaining_subtitles.py
```

2. Preview subtitle moves and rebuild the remaining queue:

```bash
DRY_RUN=1 ./16_prepare_remaining_mux_queue.py
```

3. Actually move subtitle-only subfolder files to the movie folder and rebuild
   the remaining queue:

```bash
DRY_RUN=0 ./16_prepare_remaining_mux_queue.py
```

4. Dry-run the first queued movie:

```bash
QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv RUN_LIMIT=1 ./14_run_mux_clean_queue.sh
```

5. Run a small real batch:

```bash
DRY_RUN=0 QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv RUN_LIMIT=5 PROGRESS_INTERVAL=60 ./14_run_mux_clean_queue.sh
```

6. Continue larger batches after the first batch looks good:

```bash
DRY_RUN=0 QUEUE_FILE=/Users/milou/Movies/FilmSubTitlePlan/remaining_mux_clean_queue.tsv RUN_LIMIT=20 PROGRESS_INTERVAL=60 ./14_run_mux_clean_queue.sh
```

The runner verifies appended text subtitles by extraction. VobSub image
subtitles are verified by track presence; they cannot be OCR-checked by this
script.
