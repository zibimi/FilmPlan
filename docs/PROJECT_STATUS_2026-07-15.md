# FilmSubTitlePlan status - 2026-07-15

## Current queue

- `mux_clean_queue.tsv` status counts: `DONE 378`, `DONE_REVIEW 5`, `FAILED 45`, `PENDING 119`.
- The next real queue item is line 430: `/Volumes/分类/黑色电影/金臂人`.
- Line 429, `/Volumes/分类/黑色电影/邮差总按两次铃`, is intentionally `FAILED` because the CD1 movie folder includes a CD2 subtitle.

## Lessons already baked into the script

- Use `mkvmerge` for soft subtitles and remuxing; no video re-encode.
- Normalize text subtitles to UTF-8 locally before muxing.
- Treat `.srt`, `.ass`, and `.ssa` as text subtitle inputs.
- Keep `.idx/.sub` graphical subtitles out of the automatic path.
- Detect subtitle encoding by trying multiple candidates and scoring structure/content, not by trusting one tool.
- Reject replacement characters and suspicious mojibake before cleanup.
- Extract newly added subtitle tracks after muxing and verify them again before deleting sources.
- Chinese subtitles default on; English subtitles default off; unknown subtitles do not pretend to be Chinese.
- A single `und` subtitle may be default on, but it remains language `und`.
- CD1/CD2 marker mismatches fail before muxing.
- Temporary `.muxing.mkv` files are only reused if readable and plausible; otherwise they are moved aside as `abandoned`.
- Progress heartbeat reports temporary output size and growth every 60 seconds during muxing.

## Dry-run results from 2026-07-15

1. `/Volumes/分类/黑色电影/金臂人`
   - Result: dry-run failed safely.
   - Reason: folder contains `.idx/.sub` graphical subtitles.
   - Action: keep as manual review or handle with a separate OCR/graphical subtitle workflow.

2. `/Volumes/分类/黑色电影/魂断今宵`
   - Result: dry-run passed after language hint fix.
   - Movie: AVI.
   - Subtitle: `魂断今宵Angel_Face_eng.srt`.
   - Charset: `CP1252`.
   - Language: `eng`.
   - Default flag: off.

3. `/Volumes/分类/西部/原野铁汉`
   - Result: dry-run passed.
   - Movie: AVI.
   - Subtitle charset: `GB18030`.
   - Language: `chi`.
   - Default flag: on.

4. `/Volumes/分类/黑色电影/邮差总按两次铃`
   - Result: dry-run failed safely before muxing.
   - Reason: movie is `CD1`, but one subtitle is `CD2`.

## Fix made on 2026-07-15

- Updated `subtitle_lang_hint` in `14_run_mux_clean_queue.sh`.
- Chinese markers are checked before English markers, so bilingual names like `eng&chs` remain Chinese.
- English markers now include separator-based forms like `_eng`, `-eng`, `.eng.`, and ` english `.
- Updated SRT normalization in `14_run_mux_clean_queue.sh`.
- SRT subtitles are now renumbered from timing blocks during UTF-8 normalization, which fixes files that start with unnumbered cues but are otherwise valid.
- Updated subtitle encoding scoring in `14_run_mux_clean_queue.sh`.
- Files with a UTF BOM now strongly prefer the matching Unicode codec, and non-strict decodes are heavily penalized so a clean UTF-8 English subtitle cannot be misdetected as GB18030.

## Real run results from 2026-07-15

Processed safely:

- `/Volumes/分类/黑色电影/金臂人`
  - Status: `FAILED`.
  - Reason: `.idx/.sub` graphical subtitles are not handled automatically.
- `/Volumes/分类/黑色电影/魂断今宵`
  - Status: `DONE`.
  - Output: `/Volumes/分类/黑色电影/魂断今宵1952_-_Angel_Face_-_Robert_Mitchum_-_Jean_Simmons.mkv`.
  - Subtitle: English SRT, `eng`, default off.
- `/Volumes/分类/西部/原野铁汉`
  - Status: `DONE`.
  - Output: `/Volumes/分类/西部/HUD 1963.DVDrip.by_Galmuchet.mkv`.
  - Subtitle: Chinese SRT, `chi`, default on.
- `/Volumes/分类/西部/西部世界`
  - Status: `DONE`.
  - Output: `/Volumes/分类/西部/Westworld (1973) DVDRip Xvid AC3-ShitBusters.mkv`.
  - Subtitle: Chinese SRT, `chi`, default on.
- `/Volumes/分类/西部/赛伊特•汉`
  - Status: `DONE`.
  - Output: `/Volumes/分类/西部/Yilmaz_Güney-Seyyit_Han_(1968).mkv`.
  - Subtitles: Chinese SRT default on, English SRT default off.
- `/Volumes/分类/西部/金沙镇`
  - First attempt failed because mkvmerge could not recognize an unnumbered SRT.
  - Script was fixed to renumber SRT cues during normalization.
  - Retry succeeded.
  - Output: `/Volumes/分类/西部/金沙镇.Yellow.Sky.1949.DVDRip.XviD-AEN.mkv`.
  - Subtitle: Chinese SRT, `chi`, default on.

Queue after this run: `DONE 383`, `DONE_REVIEW 5`, `FAILED 46`, `PENDING 113`.

## Continued real run results from 2026-07-15

Processed safely after resuming:

- `/Volumes/分类/音乐/乐队造访`
  - Status: `DONE`.
  - Subtitle: Chinese SRT, `chi`, default on.
- `/Volumes/分类/音乐/十字街头`
  - Status: `DONE`.
  - Subtitle: Chinese SRT, `chi`, default on.
- `/Volumes/分类/音乐/安娜`
  - Status: `DONE`.
  - Subtitle: English SRT, `eng`, default off.
- `/Volumes/分类/音乐/小王子音乐剧/Le_Petit_Prince_ch`
  - Status: `DONE_REVIEW`.
  - Output passed extraction and mojibake checks, but mkvmerge skipped 2 SSA lines with invalid timestamps.
- `/Volumes/分类/音乐/期待幸福`
  - Status: `DONE`.
  - Subtitles: unknown SRT default off, Simplified Chinese default on, Traditional Chinese default off.
- `/Volumes/分类/战争/刽子手就在我们中间`
  - Status: `FAILED`.
  - Reason: `.idx/.sub` graphical subtitles are not handled automatically.
- `/Volumes/分类/战争/带黑色标记的白鸟`
  - Status: `DONE`.
  - Subtitles: unknown SRT default off, Simplified Chinese default on, Traditional Chinese default off.
- `/Volumes/分类/战争/德国,苍白的母亲`
  - Status: `DONE`.
  - Subtitle: Chinese SRT, `chi`, default on.
- `/Volumes/分类/战争/德里纳河进行曲`
  - Status: `DONE`.
  - Fix verified: English UTF-8-SIG subtitle is now detected as `eng`, not GB18030.
  - Subtitles: English default off, Chinese default on.
- `/Volumes/分类/战争/欧洲的某个地方`
  - Status: `DONE`.
  - Subtitle: Chinese SRT, `chi`, default on.
- `/Volumes/分类/战争/燃烧，燃烧，我的星`
  - Status: `DONE`.
  - Subtitles: unknown SRT default off, Simplified Chinese default on, Traditional Chinese default off.
- `/Volumes/分类/战争/西线战场`
  - Status: `DONE`.
  - Subtitles: Chinese default on, English default off.

Queue after continued run checkpoint: `DONE 393`, `DONE_REVIEW 6`, `FAILED 47`, `PENDING 101`.

## Before next real run

Recommended sequence:

```bash
cd /Users/milou/Movies/FilmSubTitlePlan
DRY_RUN=1 RUN_LIMIT=1 ./14_run_mux_clean_queue.sh
```

If line 430 remains the next item, it should fail safely because of `.idx/.sub`. For real processing, either mark that row `FAILED` manually after review or let the real run mark it failed and continue.

Then:

```bash
DRY_RUN=0 RUN_LIMIT=1 ./14_run_mux_clean_queue.sh
```

Only increase the limit after reviewing the first real output in Infuse or Finder.
