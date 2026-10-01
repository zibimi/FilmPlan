#!/usr/bin/env python3
"""Reconcile the active film naming tracker with the mounted NAS.

The default run is a read-only preview. --execute updates only the local JSON
tracker; it never renames, moves, or deletes NAS media.
"""

import argparse
import json
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_ROOT = Path("/Volumes/分类")
DEFAULT_TRACKER = Path("/Users/milou/Documents/电影整理计划/分类审阅草案/每日命名扫描.json")
DEFAULT_EXCLUDES = {
    "体育", "公路", "冒险·灾难", "动漫改真", "宗教", "家庭", "怪兽",
    "情色", "政法委", "歌舞", "西部", "音乐", "#recycle",
}
DEFAULT_EXCLUDED_PATHS = {
    Path("/Volumes/分类/华语世界/禁"),
    Path("/Volumes/分类/合集/蚂蚁"),
}
VIDEO_EXTS = {
    ".mkv", ".mp4", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg", ".mkv1",
    ".mov", ".m4v", ".wmv", ".flv", ".ts", ".webm", ".divx", ".vob",
    ".f4v", ".ogg", ".ogv", ".dat",
}
SUBTITLE_EXTS = {".srt", ".ass", ".ssa", ".sub", ".idx", ".vtt", ".smi", ".sup"}
SUSPICIOUS_EXTS = {"", ".bin", ".raw", ".file", ".video", ".av", ".tmp"}
YEAR_RE = re.compile(r"(?<!\d)((?:18|19|20)\d{2})(?!\d)")
CHINESE_RE = re.compile(r"[\u3400-\u9fff]")
FOREIGN_RE = re.compile(r"[A-Za-z\u00c0-\u024f\u0370-\u03ff\u0400-\u04ff\u0590-\u06ff\u0900-\u097f\u0e00-\u0e7f]")
EPISODE_RE = re.compile(r"(?i)(?:^|[._ -])(?:s\d{1,2}e\d{1,3}|e\d{2,3})(?:$|[._ -])")
MULTIPART_RE = re.compile(r"(?i)(?:^|[._ -])(?:cd|disc|disk|part|pt)[._ -]*\d+(?:$|[._ -])")
EXTRA_RE = re.compile(r"(?i)(花絮|导评|访谈|采访|删减|预告|制作|extras?|bonus|commentary|interview|trailer|making[._ -]*of|featurette)")
COLLECTION_RE = re.compile(r"(?i)(合集|短片集|短片选|作品集|三部曲|anthology|collection|series)")
NOISE_RE = re.compile(r"[\[\]【】（）()]|百度|贴吧|torrents?\.|www\.|\.com\b", re.I)


def parse_args():
    parser = argparse.ArgumentParser(description="Safely refresh the active NAS film tracker")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--tracker", type=Path, default=DEFAULT_TRACKER)
    parser.add_argument("--execute", action="store_true", help="write the refreshed local tracker")
    return parser.parse_args()


def looks_like_video(path):
    try:
        with path.open("rb") as handle:
            head = handle.read(65536)
    except OSError:
        return False
    return (
        head.startswith(b"\x1aE\xdf\xa3")
        or head.startswith(b"FLV")
        or (head.startswith(b"OggS") and b"theora" in head.lower())
        or (head.startswith(b"RIFF") and head[8:12] == b"AVI ")
        or head.startswith(b"\x00\x00\x01\xba")
        or (len(head) >= 12 and head[4:8] == b"ftyp")
        or (len(head) >= 1 and head[0] == 0x47)
    )


def is_excluded(path, root):
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    if rel.parts and rel.parts[0] in DEFAULT_EXCLUDES:
        return True
    return any(path == excluded or excluded in path.parents for excluded in DEFAULT_EXCLUDED_PATHS)


def classify(path, existing):
    suffix = path.suffix.lower()
    stem = path.stem
    if suffix in SUBTITLE_EXTS:
        return "subtitle", ["related_subtitle"], "related"
    if suffix == ".dat":
        return "video", ["vcd_dat"], "review_structure"
    if EPISODE_RE.search(stem):
        return "video", ["episode"], "skip_episode"
    if MULTIPART_RE.search(stem):
        return "video", ["multipart"], "skip_multipart"
    if EXTRA_RE.search(str(path)):
        return "video", ["extra"], "skip_extra"
    if COLLECTION_RE.search(str(path)):
        return "video", ["collection_or_series"], "skip_collection_or_series"

    issues = []
    if not YEAR_RE.search(stem):
        issues.append("missing_year")
    if not CHINESE_RE.search(stem):
        accepted_foreign_only = (
            existing.get("metadata", {}).get("confidence", 0) >= 0.8
            and existing.get("metadata", {}).get("chinese_title") is None
        )
        if not accepted_foreign_only:
            issues.append("missing_chinese")
    if CHINESE_RE.search(stem) and not FOREIGN_RE.search(stem):
        issues.append("missing_foreign")
    if NOISE_RE.search(stem) or re.search(r"\s|_", stem):
        issues.append("punctuation_or_source_noise")
    if issues:
        return "video", issues, "needs_metadata_review"
    return "video", ["canonical_shape"], "done"


def earliest_original(path, actions):
    reverse = {
        action.get("new_path"): action.get("original_path")
        for action in actions
        if action.get("new_path") and action.get("original_path") != action.get("new_path")
    }
    current = path
    seen = set()
    while current in reverse and current not in seen:
        seen.add(current)
        current = reverse[current]
    return current


def scan(root):
    rows = []
    errors = []
    for base, dirs, files in os.walk(root):
        base_path = Path(base)
        dirs[:] = [name for name in dirs if not is_excluded(base_path / name, root)]
        for name in files:
            path = base_path / name
            if is_excluded(path, root):
                continue
            suffix = path.suffix.lower()
            kind = None
            if suffix == ".ogg":
                if looks_like_video(path):
                    kind = "video"
            elif suffix in VIDEO_EXTS:
                kind = "video"
            elif suffix in SUBTITLE_EXTS:
                kind = "subtitle"
            elif suffix in SUSPICIOUS_EXTS:
                try:
                    large_enough = path.stat().st_size >= 1024 * 1024
                except OSError:
                    large_enough = False
                if large_enough and looks_like_video(path):
                    kind = "video"
            if kind:
                rows.append((path, kind))
    return rows, errors


def main():
    args = parse_args()
    if not args.root.is_dir():
        raise SystemExit("NAS root is not mounted: %s" % args.root)
    if not args.tracker.is_file():
        raise SystemExit("tracker not found: %s" % args.tracker)

    data = json.loads(args.tracker.read_text(encoding="utf-8"))
    old_by_path = {item["path"]: item for item in data.get("files", [])}
    actions = data.get("executed_actions", [])
    scanned, errors = scan(args.root)
    live_paths = {str(path) for path, _ in scanned}
    old_paths = set(old_by_path)
    now = datetime.now(ZoneInfo("America/Los_Angeles")).isoformat()
    refreshed = []

    for path, detected_kind in scanned:
        path_text = str(path)
        old = dict(old_by_path.get(path_text, {}))
        try:
            stat = path.stat()
        except OSError as exc:
            errors.append({"path": path_text, "error": str(exc)})
            continue
        kind, issues, disposition = classify(path, old)
        if detected_kind == "subtitle":
            kind = "subtitle"
        old.update({
            "path": path_text,
            "original_path": old.get("original_path") or earliest_original(path_text, actions),
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
            "kind": kind,
            "issues": issues,
            "disposition": disposition,
            "synced_at": now,
        })
        refreshed.append(old)

    refreshed.sort(key=lambda item: item["path"])
    finding_counts = Counter(issue for item in refreshed if item["kind"] == "video" for issue in item.get("issues", []))
    summary = {
        "synced_at": now,
        "live_count": len(refreshed),
        "live_not_tracked_count": len(live_paths - old_paths),
        "tracked_not_live_count": len(old_paths - live_paths),
        "live_not_tracked": sorted(live_paths - old_paths),
        "tracked_not_live": sorted(old_paths - live_paths),
        "video_extensions": sorted(VIDEO_EXTS),
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not args.execute:
        print("preview_only=true; add --execute to update the local tracker")
        return

    data["files"] = refreshed
    data["counts"] = {
        "files": len(refreshed),
        "videos": sum(item["kind"] == "video" for item in refreshed),
        "subtitles": sum(item["kind"] == "subtitle" for item in refreshed),
        "other": 0,
        "errors": len(errors),
    }
    data["finding_counts"] = dict(sorted(finding_counts.items()))
    data["errors"] = errors
    data["last_updated_at"] = now
    data["last_sync"] = summary
    temp = args.tracker.with_suffix(".json.tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(args.tracker)
    print("tracker_updated=%s" % args.tracker)


if __name__ == "__main__":
    main()
