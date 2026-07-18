#!/usr/bin/env bash
set -Eeuo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$WORKDIR/logs"
QUEUE_FILE="${QUEUE_FILE:-$WORKDIR/mux_clean_queue.tsv}"
RUN_LOG="$LOG_DIR/run-mux-clean-queue.log"
NORMALIZED_DIR="$LOG_DIR/normalized-subtitles"

KNOWN_TOOL_DIR="/Users/milou/Documents/电影整理计划/tools/MKVToolNix.app/Contents/MacOS"
LOCAL_TOOL_DIR="$WORKDIR/tools/MKVToolNix.app/Contents/MacOS"
MKVMERGE="${MKVMERGE:-}"
MKVEXTRACT="${MKVEXTRACT:-}"

DRY_RUN="${DRY_RUN:-1}"
RUN_LIMIT="${RUN_LIMIT:-0}"
PROGRESS_INTERVAL="${PROGRESS_INTERVAL:-60}"
PROCESSED_COUNT=0

mkdir -p "$LOG_DIR" "$NORMALIZED_DIR"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "$RUN_LOG"
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

is_movie() {
  case "$1" in
    *.[mM][kK][vV]|*.[mM][pP]4|*.[aA][vV][iI]) return 0 ;;
    *) return 1 ;;
  esac
}

is_text_subtitle() {
  case "$1" in
    *.[sS][rR][tT]|*.[aA][sS][sS]|*.[sS][sS][aA]) return 0 ;;
    *) return 1 ;;
  esac
}

is_vobsub_index() {
  case "$1" in
    *.[iI][dD][xX]) return 0 ;;
    *) return 1 ;;
  esac
}

is_vobsub_sidecar() {
  case "$1" in
    *.[sS][uU][bB]) return 0 ;;
    *) return 1 ;;
  esac
}

is_subtitle() {
  is_text_subtitle "$1" || is_vobsub_index "$1"
}

matching_vobsub_sidecar() {
  local idx="$1"
  local idx_stem sidecar sidecar_stem
  idx_stem="$(printf '%s' "${idx%.*}" | tr '[:upper:]' '[:lower:]')"
  shift
  for sidecar in "$@"; do
    sidecar_stem="$(printf '%s' "${sidecar%.*}" | tr '[:upper:]' '[:lower:]')"
    if [[ "$sidecar_stem" == "$idx_stem" ]]; then
      printf '%s\n' "$sidecar"
      return 0
    fi
  done
  return 1
}

is_ignored_file() {
  case "$(basename "$1")" in
    .DS_Store|Thumbs.db|desktop.ini|._*) return 0 ;;
    *) return 1 ;;
  esac
}

file_size_bytes() {
  stat -f '%z' "$1"
}

bytes_to_gib() {
  awk -v bytes="$1" 'BEGIN { printf "%.2f GiB", bytes / 1024 / 1024 / 1024 }'
}

shell_quote_command() {
  local arg
  for arg in "$@"; do
    printf '"%s" ' "$arg"
  done
  printf '\n'
}

resolve_tool() {
  local current="$1"
  local local_path="$2"
  local tool_name="$3"
  local known_path="$4"
  if [[ -n "$current" && -x "$current" ]]; then
    printf '%s\n' "$current"
  elif command -v "$tool_name" >/dev/null 2>&1; then
    command -v "$tool_name"
  elif [[ -x "$local_path" ]]; then
    printf '%s\n' "$local_path"
  elif [[ -x "$known_path" ]]; then
    printf '%s\n' "$known_path"
  else
    return 1
  fi
}

subtitle_lang_hint() {
  local lower
  lower="$(basename "$1" | tr '[:upper:]' '[:lower:]')"
  if [[ "$lower" == *".zh."* || "$lower" == *".ch."* || "$lower" == *".chn."* || "$lower" == *".chs."* || "$lower" == *"chs"* || "$lower" == *".cht."* || "$lower" == *"cht"* || "$lower" == *".sc."* || "$lower" == *".tc."* || "$lower" == *".big5."* || "$lower" == *".big5"* || "$lower" == *"中文"* || "$lower" == *"中字"* || "$lower" == *"简体"* || "$lower" == *"繁体"* || "$lower" == *"簡體"* || "$lower" == *"繁體"* ]]; then
    printf 'chi'
  elif [[ "$lower" =~ (^|[^[:alnum:]])(en|eng|english)([^[:alnum:]]|$) || "$lower" == *"英文"* || "$lower" == *"英字"* ]]; then
    printf 'eng'
  elif [[ "$lower" =~ (^|[^[:alnum:]])(es|spa|spanish)([^[:alnum:]]|$) || "$lower" == *"español"* ]]; then
    printf 'spa'
  elif [[ "$lower" =~ (^|[^[:alnum:]])(it|ita|italian)([^[:alnum:]]|$) || "$lower" == *"sub-ita"* ]]; then
    printf 'ita'
  elif [[ "$lower" == *.de.srt || "$lower" == *.de.ass || "$lower" == *.de.ssa || "$lower" == *.de.idx || "$lower" =~ (^|[^[:alnum:]])(deu|ger|german)([^[:alnum:]]|$) || "$lower" == *"德语"* || "$lower" == *"德語"* || "$lower" == *"德文"* || "$lower" == *"德字"* ]]; then
    printf 'deu'
  elif [[ "$lower" =~ (^|[^[:alnum:]])(ru|rus|russian)([^[:alnum:]]|$) || "$lower" == *"рус"* ]]; then
    printf 'rus'
  elif [[ "$lower" =~ (^|[^[:alnum:]])(cz|cze|ces|czech)([^[:alnum:]]|$) ]]; then
    printf 'cze'
  elif [[ "$lower" =~ (^|[^[:alnum:]])(sk|slk|slo|slovak)([^[:alnum:]]|$) ]]; then
    printf 'slo'
  elif [[ "$lower" =~ (^|[^[:alnum:]])(pl|pol|polish)([^[:alnum:]]|$) ]]; then
    printf 'pol'
  else
    printf 'und'
  fi
}

disc_marker() {
  local lower
  lower="$(basename "$1" | tr '[:upper:]' '[:lower:]')"
  if [[ "$lower" =~ cd[[:space:]._-]*([0-9]+) ]]; then
    printf 'cd%s' "${BASH_REMATCH[1]}"
  fi
}

detect_subtitle() {
  local subtitle="$1"
  local hint="$2"
  python3 - "$subtitle" "$hint" <<'PY'
from pathlib import Path
import sys, re

path = Path(sys.argv[1])
hint = sys.argv[2]
data = path.read_bytes()
name = path.name.lower()

kind = "ass" if name.endswith((".ass", ".ssa")) else "srt"
base = []
if data.startswith(b"\xff\xfe"):
    base.append("UTF-16LE")
elif data.startswith(b"\xfe\xff"):
    base.append("UTF-16BE")
elif data.startswith(b"\xef\xbb\xbf"):
    base.append("UTF-8-SIG")

if hint == "chi":
    if any(x in name for x in ["big5", "cht", "繁体", "繁體"]):
        base += ["BIG5", "CP950", "UTF-8", "GB18030", "GBK", "UTF-16LE", "UTF-16BE", "CP1252", "LATIN1"]
    else:
        base += ["UTF-8", "GB18030", "GBK", "UTF-16LE", "UTF-16BE", "BIG5", "CP950", "CP1252", "LATIN1"]
elif hint == "eng":
    base += ["UTF-8", "UTF-8-SIG", "CP1252", "CP1251", "LATIN1", "UTF-16LE", "UTF-16BE", "GB18030"]
elif hint in ("spa", "ita", "deu"):
    base += ["UTF-8", "UTF-8-SIG", "CP1252", "LATIN1", "UTF-16LE", "UTF-16BE", "CP1251", "GB18030"]
elif hint == "rus":
    base += ["UTF-8", "UTF-8-SIG", "CP1251", "UTF-16LE", "UTF-16BE", "CP1252", "LATIN1", "GB18030"]
elif hint in ("cze", "slo", "pol"):
    base += ["UTF-8", "UTF-8-SIG", "CP1250", "CP1252", "LATIN1", "UTF-16LE", "UTF-16BE", "CP1251", "GB18030"]
else:
    base += ["UTF-8", "UTF-8-SIG", "GB18030", "GBK", "BIG5", "CP950", "UTF-16LE", "UTF-16BE", "CP1250", "CP1252", "LATIN1", "CP1251"]

seen = []
for enc in base:
    enc = {"GBK": "GB18030", "LATIN1": "ISO-8859-1"}.get(enc, enc)
    if enc not in seen:
        seen.append(enc)

best = None
for idx, enc in enumerate(seen):
    try:
        text = data.decode(enc)
        ok = True
    except UnicodeDecodeError:
        text = data.decode(enc, errors="replace")
        ok = False
    repl = text.count("\ufffd")

    cjk = len(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", text))
    cyrillic = len(re.findall(r"[\u0400-\u04ff]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    digits = len(re.findall(r"[0-9]", text))
    arrows = text.count("-->")
    loose_time = r"\d{1,2}\s*:\s*\d{1,2}\s*:\s*\d{1,2}\s*[,.]\s*\d{1,3}"
    single_arrows = len(re.findall(loose_time + r"\s*->\s*" + loose_time, text))
    timestamps = len(re.findall(loose_time, text))
    ass_marks = len(re.findall(r"^(Dialogue:|\[(Script Info|V4\+? Styles|Events)\])", text, re.M))
    ctrl = len(re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text))
    c1 = len(re.findall(r"[\x80-\x9f]", text))
    mojibake = len(re.findall(r"[ÃÂµÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß»¼½¾]", text))
    ascii_printable = sum(1 for ch in text if ch in "\r\n\t" or " " <= ch <= "~")
    ascii_ratio = ascii_printable / max(len(text), 1)

    if hint == "chi":
        score = cjk * 300 + latin + digits - repl * 5000 - ctrl * 1000 - c1 * 2000 - mojibake * 500
        if cjk == 0:
            score -= 1000000
    elif hint == "eng":
        score = latin * 30 + digits - cjk * 2000 - cyrillic * 2000 - repl * 100000 - ctrl * 1000 - c1 * 2000 - mojibake * 2000
    elif hint in ("spa", "ita", "deu"):
        score = latin * 30 + digits - cjk * 2000 - cyrillic * 2000 - repl * 100000 - ctrl * 1000 - c1 * 2000 - mojibake * 2000
    elif hint in ("cze", "slo", "pol"):
        score = latin * 30 + digits - cjk * 2000 - cyrillic * 2000 - repl * 100000 - ctrl * 1000 - c1 * 2000 - mojibake * 1000
    elif hint == "rus":
        score = cyrillic * 120 + latin * 5 + digits - cjk * 2000 - repl * 100000 - ctrl * 1000 - c1 * 2000 - mojibake * 500
        if cyrillic == 0:
            score -= 1000000
    else:
        if cjk >= 50:
            score = cjk * 200 + latin * 10 + digits - cyrillic * 100 - repl * 5000 - ctrl * 1000 - c1 * 2000 - mojibake * 300
        elif cyrillic >= 50:
            score = cyrillic * 80 + latin * 5 + digits - cjk * 100 - repl * 5000 - ctrl * 1000 - c1 * 2000 - mojibake * 300
            if enc in ("CP1251",):
                score += 20000
        else:
            score = latin * 10 + digits - cjk * 100 - cyrillic * 500 - repl * 5000 - ctrl * 1000 - c1 * 2000 - mojibake * 300
            if enc in ("GB18030", "BIG5", "CP950"):
                score -= 20000
            if enc == "CP1251":
                score -= 20000

    if kind == "srt":
        score += (arrows + single_arrows) * 50000 + timestamps * 1000
        if arrows == 0 and single_arrows == 0:
            score -= 100000000
        if timestamps < 2:
            score -= 100000000
        if ascii_ratio < 0.20:
            score -= 50000000
    else:
        score += ass_marks * 50000
        if ass_marks == 0:
            score -= 10000000

    if ok:
        score += 1000
    else:
        score -= 1000000
    if data.startswith(b"\xef\xbb\xbf") and enc == "UTF-8-SIG":
        score += 10000000
    elif data.startswith(b"\xff\xfe") and enc == "UTF-16LE":
        score += 10000000
    elif data.startswith(b"\xfe\xff") and enc == "UTF-16BE":
        score += 10000000
    score -= idx

    row = (score, enc, cjk, cyrillic, repl, ok, latin, arrows, ass_marks, mojibake, c1)
    if best is None or score > best[0]:
        best = row

if best is None:
    raise SystemExit("ERROR\tno-decodable-encoding")

score, enc, cjk, cyrillic, repl, ok, latin, arrows, ass_marks, mojibake, c1 = best
lang = hint
english_hits = len(re.findall(r"\b(the|and|you|that|this|with|from|have|not|for|are|was|were|movie|city)\b", text, re.I))
if hint == "und" and lang != "chi" and cjk >= 50:
    lang = "chi"
if lang in ("und", "ita", "spa", "cze", "slo", "pol") and cjk == 0 and latin > 200 and english_hits >= 10 and cyrillic * 5 < latin:
    lang = "eng"
if lang == "und" and cyrillic >= 50 and cyrillic * 5 >= latin:
    lang = "rus"
if lang == "chi" and cjk < 1:
    raise SystemExit(f"ERROR\t{enc}\tChinese subtitle decoded with cjk=0")
if lang == "rus" and cyrillic < 1:
    raise SystemExit(f"ERROR\t{enc}\tRussian subtitle decoded with cyrillic=0")
if lang == "rus" and hint != "rus" and mojibake >= 40:
    raise SystemExit(f"ERROR\t{enc}\tsubtitle inferred as Russian but has high mojibake_score={mojibake}; review before cleaning")
if lang == "und" and enc in ("ISO-8859-1", "CP1252") and mojibake >= 40:
    raise SystemExit(f"ERROR\t{enc}\tund subtitle has high mojibake_score={mojibake}; review before cleaning")

print(f"OK\t{enc}\t{lang}\t{cjk}\t{repl}\t{score}\t{mojibake}")
PY
}

normalize_subtitle_to_utf8() {
  local subtitle="$1"
  local charset="$2"
  local lang="$3"
  local index="$4"
  local safe_stem="$5"
  local ext out_dir out_file

  ext="${subtitle##*.}"
  out_dir="$NORMALIZED_DIR/$safe_stem"
  mkdir -p "$out_dir"
  out_file="$out_dir/subtitle_${index}_${lang}.${ext}"

  python3 - "$subtitle" "$charset" "$out_file" <<'PY'
from pathlib import Path
import sys
import re

src = Path(sys.argv[1])
charset = sys.argv[2]
out = Path(sys.argv[3])

codec = {
    "UTF-8": "utf-8",
    "UTF-8-SIG": "utf-8-sig",
    "GBK": "gb18030",
    "GB18030": "gb18030",
    "BIG5": "big5",
    "CP950": "cp950",
    "CP1251": "cp1251",
    "CP1250": "cp1250",
    "CP1252": "cp1252",
    "ISO-8859-1": "iso-8859-1",
    "LATIN1": "iso-8859-1",
    "UTF-16LE": "utf-16le",
    "UTF-16BE": "utf-16be",
}.get(charset.upper(), charset)

data = src.read_bytes()
try:
    text = data.decode(codec, errors="strict")
except UnicodeDecodeError as exc:
    print(f"ERROR\tstrict decode failed with {codec}: {exc}", file=sys.stderr)
    raise SystemExit(2)

text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
if "\ufffd" in text:
    print("ERROR\tdecoded text contains replacement character", file=sys.stderr)
    raise SystemExit(3)

if src.suffix.lower() == ".srt":
    text = re.sub(
        r"(\d{1,2}\s*:\s*\d{1,2}\s*:\s*\d{1,2}\s*[,.]\s*\d{1,3})\s*->\s*(\d{1,2}\s*:\s*\d{1,2}\s*:\s*\d{1,2}\s*[,.]\s*\d{1,3})",
        r"\1 --> \2",
        text,
    )
    timing_re = re.compile(
        r"^\s*(\d{1,2})\s*:\s*(\d{1,2})\s*:\s*(\d{1,2})\s*[,.]\s*(\d{1,3})\s*-->\s*(\d{1,2})\s*:\s*(\d{1,2})\s*:\s*(\d{1,2})\s*[,.]\s*(\d{1,3})(.*)$"
    )
    def fmt_time(h, m, s, ms):
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{ms.strip().ljust(3, '0')[:3]}"
    blocks = re.split(r"\n\s*\n", text.strip())
    renumbered = []
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if not lines:
            continue
        timing_index = None
        for i, line in enumerate(lines):
            if timing_re.match(line):
                timing_index = i
                break
        if timing_index is None:
            continue
        body = lines[timing_index + 1 :]
        if not body:
            continue
        m = timing_re.match(lines[timing_index])
        timing = f"{fmt_time(*m.group(1, 2, 3, 4))} --> {fmt_time(*m.group(5, 6, 7, 8))}{m.group(9).strip()}"
        renumbered.append(f"{len(renumbered) + 1}\n{timing}\n" + "\n".join(body).strip())
    if not renumbered:
        print("ERROR\tSRT normalization found no valid cues", file=sys.stderr)
        raise SystemExit(4)
    text = "\n\n".join(renumbered) + "\n"

out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", encoding="utf-8") as f:
    f.write(text)
print(str(out))
PY
}

find_first_pending() {
  awk -F '\t' '$0 !~ /^#/ && $1 == "PENDING" { print NR "\t" $2; exit }' "$QUEUE_FILE"
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
      log "PROGRESS: temp output size=$current_size bytes ($(bytes_to_gib "$current_size")); delta=$delta bytes ($(bytes_to_gib "$delta")); source ratio=${percent}%"
    else
      log "PROGRESS: temp output not visible yet: $tmp_output"
    fi
  done
}

verify_muxed_output() {
  local mkv="$1"
  local expected_appended="$2"
  local expect_default_chi="$3"
  local verify_dir="$4"
  local original_subtitle_count="$5"
  local json_file tracks_tsv subtitle_count default_chi_count

  mkdir -p "$verify_dir"
  json_file="$verify_dir/mkvmerge-info.json"
  "$MKVMERGE" -J "$mkv" > "$json_file" || { fail_current "could not inspect muxed output: $mkv"; return 1; }
  tracks_tsv="$(python3 - "$expected_appended" "$original_subtitle_count" "$json_file" <<'PY'
import json, sys
n = int(sys.argv[1])
original = int(sys.argv[2])
with open(sys.argv[3], "r", encoding="utf-8") as f:
    doc = json.load(f)
subs = []
subtitle_count = 0
default_chi = 0
for t in doc.get("tracks", []):
    if t.get("type") != "subtitles":
        continue
    subtitle_count += 1
    p = t.get("properties", {})
    lang = p.get("language", "")
    ietf = p.get("language_ietf", "")
    if p.get("default_track") and (lang in ("chi", "zho") or ietf.startswith("zh")):
        default_chi += 1
    codec_id = p.get("codec_id", "")
    subs.append((t.get("id"), lang, ietf, codec_id, p.get("track_name", "")))
appended = subs[original:]
print(f"COUNTS\t{subtitle_count}\t{default_chi}\t{len(appended)}")
for row in appended:
    print("TRACK\t" + "\t".join("" if x is None else str(x) for x in row))
PY
)"
  subtitle_count="$(printf '%s\n' "$tracks_tsv" | awk -F '\t' '$1=="COUNTS"{print $2}')"
  default_chi_count="$(printf '%s\n' "$tracks_tsv" | awk -F '\t' '$1=="COUNTS"{print $3}')"
  local appended_subtitle_count
  appended_subtitle_count="$(printf '%s\n' "$tracks_tsv" | awk -F '\t' '$1=="COUNTS"{print $4}')"
  log "Verification: subtitle_tracks=$subtitle_count appended_subtitle_tracks=$appended_subtitle_count default_chinese_tracks=$default_chi_count"
  if [[ "$appended_subtitle_count" -lt "$expected_appended" ]]; then
    fail_current "verification failed: expected at least $expected_appended appended subtitle tracks, found $appended_subtitle_count"
    return 1
  fi
  if [[ "$expect_default_chi" -eq 1 && "$default_chi_count" -lt 1 ]]; then
    fail_current "verification failed: no default Chinese subtitle track"
    return 1
  fi

  local line id lang ietf codec name out metrics repl cjk
  while IFS=$'\t' read -r marker id lang ietf codec name; do
    [[ "$marker" == "TRACK" ]] || continue
    if [[ "$codec" != S_TEXT/* ]]; then
      log "Verification: appended subtitle track $id is non-text codec $codec; skipping text extraction"
      continue
    fi
    out="$verify_dir/track_${id}.srt"
    "$MKVEXTRACT" tracks "$mkv" "$id:$out" >> "$RUN_LOG" 2>&1 || { fail_current "could not extract appended subtitle track $id"; return 1; }
    metrics="$(python3 - "$out" <<'PY'
from pathlib import Path
import sys, re
s = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
cjk = len(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", s))
repl = s.count(chr(0xfffd))
print(str(cjk) + "\t" + str(repl))
PY
)"
    cjk="${metrics%%$'\t'*}"
    repl="${metrics#*$'\t'}"
    log "Verification: extracted appended subtitle track=$id lang=$lang codec=$codec cjk=$cjk replacement_chars=$repl"
    if [[ "$repl" -ne 0 ]]; then
      fail_current "verification failed: extracted subtitle track $id contains replacement characters"
      return 1
    fi
    if [[ "$lang" == "chi" || "$ietf" == zh* ]]; then
      if [[ "$cjk" -lt 1 ]]; then
        fail_current "verification failed: Chinese subtitle track $id has no CJK characters"
        return 1
      fi
    fi
  done <<< "$tracks_tsv"
}

count_subtitle_tracks_in_mkv() {
  local mkv="$1"
  "$MKVMERGE" -J "$mkv" 2>/dev/null | python3 -c 'import json,sys
try:
    doc=json.load(sys.stdin)
except Exception:
    print(-1)
    raise SystemExit(0)
print(sum(1 for t in doc.get("tracks", []) if t.get("type")=="subtitles"))'
}

count_default_chinese_subtitle_tracks() {
  local mkv="$1"
  "$MKVMERGE" -J "$mkv" 2>/dev/null | python3 -c 'import json,sys
try:
    doc=json.load(sys.stdin)
except Exception:
    print(0)
    raise SystemExit(0)
count=0
for t in doc.get("tracks", []):
    if t.get("type") != "subtitles":
        continue
    p=t.get("properties", {})
    lang=p.get("language", "")
    ietf=p.get("language_ietf", "")
    if p.get("default_track") and (lang in ("chi", "zho") or ietf.startswith("zh")):
        count += 1
print(count)'
}

process_folder() {
  local folder="$1"
  local item base movie="" movie_count=0
  local -a subtitles=()
  local -a vobsub_sidecars=()
  local -a ignored=()
  local -a unexpected=()

  [[ -d "$folder" ]] || { fail_current "folder does not exist: $folder"; return 1; }
  [[ "$folder" != *"/#recycle/"* && "$folder" != *"/#recycle" ]] || { fail_current "refusing to process #recycle path: $folder"; return 1; }

  while IFS= read -r -d '' item; do
    base="$(basename "$item")"
    if is_ignored_file "$item"; then
      ignored+=("$item")
    elif [[ "$base" == .*".muxing.mkv" ]]; then
      :
    elif [[ "$base" == *".muxing.mkv.abandoned."* || "$base" == *".muxing.mkv.failed."* ]]; then
      ignored+=("$item")
    elif is_movie "$item"; then
      case "$base" in
        OG.*) unexpected+=("$item") ;;
        *) movie="$item"; movie_count=$((movie_count + 1)) ;;
      esac
    elif is_subtitle "$item"; then
      subtitles+=("$item")
    elif is_vobsub_sidecar "$item"; then
      vobsub_sidecars+=("$item")
    else
      unexpected+=("$item")
    fi
  done < <(find "$folder" -mindepth 1 -maxdepth 1 -type f -print0 2>/dev/null | sort -z)

  [[ "$movie_count" -eq 1 ]] || { fail_current "expected exactly one movie, found $movie_count in $folder"; return 1; }
  [[ "${#subtitles[@]}" -gt 0 ]] || { fail_current "no subtitle files found in $folder"; return 1; }
  local vobsub_idx vobsub_sidecar
  for vobsub_idx in "${subtitles[@]}"; do
    if is_vobsub_index "$vobsub_idx"; then
      vobsub_sidecar="$(matching_vobsub_sidecar "$vobsub_idx" "${vobsub_sidecars[@]+"${vobsub_sidecars[@]}"}")" || {
        unexpected+=("$vobsub_idx")
        continue
      }
    fi
  done
  for vobsub_sidecar in "${vobsub_sidecars[@]+"${vobsub_sidecars[@]}"}"; do
    local has_index=0
    for vobsub_idx in "${subtitles[@]}"; do
      if is_vobsub_index "$vobsub_idx" && [[ "$(printf '%s' "${vobsub_idx%.*}" | tr '[:upper:]' '[:lower:]')" == "$(printf '%s' "${vobsub_sidecar%.*}" | tr '[:upper:]' '[:lower:]')" ]]; then
        has_index=1
        break
      fi
    done
    [[ "$has_index" -eq 1 ]] || unexpected+=("$vobsub_sidecar")
  done
  [[ "${#unexpected[@]}" -eq 0 ]] || {
    log "Unexpected files:"
    printf '%s\n' "${unexpected[@]}" | sed 's/^/  /' | tee -a "$RUN_LOG"
    fail_current "unexpected files found in $folder"
    return 1
  }

  local movie_base stem safe_stem parent target tmp_output input_size estimated_total verify_dir source_subtitle_count
  movie_base="$(basename "$movie")"
  stem="${movie_base%.*}"
  safe_stem="${stem//[^A-Za-z0-9._-]/_}-$(date '+%Y%m%d-%H%M%S')"
  parent="$(dirname "$folder")"
  target="$parent/$stem.mkv"
  tmp_output="$folder/.$stem.muxing.mkv"
  verify_dir="$LOG_DIR/verify-$safe_stem"
  input_size="$(file_size_bytes "$movie")"
  source_subtitle_count="$(count_subtitle_tracks_in_mkv "$movie")"
  [[ "$source_subtitle_count" -ge 0 ]] || { fail_current "could not inspect source subtitle tracks: $movie"; return 1; }

  [[ ! -e "$target" ]] || { fail_current "parent target already exists: $target"; return 1; }
  if [[ -e "$tmp_output" ]]; then
    local tmp_size abandoned_tmp
    tmp_size="$(file_size_bytes "$tmp_output")"
    if [[ "$DRY_RUN" == "1" ]]; then
      log "DRY-RUN: found existing temporary output that would be moved aside before remux: size=$tmp_size bytes ($(bytes_to_gib "$tmp_size")); file=$tmp_output"
    else
      log "Found existing temporary output; moving aside before remux to avoid reusing stale interrupted output: $tmp_output"
      abandoned_tmp="$tmp_output.abandoned.$(date '+%Y%m%d-%H%M%S')"
      log "Existing temporary output size=$tmp_size bytes ($(bytes_to_gib "$tmp_size")); moved to: $abandoned_tmp"
      mv "$tmp_output" "$abandoned_tmp"
      ignored+=("$abandoned_tmp")
    fi
  fi

  estimated_total=$((input_size * 2))
  log "Folder: $folder"
  log "Movie: $movie"
  log "Target: $target"
  log "Subtitles: ${#subtitles[@]}"
  log "Estimated NAS SMB traffic: about $estimated_total bytes ($(bytes_to_gib "$estimated_total")), plus overhead"

  local movie_disc subtitle_disc
  movie_disc="$(disc_marker "$movie_base")"
  if [[ -n "$movie_disc" ]]; then
    for subtitle in "${subtitles[@]}"; do
      subtitle_disc="$(disc_marker "$subtitle")"
      if [[ -n "$subtitle_disc" && "$subtitle_disc" != "$movie_disc" ]]; then
        fail_current "subtitle disc marker mismatch: movie=$movie_disc subtitle=$subtitle_disc file=$subtitle"
        return 1
      fi
    done
  fi

  local -a cmd=("$MKVMERGE" "--output" "$tmp_output" "$movie")
  local subtitle hint detect_status charset lang cjk repl score mojibake name default_flag has_default_chi=0 expect_default_chi=0
  local normalized_subtitle subtitle_index=0
  local -a subtitle_files=()
  local appended_subtitle_count=0
  local review_required=0 review_message=""

  has_default_chi="$(count_default_chinese_subtitle_tracks "$movie")"
  if [[ "$has_default_chi" -gt 0 ]]; then
    expect_default_chi=1
    log "Source already has $has_default_chi default Chinese subtitle track(s); appended Chinese subtitles will not be set as default"
  fi

  for subtitle in "${subtitles[@]}"; do
    hint="$(subtitle_lang_hint "$subtitle")"
    subtitle_index=$((subtitle_index + 1))
    if is_vobsub_index "$subtitle"; then
      lang="$hint"
      charset="VobSub"
      cjk=0
      repl=0
      mojibake=0
      normalized_subtitle="$subtitle"
      log "Subtitle format: VobSub image subtitle | language: $lang | file: $subtitle"
      vobsub_sidecar="$(matching_vobsub_sidecar "$subtitle" "${vobsub_sidecars[@]+"${vobsub_sidecars[@]}"}")" || {
        fail_current "VobSub index has no matching .sub sidecar: $subtitle"
        return 1
      }
      subtitle_files+=("$vobsub_sidecar")
    else
      detect_status="$(detect_subtitle "$subtitle" "$hint")" || { fail_current "subtitle encoding detection failed: $subtitle :: $detect_status"; return 1; }
      IFS=$'\t' read -r _ charset lang cjk repl score mojibake <<< "$detect_status"
      log "Subtitle charset: $charset | language: $lang | cjk=$cjk | replacement_chars=$repl | mojibake_score=${mojibake:-0} | file: $subtitle"
      if [[ "$repl" -ne 0 ]]; then
        fail_current "subtitle decode produced replacement characters: $subtitle"
        return 1
      fi
      if [[ "$DRY_RUN" == "1" ]]; then
        normalized_subtitle="$NORMALIZED_DIR/$safe_stem/subtitle_${subtitle_index}_${lang}.${subtitle##*.}"
        log "DRY-RUN: would normalize subtitle to UTF-8: $normalized_subtitle"
      else
        normalized_subtitle="$(normalize_subtitle_to_utf8 "$subtitle" "$charset" "$lang" "$subtitle_index" "$safe_stem")" || {
          fail_current "subtitle UTF-8 normalization failed: $subtitle"
          return 1
        }
        log "Normalized subtitle to UTF-8: $normalized_subtitle"
      fi
    fi
    case "$lang" in
      chi) name="Chinese" ;;
      eng) name="English" ;;
      spa) name="Spanish" ;;
      ita) name="Italian" ;;
      deu) name="German" ;;
      rus) name="Russian" ;;
      cze) name="Czech" ;;
      slo) name="Slovak" ;;
      pol) name="Polish" ;;
      *) name="Subtitle" ;;
    esac
    default_flag="no"
    if [[ "$lang" == "chi" && "$has_default_chi" -eq 0 ]]; then
      default_flag="yes"
      has_default_chi=1
      expect_default_chi=1
    elif [[ "${#subtitles[@]}" -eq 1 && "$lang" == "und" ]]; then
      default_flag="yes"
    fi
    cmd+=("--language" "0:$lang" "--track-name" "0:$name" "--default-track-flag" "0:$default_flag" "$normalized_subtitle")
    subtitle_files+=("$subtitle")
    appended_subtitle_count=$((appended_subtitle_count + 1))
  done

  if [[ "$DRY_RUN" == "1" ]]; then
    log "DRY-RUN: would run mkvmerge, verify appended subtitle tracks by extraction, move output to parent, delete source movie/subtitles, and remove the now-empty folder"
    printf 'DRY-RUN command: ' | tee -a "$RUN_LOG"
    shell_quote_command "${cmd[@]}" | tee -a "$RUN_LOG"
    PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
    return 0
  fi

  if [[ -e "$tmp_output" ]]; then
    local existing_subtitle_count
    existing_subtitle_count="$(count_subtitle_tracks_in_mkv "$tmp_output")"
    if [[ "$existing_subtitle_count" -lt "$appended_subtitle_count" ]]; then
      local abandoned_tmp
      abandoned_tmp="$tmp_output.abandoned.$(date '+%Y%m%d-%H%M%S')"
      log "Existing temporary output has $existing_subtitle_count subtitle tracks but expected $appended_subtitle_count; moving aside before remux: $abandoned_tmp"
      mv "$tmp_output" "$abandoned_tmp"
      ignored+=("$abandoned_tmp")
    fi
  fi

  if [[ ! -e "$tmp_output" ]]; then
    local mkvmerge_pid monitor_pid mkvmerge_status mkvmerge_log_start
    mkvmerge_log_start="$(wc -l < "$RUN_LOG" | tr -d ' ')"
    set +e
    "${cmd[@]}" >> "$RUN_LOG" 2>&1 &
    mkvmerge_pid=$!
    monitor_temp_output_growth "$tmp_output" "$mkvmerge_pid" "$input_size" &
    monitor_pid=$!
    wait "$mkvmerge_pid"
    mkvmerge_status=$?
    kill "$monitor_pid" >/dev/null 2>&1 || true
    wait "$monitor_pid" >/dev/null 2>&1 || true
    set -e

    if [[ "$mkvmerge_status" -eq 1 ]]; then
      log "mkvmerge completed with warnings; continuing to verification"
    elif [[ "$mkvmerge_status" -ne 0 ]]; then
      [[ -e "$tmp_output" ]] && mv "$tmp_output" "$tmp_output.failed.$(date '+%Y%m%d-%H%M%S')" || true
      fail_current "mkvmerge failed with exit code $mkvmerge_status"
      return 1
    fi
    if tail -n +"$mkvmerge_log_start" "$RUN_LOG" | grep -Eiq 'audio/video synchronization may have been lost|invalid data which were skipped'; then
      review_required=1
      review_message="mkvmerge warned about skipped invalid media data; review audio/video sync before deleting source"
      log "REVIEW REQUIRED: $review_message"
    fi
  else
    log "Skipping mkvmerge because temporary output already exists"
  fi

  verify_muxed_output "$tmp_output" "$appended_subtitle_count" "$expect_default_chi" "$verify_dir" "$source_subtitle_count" || return 1

  log "Moving verified MKV to parent folder"
  mv "$tmp_output" "$target" || { fail_current "could not move output to parent: $target"; return 1; }

  if [[ "$review_required" -eq 1 ]]; then
    log "DONE_REVIEW: output verified and moved, but source movie/subtitles were kept for manual review"
    queue_update "$CURRENT_LINE_NO" "DONE_REVIEW" "$CURRENT_FOLDER" "$review_message; output=$target"
    PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
    return 0
  fi

  log "Deleting source movie and external subtitles after verification"
  rm -f "$movie"
  local delete_file
  for delete_file in "${subtitle_files[@]}"; do
    rm -f "$delete_file"
  done
  for delete_file in "${ignored[@]+"${ignored[@]}"}"; do
    rm -f "$delete_file"
  done

  find "$folder" -path '*/__MACOSX/._*' -type f -delete 2>> "$RUN_LOG" || true
  find "$folder" -mindepth 1 -depth -type d -empty -exec rmdir {} \; 2>> "$RUN_LOG" || true

  if ! rmdir "$folder"; then
    log "WARNING: output moved and source files deleted, but folder is not empty and needs review: $folder"
    find "$folder" -maxdepth 2 -print 2>/dev/null | sed 's/^/  leftover: /' | tee -a "$RUN_LOG"
    queue_update "$CURRENT_LINE_NO" "DONE_REVIEW" "$CURRENT_FOLDER" "output completed, but folder was not removed: $target"
    PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
    return 0
  fi

  log "SUCCESS: $folder"
  queue_update "$CURRENT_LINE_NO" "DONE" "$CURRENT_FOLDER" "completed $(timestamp); output=$target"
  PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
}

main() {
  : >> "$RUN_LOG"
  [[ -f "$QUEUE_FILE" ]] || { log "ERROR: queue file does not exist: $QUEUE_FILE"; exit 1; }
  MKVMERGE="$(resolve_tool "$MKVMERGE" "$LOCAL_TOOL_DIR/mkvmerge" "mkvmerge" "$KNOWN_TOOL_DIR/mkvmerge")" || { log "ERROR: mkvmerge not found"; exit 1; }
  MKVEXTRACT="$(resolve_tool "$MKVEXTRACT" "$LOCAL_TOOL_DIR/mkvextract" "mkvextract" "$KNOWN_TOOL_DIR/mkvextract")" || { log "ERROR: mkvextract not found"; exit 1; }
  log "Using mkvmerge: $MKVMERGE"
  log "Using mkvextract: $MKVEXTRACT"
  if [[ "$DRY_RUN" == "1" ]]; then
    log "DRY-RUN mode: no media files, queue rows, or names will be changed"
  else
    log "REAL RUN mode: verified outputs will be moved to parent folders; source movies/subtitles will be deleted"
  fi

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

    set +e
    process_folder "$CURRENT_FOLDER"
    process_status=$?
    set -e

    if [[ "$process_status" -ne 0 ]]; then
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
