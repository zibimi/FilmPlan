# `/Volumes/导演们` Layout

## Terms

- **Director folder:** `/Volumes/导演们/<导演名>`.
- **Direct movie file:** a video directly inside a director folder.
- **Movie folder:** a child folder inside a director folder representing one work. It may contain one feature, multipart discs, a feature plus subtitles, extras, or a series.

## Folder Evidence

A parent folder is generally only a lookup clue. Two director-layout exceptions may provide metadata after identity confirmation:

1. A movie folder whose name is a clear Chinese movie title may provide the Chinese title for files inside that same folder.
2. A folder shaped like `(年份)中文名 外语名` may provide all three fields. Rename the folder to `中文名` and its feature to `中文名.外语名.年份.剩余信息.ext`.

Never treat `默片`, `有声片`, `短片`, `花絮`, `字幕`, `资料`, `合集`, or `电视剧` as movie titles.

## Direct Movie Files

- Research from the file name plus director name. The director disambiguates search; it is not automatically part of the final name.
- Disc-like `D1.`/`D2.` prefixes in Harold Lloyd material may be stripped before matching, without erasing real multipart identity.
- Buster Keaton short-film collections and Georges Méliès collections are standing skips unless the user reopens them.

## Movie Folders

- Rename feature and subtitle files first; rename the folder only after contents are correct.
- With exactly one video and no companion or nested content: rename it, move it to the director folder with no-clobber semantics, verify it, then remove the empty folder using `rmdir`.
- With one video plus one subtitle: keep them together, align stems, and name the folder with the Chinese title.
- With A/B, CD1/CD2, Disc1/Disc2, Part1/Part2, numbered features, or episodes: treat the whole group as multipart. Do not flatten or independently normalize it; record it in the multipart backlog.
- Historical disc splits may use `中文名.外语名.年份.CD1.ext` only when the user chooses to retain them. The current preference is often to replace them with a complete source later.
- Remove an empty directory only with `rmdir`, never recursive deletion.

## Extras And Collections

- Skip interviews, commentary, trailers, deleted scenes, making-ofs, video essays, person profiles, and other extras during feature naming.
- When the relationship is certain and organization is requested, extras may go under the movie folder's `花絮` child.
- Preserve collections, series, trilogies, and old short-film anthologies unless item-level normalization is explicitly requested.
