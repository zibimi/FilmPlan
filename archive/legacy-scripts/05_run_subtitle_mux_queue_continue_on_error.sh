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
PROGRESS_INTERVAL="${PROGRESS_INTERVAL:-60}"
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
  return 1
}

pause_current() {
  local message="$1"
  log "ERROR: $message"
  if [[ "$DRY_RUN" != "1" && -n "${CURRENT_LINE_NO:-}" && -n "${CURRENT_FOLDER:-}" ]]; then
    queue_update "$CURRENT_LINE_NO" "PENDING" "$CURRENT_FOLDER" "$message"
  fi
  return 88
}

is_volume_path() {
  case "$1" in
    /Volumes/*) return 0 ;;
    *) return 1 ;;
  esac
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
    *".en."*|*".eng."*|*"english"*|*"英文"*) printf 'eng' ;;
    *".zh."*|*".chs."*|*"chs"*|*".cht."*|*"cht"*|*".sc."*|*".tc."*|*".big5."*|*".big5"*|*"中文"*|*"中字"*|*"简体"*|*"繁体"*|*"簡體"*|*"繁體"*) printf 'chi' ;;
    *)
      if printf '%s' "$lower" | perl -CS -Mutf8 -ne 'exit(/[一-龥]/ ? 0 : 1)' >/dev/null 2>&1; then
        printf 'chi'
      else
        printf 'und'
      fi
      ;;
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
  local hint expected file_hint bom enc score cjk best_enc="" best_score=-999999 best_cjk=0 subtitle_kind

  case "$subtitle" in
    *.[sS][rR][tT]) subtitle_kind="srt" ;;
    *.[aA][sS][sS]|*.[sS][sS][aA]) subtitle_kind="ass" ;;
    *)
      printf '\n'
      return 0
      ;;
  esac

  hint="$(subtitle_lang "$subtitle")"
  expected="$hint"
  bom="$(od -An -tx1 -N4 "$subtitle" 2>/dev/null | tr -d ' \n')"
  file_hint="$(file -I "$subtitle" 2>/dev/null | sed -n 's/.*charset=//p' | tr '[:lower:]' '[:upper:]')"

  local -a candidates=()
  case "$bom" in
    FFFE*|fffe*) candidates+=("UTF-16LE") ;;
    FEFF*|feff*) candidates+=("UTF-16BE") ;;
    EFBBBF*|efbbbf*) candidates+=("UTF-8") ;;
  esac

  case "$file_hint" in
    UTF-8|US-ASCII) candidates+=("UTF-8") ;;
    UTF-16LE|UTF-16BE|UTF-16|ISO-8859-1|WINDOWS-1252|CP1252|BIG5|CP950|GB18030|GBK) candidates+=("$file_hint") ;;
  esac

  case "$hint" in
    chi)
      case "$(basename "$subtitle" | tr '[:upper:]' '[:lower:]')" in
        *big5*|*cht*|*繁体*|*繁體*) candidates+=("BIG5" "CP950" "UTF-8" "UTF-16LE" "UTF-16BE" "UTF-16" "GB18030" "GBK" "WINDOWS-1252" "ISO-8859-1") ;;
        *) candidates+=("UTF-8" "UTF-16LE" "UTF-16BE" "UTF-16" "GB18030" "GBK" "BIG5" "CP950" "WINDOWS-1252" "ISO-8859-1") ;;
      esac
      ;;
    eng)
      candidates+=("UTF-8" "UTF-16LE" "UTF-16BE" "UTF-16" "WINDOWS-1252" "ISO-8859-1" "GB18030")
      ;;
    *)
      candidates+=("UTF-8" "UTF-16LE" "UTF-16BE" "UTF-16" "WINDOWS-1252" "ISO-8859-1" "GB18030" "BIG5" "CP950")
      ;;
  esac

  local seen=" "
  for enc in "${candidates[@]}"; do
    [[ -n "$enc" ]] || continue
    [[ "$enc" == "CP1252" ]] && enc="WINDOWS-1252"
    [[ "$enc" == "GBK" ]] && enc="GB18030"
    [[ "$seen" == *" $enc "* ]] && continue
    seen="$seen$enc "

    local metrics
    if ! metrics="$(iconv -f "$enc" -t UTF-8 "$subtitle" 2>/dev/null | perl -CS -Mutf8 -e '
      my $expected = shift @ARGV;
      my $kind = shift @ARGV;
      binmode STDIN, ":encoding(UTF-8)";
      local $/;
      my $text = <STDIN> // "";
      my $cjk = () = $text =~ /[\x{3400}-\x{9FFF}\x{F900}-\x{FAFF}]/g;
      my $latin = () = $text =~ /[A-Za-z]/g;
      my $digits = () = $text =~ /[0-9]/g;
      my $arrows = () = $text =~ /-->/g;
      my $timestamps = () = $text =~ /\d\d:\d\d:\d\d[,.]\d\d\d/g;
      my $ass_dialogues = () = $text =~ /^Dialogue:/mg;
      my $ass_headers = () = $text =~ /^\[(Script Info|V4\+? Styles|Events)\]/mg;
      my $ctrl = () = $text =~ /[\x{0000}-\x{0008}\x{000B}\x{000C}\x{000E}-\x{001F}]/g;
      my $score;
      if ($expected eq "chi") {
        $score = $cjk * 200 + $latin + $digits - $ctrl * 1000;
        $score -= 10000 if $cjk == 0;
      } elsif ($expected eq "eng") {
        $score = $latin * 20 + $digits - $cjk * 50 - $ctrl * 1000;
      } else {
        $score = $cjk * 20 + $latin * 5 + $digits - $ctrl * 1000;
      }
      $score += $arrows * 50000 + $timestamps * 1000;
      $score += $ass_dialogues * 2000 + $ass_headers * 50000;
      $score -= 10000000 if $kind eq "srt" && $arrows == 0;
      $score -= 10000000 if $kind eq "ass" && ($ass_dialogues + $ass_headers) == 0;
      print "$score\t$cjk\n";
    ' "$expected" "$subtitle_kind")"; then
      continue
    fi
    score="${metrics%%$'\t'*}"
    cjk="${metrics#*$'\t'}"

    if (( score > best_score )); then
      best_score="$score"
      best_cjk="$cjk"
      best_enc="$enc"
    fi
  done

  [[ -n "$best_enc" ]] || return 1
  if [[ "$hint" == "chi" && "$best_cjk" -eq 0 ]]; then
    return 1
  fi

  printf '%s\n' "$best_enc"
}

decoded_cjk_count() {
  local subtitle="$1"
  local charset="$2"
  iconv -f "$charset" -t UTF-8 "$subtitle" 2>/dev/null | perl -CS -Mutf8 -e '
    binmode STDIN, ":encoding(UTF-8)";
    local $/;
    my $text = <STDIN> // "";
    my $cjk = () = $text =~ /[\x{3400}-\x{9FFF}\x{F900}-\x{FAFF}]/g;
    print "$cjk\n";
  '
}

file_size_bytes() {
  stat -f '%z' "$1"
}

bytes_to_gib() {
  awk -v bytes="$1" 'BEGIN { printf "%.2f GiB", bytes / 1024 / 1024 / 1024 }'
}

monitor_temp_output_growth() {
  local tmp_output="$1"
  local watched_pid="$2"
  local input_size="$3"
  local previous_size=0 current_size=0 delta=0 percent="0.0"

  while kill -0 "$watched_pid" >/dev/null 2>&1; do
    sleep "$PROGRESS_INTERVAL"
    if [[ -e "$tmp_output" ]]; then
      current_size="$(file_size_bytes "$tmp_output")"
      delta=$((current_size - previous_size))
      previous_size="$current_size"
      if [[ "$input_size" -gt 0 ]]; then
        percent="$(awk -v current="$current_size" -v input="$input_size" 'BEGIN { printf "%.1f", current * 100 / input }')"
      fi
      log "PROGRESS: temp output size=$current_size bytes ($(bytes_to_gib "$current_size")); delta since last check=$delta bytes ($(bytes_to_gib "$delta")); approx source ratio=${percent}%"
    else
      log "PROGRESS: temp output not visible yet: $tmp_output"
    fi
  done
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
  ((total_tracks > 0)) || { fail_current "could not inspect output tracks: $mkv"; return 1; }

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
    return 1
  fi
}

verify_muxed_output() {
  local mkv="$1"
  local expected_appended_count="$2"
  local expect_default_chi="$3"
  local info metrics subtitle_count default_chi_count

  info="$("$MKVMERGE" -J "$mkv")" || { fail_current "could not inspect muxed output: $mkv"; return 1; }
  metrics="$(printf '%s\n' "$info" | perl -MJSON::PP -0777 -ne '
    my $json = decode_json($_);
    my $subtitle_count = 0;
    my $default_chi_count = 0;
    for my $track (@{ $json->{tracks} || [] }) {
      next unless ($track->{type} || "") eq "subtitles";
      $subtitle_count++;
      my $props = $track->{properties} || {};
      my $is_default = $props->{default_track} ? 1 : 0;
      my $language = $props->{language} || "";
      my $language_ietf = $props->{language_ietf} || "";
      my $is_chi = ($language eq "chi" || $language eq "zho" || $language_ietf =~ /^zh(?:-|$)/);
      $default_chi_count++ if $is_default && $is_chi;
    }
    print "$subtitle_count\t$default_chi_count\n";
  ')"
  subtitle_count="${metrics%%$'\t'*}"
  default_chi_count="${metrics#*$'\t'}"

  log "Verification: subtitle_tracks=$subtitle_count default_chinese_tracks=$default_chi_count"

  if (( subtitle_count < expected_appended_count )); then
    fail_current "verification failed: expected at least $expected_appended_count subtitle tracks, found $subtitle_count in $mkv"
    return 1
  fi

  if [[ "$expect_default_chi" -eq 1 && "$default_chi_count" -lt 1 ]]; then
    fail_current "verification failed: no default Chinese subtitle track found in $mkv"
    return 1
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

  if [[ ! -d "$folder" ]]; then
    if is_volume_path "$folder"; then
      pause_current "volume path is unavailable; NAS/SMB mount may be disconnected: $folder"
      return 88
    fi
    fail_current "folder does not exist: $folder"
    return 1
  fi

  while IFS= read -r -d '' item; do
    base="$(basename "$item")"
    if is_mkv "$item" && [[ "$base" != OG.* && "$base" != .*".muxing.mkv" && "$base" != *".muxing.mkv.abandoned."* ]]; then
      movie="$item"
      ((mkv_count += 1))
    elif is_subtitle "$item"; then
      subtitles+=("$item")
    fi
  done < <(find "$folder" -maxdepth 1 -type f -print0 | sort -z)

  [[ "$mkv_count" -eq 1 ]] || { fail_current "expected exactly one non-OG MKV, found $mkv_count in $folder"; return 1; }
  ((${#subtitles[@]} > 0)) || { fail_current "no subtitle files found in $folder"; return 1; }

  local movie_base og_movie tmp_output net_before net_after tmp_output_exists=0
  movie_base="$(basename "$movie")"
  og_movie="$folder/OG.$movie_base"
  tmp_output="$folder/.$movie_base.muxing.mkv"
  net_before="$LOG_DIR/net-before-$(date '+%Y%m%d-%H%M%S').txt"
  net_after="$LOG_DIR/net-after-$(date '+%Y%m%d-%H%M%S').txt"

  [[ ! -e "$og_movie" ]] || { fail_current "OG file already exists: $og_movie"; return 1; }
  if [[ -e "$tmp_output" ]]; then
    tmp_output_exists=1
    if [[ "$DRY_RUN" == "1" ]]; then
      log "DRY-RUN: leftover temporary output exists and would be verified before retry: $tmp_output"
    fi
  fi

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
      return 1
    fi

    local decoded_cjk=0
    if [[ -n "$charset" ]]; then
      decoded_cjk="$(decoded_cjk_count "$subtitle" "$charset" || printf '0')"
    fi

    lang="$(subtitle_lang "$subtitle")"
    if [[ "$lang" == "und" && ( "$charset" == "GB18030" || "$charset" == "BIG5" || "$charset" == "CP950" || "$charset" == "UTF-16LE" || "$charset" == "UTF-16" ) ]]; then
      if [[ "$decoded_cjk" -gt 5 ]]; then
      lang="chi"
      fi
    fi
    if [[ "$lang" == "chi" && -n "$charset" && "$decoded_cjk" -lt 1 ]]; then
      fail_current "subtitle charset check failed: expected Chinese text but decoded CJK count is 0: $subtitle"
      return 1
    fi
    log "Subtitle charset: $charset | language: $lang | decoded_cjk=$decoded_cjk | file: $subtitle"

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
    log "DRY-RUN: would report temporary output growth every $PROGRESS_INTERVAL seconds while mkvmerge is running"
    log "DRY-RUN: would then update subtitle default flags on $tmp_output"
    if [[ "$tmp_output_exists" -eq 1 ]]; then
      log "DRY-RUN: existing temporary output would be verified and reused if valid"
    fi
    log "DRY-RUN: would rename original to $og_movie"
    log "DRY-RUN: would rename muxed file to $movie"
    log "DRY-RUN: queue would be updated to DONE on success"
    PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
    return 0
  fi

  set +e
  local mkvmerge_status=0 used_existing_tmp=0
  if [[ "$tmp_output_exists" -eq 1 ]]; then
    log "Found existing temporary output; verifying it before deciding whether to remux: $tmp_output"
    local tmp_info tmp_track_count
    tmp_info="$("$MKVMERGE" -i "$tmp_output" 2>> "$RUN_LOG")"
    tmp_track_count="$(printf '%s\n' "$tmp_info" | awk '/^Track ID [0-9]+:/ { count += 1 } END { print count + 0 }')"

    if [[ "$tmp_track_count" -eq 0 ]]; then
      local abandoned_tmp
      abandoned_tmp="$tmp_output.abandoned.$(date '+%Y%m%d-%H%M%S')"
      log "Existing temporary output has no tracks; moving it aside before remux: $abandoned_tmp"
      if ! mv "$tmp_output" "$abandoned_tmp"; then
        fail_current "temporary output has no tracks and could not be moved aside: $tmp_output"
        return 1
      fi
      tmp_output_exists=0
    else
      local tmp_size
      tmp_size="$(file_size_bytes "$tmp_output")"
      if [[ "$tmp_size" -lt "$input_size" ]]; then
        local abandoned_tmp
        abandoned_tmp="$tmp_output.abandoned.$(date '+%Y%m%d-%H%M%S')"
        log "Existing temporary output is smaller than the source movie; moving it aside before remux: $abandoned_tmp"
        if ! mv "$tmp_output" "$abandoned_tmp"; then
          fail_current "temporary output is incomplete and could not be moved aside: $tmp_output"
          return 1
        fi
        tmp_output_exists=0
      else
      set -e
      set_subtitle_default_flags "$tmp_output" "${appended_defaults[@]}" || return 1
      verify_muxed_output "$tmp_output" "${#subtitles[@]}" "$has_default_chi" || return 1
      set +e
      used_existing_tmp=1
      log "Existing temporary output passed verification; reusing it"
      fi
    fi
  fi

  if [[ "$used_existing_tmp" -eq 0 ]]; then
    local mkvmerge_pid monitor_pid
    "${cmd[@]}" >> "$RUN_LOG" 2>&1 &
    mkvmerge_pid=$!
    monitor_temp_output_growth "$tmp_output" "$mkvmerge_pid" "$input_size" &
    monitor_pid=$!
    wait "$mkvmerge_pid"
    mkvmerge_status=$?
    kill "$monitor_pid" >/dev/null 2>&1 || true
    wait "$monitor_pid" >/dev/null 2>&1 || true
    if [[ -e "$tmp_output" ]]; then
      local final_tmp_size
      final_tmp_size="$(file_size_bytes "$tmp_output")"
      log "PROGRESS: mkvmerge finished; temp output size=$final_tmp_size bytes ($(bytes_to_gib "$final_tmp_size"))"
    fi
  fi
  set -e
  if [[ "$used_existing_tmp" -eq 0 ]]; then
    if [[ "$mkvmerge_status" -eq 1 ]]; then
      log "mkvmerge completed with warnings; continuing"
    elif [[ "$mkvmerge_status" -ne 0 ]]; then
      if is_volume_path "$folder" && [[ ! -d "$folder" ]]; then
        pause_current "mkvmerge failed and NAS/SMB mount disappeared; leaving queue row PENDING: $folder"
        return 88
      fi
      if [[ -e "$tmp_output" ]]; then
        local failed_tmp
        failed_tmp="$tmp_output.failed.$(date '+%Y%m%d-%H%M%S')"
        log "Moving failed temporary output aside: $failed_tmp"
        mv "$tmp_output" "$failed_tmp" || true
      fi
      fail_current "mkvmerge failed for $folder with exit code $mkvmerge_status"
      return 1
    fi

    set_subtitle_default_flags "$tmp_output" "${appended_defaults[@]}" || return 1
    verify_muxed_output "$tmp_output" "${#subtitles[@]}" "$has_default_chi" || return 1
  fi

  log "Renaming original to OG prefix"
  if ! mv "$movie" "$og_movie"; then
    fail_current "could not rename original to $og_movie"
    return 1
  fi

  log "Renaming muxed file to original movie filename"
  if ! mv "$tmp_output" "$movie"; then
    log "Attempting rollback because final rename failed"
    mv "$og_movie" "$movie" || true
    fail_current "could not rename muxed file to $movie"
    return 1
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

  [[ -f "$QUEUE_FILE" ]] || { fail_current "queue file does not exist: $QUEUE_FILE"; exit 1; }
  if [[ "$DRY_RUN" == "1" ]]; then
    log "DRY-RUN mode: no media files, queue rows, or names will be changed"
  fi

  MKVMERGE="$(resolve_tool_or_name_for_dry_run "$MKVMERGE" "$LOCAL_MKVMERGE" "mkvmerge" "$KNOWN_MKVMERGE")" || { fail_current "mkvmerge not found. Install MKVToolNix or set MKVMERGE=/path/to/mkvmerge"; exit 1; }
  MKVPROPEDIT="$(resolve_tool_or_name_for_dry_run "$MKVPROPEDIT" "$LOCAL_MKVPROPEDIT" "mkvpropedit" "$KNOWN_MKVPROPEDIT")" || { fail_current "mkvpropedit not found. Install MKVToolNix or set MKVPROPEDIT=/path/to/mkvpropedit"; exit 1; }
  log "Using mkvmerge: $MKVMERGE"
  log "Using mkvpropedit: $MKVPROPEDIT"

  local pending process_status
  while true; do
    pending="$(find_first_pending || true)"
    if [[ -z "$pending" ]]; then
      log "No PENDING folders left in $QUEUE_FILE"
      exit 0
    fi

    CURRENT_LINE_NO="${pending%%$'\t'*}"
    CURRENT_FOLDER="${pending#*$'\t'}"

    log "Next queue line: $CURRENT_LINE_NO"

    # Keep batch processing resilient: a failure in one folder should mark that
    # queue row as FAILED, then continue with the next PENDING folder.
    set +e
    process_folder "$CURRENT_FOLDER"
    process_status=$?
    set -e

    if [[ "$process_status" -ne 0 ]]; then
      if [[ "$process_status" -eq 88 ]]; then
        log "Pausing queue because NAS/SMB path is unavailable: $CURRENT_FOLDER"
        exit 88
      fi
      log "Skipping failed folder and continuing: $CURRENT_FOLDER"
      if [[ "$DRY_RUN" == "1" ]]; then
        log "DRY-RUN: stopping after first failed PENDING folder"
        exit 0
      fi
      continue
    fi

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
