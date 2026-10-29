---
name: film-category-rules
description: Review and organize films in /Volumes/分类 using the user's genre, subject, and style preferences; inventory the selected source, research identities, produce fixed routing plans, and execute authorized moves.
---

# Film classification rules

English edition, 2026-10-27. This is a translation of the user's collection rules, with the latest execution preference incorporated. Keep Chinese directory names unchanged: they are real filesystem destinations. This is the English entry point of the same skill, not a separate competing skill.

## Workflow

1. Read [category rules](references/rules.en.md). Use the requested source; when the user says “要分类”, use `/Volumes/分类/合集/要分类`. Ask for scope only if it is missing; do not scan the entire library by default.
2. Run `scripts/inventory.py` to create a fresh read-only inventory in the local workspace. Verify mounts, errors, current files, and existing destination directories. An unavailable mount is not an empty directory.
3. Follow [research and execution](references/workflow.en.md) to establish identity and the organizing narrative. Research missing facts yourself; ask the user about collection preferences, not ordinary factual lookups. Naming need not be complete before classification, but renaming is a separate action.
4. Produce a reviewable Markdown report and fixed JSON plan. Use a deterministic executor that consumes only this plan; do not reclassify during execution.
5. The user has authorized direct moves from “要分类” when identity is established and classification confidence is at least approximately 80%. Within this continuing task, execute qualifying moves without requesting approval for each title. This is practical judgment, not a statistically calibrated probability. Record reasons and authorization. Hold unresolved identities, destination conflicts, and lower-confidence choices. This authorization does not extend to the entire library or unrelated actions.
6. Report research, pending facts, pending preferences, planned moves, actual moves, and verified results separately. Film counts and file counts differ.

## Scope and precedence

- Latest user instructions override confirmed skill rules; confirmed rules override suggested defaults. A high-confidence application of a suggested default does not turn that default into a confirmed universal preference.
- This skill supersedes conflicting legacy `nas-film-curator/references/category-routing.md` instructions about matching website tags, automatic Chinese-language routing, or requiring completed renaming before research.
- Do not route into 华语世界; franchise/series organization remains paused. 合集 may be an explicitly selected source. Pausing series does not authorize splitting them into individual films.
- Exclude hidden items, `#recycle`, `/Volumes/分类/华语世界/禁`, and `/Volumes/分类/合集/蚂蚁` unless explicitly reopened. Do not follow symlinks.
- Do not incidentally deduplicate, delete, rename, transcode, synchronize whole-library trackers, reorganize director libraries, or publish to GitHub. Each requires its own authorized scope.
- Preserve subtitles, extras, multipart films, and related versions. Choose one primary location; do not resolve category overlap by making copies.

## Reuse and refinement

Record general preferences as rules and title-specific decisions as cases. Do not extrapolate a single approved title into a universal rule. Update both language editions together. Preserve the distinction between preference, confidence, and authorization.

Examples:
- `$film-category-rules Review /Volumes/分类/故事 and show a preview.`
- `$film-category-rules Organize 要分类 using my 80% confidence threshold; exclude 华语世界 and leave series alone.`
- `$film-category-rules Execute the specified approved plan and verify the results.`

This is a reusable workflow, not a scheduled background task.
