# Part-like movie merge run - 2026-07-27

Scope:
- Scanned `/Volumes/分类` and `/Volumes/导演们`.
- Looked for main-title split files named like `Part1/Part2`, `Disc1/Disc2`, `01/02`, and multi-part variants such as `1-5`.
- Excluded `#recycle` from the final processing script.

Rules used:
- Merge only candidates classified as likely feature/main work.
- Skip external-subtitle cases only when they need manual muxing; if subtitles are unrelated extras in the same folder, keep the folder and preserve subtitles.
- Require matching track signatures before merge.
- Accept `mkvmerge` warning return code only if the output can be read and duration validation passes.
- Delete original part files only after validation.
- Move the merged file to the parent folder and remove the source folder only when no meaningful extra files remain.

Outcome:
- Processed all automatically safe likely-feature candidates.
- Final remaining likely-feature candidates: 9.
- Remaining skipped groups:
  - 8 track mismatches.
  - 1 non-sequential or duplicate part naming case.

Notable processed groups:
- `/Volumes/分类/华语世界/中国大陆/导演们/王兵/死灵魂` was repaired into a complete 4-part merge.
- `/Volumes/导演们/扎克·施奈德/扎克施耐德的正义联盟` was merged into parent folder successfully.
- Multi-part groups `/Volumes/导演们/阿涅斯·瓦尔达` and `/Volumes/导演们/朱塞佩·托纳多雷/幽国车站` were merged after fixing manifest handling for more than two parts.

NAS note:
- During the run, `/Volumes/分类` and `/Volumes/导演们` disconnected.
- Finder reopened the folders and macOS remounted them.
- Observed SMB mount targets:
  - `//zibimi@ThereNone._smb._tcp.local/%E5%88%86%E7%B1%BB` -> `/Volumes/分类`
  - `//zibimi@ThereNone._smb._tcp.local/%E5%AF%BC%E6%BC%94%E4%BB%AC` -> `/Volumes/导演们`

Remaining manual review list:
- `/Volumes/分类/纪录/世纪中国` - track mismatch
- `/Volumes/分类/短篇集/台北异想` - non-sequential or duplicate part files
- `/Volumes/分类/短篇集/坏小子` - track mismatch
- `/Volumes/导演们/让·雷诺阿/艾琳娜和她的男人们` - track mismatch
- `/Volumes/导演们/法斯宾德/女人三部曲/维洛妮卡佛丝` - track mismatch
- `/Volumes/导演们/阿贝尔·冈斯/(1923)铁路的白蔷薇 La roue` - track mismatch
- `/Volumes/导演们/林赛·安德森` - track mismatch
- `/Volumes/导演们/安东尼奥尼/中国` - track mismatch
- `/Volumes/导演们/卢基诺·维斯康蒂/路德维希` - track mismatch
