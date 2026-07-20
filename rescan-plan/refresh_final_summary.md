# Refresh execution final summary

Generated: 2026-07-20

## Result

- Mux queue:
  - DONE: 75
  - DONE_REVIEW: 75
  - FAILED: 2
  - MANUAL_REVIEW: 4
- Cleanup-only actions:
  - DONE: 12

## Failed

- `/Volumes/导演们/市川昆/1964年东京奥林匹克运动会`
  - `refresh-0032`: Chinese-labeled track had no CJK after extraction.
  - `refresh-0033`: Chinese-labeled track had no CJK after extraction.
  - Source files were not removed by the failed tasks.

## Manual Review

- `/Volumes/分类/科幻·奇幻/外星奇遇`
  - Skipped because the folder contains duplicate part 1 movie candidates:
    `Kin_Dza_Dza_GLs1.avi` and `外星奇遇.Kin-dza-dza.1986.e1.BD.MiniSD-TLF.mkv`.
  - The script could not safely choose which part 1 file should receive the part 1 subtitle.

- `/Volumes/分类/青春·儿童/往事如烟`
  - CD1 initially matched an unrelated `Riget/The Kingdom` subtitle because the old matcher relied too much on `CD1`.
  - The wrong subtitle track was removed from the output.
  - Final CD1 output currently has no subtitle track and needs a correct CD1 subtitle if desired.

## Script Fixes Added During Run

- Non-Chinese subtitles now fail if extraction contains suspicious CJK characters.
- Non-Chinese subtitles now fail if extraction contains high mojibake counts.
- `.EN.srt` and similar names are now recognized as English before `Rus` or other release metadata.
- Future scans now skip folders with duplicate part tokens.
- Future scans require more than just `CD1/CD2` to match multi-part subtitles.
