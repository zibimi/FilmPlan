#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$WORKDIR/rescan-plan"
LOG_DIR="$WORKDIR/logs"
TS="$(date '+%Y%m%d-%H%M%S')"

ROOTS="${ROOTS:-/Volumes/导演们
/Volumes/分类}"
DRY_RUN="${DRY_RUN:-1}"

SCAN_LOG="$LOG_DIR/rescan-movie-subtitle-candidates-$TS.log"
CANDIDATE_TSV="$OUT_DIR/movie_subtitle_candidates_$TS.tsv"
PLANNED_MOVES_TSV="$OUT_DIR/subtitle_moves_$TS.tsv"
SKIPPED_SUBDIRS_TSV="$OUT_DIR/skipped_subdirs_$TS.tsv"
OTHER_CASES_TSV="$OUT_DIR/other_cases_$TS.tsv"
SUMMARY_MD="$OUT_DIR/rescan_summary_$TS.md"

mkdir -p "$OUT_DIR" "$LOG_DIR"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "$SCAN_LOG"
}

is_movie() {
  case "$1" in
    *.[mM][kK][vV]|*.[mM][pP]4|*.[aA][vV][iI]) return 0 ;;
    *) return 1 ;;
  esac
}

is_subtitle() {
  case "$1" in
    *.[sS][rR][tT]|*.[aA][sS][sS]|*.[sS][sS][aA]) return 0 ;;
    *) return 1 ;;
  esac
}

is_ignored_file() {
  case "$(basename "$1")" in
    .DS_Store|Thumbs.db|desktop.ini|._*) return 0 ;;
    *) return 1 ;;
  esac
}

is_feature_subdir() {
  local lower
  lower="$(basename "$1" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    *花絮*|*特典*|*特辑*|*特輯*|*幕后*|*幕後*|*extras*|*extra*|*bonus*|*behind*|*featurette*|*making*|*sample*|*samples*|*trailer*|*trailers*|*预告*|*預告*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

record_other() {
  local folder="$1"
  local reason="$2"
  local detail="${3:-}"
  printf '%s\t%s\t%s\n' "$folder" "$reason" "$detail" >> "$OTHER_CASES_TSV"
}

move_or_record_subtitle() {
  local folder="$1"
  local src="$2"
  local dst="$folder/$(basename "$src")"

  if [[ -e "$dst" ]]; then
    printf '%s\t%s\t%s\t%s\n' "$folder" "$src" "$dst" "CONFLICT_DEST_EXISTS" >> "$PLANNED_MOVES_TSV"
    record_other "$folder" "subtitle move conflict" "$src -> $dst"
    return 0
  fi

  if [[ "$DRY_RUN" == "1" ]]; then
    printf '%s\t%s\t%s\t%s\n' "$folder" "$src" "$dst" "DRY_RUN_WOULD_MOVE" >> "$PLANNED_MOVES_TSV"
  else
    if mv "$src" "$dst"; then
      printf '%s\t%s\t%s\t%s\n' "$folder" "$src" "$dst" "MOVED" >> "$PLANNED_MOVES_TSV"
    else
      printf '%s\t%s\t%s\t%s\n' "$folder" "$src" "$dst" "MOVE_FAILED" >> "$PLANNED_MOVES_TSV"
      record_other "$folder" "subtitle move failed" "$src -> $dst"
    fi
  fi
}

scan_subdir() {
  local folder="$1"
  local subdir="$2"
  local item
  local subtitle_count=0
  local movie_count=0
  local other_count=0
  local nested_dir_count=0
  local -a subtitles=()
  local -a others=()

  if is_feature_subdir "$subdir"; then
    printf '%s\t%s\t%s\n' "$folder" "$subdir" "feature/extras-like subdir skipped" >> "$SKIPPED_SUBDIRS_TSV"
    return 0
  fi

  while IFS= read -r -d '' item; do
    if [[ -d "$item" ]]; then
      nested_dir_count=$((nested_dir_count + 1))
    elif is_ignored_file "$item"; then
      :
    elif is_subtitle "$item"; then
      subtitles+=("$item")
      subtitle_count=$((subtitle_count + 1))
    elif is_movie "$item"; then
      movie_count=$((movie_count + 1))
      others+=("$item")
    else
      other_count=$((other_count + 1))
      others+=("$item")
    fi
  done < <(find "$subdir" -mindepth 1 -maxdepth 1 -print0 2>/dev/null | sort -z)

  if [[ "$subtitle_count" -gt 0 && "$movie_count" -eq 0 && "$other_count" -eq 0 && "$nested_dir_count" -eq 0 ]]; then
    for item in "${subtitles[@]}"; do
      move_or_record_subtitle "$folder" "$item"
    done
  else
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$folder" "$subdir" "$subtitle_count" "$movie_count" "$other_count" "$nested_dir_count" >> "$SKIPPED_SUBDIRS_TSV"
    record_other "$folder" "subdir is not subtitle-only or feature-like" "$subdir subtitles=$subtitle_count movies=$movie_count others=$other_count nested_dirs=$nested_dir_count"
  fi
}

scan_folder() {
  local folder="$1"
  local item
  local movie_count=0
  local subtitle_count=0
  local subdir_count=0
  local other_file_count=0
  local -a movies=()
  local -a subtitles=()
  local -a subdirs=()
  local -a other_files=()

  while IFS= read -r -d '' item; do
    if [[ -d "$item" ]]; then
      subdirs+=("$item")
      subdir_count=$((subdir_count + 1))
    elif is_movie "$item"; then
      case "$(basename "$item")" in
        OG.*|.*".muxing.mkv"|*".muxing.mkv.abandoned."*|*".muxing.mkv.failed."*) ;;
        *)
          movies+=("$item")
          movie_count=$((movie_count + 1))
          ;;
      esac
    elif is_ignored_file "$item"; then
      :
    elif is_subtitle "$item"; then
      subtitles+=("$item")
      subtitle_count=$((subtitle_count + 1))
    else
      other_files+=("$item")
      other_file_count=$((other_file_count + 1))
    fi
  done < <(find "$folder" -mindepth 1 -maxdepth 1 -print0 2>/dev/null | sort -z)

  if [[ "$movie_count" -eq 1 ]]; then
    if [[ "$subdir_count" -gt 0 ]]; then
      for item in "${subdirs[@]}"; do
        scan_subdir "$folder" "$item"
      done
      subtitle_count=0
      subtitles=()
      while IFS= read -r -d '' item; do
        subtitles+=("$item")
        subtitle_count=$((subtitle_count + 1))
      done < <(find "$folder" -mindepth 1 -maxdepth 1 -type f -print0 2>/dev/null | while IFS= read -r -d '' item; do is_subtitle "$item" && printf '%s\0' "$item"; done | sort -z)
    fi

    if [[ "$subtitle_count" -gt 0 ]]; then
      printf '%s\t%s\t%s\t%s\t%s\n' "$folder" "${movies[0]}" "$subtitle_count" "$subdir_count" "$other_file_count" >> "$CANDIDATE_TSV"
    elif [[ "$subdir_count" -gt 0 || "$other_file_count" -gt 0 ]]; then
      record_other "$folder" "single movie folder without root subtitles but has extras/other files" "subdirs=$subdir_count other_files=$other_file_count"
    fi
  elif [[ "$movie_count" -gt 1 || "$subtitle_count" -gt 0 || "$other_file_count" -gt 0 ]]; then
    record_other "$folder" "not a single movie folder" "movies=$movie_count subtitles=$subtitle_count subdirs=$subdir_count other_files=$other_file_count"
  fi
}

write_summary() {
  local candidates moves skipped other
  candidates="$(awk 'NR>1 {count++} END {print count+0}' "$CANDIDATE_TSV")"
  moves="$(awk 'NR>1 {count++} END {print count+0}' "$PLANNED_MOVES_TSV")"
  skipped="$(awk 'NR>1 {count++} END {print count+0}' "$SKIPPED_SUBDIRS_TSV")"
  other="$(awk 'NR>1 {count++} END {print count+0}' "$OTHER_CASES_TSV")"
  {
    printf '# Movie Subtitle Rescan Summary\n\n'
    printf -- '- Generated: `%s`\n' "$(timestamp)"
    printf -- '- DRY_RUN: `%s`\n' "$DRY_RUN"
    printf -- '- Roots:\n'
    while IFS= read -r root; do
      [[ -n "$root" ]] && printf '  - `%s`\n' "$root"
    done <<< "$ROOTS"
    printf '\n## Counts\n\n'
    printf -- '- Single movie folders with subtitles: `%s`\n' "$candidates"
    printf -- '- Subtitle moves recorded: `%s`\n' "$moves"
    printf -- '- Subdirs skipped/recorded: `%s`\n' "$skipped"
    printf -- '- Other cases: `%s`\n\n' "$other"
    printf '## Files\n\n'
    printf -- '- Candidates: `%s`\n' "$CANDIDATE_TSV"
    printf -- '- Subtitle moves: `%s`\n' "$PLANNED_MOVES_TSV"
    printf -- '- Skipped subdirs: `%s`\n' "$SKIPPED_SUBDIRS_TSV"
    printf -- '- Other cases: `%s`\n' "$OTHER_CASES_TSV"
    printf -- '- Log: `%s`\n' "$SCAN_LOG"
  } > "$SUMMARY_MD"
}

main() {
  printf 'folder\tmovie\tsubtitle_count\tsubdir_count\tother_file_count\n' > "$CANDIDATE_TSV"
  printf 'folder\tsource\tdestination\tstatus\n' > "$PLANNED_MOVES_TSV"
  printf 'folder\tsubdir\tnote_or_subtitle_count\tmovie_count\tother_file_count\tnested_dir_count\n' > "$SKIPPED_SUBDIRS_TSV"
  printf 'folder\treason\tdetail\n' > "$OTHER_CASES_TSV"

  if [[ "$DRY_RUN" == "1" ]]; then
    log "DRY-RUN mode: subtitle files in subfolders will be recorded but not moved"
  else
    log "REAL RUN mode: subtitle-only subfolders may have subtitle files moved to parent movie folders"
  fi

  local root scanned=0
  while IFS= read -r root; do
    [[ -n "$root" ]] || continue
    if [[ ! -d "$root" ]]; then
      log "WARNING: root not mounted or missing: $root"
      continue
    fi
    log "Scanning root: $root"
    while IFS= read -r -d '' folder; do
      scan_folder "$folder"
      scanned=$((scanned + 1))
      if (( scanned % 200 == 0 )); then
        log "Scanned folders: $scanned"
      fi
    done < <(find "$root" -type d -name '#recycle' -prune -o -type d -print0 2>/dev/null)
  done <<< "$ROOTS"

  write_summary
  log "Done. Scanned folders: $scanned"
  log "Summary: $SUMMARY_MD"
}

main "$@"
