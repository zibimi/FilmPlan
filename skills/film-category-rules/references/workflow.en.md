# Inventory, research, planning, and execution

## Fresh inventory

From the skill directory:

```bash
python3 scripts/inventory.py --source '/Volumes/分类/合集/要分类' --output '/tmp/film-category-snapshot.json'
```

Choose a new local output path each run; the script refuses overwrites by default. It records paths, sizes, mtimes, extensions, and resource clues without reading movie content or establishing identity. Inspect only top-level category directories outside the chosen source. Exclude symlinks, hidden items, recycle bins, and fixed excluded trees. An explicitly reopened excluded scope needs a separately scoped read-only inventory.

Check completeness, errors, mount availability, source paths, and changed category names. Never treat an old destination as valid after it has disappeared or changed. Files are not films: account separately for subtitles, artwork, extras, and parts.

## Research and classification

- Establish identity from Chinese title, original title, and year. Parent folders are clues, not proof. Resolve contradictions rather than inventing metadata.
- Follow the user's preferred order: Google search, then Douban verification; supplement with IMDb, festivals, distributors, and film archives. If Google or Douban is unavailable, state the limitation and use available sources honestly.
- Read plot descriptions and relevant criticism to explain what organizes the whole film. Website genre tags only suggest candidates. Borderline, obscure, recent, and same-title films especially need evidence.
- Separate sourced facts from collection judgments. Do not claim to have read full pages when only snippets were available. No search results does not prove nonexistence.
- For 公路, examine sustained movement, transformation caused by encounters en route, and whether the narrative would remain essentially intact without the journey. Vehicle/travel words in titles are insufficient.
- Assign one primary destination; record secondary labels and alternatives in the plan. Apply the confirmed 名著改编 priority.
- Record rule status separately from confidence. Under the current inbox authorization, established identity and approximately 80% or greater classification confidence permit execution after preflight, including reasoned applications of suggested defaults. Do not relabel these defaults as confirmed preferences.
- Hold lower-confidence preference conflicts. Continue factual research yourself. Unknown identity, unresolved resource relationships, or contradictory evidence remain research_pending. An identified film with no dominant category can fit 故事.

## Fixed plan

Create dated/batch-specific Markdown and JSON artifacts. Use stable route IDs for unchanged original paths and execution records to track moves.

Top-level fields: `schema_version`, `rule_version`, rule-file SHA-256 hashes, `source_root`, `snapshot_path`, `snapshot_sha256`, `created_at`, `scan_complete`, `items`.

Item fields: `route_id`, `original_path`, `source_size`, `source_mtime_ns`, `resource_group`, `media_kind`, `identity` (Chinese/original title, year, evidence), `proposed_path` (null if unresolved), `category`, `rule_state`, `reason`, `alternatives`, `sources` (URLs and supported facts), `confidence`, `status`, `authorization`.

Initial statuses: `keep`, `planned`, `review_preference`, `research_pending`, `related`, `skip`. Record execution outcomes separately as `executed`, `already_done`, `conflict`, or `failed`; do not erase original decisions. Authorization must cite the applicable user instruction and scope, such as the inbox 80% threshold; the presence of a skill is not permission.

Report resource counts, identified films, proposed moves, retained items, factual gaps, preference decisions, series, and associated resources. Include rule version, sources actually consulted, and unverified details.

When continuing a PR-reviewed batch, retrieve current submitted comments and review decisions before finalizing affected destinations. Match each decision to its title/stable ID. Reading feedback does not itself authorize posting replies or publishing updates.

When resuming, compare current paths, sizes, and mtimes; distinguish new, missing, and changed items. Reuse research for unchanged verified identities, but reconsider entries affected by new preferences. Never infer already_done solely from an identical destination filename.

## Execute within authorization

Research does not itself mutate the NAS. Prepare a deterministic executor that consumes only the fixed plan, defaults to dry-run, and requires an explicit execution flag and plan digest. Do not query the web or change classifications during execution. Within the user's continuing 80% inbox authorization, proceed without another per-title confirmation.

Preflight the entire batch: available mounts, authorized paths, unchanged source sizes/mtimes, existing category directories, no destination collision, complete resource groups, no symlinks or path traversal. Report conflicts separately. Unapproved, unresolved, preference-pending, and paused-series entries cannot enter the executable set.

Use no-clobber moves on the same volume and verify results. If a target appears, overwrite neither copy and delete neither copy. Cross-volume moves require a separately authorized copy/verify/cleanup plan. Include complete manifests for subtitles, parts, and extras; do not move a mixed directory wholesale.

Record intent and result per item. On recovery, compare logs and complete source/destination manifests; unprovable success is a conflict. Read back source absence and destination paths, sizes, and manifests after execution. Stop the batch on mount errors, systemic empty reads, or path drift; preserve logs and do not retry deletions automatically.

Deduplication, renaming, deletion, transcoding, publishing, and director-library migration require their own explicit scope.
