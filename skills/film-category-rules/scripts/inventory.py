#!/usr/bin/env python3
"""Read-only scoped NAS inventory. Writes a NEW local JSON, never media."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

VIDEO = {'.mkv','.mp4','.avi','.rmvb','.rm','.mov','.m4v','.mpg','.mpeg','.wmv','.flv','.ts','.m2ts','.vob','.webm','.iso'}
SUBTITLE = {'.srt','.ass','.ssa','.sub','.idx','.sup','.vtt'}
EXCLUDED = [('华语世界','禁'), ('合集','蚂蚁')]

def blocked(parts):
    return any(p.startswith('.') or p == '#recycle' for p in parts) or any(tuple(parts[:len(x)]) == x for x in EXCLUDED)

def snapshot(library, source):
    library, source = Path(os.path.abspath(library)), Path(os.path.abspath(source))
    if library.resolve() != library or source.resolve() != source:
        raise ValueError('源或库路径包含符号链接')
    if not library.is_dir() or not os.path.ismount(library):
        raise ValueError('分类库未挂载，不能当成空库')
    relative = source.relative_to(library)
    if blocked(relative.parts):
        raise ValueError('源位于排除范围')
    if not source.is_dir():
        raise ValueError('源目录不存在')
    errors, skipped, files = [], [], []
    categories = sorted(p.name for p in library.iterdir() if not p.is_symlink() and p.is_dir() and not blocked((p.name,)))
    def onerror(exc):
        errors.append({'path':exc.filename, 'error':str(exc)})
    for base, dirs, names in os.walk(source, followlinks=False, onerror=onerror):
        keep = []
        for name in sorted(dirs):
            p = Path(base)/name
            if p.is_symlink() or blocked(p.relative_to(library).parts):
                skipped.append(str(p))
            else:
                keep.append(name)
        dirs[:] = keep
        for name in sorted(names):
            p = Path(base)/name
            if p.is_symlink() or blocked(p.relative_to(library).parts):
                skipped.append(str(p)); continue
            try:
                s = p.lstat()
                if not stat.S_ISREG(s.st_mode):
                    skipped.append(str(p)); continue
                suffix = p.suffix.lower()
                files.append({'route_id':hashlib.sha256(str(p).encode()).hexdigest()[:20],
                    'original_path':str(p), 'relative_path':str(p.relative_to(source)),
                    'name':p.name, 'size':s.st_size, 'mtime_ns':s.st_mtime_ns,
                    'extension':suffix, 'resource_hint':'video' if suffix in VIDEO else 'subtitle' if suffix in SUBTITLE else 'other'})
            except OSError as exc:
                onerror(exc)
    files.sort(key=lambda x:x['original_path'])
    return {'schema_version':1, 'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'library_root':str(library), 'source_root':str(source), 'categories':categories,
        'complete':not errors, 'errors':errors, 'skipped':skipped, 'files':files}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--library-root', default='/Volumes/分类')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output).expanduser().resolve()
    # The helper intentionally writes only outside mounted shares and the scanned tree.
    library = Path(args.library_root).resolve()
    if output.is_relative_to(Path('/Volumes')) or output.is_relative_to(library):
        parser.error('输出必须在本地工作区，不能在 NAS/被扫描库内')
    if output.exists():
        parser.error('输出已存在；请使用新的批次文件名')
    try:
        result = snapshot(args.library_root, args.source)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    with output.open('x', encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({'output':str(output),'files':len(result['files']),
        'complete':result['complete'],'errors':len(result['errors'])},ensure_ascii=False))
    return 0 if result['complete'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
