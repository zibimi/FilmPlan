# Documentary folder cleanup summary

Generated: 2026-07-20
Updated: 2026-07-21

Scope: `/Volumes/分类/纪录`

## Rule Correction

- Single-movie-only folders may be flattened: move the finished movie to the parent folder and remove the now-empty movie folder.
- Multi-movie folders, including CD1/CD2 and numbered-part folders, must stay as folders. After muxing, keep finished MKV files inside the original folder and clean only old no-subtitle movie files plus subtitle sidecars.
- Folders with extras/subfolders should keep those extras/subfolders.

## Completed / Confirmed

- `世纪中国`: 3 VobSub pairs confirmed in the original multi-file folder.
- `大熊猫的生活`: CD1, CD2, and Extra confirmed in the original multi-file folder.
- `森山大道`: 2 movie files restored into the original multi-file folder after the rule correction.
- Single-movie folder flatten actions already completed: 8.

## Needs Manual Review

- `寻找贝多芬`: one finished file was restored into the original folder; the expected `(1)` output was not found during the restore audit. Do not clean this folder automatically until it is checked.

## Final Rule For Future Runs

- `category=cd` or `category=multi`: `keep_folder=true`; target output stays inside the original folder.
- Single movie without real subfolders: target output may be placed in the parent folder as part of flattening.
- Any missing expected output or ambiguous pair remains `MANUAL_REVIEW`.
