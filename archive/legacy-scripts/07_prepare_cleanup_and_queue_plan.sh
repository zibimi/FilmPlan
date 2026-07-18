#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_TSV="${AUDIT_TSV:-$WORKDIR/cleanup-audit/cleanup_audit_20260608-232657.tsv}"
QUEUE_FILE="${QUEUE_FILE:-$WORKDIR/subtitle_mux_queue.tsv}"
OUT_DIR="$WORKDIR/cleanup-plan"
TS="$(date '+%Y%m%d-%H%M%S')"

mkdir -p "$OUT_DIR"

REVIEW_IN_INFUSE="$OUT_DIR/review_in_infuse_$TS.txt"
REVIEW_BEFORE_DELETE="$OUT_DIR/review_before_delete_$TS.txt"
MANUAL_REVIEW="$OUT_DIR/manual_review_$TS.txt"
SAFE_CLEANUP_TSV="$OUT_DIR/safe_cleanup_plan_$TS.tsv"
ADD_QUEUE_ALL="$OUT_DIR/add_to_mux_queue_all_$TS.txt"
ADD_QUEUE_NEW="$OUT_DIR/add_to_mux_queue_new_$TS.txt"
SUMMARY_MD="$OUT_DIR/cleanup_plan_summary_$TS.md"

[[ -f "$AUDIT_TSV" ]] || { printf 'ERROR: audit TSV not found: %s\n' "$AUDIT_TSV" >&2; exit 1; }
[[ -f "$QUEUE_FILE" ]] || { printf 'ERROR: queue file not found: %s\n' "$QUEUE_FILE" >&2; exit 1; }

awk -F '\t' 'NR>1 && $9=="REVIEW_IN_INFUSE" {
  print $3 "\n  movie: " $4 "\n  note: " $10 "\n"
}' "$AUDIT_TSV" > "$REVIEW_IN_INFUSE"

awk -F '\t' 'NR>1 && $9=="REVIEW_BEFORE_DELETE" {
  print $3 "\n  movie: " $4 "\n  note: " $10 "\n"
}' "$AUDIT_TSV" > "$REVIEW_BEFORE_DELETE"

awk -F '\t' 'NR>1 && $9=="MANUAL_REVIEW" {
  print $3 "\n  movie: " $4 "\n  note: " $10 "\n"
}' "$AUDIT_TSV" > "$MANUAL_REVIEW"

awk -F '\t' 'BEGIN {
  OFS="\t";
  print "folder","movie","note";
}
NR>1 && $9=="SAFE_TO_PLAN_CLEANUP" {
  print $3,$4,$10;
}' "$AUDIT_TSV" > "$SAFE_CLEANUP_TSV"

awk -F '\t' 'NR>1 && $9=="ADD_TO_MUX_QUEUE" { print $3 }' "$AUDIT_TSV" | sort -u > "$ADD_QUEUE_ALL"

tmp_current="$(mktemp "${TMPDIR:-/tmp}/film-current-queue.XXXXXX")"
awk -F '\t' '$0 !~ /^#/ && NF>=2 { print $2 }' "$QUEUE_FILE" | sort -u > "$tmp_current"
comm -23 "$ADD_QUEUE_ALL" "$tmp_current" > "$ADD_QUEUE_NEW"
rm -f "$tmp_current"

safe_count="$(awk 'NR>1 {count++} END {print count+0}' "$SAFE_CLEANUP_TSV")"
review_infuse_count="$(grep -c '^/Volumes/' "$REVIEW_IN_INFUSE" || true)"
review_before_count="$(grep -c '^/Volumes/' "$REVIEW_BEFORE_DELETE" || true)"
manual_count="$(grep -c '^/Volumes/' "$MANUAL_REVIEW" || true)"
add_all_count="$(wc -l < "$ADD_QUEUE_ALL" | tr -d ' ')"
add_new_count="$(wc -l < "$ADD_QUEUE_NEW" | tr -d ' ')"

{
  printf '# Cleanup And Queue Plan\n\n'
  printf -- '- Generated: `%s`\n' "$(date '+%Y-%m-%d %H:%M:%S')"
  printf -- '- Audit TSV: `%s`\n' "$AUDIT_TSV"
  printf -- '- Queue file: `%s`\n\n' "$QUEUE_FILE"
  printf '## Counts\n\n'
  printf -- '- SAFE_TO_PLAN_CLEANUP: `%s`\n' "$safe_count"
  printf -- '- REVIEW_IN_INFUSE: `%s`\n' "$review_infuse_count"
  printf -- '- REVIEW_BEFORE_DELETE: `%s`\n' "$review_before_count"
  printf -- '- MANUAL_REVIEW: `%s`\n' "$manual_count"
  printf -- '- ADD_TO_MUX_QUEUE total in audit: `%s`\n' "$add_all_count"
  printf -- '- ADD_TO_MUX_QUEUE new, not already in queue: `%s`\n\n' "$add_new_count"
  printf '## Files\n\n'
  printf -- '- Review in Infuse: `%s`\n' "$REVIEW_IN_INFUSE"
  printf -- '- Review before delete: `%s`\n' "$REVIEW_BEFORE_DELETE"
  printf -- '- Manual review: `%s`\n' "$MANUAL_REVIEW"
  printf -- '- Safe cleanup plan TSV: `%s`\n' "$SAFE_CLEANUP_TSV"
  printf -- '- Add to mux queue, all: `%s`\n' "$ADD_QUEUE_ALL"
  printf -- '- Add to mux queue, new only: `%s`\n' "$ADD_QUEUE_NEW"
} > "$SUMMARY_MD"

printf '%s\n' "$SUMMARY_MD"
