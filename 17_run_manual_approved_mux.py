#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


WORKDIR = Path(__file__).resolve().parent
LOG_DIR = WORKDIR / "logs"
QUEUE = WORKDIR / "manual_approved_mux_queue.json"
RUN_LOG = LOG_DIR / "manual-approved-mux.log"
NORMALIZED_DIR = LOG_DIR / "manual-normalized-subtitles"
VOBSUB_DIR = LOG_DIR / "manual-vobsub-pairs"

MKVMERGE = Path(os.environ.get("MKVMERGE", "/Users/milou/Documents/电影整理计划/tools/MKVToolNix.app/Contents/MacOS/mkvmerge"))
MKVEXTRACT = Path(os.environ.get("MKVEXTRACT", "/Users/milou/Documents/电影整理计划/tools/MKVToolNix.app/Contents/MacOS/mkvextract"))


def log(message: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(line, flush=True)
    with RUN_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(cmd: list[str], check: bool = True, ok_codes: tuple[int, ...] = (0,)) -> subprocess.CompletedProcess[str]:
    with RUN_LOG.open("a", encoding="utf-8") as f:
        f.write("+ " + " ".join(json.dumps(x, ensure_ascii=False) for x in cmd) + "\n")
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with RUN_LOG.open("a", encoding="utf-8") as f:
        f.write(proc.stdout)
    if check and proc.returncode not in ok_codes:
        raise RuntimeError(f"command failed with exit code {proc.returncode}: {cmd[0]}")
    return proc


def save_queue(tasks: list[dict]) -> None:
    tmp = QUEUE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(QUEUE)


def load_queue() -> list[dict]:
    return json.loads(QUEUE.read_text(encoding="utf-8"))


def inspect_tracks(path: Path) -> dict:
    proc = subprocess.run([str(MKVMERGE), "-J", str(path)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(f"could not inspect {path}: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def subtitle_count(path: Path) -> int:
    doc = inspect_tracks(path)
    return sum(1 for t in doc.get("tracks", []) if t.get("type") == "subtitles")


def text_metrics(text: str) -> dict[str, int]:
    return {
        "cjk": len(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", text)),
        "latin": len(re.findall(r"[A-Za-z]", text)),
        "replacement": text.count("\ufffd"),
        "arrows": text.count("-->") + len(re.findall(r"\d\s*->\s*\d", text)),
        "timestamps": len(re.findall(r"\d{1,2}\s*:\s*\d{1,2}\s*:\s*\d{1,2}\s*[,.]\s*\d{1,3}", text)),
        "mojibake": len(re.findall(r"[ÃÂµÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß»¼½¾]", text)),
    }


def decode_text_subtitle(path: Path, forced_lang: str | None = None) -> tuple[str, str, dict[str, int]]:
    data = path.read_bytes()
    name = path.name.lower()
    candidates = []
    if data.startswith(b"\xff\xfe"):
        candidates.append("utf-16le")
    if data.startswith(b"\xfe\xff"):
        candidates.append("utf-16be")
    if data.startswith(b"\xef\xbb\xbf"):
        candidates.append("utf-8-sig")
    candidates += ["utf-8", "utf-8-sig", "gb18030", "big5", "cp950", "utf-16le", "utf-16be", "cp1252", "cp1250", "cp1251", "iso-8859-1"]

    seen = []
    best = None
    for enc in candidates:
        if enc in seen:
            continue
        seen.append(enc)
        try:
            text = data.decode(enc)
            strict_bonus = 10000
        except UnicodeDecodeError:
            text = data.decode(enc, errors="replace")
            strict_bonus = -100000
        metrics = text_metrics(text)
        score = strict_bonus
        score += metrics["arrows"] * 50000 + metrics["timestamps"] * 1000
        score += metrics["cjk"] * 150 + metrics["latin"]
        score -= metrics["replacement"] * 100000 + metrics["mojibake"] * 400
        if path.suffix.lower() == ".srt" and (metrics["arrows"] == 0 or metrics["timestamps"] < 2):
            score -= 1000000
        if best is None or score > best[0]:
            best = (score, enc, text, metrics)
    if best is None:
        raise RuntimeError(f"no decodable text subtitle: {path}")
    _, enc, text, metrics = best
    if metrics["replacement"]:
        raise RuntimeError(f"decoded subtitle contains replacement chars: {path}")

    lower = name
    if forced_lang:
        lang = forced_lang
    elif any(x in lower for x in ("eng", "english", "英字", "英文")):
        lang = "eng"
    elif any(x in lower for x in ("spa", "spanish", ".es.")):
        lang = "spa"
    elif metrics["cjk"] > 0 and any(x in lower for x in ("chs", "cht", "chn", "中文", "中字", "简", "繁")):
        lang = "chi"
    elif metrics["cjk"] > 50:
        lang = "chi"
    elif metrics["latin"] > 100:
        lang = "eng"
    else:
        lang = "und"
    return enc, lang, metrics


def normalize_srt(text: str) -> str:
    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(
        r"(\d{1,2}\s*:\s*\d{1,2}\s*:\s*\d{1,2}\s*[,.]\s*\d{1,3})\s*->\s*(\d{1,2}\s*:\s*\d{1,2}\s*:\s*\d{1,2}\s*[,.]\s*\d{1,3})",
        r"\1 --> \2",
        text,
    )
    timing_re = re.compile(
        r"^\s*(\d{1,2})\s*:\s*(\d{1,2})\s*:\s*(\d{1,2})\s*[,.]\s*(\d{1,3})\s*-->\s*(\d{1,2})\s*:\s*(\d{1,2})\s*:\s*(\d{1,2})\s*[,.]\s*(\d{1,3})(.*)$"
    )

    def fmt(groups: tuple[str, str, str, str]) -> str:
        h, m, s, ms = groups
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{ms.strip().ljust(3, '0')[:3]}"

    blocks = re.split(r"\n\s*\n", text.strip())
    out = []
    for block in blocks:
        lines = [x.rstrip() for x in block.splitlines()]
        idx = next((i for i, line in enumerate(lines) if timing_re.match(line)), None)
        if idx is None:
            continue
        body = lines[idx + 1 :]
        if not body:
            continue
        m = timing_re.match(lines[idx])
        assert m
        timing = f"{fmt(m.group(1,2,3,4))} --> {fmt(m.group(5,6,7,8))}{m.group(9).strip()}"
        out.append(f"{len(out) + 1}\n{timing}\n" + "\n".join(body).strip())
    if not out:
        raise RuntimeError("SRT normalization found no valid cues")
    return "\n\n".join(out) + "\n"


def prepare_text_subtitle(path: Path, task_id: str, index: int, forced_lang: str | None) -> tuple[Path, str]:
    enc, lang, metrics = decode_text_subtitle(path, forced_lang)
    text = path.read_bytes().decode(enc).lstrip("\ufeff")
    if path.suffix.lower() == ".srt":
        text = normalize_srt(text)
    out_dir = NORMALIZED_DIR / task_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"subtitle_{index}_{lang}{path.suffix.lower()}"
    out.write_text(text, encoding="utf-8")
    log(f"Subtitle charset={enc} lang={lang} cjk={metrics['cjk']} repl={metrics['replacement']} mojibake={metrics['mojibake']} file={path}")
    return out, lang


def find_sidecar(idx: Path, explicit_sidecar: str | None, task_id: str, index: int) -> Path:
    if explicit_sidecar:
        sidecar = Path(explicit_sidecar)
    else:
        sidecar = idx.with_suffix(".sub")
    if sidecar.exists() and sidecar.with_suffix("").name == idx.with_suffix("").name:
        return idx
    if not sidecar.exists():
        raise RuntimeError(f"VobSub sidecar missing: idx={idx} sub={sidecar}")
    out_dir = VOBSUB_DIR / task_id / f"sub_{index}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_idx = out_dir / "subtitle.idx"
    out_sub = out_dir / "subtitle.sub"
    shutil.copy2(idx, out_idx)
    shutil.copy2(sidecar, out_sub)
    return out_idx


def lang_name(lang: str) -> str:
    return {
        "chi": "Chinese",
        "eng": "English",
        "spa": "Spanish",
        "ita": "Italian",
        "deu": "German",
        "rus": "Russian",
    }.get(lang, "Subtitle")


def verify_output(output: Path, source_subs: int, appended: int, expect_chi: bool, verify_dir: Path) -> None:
    doc = inspect_tracks(output)
    subs = [t for t in doc.get("tracks", []) if t.get("type") == "subtitles"]
    appended_tracks = subs[source_subs:]
    default_chi = 0
    for t in subs:
        p = t.get("properties", {})
        lang = p.get("language", "")
        ietf = p.get("language_ietf", "")
        if p.get("default_track") and (lang in ("chi", "zho") or ietf.startswith("zh")):
            default_chi += 1
    log(f"Verification: subtitle_tracks={len(subs)} appended={len(appended_tracks)} default_chinese={default_chi}")
    if len(appended_tracks) < appended:
        raise RuntimeError(f"verification failed: expected {appended} appended subtitle tracks, found {len(appended_tracks)}")
    if expect_chi and default_chi < 1:
        raise RuntimeError("verification failed: no default Chinese subtitle track")
    verify_dir.mkdir(parents=True, exist_ok=True)
    for t in appended_tracks:
        tid = t["id"]
        p = t.get("properties", {})
        codec = p.get("codec_id", "")
        lang = p.get("language", "")
        if not codec.startswith("S_TEXT/"):
            log(f"Verification: track={tid} codec={codec}; non-text, skip extraction")
            continue
        out = verify_dir / f"track_{tid}.srt"
        run([str(MKVEXTRACT), "tracks", str(output), f"{tid}:{out}"])
        text = out.read_text(encoding="utf-8", errors="replace")
        metrics = text_metrics(text)
        log(f"Verification: extracted track={tid} lang={lang} cjk={metrics['cjk']} repl={metrics['replacement']}")
        if metrics["replacement"]:
            raise RuntimeError(f"verification failed: extracted track {tid} has replacement chars")
        if lang in ("chi", "zho") and metrics["cjk"] < 1:
            raise RuntimeError(f"verification failed: Chinese track {tid} has no CJK")


def process_task(task: dict) -> None:
    folder = Path(task["folder"])
    movie = Path(task["movie"])
    task_id = str(task["id"])
    keep_source = bool(task.get("keep_source", False))
    delete_extra = [Path(x) for x in task.get("delete_extra", [])]
    ignore_leftovers = bool(task.get("ignore_leftovers", False))
    keep_folder = bool(task.get("keep_folder", False)) or ignore_leftovers

    if not folder.exists():
        raise RuntimeError(f"folder missing: {folder}")
    if not movie.exists():
        raise RuntimeError(f"movie missing: {movie}")
    target = Path(task.get("target") or ((folder / f"{movie.stem}.mkv") if keep_folder else (folder.parent / f"{movie.stem}.mkv")))
    replacing_source = target == movie
    if target.exists() and not replacing_source:
        raise RuntimeError(f"target already exists: {target}")
    tmp = folder / f".{movie.stem}.manual.muxing.mkv"
    if tmp.exists():
        log(f"Removing stale temp from previous interrupted run: {tmp}")
        tmp.unlink()

    source_subs = subtitle_count(movie)
    cmd = [str(MKVMERGE), "--output", str(tmp), str(movie)]
    cleanup_files: list[Path] = [movie]
    appended = 0
    expect_chi = False
    has_default_chi = False

    for index, sub in enumerate(task["subtitles"], 1):
        sub_path = Path(sub["path"])
        if not sub_path.exists():
            raise RuntimeError(f"subtitle missing: {sub_path}")
        if sub_path.suffix.lower() == ".idx":
            prepared = find_sidecar(sub_path, sub.get("sidecar"), task_id, index)
            lang = sub.get("lang") or "und"
            cleanup_files.append(sub_path)
            sidecar = Path(sub.get("sidecar") or str(sub_path.with_suffix(".sub")))
            if sidecar.exists():
                cleanup_files.append(sidecar)
        else:
            prepared, lang = prepare_text_subtitle(sub_path, task_id, index, sub.get("lang"))
            cleanup_files.append(sub_path)
        default = "no"
        if lang == "chi" and not has_default_chi:
            default = "yes"
            has_default_chi = True
            expect_chi = True
        elif lang == "und" and len(task["subtitles"]) == 1:
            default = "yes"
        cmd += ["--language", f"0:{lang}", "--track-name", f"0:{lang_name(lang)}", "--default-track-flag", f"0:{default}", str(prepared)]
        appended += 1

    log(f"Folder: {folder}")
    log(f"Movie: {movie}")
    log(f"Target: {target}")
    log(f"Subtitles: {appended}")
    estimated = movie.stat().st_size * 2
    log(f"Estimated NAS SMB traffic: about {estimated} bytes ({estimated / 1024 / 1024 / 1024:.2f} GiB), plus overhead")
    run(cmd, ok_codes=(0, 1))
    verify_output(tmp, source_subs, appended, expect_chi, LOG_DIR / f"manual-verify-{task_id}")
    if replacing_source:
        movie.unlink()
    tmp.rename(target)
    log(f"Moved verified output: {target}")

    if keep_source:
        task["status"] = "DONE_REVIEW"
        task["message"] = f"output completed; source kept for review; output={target}"
        return

    for p in cleanup_files + delete_extra:
        if replacing_source and p == movie:
            continue
        if p.exists() and p.is_file():
            p.unlink()
    if keep_folder:
        task["status"] = "DONE_REVIEW" if ignore_leftovers else "DONE"
        task["message"] = f"completed in original folder; leftovers preserved; output={target}"
        return
    for child in sorted(folder.rglob("__MACOSX"), reverse=True):
        if child.is_dir():
            shutil.rmtree(child, ignore_errors=True)
    for child in sorted(folder.rglob("*"), key=lambda x: len(x.parts), reverse=True):
        if child.is_dir():
            try:
                child.rmdir()
            except OSError:
                pass
    try:
        folder.rmdir()
        task["status"] = "DONE"
        task["message"] = f"completed; output={target}"
    except OSError:
        task["status"] = "DONE_REVIEW" if ignore_leftovers else "DONE_REVIEW"
        task["message"] = f"output completed, folder not empty; output={target}"


def main() -> int:
    tasks = load_queue()
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)
    VOBSUB_DIR.mkdir(parents=True, exist_ok=True)
    for task in tasks:
        if task.get("status") != "PENDING":
            continue
        log(f"Next manual task: {task['id']}")
        try:
            process_task(task)
            log(f"{task['status']}: {task['folder']}")
        except Exception as exc:
            task["status"] = "FAILED"
            task["message"] = str(exc)
            log(f"ERROR: {task['folder']} :: {exc}")
        finally:
            save_queue(tasks)
    log("No PENDING manual tasks left")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
