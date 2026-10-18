#!/usr/bin/env python3
"""离线固定计划执行器。默认仅预演；不根据片名自动分类。"""
import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from datetime import datetime

BASE=Path(__file__).resolve().parent
ROOT=Path('/Volumes/分类')
DESTS={'儿童','青春','科幻','奇幻','传记','一段历史','犯罪','动作','惊悚','灾难'}
CATS={'青春·儿童','科幻·奇幻','传记·一段历史','惊悚·犯罪·动作','冒险·灾难'}

def fingerprint(path):
    """目录自身时间/大小会随 SMB 实现变化，不用于数据核对。"""
    out=[]
    for p in [path]+(sorted(path.rglob('*')) if path.is_dir() else []):
        s=p.lstat()
        if stat.S_ISLNK(s.st_mode): raise ValueError(f'禁止符号链接：{p}')
        if not (stat.S_ISDIR(s.st_mode) or stat.S_ISREG(s.st_mode)):
            raise ValueError(f'不是常规文件或目录：{p}')
        out.append({'rel':'.' if p==path else str(p.relative_to(path)),
                    'kind':'dir' if p.is_dir() else 'file', 'size':s.st_size,'mtime_ns':s.st_mtime_ns})
    return normalize(out)

def normalize(manifest):
    return sorted((x['rel'],x['kind'],x['size'] if x['kind']=='file' else 0,
                   x['mtime_ns'] if x['kind']=='file' else 0) for x in manifest)

def safe_path(path):
    if path.is_absolute() is False or '..' in path.parts: raise ValueError(f'非法路径：{path}')
    path.relative_to(ROOT)
    current=ROOT
    for part in path.relative_to(ROOT).parts:
        current=current/part
        if current.is_symlink(): raise ValueError(f'路径含符号链接：{current}')
    if ROOT.is_symlink(): raise ValueError('根目录是符号链接')

def read_log(path,digest):
    events=[]
    if path.exists():
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            event=json.loads(line)
            if event.get('plan_sha256')==digest: events.append(event)
    return events

def validate(plan,digest,events):
    if plan['root']!=str(ROOT) or set(plan['categories'])!=CATS: raise ValueError('计划根目录或范围不符')
    if not ROOT.is_dir() or not os.path.ismount(ROOT): raise ValueError('分类根目录未挂载')
    safe_path(ROOT)
    intents={e['id'] for e in events if e['event']=='intent'}
    sources=set();targets=set();ids=set();todo=[];done=[]
    for row in plan['items']:
        if row['id'] in ids: raise ValueError('重复 ID')
        ids.add(row['id'])
        src=Path(row['original_path']);safe_path(src)
        if src.parent.parent!=ROOT or src.parent.name not in CATS or src.name!=row['name'] or src.parent.name!=row['category']:
            raise ValueError(f'来源越界：{src}')
        if src in sources: raise ValueError('重复来源')
        sources.add(src)
        if row['status'] not in {'planned','review','ignore'}: raise ValueError('未知状态')
        if row['status']!='planned':
            if row['proposed_path'] is not None: raise ValueError('非拟执行项不应有目标')
            continue
        dst=Path(row['proposed_path']);safe_path(dst)
        if dst.parent.parent!=ROOT or dst.parent.name not in DESTS or dst.name!=src.name:
            raise ValueError(f'目标越界或改名：{dst}')
        if dst in targets: raise ValueError('重复目标')
        targets.add(dst)
        expected=normalize(row['manifest'])
        if not src.exists():
            if row['id'] in intents and dst.exists() and fingerprint(dst)==expected:
                done.append(row);continue
            raise ValueError(f'来源缺失且无匹配执行记录：{src}')
        if dst.exists(): raise ValueError(f'目标已存在：{dst}')
        if dst.parent.exists() and not dst.parent.is_dir(): raise ValueError(f'目标父路径不是目录：{dst.parent}')
        if fingerprint(src)!=expected: raise ValueError(f'来源内容清单/大小/时间已变化：{src}')
        if src.stat().st_dev!=ROOT.stat().st_dev: raise ValueError(f'来源不是同一卷：{src}')
        if dst.parent.exists() and dst.parent.stat().st_dev!=ROOT.stat().st_dev: raise ValueError('目标不是同一卷')
        todo.append(row)
    # 扫描后新增/缺失的非隐藏条目均使整个批次停下；已执行项由日志和目标读回证明。
    moved={Path(r['original_path']) for r in done}
    for cat in CATS:
        parent=ROOT/cat
        safe_path(parent)
        if not parent.is_dir(): raise ValueError(f'原目录缺失：{parent}')
        actual={p for p in parent.iterdir() if not p.name.startswith('.')}
        expected={Path(r['original_path']) for r in plan['items'] if r['category']==cat and not r['name'].startswith('.')} - moved
        if actual!=expected: raise ValueError(f'目录条目变化：{cat}；新增 {actual-expected}；缺失 {expected-actual}')
    return todo,done

def append_log(path,digest,row,event,**extra):
    with path.open('a') as f:
        f.write(json.dumps({'time':datetime.now().astimezone().isoformat(),'plan_sha256':digest,
            'id':row['id'],'event':event,'source':row['original_path'],'target':row['proposed_path'],**extra},ensure_ascii=False)+'\n')
        f.flush();os.fsync(f.fileno())

def run(plan_path,execute=False,approved_hash=None):
    data=plan_path.read_bytes();digest=hashlib.sha256(data).hexdigest();plan=json.loads(data)
    if execute and approved_hash!=digest: raise ValueError('必须提供与当前计划完全匹配的 --plan-sha256')
    log=plan_path.with_name('执行日志.jsonl')
    todo,done=validate(plan,digest,read_log(log,digest))
    skipped=sum(r['status']!='planned' for r in plan['items'])
    print(f'预检通过：待移动 {len(todo)}；已执行且核对通过 {len(done)}；跳过 {skipped}；计划 {digest}')
    if not execute:
        for row in todo: print(f"{row['id']} {row['original_path']} → {row['proposed_path']}")
        print('仅预演；没有修改 NAS 或执行日志。');return
    for row in todo:
        src=Path(row['original_path']);dst=Path(row['proposed_path'])
        try:
            safe_path(src);safe_path(dst)
            if not src.exists() or dst.exists() or fingerprint(src)!=normalize(row['manifest']):
                raise ValueError('逐项执行前检查失败')
            dst.parent.mkdir(exist_ok=True)
            safe_path(dst)
            if dst.parent.stat().st_dev!=src.stat().st_dev: raise ValueError('禁止跨卷移动')
            append_log(log,digest,row,'intent')
            subprocess.run(['/bin/mv','-n',str(src),str(dst)],check=True)
            if src.exists() or not dst.exists() or fingerprint(dst)!=normalize(row['manifest']):
                raise ValueError('移动后核对失败')
            append_log(log,digest,row,'executed')
            print(f"已执行 {row['id']}",flush=True)
        except Exception as exc:
            append_log(log,digest,row,'failed',error=str(exc))
            raise
    remaining,verified=validate(plan,digest,read_log(log,digest))
    if remaining: raise ValueError('最终核验仍有未执行条目')
    summary={'plan_sha256':digest,'executed_this_run':len(todo),'already_done_before_run':len(done),
             'verified_total':len(verified),'skipped':skipped,'conflicts':0,'failed':0}
    plan_path.with_name('执行结果.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--plan-sha256')
    parser.add_argument('--report',action='store_true',help='仅从当前 JSON 重生成报告，不重新分类')
    args=parser.parse_args()
    if args.report:
        if args.execute: parser.error('--report 不能与 --execute 同用')
        spec=importlib.util.spec_from_file_location('report',BASE/'生成报告.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.main(False);return
    if args.execute:
        with (BASE/'执行锁').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            run(BASE/'分类计划.json',True,args.plan_sha256)
    else: run(BASE/'分类计划.json')

if __name__=='__main__':
    try: main()
    except Exception as exc: print(f'停止：{exc}',file=sys.stderr);sys.exit(1)
