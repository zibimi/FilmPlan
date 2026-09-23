# Naming Rules

## Canonical Form

Preferred feature-film filename:

```text
中文名.Foreign.or.Original.Title.年份.剩余信息.ext
```

Examples:

```text
伊甸园之东.East.of.Eden.1955.mkv
底层的珍珠.Perlicky.na.dne.1965.cz.dabing.AX.mkv
牛头.極道恐怖大劇場.牛頭.2003.mkv
```

- Put the Chinese title first when a reliable Chinese title exists.
- The foreign title may be English, the original language, romanization, or another established title. Do not translate a valid non-English title to English merely for uniformity.
- Replace spaces inside Chinese and foreign title components with `.`. Use `.` between semantic components and collapse repeated dots.
- Remove decorative square brackets and release-site prefixes from normal feature names. Preserve useful release, source, codec, edition, subtitle-group, and disc information after the year.
- Keep exactly one real extension. A source tag such as `mpeg` may remain before `.mkv` only when it describes the original resource rather than an accidental duplicate extension.
- Use the film's release year. For concert/stage recordings, deliberately choose performance, production, broadcast, or release year and note which one was used when ambiguous.
- Do not silently change a film to a remake or another same-title version. Match title, year, director, country/language, runtime, and available technical clues.
- If no reliable Chinese title exists, `Original.Title.年份.ext` is acceptable. Do not invent a Chinese film title unless the user authorized a literal translation and identity is otherwise high confidence.

## Incomplete Names

Flag a normal single feature when it lacks a reliable available Chinese title, foreign/original title, four-digit release year, or dot boundaries. Also flag glued titles, spaces/underscores/brackets, download-site advertisements, collection prefixes, and possible wrong-version matches.

Do not apply this strict test unchanged to series episodes, collections, short-film anthologies, extras, concerts, stage recordings, or archival material.

## Remainder Preservation

After `中文名.外文名.年份`, retain meaningful tokens such as source, resolution, codec, edition, restoration, broadcaster, language, and subtitle-group information. Preserve `CD1`, `Part1`, or episode markers only when intentionally retaining multipart media.

## Companion Subtitles

- Match the movie stem exactly.
- Add `.chs`, `.cht`, or `.eng` before the subtitle extension when known.
- Keep `.idx` and `.sub` together as one VobSub pair.
- Do not guess language solely from encoding or a generic numeric name.
