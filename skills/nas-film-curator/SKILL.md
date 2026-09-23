---
name: nas-film-curator
description: Safely inventory, research, rename, restructure, and clean the user's mounted NAS film library, especially /Volumes/导演们 and /Volumes/分类. Use for movie-name normalization, director/movie folder handling, subtitle matching, multipart detection, metadata verification, archive cleanup, and JSON-tracked NAS synchronization.
---

# NAS Film Curator

Organize the mounted movie library without losing source identity or confusing a proposal with an executed change.

## Operating Contract

- Treat `/Volumes/导演们` as the default root when the request concerns directors. Never silently broaden to another `/Volumes` share.
- Confirm that the requested root is mounted before scanning. An unavailable root is an error, not an empty library.
- Prefer one snapshot followed by local JSON analysis; avoid repeatedly traversing the NAS.
- Research ambiguous metadata proactively. Do not hand ordinary lookup work back to the user.
- A parent folder is normally a search clue, not title evidence. The director-layout exceptions are defined in [references/director-layout.md](references/director-layout.md).
- Before a NAS mutation, verify the source still exists, the target does not exist, and the proposal is authorized by the current request. Use `mv -n` or equivalent no-clobber behavior.
- After every mutation batch, read back source and target state. Report actual successes, conflicts, skips, and failures separately.
- Never describe researched proposals as completed changes.

## Workflow

1. Read the relevant references below.
2. Confirm mount and scope; exclude `#recycle` and user-designated skip trees.
3. Reuse a current snapshot when possible. Refresh once if the physical library has changed materially.
4. Analyze locally and classify each item as `done`, `planned`, `review`, `skip`, `related`, or `ignore`.
5. Separate normal single films from multipart/episode resources, extras, collections, subtitles, and archives before researching names.
6. Research unresolved single films using [references/metadata-research.md](references/metadata-research.md).
7. Write only executable, high-confidence changes to the small working plan. Preserve `original_path` and `proposed_path`.
8. Validate against the immutable snapshot and current filesystem. Dry-run first unless the user explicitly requests immediate execution and the exact changes are already established.
9. Execute without overwriting, rescan only touched paths, and update statuses to `executed`, `already_done`, `conflict`, or `failed`.

For ordinary naming, read [references/naming-rules.md](references/naming-rules.md). For `/Volumes/导演们`, also read [references/director-layout.md](references/director-layout.md). Before any write, read [references/tracking-and-safety.md](references/tracking-and-safety.md).

Read [references/media-cleanup.md](references/media-cleanup.md) only for subtitles, images, archives, extras, or multipart media. Read [references/category-routing.md](references/category-routing.md) only under `/Volumes/分类`.

## Tooling

The bundled [scripts/film_naming_tool.py](scripts/film_naming_tool.py) is the current local helper. Its persistent state defaults to `/Users/milou/Movies/FilmNamingPlan`.

Typical director workflow:

```bash
python3 scripts/film_naming_tool.py snapshot-json
python3 scripts/film_naming_tool.py analyze-json --output /tmp/导演们文件快照_已分析.json
python3 scripts/film_naming_tool.py validate-plan
python3 scripts/film_naming_tool.py apply-json
python3 scripts/film_naming_tool.py apply-json --execute
python3 scripts/film_naming_tool.py plan-status
```

Do not run `--execute` merely because the command exists. The current user request must authorize the proposed filesystem changes.
