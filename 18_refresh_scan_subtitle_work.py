#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path


WORKDIR = Path(__file__).resolve().parent
PLAN_DIR = WORKDIR / "rescan-plan"
QUEUE = PLAN_DIR / "refresh_mux_queue.json"
CLEANUP = PLAN_DIR / "refresh_cleanup_actions.json"
REPORT = PLAN_DIR / "refresh_report.md"
RUN_LOG = WORKDIR / "logs" / "refresh-mux.log"

ROOTS = [Path("/Volumes/导演们"), Path("/Volumes/分类")]
MOVIE_EXTS = {".mkv", ".mp4", ".avi", ".rmvb", ".rm", ".mov", ".m4v"}
TEXT_SUB_EXTS = {".srt", ".ass", ".ssa"}
VOBSUB_EXTS = {".idx", ".sub"}
JUNK_NAMES = {".DS_Store", "Thumbs.db"}
SKIP_DIR_NAMES = {
    "__MACOSX",
    "@eaDir",
    ".AppleDouble",
    "#recycle",
    "#snapshot",
    ".Trashes",
}
EXTRA_DIR_RE = re.compile(r"(花絮|特典|extra|extras|bonus|making|interview|访谈|采访|幕后|制作)", re.I)


def natural_key(path: Path) -> tuple:
    return tuple(int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", str(path)))


def visible_file(path: Path) -> bool:
    return path.is_file() and not path.name.startswith(".") and path.name not in JUNK_NAMES


def is_movie(path: Path) -> bool:
    return visible_file(path) and path.suffix.lower() in MOVIE_EXTS and not path.name.startswith("OG.")


def is_text_sub(path: Path) -> bool:
    return visible_file(path) and path.suffix.lower() in TEXT_SUB_EXTS


def is_idx(path: Path) -> bool:
    return visible_file(path) and path.suffix.lower() == ".idx"


def is_sub(path: Path) -> bool:
    return visible_file(path) and path.suffix.lower() == ".sub"


def norm(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\[[^\]]+\]|\([^)]*\)", " ", text)
    text = re.sub(r"(1080p|720p|480p|bluray|brrip|dvdrip|webrip|xvid|x264|x265|h264|h265|ac3|aac|dts|proper|limited|internal|repack)", " ", text)
    return re.sub(r"[^0-9a-z\u3400-\u9fff]+", "", text)


def part_token(path: Path) -> str | None:
    name = path.stem.lower()
    patterns = [
        r"(?:^|[^a-z0-9])cd\s*0*([1-9][0-9]?)(?:[^a-z0-9]|$)",
        r"(?:^|[^a-z0-9])disc\s*0*([1-9][0-9]?)(?:[^a-z0-9]|$)",
        r"(?:^|[^a-z0-9])disk\s*0*([1-9][0-9]?)(?:[^a-z0-9]|$)",
        r"(?:^|[^a-z0-9])part\s*0*([1-9][0-9]?)(?:[^a-z0-9]|$)",
        r"(?:^|[^a-z0-9])pt\s*0*([1-9][0-9]?)(?:[^a-z0-9]|$)",
        r"(?:^|[^a-z0-9])ep\s*0*([1-9][0-9]?)(?:[^a-z0-9]|$)",
        r"(?:^|[^a-z0-9])e\s*0*([1-9][0-9]?)(?:[^a-z0-9]|$)",
    ]
    for pat in patterns:
        m = re.search(pat, name)
        if m:
            return m.group(1).lstrip("0") or "0"
    if re.search(r"(?:^|[^0-9])0?([1-9])(?:[^0-9]|$)", name):
        return re.search(r"(?:^|[^0-9])0?([1-9])(?:[^0-9]|$)", name).group(1)
    return None


def lang_for(path: Path) -> str | None:
    lower = path.name.lower()
    if re.search(r"(^|[._\-\s])(en|eng|english)([._\-\s]|$)", lower) or any(x in lower for x in ("英文", "英字")):
        return "eng"
    if re.search(r"(^|[._\-\s])(chs|cht|chi|chn)([._\-\s]|$)", lower) or any(x in lower for x in ("中文", "中字", "简", "繁")):
        return "chi"
    if re.search(r"(^|[._\-\s])(rus|russian)([._\-\s]|$)", lower) or any(x in lower for x in ("俄文", "俄语")):
        return "rus"
    return None


def sidecar_for(idx: Path, subs: list[Path]) -> Path | None:
    same = idx.with_suffix(".sub")
    if same.exists():
        return same
    idx_norm = norm(idx.stem)
    choices = [s for s in subs if norm(s.stem) == idx_norm]
    if len(choices) == 1:
        return choices[0]
    return None


def paired_vobsubs(idxs: list[Path], subs: list[Path]) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    used: set[Path] = set()
    for idx in idxs:
        sidecar = sidecar_for(idx, subs)
        if sidecar and sidecar not in used:
            pairs.append((idx, sidecar))
            used.add(sidecar)
    if not pairs and len(idxs) == 1 and len(subs) == 1:
        pairs.append((idxs[0], subs[0]))
    return pairs


def score_match(movie: Path, subtitle: Path, multi: bool) -> int:
    ms = norm(movie.stem)
    ss = norm(subtitle.stem)
    score = 0
    if ms and ss and (ms in ss or ss in ms):
        score += 100
    mt = part_token(movie)
    st = part_token(subtitle)
    if mt and st and mt == st:
        score += 200
    elif multi and (mt or st):
        score -= 200
    common = set(re.findall(r"[a-z]{4,}|\d{4}", movie.stem.lower())) & set(re.findall(r"[a-z]{4,}|\d{4}", subtitle.stem.lower()))
    score += len(common) * 10
    return score


def match_text_subs(movie: Path, subs: list[Path], multi: bool) -> list[Path]:
    matched = []
    for sub in subs:
        score = score_match(movie, sub, multi)
        if not multi and score >= 0:
            matched.append(sub)
        elif multi and score >= 210:
            matched.append(sub)
    return sorted(matched, key=natural_key)


def match_vobsubs(movie: Path, pairs: list[tuple[Path, Path]], multi: bool) -> list[tuple[Path, Path]]:
    matched = []
    for idx, sidecar in pairs:
        score = score_match(movie, idx, multi)
        if not multi and score >= 0:
            matched.append((idx, sidecar))
        elif multi and score >= 210:
            matched.append((idx, sidecar))
    return sorted(matched, key=lambda x: natural_key(x[0]))


def folder_has_real_subdir(folder: Path) -> bool:
    for child in folder.iterdir():
        if child.is_dir() and not child.name.startswith(".") and child.name not in SKIP_DIR_NAMES:
            return True
    return False


def should_skip_folder(folder: Path) -> bool:
    for part in folder.parts:
        if part in SKIP_DIR_NAMES or part.startswith("."):
            return True
    return bool(EXTRA_DIR_RE.search(folder.name))


def remaining_regular_items(folder: Path, deleting: set[Path]) -> list[Path]:
    items = []
    for child in folder.iterdir():
        if child in deleting:
            continue
        if child.name in JUNK_NAMES or child.name in SKIP_DIR_NAMES:
            continue
        if child.name.startswith("."):
            continue
        items.append(child)
    return items


def scan(roots: list[Path] | None = None, include_single: bool = False) -> tuple[list[dict], list[dict], list[dict]]:
    tasks: list[dict] = []
    cleanup: list[dict] = []
    review: list[dict] = []
    seen_task_keys: set[tuple[str, str]] = set()
    task_no = 1
    cleanup_no = 1

    for root in roots or ROOTS:
        if not root.exists():
            review.append({"kind": "missing_root", "path": str(root)})
            continue
        for folder in sorted([p for p in root.rglob("*") if p.is_dir()], key=natural_key):
            if should_skip_folder(folder):
                continue
            try:
                children = list(folder.iterdir())
            except OSError as exc:
                review.append({"kind": "unreadable", "path": str(folder), "reason": str(exc)})
                continue
            movies = sorted([p for p in children if is_movie(p)], key=natural_key)
            if not movies:
                continue
            text_subs = sorted([p for p in children if is_text_sub(p)], key=natural_key)
            idxs = sorted([p for p in children if is_idx(p)], key=natural_key)
            raw_subs = sorted([p for p in children if is_sub(p)], key=natural_key)
            pairs = paired_vobsubs(idxs, raw_subs)
            paired_idx = {idx for idx, _ in pairs}
            paired_sub = {sub for _, sub in pairs}
            orphan_vob = [p for p in idxs + raw_subs if p not in paired_idx and p not in paired_sub]
            multi = len(movies) > 1
            tokens = [part_token(m) for m in movies]
            has_parts = len({t for t in tokens if t}) >= 2
            all_movies_have_tokens = bool(movies) and all(tokens)
            duplicate_tokens = [token for token, count in Counter(t for t in tokens if t).items() if count > 1]
            has_external_subtitle_candidates = bool(text_subs or pairs or orphan_vob)
            if duplicate_tokens and has_external_subtitle_candidates:
                review.append({
                    "kind": "multi_duplicate_part_tokens_skipped",
                    "folder": str(folder),
                    "duplicate_tokens": duplicate_tokens,
                    "movies": [str(p) for p in movies],
                })
                continue

            folder_tasks = []
            for movie in movies:
                subs_payload = []
                for sub in match_text_subs(movie, text_subs, multi):
                    payload = {"path": str(sub)}
                    lang = lang_for(sub)
                    if lang:
                        payload["lang"] = lang
                    subs_payload.append(payload)
                for idx, sidecar in match_vobsubs(movie, pairs, multi):
                    payload = {"path": str(idx), "sidecar": str(sidecar)}
                    lang = lang_for(idx)
                    if lang:
                        payload["lang"] = lang
                    subs_payload.append(payload)
                if not subs_payload:
                    continue
                key = (str(folder), str(movie))
                if key in seen_task_keys:
                    continue
                seen_task_keys.add(key)
                category = "single"
                if multi and any(re.search(r"cd\s*0*[12]", m.name, re.I) for m in movies):
                    category = "cd"
                elif multi and has_parts:
                    category = "multi"
                elif any(s["path"].lower().endswith(".idx") for s in subs_payload):
                    category = "vobsub"
                if category == "single" and not include_single:
                    review.append({
                        "kind": "single_text_subtitle_skipped",
                        "folder": str(folder),
                        "movie": str(movie),
                        "subtitles": [s["path"] for s in subs_payload],
                    })
                    continue
                if multi and not all_movies_have_tokens:
                    review.append({
                        "kind": "multi_without_clear_tokens_skipped",
                        "folder": str(folder),
                        "movies": [str(p) for p in movies],
                    })
                    continue
                if category in {"cd", "multi"} and part_token(movie) is None:
                    review.append({
                        "kind": "part_movie_without_token_skipped",
                        "folder": str(folder),
                        "movie": str(movie),
                    })
                    continue
                keep_folder = folder_has_real_subdir(folder) or category in {"cd", "multi"}
                target = folder.parent / f"{movie.stem}.mkv"
                if keep_folder:
                    target = folder / f"{movie.stem}.mkv"
                if target.exists() and target != movie:
                    review.append({
                        "kind": "target_exists_skipped",
                        "folder": str(folder),
                        "movie": str(movie),
                        "target": str(target),
                    })
                    continue
                task = {
                    "id": f"refresh-{task_no:04d}",
                    "status": "PENDING",
                    "category": category,
                    "folder": str(folder),
                    "movie": str(movie),
                    "target": str(target),
                    "subtitles": subs_payload,
                    "keep_source": movie.suffix.lower() in {".rmvb", ".rm"},
                    "keep_folder": keep_folder,
                    "ignore_leftovers": keep_folder,
                    "note": "generated by 18_refresh_scan_subtitle_work.py",
                }
                folder_tasks.append(task)
                task_no += 1
            if multi and folder_tasks:
                matched_movies = {Path(t["movie"]) for t in folder_tasks}
                missing_movies = [m for m in movies if m not in matched_movies]
                if missing_movies:
                    review.append({
                        "kind": "multi_partial_match_skipped",
                        "folder": str(folder),
                        "matched_movies": [str(p) for p in sorted(matched_movies, key=natural_key)],
                        "missing_movies": [str(p) for p in missing_movies],
                    })
                    folder_tasks = []
            tasks.extend(folder_tasks)

            if not folder_tasks and orphan_vob:
                deleting = set(orphan_vob)
                regular = remaining_regular_items(folder, deleting)
                remaining_movies = [p for p in regular if is_movie(p)]
                if len(remaining_movies) == 1 and len(regular) == 1:
                    movie = remaining_movies[0]
                    cleanup.append({
                        "id": f"cleanup-{cleanup_no:04d}",
                        "status": "PENDING",
                        "folder": str(folder),
                        "movie": str(movie),
                        "target": str(folder.parent / movie.name),
                        "delete_files": [str(p) for p in sorted(orphan_vob, key=natural_key)],
                        "reason": "orphan idx/sub files; folder will contain only one movie after deletion",
                    })
                    cleanup_no += 1
                else:
                    review.append({
                        "kind": "orphan_idx_sub_not_cleaned",
                        "folder": str(folder),
                        "movies": [str(p) for p in movies],
                        "orphan_files": [str(p) for p in orphan_vob],
                        "remaining_items_after_delete": [str(p) for p in regular],
                    })
            elif folder_tasks and orphan_vob:
                for task in folder_tasks:
                    task.setdefault("delete_extra", [])
                    task["delete_extra"].extend(str(p) for p in orphan_vob)

    return tasks, cleanup, review


def write_outputs(tasks: list[dict], cleanup: list[dict], review: list[dict]) -> None:
    PLAN_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CLEANUP.write_text(json.dumps(cleanup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = Counter(t.get("category", "unknown") for t in tasks)
    lines = [
        "# Refresh subtitle work report",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Summary",
        "",
        f"- Mux tasks: {len(tasks)}",
        f"- Cleanup-only actions: {len(cleanup)}",
        f"- Review items: {len(review)}",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- {key}: {value}")
    lines += ["", "## Mux Tasks", ""]
    for task in tasks:
        lines.append(f"- {task['id']} [{task['category']}] {task['folder']}")
        lines.append(f"  - movie: {Path(task['movie']).name}")
        lines.append(f"  - subtitles: {len(task['subtitles'])}")
        lines.append(f"  - target: {task['target']}")
        if task.get("keep_folder"):
            lines.append("  - keep_folder: yes")
        if task.get("keep_source"):
            lines.append("  - keep_source: yes")
    lines += ["", "## Cleanup Actions", ""]
    for action in cleanup:
        lines.append(f"- {action['id']} {action['folder']}")
        lines.append(f"  - movie: {Path(action['movie']).name}")
        lines.append(f"  - delete: {', '.join(Path(p).name for p in action['delete_files'])}")
        lines.append(f"  - target: {action['target']}")
    lines += ["", "## Review Items", ""]
    for item in review:
        lines.append(f"- {item.get('kind')}: {item.get('folder') or item.get('path')}")
        if item.get("reason"):
            lines.append(f"  - reason: {item['reason']}")
        if item.get("orphan_files"):
            lines.append(f"  - orphan: {', '.join(Path(p).name for p in item['orphan_files'])}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_mux_queue() -> int:
    env = os.environ.copy()
    env["MUX_QUEUE"] = str(QUEUE)
    env["MUX_RUN_LOG"] = str(RUN_LOG)
    return subprocess.call([sys.executable, str(WORKDIR / "17_run_manual_approved_mux.py")], env=env)


def apply_cleanup() -> None:
    actions = json.loads(CLEANUP.read_text(encoding="utf-8"))
    changed = False
    for action in actions:
        if action.get("status") != "PENDING":
            continue
        folder = Path(action["folder"])
        movie = Path(action["movie"])
        target = Path(action["target"])
        delete_files = [Path(p) for p in action["delete_files"]]
        if not folder.exists() or not movie.exists():
            action["status"] = "FAILED"
            action["message"] = "folder or movie missing"
            changed = True
            continue
        if target.exists():
            action["status"] = "FAILED"
            action["message"] = f"target exists: {target}"
            changed = True
            continue
        for p in delete_files:
            if p.parent != folder or p.suffix.lower() not in VOBSUB_EXTS:
                action["status"] = "FAILED"
                action["message"] = f"unsafe delete path: {p}"
                changed = True
                break
        if action.get("status") == "FAILED":
            continue
        for p in delete_files:
            if p.exists():
                p.unlink()
        for child in folder.iterdir():
            if child.name in JUNK_NAMES and child.is_file():
                child.unlink()
        remaining = [p for p in folder.iterdir() if not p.name.startswith(".") and p.name not in JUNK_NAMES]
        if len(remaining) != 1 or remaining[0] != movie:
            action["status"] = "FAILED"
            action["message"] = "folder did not reduce to exactly one movie"
            changed = True
            continue
        movie.rename(target)
        folder.rmdir()
        action["status"] = "DONE"
        action["message"] = f"moved movie and removed folder; output={target}"
        changed = True
    if changed:
        CLEANUP.write_text(json.dumps(actions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="run mux queue and cleanup actions after scanning")
    parser.add_argument("--root", action="append", help="scan only this root/category path; can be passed more than once")
    parser.add_argument("--prefix", help="write queue/report files with this prefix under rescan-plan")
    parser.add_argument("--include-single", action="store_true", help="include single movie folders with matched external subtitles")
    args = parser.parse_args()
    global QUEUE, CLEANUP, REPORT, RUN_LOG
    if args.prefix:
        safe_prefix = re.sub(r"[^0-9A-Za-z_.-]+", "_", args.prefix).strip("_")
        if not safe_prefix:
            raise SystemExit("--prefix produced an empty safe filename")
        QUEUE = PLAN_DIR / f"{safe_prefix}_mux_queue.json"
        CLEANUP = PLAN_DIR / f"{safe_prefix}_cleanup_actions.json"
        REPORT = PLAN_DIR / f"{safe_prefix}_report.md"
        RUN_LOG = WORKDIR / "logs" / f"{safe_prefix}-mux.log"
    roots = [Path(p) for p in args.root] if args.root else None
    tasks, cleanup, review = scan(roots, include_single=args.include_single)
    write_outputs(tasks, cleanup, review)
    print(f"report: {REPORT}")
    print(f"mux tasks: {len(tasks)}")
    print(f"cleanup actions: {len(cleanup)}")
    print(f"review items: {len(review)}")
    if not args.apply:
        return 0
    code = run_mux_queue()
    apply_cleanup()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
