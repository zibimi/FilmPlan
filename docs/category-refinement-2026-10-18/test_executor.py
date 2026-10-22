"""所有写入仅发生在 TemporaryDirectory；不触碰 NAS。"""
import hashlib
import importlib.util
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('executor',Path(__file__).with_name('执行分类.py'))
executor=importlib.util.module_from_spec(spec);spec.loader.exec_module(executor)

class ExecutorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name)
        self.root=self.base/'NAS';self.root.mkdir()
        for c in executor.CATS: (self.root/c).mkdir()
        self.src=self.root/'青春·儿童'/'影片目录';self.src.mkdir()
        (self.src/'正片.mkv').write_bytes(b'video')
        (self.src/'字幕.srt').write_bytes(b'subtitle')
        (self.src/'花絮').mkdir();(self.src/'花絮'/'花絮.mkv').write_bytes(b'extra')
        self.dst=self.root/'儿童'/self.src.name
        self.row={'id':'test-1','original_path':str(self.src),'proposed_path':str(self.dst),
          'category':'青春·儿童','name':self.src.name,'status':'planned','manifest':[]}
        for p in [self.src]+sorted(self.src.rglob('*')):
            s=p.stat();self.row['manifest'].append({'rel':'.' if p==self.src else str(p.relative_to(self.src)),
             'kind':'dir' if p.is_dir() else 'file','size':s.st_size,'mtime_ns':s.st_mtime_ns})
        self.plan={'root':str(self.root),'categories':sorted(executor.CATS),'items':[self.row]}
        self.path=self.base/'分类计划.json';self.save()
        self.rootpatch=patch.object(executor,'ROOT',self.root);self.rootpatch.start()
        self.mountpatch=patch.object(executor.os.path,'ismount',return_value=True);self.mountpatch.start()
        self.output=redirect_stdout(io.StringIO());self.output.__enter__()

    def save(self):
        self.path.write_text(json.dumps(self.plan));self.digest=hashlib.sha256(self.path.read_bytes()).hexdigest()

    def tearDown(self):
        self.output.__exit__(None,None,None);self.rootpatch.stop();self.mountpatch.stop();self.temp.cleanup()

    def test_dry_run_does_not_write(self):
        before=set(self.base.rglob('*'));executor.run(self.path)
        self.assertEqual(before,set(self.base.rglob('*')));self.assertTrue(self.src.exists())

    def test_execute_preserves_companions_and_resumes(self):
        executor.run(self.path,True,self.digest)
        self.assertFalse(self.src.exists());self.assertEqual((self.dst/'字幕.srt').read_bytes(),b'subtitle')
        self.assertEqual((self.dst/'花絮'/'花絮.mkv').read_bytes(),b'extra')
        executor.run(self.path,True,self.digest)
        summary=json.loads((self.base/'执行结果.json').read_text())
        self.assertEqual(summary['executed_this_run'],0);self.assertEqual(summary['already_done_before_run'],1)

    def test_target_collision_aborts_before_move(self):
        self.dst.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError,'目标已存在'): executor.run(self.path,True,self.digest)
        self.assertTrue(self.src.exists());self.assertFalse((self.base/'执行日志.jsonl').exists())

    def test_source_changed_aborts(self):
        (self.src/'正片.mkv').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'已变化'): executor.run(self.path,True,self.digest)
        self.assertFalse(self.dst.exists())

    def test_wrong_digest_aborts(self):
        with self.assertRaisesRegex(ValueError,'sha256'): executor.run(self.path,True,'wrong')

    def test_new_item_aborts(self):
        (self.root/'青春·儿童'/'新增.mkv').write_bytes(b'new')
        with self.assertRaisesRegex(ValueError,'目录条目变化'): executor.run(self.path,True,self.digest)

    def test_target_symlink_aborts(self):
        elsewhere=self.base/'elsewhere';elsewhere.mkdir();self.dst.parent.symlink_to(elsewhere,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'符号链接'): executor.run(self.path,True,self.digest)

    def test_interrupted_after_move_recovers_from_intent(self):
        executor.append_log(self.base/'执行日志.jsonl',self.digest,self.row,'intent')
        self.dst.parent.mkdir();self.src.rename(self.dst)
        executor.run(self.path,True,self.digest)
        self.assertTrue(self.dst.exists());self.assertFalse(self.src.exists())

    def test_absent_source_without_log_is_not_already_done(self):
        self.dst.parent.mkdir();self.src.rename(self.dst)
        with self.assertRaisesRegex(ValueError,'无匹配执行记录'): executor.run(self.path,True,self.digest)

    def test_review_never_moves(self):
        self.row.update(status='review',proposed_path=None);self.save()
        executor.run(self.path,True,self.digest)
        self.assertTrue(self.src.exists());self.assertFalse(self.dst.exists())

if __name__=='__main__': unittest.main()
