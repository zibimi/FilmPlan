#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$WORKDIR/logs"
QUEUE_FILE="${QUEUE_FILE:-$WORKDIR/subtitle_mux_queue.tsv}"
RUN_LOG="$LOG_DIR/run-subtitle-mux-queue.log"
LOCAL_MKVMERGE="$WORKDIR/tools/MKVToolNix.app/Contents/MacOS/mkvmerge"
LOCAL_MKVPROPEDIT="$WORKDIR/tools/MKVToolNix.app/Contents/MacOS/mkvpropedit"
KNOWN_MKVMERGE="/Users/milou/Documents/电影整理计划/tools/MKVToolNix.app/Contents/MacOS/mkvmerge"
KNOWN_MKVPROPEDIT="/Users/milou/Documents/电影整理计划/tools/MKVToolNix.app/Contents/MacOS/mkvpropedit"
MKVMERGE="${MKVMERGE:-}"
MKVPROPEDIT="${MKVPROPEDIT:-}"
DRY_RUN="${DRY_RUN:-0}"
RUN_LIMIT="${RUN_LIMIT:-0}"
PROCESSED_COUNT=0

mkdir -p "$LOG_DIR"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "$RUN_LOG"
}

shell_quote_command() {
  printf '%q ' "$@"
  printf '\n'
}

queue_update() {
  local line_no="$1"
  local status="$2"
  local folder="$3"
  local message="$4"
  local tmp="$QUEUE_FILE.tmp.$$"

  awk -v line_no="$line_no" -v status="$status" -v folder="$folder" -v message="$message" '
    NR == line_no { print status "\t" folder "\t" message; next }
    { print }
  ' "$QUEUE_FILE" > "$tmp"
  mv "$tmp" "$QUEUE_FILE"
}

fail_current() {
  local message="$1"
  log "ERROR: $message"
  if [[ "$DRY_RUN" != "1" && -n "${CURRENT_LINE_NO:-}" && -n "${CURRENT_FOLDER:-}" ]]; then
    queue_update "$CURRENT_LINE_NO" "FAILED" "$CURRENT_FOLDER" "$message"
  fi
  exit 1
}

is_subtitle() {
  case "$1" in
    *.[sS][rR][tT]|*.[aA][sS][sS]|*.[sS][sS][aA]) return 0 ;;
    *) return 1 ;;
  esac
}

is_mkv() {
  case "$1" in
    *.[mM][kK][vV]) return 0 ;;
    *) return 1 ;;
  esac
}

subtitle_lang() {
  local lower
  lower="$(basename "$1" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    *".zh."*|*".chs."*|*".cht."*|*".sc."*|*".tc."*|*"中文"*|*"简体"*|*"繁体"*|*"簡體"*|*"繁體"*) printf 'chi' ;;
    *".en."*|*".eng."*|*"english"*|*"英文"*) printf 'eng' ;;
    *) printf 'und' ;;
  esac
}

subtitle_name() {
  case "$(subtitle_lang "$1")" in
    chi) printf 'Chinese' ;;
    eng) printf 'English' ;;
    *) printf 'Subtitle' ;;
  esac
}

subtitle_charset() {
  local subtitle="$1"
  case "$subtitle" in
    *.[sS][rR][tT])
      if iconv -f UTF-8 -t UTF-8 "$subtitle" >/dev/null 2>&1; then
        printf 'UTF-8\n'
        return 0
      fi
      if iconv -f GB18030 -t UTF-8 "$subtitle" >/dev/null 2>&1; then
        printf 'GB18030\n'
        return 0
      fi
      if iconv -f UTF-16LE -t UTF-8 "$subtitle" >/dev/null 2>&1; then
        printf 'UTF-16LE\n'
        return 0
      fi
      if iconv -f UTF-16 -t UTF-8 "$subtitle" >/dev/null 2>&1; then
        printf 'UTF-16\n'
        return 0
      fi
      if iconv -f BIG5 -t UTF-8 "$subtitle" >/dev/null 2>&1; then
        printf 'BIG5\n'
        return 0
      fi
      if iconv -f CP950 -t UTF-8 "$subtitle" >/dev/null 2>&1; then
        printf 'CP950\n'
        return 0
      fi
      return 1
      ;;
    *)
      printf '\n'
      return 0
      ;;
  esac
}

file_size_bytes() {
  stat -f '%z' "$1"
}

bytes_to_gib() {
  awk -v bytes="$1" 'BEGIN { printf "%.2f GiB", bytes / 1024 / 1024 / 1024 }'
}

capture_network_snapshot() {
  local target="$1"
  netstat -ibn > "$target" 2>/dev/null || true
}

network_totals() {
  local snapshot="$1"
  awk '
    NR > 1 && $1 ~ /^en[0-9]+$/ {
      ibytes += $7
      obytes += $10
    }
    END {
      printf "%s %s\n", ibytes + 0, obytes + 0
    }
  ' "$snapshot"
}

resolve_tool() {
  local current="$1"
  local local_path="$2"
  local tool_name="$3"
  local known_path="${4:-}"

  if [[ -n "$current" && -x "$current" ]]; then
    printf '%s\n' "$current"
  elif command -v "$tool_name" >/dev/null 2>&1; then
    command -v "$tool_name"
  elif [[ -x "$local_path" ]]; then
    printf '%s\n' "$local_path"
  elif [[ -n "$known_path" && -x "$known_path" ]]; then
    printf '%s\n' "$known_path"
  else
    return 1
  fi
}

resolve_tool_or_name_for_dry_run() {
  local current="$1"
  local local_path="$2"
  local tool_name="$3"
  local known_path="${4:-}"
  local resolved

  if resolved="$(resolve_tool "$current" "$local_path" "$tool_name" "$known_path")"; then
    printf '%s\n' "$resolved"
  elif [[ "$DRY_RUN" == "1" ]]; then
    printf '[%s] DRY-RUN WARNING: %s not found. Formal run will fail unless it is installed or explicitly provided.\n' "$(timestamp)" "$tool_name" | tee -a "$RUN_LOG" >&2
    printf '%s\n' "$tool_name"
  else
    return 1
  fi
}

set_subtitle_default_flags() {
  local mkv="$1"
  shift
  local -a appended_defaults=("$@")

  local info
  info="$("$MKVMERGE" -i "$mkv")"

  local total_tracks
  total_tracks="$(printf '%s\n' "$info" | awk '/^Track ID [0-9]+:/ { count += 1 } END { print count + 0 }')"
  ((total_tracks > 0)) || fail_current "could not inspect output tracks: $mkv"

  local -a edit_cmd=("$MKVPROPEDIT" "$mkv")
  local id track_no
  while IFS= read -r id; do
    track_no=$((id + 1))
    edit_cmd+=("--edit" "track:$track_no" "--set" "flag-default=0")
  done < <(printf '%s\n' "$info" | awk '/^Track ID [0-9]+: subtitles / { gsub(":", "", $3); print $3 }')

  local first_appended_track
  first_appended_track=$((total_tracks - ${#appended_defaults[@]} + 1))
  local i default_flag appended_track
  for i in "${!appended_defaults[@]}"; do
    default_flag="${appended_defaults[$i]}"
    appended_track=$((first_appended_track + i))
    if [[ "$default_flag" == "yes" ]]; then
      edit_cmd+=("--edit" "track:$appended_track" "--set" "flag-default=1")
    fi
  done

  log "Updating subtitle default flags"
  if ! "${edit_cmd[@]}" >> "$RUN_LOG" 2>&1; then
    fail_current "mkvpropedit failed while updating subtitle default flags for $mkv"
  fi
}

find_first_pending() {
  awk -F '\t' '
    $0 !~ /^#/ && $1 == "PENDING" {
      print NR "\t" $2
      exit
    }
  ' "$QUEUE_FILE"
}

process_folder() {
  local folder="$1"
  local movie=""
  local mkv_count=0
  local item base
  local -a subtitles=()

  [[ -d "$folder" ]] || fail_current "folder does not exist: $folder"

  while IFS= read -r -d '' item; do
    base="$(basename "$item")"
    if is_mkv "$item" && [[ "$base" != OG.* ]]; then
      movie="$item"
      ((mkv_count += 1))
    elif is_subtitle "$item"; then
      subtitles+=("$item")
    fi
  done < <(find "$folder" -maxdepth 1 -type f -print0 | sort -z)

  [[ "$mkv_count" -eq 1 ]] || fail_current "expected exactly one non-OG MKV, found $mkv_count in $folder"
  ((${#subtitles[@]} > 0)) || fail_current "no subtitle files found in $folder"

  local movie_base og_movie tmp_output net_before net_after
  movie_base="$(basename "$movie")"
  og_movie="$folder/OG.$movie_base"
  tmp_output="$folder/.$movie_base.muxing.mkv"
  net_before="$LOG_DIR/net-before-$(date '+%Y%m%d-%H%M%S').txt"
  net_after="$LOG_DIR/net-after-$(date '+%Y%m%d-%H%M%S').txt"

  [[ ! -e "$og_movie" ]] || fail_current "OG file already exists: $og_movie"
  [[ ! -e "$tmp_output" ]] || fail_current "temporary output already exists: $tmp_output"

  local input_size estimated_total
  input_size="$(file_size_bytes "$movie")"
  estimated_total=$((input_size * 2))

  log "Folder: $folder"
  log "Movie: $movie"
  log "Subtitles: ${#subtitles[@]}"
  log "Estimated NAS SMB traffic: about $estimated_total bytes ($(bytes_to_gib "$estimated_total")), plus overhead"

  local -a cmd=("$MKVMERGE" "--output" "$tmp_output" "$movie")
  local subtitle lang name default_flag charset
  local -a appended_defaults=()
  local has_default_chi=0

  for subtitle in "${subtitles[@]}"; do
    if ! charset="$(subtitle_charset "$subtitle")"; then
      fail_current "subtitle encoding is not supported: $subtitle"
    fi

    lang="$(subtitle_lang "$subtitle")"
    if [[ "$lang" == "und" && ( "$charset" == "GB18030" || "$charset" == "BIG5" || "$charset" == "CP950" || "$charset" == "UTF-16LE" || "$charset" == "UTF-16" ) ]]; then
      lang="chi"
    fi
    case "$lang" in
      chi) name="Chinese" ;;
      eng) name="English" ;;
      *) name="Subtitle" ;;
    esac
    default_flag="no"
    if [[ "$lang" == "chi" && "$has_default_chi" -eq 0 ]]; then
      default_flag="yes"
      has_default_chi=1
    fi
    appended_defaults+=("$default_flag")

    if [[ -n "$charset" && "$charset" != "UTF-8" ]]; then
      cmd+=("--sub-charset" "0:$charset")
    fi
    cmd+=("--language" "0:$lang" "--track-name" "0:$name" "--default-track" "0:$default_flag" "$subtitle")
  done

  capture_network_snapshot "$net_before"
  read -r net_in_before net_out_before < <(network_totals "$net_before")
  local start_epoch
  start_epoch="$(date '+%s')"

  log "Running mkvmerge"
  if [[ "$DRY_RUN" == "1" ]]; then
    log "DRY-RUN: would run command:"
    shell_quote_command "${cmd[@]}" | tee -a "$RUN_LOG"
    log "DRY-RUN: would then update subtitle default flags on $tmp_output"
    log "DRY-RUN: would rename original to $og_movie"
    log "DRY-RUN: would rename muxed file to $movie"
    log "DRY-RUN: queue would be updated to DONE on success"
    PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
    return 0
  fi

  set +e
  "${cmd[@]}" >> "$RUN_LOG" 2>&1
  local mkvmerge_status=$?
  set -e
  if [[ "$mkvmerge_status" -eq 1 ]]; then
    log "mkvmerge completed with warnings; continuing"
  elif [[ "$mkvmerge_status" -ne 0 ]]; then
    fail_current "mkvmerge failed for $folder with exit code $mkvmerge_status"
  fi

  set_subtitle_default_flags "$tmp_output" "${appended_defaults[@]}"

  log "Renaming original to OG prefix"
  if ! mv "$movie" "$og_movie"; then
    fail_current "could not rename original to $og_movie"
  fi

  log "Renaming muxed file to original movie filename"
  if ! mv "$tmp_output" "$movie"; then
    log "Attempting rollback because final rename failed"
    mv "$og_movie" "$movie" || true
    fail_current "could not rename muxed file to $movie"
  fi

  local end_epoch output_size elapsed net_in_after net_out_after net_in_delta net_out_delta
  end_epoch="$(date '+%s')"
  output_size="$(file_size_bytes "$movie")"
  elapsed=$((end_epoch - start_epoch))

  capture_network_snapshot "$net_after"
  read -r net_in_after net_out_after < <(network_totals "$net_after")
  net_in_delta=$((net_in_after - net_in_before))
  net_out_delta=$((net_out_after - net_out_before))

  log "SUCCESS: $folder"
  log "Output size: $output_size bytes ($(bytes_to_gib "$output_size"))"
  log "Elapsed seconds: $elapsed"
  log "Approx en* network received: $net_in_delta bytes ($(bytes_to_gib "$net_in_delta"))"
  log "Approx en* network sent: $net_out_delta bytes ($(bytes_to_gib "$net_out_delta"))"
  queue_update "$CURRENT_LINE_NO" "DONE" "$CURRENT_FOLDER" "completed $(timestamp)"
  PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
}

main() {
  : >> "$RUN_LOG"

  [[ -f "$QUEUE_FILE" ]] || fail_current "queue file does not exist: $QUEUE_FILE"
  if [[ "$DRY_RUN" == "1" ]]; then
    log "DRY-RUN mode: no media files, queue rows, or names will be changed"
  fi

  MKVMERGE="$(resolve_tool_or_name_for_dry_run "$MKVMERGE" "$LOCAL_MKVMERGE" "mkvmerge" "$KNOWN_MKVMERGE")" || fail_current "mkvmerge not found. Install MKVToolNix or set MKVMERGE=/path/to/mkvmerge"
  MKVPROPEDIT="$(resolve_tool_or_name_for_dry_run "$MKVPROPEDIT" "$LOCAL_MKVPROPEDIT" "mkvpropedit" "$KNOWN_MKVPROPEDIT")" || fail_current "mkvpropedit not found. Install MKVToolNix or set MKVPROPEDIT=/path/to/mkvpropedit"
  log "Using mkvmerge: $MKVMERGE"
  log "Using mkvpropedit: $MKVPROPEDIT"

  local pending
  while true; do
    pending="$(find_first_pending || true)"
    if [[ -z "$pending" ]]; then
      log "No PENDING folders left in $QUEUE_FILE"
      exit 0
    fi

    CURRENT_LINE_NO="${pending%%$'\t'*}"
    CURRENT_FOLDER="${pending#*$'\t'}"

    log "Next queue line: $CURRENT_LINE_NO"
    process_folder "$CURRENT_FOLDER"
    if [[ "$DRY_RUN" == "1" ]]; then
      log "DRY-RUN: stopping after first PENDING folder"
      exit 0
    fi
    if [[ "$RUN_LIMIT" -gt 0 && "$PROCESSED_COUNT" -ge "$RUN_LIMIT" ]]; then
      log "RUN_LIMIT reached: $RUN_LIMIT"
      exit 0
    fi
  done
}

main "$@"
