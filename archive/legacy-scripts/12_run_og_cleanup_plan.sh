#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAN_TSV="${PLAN_TSV:-}"
DRY_RUN="${DRY_RUN:-1}"
LOG_DIR="$WORKDIR/logs"
RUN_LOG="$LOG_DIR/og-cleanup-run-$(date '+%Y%m%d-%H%M%S').log"

mkdir -p "$LOG_DIR"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "$RUN_LOG"
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

find_latest_plan() {
  find "$WORKDIR/og-cleanup-plan" -maxdepth 1 -type f -name 'og_cleanup_cleanable_*.tsv' -print 2>/dev/null | sort | tail -n 1
}

shell_quote() {
  local first=1 arg
  for arg in "$@"; do
    if [[ "$first" -eq 1 ]]; then
      printf '"%s"' "$arg"
      first=0
    else
      printf ' "%s"' "$arg"
    fi
  done
  printf '\n'
}

run_or_echo() {
  if [[ "$DRY_RUN" == "1" ]]; then
    printf 'DRY-RUN: '
    shell_quote "$@"
  else
    "$@"
  fi
}

cleanup_one_folder() {
  local folder="$1"
  local expected_current="$2"
  local expected_target="$3"
  local item base parent target
  local -a current_movies=()
  local -a og_movies=()
  local -a subtitles=()
  local -a ignored=()
  local -a unexpected=()
  local -a subdirs=()

  [[ -d "$folder" ]] || { log "SKIP: folder missing: $folder"; return 0; }

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

  if [[ "${#current_movies[@]}" -ne 1 ]]; then
    log "SKIP: expected exactly one current movie, found ${#current_movies[@]}: $folder"
    return 0
  fi
  if [[ "${current_movies[0]}" != "$expected_current" ]]; then
    log "SKIP: current movie changed: $folder"
    log "  expected: $expected_current"
    log "  found: ${current_movies[0]}"
    return 0
  fi
  if [[ "${#og_movies[@]}" -lt 1 ]]; then
    log "SKIP: no OG movie remains: $folder"
    return 0
  fi
  if [[ "${#subdirs[@]}" -gt 0 ]]; then
    log "SKIP: subdirs remain: $folder"
    printf '%s\n' "${subdirs[@]}" | sed 's/^/  subdir: /' | tee -a "$RUN_LOG"
    return 0
  fi
  if [[ "${#unexpected[@]}" -gt 0 ]]; then
    log "SKIP: unexpected files remain: $folder"
    printf '%s\n' "${unexpected[@]}" | sed 's/^/  unexpected: /' | tee -a "$RUN_LOG"
    return 0
  fi

  parent="$(dirname "$folder")"
  target="$parent/$(basename "${current_movies[0]}")"
  if [[ "$target" != "$expected_target" ]]; then
    log "SKIP: target changed: $folder"
    log "  expected: $expected_target"
    log "  found: $target"
    return 0
  fi
  if [[ -e "$target" && "$target" != "${current_movies[0]}" ]]; then
    log "SKIP: parent target already exists: $target"
    return 0
  fi

  log "CLEAN: $folder"
  log "  delete OG movies: ${#og_movies[@]}"
  log "  delete subtitles: ${#subtitles[@]}"
  log "  delete ignored files: ${#ignored[@]}"
  log "  move: ${current_movies[0]} -> $target"

  local delete_file
  for delete_file in "${og_movies[@]+"${og_movies[@]}"}"; do
    run_or_echo rm -f "$delete_file" | tee -a "$RUN_LOG"
  done
  for delete_file in "${subtitles[@]+"${subtitles[@]}"}"; do
    run_or_echo rm -f "$delete_file" | tee -a "$RUN_LOG"
  done
  for delete_file in "${ignored[@]+"${ignored[@]}"}"; do
    run_or_echo rm -f "$delete_file" | tee -a "$RUN_LOG"
  done
  run_or_echo mv "${current_movies[0]}" "$target" | tee -a "$RUN_LOG"
  run_or_echo rmdir "$folder" | tee -a "$RUN_LOG"
}

main() {
  if [[ -z "$PLAN_TSV" ]]; then
    PLAN_TSV="$(find_latest_plan)"
  fi
  [[ -n "$PLAN_TSV" && -f "$PLAN_TSV" ]] || { log "ERROR: PLAN_TSV not found. Run 11_analyze_og_leftovers.sh first."; exit 1; }

  if [[ "$DRY_RUN" == "1" ]]; then
    log "DRY-RUN mode: no files will be deleted, moved, or renamed"
  else
    log "REAL RUN mode: files may be deleted and movies moved"
  fi
  log "Plan TSV: $PLAN_TSV"
  log "Log: $RUN_LOG"

  local folder current target og_count sub_count ignored_count og_movies
  local cleaned=0
  while IFS=$'\t' read -r folder current target og_count sub_count ignored_count og_movies; do
    [[ "$folder" != "folder" ]] || continue
    cleanup_one_folder "$folder" "$current" "$target"
    cleaned=$((cleaned + 1))
  done < "$PLAN_TSV"

  log "Done. Planned rows visited: $cleaned"
}

main "$@"
