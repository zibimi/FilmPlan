#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAN_TSV="${PLAN_TSV:-}"
DRY_RUN="${DRY_RUN:-1}"
LOG_DIR="$WORKDIR/logs"
RUN_LOG="$LOG_DIR/safe-cleanup-$(date '+%Y%m%d-%H%M%S').log"

mkdir -p "$LOG_DIR"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "$RUN_LOG"
}

is_mkv() {
  case "$1" in
    *.[mM][kK][vV]) return 0 ;;
    *) return 1 ;;
  esac
}

is_subtitle() {
  case "$1" in
    *.[sS][rR][tT]|*.[aA][sS][sS]|*.[sS][sS][aA]) return 0 ;;
    *) return 1 ;;
  esac
}

find_latest_plan() {
  find "$WORKDIR/cleanup-plan" -maxdepth 1 -type f -name 'safe_cleanup_plan_*.tsv' -print 2>/dev/null | sort | tail -n 1
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
  local expected_movie="$2"
  local item base parent target
  local -a current_movies=()
  local -a og_movies=()
  local -a subtitles=()
  local -a allowed_extras=()
  local -a unexpected=()

  [[ -d "$folder" ]] || { log "SKIP: folder missing: $folder"; return 0; }

  while IFS= read -r -d '' item; do
    base="$(basename "$item")"
    if is_mkv "$item"; then
      case "$base" in
        OG.*) og_movies+=("$item") ;;
        .*".muxing.mkv"|*".muxing.mkv.abandoned."*|*".muxing.mkv.failed."*) unexpected+=("$item") ;;
        *) current_movies+=("$item") ;;
      esac
    elif is_subtitle "$item"; then
      subtitles+=("$item")
    else
      case "$base" in
        .DS_Store|Thumbs.db) allowed_extras+=("$item") ;;
        *) unexpected+=("$item") ;;
      esac
    fi
  done < <(find "$folder" -maxdepth 1 -type f -print0 | sort -z)

  if [[ "${#current_movies[@]}" -ne 1 ]]; then
    log "SKIP: expected exactly one current MKV, found ${#current_movies[@]}: $folder"
    return 0
  fi
  if [[ "${#og_movies[@]}" -lt 1 ]]; then
    log "SKIP: expected at least one OG.* MKV: $folder"
    return 0
  fi
  if [[ "${current_movies[0]}" != "$expected_movie" ]]; then
    log "SKIP: current MKV differs from audit movie: folder=$folder current=${current_movies[0]} expected=$expected_movie"
    return 0
  fi
  if [[ "${#unexpected[@]}" -gt 0 ]]; then
    log "SKIP: unexpected files remain in folder: $folder"
    printf '%s\n' "${unexpected[@]}" | sed 's/^/  unexpected: /' | tee -a "$RUN_LOG"
    return 0
  fi

  parent="$(dirname "$folder")"
  target="$parent/$(basename "${current_movies[0]}")"
  if [[ -e "$target" && "$target" != "${current_movies[0]}" ]]; then
    log "SKIP: parent target already exists: $target"
    return 0
  fi

  log "CLEANUP CANDIDATE: $folder"
  log "  move movie: ${current_movies[0]} -> $target"
  log "  delete OG movies: ${#og_movies[@]}"
  log "  delete subtitles: ${#subtitles[@]}"
  log "  delete allowed extras: ${#allowed_extras[@]}"

  local delete_file
  for delete_file in "${og_movies[@]}"; do
    run_or_echo rm -f "$delete_file" | tee -a "$RUN_LOG"
  done
  for delete_file in "${subtitles[@]}"; do
    run_or_echo rm -f "$delete_file" | tee -a "$RUN_LOG"
  done
  for delete_file in "${allowed_extras[@]:-}"; do
    [[ -n "$delete_file" ]] || continue
    run_or_echo rm -f "$delete_file" | tee -a "$RUN_LOG"
  done

  if [[ "${current_movies[0]}" != "$target" ]]; then
    run_or_echo mv "${current_movies[0]}" "$target" | tee -a "$RUN_LOG"
  fi
  run_or_echo rmdir "$folder" | tee -a "$RUN_LOG"
}

main() {
  if [[ -z "$PLAN_TSV" ]]; then
    PLAN_TSV="$(find_latest_plan)"
  fi
  [[ -n "$PLAN_TSV" && -f "$PLAN_TSV" ]] || { log "ERROR: PLAN_TSV not found. Run 07_prepare_cleanup_and_queue_plan.sh first."; exit 1; }

  if [[ "$DRY_RUN" == "1" ]]; then
    log "DRY-RUN mode: no files will be deleted, moved, or renamed"
  else
    log "REAL RUN mode: files may be deleted and movies moved"
  fi
  log "Plan TSV: $PLAN_TSV"
  log "Log: $RUN_LOG"

  local folder movie note
  while IFS=$'\t' read -r folder movie note; do
    [[ "$folder" != "folder" ]] || continue
    cleanup_one_folder "$folder" "$movie"
  done < "$PLAN_TSV"

  log "Done"
}

main "$@"
