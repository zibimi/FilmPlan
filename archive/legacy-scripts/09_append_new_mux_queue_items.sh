#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUEUE_FILE="${QUEUE_FILE:-$WORKDIR/subtitle_mux_queue.tsv}"
ADD_LIST="${ADD_LIST:-}"
DRY_RUN="${DRY_RUN:-1}"
TS="$(date '+%Y%m%d-%H%M%S')"

find_latest_add_list() {
  find "$WORKDIR/cleanup-plan" -maxdepth 1 -type f -name 'add_to_mux_queue_new_*.txt' -print 2>/dev/null | sort | tail -n 1
}

if [[ -z "$ADD_LIST" ]]; then
  ADD_LIST="$(find_latest_add_list)"
fi

[[ -f "$QUEUE_FILE" ]] || { printf 'ERROR: queue file not found: %s\n' "$QUEUE_FILE" >&2; exit 1; }
[[ -n "$ADD_LIST" && -f "$ADD_LIST" ]] || { printf 'ERROR: add list not found. Run 07_prepare_cleanup_and_queue_plan.sh first.\n' >&2; exit 1; }

tmp_existing="$(mktemp "${TMPDIR:-/tmp}/film-existing-queue.XXXXXX")"
tmp_new="$(mktemp "${TMPDIR:-/tmp}/film-new-queue.XXXXXX")"
awk -F '\t' '$0 !~ /^#/ && NF>=2 { print $2 }' "$QUEUE_FILE" | sort -u > "$tmp_existing"
sort -u "$ADD_LIST" | comm -23 - "$tmp_existing" > "$tmp_new"

count="$(wc -l < "$tmp_new" | tr -d ' ')"
printf 'Queue file: %s\n' "$QUEUE_FILE"
printf 'Add list: %s\n' "$ADD_LIST"
printf 'New rows to append: %s\n' "$count"

if [[ "$count" -eq 0 ]]; then
  rm -f "$tmp_existing" "$tmp_new"
  exit 0
fi

if [[ "$DRY_RUN" == "1" ]]; then
  printf 'DRY-RUN: would append these folders as PENDING:\n'
  sed 's/^/  /' "$tmp_new"
  rm -f "$tmp_existing" "$tmp_new"
  exit 0
fi

backup="$QUEUE_FILE.before-add-cleanup-audit-$TS.tsv"
cp "$QUEUE_FILE" "$backup"
{
  printf '# appended_from_cleanup_audit\t%s\n' "$(date '+%Y-%m-%d %H:%M:%S')"
  while IFS= read -r folder; do
    [[ -n "$folder" ]] || continue
    printf 'PENDING\t%s\tadded from cleanup audit %s\n' "$folder" "$TS"
  done < "$tmp_new"
} >> "$QUEUE_FILE"

rm -f "$tmp_existing" "$tmp_new"
printf 'Backup: %s\n' "$backup"
printf 'Appended rows: %s\n' "$count"
