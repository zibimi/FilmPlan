#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESCAN_TSV="${RESCAN_TSV:-}"
QUEUE_FILE="${QUEUE_FILE:-$WORKDIR/mux_clean_queue.tsv}"
LOG_DIR="$WORKDIR/logs"
RUN_LOG="$LOG_DIR/prepare-mux-clean-queue-$(date '+%Y%m%d-%H%M%S').log"

mkdir -p "$LOG_DIR"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "$RUN_LOG"
}

find_latest_rescan() {
  find "$WORKDIR/rescan-plan" -maxdepth 1 -type f -name 'movie_subtitle_candidates_*.tsv' -print 2>/dev/null | sort | tail -n 1
}

is_movie() {
  case "$1" in
    *.[mM][kK][vV]|*.[mM][pP]4|*.[aA][vV][iI]) return 0 ;;
    *) return 1 ;;
  esac
}

target_for_movie() {
  local movie="$1"
  local folder parent base stem
  folder="$(dirname "$movie")"
  parent="$(dirname "$folder")"
  base="$(basename "$movie")"
  stem="${base%.*}"
  printf '%s/%s.mkv\n' "$parent" "$stem"
}

main() {
  if [[ -z "$RESCAN_TSV" ]]; then
    RESCAN_TSV="$(find_latest_rescan)"
  fi
  [[ -n "$RESCAN_TSV" && -f "$RESCAN_TSV" ]] || { log "ERROR: no rescan candidate TSV found. Run 10_scan_movie_subtitle_candidates.sh first."; exit 1; }

  local backup=""
  if [[ -f "$QUEUE_FILE" ]]; then
    backup="$QUEUE_FILE.before-prepare-$(date '+%Y%m%d-%H%M%S').tsv"
    cp "$QUEUE_FILE" "$backup"
    log "Backed up existing queue: $backup"
  fi

  printf '# status\tfolder\tmessage\n' > "$QUEUE_FILE"

  local folder movie subtitle_count subdir_count other_file_count target
  local added=0 skipped=0
  while IFS=$'\t' read -r folder movie subtitle_count subdir_count other_file_count; do
    [[ "$folder" != "folder" ]] || continue
    if [[ "$folder" == *"/#recycle/"* || "$folder" == *"/#recycle" ]]; then
      skipped=$((skipped + 1))
      log "SKIP #recycle: $folder"
      continue
    fi
    if [[ ! -d "$folder" ]]; then
      skipped=$((skipped + 1))
      log "SKIP missing folder: $folder"
      continue
    fi
    if [[ ! -f "$movie" ]] || ! is_movie "$movie"; then
      skipped=$((skipped + 1))
      log "SKIP missing/non-movie: $movie"
      continue
    fi
    if find "$folder" -maxdepth 1 -type f -name 'OG.*' -print -quit | grep -q .; then
      skipped=$((skipped + 1))
      log "SKIP folder already has OG file: $folder"
      continue
    fi
    target="$(target_for_movie "$movie")"
    if [[ -e "$target" ]]; then
      skipped=$((skipped + 1))
      log "SKIP parent target exists: $target"
      continue
    fi
    printf 'PENDING\t%s\tprepared from %s\n' "$folder" "$(basename "$RESCAN_TSV")" >> "$QUEUE_FILE"
    added=$((added + 1))
  done < "$RESCAN_TSV"

  log "Queue: $QUEUE_FILE"
  log "Added PENDING rows: $added"
  log "Skipped rows: $skipped"
  log "Log: $RUN_LOG"
}

main "$@"
