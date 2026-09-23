# Subtitles, Archives, Images, And Multipart Media

## Subtitles

- Align a companion subtitle with the final feature stem.
- Use `.chs`, `.cht`, or `.eng` when known; keep `.idx` and `.sub` together.
- Do not delete an external subtitle merely because an MKV exists. Verify the intended subtitle track was muxed first.

## Images And Small Debris

- The standing preference allows deleting obvious `.jpg`, `.jpeg`, `.png`, and `.webp` files during an explicitly authorized cleanup pass. Preview and log paths.
- `.par2` recovery files may be deleted under the user's standing rule; record them.
- Ignore `.DS_Store` for naming and remove it only during authorized cleanup.

## Archives

- Exclude `#recycle`.
- A pure subtitle archive may extract only `.srt`, `.ass`, `.ssa`, `.sub`, and `.idx`.
- Delete an archive only after successful extraction, content validation, and verified placement in its original NAS directory.
- For multipart RAR/numeric slices, copy every part to a local temporary directory, extract locally, validate, upload to the original location, validate again, then delete local and NAS archive parts.
- If an equivalent extracted target already exists on NAS, skip duplicate upload; remove archives only after verifying equivalence.
- Keep at least 8 GB local free by default and process serially.
- On unexpected layout, missing volume, extraction failure, timeout, or size mismatch: record and skip without deletion.
- Prefer `7zz`, `7z`, `unar`, or `unrar`; macOS `bsdtar` has failed on RAR multipart data.

## Multipart Features

- Detect A/B, CD, Disc, Part, Pt, D1/D2, numbered adjacent features, and episodes before ordinary naming.
- Keep groups out of the rename plan and add every full path to `导演们_多段资源清单.json`.
- Do not merge based on names alone. Verify codec, dimensions, frame rate, streams, duration, ordering, and shared identity.
- The common preference is later replacement with a complete source; preserve existing segments until a separate merge/replacement task is authorized.
