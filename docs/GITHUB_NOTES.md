# GitHub organization notes

This folder should be treated as a small private automation project.

## Recommended repository contents

Commit:

- Active scripts: `03_*.sh` through `14_*.sh`.
- Current queue snapshots: `subtitle_mux_queue.tsv`, `mux_clean_queue.tsv`.
- Human-readable docs: `README.md`, `RUNBOOK_MUX_CLEAN.md`, `PROJECT_STATUS_2026-07-15.md`, `GITHUB_NOTES.md`.
- Planning reports under `cleanup-audit/`, `cleanup-plan/`, `og-cleanup-plan/`, and `rescan-plan/` if they are useful for review.

Do not commit:

- `logs/`
- `tools/`
- downloaded binaries
- temporary `.muxing.mkv` or `abandoned` media files
- `.DS_Store`, editor swap files, and historical backup copies

## Suggested first commit

```bash
cd /Users/milou/Movies/FilmSubTitlePlan
git init
git add .
git status
git commit -m "Initial subtitle mux automation plan"
```

Use a private GitHub repository because the queue and reports contain personal NAS paths and media library structure.
