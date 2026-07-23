# Film Subtitle Plan Final Report

Generated: 2026-07-22

## 1. Scope

This report summarizes the current subtitle muxing and cleanup work for the movie library under:

- `/Volumes/分类`
- earlier related work under `/Volumes/导演们`

The active project is:

- `/Users/milou/Movies/FilmSubTitlePlan`
- GitHub: `https://github.com/zibimi/FilmPlan`

The main objective was:

- mux external subtitles into movie files as soft subtitles
- standardize outputs as MKV where possible
- avoid video/audio re-encoding
- preserve quality with stream copy/remux behavior
- clean old source folders only after verified outputs exist
- keep multi-part folders in place
- avoid deleting ambiguous source/subtitle pairs

## 2. Safety Rules Currently Followed

The current workflow follows these rules:

- Source video is not deleted until the output MKV exists and passes verification.
- Text subtitles are decoded, normalized to UTF-8, muxed, then extracted back from the output MKV for verification.
- Text subtitle verification checks:
  - replacement character count is `0`
  - mojibake score is `0` or below the configured risk threshold
  - Chinese tracks contain CJK characters
  - non-Chinese tracks do not contain suspicious CJK or mojibake
- VobSub subtitles (`.idx + .sub`) are verified by appended subtitle tracks because they are image subtitles and cannot be text-extracted for encoding validation.
- CD1/CD2 and multi-part movies remain inside their original folder after muxing.
- Single-movie folders can be flattened only when no meaningful leftover files/subfolders remain.
- Collection/franchise/series folders are preserved.
- Ambiguous cases are left for manual review.

## 3. Main Scripts

Important files:

- `17_run_manual_approved_mux.py`
  - Executes an approved JSON queue.
  - Handles MKV/MP4/AVI/RMVB-like sources through `mkvmerge`.
  - Handles SRT/ASS/SSA and VobSub `.idx + .sub`.
  - Performs subtitle encoding detection and post-mux verification.

- `18_refresh_scan_subtitle_work.py`
  - Scans roots/categories.
  - Generates mux queues, cleanup plans, and reports.
  - Supports category-specific scanning with:
    - `--root`
    - `--prefix`
    - `--include-single`
    - `--apply`

Important directories:

- `rescan-plan/`
  - category reports
  - category mux queues
  - cleanup action files

- `logs/`
  - mux logs
  - normalized subtitles
  - extracted verification subtitles
  - manual run logs

## 4. GitHub Status

Current repository:

- `https://github.com/zibimi/FilmPlan`

Latest pushed commit at the end of this phase:

- `5ba2124 Record romance audit`

The working tree was clean after the last run.

## 5. Categories Processed Or Audited

The following `/Volumes/分类` categories have now been processed or audited with category-level reports:

- `华语世界`
- `传记·一段历史`
- `动画片`
- `公路`
- `冒险·灾难`
- `体育`
- `CULT·实验`
- `黑色电影`
- `家庭`
- `恐怖`
- `情色`
- `西部`
- `音乐`
- `战争`
- `爱情`
- `纪录`
- `青春·儿童`
- `科幻·奇幻`
- `短篇集`
- `合集`
- `动漫改真`
- `政法委`
- `名著改编`
- `宗教`
- `故事`
- `歌舞`
- `喜剧`
- `怪兽`
- `惊悚·犯罪·动作`

`/Volumes/分类/#recycle` is intentionally ignored.

## 6. Recently Completed Work

### 华语世界

Completed:

- `/Volumes/分类/华语世界/香港/导演们/彭浩翔/出埃及记`

Result:

- MKV output moved to parent folder.
- Chinese SRT was detected as `gb18030`.
- Verification passed:
  - Chinese default subtitle track present
  - extracted CJK count: `5956`
  - replacement characters: `0`
  - mojibake: `0`

Remaining manual cases:

- `台湾/杨德昌/恐怖分子`
- `禁/地震`
- broader collection-level duplicate-token reports in `华语世界`

### 传记·一段历史

Completed:

- `/Volumes/分类/传记·一段历史/阿尔卡特兹的养鸟人`

Result:

- CD1 MKV received matching Chinese SRT.
- CD2 AVI was remuxed to MKV and received matching Chinese SRT.
- Folder was kept because this is a multi-part movie.

Verification:

- CD1 extracted CJK: `7820`, replacement: `0`, mojibake: `0`
- CD2 extracted CJK: `8331`, replacement: `0`, mojibake: `0`

Manual review:

- `/Volumes/分类/传记·一段历史/海伦凯勒`
  - two AVI files and two SRT files are not binary-identical
  - skipped to avoid deleting or pairing the wrong file

### 动画片

Completed:

- `/Volumes/分类/动画片/贪吃树`

Result:

- CD1/CD2 MKVs received matching VobSub subtitle pairs.
- Folder was kept because this is a multi-part movie.

Verification:

- VobSub tracks appended successfully.
- Chinese default subtitle tracks present.

Remaining manual cases:

- `动画大师`
- `卢茨·丹姆贝克作品集(1975-1986)`
- `大妹子们的动画时间`
- `胡萝卜之夜`

### CULT·实验

Completed:

- `/Volumes/分类/CULT·实验/月亮上的人`
- `/Volumes/分类/CULT·实验/莫雷尔的发明`

Result:

- `月亮上的人` CD1/CD2 MP4 files were remuxed to MKV with matching VobSub subtitle pairs.
- `莫雷尔的发明` AVI was remuxed to MKV with Chinese SRT and flattened to the parent category.

Verification:

- `月亮上的人`: VobSub tracks appended successfully.
- `莫雷尔的发明`:
  - subtitle encoding: `gb18030`
  - extracted CJK: `5340`
  - replacement: `0`
  - mojibake: `0`

Remaining manual case:

- `/Volumes/分类/CULT·实验/亲信`
  - three MKV files
  - subtitles are `英文.srt`, `簡體.srt`, `正體.srt`
  - no reliable per-part mapping

### 黑色电影

Completed cleanup for residual folders:

- `/Volumes/分类/黑色电影/十字交锋`
- `/Volumes/分类/黑色电影/卡车斗士`
- `/Volumes/分类/黑色电影/堕落天使`
- `/Volumes/分类/黑色电影/夜逃鸳鸯`
- `/Volumes/分类/黑色电影/步步惊魂`

Reason:

- parent-level MKV outputs already existed
- each target was inspected and confirmed to contain subtitle tracks
- residual source folders were removed after verification

Verified target subtitle counts:

- `十字交锋Cris_Cros_1949.mkv`: `2`
- `They_Drive_by_Night_(1940).mkv`: `8`
- `堕落天使Fallen_Angel_(1945).mkv`: `1`
- `夜逃鸳鸯They_Live_by_Night_(1948).mkv`: `1`
- `步步惊魂Point_Blank.mkv`: `1`

Note:

- `They_Drive_by_Night_(1940).mkv` contains multiple VobSub subtitle tracks, and several are marked default by mkvmerge. This is not a text-encoding risk, but default flags can be cleaned later if desired.

### Empty Audit Categories

These were scanned and had no remaining mux, cleanup, or review items:

- `公路`
- `冒险·灾难`
- `体育`
- `家庭`
- `恐怖`
- `情色`
- `西部`
- `音乐`
- `战争`
- `爱情`

## 7. Remaining External Subtitle Files

The latest full scan under `/Volumes/分类`, excluding `#recycle`, still finds external subtitle files in these areas.

### 华语世界

- `/Volumes/分类/华语世界/台湾/杨德昌/恐怖分子`
  - VobSub pair:
    - `[恐怖分子].Terroriser.1986.DVDRip.X264-KEN.idx`
    - `[恐怖分子].Terroriser.1986.DVDRip.X264-KEN.sub`

- `/Volumes/分类/华语世界/禁/地震`
  - multiple NHK SRT files:
    - `[NHK][纪录片]四川大地震 ～被封印的瞬间～.srt`
    - `[NHK][纪录片]四川大地震灾区现状系列(1)重建家园路漫漫.srt`
    - `[NHK][纪录片]四川大地震灾区现状系列(3)观光村风波.srt`
    - `[NHK][纪录片]李老师和30个孩子们.srt`
    - `[NHK][纪录片]颤慄的童心：陈美龄 四川大地震报告.srt`
    - `[NHK]中国·四川大地震.srt`

### 传记·一段历史

- `/Volumes/分类/传记·一段历史/海伦凯勒`
  - `[海伦凯勒].The.Miracle.Worker.1962..XviD....srt`
  - `[海伦凯勒].The.Miracle.Worker.1962.XviD.....srt`

Skipped because the two AVI files and two SRT files are not binary-identical.

### 动画片

- `/Volumes/分类/动画片/动画大师/【翻译】《动画大师》(Masters of Animation)`
  - multiple Chs/Eng SRT/ASS files

- `/Volumes/分类/动画片/卢茨·丹姆贝克作品集(1975-1986)`
  - multiple Chs/Eng SRT files

- `/Volumes/分类/动画片/大妹子们的动画时间/[SGS][Otona_Jyoshi_no_Anime_Time_Kawamo_wo_Suberu_Kaze][720p][Subs_Fonts]`
  - `.jpsc.ass`
  - `.jp.ass`
  - `.sc.ass`

- `/Volumes/分类/动画片/胡萝卜之夜`
  - `Priit Parn (1998) - Porgandite Oo.srt`
  - `Priit Parn (1998) - Porgandite Oo_eng_new.srt`

These are collection/series/nested subtitle cases that need explicit matching before muxing.

### CULT·实验

- `/Volumes/分类/CULT·实验/亲信`
  - `英文.srt`
  - `簡體.srt`
  - `正體.srt`

Skipped because the folder has multiple MKVs but the subtitles do not identify which movie/part they belong to.

### Previously Known Manual Review Areas

These remain from earlier category passes:

- `/Volumes/分类/短篇集/大师们的第一部`
- `/Volumes/分类/短篇集/穆府的歌剧`
- `/Volumes/分类/喜剧/黑色池塘`
- `/Volumes/分类/惊悚·犯罪·动作/人性`
- `/Volumes/分类/青春·儿童/坏痞子`

Reasons include ambiguous CD pairing, orphan subtitle-only folders, missing matching movie files, or unclear subtitle-to-video mapping.

## 8. Known Limitations

### Text subtitles

SRT/ASS/SSA are reasonably safe because the runner:

- tries multiple encodings
- chooses the best candidate using subtitle timing, CJK count, Latin count, replacement characters, and mojibake scoring
- writes normalized UTF-8 temporary subtitles
- muxes the normalized subtitle
- extracts the muxed subtitle back from the MKV
- checks it again

This does not prove every line is semantically correct, but it catches the common dangerous cases:

- GBK/GB18030 decoded as UTF-8
- Big5/CP950 mistakes
- mojibake
- replacement characters
- wrong Chinese/non-Chinese language assumption

### VobSub subtitles

VobSub `.idx + .sub` are image subtitles, so there is no character encoding to validate.

The safe checks are:

- `.idx` and `.sub` exist as a pair
- the pair matches the movie/part
- mkvmerge appends subtitle tracks
- output MKV contains the appended subtitle tracks
- default language flags are set

Visual correctness still requires playback if the source subtitle image stream itself is wrong.

### `.sup` subtitles

PGS `.sup` can be muxed with mkvmerge, but the current automatic runner is not primarily designed around `.sup`.

Previously this was handled manually for:

- `/Volumes/分类/故事/昨日青春`

### RMVB/RM

The runner can ask mkvmerge to remux RMVB/RM-like inputs to MKV, but compatibility depends on mkvmerge support for the specific file.

For RMVB/RM, keep-source behavior has generally been conservative.

## 9. Suggested Next Steps

The remaining work should not be run as one broad automatic cleanup. The right next phase is targeted manual matching for the remaining folders.

Recommended priority:

1. `华语世界/台湾/杨德昌/恐怖分子`
   - likely simple VobSub case

2. `动画片/胡萝卜之夜`
   - likely simple single movie with Chinese/English subtitles

3. `CULT·实验/亲信`
   - inspect the three MKVs to determine whether they are duplicate versions or separate parts

4. `传记·一段历史/海伦凯勒`
   - compare durations/content and decide which AVI/SRT pair is correct

5. Large collection folders:
   - `动画大师`
   - `卢茨·丹姆贝克作品集`
   - `大妹子们的动画时间`
   - `华语世界/禁/地震`

For the collection folders, the best next script improvement would be a "strict basename matcher" report:

- list movie files
- list subtitle files
- propose subtitle-to-movie pairs
- require exact normalized basename, episode token, or explicit user approval
- generate a manual queue only after review

## 10. Bottom Line

The broad `/Volumes/分类` cleanup phase is complete.

The library is now mostly clean from the perspective of simple muxable subtitle folders. The remaining external subtitle files are concentrated in a small number of complex or ambiguous folders.

The automation is safe enough for:

- single movie + clearly matching text subtitle
- CD1/CD2 with clearly matching text subtitle
- CD1/CD2 with clearly matching VobSub pairs
- cleanup of old source folders when target MKV is verified

The automation should still avoid:

- multiple movies with generic subtitles
- collection folders without exact matching
- duplicate source files that are not binary-identical
- orphan subtitles when the matching movie cannot be found
