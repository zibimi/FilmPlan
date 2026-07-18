#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$WORKDIR/og-cleanup-plan"
LOG_DIR="$WORKDIR/logs"
TS="$(date '+%Y%m%d-%H%M%S')"

ROOTS="${ROOTS:-/Volumes/导演们
/Volumes/分类}"

LOG_FILE="$LOG_DIR/og-cleanup-analyze-$TS.log"
CLEANABLE_TSV="$OUT_DIR/og_cleanup_cleanable_$TS.tsv"
REVIEW_TSV="$OUT_DIR/og_cleanup_review_$TS.tsv"
SUMMARY_MD="$OUT_DIR/og_cleanup_summary_$TS.md"

mkdir -p "$OUT_DIR" "$LOG_DIR"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "$LOG_FILE"
}

is_movie() {
  case "$1" in
    *.[mM][kK][vV]|*.[mM][pP]4|*.[aA][vV][iI]) return 0 ;;
    *) return 1 ;;
  esac
}

is_subtitle() {
  case "$1" in
    *.[sS][rR][tT]|*.[aA][sS][sS]|*.[sS][sS][aA]|*.[iI][dD][xX]|*.[sS][uU][bB]) return 0 ;;
    *) return 1 ;;
  esac
}

is_ignored_file() {
  case "$(basename "$1")" in
    .DS_Store|Thumbs.db|desktop.ini|._*) return 0 ;;
    *) return 1 ;;
  esac
}

join_paths() {
  local IFS='|'
  printf '%s' "$*"
}

count_lines() {
  awk 'NR>1 {count++} END {print count+0}' "$1"
}

inspect_folder() {
  local folder="$1"
  local item base parent target reason details
  local -a current_movies=()
  local -a og_movies=()
  local -a subtitles=()
  local -a ignored=()
  local -a unexpected=()
  local -a subdirs=()

  while IFS= read -r -d '' item; do
    base="$(basename "$item")"
    if [[ -d "$item" ]]; then
      subdirs+=("$item")
    elif is_ignored_file "$item"; then
      ignored+=("$item")
    elif is_movie "$item"; then
      case "$base" in
        OG.*) og_movies+=("$item") ;;
        .*".muxing.mkv"|*".muxing.mkv.abandoned."*|*".muxing.mkv.failed."*) unexpected+=("$item") ;;
        *) current_movies+=("$item") ;;
      esac
    elif is_subtitle "$item"; then
      subtitles+=("$item")
    else
      unexpected+=("$item")
    fi
  done < <(find "$folder" -mindepth 1 -maxdepth 1 -print0 2>/dev/null | sort -z)

  if [[ "${#og_movies[@]}" -eq 0 ]]; then
    return 0
  fi

  parent="$(dirname "$folder")"
  target=""
  reason=""
  details=""

  if [[ "${#current_movies[@]}" -ne 1 ]]; then
    reason="CURRENT_MOVIE_COUNT_${#current_movies[@]}"
    details="current_movies=$(join_paths "${current_movies[@]:-}")"
  elif [[ "${#subdirs[@]}" -gt 0 ]]; then
    reason="HAS_SUBDIRS"
    details="$(join_paths "${subdirs[@]}")"
  elif [[ "${#unexpected[@]}" -gt 0 ]]; then
    reason="HAS_UNEXPECTED_FILES"
    details="$(join_paths "${unexpected[@]}")"
  else
    target="$parent/$(basename "${current_movies[0]}")"
    if [[ -e "$target" && "$target" != "${current_movies[0]}" ]]; then
      reason="PARENT_TARGET_EXISTS"
      details="$target"
    fi
  fi

  if [[ -z "$reason" ]]; then
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$folder" \
      "${current_movies[0]}" \
      "$target" \
      "${#og_movies[@]}" \
      "${#subtitles[@]}" \
      "${#ignored[@]}" \
      "$(join_paths "${og_movies[@]}")" >> "$CLEANABLE_TSV"
  else
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$folder" \
      "$reason" \
      "${#current_movies[@]}" \
      "${#og_movies[@]}" \
      "${#subtitles[@]}" \
      "${#subdirs[@]}" \
      "${#unexpected[@]}" \
      "$details" >> "$REVIEW_TSV"
  fi
}

write_summary() {
  local og_files og_folders cleanable review by_reason
  og_files="$(find_from_roots -type f -name 'OG.*' | wc -l | tr -d ' ')"
  og_folders="$(find_from_roots -type f -name 'OG.*' -exec dirname {} \; | sort -u | wc -l | tr -d ' ')"
  cleanable="$(count_lines "$CLEANABLE_TSV")"
  review="$(count_lines "$REVIEW_TSV")"
  by_reason="$(awk -F '\t' 'NR>1 {count[$2]++} END {for (r in count) print r "\t" count[r]}' "$REVIEW_TSV" | sort)"

  {
    printf '# OG Cleanup Analysis\n\n'
    printf -- '- Generated: `%s`\n' "$(timestamp)"
    printf -- '- Roots:\n'
    while IFS= read -r root; do
      [[ -n "$root" ]] && printf '  - `%s`\n' "$root"
    done <<< "$ROOTS"
    printf '\n## Counts\n\n'
    printf -- '- OG files found: `%s`\n' "$og_files"
    printf -- '- Folders with OG files: `%s`\n' "$og_folders"
    printf -- '- Cleanable folders: `%s`\n' "$cleanable"
    printf -- '- Review folders: `%s`\n\n' "$review"
    printf '## Review Reasons\n\n'
    if [[ -n "$by_reason" ]]; then
      while IFS=$'\t' read -r reason count; do
        [[ -n "$reason" ]] && printf -- '- `%s`: `%s`\n' "$reason" "$count"
      done <<< "$by_reason"
    else
      printf -- '- none\n'
    fi
    printf '\n## Files\n\n'
    printf -- '- Cleanable TSV: `%s`\n' "$CLEANABLE_TSV"
    printf -- '- Review TSV: `%s`\n' "$REVIEW_TSV"
    printf -- '- Log: `%s`\n' "$LOG_FILE"
  } > "$SUMMARY_MD"
}

find_from_roots() {
  local -a roots=()
  local root
  while IFS= read -r root; do
    [[ -n "$root" ]] && roots+=("$root")
  done <<< "$ROOTS"
  find "${roots[@]}" "$@" 2>/dev/null
}

main() {
  printf 'folder\tcurrent_movie\ttarget_movie\tog_movie_count\tsubtitle_count\tignored_count\tog_movies\n' > "$CLEANABLE_TSV"
  printf 'folder\treason\tcurrent_movie_count\tog_movie_count\tsubtitle_count\tsubdir_count\tunexpected_count\tdetails\n' > "$REVIEW_TSV"

  log "Scanning OG leftovers"
  while IFS= read -r folder; do
    inspect_folder "$folder"
  done < <(find_from_roots -type f -name 'OG.*' -exec dirname {} \; | sort -u)

  write_summary
  log "Summary: $SUMMARY_MD"
  log "Cleanable: $CLEANABLE_TSV"
  log "Review: $REVIEW_TSV"
}

main "$@"
