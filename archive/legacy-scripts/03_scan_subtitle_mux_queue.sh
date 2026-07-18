#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$WORKDIR/logs"
QUEUE_FILE="${QUEUE_FILE:-$WORKDIR/subtitle_mux_queue.tsv}"
SCAN_LOG="$LOG_DIR/scan-subtitle-mux-queue.log"

mkdir -p "$LOG_DIR"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "$SCAN_LOG"
}

write_queue_header() {
  {
    printf '# subtitle mux queue\n'
    printf '# generated_at\t%s\n' "$(timestamp)"
    printf '# scan_roots\t/Volumes/看\t/Volumes/导演们\t/Volumes/分类\n'
    printf '# columns: status<TAB>folder_path<TAB>message\n'
    printf '# status: PENDING, DONE, FAILED\n'
  } > "$QUEUE_FILE"
}

main() {
  : > "$SCAN_LOG"

  local roots=("$@")
  if ((${#roots[@]} == 0)); then
    roots=(/Volumes/看 /Volumes/导演们 /Volumes/分类)
  fi

  write_queue_header
  log "Writing queue to $QUEUE_FILE"

  local tmp
  tmp="$LOG_DIR/scan-candidates.$$"
  : > "$tmp"

  local root
  for root in "${roots[@]}"; do
    if [[ ! -d "$root" ]]; then
      log "Skipping missing root: $root"
      continue
    fi

    log "Scanning root: $root"
    find "$root" \
      \( -path '*/.Spotlight-V100/*' -o -path '*/.Trashes/*' -o -path '*/.fseventsd/*' -o -path '*/#recycle/*' -o -path '*/@eaDir/*' \) -prune \
      -o -type f \( -iname '*.mkv' -o -iname '*.srt' -o -iname '*.ass' -o -iname '*.ssa' \) -print \
      >> "$tmp"
  done

  awk '
    function dirname(path) {
      sub(/\/[^\/]*$/, "", path)
      return path
    }
    function basename(path) {
      sub(/^.*\//, "", path)
      return path
    }
    function lower(s) {
      return tolower(s)
    }
    {
      dir = dirname($0)
      name = basename($0)
      lname = lower(name)
      dirs[dir] = 1
      if (lname ~ /\.mkv$/ && name !~ /^OG\./) {
        mkv_count[dir] += 1
      } else if (lname ~ /\.(srt|ass|ssa)$/) {
        sub_count[dir] += 1
      }
    }
    END {
      for (dir in dirs) {
        if (mkv_count[dir] == 1 && sub_count[dir] >= 1) {
          print dir
        }
      }
    }
  ' "$tmp" | sort | while IFS= read -r folder; do
    printf 'PENDING\t%s\t\n' "$folder" >> "$QUEUE_FILE"
  done

  local files eligible
  files="$(wc -l < "$tmp" | tr -d ' ')"
  eligible="$(awk -F '\t' '$1 == "PENDING" { count += 1 } END { print count + 0 }' "$QUEUE_FILE")"
  : > "$tmp"

  log "Candidate media/subtitle files: $files"
  log "Eligible folders: $eligible"
  log "Done"
}

main "$@"
