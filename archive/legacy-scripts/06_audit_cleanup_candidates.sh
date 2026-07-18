#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$WORKDIR/logs"
OUT_DIR="$WORKDIR/cleanup-audit"
TS="$(date '+%Y%m%d-%H%M%S')"
AUDIT_TSV="$OUT_DIR/cleanup_audit_$TS.tsv"
AUDIT_MD="$OUT_DIR/cleanup_audit_$TS.md"
RUN_LOG="$LOG_DIR/cleanup-audit-$TS.log"

LOCAL_MKVMERGE="$WORKDIR/tools/MKVToolNix.app/Contents/MacOS/mkvmerge"
LOCAL_MKVEXTRACT="$WORKDIR/tools/MKVToolNix.app/Contents/MacOS/mkvextract"
KNOWN_MKVMERGE="/Users/milou/Documents/电影整理计划/tools/MKVToolNix.app/Contents/MacOS/mkvmerge"
KNOWN_MKVEXTRACT="/Users/milou/Documents/电影整理计划/tools/MKVToolNix.app/Contents/MacOS/mkvextract"

MKVMERGE="${MKVMERGE:-}"
MKVEXTRACT="${MKVEXTRACT:-}"
if [[ -z "${ROOTS:-}" ]]; then
  ROOTS=$'/Volumes/分类\n/Volumes/导演们'
fi
VERIFY_DONE="${VERIFY_DONE:-1}"
SCAN_LIMIT="${SCAN_LIMIT:-0}"
EXTRACT_TIMEOUT="${EXTRACT_TIMEOUT:-180}"

mkdir -p "$LOG_DIR" "$OUT_DIR"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "$RUN_LOG"
}

resolve_tool() {
  local current="$1"
  local local_path="$2"
  local tool_name="$3"
  local known_path="$4"

  if [[ -n "$current" && -x "$current" ]]; then
    printf '%s\n' "$current"
  elif [[ -x "$local_path" ]]; then
    printf '%s\n' "$local_path"
  elif [[ -x "$known_path" ]]; then
    printf '%s\n' "$known_path"
  elif command -v "$tool_name" >/dev/null 2>&1; then
    command -v "$tool_name"
  else
    return 1
  fi
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

join_paths() {
  local first=1 path
  for path in "$@"; do
    if [[ "$first" -eq 1 ]]; then
      printf '%s' "$path"
      first=0
    else
      printf ' | %s' "$path"
    fi
  done
}

quality_metrics() {
  local file="$1"
  perl -CS -Mutf8 -e '
    binmode STDIN, ":encoding(UTF-8)";
    local $/;
    my $text = <STDIN> // "";
    my $cjk = () = $text =~ /[\x{3400}-\x{9FFF}\x{F900}-\x{FAFF}]/g;
    my $replacement = () = $text =~ /\x{FFFD}/g;
    my $private = () = $text =~ /[\x{E000}-\x{F8FF}]/g;
    my $control = () = $text =~ /[\x00-\x08\x0B\x0C\x0E-\x1F]/g;
    my $mojibake = () = $text =~ /(锟斤拷|Ã|Â|ä¸|å|æ|ðŸ|¤|¦|§|¨|©|ª|«|¬)/g;
    my $lines = () = $text =~ /\n/g;
    print join("\t", $cjk, $replacement, $private, $control, $mojibake, $lines), "\n";
  ' < "$file"
}

extract_track_with_timeout() {
  local movie="$1"
  local track_id="$2"
  local out="$3"
  local pid elapsed=0 status=0

  "$MKVEXTRACT" tracks "$movie" "$track_id:$out" >> "$RUN_LOG" 2>&1 &
  pid=$!

  while kill -0 "$pid" >/dev/null 2>&1; do
    sleep 1
    elapsed=$((elapsed + 1))
    if [[ "$elapsed" -ge "$EXTRACT_TIMEOUT" ]]; then
      log "WARNING: mkvextract timed out after ${EXTRACT_TIMEOUT}s; track=$track_id movie=$movie"
      kill "$pid" >/dev/null 2>&1 || true
      wait "$pid" >/dev/null 2>&1 || true
      return 124
    fi
  done

  wait "$pid"
  status=$?
  return "$status"
}

append_row() {
  local status="$1"
  local confidence="$2"
  local folder="$3"
  local movie="$4"
  local og_count="$5"
  local subtitle_count="$6"
  local internal_tracks="$7"
  local default_chi="$8"
  local action="$9"
  local note="${10}"

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$status" "$confidence" "$folder" "$movie" "$og_count" "$subtitle_count" \
    "$internal_tracks" "$default_chi" "$action" "$note" >> "$AUDIT_TSV"
}

verify_done_movie() {
  local folder="$1"
  local movie="$2"
  local subtitle_count="$3"
  local tmpdir json track_lines track_count text_track_count chi_track_count default_chi_count
  local best_cjk=0 best_bad=999999 best_note="" id lang lang_ietf default_track text_subtitles codec out metrics
  local cjk replacement private control mojibake lines bad

  tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/film-subtitle-audit.XXXXXX")"

  if ! json="$("$MKVMERGE" -J "$movie" 2>> "$RUN_LOG")"; then
    append_row "DONE_NEEDS_REVIEW" "LOW" "$folder" "$movie" "1+" "$subtitle_count" "0" "0" "REVIEW_IN_INFUSE" "mkvmerge could not inspect muxed movie"
    rm -rf "$tmpdir"
    return 0
  fi

  track_lines="$(printf '%s\n' "$json" | perl -MJSON::PP -0777 -ne '
    my $json = decode_json($_);
    for my $track (@{ $json->{tracks} || [] }) {
      next unless ($track->{type} || "") eq "subtitles";
      my $props = $track->{properties} || {};
      my $text = $props->{text_subtitles} ? 1 : 0;
      my $default = $props->{default_track} ? 1 : 0;
      print join("\t",
        $track->{id},
        $props->{language} || "",
        $props->{language_ietf} || "",
        $default,
        $text,
        $track->{codec} || ""
      ), "\n";
    }
  ')"

  track_count="$(printf '%s\n' "$track_lines" | awk 'NF { count += 1 } END { print count + 0 }')"
  text_track_count="$(printf '%s\n' "$track_lines" | awk -F '\t' '$5 == 1 { count += 1 } END { print count + 0 }')"
  chi_track_count="$(printf '%s\n' "$track_lines" | awk -F '\t' '$2 == "chi" || $2 == "zho" || $3 ~ /^zh/ { count += 1 } END { print count + 0 }')"
  default_chi_count="$(printf '%s\n' "$track_lines" | awk -F '\t' '$4 == 1 && ($2 == "chi" || $2 == "zho" || $3 ~ /^zh/) { count += 1 } END { print count + 0 }')"

  if [[ "$track_count" -eq 0 || "$text_track_count" -eq 0 ]]; then
    append_row "DONE_NEEDS_REVIEW" "LOW" "$folder" "$movie" "1+" "$subtitle_count" "$track_count" "$default_chi_count" "REVIEW_IN_INFUSE" "no internal text subtitle tracks found"
    rm -rf "$tmpdir"
    return 0
  fi

  while IFS=$'\t' read -r id lang lang_ietf default_track text_subtitles codec; do
    [[ -n "${id:-}" ]] || continue
    [[ "$text_subtitles" == "1" ]] || continue
    if [[ "$lang" != "chi" && "$lang" != "zho" && "$lang_ietf" != zh* && "$default_track" != "1" ]]; then
      continue
    fi

    out="$tmpdir/track-$id.txt"
    if ! extract_track_with_timeout "$movie" "$id" "$out"; then
      continue
    fi
    metrics="$(quality_metrics "$out")"
    IFS=$'\t' read -r cjk replacement private control mojibake lines <<< "$metrics"
    bad=$((replacement + private + control + mojibake))

    if [[ "$cjk" -gt "$best_cjk" || ( "$cjk" -eq "$best_cjk" && "$bad" -lt "$best_bad" ) ]]; then
      best_cjk="$cjk"
      best_bad="$bad"
      best_note="track=$id lang=$lang/$lang_ietf default=$default_track codec=$codec cjk=$cjk bad=$bad lines=$lines"
    fi
  done <<< "$track_lines"

  if [[ "$default_chi_count" -ge 1 && "$best_cjk" -ge 100 && "$best_bad" -eq 0 ]]; then
    append_row "DONE_VERIFIED_TEXT_OK" "HIGH" "$folder" "$movie" "1+" "$subtitle_count" "$track_count" "$default_chi_count" "SAFE_TO_PLAN_CLEANUP" "$best_note"
  elif [[ "$chi_track_count" -ge 1 && "$best_cjk" -ge 30 && "$best_bad" -le 2 ]]; then
    append_row "DONE_PROBABLY_OK" "MEDIUM" "$folder" "$movie" "1+" "$subtitle_count" "$track_count" "$default_chi_count" "REVIEW_BEFORE_DELETE" "$best_note"
  else
    append_row "DONE_NEEDS_REVIEW" "LOW" "$folder" "$movie" "1+" "$subtitle_count" "$track_count" "$default_chi_count" "REVIEW_IN_INFUSE" "$best_note"
  fi
  rm -rf "$tmpdir"
}

scan_folder() {
  local folder="$1"
  local item base
  local -a current_movies=()
  local -a og_movies=()
  local -a subtitles=()

  while IFS= read -r -d '' item; do
    base="$(basename "$item")"
    if is_mkv "$item"; then
      case "$base" in
        .*".muxing.mkv"|*".muxing.mkv.abandoned."*|*".muxing.mkv.failed."*) ;;
        OG.*) og_movies+=("$item") ;;
        *) current_movies+=("$item") ;;
      esac
    elif is_subtitle "$item"; then
      subtitles+=("$item")
    fi
  done < <(find "$folder" -maxdepth 1 -type f -print0 2>/dev/null | sort -z)

  if [[ "${#og_movies[@]}" -gt 0 && "${#current_movies[@]}" -eq 1 ]]; then
    if [[ "$VERIFY_DONE" == "1" ]]; then
      verify_done_movie "$folder" "${current_movies[0]}" "${#subtitles[@]}"
    else
      append_row "DONE_UNVERIFIED" "UNKNOWN" "$folder" "${current_movies[0]}" "${#og_movies[@]}" "${#subtitles[@]}" "" "" "VERIFY_BEFORE_CLEANUP" "OG movie exists"
    fi
  elif [[ "${#og_movies[@]}" -eq 0 && "${#current_movies[@]}" -eq 1 && "${#subtitles[@]}" -gt 0 ]]; then
    append_row "NEW_OR_PENDING" "UNKNOWN" "$folder" "${current_movies[0]}" "0" "${#subtitles[@]}" "" "" "ADD_TO_MUX_QUEUE" "movie plus external subtitles, no OG movie"
  elif [[ "${#og_movies[@]}" -gt 0 && "${#current_movies[@]}" -ne 1 ]]; then
    local current_movie_list=""
    if [[ "${#current_movies[@]}" -gt 0 ]]; then
      current_movie_list="$(join_paths "${current_movies[@]}")"
    fi
    append_row "DONE_NEEDS_REVIEW" "LOW" "$folder" "$current_movie_list" "${#og_movies[@]}" "${#subtitles[@]}" "" "" "MANUAL_REVIEW" "OG exists but current movie count is ${#current_movies[@]}"
  fi
}

write_markdown_report() {
  {
    printf '# Subtitle Cleanup Audit\n\n'
    printf -- '- Generated: `%s`\n' "$(timestamp)"
    printf -- '- TSV: `%s`\n' "$AUDIT_TSV"
    printf -- '- Verification enabled: `%s`\n\n' "$VERIFY_DONE"
    printf '## Summary\n\n'
    awk -F '\t' 'NR > 1 { status[$1] += 1; action[$9] += 1 } END {
      print "### By Status\n";
      for (s in status) printf "- `%s`: %d\n", s, status[s];
      print "\n### By Suggested Action\n";
      for (a in action) printf "- `%s`: %d\n", a, action[a];
    }' "$AUDIT_TSV"
    printf '\n## Notes\n\n'
    printf -- '- `DONE_VERIFIED_TEXT_OK` means the folder has an `OG.` movie and the current MKV contains an internal Chinese text subtitle track that extracts cleanly.\n'
    printf -- '- `DONE_PROBABLY_OK` should be sampled in Infuse before deleting anything.\n'
    printf -- '- `NEW_OR_PENDING` means there is a movie plus external subtitles but no `OG.` marker, so it probably belongs in the mux queue.\n'
    printf -- '- This script does not delete, move, or rename media files.\n'
  } > "$AUDIT_MD"
}

main() {
  MKVMERGE="$(resolve_tool "$MKVMERGE" "$LOCAL_MKVMERGE" "mkvmerge" "$KNOWN_MKVMERGE")" || { log "ERROR: mkvmerge not found"; exit 1; }
  MKVEXTRACT="$(resolve_tool "$MKVEXTRACT" "$LOCAL_MKVEXTRACT" "mkvextract" "$KNOWN_MKVEXTRACT")" || { log "ERROR: mkvextract not found"; exit 1; }

  printf 'status\tconfidence\tfolder\tmovie\tog_count\texternal_subtitle_count\tinternal_subtitle_tracks\tdefault_chinese_tracks\tsuggested_action\tnote\n' > "$AUDIT_TSV"

  log "Using mkvmerge: $MKVMERGE"
  log "Using mkvextract: $MKVEXTRACT"
  log "Writing audit TSV: $AUDIT_TSV"
  log "Writing audit Markdown: $AUDIT_MD"

  local root scanned=0 folder candidate_count
  while IFS= read -r root; do
    [[ -n "$root" ]] || continue
    if [[ ! -d "$root" ]]; then
      log "WARNING: root does not exist or is not mounted: $root"
      continue
    fi
    log "Scanning root: $root"
    while IFS= read -r -d '' folder; do
      scan_folder "$folder"
      scanned=$((scanned + 1))
      if [[ "$SCAN_LIMIT" -gt 0 && "$scanned" -ge "$SCAN_LIMIT" ]]; then
        log "SCAN_LIMIT reached: $SCAN_LIMIT"
        write_markdown_report
        exit 0
      fi
      if (( scanned % 100 == 0 )); then
        candidate_count="$(awk 'NR > 1 { count += 1 } END { print count + 0 }' "$AUDIT_TSV")"
        log "Scanned folders: $scanned; matched candidate folders: $candidate_count"
      fi
    done < <(find "$root" -type d -print0 2>/dev/null)
  done <<< "$ROOTS"

  write_markdown_report
  log "Done. Scanned folders: $scanned"
  log "Report: $AUDIT_MD"
}

main "$@"
