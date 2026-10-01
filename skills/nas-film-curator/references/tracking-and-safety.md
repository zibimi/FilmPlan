# Tracking And Safe Execution

## Persistent Files

Keep durable planning data outside the NAS media tree, currently under `/Users/milou/Movies/FilmNamingPlan`:

- `导演们文件快照.json`: immutable original backup.
- `导演们文件快照_当前.json`: refreshed physical-state snapshot when needed.
- `导演们_改名计划.json`: small editable synchronization plan.
- `导演们_多段资源清单.json`: multipart/replacement backlog; never feed it to the normal rename executor.
- equivalent `分类...` files for `/Volumes/分类`.

Write disposable scans, previews, and validation output to `/tmp`. Do not create a permanent JSON for every pass.

For the active `/Volumes/分类` workflow, the maintained tracker is currently:

```text
/Users/milou/Documents/电影整理计划/分类审阅草案/每日命名扫描.json
```

Refresh this file in place rather than creating another permanent scan. Preserve execution history, research metadata, and the earliest known `original_path`, but replace stale path membership with the current mounted filesystem.

## Plan Record

```json
{
  "id": "rename-00001",
  "operation": "rename",
  "status": "planned",
  "original_path": "/Volumes/导演们/导演/old.mkv",
  "proposed_path": "/Volumes/导演们/导演/中文名.Title.2000.mkv",
  "reason": "metadata evidence and normalization reason",
  "confidence": "high",
  "sources": [],
  "notes": []
}
```

Statuses:

- `done`: already compliant;
- `planned`/`approved`: ready for execution;
- `executed`: this plan changed the NAS successfully;
- `already_done`: source absent and verified target present;
- `review`: unresolved metadata or structure;
- `skip`: multipart, series, extras, collection, or user skip;
- `related`: subtitle/archive/companion;
- `ignore`: unrelated ordinary file;
- `conflict`/`failed`: stop and do not retry blindly.

When a human or a completed research pass has conclusively classified an item,
store a locked `review_override` with its disposition, issues, reason, and review
time. A refresh may update the live path, size, and mtime, but must not replace
that conclusion with filename heuristics. Remove or revise the override only
after a new review changes the conclusion.

## Validation

Before execution verify mount, snapshot membership, current source existence, target absence, unique sources/targets, authorized-root containment, companion/multipart integrity, and `problem_count = 0`.

Before trusting tracker status, also verify:

- tracked count equals the current in-scope path count;
- `live_not_tracked = 0` and `tracked_not_live = 0` after an intentional refresh;
- extensions include F4V, OGG/Theora, DAT/VCD, and content-detected video with missing or abnormal extensions;
- `done` is not inferred merely from a previous review action.

## Execution

- Preview exact old and new paths.
- Use `/bin/mv -n` for same-volume moves.
- Never overwrite an existing media target or use `rm -rf`.
- Verify source absent, target present, and expected regular-file size after each success.
- Delete emptied directories only with `rmdir` after checking hidden/nested entries.
- Update plan status immediately so resumed runs do not repeat work.
- Report proposed, executed, already done, skipped, conflicted, and failed counts separately.
