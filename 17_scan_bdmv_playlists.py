#!/usr/bin/env python3
"""Scan Blu-ray BDMV playlists and write a conservative remux plan."""

from __future__ import annotations

import argparse
import csv
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


WORKDIR = Path(__file__).resolve().parent
LOCAL_MKVMERGE = WORKDIR / "tools" / "MKVToolNix.app" / "Contents" / "MacOS" / "mkvmerge"


@dataclass
class PlaylistInfo:
    playlist: Path
    duration_seconds: float
    size_bytes: int
    stream_files: list[str]
    tracks: list[dict]
    chapters: int
    repeated_stream: bool
    role: str = ""


def find_mkvmerge() -> str:
    env = os.environ.get("MKVMERGE")
    if env:
        return env
    if LOCAL_MKVMERGE.exists():
        return str(LOCAL_MKVMERGE)
    return "mkvmerge"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect a Blu-ray BDMV folder and produce a no-reencode MKV remux plan."
    )
    parser.add_argument("disc", help="Blu-ray root folder, BDMV folder, or PLAYLIST folder")
    parser.add_argument(
        "--out-dir",
        default=str(WORKDIR / "bdmv-plan"),
        help="Where to write the TSV and Markdown reports.",
    )
    parser.add_argument(
        "--min-extra-minutes",
        type=float,
        default=2.0,
        help="Shortest playlist duration to keep as a possible extra.",
    )
    parser.add_argument(
        "--feature-min-minutes",
        type=float,
        default=60.0,
        help="Minimum duration for an automatic feature candidate.",
    )
    return parser.parse_args()


def playlist_dir_for(path: Path) -> Path:
    if path.name == "PLAYLIST":
        return path
    if path.name == "BDMV":
        return path / "PLAYLIST"
    return path / "BDMV" / "PLAYLIST"


def inspect_playlist(mkvmerge: str, playlist: Path) -> PlaylistInfo | None:
    proc = subprocess.run(
        [mkvmerge, "-J", str(playlist)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        print(f"WARN: could not inspect {playlist}: {proc.stderr.strip()}", file=sys.stderr)
        return None

    doc = json.loads(proc.stdout)
    props = doc.get("container", {}).get("properties", {})
    stream_files = [str(p) for p in props.get("playlist_file", [])]
    unique_streams = set(stream_files)
    chapters = sum(int(ch.get("num_entries", 0)) for ch in doc.get("chapters", []))
    return PlaylistInfo(
        playlist=playlist,
        duration_seconds=float(props.get("playlist_duration", 0)) / 1_000_000_000,
        size_bytes=int(props.get("playlist_size", 0)),
        stream_files=stream_files,
        tracks=doc.get("tracks", []),
        chapters=chapters,
        repeated_stream=len(stream_files) > 1 and len(unique_streams) < len(stream_files),
    )


def duration_label(seconds: float) -> str:
    total = int(round(seconds))
    hours, rest = divmod(total, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def size_label(size: int) -> str:
    return f"{size / 1024 / 1024 / 1024:.2f} GiB"


def track_summary(tracks: list[dict]) -> tuple[str, str, str]:
    audio: list[str] = []
    subtitles: list[str] = []
    video: list[str] = []
    for track in tracks:
        props = track.get("properties", {})
        lang = props.get("language", "und")
        codec = track.get("codec", "unknown")
        if track.get("type") == "audio":
            channels = props.get("audio_channels")
            suffix = f" {channels}ch" if channels else ""
            audio.append(f"{lang} {codec}{suffix}")
        elif track.get("type") == "subtitles":
            subtitles.append(f"{lang} {codec}")
        elif track.get("type") == "video":
            dims = props.get("pixel_dimensions", "")
            video.append(f"{codec} {dims}".strip())
    return "; ".join(video), "; ".join(audio), "; ".join(subtitles)


def classify(playlists: list[PlaylistInfo], feature_min_seconds: float, extra_min_seconds: float) -> None:
    sane = [p for p in playlists if not p.repeated_stream and p.duration_seconds > 0]
    largest = max(sane, key=lambda p: (p.duration_seconds, p.size_bytes), default=None)
    for p in playlists:
        if p.repeated_stream:
            p.role = "REVIEW_REPEATED_STREAM"
        elif (
            largest is not None
            and p is not largest
            and abs(p.duration_seconds - largest.duration_seconds) < 1
            and p.size_bytes == largest.size_bytes
            and p.stream_files == largest.stream_files
        ):
            p.role = "DUPLICATE_OF_FEATURE"
        elif p is largest and p.duration_seconds >= feature_min_seconds:
            p.role = "FEATURE"
        elif p.duration_seconds >= extra_min_seconds:
            p.role = "EXTRA_CANDIDATE"
        else:
            p.role = "TINY_SKIP"


def suggested_output(disc_root: Path, info: PlaylistInfo) -> Path:
    stem = disc_root.name
    if info.role == "FEATURE":
        return disc_root.parent / f"{stem}.mkv"
    return disc_root / "Extras" / f"{stem}.{info.playlist.stem}.mkv"


def write_reports(out_dir: Path, disc_root: Path, playlists: list[PlaylistInfo], mkvmerge: str) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in disc_root.name)[:80]
    tsv_path = out_dir / f"bdmv_playlists_{safe_name}_{stamp}.tsv"
    md_path = out_dir / f"bdmv_playlists_{safe_name}_{stamp}.md"

    with tsv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(
            [
                "role",
                "playlist",
                "duration",
                "size",
                "chapters",
                "streams",
                "video",
                "audio",
                "subtitles",
                "suggested_output",
            ]
        )
        for info in playlists:
            video, audio, subtitles = track_summary(info.tracks)
            writer.writerow(
                [
                    info.role,
                    str(info.playlist),
                    duration_label(info.duration_seconds),
                    size_label(info.size_bytes),
                    info.chapters,
                    ", ".join(Path(s).name for s in info.stream_files),
                    video,
                    audio,
                    subtitles,
                    str(suggested_output(disc_root, info)),
                ]
            )

    lines = [
        f"# BDMV playlist scan: {disc_root.name}",
        "",
        f"- Disc: `{disc_root}`",
        f"- Playlists inspected: `{len(playlists)}`",
        "",
        "## Candidates",
        "",
        "| Role | Playlist | Duration | Size | Chapters | Streams | Audio | Subtitles |",
        "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for info in playlists:
        _, audio, subtitles = track_summary(info.tracks)
        streams = ", ".join(Path(s).name for s in info.stream_files)
        lines.append(
            "| "
            + " | ".join(
                [
                    info.role,
                    info.playlist.name,
                    duration_label(info.duration_seconds),
                    size_label(info.size_bytes),
                    str(info.chapters),
                    streams,
                    audio or "-",
                    subtitles or "-",
                ]
            )
            + " |"
        )

    lines.extend(["", "## Suggested Commands", ""])
    for info in playlists:
        if info.role not in {"FEATURE", "EXTRA_CANDIDATE"}:
            continue
        output = suggested_output(disc_root, info)
        cmd = [mkvmerge, "-o", str(output), str(info.playlist)]
        lines.append(f"- `{info.role}` `{info.playlist.name}`")
        lines.append("")
        lines.append("```bash")
        lines.append(shlex.join(cmd))
        lines.append("```")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return tsv_path, md_path


def main() -> int:
    args = parse_args()
    disc_arg = Path(args.disc).expanduser()
    playlist_dir = playlist_dir_for(disc_arg)
    if not playlist_dir.is_dir():
        print(f"ERROR: PLAYLIST folder not found: {playlist_dir}", file=sys.stderr)
        return 1

    disc_root = playlist_dir.parent.parent
    mkvmerge = find_mkvmerge()
    playlists: list[PlaylistInfo] = []
    for playlist in sorted(playlist_dir.glob("*.mpls")):
        info = inspect_playlist(mkvmerge, playlist)
        if info:
            playlists.append(info)

    classify(
        playlists,
        feature_min_seconds=args.feature_min_minutes * 60,
        extra_min_seconds=args.min_extra_minutes * 60,
    )
    playlists.sort(key=lambda p: (p.role != "FEATURE", -p.duration_seconds, p.playlist.name))
    tsv_path, md_path = write_reports(Path(args.out_dir), disc_root, playlists, mkvmerge)
    print(f"Wrote TSV: {tsv_path}")
    print(f"Wrote report: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
