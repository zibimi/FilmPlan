#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path


ROOTS = [Path("/Volumes/分类"), Path("/Volumes/导演们")]
WORKDIR = Path("/Users/milou/Documents/电影整理计划")
MKVMERGE = WORKDIR / "tools/MKVToolNix.app/Contents/MacOS/mkvmerge"
MEDIA_EXTS = {".mkv", ".mp4", ".avi", ".flv"}
SUB_EXTS = {".srt", ".ass", ".ssa", ".sub", ".idx", ".sup", ".smi", ".vtt"}
CD_RE = re.compile(r"(?i)(?<![a-z0-9])cd\s*0?[12](?![a-z0-9])")
PATTERNS = [
    ("part", re.compile(r"(?i)(?<![a-z0-9])(?:part|pt|disc|disk|dvd)\s*0?([1-9])(?![a-z0-9])")),
    ("numeric", re.compile(r"(?i)(?:^|[\s._\-\[\]()（）【】])0?([1-9])(?:$|[\s._\-\[\]()（）【】])")),
]
SEP_RE = re.compile(r"[\s._\-+\[\]（）()【】]+")
NOISE_RE = re.compile(r"(?i)(cd\s*0?[1-9]|part\s*0?[1-9]|pt\s*0?[1-9]|disc\s*0?[1-9]|disk\s*0?[1-9]|dvd\s*0?[1-9])")
NUM_NOISE_RE = re.compile(r"(?i)(?:^|[\s._\-\[\]()（）【】])0?[1-9](?:$|[\s._\-\[\]()（）【】])")


def clean_base(name, kind):
    stem = Path(name).stem
    stem = NOISE_RE.sub(" ", stem)
    if kind == "numeric":
        stem = NUM_NOISE_RE.sub(" ", stem)
    return SEP_RE.sub(" ", stem).strip().lower()


def classify(candidate):
    directory = str(candidate["dir"]).lower()
    base = candidate["base"].lower()
    names = " ".join(path.name for path in candidate["files"]).lower()
    if "/video_ts" in directory or candidate["ext"] == ".vob":
        return "dvd_raw_vob"
    if any(token in base or token in names for token in ["extras", "extra", "花絮", "shorts", "collected shorts"]):
        return "extras_or_shorts"
    if candidate["kind"] == "numeric" and any(
        token in base or token in names for token in ["episode", "集", "长路", "century of revolution", "雷曼三部曲", "trilogy"]
    ):
        return "episodes_or_program_parts"
    return "likely_feature_or_main_work"


def output_stem(name, kind):
    stem = Path(name).stem
    stem = NOISE_RE.sub(" ", stem)
    if kind == "numeric":
        stem = NUM_NOISE_RE.sub(" ", stem)
    return stem.strip(" ._-+[]【】()（）") or Path(name).stem


def unique_path(path):
    if not path.exists():
        return path
    for index in range(2, 1000):
        candidate = path.with_name(f"{path.stem}.merged-{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Cannot find unique output path for {path}")


def mkv_info(path):
    result = subprocess.run(
        [str(MKVMERGE), "-J", str(path)],
        cwd=str(WORKDIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"mkvmerge cannot read {path}")
    return json.loads(result.stdout)


def duration_ns(data):
    return int(data.get("container", {}).get("properties", {}).get("duration") or 0)


def track_signature(data):
    signature = []
    for track in data.get("tracks", []):
        props = track.get("properties", {})
        kind = track.get("type")
        if kind == "video":
            details = (props.get("pixel_dimensions"), props.get("display_dimensions"))
        elif kind == "audio":
            details = (props.get("audio_channels"), props.get("audio_sampling_frequency"))
        else:
            details = ()
        signature.append((kind, track.get("codec"), props.get("codec_id"), details))
    return signature


def subtitle_tracks(data):
    labels = []
    for track in data.get("tracks", []):
        if track.get("type") == "subtitles":
            props = track.get("properties", {})
            lang = props.get("language_ietf") or props.get("language") or "und"
            name = props.get("track_name") or ""
            labels.append(f"{lang}/{name}" if name else lang)
    return labels


def scan():
    candidates = []
    for root in ROOTS:
        for dirpath, _dirnames, filenames in os.walk(root):
            folder = Path(dirpath)
            if "#recycle" in folder.parts:
                continue
            external_subs = sorted(
                [name for name in filenames if Path(name).suffix.lower() in SUB_EXTS],
                key=str.lower,
            )
            entries = []
            for name in filenames:
                ext = Path(name).suffix.lower()
                if ext not in MEDIA_EXTS or CD_RE.search(name):
                    continue
                for kind, regex in PATTERNS:
                    match = regex.search(name)
                    if not match:
                        continue
                    base = clean_base(name, kind)
                    if kind == "numeric" and (not base or len(base) < 3):
                        continue
                    entries.append(
                        {
                            "path": folder / name,
                            "ext": ext,
                            "part": match.group(1),
                            "kind": kind,
                            "base": base,
                        }
                    )
                    break
            groups = {}
            for entry in entries:
                groups.setdefault((entry["kind"], entry["ext"], entry["base"]), []).append(entry)
            for (kind, ext, base), group in groups.items():
                part_numbers = {int(entry["part"]) for entry in group}
                if 1 in part_numbers and 2 in part_numbers:
                    files = [entry["path"] for entry in sorted(group, key=lambda e: (e["part"], e["path"].name.lower()))]
                    candidate = {
                        "dir": folder,
                        "kind": kind,
                        "ext": ext,
                        "base": base,
                        "files": files,
                        "external_subtitles": external_subs,
                    }
                    if classify(candidate) == "likely_feature_or_main_work":
                        candidates.append(candidate)
    return candidates


def candidate_key(candidate):
    return tuple(str(path) for path in candidate["files"])


def load_manifest(path):
    allowed = set()
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    for item in data.get("candidates", []):
        files = item.get("files") or []
        if len(files) >= 2:
            allowed.add(tuple(files))
    return allowed


def write_manifest(path, candidates):
    data = {
        "root_scan": [str(root) for root in ROOTS],
        "candidate_count": len(candidates),
        "candidates": [
            {
                "dir": str(candidate["dir"]),
                "kind": candidate["kind"],
                "ext": candidate["ext"],
                "base": candidate["base"],
                "files": [str(path) for path in candidate["files"]],
                "external_subtitles": candidate["external_subtitles"],
            }
            for candidate in candidates
        ],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def real_non_part_entries(folder, part_paths, output):
    ignored = {".ds_store", "thumbs.db", "desktop.ini"}
    part_set = {path.resolve() for path in part_paths}
    output_resolved = output.resolve() if output.exists() else None
    entries = []
    for item in folder.iterdir():
        if item.name.lower() in ignored:
            continue
        try:
            resolved = item.resolve()
        except Exception:
            resolved = item
        if resolved in part_set:
            continue
        if output_resolved is not None and resolved == output_resolved:
            continue
        entries.append(item)
    return entries


def merge_candidate(candidate, dry_run):
    folder = candidate["dir"]
    files = candidate["files"]
    numbered_files = []
    for path in files:
        matches = [(regex.search(path.name), regex) for _kind, regex in PATTERNS]
        parts = [int(match.group(1)) for match, _regex in matches if match]
        if parts:
            numbered_files.append((parts[0], path))
    part_counts = {}
    for number, _path in numbered_files:
        part_counts[number] = part_counts.get(number, 0) + 1
    numbers = sorted(part_counts)
    if numbers != list(range(1, max(numbers) + 1)) or any(count != 1 for count in part_counts.values()):
        return {"status": "skipped", "reason": "non_sequential_or_duplicate_part_files", "dir": str(folder)}

    ordered_parts = [path for _number, path in sorted(numbered_files)]
    infos = [mkv_info(path) for path in ordered_parts]
    if any(track_signature(info) != track_signature(infos[0]) for info in infos[1:]):
        return {
            "status": "skipped",
            "reason": "track_mismatch",
            "dir": str(folder),
            "files": [path.name for path in ordered_parts],
        }

    output = unique_path(folder / f"{output_stem(ordered_parts[0].name, candidate['kind'])}.mkv")
    extras = real_non_part_entries(folder, ordered_parts, output)
    action = "keep_folder_delete_part_files" if extras else "move_to_parent_delete_folder"
    result_base = {
        "label": output.stem,
        "dir": str(folder),
        "output": str(output),
        "ext": candidate["ext"],
        "kind": candidate["kind"],
        "action": action,
        "files": [path.name for path in ordered_parts],
        "external_subtitles": candidate["external_subtitles"],
        "embedded_subtitles": sorted({label for info in infos for label in subtitle_tracks(info)}),
    }
    if dry_run:
        return {"status": "would_process", **result_base}

    result = subprocess.run(
        [str(MKVMERGE), "-o", str(output), str(ordered_parts[0])] + [item for path in ordered_parts[1:] for item in ["+", str(path)]],
        cwd=str(WORKDIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode not in (0, 1) or not output.exists():
        if output.exists():
            output.unlink()
        return {"status": "failed", "reason": "merge_failed", **result_base, "detail": result.stdout[-2000:]}

    merged = mkv_info(output)
    expected = sum(duration_ns(info) for info in infos)
    actual = duration_ns(merged)
    if expected and actual + 2_000_000_000 < expected:
        if output.exists():
            output.unlink()
        return {
            "status": "failed",
            "reason": "duration_short",
            **result_base,
            "expected_seconds": round(expected / 1_000_000_000, 3),
            "actual_seconds": round(actual / 1_000_000_000, 3),
        }

    final_output = output
    if action == "move_to_parent_delete_folder":
        final_output = unique_path(folder.parent / output.name)
        shutil.move(str(output), str(final_output))

    for path in ordered_parts:
        path.unlink()

    if action == "move_to_parent_delete_folder":
        for item in list(folder.iterdir()):
            if item.name.lower() in {".ds_store", "thumbs.db", "desktop.ini"}:
                item.unlink()
        if not any(folder.iterdir()):
            folder.rmdir()
        else:
            return {
                "status": "partial",
                "reason": "folder_not_empty_after_cleanup",
                **result_base,
                "output": str(final_output),
                "remaining": [item.name for item in folder.iterdir()],
            }

    return {
        "status": "processed",
        **result_base,
        "output": str(final_output),
        "duration_seconds": round(actual / 1_000_000_000, 3) if actual else None,
        "embedded_subtitles": sorted(set(subtitle_tracks(merged))),
        "mkvmerge_warning": result.returncode == 1,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--write-manifest", type=Path)
    args = parser.parse_args()
    dry_run = not args.execute
    candidates = scan()
    if args.write_manifest:
        write_manifest(args.write_manifest, candidates)
    if args.manifest:
        allowed = load_manifest(args.manifest)
        candidates = [candidate for candidate in candidates if candidate_key(candidate) in allowed]
    results = []
    for index, candidate in enumerate(candidates, 1):
        try:
            result = merge_candidate(candidate, dry_run)
        except Exception as exc:
            result = {
                "status": "failed",
                "reason": type(exc).__name__,
                "dir": str(candidate["dir"]),
                "detail": str(exc),
            }
        results.append(result)
        if args.execute:
            print(json.dumps({"index": index, **result}, ensure_ascii=False), flush=True)
    counts = {}
    for result in results:
        key = result["status"] if result["status"] != "skipped" else f"skipped:{result.get('reason')}"
        counts[key] = counts.get(key, 0) + 1
    summary = {
        "mode": "execute" if args.execute else "dry_run",
        "total_likely_feature_groups": len(results),
        "counts": counts,
    }
    if dry_run:
        summary["sample"] = results[:30]
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
