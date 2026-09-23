# Tracking And Safe Execution

## Persistent Files

Keep durable planning data outside the NAS media tree, currently under `/Users/milou/Movies/FilmNamingPlan`:

- `导演们文件快照.json`: immutable original backup.
- `导演们文件快照_当前.json`: refreshed physical-state snapshot when needed.
- `导演们_改名计划.json`: small editable synchronization plan.
- `导演们_多段资源清单.json`: multipart/replacement backlog; never feed it to the normal rename executor.
- equivalent `分类...` files for `/Volumes/分类`.

Write disposable scans, previews, and validation output to `/tmp`. Do not create a permanent JSON for every pass.

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

## Validation

Before execution verify mount, snapshot membership, current source existence, target absence, unique sources/targets, authorized-root containment, companion/multipart integrity, and `problem_count = 0`.

## Execution

- Preview exact old and new paths.
- Use `/bin/mv -n` for same-volume moves.
- Never overwrite an existing media target or use `rm -rf`.
- Verify source absent, target present, and expected regular-file size after each success.
- Delete emptied directories only with `rmdir` after checking hidden/nested entries.
- Update plan status immediately so resumed runs do not repeat work.
- Report proposed, executed, already done, skipped, conflicted, and failed counts separately.
